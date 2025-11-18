#!/usr/bin/env python3
"""
Generate Next Best Action data by applying business rules to customer and device data.
"""

import pandas as pd
from pathlib import Path

def determine_next_best_action(row):
    """
    Apply business rules based on device capability vs. current speed.
    
    Device Capabilities (max speed supported):
    - Eero 6: 1Gig
    - Eero 6+: 1Gig
    - Pro 6: 2Gig
    - Pro 6e: 5Gig
    
    Rules:
    1. Speed > Device Capability → Ship new device (customer speed exceeds device)
    2. Speed = Device Capability → Speed upgrade + new device (device at max)
    3. Speed < Device Capability → Speed upgrade only (device underutilized)
    4. Otherwise → Keep as is
    """
    
    # Define device max capabilities
    device_capabilities = {
        'Eero 6': '1Gig',
        'Eero 6+': '1Gig',
        'Pro 6': '2Gig',
        'Pro 6e': '5Gig'
    }
    
    # Define speed tier ordering for comparison
    speed_order = {
        '50Mbps': 1,
        '100Mbps': 2,
        '200Mbps': 3,
        '500Mbps': 4,
        '1Gig': 5,
        '2Gig': 6,
        '5Gig': 7
    }
    
    device_model = row['device_model']
    current_speed = row['current_bb_speed']
    
    # Only process if device is in our known list
    if device_model not in device_capabilities:
        return 'Keep as is'
    
    device_max_speed = device_capabilities[device_model]
    
    # Get numeric comparison values
    current_speed_value = speed_order.get(current_speed, 0)
    device_max_value = speed_order.get(device_max_speed, 0)
    
    # Rule 1: Customer speed exceeds device capability → Ship new device
    if current_speed_value > device_max_value:
        return 'Ship new device'
    
    # Rule 2: Customer speed equals device max capability → Speed upgrade + new device
    elif current_speed_value == device_max_value:
        return 'Speed upgrade + new device'
    
    # Rule 3: Customer speed below device capability → Speed upgrade only
    elif current_speed_value < device_max_value:
        return 'Speed upgrade only'
    
    # Rule 4: Default
    return 'Keep as is'

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

