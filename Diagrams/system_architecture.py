# system_architecture.py
# System Architecture for AI-ThreatSim: Adversarial AI Training Platform
# Core Flow: Train Models → Upload Real Logs → AI Battle → Learn from Results → Retrain
from graphviz import Digraph

def create_system_architecture_diagram(output_basename='system_architecture'):
    """
    Generates system architecture for AI-ThreatSim adversarial training platform.
    Shows: Training Phase → Inference Phase → Adversarial Learning Loop
    """
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes ---
    g.attr(rankdir='TB', splines='ortho', bgcolor='#FAFBFC', compound='true', dpi='300')
    g.attr('node', shape='plain', fontname='Arial', fontsize='12')
    g.attr('edge', fontname='Arial', fontsize='11', color='#4A5568')

    # --- Phase 1: TRAINING PHASE ---
    with g.subgraph(name='cluster_training') as c:
        c.attr(label='📚 PHASE 1: Model Training', style='filled,rounded', color='#C6F6D5', 
               fontname='Arial Black', fontcolor='#2F855A', penwidth='3', fontsize='14')
        
        c.node('TrainingData', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">📊 Training Data</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Attacker Data (20 examples):</B><BR ALIGN="LEFT"/>
    • data/attacker_training.jsonl<BR ALIGN="LEFT"/>
    • MITRE ATT&amp;CK TTPs (T1595, T1046...)<BR ALIGN="LEFT"/>
    • Attack strategies &amp; tool usage<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Defender Data (20 examples):</B><BR ALIGN="LEFT"/>
    • data/defender_training.jsonl<BR ALIGN="LEFT"/>
    • MITRE D3FEND techniques<BR ALIGN="LEFT"/>
    • Defense strategies &amp; mitigations<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('LoRATraining', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🧠 LoRA Training</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Base Model:</B> Qwen2.5-0.5B-Instruct<BR ALIGN="LEFT"/>
    <B>Method:</B> LoRA adapter (rank 16)<BR ALIGN="LEFT"/>
    <B>Quantization:</B> 4-bit NF4<BR ALIGN="LEFT"/>
    <B>Hardware:</B> RTX 3050 (4GB VRAM)<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Commands:</B><BR ALIGN="LEFT"/>
    • python main.py train-attacker<BR ALIGN="LEFT"/>
    • python main.py train-defender<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('TrainedModels', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">✅ Trained Models</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>attacker_lora/</B> (9.2MB adapter)<BR ALIGN="LEFT"/>
    • Generates attack strategies<BR ALIGN="LEFT"/>
    • Maps to MITRE ATT&amp;CK<BR ALIGN="LEFT"/>
    • Creates exploitation plans<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>defender_lora/</B> (36.7MB adapter)<BR ALIGN="LEFT"/>
    • Generates defense responses<BR ALIGN="LEFT"/>
    • Maps to MITRE D3FEND<BR ALIGN="LEFT"/>
    • Creates mitigation plans<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Phase 2: INFERENCE PHASE (Real Log Analysis) ---
    with g.subgraph(name='cluster_inference') as c:
        c.attr(label='⚡ PHASE 2: Real Log Analysis & AI Battle', style='filled,rounded', color='#BEE3F8', 
               fontname='Arial Black', fontcolor='#2C5282', penwidth='3')
        
        c.node('RealLogs', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">📁 Real Security Logs</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Input Sources:</B><BR ALIGN="LEFT"/>
    • Linux /var/log/auth.log<BR ALIGN="LEFT"/>
    • Windows Event Log (CSV)<BR ALIGN="LEFT"/>
    • Network traffic logs<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Upload via:</B><BR ALIGN="LEFT"/>
    • Web UI (http://localhost:8000)<BR ALIGN="LEFT"/>
    • API endpoint /api/battle<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('LogParser', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#3182CE">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🔍 RealLogParser</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Detection:</B><BR ALIGN="LEFT"/>
    • SSH brute-force (T1110.001)<BR ALIGN="LEFT"/>
    • Privilege escalation (T1548.003)<BR ALIGN="LEFT"/>
    • Port scanning (T1046)<BR ALIGN="LEFT"/>
    • Account compromise (T1078)<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Output:</B> Attack indicators + TTPs<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('AttackerModel', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">⚔️ Attacker Model</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Input:</B> Attack indicators from logs<BR ALIGN="LEFT"/>
    <B>Process:</B> Inference with attacker_lora<BR ALIGN="LEFT"/>
    <B>Output:</B><BR ALIGN="LEFT"/>
    • Attack strategy analysis<BR ALIGN="LEFT"/>
    • Next exploitation steps<BR ALIGN="LEFT"/>
    • MITRE ATT&amp;CK TTP mappings<BR ALIGN="LEFT"/>
    • Realistic attack commands<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('DefenderModel', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🛡️ Defender Model</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Input:</B> Attack strategy + log indicators<BR ALIGN="LEFT"/>
    <B>Process:</B> Inference with defender_lora<BR ALIGN="LEFT"/>
    <B>Output:</B><BR ALIGN="LEFT"/>
    • Defense strategy<BR ALIGN="LEFT"/>
    • Mitigation recommendations<BR ALIGN="LEFT"/>
    • MITRE D3FEND technique mappings<BR ALIGN="LEFT"/>
    • Real defensive commands<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('ActionExecutor', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">⚡ RealActionExecutor</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Defensive Actions:</B><BR ALIGN="LEFT"/>
    • block_ip_address() - iptables/firewall<BR ALIGN="LEFT"/>
    • enable_fail2ban() - SSH protection<BR ALIGN="LEFT"/>
    • reset_user_password() - Force reset<BR ALIGN="LEFT"/>
    • disable_user_account() - Lock account<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Mode:</B> dry_run=True (safe demo)<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('BattleResult', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#805AD5">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🏆 Battle Result</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Winner Determination:</B><BR ALIGN="LEFT"/>
    • Attack score vs Defense score<BR ALIGN="LEFT"/>
    • Action effectiveness analysis<BR ALIGN="LEFT"/>
    • Real-time visualization in UI<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Logged to:</B> logs/selfplay.jsonl<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Phase 3: ADVERSARIAL LEARNING LOOP ---
    with g.subgraph(name='cluster_learning') as c:
        c.attr(label='🔄 PHASE 3: Adversarial Learning & Continuous Improvement', style='filled,rounded', color='#FED7D7', 
               fontname='Arial Black', fontcolor='#C53030', penwidth='3')
        
        c.node('AdversarialTraining', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🔄 Adversarial Training</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Self-Play Loop:</B><BR ALIGN="LEFT"/>
    1. Models battle in episodes<BR ALIGN="LEFT"/>
    2. Track win/loss outcomes<BR ALIGN="LEFT"/>
    3. Losing side analyzes winning strategy<BR ALIGN="LEFT"/>
    4. Generate adaptation data<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Command:</B> python main.py adversarial<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('AdaptationData', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">📈 Adaptation Data</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>New Training Examples:</B><BR ALIGN="LEFT"/>
    • attacker_adaptations.jsonl<BR ALIGN="LEFT"/>
    • defender_adaptations.jsonl<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Contains:</B><BR ALIGN="LEFT"/>
    • Winning strategies<BR ALIGN="LEFT"/>
    • Successful tactics<BR ALIGN="LEFT"/>
    • Effective countermeasures<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('Retraining', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🔁 Model Retraining</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Process:</B><BR ALIGN="LEFT"/>
    1. Append adaptation data to training set<BR ALIGN="LEFT"/>
    2. Retrain losing model<BR ALIGN="LEFT"/>
    3. Updated model learns new strategies<BR ALIGN="LEFT"/>
    4. Return to battle phase<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Result:</B> Continuous improvement loop<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Phase 4: MONITORING & ANALYSIS ---
    with g.subgraph(name='cluster_monitoring') as c:
        c.attr(label='📊 PHASE 4: Monitoring & Metrics', style='filled,rounded', color='#E9D8FD', 
               fontname='Arial Black', fontcolor='#6B46C1', penwidth='3')
        
        c.node('Metrics', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#805AD5">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">📈 Research Metrics</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Tracking:</B><BR ALIGN="LEFT"/>
    • Win rates (Attacker vs Defender)<BR ALIGN="LEFT"/>
    • Training loss convergence<BR ALIGN="LEFT"/>
    • Tool call success rates<BR ALIGN="LEFT"/>
    • MITRE TTP coverage<BR ALIGN="LEFT"/>
    <BR ALIGN="LEFT"/>
    <B>Commands:</B><BR ALIGN="LEFT"/>
    • python main.py monitor-training<BR ALIGN="LEFT"/>
    • python main.py generate-metrics<BR ALIGN="LEFT"/>
    • python main.py visualize-training<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- User Interfaces ---
    with g.subgraph(name='cluster_interfaces') as c:
        c.attr(label='🖥️ User Interfaces', style='dashed,rounded', color='#A0AEC0', 
               fontname='Arial', fontcolor='#4A5568')
        
        c.node('WebUI', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#9F7AEA">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">🌐 Web Application</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    • http://localhost:8000<BR ALIGN="LEFT"/>
    • Drag-and-drop log upload<BR ALIGN="LEFT"/>
    • Real-time battle visualization<BR ALIGN="LEFT"/>
    • Winner display &amp; statistics<BR ALIGN="LEFT"/>
    • Action execution log<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')
        
        c.node('CLI', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#9F7AEA">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="14">💻 Command Line</FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>main.py - 11 Commands:</B><BR ALIGN="LEFT"/>
    • train-attacker / train-defender<BR ALIGN="LEFT"/>
    • inference-attacker / inference-defender<BR ALIGN="LEFT"/>
    • adversarial (self-play loop)<BR ALIGN="LEFT"/>
    • webapp (start web server)<BR ALIGN="LEFT"/>
    • continuous-training / monitor-training<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- EDGES: Training Phase Flow ---
    g.edge('TrainingData', 'LoRATraining', label='MITRE TTPs', penwidth='3', color='#38A169')
    g.edge('LoRATraining', 'TrainedModels', label='Fine-tuned adapters', penwidth='3', color='#38A169')

    # --- EDGES: Inference Phase Flow ---
    g.edge('RealLogs', 'LogParser', label='Raw logs', penwidth='3', color='#3182CE')
    g.edge('LogParser', 'AttackerModel', label='Attack indicators', penwidth='3', color='#E53E3E')
    g.edge('AttackerModel', 'DefenderModel', label='Attack strategy', penwidth='3', color='#E53E3E')
    g.edge('DefenderModel', 'ActionExecutor', label='Defense plan', penwidth='3', color='#38A169')
    g.edge('ActionExecutor', 'BattleResult', label='Execution results', penwidth='3', color='#DD6B20')

    # --- EDGES: Adversarial Learning Flow ---
    g.edge('BattleResult', 'AdversarialTraining', label='Win/loss data', penwidth='3', color='#E53E3E', style='dashed')
    g.edge('AdversarialTraining', 'AdaptationData', label='Extract winning strategies', penwidth='3', color='#E53E3E')
    g.edge('AdaptationData', 'Retraining', label='New examples', penwidth='3', color='#E53E3E')
    g.edge('Retraining', 'TrainingData', label='Augment dataset', penwidth='3', color='#38A169', style='dashed')

    # --- EDGES: Model Usage in Inference ---
    g.edge('TrainedModels', 'AttackerModel', label='Load attacker_lora', style='dotted', color='#718096')
    g.edge('TrainedModels', 'DefenderModel', label='Load defender_lora', style='dotted', color='#718096')

    # --- EDGES: Monitoring ---
    g.edge('BattleResult', 'Metrics', label='Log outcomes', style='dotted', color='#805AD5')
    g.edge('AdversarialTraining', 'Metrics', label='Track progress', style='dotted', color='#805AD5')

    # --- EDGES: User Interfaces ---
    g.edge('CLI', 'LoRATraining', label='train-* cmds', style='dotted')
    g.edge('CLI', 'AdversarialTraining', label='adversarial cmd', style='dotted')
    g.edge('CLI', 'Metrics', label='monitor cmds', style='dotted')
    g.edge('WebUI', 'RealLogs', label='Upload logs', penwidth='2', color='#9F7AEA')
    g.edge('BattleResult', 'WebUI', label='Display results', penwidth='2', color='#9F7AEA')
    
    return g

def main():
    """Main function to generate the system architecture diagram."""
    print("🚀 Generating AI-ThreatSim System Architecture Diagram...")
    try:
        diag = create_system_architecture_diagram()
        output_file = diag.render(cleanup=True)
        print(f"✅ System architecture diagram saved successfully as: {output_file}")
        print("📊 Shows: Training → Inference → Adversarial Learning → Continuous Improvement")
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")
        print("💡 Make sure graphviz is installed and in your system's PATH.")

if __name__ == "__main__":
    main()
