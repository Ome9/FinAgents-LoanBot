"""Utility functions for the application."""
from typing import Dict, Any
from datetime import datetime
import random
import string


def generate_reference_number(prefix: str = "REF") -> str:
    """Generate a unique reference number."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{timestamp}{random_suffix}"


def generate_loan_account_number() -> str:
    """Generate a loan account number."""
    return f"LA{datetime.now().strftime('%Y')}{''.join(random.choices(string.digits, k=10))}"


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    Calculate EMI using the standard formula.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (%)
        tenure_months: Loan tenure in months
        
    Returns:
        Monthly EMI amount
    """
    monthly_rate = annual_rate / (12 * 100)
    
    if monthly_rate == 0:
        return principal / tenure_months
    
    emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)


def format_currency(amount: float, currency: str = "₹") -> str:
    """Format amount as currency with Indian numbering system."""
    return f"{currency}{amount:,.2f}"


def validate_phone_number(phone: str) -> bool:
    """Validate Indian phone number format."""
    # Remove common separators
    cleaned = phone.replace(" ", "").replace("-", "").replace("+91", "")
    
    # Check if it's a valid 10-digit number
    return len(cleaned) == 10 and cleaned.isdigit()


def validate_email(email: str) -> bool:
    """Basic email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_approval_message(customer_name: str, loan_amount: float, tenure: int) -> str:
    """Generate a congratulatory approval message."""
    return f"""
🎉 Congratulations {customer_name}! 

Your personal loan of ₹{loan_amount:,.0f} has been approved!

✅ Loan Amount: ₹{loan_amount:,.0f}
✅ Tenure: {tenure} months
✅ Status: APPROVED

Your sanction letter is being generated. You'll receive the disbursement within 24-48 hours.
    """.strip()


def get_rejection_message(reason: str) -> str:
    """Generate a polite rejection message."""
    messages = {
        "credit_score": """
We appreciate your interest in our personal loan. However, based on our current credit assessment, 
we're unable to process your application at this time.

💡 Suggestion: You can improve your credit score by:
- Making timely payments on existing loans
- Reducing credit card utilization
- Avoiding multiple loan inquiries

Please feel free to apply again after 6 months.
        """,
        "high_amount": """
We appreciate your interest. However, the requested loan amount exceeds our current lending limit 
for your profile.

💡 Alternative: Consider applying for a lower amount that fits within your pre-approved limit, 
or you can reapply after demonstrating additional income sources.
        """,
        "emi_ratio": """
We appreciate your interest. However, based on your current income and existing obligations, 
the EMI would exceed our comfortable lending ratio.

💡 Suggestion: Consider:
- Applying for a lower loan amount
- Choosing a longer tenure to reduce EMI
- Providing proof of additional income sources
        """
    }
    return messages.get(reason, "We're unable to process your application at this time.").strip()
