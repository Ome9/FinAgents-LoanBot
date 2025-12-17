# sequence_diagram.py
# Sequence Diagram for AI-ThreatSim showing temporal interaction flow
from graphviz import Digraph

def create_sequence_diagram(output_basename='sequence_diagram'):
    """
    Generates sequence diagram for AI-ThreatSim platform.
    Shows temporal flow of interactions between components during a battle.
    """
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes ---
    g.attr(rankdir='LR', splines='polyline', bgcolor='#FAFBFC', dpi='300',
           nodesep='1.8', ranksep='0.7')
    g.attr('node', shape='plain', fontname='Arial', fontsize='14')
    g.attr('edge', fontname='Arial', fontsize='12', color='#4A5568')

    # --- Actors/Components (Lifelines) ---
    # Note: All WIDTH attributes were already correctly removed.
    g.node('User', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#718096">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>👤 User</B></FONT></TD></TR>
  <TR><TD HEIGHT="25" BGCOLOR="#EDF2F7"></TD></TR>
</TABLE>>''')

    g.node('WebApp', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>🌐 Web App</B></FONT></TD></TR>
  <TR><TD HEIGHT="25" BGCOLOR="#BEE3F8"></TD></TR>
</TABLE>>''')

    g.node('LogParser', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#D69E2E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>📊 Log Parser</B></FONT></TD></TR>
  <TR><TD HEIGHT="25" BGCOLOR="#FEEBC8"></TD></TR>
</TABLE>>''')

    g.node('AttackerAI', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>⚔️ Attacker AI</B></FONT></TD></TR>
  <TR><TD HEIGHT="25" BGCOLOR="#FED7D7"></TD></TR>
</TABLE>>''')

    g.node('DefenderAI', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>🛡️ Defender AI</B></FONT></TD></TR>
  <TR><TD HEIGHT="25" BGCOLOR="#C6F6D5"></TD></TR>
</TABLE>>''')

    g.node('ActionExecutor', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>⚙️ Executor</B></FONT></TD></TR>
  <TR><TD HEIGHT="25" BGCOLOR="#FEEBC8"></TD></TR>
</TABLE>>''')

    g.node('BattleEngine', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#805AD5">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>🎯 Battle Engine</B></FONT></TD></TR>
  <TR><TD HEIGHT="25" BGCOLOR="#E9D8FD"></TD></TR>
</TABLE>>''')

    g.node('SelfPlay', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#D53F8C">
  <TR><TD HEIGHT="50"><FONT COLOR="#FFFFFF" POINT-SIZE="16"><B>🔄 Self-Play</B></FONT></TD></TR>
  <TR><TD HEIGHT="25" BGCOLOR="#FED7E2"></TD></TR>
</TABLE>>''')

    # --- Sequence Flow (Numbered Messages) ---
    # Step 1: User uploads log
    g.edge('User', 'WebApp', label='1. Upload Log File', color='#3182CE', penwidth='3', 
           constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 2: Web app sends to parser
    g.edge('WebApp', 'LogParser', label='2. Parse Log', color='#D69E2E', penwidth='3',
           constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 3: Parser extracts indicators
    g.edge('LogParser', 'WebApp', label='3. Return Indicators\n(IPs, Users, TTPs)', 
           color='#718096', penwidth='2.5', style='dashed', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 4: Send to Attacker AI
    g.edge('WebApp', 'AttackerAI', label='4. Generate Attack\nStrategy', color='#E53E3E', 
           penwidth='3', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 5: Attacker returns strategy
    g.edge('AttackerAI', 'WebApp', label='5. Attack Strategy\n(Commands, Tactics)', 
           color='#718096', penwidth='2.5', style='dashed', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 6: Send to Defender AI
    g.edge('WebApp', 'DefenderAI', label='6. Generate Defense\nResponse', color='#38A169', 
           penwidth='3', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 7: Defender returns response
    g.edge('DefenderAI', 'WebApp', label='7. Defense Strategy\n(Block, Isolate)', 
           color='#718096', penwidth='2.5', style='dashed', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 8: Execute defensive actions
    g.edge('WebApp', 'ActionExecutor', label='8. Execute Actions', color='#DD6B20', 
           penwidth='3', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 9: Return execution log
    g.edge('ActionExecutor', 'WebApp', label='9. Execution Log\n(Success/Fail)', 
           color='#718096', penwidth='2.5', style='dashed', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 10: Calculate battle result
    g.edge('WebApp', 'BattleEngine', label='10. Calculate Winner', color='#805AD5', 
           penwidth='3', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 11: Return battle result
    g.edge('BattleEngine', 'WebApp', label='11. Battle Result\n(Winner: Attacker/Defender)', 
           color='#718096', penwidth='2.5', style='dashed', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 12: Display to user
    g.edge('WebApp', 'User', label='12. Display Results\n(Scores, Logs)', color='#3182CE', 
           penwidth='3', style='bold', constraint='true', arrowhead='vee', fontsize='13')
    
    # Step 13: Async - Send to self-play (background)
    g.edge('BattleEngine', 'SelfPlay', label='13. [Async] Learn from Battle', 
           color='#D53F8C', penwidth='3', style='dotted', constraint='false', arrowhead='vee', fontsize='13')
    
    # Step 14: Extract winning strategies
    g.edge('SelfPlay', 'AttackerAI', label='14. Update Attacker\n(if lost)', 
           color='#E53E3E', penwidth='2.5', style='dotted', constraint='false', arrowhead='vee', fontsize='13')
    
    g.edge('SelfPlay', 'DefenderAI', label='15. Update Defender\n(if lost)', 
           color='#38A169', penwidth='2.5', style='dotted', constraint='false', arrowhead='vee', fontsize='13')

    # --- Add Legend ---
    with g.subgraph(name='cluster_legend') as c:
        c.attr(label='📖 Message Types', style='filled,rounded', color='#E2E8F0',
               fontname='Arial Black', fontsize='14', penwidth='2.5')
        
        c.node('legend', label='''<
<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="6">
  <TR><TD ALIGN="LEFT" HEIGHT="80"><FONT COLOR="#2D3748" POINT-SIZE="13">
    <B>→ Solid:</B> Synchronous request<BR ALIGN="LEFT"/>
    <B>⇢ Dashed:</B> Response/Return<BR ALIGN="LEFT"/>
    <B>⋯ Dotted:</B> Asynchronous/Background
  </FONT></TD></TR>
</TABLE>>''', shape='plain')

    return g

def main():
    """Main function to generate the sequence diagram."""
    print("🚀 Generating AI-ThreatSim Sequence Diagram...")
    try:
        diag = create_sequence_diagram()
        output_file = diag.render(cleanup=True)
        print(f"✅ Sequence diagram saved successfully as: {output_file}")
        print("📊 Shows: Temporal interaction flow during AI battle (15 steps)")
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")
        print("💡 Make sure graphviz is installed and in your system's PATH.")

if __name__ == '__main__':
    main()