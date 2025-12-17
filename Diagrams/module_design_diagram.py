# module_design_diagram.py
# Generates a detailed module design diagram for the detection lab.
from graphviz import Digraph

def create_module_design_diagram(output_basename='module_design'):
    """Generates an enhanced, professional-grade module design diagram."""
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes for a Vertical Layout ---
    g.attr(rankdir='TB', splines='ortho', bgcolor='#FFFFFF', compound='true',
           label='High-Level Module Design: AI-Driven Detection Lab', labelloc='t',
           fontname='Arial', fontsize='18', fontcolor='#2D3748')
    
    g.attr('node', shape='plain', fontname='Arial', fontsize='11')
    g.attr('edge', fontname='Arial', fontsize='9', color='#4A5568')

    # --- 1. Frontend Layer ---
    with g.subgraph(name='cluster_frontend') as c:
        c.attr(label='Frontend Layer', style='filled,rounded', color='#EBF4FF', 
               fontname='Arial', fontcolor='#4C51BF', penwidth='2')
        c.node('UI', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#4C51BF">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🎨 User Interface</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Web Dashboard (React/Gradio)<BR/>
    • Simulation Control &amp; Scheduling<BR/>
    • Results Visualization (Heatmaps)<BR/>
    • Report Access<BR/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- 2. Backend Services Layer ---
    with g.subgraph(name='cluster_backend') as c:
        c.attr(label='Backend Services', style='filled,rounded', color='#EBF8FF', 
               fontname='Arial', fontcolor='#2C5282', penwidth='2')
        c.node('API_Gateway', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🔌 API Gateway</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Handles UI Requests<BR/>
    • Authentication &amp; Authorization<BR/>
    • Routes to Internal Services<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        c.node('Orchestration_Engine', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">⚙️ Orchestration Engine</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Manages Simulation Lifecycle<BR/>
    • Executes Scenarios via Connectors<BR/>
    • Task Scheduling &amp; State Mgmt<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        c.node('Config_Store', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🗳️ Config &amp; Results Store</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Stores Attack Scenarios (YAML/JSON)<BR/>
    • Caches Simulation Results<BR/>
    • Manages User Settings (SQL/NoSQL)<BR/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- 3. Simulation Connectors Layer ---
    with g.subgraph(name='cluster_connectors') as c:
        c.attr(label='Simulation Connectors', style='filled,rounded', color='#F0FFF4', 
               fontname='Arial', fontcolor='#2F855A', penwidth='2')
        c.node('Win_Connector', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD><FONT COLOR="#FFFFFF">🖥️ Windows Connector</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Interfaces with Splunk Attack Range<BR/>
    • Translates commands for Atomic Red Team<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        c.node('Linux_Connector', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD><FONT COLOR="#FFFFFF">🐧 Linux Connector</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Interfaces with Caldera API<BR/>
    • Deploys/Manages Caldera Agents<BR/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- 4. External Systems (Represented as simple nodes) ---
    with g.subgraph(name='cluster_external') as c:
        c.attr(label='External & Target Systems', style='dashed,rounded', color='#A0AEC0', 
               fontname='Arial', fontcolor='#4A5568')
        c.node('Target_Env', '🎯 Target Environment\n(Isolated VMs)', shape='box3d', style='filled', fillcolor='#EDF2F7')
        c.node('SIEM_External', '📊 External SIEM\n(Splunk/Elastic)', shape='box3d', style='filled', fillcolor='#EDF2F7')

    # --- 5. Data & Analysis Layer ---
    with g.subgraph(name='cluster_analysis') as c:
        c.attr(label='Data & Analysis Layer', style='filled,rounded', color='#FEFCBF', 
               fontname='Arial', fontcolor='#B7791F', penwidth='2')
        c.node('Telemetry_Collector', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">📡 Telemetry Collector</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Gathers logs via Forwarders<BR/>
    • Normalizes data formats<BR/>
    • Forwards to SIEM for ingestion<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        c.node('AI_Engine', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🤖 AI Analysis Engine</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Queries SIEM for detection events<BR/>
    • Maps events to MITRE ATT&amp;CK<BR/>
    • Uses LLMs for summary &amp; analysis<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        c.node('Reporting_Module', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">📄 Reporting Module</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Generates PDF &amp; Markdown reports<BR/>
    • Creates coverage heatmaps<BR/>
    • Pushes reports to GitHub<BR/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Edges (Control & Data Flows) ---
    # Control Flow (Solid Lines)
    g.edge('UI', 'API_Gateway', label='User Actions')
    g.edge('API_Gateway', 'Orchestration_Engine', label='Start/Stop Simulation')
    g.edge('API_Gateway', 'Config_Store', label='Get/Set Config')
    g.edge('Orchestration_Engine', 'Config_Store', label='Read Scenarios')
    g.edge('Orchestration_Engine', 'Win_Connector', label='Execute Win Task')
    g.edge('Orchestration_Engine', 'Linux_Connector', label='Execute Linux Task')
    g.edge('Win_Connector', 'Target_Env', label='Run TTPs')
    g.edge('Linux_Connector', 'Target_Env', label='Run TTPs')

    # Data Flow (Dashed Lines)
    g.edge('Target_Env', 'Telemetry_Collector', label='Logs & Events', style='dashed')
    g.edge('Telemetry_Collector', 'SIEM_External', label='Ingest Data', style='dashed')
    g.edge('SIEM_External', 'AI_Engine', label='Query Detections', style='dashed', penwidth='2.0', color='#B7791F')
    g.edge('AI_Engine', 'Reporting_Module', label='Analysis Results', style='dashed')
    g.edge('Reporting_Module', 'Config_Store', label='Save Reports', style='dashed')
    g.edge('Config_Store', 'UI', label='Load Reports/Results', style='dashed')
    
    return g

def main():
    """Main function to generate the module design diagram."""
    print("🚀 Generating Enhanced Module Design Diagram...")
    try:
        diag = create_module_design_diagram()
        output_file = diag.render(cleanup=True)
        print(f"✅ Module design diagram saved successfully as: {output_file}")
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")
        print("💡 Make sure graphviz is installed and in your system's PATH.")

if __name__ == "__main__":
    main()