import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("Starting data generation...")

# ============================================================================
# CUSTOMER DATA GENERATION (200,000 records)
# ============================================================================

print("\n1. Generating Customer Data (200,000 records)...")

num_customers = 200000

# Generate customer_ids
customer_ids = list(range(1, num_customers + 1))

# Generate clv_decile (10% each value from 1-10)
clv_decile = []
for decile in range(1, 11):
    clv_decile.extend([decile] * (num_customers // 10))
np.random.shuffle(clv_decile)

# Generate churn_risk (2% are 1, 98% are 0)
num_churners = int(num_customers * 0.02)
churn_risk = [1] * num_churners + [0] * (num_customers - num_churners)
np.random.shuffle(churn_risk)

# Generate current_bb_speed
# 10% Copper (<500), 32% 500mb, 35% 1Gig, 20% 2Gig, 3% other
speed_distribution = (
    ['100 Mbps'] * int(num_customers * 0.05) +
    ['200 Mbps'] * int(num_customers * 0.05) +
    ['500 Mbps'] * int(num_customers * 0.32) +
    ['1 Gig'] * int(num_customers * 0.35) +
    ['2 Gig'] * int(num_customers * 0.20) +
    ['5 Gig'] * int(num_customers * 0.03)
)
# Fill any remaining to reach exact 200,000
while len(speed_distribution) < num_customers:
    speed_distribution.append('1 Gig')
np.random.shuffle(speed_distribution)

# Generate broadband_type based on speed
broadband_type = []
for speed in speed_distribution:
    if speed in ['100 Mbps', '200 Mbps']:
        broadband_type.append('Copper')
    else:
        broadband_type.append('Fiber')

# Generate network_activity (25% heavy, 50% medium, 25% light)
network_activity = (
    ['heavy'] * int(num_customers * 0.25) +
    ['medium'] * int(num_customers * 0.50) +
    ['light'] * int(num_customers * 0.25)
)
while len(network_activity) < num_customers:
    network_activity.append('medium')
np.random.shuffle(network_activity)

# Generate account_tenure (1-120 months)
# Bias towards longer tenure (more established customers)
account_tenure = np.random.beta(2, 1.5, num_customers) * 120
account_tenure = np.clip(account_tenure, 1, 120).astype(int)

# Generate time_of_last_broadband_upgrade (1/1/2016 to 11/01/2025)
start_date = datetime(2016, 1, 1)
end_date = datetime(2025, 11, 1)
date_range = (end_date - start_date).days

upgrade_dates = []
for _ in range(num_customers):
    random_days = random.randint(0, date_range)
    upgrade_date = start_date + timedelta(days=random_days)
    upgrade_dates.append(upgrade_date.strftime('%Y-%m-%d'))

# Generate customer_segment
# Aspirational Adopters 6%, Peak Performers 22%, Budget Balancers 14%, 
# Foolproof Followers 21%, Settled Simplifiers 36%, Other 1%
customer_segment = (
    ['Aspirational Adopters'] * int(num_customers * 0.06) +
    ['Peak Performers'] * int(num_customers * 0.22) +
    ['Budget Balancers'] * int(num_customers * 0.14) +
    ['Foolproof Followers'] * int(num_customers * 0.21) +
    ['Settled Simplifiers'] * int(num_customers * 0.36) +
    ['Value Seekers'] * int(num_customers * 0.01)
)
while len(customer_segment) < num_customers:
    customer_segment.append('Settled Simplifiers')
np.random.shuffle(customer_segment)

# Create customer DataFrame
customer_df = pd.DataFrame({
    'customer_id': customer_ids,
    'clv_decile': clv_decile,
    'churn_risk': churn_risk,
    'current_bb_speed': speed_distribution,
    'network_activity': network_activity,
    'account_tenure': account_tenure,
    'time_of_last_broadband_upgrade': upgrade_dates,
    'broadband_type': broadband_type,
    'customer_segment': customer_segment
})

print(f"✓ Customer data generated: {len(customer_df)} records")

# ============================================================================
# DEVICE DATA GENERATION (300,000 records)
# ============================================================================

print("\n2. Generating Device Data (300,000 records)...")

# Determine device count per customer
# 50,000 customers with 1 device, 150,000 with 2-6 devices
customers_with_one_device = random.sample(customer_ids, 50000)
customers_with_multiple_devices = [c for c in customer_ids if c not in customers_with_one_device]

device_records = []
used_serial_numbers = set()

def generate_unique_serial():
    """Generate a unique 10-digit serial number"""
    while True:
        serial = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        if serial not in used_serial_numbers:
            used_serial_numbers.add(serial)
            return serial

def get_device_model_for_speed(bb_speed, broadband_type):
    """
    Returns appropriate device model based on broadband speed.
    Allows for devices that support higher speeds than customer has.
    """
    if broadband_type == 'Copper':
        # Copper customers only get Eero 6
        return 'Eero 6'
    
    if bb_speed == '500 Mbps':
        # Can get Eero 6+ or higher models
        choices = ['Eero 6+', 'Eero Pro 6', 'Eero Pro 6E']
        weights = [0.7, 0.2, 0.1]  # More realistic distribution
        return random.choices(choices, weights=weights)[0]
    
    elif bb_speed == '1 Gig':
        # Can get Eero Pro 6 or Eero Pro 6E
        choices = ['Eero Pro 6', 'Eero Pro 6E']
        weights = [0.7, 0.3]
        return random.choices(choices, weights=weights)[0]
    
    elif bb_speed in ['2 Gig', '5 Gig']:
        # Must get Eero Pro 6E
        return 'Eero Pro 6E'
    
    else:
        # Default for any other case
        return 'Eero 6+'

def generate_last_alive_date():
    """
    Generate last_alive_date: 60% current date, 40% random within last 5 years
    with bias towards current date
    """
    if random.random() < 0.60:
        # 60% are current date
        return '2025-11-17'
    else:
        # 40% are random dates within last 5 years, biased towards recent
        current_date = datetime(2025, 11, 17)
        days_in_5_years = 365 * 5
        
        # Use beta distribution to bias towards recent dates
        random_factor = np.random.beta(1, 3)  # Skewed towards recent
        days_ago = int(random_factor * days_in_5_years)
        
        past_date = current_date - timedelta(days=days_ago)
        return past_date.strftime('%Y-%m-%d')

def generate_ship_date():
    """Generate ship date between October 2021 and December 2022"""
    start = datetime(2021, 10, 1)
    end = datetime(2022, 12, 31)
    days_between = (end - start).days
    random_days = random.randint(0, days_between)
    ship_date = start + timedelta(days=random_days)
    return ship_date.strftime('%Y-%m-%d')

def generate_sqs_score():
    """Generate SQS score: 90% are 3, 7% are 2, 2.5% are 1, 0.5% are 0"""
    rand = random.random()
    if rand < 0.90:
        return 3
    elif rand < 0.97:
        return 2
    elif rand < 0.995:
        return 1
    else:
        return 0

def generate_device_status():
    """Generate device status with correct distribution"""
    rand = random.random()
    if rand < 0.60:
        return 'Provisioned'
    elif rand < 0.65:
        return 'CustShipped'
    elif rand < 0.75:
        return 'PendingReturn'
    else:
        return 'StockShelved'

def generate_isp():
    """Generate ISP: 90% Frontier, 10% Not Frontier"""
    return 'Frontier Communications' if random.random() < 0.90 else 'Not Frontier ISP'

print("  - Generating devices for customers with 1 device...")
# Generate 1 device for 50,000 customers
for customer_id in customers_with_one_device:
    customer_info = customer_df[customer_df['customer_id'] == customer_id].iloc[0]
    
    device_model = get_device_model_for_speed(
        customer_info['current_bb_speed'],
        customer_info['broadband_type']
    )
    
    device_records.append({
        'customer_id': customer_id,
        'device_model': device_model,
        'device_status': generate_device_status(),
        'isp': generate_isp(),
        'ship_date': generate_ship_date(),
        'last_alive_date': generate_last_alive_date(),
        'sqs_score': generate_sqs_score(),
        'serial_number': generate_unique_serial()
    })

print("  - Generating devices for customers with 2-6 devices...")
# Generate 2-6 devices for 150,000 customers to reach 300,000 total devices
remaining_devices = 300000 - 50000  # 250,000 devices remaining

# Calculate average devices per multi-device customer
avg_devices = remaining_devices / len(customers_with_multiple_devices)

# Generate device counts weighted to reach exactly 250,000
device_counts = []
for _ in range(len(customers_with_multiple_devices)):
    # Weight towards 2-3 devices, but allow up to 6
    count = random.choices([2, 3, 4, 5, 6], weights=[0.35, 0.30, 0.20, 0.10, 0.05])[0]
    device_counts.append(count)

# Adjust to reach exactly 250,000
current_total = sum(device_counts)
adjustment_needed = remaining_devices - current_total

# Distribute adjustment
while adjustment_needed != 0:
    idx = random.randint(0, len(device_counts) - 1)
    if adjustment_needed > 0 and device_counts[idx] < 6:
        device_counts[idx] += 1
        adjustment_needed -= 1
    elif adjustment_needed < 0 and device_counts[idx] > 2:
        device_counts[idx] -= 1
        adjustment_needed += 1

# Generate devices for multi-device customers
for i, customer_id in enumerate(customers_with_multiple_devices):
    customer_info = customer_df[customer_df['customer_id'] == customer_id].iloc[0]
    num_devices = device_counts[i]
    
    for _ in range(num_devices):
        device_model = get_device_model_for_speed(
            customer_info['current_bb_speed'],
            customer_info['broadband_type']
        )
        
        device_records.append({
            'customer_id': customer_id,
            'device_model': device_model,
            'device_status': generate_device_status(),
            'isp': generate_isp(),
            'ship_date': generate_ship_date(),
            'last_alive_date': generate_last_alive_date(),
            'sqs_score': generate_sqs_score(),
            'serial_number': generate_unique_serial()
        })

# Create device DataFrame
device_df = pd.DataFrame(device_records)

print(f"✓ Device data generated: {len(device_df)} records")
print(f"  - Unique serial numbers: {len(used_serial_numbers)}")

# ============================================================================
# SAVE TO CSV
# ============================================================================

print("\n3. Saving to CSV files...")

customer_output_path = 'Data/Data Output/customer_data.csv'
device_output_path = 'Data/Data Output/device_data.csv'

customer_df.to_csv(customer_output_path, index=False)
device_df.to_csv(device_output_path, index=False)

print(f"✓ Customer data saved to: {customer_output_path}")
print(f"✓ Device data saved to: {device_output_path}")

# ============================================================================
# GENERATE SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*70)
print("DATA GENERATION SUMMARY")
print("="*70)

print("\n📊 CUSTOMER DATA STATISTICS:")
print(f"  Total Records: {len(customer_df):,}")
print(f"\n  CLV Decile Distribution:")
for i in range(1, 11):
    count = len(customer_df[customer_df['clv_decile'] == i])
    pct = (count / len(customer_df)) * 100
    print(f"    Decile {i}: {count:,} ({pct:.1f}%)")

print(f"\n  Churn Risk Distribution:")
churn_counts = customer_df['churn_risk'].value_counts()
for val in [0, 1]:
    count = churn_counts.get(val, 0)
    pct = (count / len(customer_df)) * 100
    print(f"    {val}: {count:,} ({pct:.1f}%)")

print(f"\n  Broadband Speed Distribution:")
for speed in customer_df['current_bb_speed'].value_counts().index:
    count = len(customer_df[customer_df['current_bb_speed'] == speed])
    pct = (count / len(customer_df)) * 100
    print(f"    {speed}: {count:,} ({pct:.1f}%)")

print(f"\n  Broadband Type Distribution:")
for btype in ['Copper', 'Fiber']:
    count = len(customer_df[customer_df['broadband_type'] == btype])
    pct = (count / len(customer_df)) * 100
    print(f"    {btype}: {count:,} ({pct:.1f}%)")

print(f"\n  Network Activity Distribution:")
for activity in ['heavy', 'medium', 'light']:
    count = len(customer_df[customer_df['network_activity'] == activity])
    pct = (count / len(customer_df)) * 100
    print(f"    {activity}: {count:,} ({pct:.1f}%)")

print(f"\n  Customer Segment Distribution:")
for segment in customer_df['customer_segment'].value_counts().index:
    count = len(customer_df[customer_df['customer_segment'] == segment])
    pct = (count / len(customer_df)) * 100
    print(f"    {segment}: {count:,} ({pct:.1f}%)")

print("\n📱 DEVICE DATA STATISTICS:")
print(f"  Total Records: {len(device_df):,}")
print(f"  Unique Serial Numbers: {len(device_df['serial_number'].unique()):,}")

print(f"\n  Device Model Distribution:")
for model in device_df['device_model'].value_counts().index:
    count = len(device_df[device_df['device_model'] == model])
    pct = (count / len(device_df)) * 100
    print(f"    {model}: {count:,} ({pct:.1f}%)")

print(f"\n  Device Status Distribution:")
for status in device_df['device_status'].value_counts().index:
    count = len(device_df[device_df['device_status'] == status])
    pct = (count / len(device_df)) * 100
    print(f"    {status}: {count:,} ({pct:.1f}%)")

print(f"\n  ISP Distribution:")
for isp in device_df['isp'].value_counts().index:
    count = len(device_df[device_df['isp'] == isp])
    pct = (count / len(device_df)) * 100
    print(f"    {isp}: {count:,} ({pct:.1f}%)")

print(f"\n  SQS Score Distribution:")
for score in sorted(device_df['sqs_score'].unique()):
    count = len(device_df[device_df['sqs_score'] == score])
    pct = (count / len(device_df)) * 100
    print(f"    {score}: {count:,} ({pct:.1f}%)")

print(f"\n  Devices per Customer:")
devices_per_customer = device_df.groupby('customer_id').size()
print(f"    Customers with 1 device: {len(devices_per_customer[devices_per_customer == 1]):,}")
print(f"    Customers with 2+ devices: {len(devices_per_customer[devices_per_customer > 1]):,}")
print(f"    Max devices per customer: {devices_per_customer.max()}")
print(f"    Avg devices per customer: {devices_per_customer.mean():.2f}")

print("\n" + "="*70)
print("✅ DATA GENERATION COMPLETE!")
print("="*70)

