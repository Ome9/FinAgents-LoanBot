# loan_architecture_diagram.py
# Master-Worker Architecture for Agentic AI Loan Sales Chatbot
# Shows: Frontend → Master Agent → 4 Worker Agents → External Services
from graphviz import Digraph

def create_architecture_diagram(output_basename='loan_architecture_diagram'):
    """
    Generates Master-Worker architecture diagram for loan chatbot.
    Optimized for 16:9 slide ratio (1920x1080 or 1280x720 pixels).
    """
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes (Optimized for slide display) ---
    g.attr(rankdir='TB', splines='ortho', bgcolor='#FFFFFF', compound='true', dpi='150')
    g.attr('node', shape='plain', fontname='Arial', fontsize='14')
    g.attr('edge', fontname='Arial', fontsize='12', color='#4A5568')
    g.attr(size='16,9', ratio='fill')  # 16:9 aspect ratio for slides

    # --- Frontend Layer ---
    with g.subgraph(name='cluster_frontend') as c:
        c.attr(label='🖥️ FRONTEND LAYER - User Interface', style='filled,rounded', 
               color='#BEE3F8', fontname='Arial Black', fontcolor='#2C5282', 
               penwidth='3', fontsize='16')
        
        c.node('ReactUI', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD HEIGHT="60"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>💬 React Chat Interface</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="14">
    <B>Components:</B><BR ALIGN="LEFT"/>
    • ChatInterface.jsx (main UI)<BR ALIGN="LEFT"/>
    • QuickReplyButtons (interactive)<BR ALIGN="LEFT"/>
    • Progress Tracker (4 stages)<BR ALIGN="LEFT"/>
    • File Upload (salary slip)<BR ALIGN="LEFT"/>
    • PDF Download Button<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Tech:</B> React 18 + Vite + TailwindCSS<BR ALIGN="LEFT"/>
    <B>Port:</B> 5173 (localhost)<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Backend Master Layer ---
    with g.subgraph(name='cluster_master') as c:
        c.attr(label='🧠 MASTER AGENT LAYER - Orchestrator', style='filled,rounded', 
               color='#FAF089', fontname='Arial Black', fontcolor='#744210', 
               penwidth='3', fontsize='16')
        
        c.node('MasterAgent', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#D69E2E">
  <TR><TD HEIGHT="60"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>⚙️ Master Agent (LangGraph)</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="140"><FONT COLOR="#2D3748" POINT-SIZE="14">
    <B>Responsibilities:</B><BR ALIGN="LEFT"/>
    • Workflow orchestration (StateGraph)<BR ALIGN="LEFT"/>
    • State management (messages, data)<BR ALIGN="LEFT"/>
    • Routing to worker agents<BR ALIGN="LEFT"/>
    • Confirmation stage handling<BR ALIGN="LEFT"/>
    • Data validation between stages<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Framework:</B> LangGraph 0.2.62<BR ALIGN="LEFT"/>
    <B>File:</B> backend/agents/master_agent.py<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Worker Agents Layer ---
    with g.subgraph(name='cluster_workers') as c:
        c.attr(label='👷 WORKER AGENTS LAYER - Specialized Tasks', style='filled,rounded', 
               color='#C6F6D5', fontname='Arial Black', fontcolor='#22543D', 
               penwidth='3', fontsize='16')
        
        # Sales Agent
        c.node('SalesAgent', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>💼 Sales Agent</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="110"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Role:</B> Conversational AI<BR ALIGN="LEFT"/>
    <B>Tasks:</B><BR ALIGN="LEFT"/>
    • Engage customer (natural chat)<BR ALIGN="LEFT"/>
    • Collect loan requirements<BR ALIGN="LEFT"/>
    • Extract amount &amp; tenure<BR ALIGN="LEFT"/>
    • Present pre-approved offers<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>AI Model:</B> Perplexity Sonar<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        # Verification Agent
        c.node('VerificationAgent', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#805AD5">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>✅ Verification Agent</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="110"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Role:</B> KYC Validator<BR ALIGN="LEFT"/>
    <B>Tasks:</B><BR ALIGN="LEFT"/>
    • Fetch customer profile<BR ALIGN="LEFT"/>
    • Validate identity (CRM data)<BR ALIGN="LEFT"/>
    • Get pre-approved limit<BR ALIGN="LEFT"/>
    • Confirm customer details<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Integration:</B> Mock CRM API<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        # Underwriting Agent
        c.node('UnderwritingAgent', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📊 Underwriting Agent</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="110"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Role:</B> Credit Assessor<BR ALIGN="LEFT"/>
    <B>Tasks:</B><BR ALIGN="LEFT"/>
    • Fetch credit score (bureau)<BR ALIGN="LEFT"/>
    • Apply 3-tier approval logic<BR ALIGN="LEFT"/>
    • Calculate EMI &amp; interest<BR ALIGN="LEFT"/>
    • Generate loan decision<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Rules:</B> Score≥700, EMI≤50%<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        # Sanction Letter Agent
        c.node('SanctionAgent', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📄 Sanction Letter Gen</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="110"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Role:</B> Document Generator<BR ALIGN="LEFT"/>
    <B>Tasks:</B><BR ALIGN="LEFT"/>
    • Create professional PDF<BR ALIGN="LEFT"/>
    • Add loan details table<BR ALIGN="LEFT"/>
    • Include terms &amp; conditions<BR ALIGN="LEFT"/>
    • Generate download link<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Library:</B> ReportLab<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- External Services Layer ---
    with g.subgraph(name='cluster_services') as c:
        c.attr(label='🔌 EXTERNAL SERVICES - Data Sources', style='filled,rounded', 
               color='#FED7D7', fontname='Arial Black', fontcolor='#742A2A', 
               penwidth='3', fontsize='16')
        
        c.node('MockCRM', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>👤 Mock CRM</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="90"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Customer profiles (12)<BR ALIGN="LEFT"/>
    • Pre-approved limits<BR ALIGN="LEFT"/>
    • Contact info<BR ALIGN="LEFT"/>
    <B>API:</B> /api/crm/customer/{id}<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('CreditBureau', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📈 Credit Bureau</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="90"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Credit scores (CIBIL)<BR ALIGN="LEFT"/>
    • Credit ratings<BR ALIGN="LEFT"/>
    • Score range: 300-900<BR ALIGN="LEFT"/>
    <B>API:</B> /api/credit-bureau/score/{id}<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('OfferMart', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>💰 Offer Mart</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="90"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Interest rate tiers<BR ALIGN="LEFT"/>
    • Pre-approved offers<BR ALIGN="LEFT"/>
    • Rate: 10.5% - 15%<BR ALIGN="LEFT"/>
    <B>API:</B> /api/offers/preapproved/{id}<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Connection Flows ---
    # Frontend to Master
    g.edge('ReactUI', 'MasterAgent', label='HTTP/REST\n(Axios)', color='#3182CE', 
           penwidth='3', fontsize='13', style='bold', arrowhead='vee')
    
    # Master to Workers (orchestration)
    g.edge('MasterAgent', 'SalesAgent', label='1. Sales Stage', color='#3182CE', 
           penwidth='2.5', fontsize='12', constraint='true')
    g.edge('MasterAgent', 'VerificationAgent', label='2. Verify Stage', color='#805AD5', 
           penwidth='2.5', fontsize='12', constraint='true')
    g.edge('MasterAgent', 'UnderwritingAgent', label='3. Underwrite Stage', color='#DD6B20', 
           penwidth='2.5', fontsize='12', constraint='true')
    g.edge('MasterAgent', 'SanctionAgent', label='4. Sanction Stage', color='#38A169', 
           penwidth='2.5', fontsize='12', constraint='true')
    
    # Workers to Services
    g.edge('SalesAgent', 'OfferMart', label='Get Pre-approved\nOffers', color='#718096', 
           penwidth='2', fontsize='11', style='dashed')
    g.edge('VerificationAgent', 'MockCRM', label='Fetch Customer\nProfile', color='#718096', 
           penwidth='2', fontsize='11', style='dashed')
    g.edge('UnderwritingAgent', 'CreditBureau', label='Get Credit\nScore', color='#718096', 
           penwidth='2', fontsize='11', style='dashed')
    g.edge('UnderwritingAgent', 'OfferMart', label='Get Interest\nRates', color='#718096', 
           penwidth='2', fontsize='11', style='dashed')

    # Render
    g.render(cleanup=True)
    print(f"✅ Architecture diagram generated: {output_basename}.png")
    print(f"   Optimized for 16:9 slide display (1920x1080 or 1280x720)")

if __name__ == '__main__':
    create_architecture_diagram()
