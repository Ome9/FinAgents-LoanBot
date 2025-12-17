"""Master Agent - Orchestrates the entire loan processing workflow."""
from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from agents.perplexity_sales_agent import PerplexitySalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_letter_generator import SanctionLetterGenerator
import httpx
from config import settings


# Define the state structure
class AgentState(TypedDict):
    """State shared across all agents."""
    messages: List[Dict[str, str]]
    customer_id: str
    customer_data: Dict[str, Any]
    current_stage: str
    loan_amount: float
    tenure_months: int
    pre_approved_offers: Dict[str, Any]
    verification_complete: bool
    underwriting_result: Dict[str, Any]
    requires_salary_slip: bool
    salary_slip_provided: bool
    stated_salary: float
    sanction_letter_path: str
    conversation_complete: bool
    error: str
    quick_replies: List[Dict[str, str]]
    awaiting_confirmation: bool


class MasterAgent:
    """Master Agent that orchestrates all worker agents."""
    
    def __init__(self):
        self.sales_agent = PerplexitySalesAgent()
        self.verification_agent = VerificationAgent()
        self.underwriting_agent = UnderwritingAgent()
        self.sanction_generator = SanctionLetterGenerator()
        self.base_url = f"http://localhost:{settings.api_port}"
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow - simple single-node execution for chat."""
        workflow = StateGraph(AgentState)
        
        # Add single router node that decides which agent to call
        workflow.add_node("router", self._router_node)
        
        # Simple flow: always start at router, router decides what to do, then end
        workflow.set_entry_point("router")
        workflow.add_edge("router", END)
        
        return workflow.compile()
    
    async def _router_node(self, state: AgentState) -> AgentState:
        """Router node - calls appropriate agent based on current stage."""
        current_stage = state.get("current_stage", "sales")
        latest_message = state["messages"][-1]["content"].lower() if state["messages"] else ""
        
        # Handle confirmation states
        if current_stage == "awaiting_verification_confirmation":
            if "proceed" in latest_message or "yes" in latest_message:
                state["current_stage"] = "verification"
                state["awaiting_confirmation"] = False
                state["quick_replies"] = []
                return await self._verification_node(state)
            elif "change" in latest_message or "no" in latest_message:
                state["current_stage"] = "sales"
                state["awaiting_confirmation"] = False
                state["quick_replies"] = []
                msg = {"role": "assistant", "content": "No problem! What would you like to change? The loan amount or tenure?"}
                state["messages"] = state["messages"] + [msg]
                return state
        
        elif current_stage == "awaiting_underwriting_confirmation":
            if "proceed" in latest_message or "yes" in latest_message or "correct" in latest_message:
                state["current_stage"] = "underwriting"
                state["awaiting_confirmation"] = False
                state["quick_replies"] = []
                return await self._underwriting_node(state)
            else:
                state["current_stage"] = "sales"
                state["awaiting_confirmation"] = False
                state["quick_replies"] = []
                msg = {"role": "assistant", "content": "Let me know what needs to be corrected."}
                state["messages"] = state["messages"] + [msg]
                return state
        
        elif current_stage == "awaiting_sanction_confirmation":
            if "generate" in latest_message or "sanction" in latest_message or "yes" in latest_message:
                state["current_stage"] = "sanction_letter"
                state["awaiting_confirmation"] = False
                state["quick_replies"] = []
                return await self._sanction_letter_node(state)
            elif "email" in latest_message or "later" in latest_message:
                state["awaiting_confirmation"] = False
                state["current_stage"] = "end"
                state["conversation_complete"] = True
                state["quick_replies"] = []
                email_msg = {
                    "role": "assistant",
                    "content": f"📧 **Email Confirmation**\n\nPerfect! We'll send your sanction letter to **{state['customer_data'].get('email', 'your registered email')}** within 24 hours.\n\nYou'll also receive:\n✅ Loan agreement documents\n✅ Repayment schedule\n✅ Next steps for documentation\n\nThank you for choosing Tata Capital! 🎉"
                }
                state["messages"] = state["messages"] + [email_msg]
                return state
        
        # Route to appropriate agent
        if current_stage == "sales":
            return await self._sales_node(state)
        elif current_stage == "verification":
            return await self._verification_node(state)
        elif current_stage == "underwriting":
            return await self._underwriting_node(state)
        elif current_stage == "sanction_letter":
            return await self._sanction_letter_node(state)
        else:
            # Default to sales
            return await self._sales_node(state)
    
    async def _sales_node(self, state: AgentState) -> AgentState:
        """Sales agent node - handles customer engagement."""
        latest_message = state["messages"][-1]["content"] if state["messages"] else ""
        
        # Get pre-approved offers if not already fetched
        if not state.get("pre_approved_offers") and state.get("customer_id"):
            state["pre_approved_offers"] = await self._fetch_offers(state["customer_id"])
        
        # Call sales agent
        result = await self.sales_agent.engage(
            customer_data=state.get("customer_data", {}),
            conversation_history=state["messages"],
            user_message=latest_message,
            pre_approved_offers=state.get("pre_approved_offers")
        )
        
        # Update state - only add if not already added
        assistant_message = {
            "role": "assistant",
            "content": result["response"]
        }
        if not state["messages"] or state["messages"][-1] != assistant_message:
            state["messages"] = state["messages"] + [assistant_message]
        
        # Extract loan details if available
        if result.get("extracted_data", {}).get("loan_amount"):
            state["loan_amount"] = result["extracted_data"]["loan_amount"]
        if result.get("extracted_data", {}).get("tenure_months"):
            state["tenure_months"] = result["extracted_data"]["tenure_months"]
        
        # Check if ready to move to next stage
        # Only progress if we have both loan amount and tenure
        if result.get("collection_complete") and state.get("loan_amount") and state.get("tenure_months"):
            # Ask for confirmation before proceeding to verification
            confirmation_msg = {
                "role": "assistant",
                "content": f"Perfect! Let me summarize your loan request:\n\n💰 **Loan Amount:** ₹{state['loan_amount']:,.0f}\n📅 **Tenure:** {state['tenure_months']} months\n\nShall I proceed with verifying your details and processing your application?"
            }
            state["messages"] = state["messages"] + [confirmation_msg]
            state["quick_replies"] = [
                {"label": "✅ Yes, Proceed", "value": "proceed_verification"},
                {"label": "✏️ Change Details", "value": "change_details"}
            ]
            state["current_stage"] = "awaiting_verification_confirmation"
            state["awaiting_confirmation"] = True
        else:
            # Stay in sales stage - wait for more user input
            state["current_stage"] = "sales"
            state["quick_replies"] = []
        
        return state
    
    async def _verification_node(self, state: AgentState) -> AgentState:
        """Verification agent node - validates customer details."""
        customer_id = state.get("customer_id")
        
        if not customer_id:
            state["messages"] = state["messages"] + [{
                "role": "assistant",
                "content": "I need your customer ID to proceed. Could you please provide it?"
            }]
            state["current_stage"] = "sales"
            return state
        
        # Perform verification
        result = await self.verification_agent.quick_verify(customer_id)
        
        verification_message = {
            "role": "assistant",
            "content": result["message"]
        }
        state["messages"] = state["messages"] + [verification_message]
        
        if result["verified"]:
            state["verification_complete"] = True
            state["customer_data"] = result.get("customer_data", {})
            
            # Ask user to confirm details before underwriting
            customer = state["customer_data"]
            confirmation_msg = {
                "role": "assistant",
                "content": f"Great! I've verified your details:\n\n👤 **Name:** {customer.get('name', 'N/A')}\n📧 **Email:** {customer.get('email', 'N/A')}\n📱 **Phone:** {customer.get('phone', 'N/A')}\n💳 **Credit Score:** {customer.get('credit_score', 'N/A')}\n\nAre these details correct? Shall I proceed with the loan assessment?"
            }
            state["messages"] = state["messages"] + [confirmation_msg]
            state["quick_replies"] = [
                {"label": "✅ Yes, All Correct", "value": "proceed_underwriting"},
                {"label": "❌ Update Details", "value": "update_details"}
            ]
            state["current_stage"] = "awaiting_underwriting_confirmation"
            state["awaiting_confirmation"] = True
        else:
            state["verification_complete"] = False
            state["current_stage"] = "sales"
            state["quick_replies"] = []
        
        return state
    
    async def _underwriting_node(self, state: AgentState) -> AgentState:
        """Underwriting agent node - assesses loan eligibility."""
        # Validate required data is present
        if not state.get("loan_amount") or not state.get("tenure_months"):
            error_msg = {
                "role": "assistant",
                "content": "⚠️ Missing loan details. Please tell me the loan amount and tenure you need."
            }
            state["messages"] = state["messages"] + [error_msg]
            state["current_stage"] = "sales"
            return state
        
        if not state.get("customer_data"):
            error_msg = {
                "role": "assistant",
                "content": "⚠️ Customer verification incomplete. Let me verify your details first."
            }
            state["messages"] = state["messages"] + [error_msg]
            state["current_stage"] = "verification"
            return state
        
        result = await self.underwriting_agent.assess_eligibility(
            customer_id=state["customer_id"],
            loan_amount=state["loan_amount"],
            tenure_months=state["tenure_months"],
            customer_data=state["customer_data"],
            salary_slip_provided=state.get("salary_slip_provided", False),
            stated_salary=state.get("stated_salary")
        )
        
        underwriting_message = {
            "role": "assistant",
            "content": result["message"]
        }
        state["messages"] = state["messages"] + [underwriting_message]
        
        state["underwriting_result"] = result
        state["quick_replies"] = []
        
        if result.get("approved"):
            # Ask for confirmation before generating sanction letter
            approval_msg = {
                "role": "assistant",
                "content": f"🎉 **Congratulations!** Your loan has been approved!\n\nWould you like me to generate your official sanction letter now?"
            }
            state["messages"] = state["messages"] + [approval_msg]
            state["quick_replies"] = [
                {"label": "📄 Generate Sanction Letter", "value": "generate_sanction"},
                {"label": "📧 Email Me Later", "value": "email_later"}
            ]
            state["current_stage"] = "awaiting_sanction_confirmation"
            state["awaiting_confirmation"] = True
        elif result.get("requires_salary_slip"):
            state["requires_salary_slip"] = True
            state["current_stage"] = "sales"
        else:
            state["current_stage"] = "sales"
        
        return state
    
    async def _sanction_letter_node(self, state: AgentState) -> AgentState:
        """Sanction letter generator node - creates PDF approval document."""
        result = await self.sanction_generator.generate_sanction_letter(
            customer_data=state["customer_data"],
            loan_details=state["underwriting_result"]["loan_details"]
        )
        
        sanction_message = {
            "role": "assistant",
            "content": result["message"]
        }
        state["messages"] = state["messages"] + [sanction_message]
        
        if result["success"]:
            state["sanction_letter_path"] = result.get("file_path", "")
            state["conversation_complete"] = True
        
        state["current_stage"] = "end"
        
        return state
    
    async def _fetch_offers(self, customer_id: str) -> Dict[str, Any]:
        """Fetch pre-approved offers for customer."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/offers/preapproved/{customer_id}"
                )
                if response.status_code == 200:
                    return response.json()
        except:
            pass
        return {}
    
    async def process_message(
        self,
        message: str,
        session_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a user message through the workflow.
        
        Args:
            message: User's message
            session_state: Current session state
            
        Returns:
            Updated state with agent responses
        """
        # Initialize state if new session
        if not session_state:
            session_state = {
                "messages": [],
                "customer_id": "",
                "customer_data": {},
                "current_stage": "sales",
                "loan_amount": 0,
                "tenure_months": 0,
                "pre_approved_offers": {},
                "verification_complete": False,
                "underwriting_result": {},
                "requires_salary_slip": False,
                "salary_slip_provided": False,
                "stated_salary": 0,
                "sanction_letter_path": "",
                "conversation_complete": False,
                "error": "",
                "step_count": 0,
                "max_steps": 10,
                "quick_replies": [],
                "awaiting_confirmation": False
            }
        
        # Add user message
        session_state["messages"] = session_state["messages"] + [{
            "role": "user",
            "content": message
        }]
        
        # Increment step counter and check limit
        session_state["step_count"] = session_state.get("step_count", 0) + 1
        if session_state["step_count"] > session_state.get("max_steps", 10):
            session_state["error"] = "Maximum conversation steps reached. Please start a new conversation."
            session_state["messages"] = session_state["messages"] + [{
                "role": "assistant",
                "content": "I apologize, but we've reached the conversation limit. Please start a new session."
            }]
            return session_state
        
        # Run workflow
        try:
            result = await self.workflow.ainvoke(session_state)
            return result
        except Exception as e:
            session_state["error"] = str(e)
            session_state["messages"] = session_state["messages"] + [{
                "role": "assistant",
                "content": f"I encountered an error: {str(e)}. Please try again."
            }]
            return session_state
    
    async def set_customer_id(self, customer_id: str, session_state: Dict[str, Any]) -> Dict[str, Any]:
        """Set customer ID and fetch initial data."""
        session_state["customer_id"] = customer_id
        
        # Fetch customer data
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/crm/customer/{customer_id}"
                )
                if response.status_code == 200:
                    session_state["customer_data"] = response.json()["data"]
                
                # Fetch offers
                session_state["pre_approved_offers"] = await self._fetch_offers(customer_id)
        except Exception as e:
            session_state["error"] = f"Error fetching customer data: {str(e)}"
        
        return session_state
    
    async def upload_salary_slip(
        self,
        salary_amount: float,
        session_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle salary slip upload and rerun underwriting."""
        session_state["salary_slip_provided"] = True
        session_state["stated_salary"] = salary_amount
        session_state["requires_salary_slip"] = False
        
        # Rerun underwriting
        session_state = await self._underwriting_node(session_state)
        
        # If approved, generate sanction letter
        if session_state.get("underwriting_result", {}).get("approved"):
            session_state = await self._sanction_letter_node(session_state)
        
        return session_state
