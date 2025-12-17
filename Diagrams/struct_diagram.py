# structural_diagram.py
# Generates a structural/component diagram for your detection lab using graphviz
from graphviz import Digraph

def create_structural_diagram(output_basename='structural_diagram'):
    """Generates an enhanced, professional-grade structural diagram."""
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes ---
    g.attr(rankdir='LR', splines='spline', bgcolor='#FAFBFC', compound='true',
           label='System Architecture: AI-Driven Detection Engineering Lab', labelloc='t',
           fontname='Arial', fontsize='18', fontcolor='#2D3748')
    
    g.attr('node', shape='plain', fontname='Arial', fontsize='11')
    g.attr('edge', fontname='Arial', fontsize='9', color='#4A5568')

    # --- Component Definitions using HTML-like Labels for Rich Formatting ---

    # 1. Control & Orchestration Layer (Left Column)
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('Dashboard', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🎨 Dashboard &amp; API</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#EBF8FF"><FONT COLOR="#2D3748">
    • User Interface (Gradio/React)<BR/>
    • Control API Gateway<BR/>
    • Report Visualization<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        s.node('Orchestrator', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🔄 Orchestrator</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#EBF8FF"><FONT COLOR="#2D3748">
    • Scenario Scheduler<BR/>
    • API-Driven Task Execution<BR/>
    • Cross-Platform Coordination<BR/>
  </FONT></TD></TR>
</TABLE>>''')

    # 2. Simulation Engines Cluster
    with g.subgraph(name='cluster_sim') as sim:
        sim.attr(label='Simulation Engines', style='filled,rounded', color='#EBF8FF', 
                 fontname='Arial', fontcolor='#2C5282', penwidth='2')
        sim.node('WinEngine', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#63B3ED">
  <TR><TD><FONT COLOR="#FFFFFF">🖥️ Windows Engines</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Splunk Attack Range<BR/>
    • Atomic Red Team<BR/>
    • PurpleSharp<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        sim.node('LinuxEngine', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#63B3ED">
  <TR><TD><FONT COLOR="#FFFFFF">🐧 Linux Engine</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Caldera Framework<BR/>
  </FONT></TD></TR>
</TABLE>>''')

    # 3. Target Environment Cluster
    with g.subgraph(name='cluster_targets') as targets:
        targets.attr(label='Target Environment (Isolated Lab)', style='filled,rounded', color='#FEEBC8',
                     fontname='Arial', fontcolor='#9C4221', penwidth='2')
        targets.node('AD', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#F6AD55">
  <TR><TD><FONT COLOR="#FFFFFF">🏢 Active Directory DC</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Windows Server VM<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        targets.node('WinClient', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#F6AD55">
  <TR><TD><FONT COLOR="#FFFFFF">💻 Windows Endpoints</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Client Workstations<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        targets.node('LinuxHost', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#F6AD55">
  <TR><TD><FONT COLOR="#FFFFFF">🌐 Linux Servers</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • Web Servers, DBs<BR/>
  </FONT></TD></TR>
</TABLE>>''')

    # 4. Telemetry & SIEM Layer
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('Forwarders', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#48BB78">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">📡 Forwarders</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#F0FFF4"><FONT COLOR="#2D3748">
    • Winlogbeat / Sysmon<BR/>
    • Splunk UF<BR/>
    • Auditd / Filebeat<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        s.node('SIEM', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#2F855A">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">📊 SIEM Backend</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#F0FFF4"><FONT COLOR="#2D3748">
    • Splunk / Elastic<BR/>
    • Indexing &amp; Search<BR/>
    • Detection Rules Engine<BR/>
  </FONT></TD></TR>
</TABLE>>''')

    # 5. Analysis & Reporting Layer
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('LLM', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🤖 LLM Analysis</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#FEFCBF"><FONT COLOR="#2D3748">
    • Ollama / GPT / Claude<BR/>
    • Detection Summarization<BR/>
    • Coverage Assessment<BR/>
  </FONT></TD></TR>
</TABLE>>''')
        s.node('Reports', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#4C51BF">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">📁 Report Storage</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BALIGN="LEFT" BGCOLOR="#EBF4FF"><FONT COLOR="#2D3748">
    • Markdown &amp; PDF Generation<BR/>
    • GitHub Version Control<BR/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Edges (Data/Control Flows) ---
    # Control Flow
    g.edge('Dashboard', 'Orchestrator', label='Trigger/Schedule', penwidth='2.0', color='#3182CE')
    g.edge('Orchestrator', 'WinEngine', label='Invoke Win Scenarios')
    g.edge('Orchestrator', 'LinuxEngine', label='Invoke Linux Scenarios')
    
    # Simulation Flow
    g.edge('WinEngine', 'AD', label='Execute TTPs', lhead='cluster_targets')
    g.edge('LinuxEngine', 'LinuxHost', label='Execute TTPs', lhead='cluster_targets')

    # Telemetry Flow
    g.edge('AD', 'Forwarders', label='Event Logs', color='#38A169')
    g.edge('WinClient', 'Forwarders', label='Sysmon/Endpoint Logs', color='#38A169')
    g.edge('LinuxHost', 'Forwarders', label='Syslog/Auditd', color='#38A169')
    g.edge('Forwarders', 'SIEM', label='Ingest & Index', penwidth='2.0', color='#2F855A')

    # Analysis & Reporting Flow
    g.edge('SIEM', 'LLM', label='Extract Detections', penwidth='2.0', color='#DD6B20')
    g.edge('LLM', 'Reports', label='Generate Summaries')
    g.edge('Reports', 'Dashboard', label='Retrieve Reports', style='dashed')
    g.edge('SIEM', 'Dashboard', label='Live Alerts & Dashboards', style='dashed')
    
    return g

def main():
    """Main function to generate the structural diagram."""
    print("🚀 Generating Enhanced Structural Diagram...")
    try:
        diag = create_structural_diagram()
        output_file = diag.render(cleanup=True)
        print(f"✅ Structural diagram saved successfully as: {output_file}")
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")
        print("💡 Make sure graphviz is installed and in your system's PATH.")
        print("   - Python library: pip install graphviz")
        print("   - System software: See https://graphviz.org/download/")

if __name__ == "__main__":
    main()