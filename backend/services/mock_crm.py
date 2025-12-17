"""Mock CRM service for customer verification."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
import json
from pathlib import Path

router = APIRouter(prefix="/api/crm", tags=["CRM"])

# Load customer data
DATA_FILE = Path(__file__).parent.parent / "data" / "customers.json"

def load_customers() -> Dict[str, Any]:
    """Load customer data from JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)


@router.get("/customer/{customer_id}")
async def get_customer(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve customer details from CRM.
    
    Args:
        customer_id: Unique customer identifier
        
    Returns:
        Customer details including KYC information
    """
    data = load_customers()
    
    for customer in data["customers"]:
        if customer["customer_id"] == customer_id:
            return {
                "success": True,
                "data": customer
            }
    
    raise HTTPException(status_code=404, detail="Customer not found")


@router.get("/customer/phone/{phone}")
async def get_customer_by_phone(phone: str) -> Dict[str, Any]:
    """
    Retrieve customer details by phone number.
    
    Args:
        phone: Customer phone number
        
    Returns:
        Customer details
    """
    data = load_customers()
    
    # Normalize phone format
    normalized_phone = phone.replace(" ", "").replace("-", "")
    
    for customer in data["customers"]:
        customer_phone = customer["phone"].replace(" ", "").replace("-", "")
        if customer_phone == normalized_phone:
            return {
                "success": True,
                "data": customer
            }
    
    raise HTTPException(status_code=404, detail="Customer not found with this phone number")


@router.post("/verify-kyc")
async def verify_kyc(customer_id: str, phone: Optional[str] = None, address: Optional[str] = None) -> Dict[str, Any]:
    """
    Verify customer KYC details.
    
    Args:
        customer_id: Customer ID
        phone: Phone number to verify (optional)
        address: Address to verify (optional)
        
    Returns:
        Verification status
    """
    data = load_customers()
    
    for customer in data["customers"]:
        if customer["customer_id"] == customer_id:
            verification_result = {
                "customer_id": customer_id,
                "verified": True,
                "details": {}
            }
            
            if phone:
                normalized_input = phone.replace(" ", "").replace("-", "")
                normalized_customer = customer["phone"].replace(" ", "").replace("-", "")
                phone_match = normalized_input == normalized_customer
                verification_result["details"]["phone"] = {
                    "verified": phone_match,
                    "stored_value": customer["phone"]
                }
                if not phone_match:
                    verification_result["verified"] = False
            
            if address:
                address_match = address.lower().strip() in customer["address"].lower()
                verification_result["details"]["address"] = {
                    "verified": address_match,
                    "stored_value": customer["address"]
                }
                if not address_match:
                    verification_result["verified"] = False
            
            return {
                "success": True,
                "data": verification_result
            }
    
    raise HTTPException(status_code=404, detail="Customer not found")


@router.get("/customers/list")
async def list_customers() -> Dict[str, Any]:
    """
    List all customers (for testing purposes).
    
    Returns:
        List of all customers with basic info
    """
    data = load_customers()
    
    customer_list = [
        {
            "customer_id": c["customer_id"],
            "name": c["name"],
            "city": c["city"],
            "phone": c["phone"]
        }
        for c in data["customers"]
    ]
    
    return {
        "success": True,
        "count": len(customer_list),
        "data": customer_list
    }
