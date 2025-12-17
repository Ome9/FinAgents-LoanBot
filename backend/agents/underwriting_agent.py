"""Underwriting Agent - Performs loan eligibility checks."""
from typing import Dict, Any, Optional
import httpx
from config import settings
from utils.helpers import calculate_emi


class UnderwritingAgent:
    """Underwriting Agent for credit assessment and eligibility checks."""
    
    def __init__(self):
        self.base_url = f"http://localhost:{settings.api_port}"
        self.min_credit_score = settings.min_credit_score
        self.max_emi_ratio = settings.max_emi_to_salary_ratio
        self.conditional_multiplier = settings.conditional_approval_multiplier
    
    async def assess_eligibility(
        self,
        customer_id: str,
        loan_amount: float,
        tenure_months: int,
        customer_data: Dict[str, Any],
        salary_slip_provided: bool = False,
        stated_salary: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Assess loan eligibility based on credit score and financial rules.
        
        Business Rules:
        - Reject if credit score < 700
        - Instant approval if amount <= pre-approved limit and score >= 700
        - Conditional approval if amount <= 2x pre-approved and score >= 700 (needs salary slip)
        - Reject if amount > 2x pre-approved limit
        
        Args:
            customer_id: Customer ID
            loan_amount: Requested loan amount
            tenure_months: Loan tenure in months
            customer_data: Customer information
            salary_slip_provided: Whether salary slip was provided
            stated_salary: Salary amount if provided
            
        Returns:
            Eligibility assessment result
        """
        try:
            # Validate customer_data has required fields
            if not customer_data:
                return {
                    "success": False,
                    "approved": False,
                    "message": "❌ Error: Customer data is missing. Please complete verification first.",
                    "next_agent": None
                }
            
            # Validate loan amount and tenure
            if not loan_amount or loan_amount <= 0:
                return {
                    "success": False,
                    "approved": False,
                    "message": "❌ Error: Invalid loan amount. Please provide a valid amount.",
                    "next_agent": None
                }
            
            if not tenure_months or tenure_months <= 0:
                return {
                    "success": False,
                    "approved": False,
                    "message": "❌ Error: Invalid tenure. Please provide a valid tenure.",
                    "next_agent": None
                }
            
            # Get credit score
            credit_result = await self._get_credit_score(customer_id)
            
            if not credit_result['success']:
                return {
                    "success": False,
                    "approved": False,
                    "message": "Unable to fetch credit score. Please try again.",
                    "next_agent": None
                }
            
            credit_score = credit_result['credit_score']
            
            # Get pre_approved_limit from customer_data (must exist)
            pre_approved_limit = customer_data.get('pre_approved_limit')
            if pre_approved_limit is None:
                return {
                    "success": False,
                    "approved": False,
                    "message": "❌ Error: Pre-approved limit not found. Please complete verification.",
                    "next_agent": None
                }
            
            customer_salary = stated_salary or customer_data.get('salary', 0)
            
            # Get offer details for interest rate
            offer_result = await self._get_offers(customer_id)
            interest_rate = 12.5  # Default
            
            if offer_result['success'] and offer_result['offers']:
                # Find appropriate offer tier
                for offer in offer_result['offers']:
                    if loan_amount <= offer['max_amount']:
                        interest_rate = offer['interest_rate']
                        break
            
            # Calculate EMI
            emi = calculate_emi(loan_amount, interest_rate, tenure_months)
            
            # Rule 1: Check credit score
            if credit_score < self.min_credit_score:
                return {
                    "success": True,
                    "approved": False,
                    "decision": "REJECTED",
                    "reason": "credit_score",
                    "message": f"""❌ Loan Application - Unable to Proceed

Unfortunately, we cannot approve your loan application at this time.

Reason: Your current credit score ({credit_score}/900) is below our minimum requirement of {self.min_credit_score}.

💡 How to improve:
• Make timely payments on existing loans
• Maintain low credit card balances
• Avoid multiple loan inquiries

You're welcome to reapply after 6 months once your credit score improves.""",
                    "credit_score": credit_score,
                    "next_agent": None
                }
            
            # Rule 2: Instant Approval - Amount within pre-approved limit
            if loan_amount <= pre_approved_limit:
                total_payment = emi * tenure_months
                total_interest = total_payment - loan_amount
                
                return {
                    "success": True,
                    "approved": True,
                    "decision": "INSTANT_APPROVAL",
                    "message": f"""🎉 **Congratulations! Your Loan is APPROVED!**

**Loan Summary:**
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 **Principal Amount:** ₹{loan_amount:,.0f}
📅 **Tenure:** {tenure_months} months ({tenure_months//12} years {tenure_months%12} months)
📊 **Interest Rate:** {interest_rate}% per annum
💳 **Monthly EMI:** ₹{emi:,.0f}
━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 **Total Interest:** ₹{total_interest:,.0f}
💵 **Total Payable:** ₹{total_payment:,.0f}
🌟 **Credit Score:** {credit_score}/900 (Excellent!)

✅ **Instant Approval** - No additional documentation required!

Your official sanction letter is ready to be generated...""",
                    "loan_details": {
                        "loan_amount": loan_amount,
                        "tenure_months": tenure_months,
                        "interest_rate": interest_rate,
                        "monthly_emi": emi,
                        "total_payment": emi * tenure_months,
                        "credit_score": credit_score
                    },
                    "next_agent": "sanction_letter"
                }
            
            # Rule 3: Conditional Approval - Amount within 2x pre-approved limit
            elif loan_amount <= (pre_approved_limit * self.conditional_multiplier):
                # Check if salary slip is required and provided
                if not salary_slip_provided:
                    return {
                        "success": True,
                        "approved": False,
                        "decision": "CONDITIONAL_APPROVAL_PENDING",
                        "requires_salary_slip": True,
                        "message": f"""📋 Additional Verification Required

Good news! You're eligible for a loan of ₹{loan_amount:,.0f}.

However, since this amount exceeds your instant approval limit of ₹{pre_approved_limit:,.0f}, we need to verify your income.

Please provide:
📄 Latest salary slip or bank statement

Estimated EMI: ₹{emi:,.0f}/month
Interest Rate: {interest_rate}% p.a.

Would you like to upload your salary slip to proceed?""",
                        "loan_details": {
                            "loan_amount": loan_amount,
                            "tenure_months": tenure_months,
                            "interest_rate": interest_rate,
                            "estimated_emi": emi
                        },
                        "next_agent": None  # Wait for salary slip
                    }
                
                # Salary slip provided - check EMI to salary ratio
                emi_to_salary_ratio = emi / customer_salary
                
                if emi_to_salary_ratio > self.max_emi_ratio:
                    return {
                        "success": True,
                        "approved": False,
                        "decision": "REJECTED",
                        "reason": "emi_ratio",
                        "message": f"""❌ Loan Application - Unable to Approve

Thank you for providing your salary details. However, the EMI of ₹{emi:,.0f} would be {emi_to_salary_ratio*100:.1f}% of your monthly salary (₹{customer_salary:,.0f}).

Our policy limits EMI to {self.max_emi_ratio*100:.0f}% of monthly income for responsible lending.

💡 Alternative options:
• Apply for ₹{pre_approved_limit:,.0f} (instant approval)
• Choose longer tenure to reduce EMI
• Consider a co-applicant to increase eligibility""",
                        "next_agent": None
                    }
                
                # Approved with salary verification
                total_payment = emi * tenure_months
                total_interest = total_payment - loan_amount
                
                return {
                    "success": True,
                    "approved": True,
                    "decision": "CONDITIONAL_APPROVAL",
                    "message": f"""🎉 **Congratulations! Your Loan is APPROVED!**

**Loan Summary:**
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 **Principal Amount:** ₹{loan_amount:,.0f}
📅 **Tenure:** {tenure_months} months ({tenure_months//12} years {tenure_months%12} months)
📊 **Interest Rate:** {interest_rate}% per annum
💳 **Monthly EMI:** ₹{emi:,.0f}
━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 **Total Interest:** ₹{total_interest:,.0f}
💵 **Total Payable:** ₹{total_payment:,.0f}
📊 **EMI/Salary Ratio:** {emi_to_salary_ratio*100:.1f}% (Healthy)
🌟 **Credit Score:** {credit_score}/900

✅ **Income Verified & Approved**

Your official sanction letter is ready to be generated...""",
                    "loan_details": {
                        "loan_amount": loan_amount,
                        "tenure_months": tenure_months,
                        "interest_rate": interest_rate,
                        "monthly_emi": emi,
                        "total_payment": emi * tenure_months,
                        "credit_score": credit_score,
                        "salary_verified": True
                    },
                    "next_agent": "sanction_letter"
                }
            
            # Rule 4: Reject - Amount exceeds 2x pre-approved limit
            else:
                max_eligible = pre_approved_limit * self.conditional_multiplier
                return {
                    "success": True,
                    "approved": False,
                    "decision": "REJECTED",
                    "reason": "high_amount",
                    "message": f"""❌ Loan Amount Exceeds Eligibility

The requested amount of ₹{loan_amount:,.0f} exceeds your maximum eligible limit of ₹{max_eligible:,.0f}.

Your current eligibility:
• Instant Approval: Up to ₹{pre_approved_limit:,.0f}
• With Income Verification: Up to ₹{max_eligible:,.0f}

💡 What you can do:
• Apply for ₹{max_eligible:,.0f} or less
• Build your credit history and reapply later
• Provide additional income proof (business income, rental income, etc.)

Would you like to proceed with a lower amount?""",
                    "max_eligible_amount": max_eligible,
                    "next_agent": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "approved": False,
                "message": f"Error during eligibility assessment: {str(e)}",
                "next_agent": None
            }
    
    async def _get_credit_score(self, customer_id: str) -> Dict[str, Any]:
        """Fetch credit score from credit bureau."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/credit-bureau/score/{customer_id}"
                )
                
                if response.status_code == 200:
                    data = response.json()['data']
                    return {
                        "success": True,
                        "credit_score": data['credit_score'],
                        "rating": data['rating']
                    }
                return {"success": False}
        except:
            return {"success": False}
    
    async def _get_offers(self, customer_id: str) -> Dict[str, Any]:
        """Fetch pre-approved offers."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/offers/preapproved/{customer_id}"
                )
                
                if response.status_code == 200:
                    data = response.json()['data']
                    return {
                        "success": True,
                        "offers": data.get('offers', [])
                    }
                return {"success": False, "offers": []}
        except:
            return {"success": False, "offers": []}
