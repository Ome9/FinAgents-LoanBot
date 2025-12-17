"""Sales Agent - Handles customer engagement and loan negotiation."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
from typing import Dict, Any, List
from config import settings


class SalesAgent:
    """Sales Agent for engaging customers and collecting loan requirements."""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            temperature=0.7,
            google_api_key=settings.gemini_api_key
        )
        
        self.system_prompt = """You are an expert personal loan sales representative for a leading NBFC. 
Your goal is to engage customers in a warm, personalized, and persuasive conversation to help them 
get a personal loan that meets their needs.

Key responsibilities:
1. Greet customers warmly and build rapport
2. Understand their financial needs and loan requirements
3. Ask about desired loan amount, tenure preference, and purpose
4. Highlight benefits of personal loans (quick approval, flexible tenure, competitive rates)
5. Handle objections professionally
6. Create urgency with limited-time offers when appropriate
7. Collect necessary information: loan amount, preferred tenure
8. Be conversational, empathetic, and avoid being pushy

Conversation style:
- Use the customer's name when available
- Be friendly but professional
- Use simple language, avoid jargon
- Show genuine interest in helping
- Mention personalized offers when available
- Keep responses concise (2-4 sentences typically)

Important: You are in the sales/engagement phase. Once you have collected:
- Desired loan amount
- Preferred tenure (in months)
- Confirmed customer interest

Indicate that you're ready to move forward by saying "COLLECT_COMPLETE" at the end of your response.
"""
    
    async def engage(
        self, 
        customer_data: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        user_message: str,
        pre_approved_offers: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Engage with customer and collect loan requirements.
        
        Args:
            customer_data: Customer information from CRM
            conversation_history: Previous messages
            user_message: Latest message from user
            pre_approved_offers: Available offers for personalization
            
        Returns:
            Agent response with collection status
        """
        # Build context
        context = f"""
Customer Information:
- Name: {customer_data.get('name', 'Valued Customer')}
- City: {customer_data.get('city', 'Unknown')}
- Credit Score: {customer_data.get('credit_score', 'N/A')}
- Pre-approved Limit: ₹{customer_data.get('pre_approved_limit', 0):,}
"""
        
        if pre_approved_offers:
            offers = pre_approved_offers.get('data', {}).get('offers', [])
            if offers:
                context += f"\n- Special Offers Available: Up to ₹{offers[0].get('max_amount', 0):,} at {offers[0].get('interest_rate', 0)}% p.a."
        
        # Check if we have collected required info from history
        loan_amount = None
        tenure = None
        
        for msg in conversation_history:
            if msg['role'] == 'assistant' and 'COLLECT_COMPLETE' in msg['content']:
                # Already collected
                pass
        
        # Build messages - Gemini doesn't support SystemMessage, so we prepend context to first user message
        messages = []
        
        # Add conversation history
        history_added = False
        for i, msg in enumerate(conversation_history[-6:]):  # Last 6 messages for context
            if msg['role'] == 'user':
                # For the first user message, prepend system prompt and context
                if not history_added:
                    full_context = f"{self.system_prompt}\n\n{context}\n\nUser: {msg['content']}"
                    messages.append(HumanMessage(content=full_context))
                    history_added = True
                else:
                    messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                content = msg['content'].replace('COLLECT_COMPLETE', '').strip()
                messages.append(AIMessage(content=content))
        
        # Add current message
        if not history_added:
            # First message in conversation
            full_context = f"{self.system_prompt}\n\n{context}\n\nUser: {user_message}"
            messages.append(HumanMessage(content=full_context))
        else:
            messages.append(HumanMessage(content=user_message))
        
        # Get response
        response = await self.llm.ainvoke(messages)
        
        # Check if collection is complete
        agent_response = response.content
        collection_complete = 'COLLECT_COMPLETE' in agent_response
        
        # Clean response
        display_response = agent_response.replace('COLLECT_COMPLETE', '').strip()
        
        # Try to extract loan details from conversation
        extracted_data = self._extract_loan_details(conversation_history + [
            {'role': 'user', 'content': user_message},
            {'role': 'assistant', 'content': agent_response}
        ])
        
        return {
            "response": display_response,
            "collection_complete": collection_complete,
            "extracted_data": extracted_data,
            "next_agent": "verification" if collection_complete else None
        }
    
    def _extract_loan_details(self, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Extract loan amount and tenure from conversation."""
        import re
        
        loan_amount = None
        tenure = None
        
        # Combine all messages
        conversation_text = " ".join([msg.get('content', '') for msg in conversation_history])
        
        # Extract loan amount (looking for numbers with lakh, lakhs, or large numbers)
        amount_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs)',
            r'₹\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            r'Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            r'loan\s+(?:of|amount)?\s*(?:of)?\s*(\d+(?:,\d+)*)'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, conversation_text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                amount_val = float(amount_str)
                
                # Convert lakhs to actual number
                if 'lakh' in pattern:
                    amount_val *= 100000
                
                # If amount seems reasonable for a personal loan
                if 10000 <= amount_val <= 50000000:
                    loan_amount = int(amount_val)
                    break
        
        # Extract tenure (looking for months or years)
        tenure_patterns = [
            r'(\d+)\s*(?:months?|mnths?)',
            r'(\d+)\s*(?:years?|yrs?)',
        ]
        
        for pattern in tenure_patterns:
            match = re.search(pattern, conversation_text, re.IGNORECASE)
            if match:
                tenure_val = int(match.group(1))
                
                # Convert years to months if needed
                if 'year' in pattern or 'yr' in pattern:
                    tenure_val *= 12
                
                # Reasonable tenure range
                if 6 <= tenure_val <= 84:
                    tenure = tenure_val
                    break
        
        return {
            "loan_amount": loan_amount,
            "tenure_months": tenure,
            "ready_for_next_stage": loan_amount is not None and tenure is not None
        }
