"""Mock Offer Mart service for pre-approved loan offers."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import json
from pathlib import Path
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/offers", tags=["Offer Mart"])

# Load customer data
DATA_FILE = Path(__file__).parent.parent / "data" / "customers.json"

def load_customers() -> Dict[str, Any]:
    """Load customer data from JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def calculate_interest_rate(credit_score: int, loan_amount: int) -> float:
    """Calculate interest rate based on credit score and loan amount."""
    if credit_score >= 800:
        base_rate = 10.5
    elif credit_score >= 750:
        base_rate = 11.5
    elif credit_score >= 700:
        base_rate = 12.5
    else:
        base_rate = 14.5
    
    # Adjust for loan amount (lower rates for higher amounts)
    if loan_amount >= 500000:
        base_rate -= 0.5
    elif loan_amount >= 300000:
        base_rate -= 0.25
    
    return round(base_rate, 2)


@router.get("/preapproved/{customer_id}")
async def get_preapproved_offers(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve pre-approved loan offers for a customer.
    
    Args:
        customer_id: Unique customer identifier
        
    Returns:
        Pre-approved loan offer details
    """
    data = load_customers()
    
    for customer in data["customers"]:
        if customer["customer_id"] == customer_id:
            pre_approved_limit = customer["pre_approved_limit"]
            credit_score = customer["credit_score"]
            
            # Generate offer tiers
            offers = []
            
            # Tier 1: Instant approval amount
            tier1_amount = pre_approved_limit
            tier1_rate = calculate_interest_rate(credit_score, tier1_amount)
            offers.append({
                "tier": "Instant Approval",
                "max_amount": tier1_amount,
                "interest_rate": tier1_rate,
                "tenure_options": [12, 24, 36, 48, 60],
                "processing_fee": 0,
                "features": [
                    "Instant approval - No documentation required",
                    "Disbursal within 24 hours",
                    f"Special rate of {tier1_rate}% p.a."
                ]
            })
            
            # Tier 2: Conditional approval (2x pre-approved)
            if credit_score >= 700:
                tier2_amount = pre_approved_limit * 2
                tier2_rate = calculate_interest_rate(credit_score, tier2_amount)
                offers.append({
                    "tier": "Enhanced Offer",
                    "max_amount": tier2_amount,
                    "interest_rate": tier2_rate,
                    "tenure_options": [12, 24, 36, 48, 60],
                    "processing_fee": tier2_amount * 0.01,  # 1% processing fee
                    "features": [
                        "Salary slip verification required",
                        f"Up to ₹{tier2_amount:,} available",
                        f"Competitive rate of {tier2_rate}% p.a.",
                        "Quick approval subject to income verification"
                    ]
                })
            
            return {
                "success": True,
                "data": {
                    "customer_id": customer_id,
                    "customer_name": customer["name"],
                    "credit_score": credit_score,
                    "offers": offers,
                    "valid_until": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                    "special_message": f"Congratulations {customer['name'].split()[0]}! You have exclusive pre-approved offers available."
                }
            }
    
    raise HTTPException(status_code=404, detail="No offers found for this customer")


@router.post("/calculate-emi")
async def calculate_emi(
    principal: float,
    interest_rate: float,
    tenure_months: int
) -> Dict[str, Any]:
    """
    Calculate EMI for given loan parameters.
    
    Args:
        principal: Loan amount
        interest_rate: Annual interest rate (%)
        tenure_months: Loan tenure in months
        
    Returns:
        EMI calculation details
    """
    # Convert annual rate to monthly rate
    monthly_rate = interest_rate / (12 * 100)
    
    # EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)
    
    total_payment = emi * tenure_months
    total_interest = total_payment - principal
    
    return {
        "success": True,
        "data": {
            "principal": round(principal, 2),
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
            "monthly_emi": round(emi, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2)
        }
    }


@router.get("/interest-rates")
async def get_interest_rates() -> Dict[str, Any]:
    """
    Get current interest rate slabs.
    
    Returns:
        Interest rate information
    """
    return {
        "success": True,
        "data": {
            "rate_slabs": [
                {
                    "credit_score_range": "800-900",
                    "rate": "10.5% - 11.0%",
                    "category": "Premium"
                },
                {
                    "credit_score_range": "750-799",
                    "rate": "11.5% - 12.0%",
                    "category": "Excellent"
                },
                {
                    "credit_score_range": "700-749",
                    "rate": "12.5% - 13.0%",
                    "category": "Good"
                },
                {
                    "credit_score_range": "Below 700",
                    "rate": "14.5% - 16.0%",
                    "category": "Standard"
                }
            ],
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
    }
