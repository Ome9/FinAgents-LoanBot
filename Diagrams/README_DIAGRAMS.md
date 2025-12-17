# Loan Chatbot Diagrams for Presentation

This folder contains Python scripts to generate professional diagrams for the EY Techathon presentation slides.

## 📋 Required Software

Install Graphviz before running the scripts:

### Windows:
```powershell
# Using Chocolatey
choco install graphviz

# OR download installer from:
# https://graphviz.org/download/
```

### Python Package:
```bash
pip install graphviz
```

## 🎨 Available Diagrams

### 1. **Architecture Diagram** (`loan_architecture_diagram.py`)
- **Purpose:** Shows Master-Worker architecture with all 4 agents
- **Contains:** 
  - Frontend Layer (React UI)
  - Master Agent Layer (LangGraph orchestrator)
  - Worker Agents Layer (Sales, Verification, Underwriting, Sanction)
  - External Services (Mock CRM, Credit Bureau, Offer Mart)
- **Output:** `loan_architecture_diagram.png`
- **Slide Usage:** "Solution Architecture" slide

### 2. **Flow Diagram** (`loan_flow_diagram.py`)
- **Purpose:** End-to-end customer journey flowchart with decision diamonds
- **Contains:**
  - Complete workflow from user authentication to sanction letter
  - Decision points (credit score checks, amount validation, EMI checks)
  - Approval and rejection paths
  - Conditional approval (salary slip upload)
- **Output:** `loan_flow_diagram.png`
- **Slide Usage:** "Customer Journey" or "Algorithm Flow" slide

### 3. **Data Flow Diagram** (`loan_data_flow.py`)
- **Purpose:** Shows how data moves and transforms between agents
- **Contains:**
  - State object evolution at each stage
  - Data inputs/outputs for each agent
  - External API calls (CRM, Credit Bureau, Offer Mart)
  - Complete state management visualization
- **Output:** `loan_data_flow.png`
- **Slide Usage:** "Data Flow" or "Implementation Details" slide

## 🚀 How to Generate Diagrams

### Option 1: Generate All at Once (Recommended)
```bash
cd Diagrams
python generate_all_diagrams.py
```

### Option 2: Generate Individual Diagrams
```bash
cd Diagrams

# Architecture diagram
python loan_architecture_diagram.py

# Flow diagram
python loan_flow_diagram.py

# Data flow diagram
python loan_data_flow.py
```

## 📐 Diagram Specifications

- **Aspect Ratio:** 16:9 (optimized for presentation slides)
- **Resolution:** 150 DPI (high quality for projection)
- **Format:** PNG (widely compatible, good quality)
- **Dimensions:** Suitable for 1920x1080 or 1280x720 slides
- **Colors:** Professional color scheme matching Tata Capital branding

## 📊 Color Coding Guide

- **Blue (#3182CE):** Frontend / User-facing components
- **Orange (#D69E2E):** Master Agent / Orchestrator
- **Purple (#805AD5):** Verification processes
- **Orange-Red (#DD6B20):** Underwriting / Risk assessment
- **Green (#38A169):** Approval / Success states
- **Red (#E53E3E):** External services / APIs
- **Yellow (#F6AD55):** Decision points / Confirmations

## 📝 Customization

To modify diagrams:

1. Open the respective `.py` file
2. Edit the node labels, colors, or connections
3. Re-run the script to regenerate the PNG

### Example: Change a node label
```python
# In loan_architecture_diagram.py, find:
c.node('SalesAgent', label='''<
<TABLE...>
  ...
</TABLE>>''')

# Modify the HTML table content as needed
```

## 🖼️ Using Diagrams in Slides

### PowerPoint:
1. Insert → Pictures
2. Select generated PNG file
3. Resize to fit slide (maintains aspect ratio)
4. Add slide title and annotations

### Google Slides:
1. Insert → Image → Upload from computer
2. Select generated PNG file
3. Drag corners to resize
4. Add text boxes for annotations

## 🔧 Troubleshooting

### Error: "Graphviz executable not found"
```bash
# Windows: Add Graphviz bin to PATH
# Default location: C:\Program Files\Graphviz\bin

# Or install via Chocolatey:
choco install graphviz
```

### Error: "No module named 'graphviz'"
```bash
pip install graphviz
```

### Diagram looks pixelated
- Increase DPI in script: `g.attr(dpi='300')`
- Re-generate diagram

### Text is too small
- Increase fontsize: `fontsize='16'` (default is 12-14)
- Re-generate diagram

## 📌 Additional Diagrams (Optional)

If you need more diagrams for the presentation:

### Wireframes:
- Take screenshots of the actual running application
- Use browser developer tools to show mobile responsive view
- Annotate screenshots with arrows and labels in PowerPoint

### Graphical Representations:
Create simple Python scripts using matplotlib or plotly:

```python
# Example: Conversion Rate Comparison
import matplotlib.pyplot as plt

categories = ['Traditional Process', 'AI Chatbot']
completion_rates = [45, 85]  # percentages

plt.bar(categories, completion_rates, color=['#E53E3E', '#48BB78'])
plt.ylabel('Completion Rate (%)')
plt.title('Application Completion Rate Improvement')
plt.ylim(0, 100)
plt.savefig('conversion_improvement.png', dpi=150, bbox_inches='tight')
```

## 📚 References

- Graphviz Documentation: https://graphviz.org/documentation/
- Python Graphviz Package: https://graphviz.readthedocs.io/

## ✅ Checklist for Presentation

- [ ] All 3 diagrams generated successfully
- [ ] Diagrams are high quality (no pixelation)
- [ ] Text is readable (not too small)
- [ ] Colors are professional and consistent
- [ ] Diagrams fit well in 16:9 slides
- [ ] Saved in accessible location for presentation file

---

**Generated for:** EY Techathon Challenge II - BFSI (Tata Capital)  
**Project:** Agentic AI Loan Sales Chatbot  
**Date:** December 2025
