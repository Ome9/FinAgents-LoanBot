# use_case.py
# Use Case Diagram for AI-ThreatSim showing actors and their interactions
from graphviz import Digraph

def create_use_case_diagram(output_basename='use_case'):
    """Generates use case diagram for AI-ThreatSim adversarial training platform."""
    g = Digraph('G', filename=output_basename, format='png')
    
    # --- Global Graph Attributes ---
    g.attr(rankdir='LR', splines='true', bgcolor='#FAFBFC', dpi='300')
    g.attr('node', fontname='Arial', fontsize='13')
    g.attr('edge', fontname='Arial', fontsize='11', color='#4A5568')

    # --- Actors ---
    g.node('SOCAnalyst', label='👨‍💼\nSOC Analyst', shape='plaintext', fontsize='14', fontcolor='#2D3748')
    g.node('SecurityResearcher', label='🔬\nSecurity\nResearcher', shape='plaintext', fontsize='14', fontcolor='#2D3748')
    g.node('PenTester', label='🔴\nPenetration\nTester', shape='plaintext', fontsize='14', fontcolor='#2D3748')

    # --- System Boundary ---
    with g.subgraph(name='cluster_system') as c:
        c.attr(label='AI-ThreatSim Platform', style='rounded,dashed', color='#3182CE', 
               fontname='Arial Black', fontsize='14', fontcolor='#2D3748', penwidth='2')
        
        # Use Case 1: Train Models
        c.node('TrainModels', label='Train Attack &\nDefense Models', shape='ellipse', style='filled', 
               fillcolor='#C6F6D5', color='#38A169', penwidth='2')
        
        # Use Case 2: Upload Logs
        c.node('UploadLogs', label='Upload Real\nSecurity Logs', shape='ellipse', style='filled', 
               fillcolor='#BEE3F8', color='#3182CE', penwidth='2')
        
        # Use Case 3: Analyze Threats
        c.node('AnalyzeThreats', label='Analyze Threat\nIndicators', shape='ellipse', style='filled', 
               fillcolor='#FED7D7', color='#E53E3E', penwidth='2')
        
        # Use Case 4: Run AI Battle
        c.node('RunBattle', label='Run AI Battle\n(Attack vs Defense)', shape='ellipse', style='filled', 
               fillcolor='#E9D8FD', color='#805AD5', penwidth='2')
        
        # Use Case 5: Execute Defensive Actions
        c.node('ExecuteDefense', label='Execute Defensive\nActions', shape='ellipse', style='filled', 
               fillcolor='#C6F6D5', color='#38A169', penwidth='2')
        
        # Use Case 6: View Battle Results
        c.node('ViewResults', label='View Battle Results\n& Statistics', shape='ellipse', style='filled', 
               fillcolor='#FAF089', color='#D69E2E', penwidth='2')
        
        # Use Case 7: Run Adversarial Training
        c.node('AdversarialTraining', label='Run Adversarial\nTraining Loop', shape='ellipse', style='filled', 
               fillcolor='#FED7D7', color='#E53E3E', penwidth='2')
        
        # Use Case 8: Monitor Training
        c.node('MonitorTraining', label='Monitor Training\nProgress', shape='ellipse', style='filled', 
               fillcolor='#E9D8FD', color='#805AD5', penwidth='2')
        
        # Use Case 9: Generate Metrics
        c.node('GenerateMetrics', label='Generate Research\nMetrics', shape='ellipse', style='filled', 
               fillcolor='#FAF089', color='#D69E2E', penwidth='2')
        
        # Use Case 10: Visualize Training
        c.node('VisualizeTraining', label='Visualize Training\nResults', shape='ellipse', style='filled', 
               fillcolor='#FAF089', color='#D69E2E', penwidth='2')

    # --- Actor to Use Case Connections ---
    # SOC Analyst (Primary User - Log Analysis)
    g.edge('SOCAnalyst', 'UploadLogs', color='#3182CE', penwidth='2')
    g.edge('SOCAnalyst', 'AnalyzeThreats', color='#3182CE', penwidth='2')
    g.edge('SOCAnalyst', 'RunBattle', color='#805AD5', penwidth='3')
    g.edge('SOCAnalyst', 'ViewResults', color='#D69E2E', penwidth='2')
    g.edge('SOCAnalyst', 'ExecuteDefense', color='#38A169', penwidth='2')
    
    # Security Researcher (Model Training & Analysis)
    g.edge('SecurityResearcher', 'TrainModels', color='#38A169', penwidth='3')
    g.edge('SecurityResearcher', 'AdversarialTraining', color='#E53E3E', penwidth='3')
    g.edge('SecurityResearcher', 'MonitorTraining', color='#805AD5', penwidth='2')
    g.edge('SecurityResearcher', 'GenerateMetrics', color='#D69E2E', penwidth='2')
    g.edge('SecurityResearcher', 'VisualizeTraining', color='#D69E2E', penwidth='2')
    g.edge('SecurityResearcher', 'RunBattle', color='#805AD5', penwidth='2', style='dashed')
    
    # Penetration Tester (Attack Testing)
    g.edge('PenTester', 'UploadLogs', color='#E53E3E', penwidth='2', style='dashed')
    g.edge('PenTester', 'AnalyzeThreats', color='#E53E3E', penwidth='2')
    g.edge('PenTester', 'RunBattle', color='#805AD5', penwidth='2')
    g.edge('PenTester', 'ViewResults', color='#D69E2E', penwidth='2')

    # --- Use Case Relationships ---
    # Include relationships
    g.edge('RunBattle', 'UploadLogs', label='«include»', style='dashed', 
           color='#718096', arrowhead='open', penwidth='1.5')
    g.edge('RunBattle', 'AnalyzeThreats', label='«include»', style='dashed', 
           color='#718096', arrowhead='open', penwidth='1.5')
    g.edge('RunBattle', 'ExecuteDefense', label='«include»', style='dashed', 
           color='#718096', arrowhead='open', penwidth='1.5')
    g.edge('RunBattle', 'ViewResults', label='«include»', style='dashed', 
           color='#718096', arrowhead='open', penwidth='1.5')
    
    # Extend relationships
    g.edge('AdversarialTraining', 'RunBattle', label='«extend»', style='dotted', 
           color='#A0AEC0', arrowhead='open', penwidth='1.5')
    g.edge('AdversarialTraining', 'TrainModels', label='«extend»', style='dotted', 
           color='#A0AEC0', arrowhead='open', penwidth='1.5')
    g.edge('VisualizeTraining', 'MonitorTraining', label='«extend»', style='dotted', 
           color='#A0AEC0', arrowhead='open', penwidth='1.5')
    g.edge('GenerateMetrics', 'MonitorTraining', label='«extend»', style='dotted', 
           color='#A0AEC0', arrowhead='open', penwidth='1.5')

    return g

def main():
    """Main function to generate the use case diagram."""
    print("🚀 Generating AI-ThreatSim Use Case Diagram...")
    try:
        diag = create_use_case_diagram()
        output_file = diag.render(cleanup=True)
        print(f"✅ Use case diagram saved successfully as: {output_file}")
        print("📊 Shows: 3 Actors (SOC/Researcher/PenTester) × 10 Use Cases")
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")
        print("💡 Make sure graphviz is installed and in your system's PATH.")

if __name__ == "__main__":
    main()
