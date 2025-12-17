import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Define hierarchical project structure with dependencies
project_structure = {
    "PROJECT PLANNING & SETUP": {
        "color": "#E53E3E",
        "tasks": [
            {"name": "Requirements Analysis & Documentation", "start": "2025-07-30", "duration": 10, "resource": "Member A", "dependencies": []},
            {"name": "Task Division & Project Scheduling", "start": "2025-08-13", "duration": 5, "resource": "Member A", "dependencies": ["Requirements Analysis & Documentation"]},
            {"name": "Environment Setup and VM Configuration", "start": "2025-08-20", "duration": 10, "resource": "Member A", "dependencies": ["Task Division & Project Scheduling"]},
            {"name": "Dashboard Architecture Design", "start": "2025-09-03", "duration": 7, "resource": "Member A", "dependencies": ["Environment Setup and VM Configuration"]},
        ]
    },
    "WINDOWS SIMULATION MODULE": {
        "color": "#3182CE",
        "tasks": [
            {"name": "Windows Attack Range Integration", "start": "2025-08-10", "duration": 15, "resource": "Member A", "dependencies": []},
            {"name": "Atomic Red Team Scenario Setup", "start": "2025-08-29", "duration": 8, "resource": "Member A", "dependencies": ["Windows Attack Range Integration"]},
            {"name": "PurpleSharp Technique Integration", "start": "2025-09-10", "duration": 7, "resource": "Member A", "dependencies": ["Atomic Red Team Scenario Setup"]},
            {"name": "Cross-Platform Orchestration Development", "start": "2025-09-19", "duration": 10, "resource": "Member A", "dependencies": ["PurpleSharp Technique Integration"]},
        ]
    },
    "LINUX SIMULATION MODULE": {
        "color": "#38A169",
        "tasks": [
            {"name": "Linux Environment Preparation", "start": "2025-08-05", "duration": 8, "resource": "Member B", "dependencies": []},
            {"name": "Caldera Agent Setup and Configuration", "start": "2025-08-12", "duration": 15, "resource": "Member B", "dependencies": ["Linux Environment Preparation"]},
            {"name": "Post-Exploitation Scenario Development", "start": "2025-09-02", "duration": 10, "resource": "Member B", "dependencies": ["Caldera Agent Setup and Configuration"]},
            {"name": "Privilege Escalation Testing Framework", "start": "2025-09-16", "duration": 8, "resource": "Member B", "dependencies": ["Post-Exploitation Scenario Development"]},
            {"name": "Lateral Movement Validation System", "start": "2025-09-26", "duration": 7, "resource": "Member B", "dependencies": ["Privilege Escalation Testing Framework"]},
        ]
    },
    "DETECTION & TELEMETRY": {
        "color": "#319795",
        "tasks": [
            {"name": "Splunk SIEM Configuration and Setup", "start": "2025-08-25", "duration": 10, "resource": "Member B", "dependencies": []},
            {"name": "Forwarder Deployment Across Systems", "start": "2025-09-08", "duration": 8, "resource": "Member B", "dependencies": ["Splunk SIEM Configuration and Setup"]},
            {"name": "MITRE ATT&CK Framework Mapping", "start": "2025-09-18", "duration": 7, "resource": "Member B", "dependencies": ["Forwarder Deployment Across Systems"]},
            {"name": "Detection Rule Creation and Validation", "start": "2025-09-27", "duration": 12, "resource": "Member B", "dependencies": ["MITRE ATT&CK Framework Mapping"]},
        ]
    },
    "AI & REPORTING ENGINE": {
        "color": "#D69E2E",
        "tasks": [
            {"name": "LLM API Integration and Setup", "start": "2025-09-10", "duration": 15, "resource": "Member C", "dependencies": []},
            {"name": "Automated Report Generation Pipeline", "start": "2025-09-29", "duration": 10, "resource": "Member C", "dependencies": ["LLM API Integration and Setup"]},
            {"name": "Detection Coverage Assessment Automation", "start": "2025-10-13", "duration": 10, "resource": "Member C", "dependencies": ["Automated Report Generation Pipeline"]},
            {"name": "Markdown and PDF Report Generation", "start": "2025-10-27", "duration": 7, "resource": "Member C", "dependencies": ["Detection Coverage Assessment Automation"]},
            {"name": "GitHub Version Control Integration", "start": "2025-11-05", "duration": 5, "resource": "Member C", "dependencies": ["Markdown and PDF Report Generation"]},
        ]
    },
    "WEB DASHBOARD DEVELOPMENT": {
        "color": "#ED8936",
        "tasks": [
            {"name": "Frontend Dashboard UI Development", "start": "2025-09-15", "duration": 15, "resource": "Member C", "dependencies": []},
            {"name": "Backend API Integration Layer", "start": "2025-10-06", "duration": 10, "resource": "Member C", "dependencies": ["Frontend Dashboard UI Development"]},
            {"name": "Real-time Visualization Implementation", "start": "2025-10-20", "duration": 7, "resource": "Member C", "dependencies": ["Backend API Integration Layer"]},
            {"name": "MITRE Heatmap Visualization System", "start": "2025-10-29", "duration": 5, "resource": "Member C", "dependencies": ["Real-time Visualization Implementation"]},
        ]
    },
    "TESTING & QUALITY ASSURANCE": {
        "color": "#805AD5",
        "tasks": [
            {"name": "Unit & Integration Testing", "start": "2025-09-25", "duration": 12, "resource": "All Team", "dependencies": []},
            {"name": "Parallel Simulation Stress Testing", "start": "2025-10-10", "duration": 10, "resource": "All Team", "dependencies": ["Unit & Integration Testing"]},
            {"name": "SIEM Performance Optimization", "start": "2025-10-24", "duration": 8, "resource": "All Team", "dependencies": ["Parallel Simulation Stress Testing"]},
            {"name": "Final System Testing and Validation", "start": "2025-11-09", "duration": 8, "resource": "All Team", "dependencies": ["SIEM Performance Optimization"]},
        ]
    },
    "DOCUMENTATION & DELIVERY": {
        "color": "#9F7AEA",
        "tasks": [
            {"name": "User Guide and Technical Documentation", "start": "2025-10-10", "duration": 10, "resource": "All Team", "dependencies": []},
            {"name": "Research Paper and Technical Report", "start": "2025-10-24", "duration": 12, "resource": "All Team", "dependencies": ["User Guide and Technical Documentation"]},
            {"name": "Project Presentation Preparation", "start": "2025-11-21", "duration": 5, "resource": "All Team", "dependencies": ["Research Paper and Technical Report"]},
        ]
    },
    "FUTURE ENHANCEMENTS": {
        "color": "#718096",
        "tasks": [
            {"name": "Advanced APT Simulation Modules", "start": "2025-10-25", "duration": 10, "resource": "Member A", "dependencies": []},
            {"name": "Enhanced Machine Learning Analytics", "start": "2025-11-08", "duration": 15, "resource": "Member C", "dependencies": ["Advanced APT Simulation Modules"]},
            {"name": "CI/CD Pipeline Integration", "start": "2025-11-29", "duration": 10, "resource": "Member B", "dependencies": ["Enhanced Machine Learning Analytics"]},
        ]
    }
}

def calculate_end_date(start_date, duration):
    """Calculate end date excluding weekends"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    days_added = 0
    current_date = start
    
    while days_added < duration -1: # Adjust to include start day
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Monday to Friday
            days_added += 1
    
    return current_date.strftime("%Y-%m-%d")

def create_advanced_gantt():
    """Create an advanced Gantt chart with hierarchical structure and dependencies"""
    
    fig = go.Figure()
    
    # Resource colors
    resource_colors = {
        'Member A': '#3182CE',  # Blue
        'Member B': '#38A169',  # Green  
        'Member C': '#ED8936',  # Orange
        'All Team': '#805AD5'   # Purple
    }
    
    # Build task list with hierarchy
    y_positions = []
    task_names = []
    y_counter = 0
    task_positions = {}  # For dependency tracking
    
    # Create the chart data
    for section_name, section_data in project_structure.items():
        # Add section header
        y_positions.append(y_counter)
        task_names.append(f"<b>{section_name}</b>")
        
        # Add section header bar (lighter background)
        fig.add_trace(go.Scatter(
            x=[datetime(2025, 7, 30), datetime(2025, 12, 31)],
            y=[y_counter, y_counter],
            mode='lines',
            line=dict(color=section_data['color'], width=20),
            opacity=0.2,
            showlegend=False,
            hoverinfo='skip'
        ))
        
        y_counter -= 1
        
        # Add tasks in this section
        for task in section_data['tasks']:
            task_name = task['name']
            start_date = datetime.strptime(task['start'], "%Y-%m-%d")
            end_date = datetime.strptime(calculate_end_date(task['start'], task['duration']), "%Y-%m-%d")
            resource = task['resource']
            
            y_positions.append(y_counter)
            task_names.append(f"     {task_name}")  # Indented task name
            task_positions[task_name] = y_counter
            
            # Add task bar
            fig.add_trace(go.Scatter(
                x=[start_date, end_date, end_date, start_date, start_date],
                y=[y_counter-0.3, y_counter-0.3, y_counter+0.3, y_counter+0.3, y_counter-0.3],
                fill='toself',
                fillcolor=resource_colors[resource],
                line=dict(color=resource_colors[resource], width=2),
                mode='lines',
                name=resource,
                showlegend=resource not in [trace.name for trace in fig.data],
                hovertemplate=f"<b>{task_name}</b><br>" +
                              f"Resource: {resource}<br>" +
                              f"Start: {start_date.strftime('%Y-%m-%d')}<br>" +
                              f"End: {end_date.strftime('%Y-%m-%d')}<br>" +
                              f"Duration: {task['duration']} days<extra></extra>"
            ))
            
            # Add task label
            fig.add_annotation(
                x=start_date + (end_date - start_date) / 2,
                y=y_counter,
                text=f"{resource}",
                showarrow=False,
                font=dict(color='white', size=9, family='Arial Black'),
            )
            
            y_counter -= 1
        
        y_counter -= 0.5  # Extra space between sections
    
    # Add dependency arrows
    for section_name, section_data in project_structure.items():
        for task in section_data['tasks']:
            if task['dependencies']:
                for dep in task['dependencies']:
                    if dep in task_positions:
                        # Draw dependency arrow
                        start_y = task_positions[dep]
                        end_y = task_positions[task['name']]
                        
                        # Calculate arrow positions
                        dep_end_date = None
                        task_start_date = datetime.strptime(task['start'], "%Y-%m-%d")
                        
                        # Find the dependency task's end date
                        for s_name, s_data in project_structure.items():
                            for t in s_data['tasks']:
                                if t['name'] == dep:
                                    dep_end_date = datetime.strptime(calculate_end_date(t['start'], t['duration']), "%Y-%m-%d")
                                    break
                        
                        if dep_end_date:
                            # Add dependency line
                            fig.add_trace(go.Scatter(
                                x=[dep_end_date, task_start_date],
                                y=[start_y, end_y],
                                mode='lines+markers',
                                line=dict(color='#4A5568', width=2, dash='dash'),
                                marker=dict(symbol='arrow-right', size=8, color='#4A5568'),
                                showlegend=False,
                                hovertemplate=f"Dependency: {dep} → {task['name']}<extra></extra>"
                            ))
    
    # Create weekly date range
    start_date_range = datetime(2025, 7, 28)  # Start from Monday before July 30
    end_date_range = datetime(2025, 12, 31)
    
    # Generate weekly ticks
    weekly_dates = []
    current = start_date_range
    while current <= end_date_range:
        weekly_dates.append(current)
        current += timedelta(weeks=1)
    
    # Update layout
    fig.update_layout(
        title={
            'text': '<b>🚀 AI-Driven Detection Engineering Lab</b><br>' +
                    '<sub>Project Timeline with Dependencies & Task Hierarchy</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'family': 'Arial Black', 'color': '#2D3748'}
        },
        
        # X-axis (Timeline)
        xaxis=dict(
            title={'text': '<b>Project Timeline (2025)</b>', 'font': {'size': 16, 'color': '#4A5568'}},
            tickvals=weekly_dates,
            ticktext=[d.strftime('%b %d') for d in weekly_dates],
            tickangle=45,
            showgrid=True,
            gridwidth=1,
            gridcolor='#E2E8F0',
            showline=True,
            linewidth=2,
            linecolor='#CBD5E0',
            range=[start_date_range - timedelta(days=3), end_date_range + timedelta(days=3)]
        ),
        
        # Y-axis (Tasks)
        yaxis=dict(
            title={'text': '<b>Project Tasks & Sections</b>', 'font': {'size': 16, 'color': '#4A5568'}},
            tickvals=y_positions,
            ticktext=task_names,
            showgrid=True,
            gridwidth=1,
            gridcolor='#E2E8F0',
            showline=True,
            linewidth=2,
            linecolor='#CBD5E0',
            autorange='reversed'  # Reverse to show first tasks at top
        ),
        
        # Layout styling
        plot_bgcolor='#F7FAFC',
        paper_bgcolor='white',
        height=1200,
        width=1600,
        
        # Legend
        legend=dict(
            title="<b>Team Members</b>",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font={'size': 12, 'color': '#2D3748'},
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#CBD5E0',
            borderwidth=1
        ),
        
        margin=dict(l=400, r=150, t=120, b=100)
    )
    
    # --- FIX STARTS HERE ---
    
    # Add static vertical lines for milestones using fig.add_shape
    project_start_date = datetime(2025, 7, 30)
    fig.add_shape(type="line", x0=project_start_date, y0=0, x1=project_start_date, y1=1, yref='paper', line=dict(color="red", width=2, dash="dash"))
    fig.add_annotation(x=project_start_date, y=1.05, yref='paper', text="Project Start", showarrow=False, xanchor='left', font=dict(color="red"))

    milestone_date = datetime(2025, 9, 1)
    fig.add_shape(type="line", x0=milestone_date, y0=0, x1=milestone_date, y1=1, yref='paper', line=dict(color="blue", width=2, dash="dot"))
    fig.add_annotation(x=milestone_date, y=1.05, yref='paper', text="Linux Simulation Ready", showarrow=False, xanchor='left', font=dict(color="blue"))

    project_end_date = datetime(2025, 10, 31)
    fig.add_shape(type="line", x0=project_end_date, y0=0, x1=project_end_date, y1=1, yref='paper', line=dict(color="green", width=2, dash="dash"))
    fig.add_annotation(x=project_end_date, y=1.05, yref='paper', text="Project End", showarrow=False, xanchor='left', font=dict(color="green"))
    
    # Add today's date marker if it's within the project timeline
    today = datetime.now()
    if start_date_range <= today <= end_date_range:
        fig.add_shape(type="line", x0=today, y0=0, x1=today, y1=1, yref='paper', line=dict(color="red", width=2, dash="dash"))
        fig.add_annotation(x=today, y=1.05, yref='paper', text="Today", showarrow=False, xanchor='center', font=dict(color="red"))

    # Add other milestone markers
    milestones = [
        (datetime(2025, 10, 2), "Cross-Platform Ready", "#3182CE"),
        (datetime(2025, 10, 14), "Detection Validated", "#38A169"),  
        (datetime(2025, 11, 5), "AI Integration Complete", "#ED8936"),
        (datetime(2025, 11, 27), "Project Delivery", "#805AD5")
    ]
    
    for date, milestone, color in milestones:
        fig.add_shape(type="line", x0=date, y0=0, x1=date, y1=1, yref='paper', line=dict(color=color, width=2, dash="dot"))
        fig.add_annotation(
            x=date,
            y=1.0, 
            yref='paper',
            text=f"📍 {milestone}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            ax=0,
            ay=-25, # Position annotation below the top line
            arrowcolor=color,
            font=dict(size=10, color=color, family="Arial Black"),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor=color,
            borderwidth=1
        )
    
    return fig

# Create and display the chart
def main():
    print("🚀 Generating Advanced Gantt Chart with Dependencies...")
    
    fig = create_advanced_gantt()
    
    # Save in multiple formats
    fig.write_html("advanced_gantt_chart.html", 
                   config={'displayModeBar': True, 'toImageButtonOptions': {'width': 1800, 'height': 1200}})
    fig.write_image("advanced_gantt_chart.png", width=1800, height=1200, scale=2)
    fig.write_image("advanced_gantt_chart.pdf", width=1800, height=1200)
    
    # Display
    fig.show()
    
    print("✅ Advanced Gantt Chart Generated Successfully!")
    print("📁 Files saved:")
    print("   • advanced_gantt_chart.html (Interactive)")
    print("   • advanced_gantt_chart.png (High-resolution)")
    print("   • advanced_gantt_chart.pdf (Print-ready)")

if __name__ == "__main__":
    main()

# Installation requirements:
"""
pip install plotly pandas kaleido python-dateutil numpy

Usage:
python advanced_gantt_chart.py
"""