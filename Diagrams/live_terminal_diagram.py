"""
Live Terminal System Architecture - Visual Diagram
Generates a comprehensive diagram showing the complete data flow
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.programming.framework import React, Fastapi
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.onprem.client import Users
import os

# Change output directory
output_dir = "Diagrams"
os.makedirs(output_dir, exist_ok=True)

with Diagram("Live Terminal System - Complete Architecture", 
             filename=f"{output_dir}/live_terminal_architecture",
             show=False,
             direction="TB",
             graph_attr={"fontsize": "20", "bgcolor": "white"}):
    
    user = Users("User")
    
    with Cluster("Frontend (Astro + React)\nhttp://localhost:4321"):
        with Cluster("Threat Analysis Page"):
            upload = Custom("Upload Log", "./Diagrams/icons/upload.png") if os.path.exists("./Diagrams/icons/upload.png") else React("Upload")
            sandbox_btn = Custom("🐳 Sandbox Button", "./Diagrams/icons/docker.png") if os.path.exists("./Diagrams/icons/docker.png") else React("Sandbox Button")
            
            with Cluster("Live Terminal Display"):
                terminal_header = React("Terminal Header\n[Status] [Clear]")
                terminal_window = React("Terminal Window\n(Auto-scroll)")
                terminal_info = React("Info Bar\nContainer | Commands")
        
        with Cluster("JavaScript Polling (2s)"):
            poll_status = React("Poll Status API")
            update_terminal = React("Update Terminal")
            update_info = React("Update Info Bar")
    
    with Cluster("Backend (FastAPI)\nhttp://localhost:8000"):
        with Cluster("API Endpoints"):
            battle_endpoint = Fastapi("/api/battle/sandbox")
            status_endpoint = Fastapi("/api/battle/status/{id}")
        
        with Cluster("Battle Loop"):
            phase1 = Python("1. Attacker Planning\n+ Sandbox State")
            phase2 = Python("2. Execute Attacks\n(as vulnerable)")
            phase3 = Python("3. Collect REAL Logs\n+ Terminal Output")
            phase4 = Python("4. Defender Analysis\n(LOGS only)")
            phase5 = Python("5. Execute Defenses\n(as root)")
            phase6 = Python("6. Update Status\n+ Terminal")
        
        battle_status = Python("battle_status{}\n[battle_id]")
    
    with Cluster("MCP Server (SandboxMCP)"):
        with Cluster("Data Structures"):
            terminal_logs = Python("live_terminal_logs[]\n[user@sandbox]$ cmd")
            sandbox_state = Python("sandbox_state{}\ncommands, defenses")
        
        with Cluster("Methods"):
            execute_cmd = Python("execute_command()\n→ Auto-log")
            get_state = Python("get_sandbox_state()\n→ 8 context points")
            get_terminal = Python("get_live_terminal_output()\n→ Full history")
            get_logs = Python("get_system_logs()\n→ auth.log, syslog")
    
    with Cluster("Docker Sandbox\nUbuntu 22.04"):
        container = Docker("ai-threatsim-sandbox")
        
        with Cluster("Users"):
            vulnerable = Custom("vulnerable user", "./Diagrams/icons/user.png") if os.path.exists("./Diagrams/icons/user.png") else Docker("vulnerable")
            root = Custom("root user", "./Diagrams/icons/admin.png") if os.path.exists("./Diagrams/icons/admin.png") else Docker("root")
        
        with Cluster("System Logs"):
            auth_log = Docker("/var/log/auth.log")
            syslog = Docker("/var/log/syslog")
            apache_log = Docker("/var/log/apache2/")
    
    # User interactions
    user >> Edge(label="Upload log file") >> upload
    upload >> Edge(label="Enable") >> sandbox_btn
    sandbox_btn >> Edge(label="POST\n{log_content}") >> battle_endpoint
    
    # Battle initialization
    battle_endpoint >> Edge(label="Start battle\nReturn battle_id") >> battle_status
    battle_status >> Edge(label="200 OK\n{battle_id, container_id}") >> sandbox_btn
    
    # Polling flow
    sandbox_btn >> Edge(label="Start polling") >> poll_status
    poll_status >> Edge(label="Every 2s\nGET /status/{id}") >> status_endpoint
    status_endpoint >> Edge(label="Read") >> battle_status
    battle_status >> Edge(label="Return\nlive_terminal[]") >> poll_status
    poll_status >> Edge(label="Update UI") >> update_terminal
    update_terminal >> terminal_window
    poll_status >> Edge(label="Update stats") >> update_info
    update_info >> terminal_info
    
    # Battle loop flow
    battle_endpoint >> Edge(label="Start async\nbackground task") >> phase1
    
    # Phase 1: Attacker Planning
    phase1 >> Edge(label="get_sandbox_state()") >> get_state
    get_state >> Edge(label="Return context") >> phase1
    phase1 >> Edge(label="AI generates\nattack plan") >> phase2
    
    # Phase 2: Execute Attacks
    phase2 >> Edge(label="execute_command()\nuser='vulnerable'") >> execute_cmd
    execute_cmd >> Edge(label="Docker exec") >> vulnerable
    vulnerable >> Edge(label="Run command") >> container
    container >> Edge(label="exit_code, stdout") >> execute_cmd
    execute_cmd >> Edge(label="Auto-log to\nterminal_logs[]") >> terminal_logs
    execute_cmd >> Edge(label="Track in\nsandbox_state{}") >> sandbox_state
    
    # Phase 3: Collect Logs
    phase3 >> Edge(label="get_system_logs()") >> get_logs
    get_logs >> Edge(label="Read") >> auth_log
    get_logs >> Edge(label="Read") >> syslog
    get_logs >> Edge(label="Read") >> apache_log
    get_logs >> Edge(label="Return REAL logs") >> phase3
    phase3 >> Edge(label="get_live_terminal_output()") >> get_terminal
    get_terminal >> Edge(label="Return history") >> terminal_logs
    terminal_logs >> Edge(label="Terminal output") >> phase3
    phase3 >> Edge(label="Store in\nbattle_status") >> battle_status
    
    # Phase 4: Defender Analysis
    phase3 >> Edge(label="Pass LOGS\n(NOT commands!)") >> phase4
    phase4 >> Edge(label="AI analyzes\nlogs + state") >> phase5
    
    # Phase 5: Execute Defenses
    phase5 >> Edge(label="execute_command()\nuser='root'") >> execute_cmd
    execute_cmd >> Edge(label="Docker exec") >> root
    root >> Edge(label="Run defense\n(iptables, fail2ban)") >> container
    container >> Edge(label="exit_code") >> execute_cmd
    execute_cmd >> Edge(label="Log defense") >> terminal_logs
    execute_cmd >> Edge(label="Track in\ndefenses_applied[]") >> sandbox_state
    
    # Phase 6: Update Status
    phase5 >> Edge(label="Update") >> phase6
    phase6 >> Edge(label="get_live_terminal_output()") >> get_terminal
    get_terminal >> Edge(label="Latest terminal") >> phase6
    phase6 >> Edge(label="Store round data") >> battle_status

print("✅ Diagram generated: Diagrams/live_terminal_architecture.png")
print("📊 Shows complete data flow from user click to terminal update")
