# enhanced_wbs_diagram.py
# Enhanced Work Breakdown Structure (WBS) diagram using graphviz
from graphviz import Digraph
import os

def create_enhanced_wbs(output_basename='enhanced_wbs_diagram'):
    """Create an enhanced WBS diagram with vertical expansion and detailed structure"""
    
    dot = Digraph(comment='Enhanced WBS - AI Detection Engineering Lab', format='png')
    
    # --- FIX: Attributes optimized for a tall, vertical layout ---
    dot.attr(rankdir='TB', splines='ortho', bgcolor='#FAFBFC', size='11,17!') # Portrait page size
    dot.attr(dpi='300', ranksep='1.0', nodesep='0.6')
    
    # Node styling
    dot.attr('node', 
             shape='box', 
             style='filled,rounded,shadow', 
             fontname='Arial', 
             fontsize='10',
             margin='0.3,0.15')
    
    # Edge styling
    dot.attr('edge', 
             fontname='Arial', 
             fontsize='8', 
             penwidth='2',
             arrowsize='0.8')

    # Root project node
    dot.node('Project', 
             '🚀 AI-Driven Detection Engineering Lab\\n' +
             'Cybersecurity Simulation Platform\\n' +
             'Multi-Platform Attack Orchestration', 
             fillcolor='#1A202C', 
             fontcolor='white', 
             fontsize='14',
             width='4', 
             height='1.2')

    # This is the original, unmodified project structure
    sections = [
        {
            'id': 'Planning', 'title': '📋 Project Planning & Setup', 'color': '#E53E3E', 'light_color': '#FED7D7',
            'tasks': [
                ('Req', '📝 Requirements Analysis\\n& Documentation'), ('TaskDiv', '🎯 Task Division &\\nProject Scheduling'),
                ('EnvSetup', '💻 Environment Setup\\n& VM Configuration'), ('ArchDesign', '🏗️ Dashboard Architecture\\nDesign & Planning'),
                ('RiskAssess', '⚠️ Risk Assessment\\n& Mitigation Planning')
            ]
        },
        {
            'id': 'Windows', 'title': '🖥️ Windows Simulation Module', 'color': '#3182CE', 'light_color': '#BEE3F8',
            'tasks': [
                ('AttackRange', '🔴 Splunk Attack Range\\nIntegration & Config'), ('AtomicRed', '⚡ Atomic Red Team\\nScenario Development'),
                ('PurpleSharp', '🟣 PurpleSharp Technique\\nImplementation'), ('WinOrch', '🔄 Cross-Platform\\nOrchestration (Windows)'),
                ('ADSim', '🏢 Active Directory\\nSimulation Environment')
            ]
        },
        {
            'id': 'Linux', 'title': '🐧 Linux Simulation Module', 'color': '#38A169', 'light_color': '#C6F6D5',
            'tasks': [
                ('LinuxPrep', '🔧 Linux Environment\\nPreparation & Hardening'), ('CalderaSetup', '🎯 Caldera Agent Setup\\n& Configuration'),
                ('PostExploit', '🔓 Post-Exploitation\\nScenario Development'), ('PrivEsc', '📈 Privilege Escalation\\nTesting Framework'),
                ('LateralMov', '🌐 Lateral Movement\\nValidation System')
            ]
        },
        {
            'id': 'Detection', 'title': '🔍 Detection & Telemetry', 'color': '#319795', 'light_color': '#B2F5EA',
            'tasks': [
                ('SplunkConfig', '📊 Splunk SIEM\\nConfiguration & Setup'), ('ForwarderDep', '📡 Universal Forwarder\\nDeployment & Management'),
                ('MITREMap', '🎯 MITRE ATT&CK\\nFramework Mapping'), ('DetectionRules', '✅ Detection Rule Creation\\n& Validation Testing'),
                ('AlertTuning', '🔧 Alert Tuning &\\nFalse Positive Reduction')
            ]
        },
        {
            'id': 'AI', 'title': '🤖 AI & Reporting Engine', 'color': '#D69E2E', 'light_color': '#FAECC6',
            'tasks': [
                ('LLMInteg', '🧠 LLM API Integration\\n(GPT/Ollama/Claude)'), ('ReportAuto', '📄 Automated Report\\nGeneration Pipeline'),
                ('CoverageAssess', '📈 Detection Coverage\\nAssessment (Full/Partial/None)'), ('ReportFormats', '📋 Multi-Format Report\\nGeneration (MD/PDF)'),
                ('VersionControl', '🔄 GitHub Integration\\n& Version Control')
            ]
        },
        {
            'id': 'Dashboard', 'title': '🎨 Web Dashboard Development', 'color': '#ED8936', 'light_color': '#FBD38D',
            'tasks': [
                ('FrontendUI', '🖼️ Frontend Dashboard\\nUI Development (React/Gradio)'), ('BackendAPI', '🔌 Backend API\\nIntegration Layer'),
                ('RealTimeViz', '📊 Real-time Visualization\\n& Monitoring Dashboards'), ('MITREHeatmap', '🗺️ MITRE Heatmap\\nVisualization System'),
                ('UserAuth', '🔐 User Authentication\\n& Role-Based Access')
            ]
        },
        {
            'id': 'Testing', 'title': '🧪 Testing & Quality Assurance', 'color': '#805AD5', 'light_color': '#E9D8FD',
            'tasks': [
                ('UnitTest', '🔧 Unit & Integration\\nTesting Framework'), ('StressTest', '⚡ Parallel Simulation\\nStress Testing'),
                ('PerfOptim', '🚀 SIEM Performance\\nOptimization & Tuning'), ('SecurityTest', '🛡️ Security Testing\\n& Penetration Testing'),
                ('LoadTest', '📊 Load Testing &\\nScalability Validation')
            ]
        },
        {
            'id': 'Documentation', 'title': '📚 Documentation & Delivery', 'color': '#9F7AEA', 'light_color': '#E9D8FD',
            'tasks': [
                ('UserGuide', '📖 User Guide &\\nSetup Documentation'), ('TechnicalDoc', '📄 Technical Documentation\\n& API Reference'),
                ('ResearchPaper', '🎓 Research Paper\\n& Technical Report'), ('Presentation', '🎯 Project Presentation\\n& Demo Preparation'),
                ('VideoDemo', '🎥 Video Demonstration\\n& Tutorial Creation')
            ]
        },
        {
            'id': 'Future', 'title': '🔮 Future Enhancements', 'color': '#718096', 'light_color': '#E2E8F0',
            'tasks': [
                ('APTModules', '🎭 Advanced APT\\nSimulation Modules'), ('MLAnalytics', '🤖 Enhanced Machine Learning\\nAnalytics & Predictions'),
                ('CICDInteg', '🔄 CI/CD Pipeline\\nIntegration & Automation'), ('CloudDeploy', '☁️ Cloud Deployment\\n& Scalability Features'),
                ('ThreatIntel', '🔍 Threat Intelligence\\nIntegration & Feeds')
            ]
        }
    ]

    # Create section nodes
    for section in sections:
        dot.node(section['id'], section['title'],
                 fillcolor=section['color'], fontcolor='white', fontsize='12',
                 width='3', height='0.8')
        dot.edge('Project', section['id'], color='#4A5568', penwidth='3')

    # --- FIX: Create an invisible chain to force vertical section layout ---
    for i in range(len(sections) - 1):
        dot.edge(sections[i]['id'], sections[i+1]['id'], style='invis', weight='100')

    # Add task nodes for each section
    for section in sections:
        for task_id, task_title in section['tasks']:
            full_task_id = f"{section['id']}_{task_id}"
            dot.node(full_task_id, task_title,
                     fillcolor=section['light_color'], fontcolor='#2D3748',
                     fontsize='9', width='2.2', height='0.8')
            dot.edge(section['id'], full_task_id,
                     color=section['color'], penwidth='2', arrowhead='dot')

    # Add cross-functional dependencies
    dependencies = [
        ('Windows_WinOrch', 'Linux_PostExploit', 'Cross-Platform\\nOrchestration'),
        ('Detection_MITREMap', 'AI_CoverageAssess', 'Data Flow\\nfor Analysis'),
        ('Dashboard_BackendAPI', 'Windows_AttackRange', 'Simulation\\nControl'),
        ('Dashboard_BackendAPI', 'Linux_CalderaSetup', 'Simulation\\nControl'),
        ('AI_ReportAuto', 'Detection_DetectionRules', 'Analysis\\nInput'),
        ('Testing_StressTest', 'Dashboard_RealTimeViz', 'Performance\\nValidation'),
        ('Documentation_TechnicalDoc', 'AI_LLMInteg', 'Documentation\\nGeneration')
    ]

    for source, target, label in dependencies:
        dot.edge(source, target, style='dashed', color='#E53E3E',
                 penwidth='1.5', arrowhead='open', label=label, fontcolor='#E53E3E')

    dot.attr(label='\\nWork Breakdown Structure for the AI-Driven Detection Engineering Lab',
             fontsize='14', fontname='Arial', labelloc='b', fontcolor='#2D3748')

    return dot

def main():
    """Main function to generate the WBS diagram"""
    print("🚀 Generating Enhanced Vertical WBS Diagram...")
    try:
        wbs_diag = create_enhanced_wbs()
        output_file = wbs_diag.render(filename='wbs_vertical_final', cleanup=True)
        print(f"✅ WBS diagram saved successfully as: {output_file}")
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")
        print("💡 Make sure graphviz is installed and in your system's PATH.")
        print("   - Python library: pip install graphviz")
        print("   - System software: See https://graphviz.org/download/")

if __name__ == "__main__":
    main()