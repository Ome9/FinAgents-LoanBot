# generate_all_diagrams.py
# Master script to generate all loan chatbot diagrams for presentation slides
import sys
import os

# Add Diagrams directory to path
sys.path.insert(0, os.path.dirname(__file__))

from loan_architecture_diagram import create_architecture_diagram
from loan_flow_diagram import create_flow_diagram
from loan_data_flow import create_data_flow_diagram

def main():
    """Generate all diagrams for EY Techathon presentation."""
    print("=" * 70)
    print("🎨 Generating All Diagrams for Loan Chatbot Presentation")
    print("=" * 70)
    print()
    
    try:
        # 1. Architecture Diagram (Master-Worker Pattern)
        print("📐 1/3: Generating Architecture Diagram...")
        create_architecture_diagram('loan_architecture_diagram')
        print()
        
        # 2. Flow Diagram (Customer Journey)
        print("📊 2/3: Generating Flow Diagram...")
        create_flow_diagram('loan_flow_diagram')
        print()
        
        # 3. Data Flow Diagram (State Management)
        print("🔄 3/3: Generating Data Flow Diagram...")
        create_data_flow_diagram('loan_data_flow')
        print()
        
        print("=" * 70)
        print("✅ ALL DIAGRAMS GENERATED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("📁 Output Files (in Diagrams folder):")
        print("   1. loan_architecture_diagram.png - Master-Worker Architecture")
        print("   2. loan_flow_diagram.png - End-to-End Customer Journey Flowchart")
        print("   3. loan_data_flow.png - Data Flow & State Management")
        print()
        print("📏 All diagrams optimized for 16:9 slide ratio (1920x1080 or 1280x720)")
        print("💡 Ready to insert into PowerPoint/Google Slides!")
        print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
