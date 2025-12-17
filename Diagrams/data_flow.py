# data_flow.py
# Data Flow Diagram for AI-ThreatSim showing: Log Upload → Parsing → AI Analysis → Battle → Learning
from graphviz import Digraph

def create_data_flow_diagram(output_basename='data_flow'):
    """
    Generates data flow diagram for AI-ThreatSim platform.
    Shows complete workflow from log upload to model improvement.
    """
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes ---
    # Using TB (top-to-bottom) but with rank='same' to create a grid/square layout
    g.attr(rankdir='TB', splines='spline', bgcolor='#FAFBFC', dpi='300', 
           nodesep='1.5', ranksep='1.0')
    g.attr('node', shape='plain', fontname='Arial', fontsize='14')
    g.attr('edge', fontname='Arial', fontsize='12')

    # --- External Entity: User ---
    # Note: All WIDTH attributes were already correctly removed.
    g.node('User', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#718096">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>👤 Security Analyst</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="100"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Uploads:</B><BR ALIGN="LEFT"/>
    • Real security logs<BR ALIGN="LEFT"/>
    • System configuration<BR ALIGN="LEFT"/>
    • Log type selection<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 1: Web Server ---
    g.node('WebServer', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>🌐 FastAPI Server</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="100"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Receives POST /api/battle<BR ALIGN="LEFT"/>
    • Validates file upload<BR ALIGN="LEFT"/>
    • Routes to RealLogParser<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 2: Log Parser ---
    g.node('LogParser', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>🔍 Real Log Parser</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Regex pattern matching<BR ALIGN="LEFT"/>
    • Extract attack indicators<BR ALIGN="LEFT"/>
    • Tag MITRE ATT&amp;CK TTPs<BR ALIGN="LEFT"/>
    • Convert to attack description<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store 1: Attack Indicators ---
    g.node('Indicators', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#3182CE" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>📋 Attack Indicators</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="140"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Failed login IPs + counts<BR ALIGN="LEFT"/>
    • Privilege escalation commands<BR ALIGN="LEFT"/>
    • Port scan sources<BR ALIGN="LEFT"/>
    • Compromised user accounts<BR ALIGN="LEFT"/>
    • MITRE TTP IDs (T1110, T1548...)<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 3: Attacker AI Inference ---
    g.node('AttackerInference', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>⚔️ Attacker Model</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Load attacker_lora adapter<BR ALIGN="LEFT"/>
    • Generate attack strategy<BR ALIGN="LEFT"/>
    • Map TTPs to exploitation steps<BR ALIGN="LEFT"/>
    • Create realistic attack commands<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store 2: Attack Strategy ---
    g.node('AttackStrategy', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#E53E3E" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>🎯 Attack Strategy</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Multi-stage attack plan<BR ALIGN="LEFT"/>
    • Exploitation techniques<BR ALIGN="LEFT"/>
    • Post-exploitation goals<BR ALIGN="LEFT"/>
    • Attack score (0-100)<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 4: Defender AI Inference ---
    g.node('DefenderInference', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>🛡️ Defender Model</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Load defender_lora adapter<BR ALIGN="LEFT"/>
    • Analyze attack strategy<BR ALIGN="LEFT"/>
    • Generate countermeasures<BR ALIGN="LEFT"/>
    • Create defensive action list<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store 3: Defense Strategy ---
    g.node('DefenseStrategy', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#38A169" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>🛡️ Defense Strategy</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Mitigation recommendations<BR ALIGN="LEFT"/>
    • Defensive commands (iptables...)<BR ALIGN="LEFT"/>
    • MITRE D3FEND mappings<BR ALIGN="LEFT"/>
    • Defense score (0-100)<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 5: Action Executor ---
    g.node('ActionExecutor', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>⚡ Action Executor</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Execute block_ip_address()<BR ALIGN="LEFT"/>
    • Execute enable_fail2ban()<BR ALIGN="LEFT"/>
    • Execute reset_password()<BR ALIGN="LEFT"/>
    • dry_run mode validation<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store 4: Execution Log ---
    g.node('ExecutionLog', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#DD6B20" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>📝 Execution Log</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Action status (simulated/executed)<BR ALIGN="LEFT"/>
    • Commands generated<BR ALIGN="LEFT"/>
    • Timestamps<BR ALIGN="LEFT"/>
    • Error messages (if any)<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 6: Battle Result Calculator ---
    g.node('BattleCalculator', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#805AD5">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>🏆 Battle Calculator</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Compare attack vs defense scores<BR ALIGN="LEFT"/>
    • Determine winner<BR ALIGN="LEFT"/>
    • Generate statistics<BR ALIGN="LEFT"/>
    • Log to selfplay.jsonl<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store 5: Battle Results ---
    g.node('BattleResults', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#805AD5" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>📊 Battle Results</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Winner (Attacker/Defender)<BR ALIGN="LEFT"/>
    • Final scores<BR ALIGN="LEFT"/>
    • Statistics (failed_logins...)<BR ALIGN="LEFT"/>
    • Complete battle JSON<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 7: Adversarial Learning (Background) ---
    g.node('AdversarialLearning', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>🔄 Adversarial Learning</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Run self-play episodes<BR ALIGN="LEFT"/>
    • Extract winning strategies<BR ALIGN="LEFT"/>
    • Generate adaptation data<BR ALIGN="LEFT"/>
    • Append to training sets<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Data Store 6: Adaptation Data ---
    g.node('AdaptationData', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFFFFF">
  <TR><TD BGCOLOR="#E53E3E" HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>📈 Adaptation Data</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • attacker_adaptations.jsonl<BR ALIGN="LEFT"/>
    • defender_adaptations.jsonl<BR ALIGN="LEFT"/>
    • Winning strategies<BR ALIGN="LEFT"/>
    • New training examples<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Process 8: Model Retraining ---
    g.node('Retraining', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>🔁 Model Retraining</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="120"><FONT COLOR="#2D3748" POINT-SIZE="13">
    • Augment training datasets<BR ALIGN="LEFT"/>
    • Retrain losing model<BR ALIGN="LEFT"/>
    • Generate new adapter<BR ALIGN="LEFT"/>
    • Deploy updated model<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- External Entity: User Response ---
    g.node('UserResponse', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#718096">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="18"><B>🖥️ Browser UI</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF" HEIGHT="100"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>Displays:</B><BR ALIGN="LEFT"/>
    • Winner badge<BR ALIGN="LEFT"/>
    • Attack/Defense panels<BR ALIGN="LEFT"/>
    • Statistics grid<BR ALIGN="LEFT"/>
    • Action execution log<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- DATA FLOWS ---
    # Phase 1: Log Upload & Parsing
    g.edge('User', 'WebServer', label='Log file +\nconfig', penwidth='4', color='#48BB78', fontsize='12')
    g.edge('WebServer', 'LogParser', label='Raw log\ndata', penwidth='4', color='#48BB78', fontsize='12')
    g.edge('LogParser', 'Indicators', label='Parsed\nindicators', penwidth='4', color='#E53E3E', fontsize='12')

    # Phase 2: AI Inference
    g.edge('Indicators', 'AttackerInference', label='Attack\ncontext', penwidth='4', color='#3182CE', fontsize='12')
    g.edge('AttackerInference', 'AttackStrategy', label='Generated\nattack', penwidth='4', color='#E53E3E', fontsize='12')
    g.edge('AttackStrategy', 'DefenderInference', label='Attack\nintel', penwidth='4', color='#3182CE', fontsize='12')
    g.edge('Indicators', 'DefenderInference', label='System\nstate', penwidth='3', color='#3182CE', style='dashed', fontsize='12')
    g.edge('DefenderInference', 'DefenseStrategy', label='Generated\ndefense', penwidth='4', color='#38A169', fontsize='12')

    # Phase 3: Action Execution
    g.edge('DefenseStrategy', 'ActionExecutor', label='Action\ncommands', penwidth='4', color='#DD6B20', fontsize='12')
    g.edge('ActionExecutor', 'ExecutionLog', label='Execution\nresults', penwidth='4', color='#DD6B20', fontsize='12')

    # Phase 4: Battle Results
    g.edge('AttackStrategy', 'BattleCalculator', label='Attack\nscore', style='dotted', penwidth='2', fontsize='11')
    g.edge('DefenseStrategy', 'BattleCalculator', label='Defense\nscore', style='dotted', penwidth='2', fontsize='11')
    g.edge('ExecutionLog', 'BattleCalculator', label='Action\neffectiveness', style='dotted', penwidth='2', fontsize='11')
    g.edge('BattleCalculator', 'BattleResults', label='Final\nresults', penwidth='4', color='#805AD5', fontsize='12')
    g.edge('BattleResults', 'UserResponse', label='JSON\nresponse', penwidth='4', color='#9F7AEA', fontsize='12')

    # Phase 5: Adversarial Learning (Background Process)
    g.edge('BattleResults', 'AdversarialLearning', label='Win/loss\ndata', penwidth='3', color='#E53E3E', style='dashed', fontsize='12')
    g.edge('AdversarialLearning', 'AdaptationData', label='Extracted\nstrategies', penwidth='3', color='#E53E3E', style='dashed', fontsize='12')
    g.edge('AdaptationData', 'Retraining', label='New\nexamples', penwidth='3', color='#38A169', style='dashed', fontsize='12')
    g.edge('Retraining', 'AttackerInference', label='Updated\nmodel', penwidth='3', color='#38A169', style='dotted', constraint='false', fontsize='12')
    g.edge('Retraining', 'DefenderInference', label='Updated\nmodel', penwidth='3', color='#38A169', style='dotted', constraint='false', fontsize='12')

    # --- Layout Grouping for Square/Grid Shape ---
    # Row 1: User Input
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('User')
        s.node('WebServer')
        s.node('LogParser')

    # Row 2: Data Store + AI Models
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('Indicators')
        s.node('AttackerInference')
        s.node('DefenderInference')

    # Row 3: Strategies
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('AttackStrategy')
        s.node('DefenseStrategy')
        s.node('ActionExecutor')

    # Row 4: Execution & Results
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('ExecutionLog')
        s.node('BattleCalculator')
        s.node('BattleResults')
        
    # Row 5: Output & Learning
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('UserResponse')
        s.node('AdversarialLearning')
        s.node('AdaptationData')
        
    # Row 6: Retraining
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('Retraining')

    return g

def main():
    """Main function to generate the data flow diagram."""
    print("🚀 Generating AI-ThreatSim Data Flow Diagram...")
    try:
        diag = create_data_flow_diagram()
        output_file = diag.render(cleanup=True)
        print(f"✅ Data flow diagram saved successfully as: {output_file}")
        print("📊 Shows: Upload → Parse → AI Battle → Execute → Learn → Improve")
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")
        print("💡 Make sure graphviz is installed and in your system's PATH.")

if __name__ == "__main__":
    main()