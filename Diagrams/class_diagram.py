# class_diagram.py
# Class Diagram for AI-ThreatSim showing Python classes and relationships
from graphviz import Digraph

def create_class_diagram(output_basename='class_diagram'):
    """Generates class diagram showing main Python classes in AI-ThreatSim."""
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes ---
    g.attr(rankdir='TB', splines='ortho', bgcolor='#FAFBFC', dpi='300')
    g.attr('node', shape='plain', fontname='Arial', fontsize='11')
    g.attr('edge', fontname='Arial', fontsize='10', color='#4A5568')

    # --- Class: RealLogParser ---
    g.node('RealLogParser', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="12"><B>RealLogParser</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FED7D7"><FONT COLOR="#2D3748">
    <B>Attributes:</B><BR ALIGN="LEFT"/>
    - attack_patterns: Dict<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Methods:</B><BR ALIGN="LEFT"/>
    + parse_linux_auth_log(log: str) → Dict<BR ALIGN="LEFT"/>
    + parse_windows_event_log(log: str) → Dict<BR ALIGN="LEFT"/>
    + parse_network_log(log: str) → Dict<BR ALIGN="LEFT"/>
    + convert_to_attack_description(indicators: Dict) → str<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Class: RealActionExecutor ---
    g.node('RealActionExecutor', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#38A169">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="12"><B>RealActionExecutor</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#C6F6D5"><FONT COLOR="#2D3748">
    <B>Attributes:</B><BR ALIGN="LEFT"/>
    - dry_run: bool<BR ALIGN="LEFT"/>
    - action_log: List[Dict]<BR ALIGN="LEFT"/>
    - system: str<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Methods:</B><BR ALIGN="LEFT"/>
    + block_ip_address(ip: str) → Dict<BR ALIGN="LEFT"/>
    + enable_fail2ban(service: str) → Dict<BR ALIGN="LEFT"/>
    + reset_user_password(user: str) → Dict<BR ALIGN="LEFT"/>
    + disable_user_account(user: str) → Dict<BR ALIGN="LEFT"/>
    + get_action_log() → List[Dict]<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Class: AttackerLoRAModel ---
    g.node('AttackerLoRAModel', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#0284C7">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="12"><B>AttackerLoRAModel</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#BAE6FD"><FONT COLOR="#2D3748">
    <B>Attributes:</B><BR ALIGN="LEFT"/>
    - model: PeftModel<BR ALIGN="LEFT"/>
    - tokenizer: AutoTokenizer<BR ALIGN="LEFT"/>
    - adapter_path: str = "attacker_lora/"<BR ALIGN="LEFT"/>
    - max_new_tokens: int = 512<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Methods:</B><BR ALIGN="LEFT"/>
    + load_model() → None<BR ALIGN="LEFT"/>
    + generate_attack_strategy(indicators: Dict) → str<BR ALIGN="LEFT"/>
    + inference(prompt: str) → str<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Class: DefenderLoRAModel ---
    g.node('DefenderLoRAModel', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#0284C7">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="12"><B>DefenderLoRAModel</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#BAE6FD"><FONT COLOR="#2D3748">
    <B>Attributes:</B><BR ALIGN="LEFT"/>
    - model: PeftModel<BR ALIGN="LEFT"/>
    - tokenizer: AutoTokenizer<BR ALIGN="LEFT"/>
    - adapter_path: str = "defender_lora/"<BR ALIGN="LEFT"/>
    - max_new_tokens: int = 512<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Methods:</B><BR ALIGN="LEFT"/>
    + load_model() → None<BR ALIGN="LEFT"/>
    + generate_defense_strategy(attack: str) → str<BR ALIGN="LEFT"/>
    + inference(prompt: str) → str<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Class: LoRATrainer ---
    g.node('LoRATrainer', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#805AD5">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="12"><B>LoRATrainer</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#E9D8FD"><FONT COLOR="#2D3748">
    <B>Attributes:</B><BR ALIGN="LEFT"/>
    - base_model: str = "Qwen2.5-0.5B"<BR ALIGN="LEFT"/>
    - dataset: Dataset<BR ALIGN="LEFT"/>
    - output_dir: str<BR ALIGN="LEFT"/>
    - lora_config: LoraConfig<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Methods:</B><BR ALIGN="LEFT"/>
    + load_dataset(file: str) → Dataset<BR ALIGN="LEFT"/>
    + train(epochs: int) → None<BR ALIGN="LEFT"/>
    + save_checkpoint() → None<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Class: SelfPlayManager ---
    g.node('SelfPlayManager', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E53E3E">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="12"><B>SelfPlayManager</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FED7D7"><FONT COLOR="#2D3748">
    <B>Attributes:</B><BR ALIGN="LEFT"/>
    - attacker_model: AttackerLoRAModel<BR ALIGN="LEFT"/>
    - defender_model: DefenderLoRAModel<BR ALIGN="LEFT"/>
    - log_dir: str = "logs/adversarial"<BR ALIGN="LEFT"/>
    - max_rounds: int<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Methods:</B><BR ALIGN="LEFT"/>
    + run_adversarial_training(episodes: int) → List<BR ALIGN="LEFT"/>
    + extract_winning_strategies() → Dict<BR ALIGN="LEFT"/>
    + generate_adaptation_data() → None<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Class: FastAPIApp (WebApp) ---
    g.node('FastAPIApp', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#DD6B20">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="12"><B>FastAPIApp</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FBD38D"><FONT COLOR="#2D3748">
    <B>Attributes:</B><BR ALIGN="LEFT"/>
    - app: FastAPI<BR ALIGN="LEFT"/>
    - parser: RealLogParser<BR ALIGN="LEFT"/>
    - executor: RealActionExecutor<BR ALIGN="LEFT"/>
    - attacker: AttackerLoRAModel<BR ALIGN="LEFT"/>
    - defender: DefenderLoRAModel<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Methods:</B><BR ALIGN="LEFT"/>
    + battle_endpoint(file: UploadFile, ...) → JSON<BR ALIGN="LEFT"/>
    + analyze_log(log: str) → Dict<BR ALIGN="LEFT"/>
    + start_server(port: int) → None<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Class: SystemLauncher (main.py) ---
    g.node('SystemLauncher', label='''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#4C51BF">
  <TR><TD><FONT COLOR="#FFFFFF" POINT-SIZE="12"><B>SystemLauncher</B></FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#EBF4FF"><FONT COLOR="#2D3748">
    <B>Attributes:</B><BR ALIGN="LEFT"/>
    - commands: List[str] (11 total)<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
  <TR><TD ALIGN="LEFT" BGCOLOR="#FFFFFF"><FONT COLOR="#2D3748">
    <B>Commands:</B><BR ALIGN="LEFT"/>
    + train_attacker() → None<BR ALIGN="LEFT"/>
    + train_defender() → None<BR ALIGN="LEFT"/>
    + adversarial() → None<BR ALIGN="LEFT"/>
    + webapp() → None<BR ALIGN="LEFT"/>
    + inference_attacker() → None<BR ALIGN="LEFT"/>
    + inference_defender() → None<BR ALIGN="LEFT"/>
    + monitor_training() → None<BR ALIGN="LEFT"/>
    + generate_metrics() → None<BR ALIGN="LEFT"/>
    + visualize_training() → None<BR ALIGN="LEFT"/>
    + continuous_training() → None<BR ALIGN="LEFT"/>
  </FONT></TD></TR>
</TABLE>>''')

    # --- Relationships ---
    # SystemLauncher launches everything
    g.edge('SystemLauncher', 'FastAPIApp', label='launches', arrowhead='open', penwidth='2', color='#4C51BF')
    g.edge('SystemLauncher', 'LoRATrainer', label='invokes', arrowhead='open', penwidth='2', color='#4C51BF')
    g.edge('SystemLauncher', 'SelfPlayManager', label='invokes', arrowhead='open', penwidth='2', color='#4C51BF')

    # FastAPIApp composition
    g.edge('FastAPIApp', 'RealLogParser', label='uses', arrowhead='diamond', penwidth='2', color='#DD6B20')
    g.edge('FastAPIApp', 'RealActionExecutor', label='uses', arrowhead='diamond', penwidth='2', color='#DD6B20')
    g.edge('FastAPIApp', 'AttackerLoRAModel', label='uses', arrowhead='diamond', penwidth='2', color='#DD6B20')
    g.edge('FastAPIApp', 'DefenderLoRAModel', label='uses', arrowhead='diamond', penwidth='2', color='#DD6B20')

    # LoRATrainer creates models
    g.edge('LoRATrainer', 'AttackerLoRAModel', label='trains', arrowhead='open', penwidth='2', color='#805AD5', style='dashed')
    g.edge('LoRATrainer', 'DefenderLoRAModel', label='trains', arrowhead='open', penwidth='2', color='#805AD5', style='dashed')

    # SelfPlayManager orchestrates battle
    g.edge('SelfPlayManager', 'AttackerLoRAModel', label='loads', arrowhead='open', penwidth='2', color='#E53E3E')
    g.edge('SelfPlayManager', 'DefenderLoRAModel', label='loads', arrowhead='open', penwidth='2', color='#E53E3E')
    g.edge('SelfPlayManager', 'RealLogParser', label='uses', arrowhead='open', style='dotted', color='#718096')
    g.edge('SelfPlayManager', 'RealActionExecutor', label='uses', arrowhead='open', style='dotted', color='#718096')

    # Data flow in battle
    g.edge('AttackerLoRAModel', 'DefenderLoRAModel', label='attack strategy →', arrowhead='open', color='#E53E3E', style='dashed')
    g.edge('DefenderLoRAModel', 'RealActionExecutor', label='defense actions →', arrowhead='open', color='#38A169', style='dashed')

    return g

def main():
    """Main function to generate the class diagram."""
    print("🚀 Generating AI-ThreatSim Class Diagram...")
    try:
        diag = create_class_diagram()
        output_file = diag.render(cleanup=True)
        print(f"✅ Class diagram saved successfully as: {output_file}")
        print("📊 Shows: 8 main classes with training/inference/battle relationships")
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")
        print("💡 Make sure graphviz is installed and in your system's PATH.")

if __name__ == "__main__":
    main()
