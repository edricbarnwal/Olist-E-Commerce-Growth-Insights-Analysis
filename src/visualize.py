import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

def main():
    print("[*] Starting visualization pipeline...")
    
    # Paths
    processed_dir = r"data/processed"
    assets_dir = r"assets"
    
    # Ensure assets directory exists
    os.makedirs(assets_dir, exist_ok=True)
    
    # Set hacker/minimal aesthetic (dark background, neon accents)
    plt.style.use('dark_background')
    sns.set_theme(style='darkgrid', palette='mako')
    plt.rcParams['axes.facecolor'] = '#0d1117' # GitHub dark mode background
    plt.rcParams['figure.facecolor'] = '#0d1117'
    plt.rcParams['text.color'] = '#c9d1d9'
    plt.rcParams['axes.labelcolor'] = '#c9d1d9'
    plt.rcParams['xtick.color'] = '#c9d1d9'
    plt.rcParams['ytick.color'] = '#c9d1d9'
    plt.rcParams['grid.color'] = '#30363d'
    plt.rcParams['figure.figsize'] = (12, 6)
    
    try:
        print(f"[*] Loading analytical datasets from {processed_dir}...")
        master_df = pd.read_csv(f"{processed_dir}/master_analytical_dataset.csv")
        cat_revenue = pd.read_csv(f"{processed_dir}/category_revenue.csv")
        
        # Parse datetime
        master_df['order_purchase_timestamp'] = pd.to_datetime(master_df['order_purchase_timestamp'])
        
        print("\n--- STATISTICAL INSIGHTS ---")
        # Print basic stats in minimal hacker style
        total_revenue = master_df['total_price'].sum()
        total_orders = len(master_df)
        repeat_rate = (master_df['customer_unique_id'].value_counts() > 1).sum() / master_df['customer_unique_id'].nunique() * 100
        
        print(f"TOTAL ORDERS:  {total_orders:,}")
        print(f"TOTAL REVENUE: R$ {total_revenue:,.2f}")
        print(f"REPEAT RATE:   {repeat_rate:.2f}%")
        print("----------------------------\n")

        print("[*] Generating visualizations...")
        
        # 1. Order Volume Trend
        print("  -> Generating order_volume_trend.png")
        master_df['month'] = master_df['order_purchase_timestamp'].dt.to_period('M').astype(str)
        monthly = master_df.groupby('month').size().reset_index(name='orders')
        # Drop partial months at start/end
        monthly = monthly.iloc[1:-1]
        
        fig, ax = plt.subplots()
        sns.lineplot(data=monthly, x='month', y='orders', color='#58a6ff', linewidth=2.5, marker='o', ax=ax)
        ax.set_title('MONTHLY ORDER VOLUME TREND', fontweight='bold', color='#58a6ff', pad=15)
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Orders')
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        fig.savefig(f"{assets_dir}/order_volume_trend.png", dpi=200, bbox_inches='tight')
        plt.close()

        # 2. Category Revenue Breakdown
        print("  -> Generating category_revenue.png")
        top_cats = cat_revenue.sort_values('total_revenue', ascending=False).head(10)
        fig, ax = plt.subplots()
        sns.barplot(data=top_cats, y='product_category_name_english', x='total_revenue', palette='magma', ax=ax)
        ax.set_title('TOP 10 CATEGORIES BY REVENUE (R$)', fontweight='bold', color='#58a6ff', pad=15)
        ax.set_xlabel('Total Revenue (R$)')
        ax.set_ylabel('Category')
        plt.tight_layout()
        fig.savefig(f"{assets_dir}/category_revenue.png", dpi=200, bbox_inches='tight')
        plt.close()

        # 3. Geographic Distribution
        print("  -> Generating geo_distribution.png")
        top_states = master_df['customer_state'].value_counts().head(10).reset_index()
        top_states.columns = ['state', 'customers']
        fig, ax = plt.subplots()
        sns.barplot(data=top_states, x='state', y='customers', color='#2ea043', ax=ax)
        ax.set_title('CUSTOMER DISTRIBUTION BY STATE', fontweight='bold', color='#58a6ff', pad=15)
        ax.set_xlabel('State')
        ax.set_ylabel('Number of Customers')
        plt.tight_layout()
        fig.savefig(f"{assets_dir}/geo_distribution.png", dpi=200, bbox_inches='tight')
        plt.close()

        # 4. Delivery Performance Impact
        print("  -> Generating review_impact.png")
        # Filter where review_score and is_late are not null
        impact_df = master_df.dropna(subset=['review_score', 'is_late'])
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(data=impact_df, x='is_late', y='review_score', palette=['#2ea043', '#f85149'], ax=ax, errorbar=None)
        ax.set_title('AVERAGE REVIEW SCORE: ON-TIME VS LATE', fontweight='bold', color='#58a6ff', pad=15)
        ax.set_xticklabels(['On-Time / Early', 'Late Delivery'])
        ax.set_xlabel('Delivery Status')
        ax.set_ylabel('Average Review Score (1-5)')
        ax.set_ylim(0, 5)
        
        # Add labels on bars
        means = impact_df.groupby('is_late')['review_score'].mean()
        for i, val in enumerate(means):
            ax.text(i, val - 0.5, f"{val:.2f}★", color='white', ha='center', fontweight='bold', fontsize=14)
            
        plt.tight_layout()
        fig.savefig(f"{assets_dir}/review_impact.png", dpi=200, bbox_inches='tight')
        plt.close()

        print("[+] Visualization generation complete. Images saved to assets/ directory.")
        
    except Exception as e:
        print(f"[-] ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
