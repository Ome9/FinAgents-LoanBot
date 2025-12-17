# NBFC Loan Sales Chatbot - Setup Guide

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- OpenAI API Key

### Step 1: Setup Backend

```powershell
# Run setup script
.\setup-backend.ps1

# Edit .env file and add your OpenAI API key
# backend\.env: OPENAI_API_KEY=your_key_here
```

### Step 2: Setup Frontend

```powershell
# Run setup script
.\setup-frontend.ps1
```

### Step 3: Start Application

```powershell
# Start both servers
.\start.ps1
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## Manual Setup

### Backend Setup

```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy ..\.env.example .env

# Edit .env and add OPENAI_API_KEY
notepad .env

# Run server
python main.py
```

### Frontend Setup

```powershell
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

---

## Testing the Application

### 1. Test with Sample Customers

The application includes 12 pre-configured customers with different profiles:

**Instant Approval Scenarios:**
- **CUST001** (Rajesh Kumar) - Credit Score: 780, Pre-approved: ₹3,00,000
- **CUST002** (Priya Sharma) - Credit Score: 825, Pre-approved: ₹5,00,000
- **CUST006** (Ananya Iyer) - Credit Score: 850, Pre-approved: ₹6,00,000

**Conditional Approval (Salary Slip Required):**
- **CUST004** (Sneha Reddy) - Credit Score: 795, Pre-approved: ₹4,00,000
  - Request ₹6,00,000 (1.5x pre-approved)
  - Provide salary: ₹95,000

**Rejection Scenarios:**
- **CUST003** (Amit Patel) - Credit Score: 650 (Below 700)
- **CUST007** (Rahul Mehta) - Credit Score: 680, Pre-approved: ₹1,50,000
  - Request ₹5,00,000 (exceeds 2x limit)

### 2. Test Conversation Flow

**Example Conversation:**

```
Bot: Hello Rajesh! 👋 Welcome to Tata Capital Personal Loans...

User: Hi, I need a loan for home renovation

Bot: Great! I can help you with that. How much do you need?

User: I need 2 lakh rupees

Bot: Perfect! And what tenure would work best for you?

User: 36 months would be good

Bot: Excellent choice! Let me verify your details...
[Verification happens automatically]

Bot: ✅ Verification Successful! Now checking eligibility...
[Credit check and underwriting]

Bot: 🎉 Congratulations! Your loan is APPROVED!
[Sanction letter generated]
```

### 3. API Testing

Use the interactive API documentation at http://localhost:8000/docs

**Test Endpoints:**
- GET `/api/crm/customers/list` - View all customers
- GET `/api/crm/customer/{customer_id}` - Get customer details
- GET `/api/credit-bureau/score/{customer_id}` - Check credit score
- GET `/api/offers/preapproved/{customer_id}` - View offers
- POST `/api/chat` - Send chat message

---

## Architecture Overview

### Backend Components

1. **Master Agent** (`agents/master_agent.py`)
   - Orchestrates entire workflow using LangGraph
   - Manages state transitions between agents
   - Handles conversation flow

2. **Worker Agents**
   - **Sales Agent**: Engages customers, collects requirements
   - **Verification Agent**: Validates KYC via Mock CRM
   - **Underwriting Agent**: Assesses eligibility using business rules
   - **Sanction Letter Generator**: Creates PDF approval documents

3. **Mock Services** (FastAPI Endpoints)
   - Mock CRM: Customer data and KYC verification
   - Mock Credit Bureau: Credit scores (out of 900)
   - Mock Offer Mart: Pre-approved loan offers

### Frontend Components

1. **Customer Selection** (`App.jsx`)
   - Lists available customers
   - Displays customer cards with pre-approved status

2. **Chat Interface** (`ChatInterface.jsx`)
   - Real-time messaging with typing indicators
   - Progress bar showing current stage
   - Salary slip upload functionality
   - Sanction letter download

---

## Business Rules

### Underwriting Logic

1. **Credit Score Check**
   - Minimum required: 700/900
   - Reject if below threshold

2. **Instant Approval**
   - Loan amount ≤ pre-approved limit
   - Credit score ≥ 700
   - No additional documentation required

3. **Conditional Approval**
   - Loan amount ≤ 2× pre-approved limit
   - Credit score ≥ 700
   - Requires salary slip verification
   - EMI must be ≤ 50% of monthly salary

4. **Rejection**
   - Credit score < 700
   - Loan amount > 2× pre-approved limit
   - EMI > 50% of salary (after salary verification)

### Interest Rates

- 800-900: 10.5-11.0% p.a. (Premium)
- 750-799: 11.5-12.0% p.a. (Excellent)
- 700-749: 12.5-13.0% p.a. (Good)
- Below 700: 14.5-16.0% p.a. (Standard) - Usually rejected

---

## Troubleshooting

### Backend Issues

**Problem: "Module not found" error**
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: "OpenAI API Key not found"**
```powershell
# Check .env file exists
ls .env

# Edit and add API key
notepad backend\.env
# Add: OPENAI_API_KEY=your_actual_key
```

**Problem: "Port 8000 already in use"**
```powershell
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Frontend Issues

**Problem: "npm install fails"**
```powershell
# Clear npm cache
npm cache clean --force

# Delete node_modules and retry
rm -r node_modules
npm install
```

**Problem: "API connection failed"**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify frontend vite.config.js proxy settings

---

## Demo Presentation Tips

### 5-Slide PPT Structure

**Slide 1: Problem Statement**
- Show fragmented sales process diagram
- Highlight drop-off points and conversion issues

**Slide 2: Solution Architecture**
- Show Master Agent + Worker Agents diagram
- Explain orchestration flow
- Highlight seamless conversation approach

**Slide 3: Customer Journey - Happy Path**
- Screenshots: Initial greeting → Loan discussion → Instant approval
- Show sanction letter generation
- Emphasize speed and simplicity

**Slide 4: Edge Cases Handled**
- Screenshot: Conditional approval with salary slip request
- Screenshot: Rejection with helpful alternatives
- Show intelligent objection handling

**Slide 5: Business Impact**
- Metrics: Reduced drop-off, faster processing
- Key features: Instant approval, human-like conversation, automated documentation
- Next steps and scalability

### Live Demo Script

1. **Start with Overview** (30 sec)
   - "This is an AI-powered loan sales assistant that eliminates process fragmentation"

2. **Show Customer Selection** (15 sec)
   - "12 pre-configured customers with different profiles"

3. **Demonstrate Instant Approval** (2 min)
   - Select customer with good credit
   - Natural conversation about loan needs
   - Show automatic verification and approval
   - Download sanction letter PDF

4. **Show Conditional Approval** (1.5 min)
   - Request higher amount
   - Upload salary slip
   - Show EMI calculation and approval

5. **Demonstrate Rejection Handling** (1 min)
   - Low credit score scenario
   - Show polite rejection with alternatives

---

## Project Structure

```
EY-Techathon/
├── backend/
│   ├── agents/
│   │   ├── master_agent.py          # Main orchestrator
│   │   ├── sales_agent.py            # Customer engagement
│   │   ├── verification_agent.py     # KYC validation
│   │   ├── underwriting_agent.py     # Eligibility assessment
│   │   └── sanction_letter_generator.py  # PDF generation
│   ├── services/
│   │   ├── mock_crm.py               # Customer data service
│   │   ├── mock_credit_bureau.py     # Credit score service
│   │   └── mock_offer_mart.py        # Pre-approved offers
│   ├── data/
│   │   └── customers.json            # 12 synthetic customers
│   ├── utils/
│   │   └── helpers.py                # Utility functions
│   ├── main.py                       # FastAPI application
│   ├── config.py                     # Configuration management
│   └── requirements.txt              # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatInterface.jsx     # Main chat UI
│   │   ├── services/
│   │   │   └── api.js                # API integration
│   │   ├── App.jsx                   # Customer selection
│   │   └── main.jsx                  # Entry point
│   ├── package.json                  # Node dependencies
│   └── vite.config.js                # Vite configuration
├── README.md                         # Main documentation
├── SETUP.md                          # This file
├── setup-backend.ps1                 # Backend setup script
├── setup-frontend.ps1                # Frontend setup script
└── start.ps1                         # Quick start script
```

---

## Next Steps

1. **Add your OpenAI API key** to `backend/.env`
2. **Run the setup scripts** for backend and frontend
3. **Start the application** using `start.ps1`
4. **Test all three scenarios**: instant approval, conditional, rejection
5. **Take screenshots** for your presentation
6. **Create your 5-slide PPT** using the structure above

---

## Support

For issues or questions during the hackathon:
1. Check this guide first
2. Review API documentation at http://localhost:8000/docs
3. Check browser console and terminal logs
4. Test individual endpoints in the API docs

Good luck with your presentation! 🚀
