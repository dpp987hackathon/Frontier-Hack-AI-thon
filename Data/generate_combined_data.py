import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate Customer Data (100,000 records)
print("Generating customer data...")

# Customer IDs: unique numbers between 1 and 100,000
customer_ids = list(range(1, 100001))
random.shuffle(customer_ids)

# CLV Decile: 1-10, 10% each
clv_decile = np.repeat(range(1, 11), 10000)
np.random.shuffle(clv_decile)

# Churn Risk: 2% are 1, 98% are 0
churn_risk = np.random.choice([0, 1], size=100000, p=[0.98, 0.02])

# Current BB Speed distribution
# 10% Copper (below 500mb), 32% 500mb, 35% 1Gig, 20% 2Gig
speed_categories = ['Copper', '500mb', '1Gig', '2Gig']
speed_distribution = [0.10, 0.32, 0.35, 0.20]
# Normalize to ensure they sum to 1.0
speed_distribution = [p / sum(speed_distribution) for p in speed_distribution]
current_bb_speed = np.random.choice(speed_categories, size=100000, p=speed_distribution)

# Network Activity: 25% heavy, 50% medium, 25% light
network_activity = np.random.choice(['heavy', 'medium', 'light'], size=100000, p=[0.25, 0.50, 0.25])

# Account Tenure: 1-120 months
account_tenure = np.random.randint(1, 121, size=100000)

# Time of Last Broadband Upgrade: between 1/1/2016 and 11/1/2025
start_date = datetime(2016, 1, 1)
end_date = datetime(2025, 11, 1)
date_range = (end_date - start_date).days
time_of_last_upgrade = [start_date + timedelta(days=random.randint(0, date_range)) for _ in range(100000)]
time_of_last_upgrade = [d.strftime('%Y-%m-%d') for d in time_of_last_upgrade]

# Broadband Type: Copper if speed is Copper, else Fiber
broadband_type = ['Copper' if speed == 'Copper' else 'Fiber' for speed in current_bb_speed]

# Customer Segment distribution
# Aspirational Adopters - 6%, Peak Performers - 22%, Budget Balancers - 14%, 
# Foolproof Followers - 21%, Settled Simplifiers - 36%
segments = ['Aspirational Adopters', 'Peak Performers', 'Budget Balancers', 'Foolproof Followers', 'Settled Simplifiers']
segment_distribution = [0.06, 0.22, 0.14, 0.21, 0.36]
# Normalize to ensure they sum to 1.0
segment_distribution = [p / sum(segment_distribution) for p in segment_distribution]
customer_segment = np.random.choice(segments, size=100000, p=segment_distribution)

# Create Customer DataFrame
customer_df = pd.DataFrame({
    'customer_id': customer_ids,
    'clv_decile': clv_decile,
    'churn_risk': churn_risk,
    'current_bb_speed': current_bb_speed,
    'network_activity': network_activity,
    'account_tenure': account_tenure,
    'time_of_last_broadband_upgrade': time_of_last_upgrade,
    'broadband_type': broadband_type,
    'customer_segment': customer_segment
})

# Save Customer Data
customer_df.to_csv('Data Output/customer_data.csv', index=False)
print(f"Customer data generated: {len(customer_df)} records")

# Generate Device Data (300,000 records)
print("\nGenerating device data...")

device_records = []

# Split customers: 50,000 with 1 device, 50,000 with 2-6 devices
single_device_customers = customer_ids[:50000]
multi_device_customers = customer_ids[50000:]

# Track used serial numbers to ensure uniqueness
used_serials = set()

def generate_unique_serial():
    """Generate a unique 10-digit serial number"""
    while True:
        serial = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        if serial not in used_serials:
            used_serials.add(serial)
            return serial

# Device model mapping to speed compatibility
def get_compatible_device_models(bb_speed):
    """Return list of compatible device models based on broadband speed"""
    if bb_speed == 'Copper':
        # Copper customers can only have Eero 6
        return ['Eero 6']
    elif bb_speed == '500mb':
        # Can use Eero 6+ or higher models (customers at lower speeds than device max)
        # Most should have Eero 6+, but some may have lower models for realism
        return ['Eero 6+', 'Eero 6']
    elif bb_speed == '1Gig':
        # Can use Eero Pro 6 or higher models
        # Most should have Eero Pro 6, but some may have lower models
        return ['Eero Pro 6', 'Eero 6+', 'Eero 6']
    elif bb_speed == '2Gig':
        # Should use Eero Pro 6E, but can also use lower models for realism
        return ['Eero Pro 6E', 'Eero Pro 6', 'Eero 6+']
    return ['Eero Pro 6E']

def select_device_model(bb_speed, compatible_models):
    """Select device model with realistic distribution based on speed"""
    if bb_speed == 'Copper':
        return 'Eero 6'
    elif bb_speed == '500mb':
        # 80% Eero 6+, 20% Eero 6
        return random.choices(['Eero 6+', 'Eero 6'], weights=[0.80, 0.20])[0]
    elif bb_speed == '1Gig':
        # 70% Eero Pro 6, 20% Eero 6+, 10% Eero 6
        return random.choices(['Eero Pro 6', 'Eero 6+', 'Eero 6'], weights=[0.70, 0.20, 0.10])[0]
    elif bb_speed == '2Gig':
        # 60% Eero Pro 6E, 25% Eero Pro 6, 10% Eero 6+, 5% Eero 6
        return random.choices(['Eero Pro 6E', 'Eero Pro 6', 'Eero 6+', 'Eero 6'], weights=[0.60, 0.25, 0.10, 0.05])[0]
    return 'Eero Pro 6E'

# Device status distribution
device_statuses = ['Provisioned', 'CustShipped', 'PendingReturn', 'StockShelved']
status_probs = [0.60, 0.05, 0.10, 0.25]

# ISP distribution
isp_options = ['Frontier Communications', 'Not Frontier ISP']
isp_probs = [0.90, 0.10]

# Ship date range: October 2021 to December 2022
ship_start = datetime(2021, 10, 1)
ship_end = datetime(2022, 12, 31)
ship_date_range = (ship_end - ship_start).days

# Last alive date: 60% current date, 40% random within last 5 years with bias towards current
current_date = datetime(2025, 11, 17)
five_years_ago = datetime(2020, 11, 17)

def generate_last_alive_date():
    """Generate last alive date with 60% current date, 40% historical with bias"""
    if random.random() < 0.60:
        return current_date.strftime('%Y-%m-%d')
    else:
        # Generate date within last 5 years with bias towards current date
        # Using exponential distribution for bias
        days_back = int(np.random.exponential(scale=365) % (5 * 365))
        date = current_date - timedelta(days=days_back)
        return date.strftime('%Y-%m-%d')

# SQS Score distribution: 90% is 3, 7% is 2, 2.5% is 1, 0.5% is 0
sqs_scores = [0, 1, 2, 3]
sqs_probs = [0.005, 0.025, 0.07, 0.90]

# Process single device customers (50,000 customers, 50,000 devices)
print("Processing single device customers...")
for cust_id in single_device_customers:
    # Get customer's broadband speed
    cust_speed = customer_df[customer_df['customer_id'] == cust_id]['current_bb_speed'].values[0]
    
    # Get compatible device models and select one
    compatible_models = get_compatible_device_models(cust_speed)
    device_model = select_device_model(cust_speed, compatible_models)
    
    device_records.append({
        'customer_id': cust_id,
        'serial_number': generate_unique_serial(),
        'device_model': device_model,
        'device_status': np.random.choice(device_statuses, p=status_probs),
        'isp': np.random.choice(isp_options, p=isp_probs),
        'ship_date': (ship_start + timedelta(days=random.randint(0, ship_date_range))).strftime('%Y-%m-%d'),
        'last_alive_date': generate_last_alive_date(),
        'sqs_score': np.random.choice(sqs_scores, p=sqs_probs)
    })

# Process multi device customers (50,000 customers, 250,000 devices)
# Need to generate exactly 250,000 more devices to reach 300,000 total
print("Processing multi device customers...")
remaining_devices_needed = 300000 - 50000  # 250,000 devices needed

# Distribute devices among 50,000 customers (2-6 devices each)
# We need to ensure we get exactly 250,000 devices
devices_per_customer = []
total_devices = 0

# First, assign minimum 2 devices to each customer (100,000 devices)
for _ in range(50000):
    devices_per_customer.append(2)
    total_devices += 2

# Now we need 150,000 more devices (250,000 - 100,000)
# Distribute these randomly among customers, ensuring max 6 per customer
remaining = 150000
customer_indices = list(range(50000))
random.shuffle(customer_indices)

for idx in customer_indices:
    if remaining <= 0:
        break
    # Can add up to 4 more devices (to reach max of 6)
    max_add = min(4, remaining)
    if max_add > 0:
        add_count = random.randint(1, max_add)
        devices_per_customer[idx] += add_count
        remaining -= add_count

# Distribute any remaining devices
while remaining > 0:
    idx = random.choice(customer_indices)
    if devices_per_customer[idx] < 6:
        devices_per_customer[idx] += 1
        remaining -= 1

# Verify we have exactly 250,000 devices
assert sum(devices_per_customer) == 250000, f"Expected 250,000 devices, got {sum(devices_per_customer)}"

# Generate device records for multi-device customers
for i, cust_id in enumerate(multi_device_customers):
    if (i + 1) % 10000 == 0:
        print(f"  Processed {i + 1}/{len(multi_device_customers)} multi-device customers...")
    
    # Get customer's broadband speed
    cust_speed = customer_df[customer_df['customer_id'] == cust_id]['current_bb_speed'].values[0]
    
    # Get compatible device models
    compatible_models = get_compatible_device_models(cust_speed)
    
    # Generate devices for this customer
    num_devices = devices_per_customer[i]
    for _ in range(num_devices):
        device_model = select_device_model(cust_speed, compatible_models)
        
        device_records.append({
            'customer_id': cust_id,
            'serial_number': generate_unique_serial(),
            'device_model': device_model,
            'device_status': np.random.choice(device_statuses, p=status_probs),
            'isp': np.random.choice(isp_options, p=isp_probs),
            'ship_date': (ship_start + timedelta(days=random.randint(0, ship_date_range))).strftime('%Y-%m-%d'),
            'last_alive_date': generate_last_alive_date(),
            'sqs_score': np.random.choice(sqs_scores, p=sqs_probs)
        })

# Create Device DataFrame
device_df = pd.DataFrame(device_records)

# Verify we have exactly 300,000 device records
assert len(device_df) == 300000, f"Expected 300,000 device records, got {len(device_df)}"

# Save Device Data
device_df.to_csv('Data Output/device_data.csv', index=False)
print(f"\nDevice data generated: {len(device_df)} records")

# Print summary statistics
print("\n" + "="*60)
print("DATA GENERATION SUMMARY")
print("="*60)
print(f"\nCustomer Data: {len(customer_df)} records")
print(f"Device Data: {len(device_df)} records")
print(f"\nCustomer BB Speed Distribution:")
print(customer_df['current_bb_speed'].value_counts(normalize=True).sort_index())
print(f"\nDevice Model Distribution:")
print(device_df['device_model'].value_counts(normalize=True).sort_index())
print(f"\nDevice Status Distribution:")
print(device_df['device_status'].value_counts(normalize=True).sort_index())
print(f"\nCustomers with 1 device: {len(single_device_customers)}")
print(f"Customers with multiple devices: {len(multi_device_customers)}")
print(f"\nDevices per customer stats:")
devices_per_customer = device_df.groupby('customer_id').size()
print(f"  Min: {devices_per_customer.min()}")
print(f"  Max: {devices_per_customer.max()}")
print(f"  Mean: {devices_per_customer.mean():.2f}")
print(f"\nSerial number uniqueness: {len(device_df['serial_number'].unique())} unique serials out of {len(device_df)} records")
print("\n" + "="*60)
print("Generation complete!")
