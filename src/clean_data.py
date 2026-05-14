import pandas as pd
import os
import sys

def main():
    print("[*] Starting data cleaning pipeline...")
    
    # Paths
    raw_dir = r"data/raw"
    processed_dir = r"data/processed"
    
    # Ensure processed directory exists
    os.makedirs(processed_dir, exist_ok=True)
    
    try:
        # Load raw data
        print(f"[*] Loading raw data from {raw_dir}...")
        orders = pd.read_csv(f"{raw_dir}/olist_orders_dataset.csv")
        order_items = pd.read_csv(f"{raw_dir}/olist_order_items_dataset.csv")
        payments = pd.read_csv(f"{raw_dir}/olist_order_payments_dataset.csv")
        reviews = pd.read_csv(f"{raw_dir}/olist_order_reviews_dataset.csv")
        products = pd.read_csv(f"{raw_dir}/olist_products_dataset.csv")
        cat_trans = pd.read_csv(f"{raw_dir}/product_category_name_translation.csv")
        customers = pd.read_csv(f"{raw_dir}/olist_customers_dataset.csv")
        
        print("[*] Converting datetime columns...")
        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
        orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
        
        print("[*] Translating product categories...")
        products = products.merge(cat_trans, on='product_category_name', how='left')
        # Fill missing english translations with original portuguese
        products['product_category_name_english'].fillna(products['product_category_name'], inplace=True)
        
        print("[*] Computing logistics performance metrics...")
        # Only consider delivered orders for delivery metrics
        delivered = orders[orders['order_status'] == 'delivered'].copy()
        delivered['early_late_days'] = (delivered['order_estimated_delivery_date'] - delivered['order_delivered_customer_date']).dt.days
        delivered['is_late'] = delivered['early_late_days'] < 0
        
        print("[*] Merging master analytical dataset...")
        # Join items with products to get category names
        items_prod = order_items.merge(products[['product_id', 'product_category_name_english']], on='product_id', how='left')
        
        # Aggregate item data per order
        order_summary = items_prod.groupby('order_id').agg(
            total_items=('order_item_id', 'count'),
            total_price=('price', 'sum'),
            total_freight=('freight_value', 'sum')
        ).reset_index()
        
        # Merge orders with customer data
        orders_cust = orders.merge(customers[['customer_id', 'customer_unique_id', 'customer_state', 'customer_city']], on='customer_id', how='left')
        
        # Merge with aggregated items
        master_df = orders_cust.merge(order_summary, on='order_id', how='left')
        
        # Merge with delivery metrics
        master_df = master_df.merge(delivered[['order_id', 'early_late_days', 'is_late']], on='order_id', how='left')
        
        # Merge with review scores (taking the mean if multiple reviews exist)
        avg_reviews = reviews.groupby('order_id')['review_score'].mean().reset_index()
        master_df = master_df.merge(avg_reviews, on='order_id', how='left')
        
        print(f"[*] Saving master processed dataset ({master_df.shape[0]} rows) to {processed_dir}...")
        master_df.to_csv(f"{processed_dir}/master_analytical_dataset.csv", index=False)
        
        # Also save category revenue for easy plotting
        cat_revenue = items_prod.groupby('product_category_name_english')['price'].sum().reset_index()
        cat_revenue.rename(columns={'price': 'total_revenue'}, inplace=True)
        cat_revenue.to_csv(f"{processed_dir}/category_revenue.csv", index=False)
        
        print("[+] Data cleaning complete. Outputs saved successfully.")
        
    except Exception as e:
        print(f"[-] ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
