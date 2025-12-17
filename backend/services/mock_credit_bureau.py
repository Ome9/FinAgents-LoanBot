"""Mock Credit Bureau service for credit score retrieval."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json
from pathlib import Path
from datetime import datetime

router = APIRouter(prefix="/api/credit-bureau", tags=["Credit Bureau"])

# Load customer data
DATA_FILE = Path(__file__).parent.parent / "data" / "customers.json"

def load_customers() -> Dict[str, Any]:
    """Load customer data from JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)


@router.get("/score/{customer_id}")
async def get_credit_score(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve credit score from credit bureau.
    
    Args:
        customer_id: Unique customer identifier
        
    Returns:
        Credit score (out of 900) and credit report summary
    """
    data = load_customers()
    
    for customer in data["customers"]:
        if customer["customer_id"] == customer_id:
            credit_score = customer["credit_score"]
            
            # Calculate credit rating based on score
            if credit_score >= 800:
                rating = "Excellent"
                risk_category = "Low Risk"
            elif credit_score >= 750:
                rating = "Very Good"
                risk_category = "Low Risk"
            elif credit_score >= 700:
                rating = "Good"
                risk_category = "Medium Risk"
            elif credit_score >= 650:
                rating = "Fair"
                risk_category = "Medium-High Risk"
            else:
                rating = "Poor"
                risk_category = "High Risk"
            
            # Calculate total debt
            total_debt = sum(loan["outstanding"] for loan in customer.get("existing_loans", []))
            total_emi = sum(loan["emi"] for loan in customer.get("existing_loans", []))
            
            return {
                "success": True,
                "data": {
                    "customer_id": customer_id,
                    "credit_score": credit_score,
                    "max_score": 900,
                    "rating": rating,
                    "risk_category": risk_category,
                    "report_date": datetime.now().strftime("%Y-%m-%d"),
                    "credit_utilization": {
                        "total_outstanding_debt": total_debt,
                        "total_monthly_emi": total_emi,
                        "number_of_active_loans": len(customer.get("existing_loans", []))
                    },
                    "payment_history": "Good" if credit_score >= 700 else "Needs Improvement",
                    "credit_age_years": 5 if credit_score >= 750 else 3,
                    "recent_inquiries": 1
                }
            }
    
    raise HTTPException(status_code=404, detail="Customer credit record not found")


@router.get("/report/{customer_id}")
async def get_detailed_report(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve detailed credit report.
    
    Args:
        customer_id: Unique customer identifier
        
    Returns:
        Comprehensive credit report
    """
    data = load_customers()
    
    for customer in data["customers"]:
        if customer["customer_id"] == customer_id:
            return {
                "success": True,
                "data": {
                    "customer_id": customer_id,
                    "name": customer["name"],
                    "credit_score": customer["credit_score"],
                    "existing_loans": customer.get("existing_loans", []),
                    "credit_history_length": "5+ years" if customer["credit_score"] >= 750 else "3-5 years",
                    "defaults": [],
                    "late_payments": 0 if customer["credit_score"] >= 700 else 2,
                    "report_generated_at": datetime.now().isoformat()
                }
            }
    
    raise HTTPException(status_code=404, detail="Customer credit record not found")
