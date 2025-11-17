#!/usr/bin/env python3
"""
Generate Next Best Action data by applying business rules to customer and device data.
"""

import pandas as pd
from pathlib import Path

def determine_next_best_action(row):
    """
    Apply business rules to determine the next best action for a customer.
    
    Rules:
    1. Speed upgrade, no device upgrade: Fiber customer, CLV 1-3, SQS = 3
    2. Speed Upgrade, new device upgrade: Fiber customer, CLV 7-10, segment is Aspirational Adopters or Peak Performers
    3. Keep As Is: SQS = 3, Churn = 0, segment is Budget Balancers, Foolproof Followers, or Settled Simplifiers
    4. Ship new device: SQS = 1, Churn = 1, segment = Aspirational Adopters
    """
    
    # Rule 4: Ship new device (highest priority for at-risk customers)
    if row['sqs_score'] == 1 and row['churn_risk'] == 1 and row['customer_segment'] == 'Aspirational Adopters':
        return 'Ship new device'
    
    # Rule 2: Speed Upgrade + new device upgrade
    if (row['broadband_type'] == 'Fiber' and 
        row['clv_decile'] >= 7 and row['clv_decile'] <= 10 and 
        row['customer_segment'] in ['Aspirational Adopters', 'Peak Performers']):
        return 'Speed upgrade + new device'
    
    # Rule 1: Speed upgrade, no device upgrade
    if (row['broadband_type'] == 'Fiber' and 
        row['clv_decile'] >= 1 and row['clv_decile'] <= 3 and 
        row['sqs_score'] == 3):
        return 'Speed upgrade only'
    
    # Rule 3: Keep As Is
    if (row['sqs_score'] == 3 and 
        row['churn_risk'] == 0 and 
        row['customer_segment'] in ['Budget Balancers', 'Foolproof Followers', 'Settled Simplifiers']):
        return 'Keep as is'
    
    # Default: No specific action
    return 'No action recommended'

def main():
    print("=" * 60)
    print("Next Best Action Data Generator")
    print("=" * 60)
    
    # Load data
    print("\n📂 Loading customer and device data...")
    customer_data = pd.read_csv("Data/Data Output/customer_data.csv")
    device_data = pd.read_csv("Data/Data Output/device_data.csv")
    
    print(f"✅ Loaded {len(customer_data):,} customers")
    print(f"✅ Loaded {len(device_data):,} devices")
    
    # Merge data
    print("\n🔄 Merging data...")
    merged_data = pd.merge(customer_data, device_data, on='customer_id', how='inner')
    print(f"✅ Merged dataset: {len(merged_data):,} records")
    
    # Apply Next Best Action logic
    print("\n🎯 Applying Next Best Action rules...")
    merged_data['next_best_action'] = merged_data.apply(determine_next_best_action, axis=1)
    
    # Calculate statistics
    print("\n📊 Next Best Action Distribution:")
    action_counts = merged_data['next_best_action'].value_counts()
    for action, count in action_counts.items():
        pct = (count / len(merged_data) * 100)
        print(f"   {action}: {count:,} ({pct:.1f}%)")
    
    # Save to CSV
    output_path = Path("Data/Data Output/nba_data.csv")
    print(f"\n💾 Saving to {output_path}...")
    
    # Select relevant columns for the dashboard
    output_columns = [
        'customer_id',
        'next_best_action',
        'customer_segment',
        'clv_decile',
        'churn_risk',
        'sqs_score',
        'broadband_type',
        'current_bb_speed',
        'network_activity',
        'account_tenure',
        'device_model',
        'device_status',
        'isp'
    ]
    
    merged_data[output_columns].to_csv(output_path, index=False)
    print(f"✅ Saved {len(merged_data):,} records")
    
    print("\n" + "=" * 60)
    print("✨ Next Best Action data generated successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()

