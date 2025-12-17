"""Verification Agent - Validates customer KYC details."""
from typing import Dict, Any
import httpx
from config import settings


class VerificationAgent:
    """Verification Agent for validating customer details via CRM."""
    
    def __init__(self):
        self.base_url = f"http://localhost:{settings.api_port}"
    
    async def verify_customer(
        self,
        customer_id: str,
        phone: str = None,
        address: str = None
    ) -> Dict[str, Any]:
        """
        Verify customer KYC details through CRM service.
        
        Args:
            customer_id: Customer ID to verify
            phone: Phone number to verify (optional)
            address: Address to verify (optional)
            
        Returns:
            Verification result with status and message
        """
        try:
            async with httpx.AsyncClient() as client:
                # First, get customer details
                customer_response = await client.get(
                    f"{self.base_url}/api/crm/customer/{customer_id}"
                )
                
                if customer_response.status_code != 200:
                    return {
                        "success": False,
                        "verified": False,
                        "message": "Customer not found in our records.",
                        "next_agent": None
                    }
                
                customer_data = customer_response.json()['data']
                
                # Perform KYC verification
                verification_params = {"customer_id": customer_id}
                if phone:
                    verification_params["phone"] = phone
                if address:
                    verification_params["address"] = address
                
                verify_response = await client.post(
                    f"{self.base_url}/api/crm/verify-kyc",
                    params=verification_params
                )
                
                if verify_response.status_code == 200:
                    verification_result = verify_response.json()['data']
                    
                    if verification_result['verified']:
                        message = f"""✅ Verification Successful!

Thank you for confirming your details. Your information has been verified:
- Name: {customer_data['name']}
- Phone: {customer_data['phone']}
- Address: {customer_data['city']}

Now let me check your loan eligibility..."""
                        
                        return {
                            "success": True,
                            "verified": True,
                            "message": message,
                            "customer_data": customer_data,
                            "next_agent": "underwriting"
                        }
                    else:
                        failed_checks = []
                        if 'phone' in verification_result['details'] and not verification_result['details']['phone']['verified']:
                            failed_checks.append("phone number")
                        if 'address' in verification_result['details'] and not verification_result['details']['address']['verified']:
                            failed_checks.append("address")
                        
                        message = f"""❌ Verification Failed

The following details don't match our records: {', '.join(failed_checks)}

Please provide the correct information as per your registered details."""
                        
                        return {
                            "success": False,
                            "verified": False,
                            "message": message,
                            "failed_checks": failed_checks,
                            "next_agent": None
                        }
                
                return {
                    "success": False,
                    "verified": False,
                    "message": "Unable to verify your details at this time. Please try again.",
                    "next_agent": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "verified": False,
                "message": f"Verification service temporarily unavailable. Error: {str(e)}",
                "next_agent": None
            }
    
    async def quick_verify(self, customer_id: str) -> Dict[str, Any]:
        """
        Quick verification using just customer ID (for seamless flow).
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Verification result
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/crm/customer/{customer_id}"
                )
                
                if response.status_code == 200:
                    customer_data = response.json()['data']
                    
                    # Validate that customer_data has all required fields for underwriting
                    if not customer_data.get('pre_approved_limit'):
                        return {
                            "success": False,
                            "verified": False,
                            "message": "❌ Error: Your profile is incomplete. Pre-approved limit not found. Please contact support.",
                            "next_agent": None
                        }
                    
                    message = f"""✅ Identity Verified!

Welcome back, {customer_data['name']}! 

Your details are confirmed:
- Customer ID: {customer_id}
- Registered Phone: {customer_data['phone']}
- City: {customer_data['city']}
- Pre-approved Limit: ₹{customer_data.get('pre_approved_limit', 0):,.0f}

Let me check your eligibility for the loan..."""
                    
                    return {
                        "success": True,
                        "verified": True,
                        "message": message,
                        "customer_data": customer_data,
                        "next_agent": "underwriting"
                    }
                else:
                    return {
                        "success": False,
                        "verified": False,
                        "message": "We couldn't find your details. Please contact our customer support.",
                        "next_agent": None
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "verified": False,
                "message": f"Verification service error: {str(e)}",
                "next_agent": None
            }
