# loan_data_flow.py
# Data Flow Diagram showing how data moves between agents and services
# Shows: State Object → Agent Processing → Data Validation → Next Agent
from graphviz import Digraph

def create_data_flow_diagram(output_basename='loan_data_flow'):
    """
    Generates data flow diagram showing state management and data passing.
    Optimized for 16:9 slide ratio focusing on data transformations.
    """
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes ---
    g.attr(rankdir='LR', splines='spline', bgcolor='#FFFFFF', dpi='150', 
           nodesep='1.2', ranksep='1.5')
    g.attr('node', shape='plain', fontname='Arial', fontsize='14')
    g.attr('edge', fontname='Arial', fontsize='12')
    g.attr(size='16,9', ratio='fill')  # 16:9 aspect ratio

    # --- Data Store: Initial State ---
    g.node('InitState', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#4299E1" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📦 Initial State</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="100"><FONT COLOR="#2D3748" POINT-SIZE="13">
    {<BR ALIGN="LEFT"/>
      "customer_id": "CUST001",<BR ALIGN="LEFT"/>
      "messages": [],<BR ALIGN="LEFT"/>
      "current_stage": "sales"<BR ALIGN="LEFT"/>
    }<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 1: Sales Agent ---
    g.node('SalesProcess', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#667EEA">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>💼 Sales Agent</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="110"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Input:</B> User message<BR ALIGN="LEFT"/>
    <B>Processing:</B><BR ALIGN="LEFT"/>
    • Perplexity AI conversation<BR ALIGN="LEFT"/>
    • Regex extract amount/tenure<BR ALIGN="LEFT"/>
    <B>Output:</B> loan_amount, tenure_months<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store: State After Sales ---
    g.node('StateAfterSales', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#4299E1" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📦 State Update</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    {<BR ALIGN="LEFT"/>
      "customer_id": "CUST001",<BR ALIGN="LEFT"/>
      "loan_amount": 50000,<BR ALIGN="LEFT"/>
      "tenure_months": 12,<BR ALIGN="LEFT"/>
      "messages": [...],<BR ALIGN="LEFT"/>
      "current_stage": "verification"<BR ALIGN="LEFT"/>
    }<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- External Service: CRM ---
    g.node('CRMService', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>🔌 Mock CRM API</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="90"><FONT COLOR="#2D3748" POINT-SIZE="13">
    GET /api/crm/customer/CUST001<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    Returns: name, email, phone,<BR ALIGN="LEFT"/>
    pre_approved_limit, salary<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 2: Verification Agent ---
    g.node('VerifyProcess', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#9F7AEA">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>✅ Verification Agent</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="110"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Input:</B> customer_id<BR ALIGN="LEFT"/>
    <B>Processing:</B><BR ALIGN="LEFT"/>
    • Call CRM API<BR ALIGN="LEFT"/>
    • Validate pre_approved_limit exists<BR ALIGN="LEFT"/>
    <B>Output:</B> customer_data object<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store: State After Verification ---
    g.node('StateAfterVerify', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#4299E1" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📦 State Update</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="150"><FONT COLOR="#2D3748" POINT-SIZE="13">
    {<BR ALIGN="LEFT"/>
      "customer_id": "CUST001",<BR ALIGN="LEFT"/>
      "loan_amount": 50000,<BR ALIGN="LEFT"/>
      "tenure_months": 12,<BR ALIGN="LEFT"/>
      "customer_data": {<BR ALIGN="LEFT"/>
        "name": "Rajesh Kumar",<BR ALIGN="LEFT"/>
        "pre_approved_limit": 300000<BR ALIGN="LEFT"/>
      },<BR ALIGN="LEFT"/>
      "current_stage": "underwriting"<BR ALIGN="LEFT"/>
    }<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- External Services: Credit Bureau + Offer Mart ---
    g.node('CreditService', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>🔌 Credit Bureau</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="70"><FONT COLOR="#2D3748" POINT-SIZE="13">
    GET /api/credit-bureau/score/CUST001<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    Returns: credit_score: 780<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    g.node('OfferService', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>🔌 Offer Mart</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="70"><FONT COLOR="#2D3748" POINT-SIZE="13">
    GET /api/offers/preapproved/CUST001<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    Returns: interest_rate: 10.5%<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 3: Underwriting Agent ---
    g.node('UnderwriteProcess', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#ED8936">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📊 Underwriting Agent</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="130"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Input:</B> All state data<BR ALIGN="LEFT"/>
    <B>Processing:</B><BR ALIGN="LEFT"/>
    • Validate: score ≥ 700<BR ALIGN="LEFT"/>
    • Compare: amount vs pre_approved<BR ALIGN="LEFT"/>
    • Calculate EMI<BR ALIGN="LEFT"/>
    • Apply approval logic<BR ALIGN="LEFT"/>
    <B>Output:</B> approved, loan_details<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store: State After Underwriting ---
    g.node('StateAfterUnderwrite', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#4299E1" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📦 State Update</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="160"><FONT COLOR="#2D3748" POINT-SIZE="13">
    {<BR ALIGN="LEFT"/>
      ...(previous data),<BR ALIGN="LEFT"/>
      "underwriting_result": {<BR ALIGN="LEFT"/>
        "approved": true,<BR ALIGN="LEFT"/>
        "decision": "INSTANT_APPROVAL",<BR ALIGN="LEFT"/>
        "loan_details": {<BR ALIGN="LEFT"/>
          "monthly_emi": 4424,<BR ALIGN="LEFT"/>
          "interest_rate": 10.5<BR ALIGN="LEFT"/>
        }<BR ALIGN="LEFT"/>
      },<BR ALIGN="LEFT"/>
      "current_stage": "sanction_letter"<BR ALIGN="LEFT"/>
    }<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 4: Sanction Letter Generator ---
    g.node('SanctionProcess', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38B2AC">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📄 Sanction Generator</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="110"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Input:</B> customer_data + loan_details<BR ALIGN="LEFT"/>
    <B>Processing:</B><BR ALIGN="LEFT"/>
    • Validate all required fields<BR ALIGN="LEFT"/>
    • Generate PDF (ReportLab)<BR ALIGN="LEFT"/>
    <B>Output:</B> file_path, download_url<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store: Final State ---
    g.node('FinalState', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#48BB78" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📦 Final State ✅</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="140"><FONT COLOR="#2D3748" POINT-SIZE="13">
    {<BR ALIGN="LEFT"/>
      ...(all previous data),<BR ALIGN="LEFT"/>
      "sanction_letter_path": <BR ALIGN="LEFT"/>
        "backend/sanction_letters/...",<BR ALIGN="LEFT"/>
      "conversation_complete": true,<BR ALIGN="LEFT"/>
      "current_stage": "end"<BR ALIGN="LEFT"/>
    }<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Flow Edges ---
    # Initial State to Sales
    g.edge('InitState', 'SalesProcess', label='User: "I need ₹50k for 12 months"', 
           color='#4299E1', penwidth='3')
    
    # Sales to State Update
    g.edge('SalesProcess', 'StateAfterSales', label='Extract & Store', color='#667EEA', penwidth='2.5')
    
    # State to Verification
    g.edge('StateAfterSales', 'VerifyProcess', label='Pass: customer_id', color='#4299E1', penwidth='3')
    
    # CRM Service to Verification
    g.edge('CRMService', 'VerifyProcess', label='Customer Profile Data', color='#E53E3E', 
           penwidth='2', style='dashed')
    
    # Verification to State
    g.edge('VerifyProcess', 'StateAfterVerify', label='Add: customer_data', color='#9F7AEA', penwidth='2.5')
    
    # State to Underwriting
    g.edge('StateAfterVerify', 'UnderwriteProcess', label='Pass: All Data', color='#4299E1', penwidth='3')
    
    # External Services to Underwriting
    g.edge('CreditService', 'UnderwriteProcess', label='Credit Score', color='#E53E3E', 
           penwidth='2', style='dashed')
    g.edge('OfferService', 'UnderwriteProcess', label='Interest Rate', color='#E53E3E', 
           penwidth='2', style='dashed')
    
    # Underwriting to State
    g.edge('UnderwriteProcess', 'StateAfterUnderwrite', label='Add: underwriting_result', 
           color='#ED8936', penwidth='2.5')
    
    # State to Sanction
    g.edge('StateAfterUnderwrite', 'SanctionProcess', label='Pass: customer_data + loan_details', 
           color='#4299E1', penwidth='3')
    
    # Sanction to Final State
    g.edge('SanctionProcess', 'FinalState', label='Add: sanction_letter_path', 
           color='#38B2AC', penwidth='2.5')

    # Render
    g.render(cleanup=True)
    print(f"✅ Data flow diagram generated: {output_basename}.png")
    print(f"   Shows complete state management and data passing between agents")

if __name__ == '__main__':
    create_data_flow_diagram()
