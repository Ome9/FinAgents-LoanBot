"""FastAPI main application."""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from pathlib import Path

from config import settings
from services import mock_crm, mock_credit_bureau, mock_offer_mart
from agents.master_agent import MasterAgent

# Initialize FastAPI app
app = FastAPI(
    title="NBFC Loan Sales Chatbot API",
    description="Agentic AI system for personal loan sales",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include mock service routers
app.include_router(mock_crm.router)
app.include_router(mock_credit_bureau.router)
app.include_router(mock_offer_mart.router)

# Initialize Master Agent
master_agent = MasterAgent()

# In-memory session storage (in production, use Redis or database)
sessions: Dict[str, Dict[str, Any]] = {}


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat message request."""
    session_id: Optional[str] = None
    customer_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    """Chat message response."""
    session_id: str
    messages: list
    current_stage: str
    requires_salary_slip: bool = False
    conversation_complete: bool = False
    sanction_letter_available: bool = False
    quick_replies: list = []


class SalarySlipUpload(BaseModel):
    """Salary slip upload request."""
    session_id: str
    salary_amount: float


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "NBFC Loan Sales Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes messages through Master Agent.
    
    Args:
        request: Chat request with message and optional session/customer ID
        
    Returns:
        Chat response with agent messages and state
    """
    # Get or create session
    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id] = {}
        
        # If customer ID provided, initialize with customer data
        if request.customer_id:
            sessions[session_id] = await master_agent.set_customer_id(
                request.customer_id,
                sessions[session_id]
            )
    
    # Process message
    try:
        updated_state = await master_agent.process_message(
            request.message,
            sessions[session_id]
        )
        
        sessions[session_id] = updated_state
        
        return ChatResponse(
            session_id=session_id,
            messages=updated_state.get("messages", []),
            current_stage=updated_state.get("current_stage", "sales"),
            requires_salary_slip=updated_state.get("requires_salary_slip", False),
            conversation_complete=updated_state.get("conversation_complete", False),
            sanction_letter_available=bool(updated_state.get("sanction_letter_path")),
            quick_replies=updated_state.get("quick_replies", [])
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.post("/api/upload-salary-slip")
async def upload_salary_slip(request: SalarySlipUpload):
    """
    Handle salary slip upload (simplified - just accepts salary amount).
    
    Args:
        request: Salary slip upload with session ID and salary amount
        
    Returns:
        Updated chat state after reprocessing underwriting
    """
    session_id = request.session_id
    
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        updated_state = await master_agent.upload_salary_slip(
            request.salary_amount,
            sessions[session_id]
        )
        
        sessions[session_id] = updated_state
        
        return ChatResponse(
            session_id=session_id,
            messages=updated_state.get("messages", []),
            current_stage=updated_state.get("current_stage", "underwriting"),
            requires_salary_slip=updated_state.get("requires_salary_slip", False),
            conversation_complete=updated_state.get("conversation_complete", False),
            sanction_letter_available=bool(updated_state.get("sanction_letter_path"))
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing salary slip: {str(e)}")


@app.get("/api/download-sanction-letter/{session_id}")
async def download_sanction_letter(session_id: str):
    """
    Download sanction letter PDF.
    
    Args:
        session_id: Session ID
        
    Returns:
        PDF file
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    sanction_letter_path = sessions[session_id].get("sanction_letter_path")
    
    if not sanction_letter_path or not Path(sanction_letter_path).exists():
        raise HTTPException(status_code=404, detail="Sanction letter not found")
    
    return FileResponse(
        sanction_letter_path,
        media_type="application/pdf",
        filename=Path(sanction_letter_path).name
    )


@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """
    Get current session state.
    
    Args:
        session_id: Session ID
        
    Returns:
        Session state
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[session_id]
    
    return {
        "session_id": session_id,
        "current_stage": state.get("current_stage"),
        "customer_id": state.get("customer_id"),
        "loan_amount": state.get("loan_amount"),
        "tenure_months": state.get("tenure_months"),
        "requires_salary_slip": state.get("requires_salary_slip"),
        "conversation_complete": state.get("conversation_complete"),
        "message_count": len(state.get("messages", []))
    }


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session.
    
    Args:
        session_id: Session ID
        
    Returns:
        Success message
    """
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Session not found")


@app.post("/api/start-conversation")
async def start_conversation(customer_id: str):
    """
    Start a new conversation for a customer.
    
    Args:
        customer_id: Customer ID
        
    Returns:
        New session with greeting
    """
    session_id = str(uuid.uuid4())
    sessions[session_id] = {}
    
    # Initialize with customer data
    sessions[session_id] = await master_agent.set_customer_id(
        customer_id,
        sessions[session_id]
    )
    
    # Generate greeting
    customer_name = sessions[session_id].get("customer_data", {}).get("name", "Valued Customer")
    greeting = f"""Hello {customer_name.split()[0]}! 👋

Welcome to Tata Capital Personal Loans. I'm here to help you get a personal loan quickly and easily.

I can see you have some exclusive pre-approved offers! Would you like to explore them?"""
    
    sessions[session_id]["messages"] = [
        {"role": "assistant", "content": greeting}
    ]
    
    return ChatResponse(
        session_id=session_id,
        messages=sessions[session_id]["messages"],
        current_stage="sales",
        requires_salary_slip=False,
        conversation_complete=False,
        sanction_letter_available=False
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
