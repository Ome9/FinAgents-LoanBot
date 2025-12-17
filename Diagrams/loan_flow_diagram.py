# loan_flow_diagram.py
# End-to-End Customer Journey Flowchart for Loan Application
# Shows: User Input → Sales → Verification → Underwriting → Approval/Rejection → Sanction Letter
from graphviz import Digraph

def create_flow_diagram(output_basename='loan_flow_diagram'):
    """
    Generates customer journey flowchart for loan application process.
    High-quality, compact design with minimal white space for slide display.
    """
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes (Optimized for Compactness) ---
    g.attr(rankdir='TB', splines='polyline', bgcolor='#FFFFFF', dpi='300')
    g.attr('node', shape='box', style='rounded,filled', fontname='Arial Bold', fontsize='16', 
           fillcolor='#E2E8F0', color='#2D3748', penwidth='3', margin='0.3,0.15')
    g.attr('edge', fontname='Arial', fontsize='14', color='#2D3748', penwidth='2.5', 
           len='0.5', minlen='1')
    g.attr(nodesep='0.3', ranksep='0.4')  # Minimize spacing
    g.attr(size='20,30!')  # Taller, narrower for less white space

    # --- Start Node ---
    g.node('Start', 'START\n👤 User Visits Chatbot', shape='ellipse', fillcolor='#48BB78', 
           fontcolor='white', fontsize='18', width='2.8', height='0.9', penwidth='3')

    # --- Stage 1: Authentication ---
    g.node('Auth', '🔐 AUTHENTICATION\nEnter Customer ID\n(Existing Customer)', fillcolor='#4299E1', 
           fontcolor='white', width='3.2', height='0.95', penwidth='3')
    
    # --- Stage 2: Sales Conversation ---
    g.node('Sales', '💬 SALES AGENT (AI)\nConversational Interface\nUser: "I need ₹50,000 for 12 months"\nAI: Understands & Extracts Requirements', 
           fillcolor='#667EEA', fontcolor='white', width='4.5', height='1.3', penwidth='3')
    
    # --- Stage 3: Confirmation ---
    g.node('ConfirmSales', 'CONFIRM\nLOAN DETAILS?\n━━━━━━━━\nAmount: ₹50,000\nTenure: 12 months', 
           shape='diamond', fillcolor='#F6AD55', fontcolor='white', width='3.5', height='1.8', penwidth='3')
    
    # --- Stage 4: Verification ---
    g.node('Verify', '✅ VERIFICATION AGENT\nFetch Customer Profile from CRM:\n━━━━━━━━━━━━━━━━\n• Full Name & Contact Details\n• Pre-approved Limit: ₹3,00,000\n• Existing Credit Score: 780', 
           fillcolor='#9F7AEA', fontcolor='white', width='4.8', height='1.5', penwidth='3')
    
    g.node('ConfirmVerify', 'ALL DETAILS\nCORRECT?', shape='diamond', fillcolor='#F6AD55', 
           fontcolor='white', width='2.8', height='1.5', penwidth='3')
    
    # --- Stage 5: Underwriting ---
    g.node('Underwrite', '📊 UNDERWRITING AGENT\nCredit Assessment Process:\n━━━━━━━━━━━━━━━━\n1. Fetch Latest Credit Score\n2. Compare Loan Amount vs Pre-approved Limit\n3. Calculate Monthly EMI\n4. Apply Eligibility Rules', 
           fillcolor='#ED8936', fontcolor='white', width='5', height='1.6', penwidth='3')
    
    # --- Decision: Credit Score ---
    g.node('CheckScore', 'CREDIT SCORE\n≥ 700?', shape='diamond', fillcolor='#FC8181', 
           fontcolor='white', width='2.8', height='1.5', penwidth='3')
    
    # --- Decision: Loan Amount ---
    g.node('CheckAmount', 'AMOUNT ≤\nPRE-APPROVED\nLIMIT?', shape='diamond', fillcolor='#FC8181', 
           fontcolor='white', width='3', height='1.6', penwidth='3')
    
    g.node('CheckConditional', 'AMOUNT ≤\n2× LIMIT?', shape='diamond', fillcolor='#FC8181', 
           fontcolor='white', width='2.8', height='1.5', penwidth='3')
    
    # --- Salary Slip Upload (Conditional) ---
    g.node('SalaryUpload', '📄 CONDITIONAL APPROVAL\nUpload Salary Slip for Verification\n━━━━━━━━━━━━━━\nValidate: EMI ≤ 50% Monthly Salary', 
           fillcolor='#F6AD55', fontcolor='white', width='4.5', height='1.3', penwidth='3')
    
    g.node('EMICheck', 'EMI ≤ 50%\nSALARY?', shape='diamond', fillcolor='#FC8181', 
           fontcolor='white', width='2.8', height='1.5', penwidth='3')
    
    # --- Approval Outcome ---
    g.node('Approved', '🎉 LOAN APPROVED!\n━━━━━━━━━━━\nDecision: Instant/Conditional Approval\nNext: Generate Sanction Letter', 
           fillcolor='#48BB78', fontcolor='white', width='4.2', height='1.2', penwidth='3')
    
    # --- Rejection Outcome ---
    g.node('Rejected', '❌ LOAN REJECTED\n━━━━━━━━━━━\nReason: Credit Score/Amount/EMI\nSuggestion: Apply for Lower Amount\nAlternative: Improve Credit & Reapply', 
           fillcolor='#F56565', fontcolor='white', width='4.5', height='1.4', penwidth='3')
    
    # --- Stage 6: Sanction Letter ---
    g.node('Sanction', '📄 SANCTION LETTER GENERATOR\nCreating Professional PDF Document:\n━━━━━━━━━━━━━━━━━━\n• Loan Account Number & Details\n• EMI Schedule & Interest Rate\n• Terms & Conditions\n• Digital Signature Section', 
           fillcolor='#38B2AC', fontcolor='white', width='5.2', height='1.6', penwidth='3')
    
    g.node('ChooseDownload', 'DELIVERY\nMETHOD?\n━━━━━━\nDownload Now\nOR\nEmail Later', shape='diamond', 
           fillcolor='#F6AD55', fontcolor='white', width='3.2', height='1.8', penwidth='3')
    
    g.node('Download', '📥 INSTANT DOWNLOAD\nPDF Sanction Letter\nReady for Print/Save', fillcolor='#38B2AC', 
           fontcolor='white', width='3.5', height='1.1', penwidth='3')
    
    g.node('Email', '📧 EMAIL DELIVERY\nSanction Letter Sent to:\nregistered@email.com\nDelivery Time: 24 hours', 
           fillcolor='#38B2AC', fontcolor='white', width='3.8', height='1.2', penwidth='3')
    
    # --- End Node ---
    g.node('End', 'END\n✅ Process Complete', shape='ellipse', fillcolor='#48BB78', 
           fontcolor='white', fontsize='18', width='2.8', height='0.9', penwidth='3')

    # --- Flow Connections (Compact, Bold Labels) ---
    # Start to Auth
    g.edge('Start', 'Auth', label=' Open Chat ', fontsize='15', labeldistance='1.5')
    
    # Auth to Sales
    g.edge('Auth', 'Sales', label=' ID: CUST001 ', fontsize='15')
    
    # Sales to Confirmation
    g.edge('Sales', 'ConfirmSales', label=' Extract Data ', fontsize='15')
    
    # Confirmation YES
    g.edge('ConfirmSales', 'Verify', label=' ✅ YES\nProceed ', color='#48BB78', penwidth='4', fontsize='15')
    
    # Confirmation NO (loop back)
    g.edge('ConfirmSales', 'Sales', label=' ❌ NO\nEdit ', color='#F56565', 
           style='dashed', penwidth='2', constraint='false', fontsize='14')
    
    # Verify to Confirmation
    g.edge('Verify', 'ConfirmVerify', label=' Show Profile ', fontsize='15')
    
    # Verify Confirmation YES
    g.edge('ConfirmVerify', 'Underwrite', label=' ✅ Confirmed ', color='#48BB78', penwidth='4', fontsize='15')
    
    # Verify Confirmation NO
    g.edge('ConfirmVerify', 'Sales', label=' ❌ Fix ', color='#F56565', style='dashed', 
           penwidth='2', fontsize='14')
    
    # Underwriting to Credit Check
    g.edge('Underwrite', 'CheckScore', label=' Get Score ', fontsize='15')
    
    # Credit Score < 700 → Reject
    g.edge('CheckScore', 'Rejected', label=' ❌ NO\n< 700 ', color='#F56565', penwidth='4', fontsize='15')
    
    # Credit Score ≥ 700 → Check Amount
    g.edge('CheckScore', 'CheckAmount', label=' ✅ YES\n≥ 700 ', color='#48BB78', penwidth='4', fontsize='15')
    
    # Amount ≤ Pre-approved → Instant Approval
    g.edge('CheckAmount', 'Approved', label=' ✅ YES\nInstant ', color='#48BB78', penwidth='4', fontsize='15')
    
    # Amount > Pre-approved → Check 2x
    g.edge('CheckAmount', 'CheckConditional', label=' ❌ NO\n> Limit ', color='#ED8936', penwidth='3', fontsize='15')
    
    # 2x Check YES → Salary Upload
    g.edge('CheckConditional', 'SalaryUpload', label=' ✅ YES\n≤ 2× ', 
           color='#F6AD55', penwidth='3', fontsize='15')
    
    # 2x Check NO → Reject
    g.edge('CheckConditional', 'Rejected', label=' ❌ NO\nToo High ', color='#F56565', penwidth='4', fontsize='15')
    
    # Salary Upload to EMI Check
    g.edge('SalaryUpload', 'EMICheck', label=' Calc EMI ', fontsize='15')
    
    # EMI Check YES → Approve
    g.edge('EMICheck', 'Approved', label=' ✅ YES\n≤ 50% ', color='#48BB78', penwidth='4', fontsize='15')
    
    # EMI Check NO → Reject
    g.edge('EMICheck', 'Rejected', label=' ❌ NO\n> 50% ', color='#F56565', penwidth='4', fontsize='15')
    
    # Approved to Sanction
    g.edge('Approved', 'Sanction', label=' Create PDF ', color='#48BB78', penwidth='4', fontsize='15')
    
    # Sanction to Choice
    g.edge('Sanction', 'ChooseDownload', label=' PDF Ready ', fontsize='15')
    
    # Download Choice
    g.edge('ChooseDownload', 'Download', label=' Now ', color='#38B2AC', penwidth='3', fontsize='15')
    g.edge('ChooseDownload', 'Email', label=' Later ', color='#667EEA', penwidth='3', fontsize='15')
    
    # Both choices to End
    g.edge('Download', 'End', label=' Done ', color='#48BB78', penwidth='3', fontsize='15')
    g.edge('Email', 'End', label=' Done ', color='#48BB78', penwidth='3', fontsize='15')
    
    # Rejected to End
    g.edge('Rejected', 'End', label=' Try Lower\nAmount ', color='#F56565', style='dashed', 
           penwidth='2', fontsize='14')

    # Render
    g.render(cleanup=True)
    print(f"✅ High-quality flow diagram generated: {output_basename}.png")
    print("   - Resolution: 300 DPI (double previous quality)")
    print("   - Font size: 16pt (more readable)")
    print("   - Spacing: Minimized for compact display")
    print("   - Details: Enhanced with separators and context")
    print("   Ready for slide insertion and zoom-in viewing!")


if __name__ == '__main__':
    create_flow_diagram()
