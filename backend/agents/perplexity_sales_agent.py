"""Sales Agent using Perplexity API - Handles customer engagement and loan negotiation."""
from openai import OpenAI
from typing import Dict, Any, List
from config import settings
import time


class PerplexitySalesAgent:
    """Sales Agent using Perplexity API for engaging customers and collecting loan requirements."""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.perplexity_api_key,
            base_url="https://api.perplexity.ai"
        )
        self.model = settings.perplexity_model
        self.last_api_call = 0
        self.min_call_interval = 1.0  # Minimum 1 second between API calls
        self.api_call_count = 0
        self.max_api_calls = 20  # Maximum 20 API calls per session
        
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
        
        # Build messages for Perplexity - must strictly alternate user/assistant
        messages = []
        first_user_message_added = False
        
        # Filter and add conversation history ensuring strict alternation
        for msg in conversation_history[-6:]:  # Last 6 messages for context
            if msg['role'] == 'user':
                # For first user message, prepend context and system prompt
                if not first_user_message_added:
                    full_content = f"{self.system_prompt}\n\n{context}\n\nUser: {msg['content']}"
                    messages.append({"role": "user", "content": full_content})
                    first_user_message_added = True
                else:
                    # Only add if previous message was assistant (to maintain alternation)
                    if messages and messages[-1]['role'] == 'assistant':
                        messages.append({"role": "user", "content": msg['content']})
                    elif not messages:
                        # First message but wasn't added above (shouldn't happen)
                        full_content = f"{self.system_prompt}\n\n{context}\n\nUser: {msg['content']}"
                        messages.append({"role": "user", "content": full_content})
                        first_user_message_added = True
                        
            elif msg['role'] == 'assistant':
                content = msg['content'].replace('COLLECT_COMPLETE', '').strip()
                # Only add if previous message was user (to maintain alternation)
                if messages and messages[-1]['role'] == 'user':
                    messages.append({"role": "assistant", "content": content})
        
        # Add current message - must ensure it alternates properly
        if not messages:
            # No history - start fresh with system prompt
            full_content = f"{self.system_prompt}\n\n{context}\n\nUser: {user_message}"
            messages.append({"role": "user", "content": full_content})
        elif messages[-1]['role'] == 'assistant':
            # Last message was assistant, safe to add user message
            messages.append({"role": "user", "content": user_message})
        else:
            # Last message was user - this shouldn't happen in normal flow
            # Merge with previous user message to fix alternation
            messages[-1]['content'] += f"\n\n{user_message}"
        
        # Rate limiting - prevent infinite loops
        self.api_call_count += 1
        if self.api_call_count > self.max_api_calls:
            raise Exception("API call limit reached. Please start a new conversation.")
        
        # Enforce minimum interval between calls
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call
        if time_since_last_call < self.min_call_interval:
            time.sleep(self.min_call_interval - time_since_last_call)
        
        # Get response from Perplexity
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        self.last_api_call = time.time()
        
        # Extract response
        agent_response = response.choices[0].message.content
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
        
        # Only look at USER messages (not assistant responses which might contain offers/examples)
        user_messages = [msg.get('content', '') for msg in conversation_history if msg.get('role') == 'user']
        
        # Focus on the LAST few user messages (most recent context)
        recent_user_text = " ".join(user_messages[-3:]) if user_messages else ""
        
        # Extract loan amount (look for patterns like ₹2L, 200000, 2 lakhs, etc.)
        # Priority: explicit amounts > lakhs notation
        amount_patterns = [
            (r'₹\s*(\d+(?:,\d+)+)', 'exact'),           # ₹2,00,000 (exact with commas)
            (r'(\d{5,})', 'exact'),                      # 200000 (5+ digits = exact amount)
            (r'₹\s*(\d+(?:\.\d+)?)\s*(?:l|lakh|lakhs)', 'lakh'),  # ₹2 lakhs
            (r'(\d+(?:\.\d+)?)\s*(?:l|lakh|lakhs)', 'lakh'),      # 2 lakhs
        ]
        
        for pattern, amount_type in amount_patterns:
            matches = re.findall(pattern, recent_user_text.lower(), re.IGNORECASE)
            if matches:
                # Take the LAST match (most recent in conversation)
                amount_str = matches[-1].replace(',', '')
                try:
                    amount = float(amount_str)
                    # If in lakhs notation, convert to actual amount
                    if amount_type == 'lakh' and amount < 100:
                        amount = amount * 100000
                    loan_amount = int(amount)
                    break
                except ValueError:
                    continue
        
        # Extract tenure (look for months in user messages only)
        tenure_patterns = [
            r'(\d+)\s*(?:month|months|mnth|mnths)',
            r'(\d+)\s*(?:yr|year|years)',
        ]
        
        for pattern in tenure_patterns:
            matches = re.findall(pattern, recent_user_text.lower())
            if matches:
                # Take the LAST match (most recent)
                tenure_value = int(matches[-1])
                # Convert years to months
                if 'year' in recent_user_text.lower() or 'yr' in recent_user_text.lower():
                    tenure_value = tenure_value * 12
                tenure = tenure_value
                break
        
        return {
            "loan_amount": loan_amount,
            "tenure_months": tenure
        }
