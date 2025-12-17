# metrics_visualization.py
# Optional: Generate bar charts and metrics visualizations for presentation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set style for professional look
plt.style.use('seaborn-v0_8-darkgrid')

def create_conversion_comparison():
    """Bar chart: Traditional vs AI Chatbot conversion rates."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Traditional\nProcess', 'AI Chatbot\n(Our Solution)']
    completion_rates = [45, 85]  # percentages
    colors = ['#E53E3E', '#48BB78']  # Red for traditional, Green for AI
    
    bars = ax.bar(categories, completion_rates, color=colors, width=0.6, 
                   edgecolor='#2D3748', linewidth=2)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, completion_rates)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value}%',
                ha='center', va='bottom', fontsize=20, fontweight='bold',
                color='white', bbox=dict(boxstyle='round', facecolor=colors[i], alpha=0.8))
    
    ax.set_ylabel('Application Completion Rate (%)', fontsize=14, fontweight='bold')
    ax.set_title('Customer Application Completion Rate Comparison', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    
    # Add improvement annotation
    improvement = completion_rates[1] - completion_rates[0]
    ax.annotate(f'+{improvement}% Improvement', 
                xy=(1, completion_rates[1]), xytext=(0.5, 70),
                arrowprops=dict(arrowstyle='->', color='#2C5282', lw=2),
                fontsize=13, fontweight='bold', color='#2C5282',
                bbox=dict(boxstyle='round', facecolor='#BEE3F8', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('metrics_conversion_comparison.png', dpi=150, bbox_inches='tight', 
                facecolor='white')
    print("✅ Conversion comparison chart generated: metrics_conversion_comparison.png")
    plt.close()


def create_time_to_approval():
    """Bar chart: Time to approval comparison."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Traditional\nProcess', 'AI Chatbot\n(Our Solution)']
    times = [2880, 4.5]  # minutes (2-3 days = 2880 min, vs 4.5 min)
    colors = ['#E53E3E', '#48BB78']
    
    # Use log scale for better visualization
    bars = ax.bar(categories, times, color=colors, width=0.6,
                   edgecolor='#2D3748', linewidth=2)
    
    # Add value labels
    labels = ['2-3 Days\n(2880 min)', '<5 Minutes\n(4.5 min)']
    for i, (bar, label) in enumerate(zip(bars, labels)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                label,
                ha='center', va='bottom', fontsize=16, fontweight='bold',
                color='white', bbox=dict(boxstyle='round', facecolor=colors[i], alpha=0.8))
    
    ax.set_ylabel('Time to Approval (minutes, log scale)', fontsize=14, fontweight='bold')
    ax.set_title('Loan Approval Time Reduction', fontsize=16, fontweight='bold', pad=20)
    ax.set_yscale('log')
    ax.grid(axis='y', alpha=0.3, which='both')
    
    # Add speed improvement annotation
    speedup = times[0] / times[1]
    ax.annotate(f'{speedup:.0f}× Faster', 
                xy=(1, times[1]), xytext=(0.5, 100),
                arrowprops=dict(arrowstyle='->', color='#2C5282', lw=2),
                fontsize=13, fontweight='bold', color='#2C5282',
                bbox=dict(boxstyle='round', facecolor='#BEE3F8', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('metrics_time_to_approval.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    print("✅ Time to approval chart generated: metrics_time_to_approval.png")
    plt.close()


def create_stage_funnel():
    """Funnel chart: Customer journey completion rates."""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    stages = ['Initial\nInquiry', 'Sales\nConversation', 'Verification', 
              'Underwriting', 'Sanction\nLetter']
    completion = [100, 95, 90, 88, 85]  # percentage completing each stage
    colors = ['#4299E1', '#667EEA', '#9F7AEA', '#ED8936', '#48BB78']
    
    # Create horizontal bars (inverted funnel)
    y_pos = np.arange(len(stages))
    bars = ax.barh(y_pos, completion, color=colors, edgecolor='#2D3748', linewidth=2)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, completion)):
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2.,
                f'{value}%',
                ha='left', va='center', fontsize=14, fontweight='bold',
                color='#2D3748')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages, fontsize=13)
    ax.set_xlabel('Customers Completing Stage (%)', fontsize=14, fontweight='bold')
    ax.set_title('Customer Journey Funnel - Stage Completion Rates', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(0, 110)
    ax.invert_yaxis()  # Top to bottom flow
    ax.grid(axis='x', alpha=0.3)
    
    # Add drop-off annotations
    for i in range(len(stages)-1):
        drop = completion[i] - completion[i+1]
        if drop > 0:
            ax.text(105, i + 0.5, f'-{drop}%', 
                   fontsize=10, color='#E53E3E', fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='#FED7D7', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('metrics_stage_funnel.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    print("✅ Stage funnel chart generated: metrics_stage_funnel.png")
    plt.close()


def create_business_impact():
    """Multi-metric bar chart: Business impact metrics."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    metrics = ['Conversion\nRate', 'Customer\nSatisfaction', 'Processing\nCost', 
               'Agent\nEfficiency', 'Scalability']
    traditional = [45, 60, 100, 20, 10]  # baseline percentages/units
    ai_solution = [85, 90, 30, 100, 100]  # our solution
    
    x = np.arange(len(metrics))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, traditional, width, label='Traditional Process',
                   color='#E53E3E', edgecolor='#2D3748', linewidth=1.5)
    bars2 = ax.bar(x + width/2, ai_solution, width, label='AI Chatbot (Ours)',
                   color='#48BB78', edgecolor='#2D3748', linewidth=1.5)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Score / Index (0-100)', fontsize=14, fontweight='bold')
    ax.set_title('Business Impact Metrics Comparison', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=12)
    ax.legend(fontsize=12, loc='upper left')
    ax.set_ylim(0, 120)
    ax.grid(axis='y', alpha=0.3)
    
    # Add improvement arrows
    improvements = ['+89%', '+50%', '-70%', '+400%', '+900%']
    for i, (trad, ai, imp) in enumerate(zip(traditional, ai_solution, improvements)):
        if ai > trad:
            color = '#48BB78'
            arrow = '↑'
        else:
            color = '#48BB78'
            arrow = '↓'
        ax.text(i, max(trad, ai) + 5, f'{arrow} {imp}',
               ha='center', fontsize=10, fontweight='bold', color=color)
    
    plt.tight_layout()
    plt.savefig('metrics_business_impact.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    print("✅ Business impact chart generated: metrics_business_impact.png")
    plt.close()


def main():
    """Generate all metrics visualizations."""
    print("=" * 70)
    print("📊 Generating Metrics Visualizations for Presentation")
    print("=" * 70)
    print()
    
    try:
        print("📈 1/4: Generating Conversion Comparison Chart...")
        create_conversion_comparison()
        
        print("⏱️  2/4: Generating Time to Approval Chart...")
        create_time_to_approval()
        
        print("🎯 3/4: Generating Stage Funnel Chart...")
        create_stage_funnel()
        
        print("💼 4/4: Generating Business Impact Chart...")
        create_business_impact()
        
        print()
        print("=" * 70)
        print("✅ ALL METRICS CHARTS GENERATED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("📁 Output Files (in Diagrams folder):")
        print("   1. metrics_conversion_comparison.png")
        print("   2. metrics_time_to_approval.png")
        print("   3. metrics_stage_funnel.png")
        print("   4. metrics_business_impact.png")
        print()
        print("💡 Use these charts in 'Business Impact' or 'Results' slides!")
        print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
