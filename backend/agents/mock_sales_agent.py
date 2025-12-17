"""Mock Sales Agent - Handles customer engagement without API calls for demo."""
from typing import Dict, Any, List
import re


class MockSalesAgent:
    """Mock Sales Agent for demo purposes when API quota is exhausted."""
    
    def __init__(self):
        self.conversation_state = {
            "greeting_done": False,
            "asked_amount": False,
            "asked_tenure": False,
            "collected_amount": False,
            "collected_tenure": False
        }
    
    async def engage(
        self, 
        customer_data: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        user_message: str,
        pre_approved_offers: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Engage with customer using predefined responses.
        """
        customer_name = customer_data.get('name', 'Valued Customer')
        pre_approved_limit = customer_data.get('pre_approved_limit', 0)
        
        user_msg_lower = user_message.lower()
        
        # Extract numbers from user message
        extracted_data = self._extract_loan_details(conversation_history + [
            {'role': 'user', 'content': user_message}
        ])
        
        # Initial greeting
        if not self.conversation_state["greeting_done"]:
            self.conversation_state["greeting_done"] = True
            response = f"That's great to hear! I can see you're pre-approved for up to ₹{pre_approved_limit:,}.\n\nTo help you get the best offer, could you tell me:\n1. How much loan amount are you looking for?\n2. What tenure (in months) would be comfortable for you?\n\nFor example, you could say '₹2 lakhs for 24 months' or just tell me the amount first."
            return {
                "response": response,
                "collection_complete": False,
                "extracted_data": extracted_data,
                "next_agent": None
            }
        
        # Check if user provided loan details
        if extracted_data.get('loan_amount') and not self.conversation_state["collected_amount"]:
            self.conversation_state["collected_amount"] = True
            amount = extracted_data['loan_amount']
            
            if extracted_data.get('tenure_months'):
                self.conversation_state["collected_tenure"] = True
                tenure = extracted_data['tenure_months']
                response = f"Perfect! So you're looking for ₹{amount:,} for {tenure} months. Let me verify your details and check the best rates for you. COLLECT_COMPLETE"
                return {
                    "response": response,
                    "collection_complete": True,
                    "extracted_data": extracted_data,
                    "next_agent": "verification"
                }
            else:
                response = f"Great! ₹{amount:,} is within your pre-approved limit. Now, what tenure would you prefer? We offer flexible tenures from 12 to 60 months.\n\nLonger tenure means lower EMIs but slightly higher interest overall. What works best for you?"
                return {
                    "response": response,
                    "collection_complete": False,
                    "extracted_data": extracted_data,
                    "next_agent": None
                }
        
        # User provided tenure after amount
        if self.conversation_state["collected_amount"] and extracted_data.get('tenure_months'):
            self.conversation_state["collected_tenure"] = True
            tenure = extracted_data['tenure_months']
            amount = extracted_data.get('loan_amount', 0)
            response = f"Excellent choice! {tenure} months tenure will give you manageable EMIs. Let me verify your details and process your loan application for ₹{amount:,}. COLLECT_COMPLETE"
            return {
                "response": response,
                "collection_complete": True,
                "extracted_data": extracted_data,
                "next_agent": "verification"
            }
        
        # General helpful response
        if any(word in user_msg_lower for word in ['help', 'confused', 'dont know', "don't know"]):
            response = "No worries! Let me make it simple:\n\n1. **Loan Amount**: How much money do you need? (e.g., ₹2 lakhs, ₹5 lakhs)\n2. **Tenure**: How many months do you want to repay? (e.g., 12 months, 24 months, 36 months)\n\nJust tell me both, and I'll take care of the rest!"
            return {
                "response": response,
                "collection_complete": False,
                "extracted_data": extracted_data,
                "next_agent": None
            }
        
        # Default response
        response = "I'd love to help you get the perfect loan! Could you please tell me:\n1. The loan amount you need (e.g., ₹2 lakhs)\n2. Your preferred repayment tenure in months (e.g., 24 months)\n\nThis will help me find the best offer for you."
        return {
            "response": response,
            "collection_complete": False,
            "extracted_data": extracted_data,
            "next_agent": None
        }
    
    def _extract_loan_details(self, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Extract loan amount and tenure from conversation."""
        loan_amount = None
        tenure = None
        
        # Combine all messages
        conversation_text = " ".join([msg.get('content', '') for msg in conversation_history])
        
        # Extract loan amount (look for patterns like ₹2L, 200000, 2 lakhs, etc.)
        amount_patterns = [
            r'₹\s*(\d+(?:\.\d+)?)\s*(?:l|lakh|lakhs)',  # ₹2 lakhs
            r'(\d+(?:\.\d+)?)\s*(?:l|lakh|lakhs)',      # 2 lakhs
            r'₹\s*(\d+(?:,\d+)*)',                      # ₹200,000
            r'(\d{5,})'                                 # 200000
        ]
        
        for pattern in amount_patterns:
            matches = re.findall(pattern, conversation_text.lower(), re.IGNORECASE)
            if matches:
                # Convert to actual number
                amount_str = matches[-1].replace(',', '')
                try:
                    amount = float(amount_str)
                    # If in lakhs, convert to actual amount
                    if 'lakh' in conversation_text.lower() or 'l' in conversation_text.lower():
                        if amount < 100:  # Likely in lakhs
                            amount = amount * 100000
                    loan_amount = int(amount)
                    break
                except ValueError:
                    continue
        
        # Extract tenure (look for months)
        tenure_patterns = [
            r'(\d+)\s*(?:month|months|mnth|mnths)',
            r'(\d+)\s*(?:yr|year|years)',
        ]
        
        for pattern in tenure_patterns:
            matches = re.findall(pattern, conversation_text.lower())
            if matches:
                tenure_value = int(matches[-1])
                # Convert years to months
                if 'year' in conversation_text.lower() or 'yr' in conversation_text.lower():
                    tenure_value = tenure_value * 12
                tenure = tenure_value
                break
        
        return {
            "loan_amount": loan_amount,
            "tenure_months": tenure
        }
