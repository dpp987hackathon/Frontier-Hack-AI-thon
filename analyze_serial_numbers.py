import pandas as pd

# Load the data
customer_df = pd.read_csv('Data/Data Output/customer_data.csv')
device_df = pd.read_csv('Data/Data Output/device_data.csv')

print("=" * 60)
print("SERIAL NUMBER ANALYSIS")
print("=" * 60)

# Basic counts
print(f"\nTotal customers: {len(customer_df):,}")
print(f"Total device records: {len(device_df):,}")
print(f"Unique customers with devices: {device_df['customer_id'].nunique():,}")
print(f"Unique serial numbers: {device_df['serial_number'].nunique():,}")

# Check if serial numbers are unique per customer
serial_customer_mapping = device_df.groupby('serial_number')['customer_id'].nunique()
customers_per_serial = serial_customer_mapping.value_counts().sort_index()

print("\n" + "=" * 60)
print("SERIAL NUMBER UNIQUENESS")
print("=" * 60)

print("\nCustomers per serial number distribution:")
for num_customers, count in customers_per_serial.items():
    print(f"  {count:,} serial numbers are associated with {num_customers} customer(s)")

# Find customers with unique serial numbers (serial number used by only one customer)
unique_serials = serial_customer_mapping[serial_customer_mapping == 1].index
customers_with_unique_serials = device_df[device_df['serial_number'].isin(unique_serials)]['customer_id'].nunique()

print("\n" + "=" * 60)
print("ANSWER TO YOUR QUESTION")
print("=" * 60)
print(f"\nCustomers with unique serial numbers: {customers_with_unique_serials:,}")
print(f"Percentage: {customers_with_unique_serials/customer_df['customer_id'].nunique()*100:.2f}%")

# Check for customers with multiple devices
devices_per_customer = device_df.groupby('customer_id')['serial_number'].count()
customers_with_multiple_devices = (devices_per_customer > 1).sum()

print("\n" + "=" * 60)
print("ADDITIONAL INSIGHTS")
print("=" * 60)
print(f"\nCustomers with multiple device records: {customers_with_multiple_devices:,}")
if customers_with_multiple_devices > 0:
    print(f"Max devices per customer: {devices_per_customer.max()}")
    print(f"Average devices per customer: {devices_per_customer.mean():.2f}")

# Check if any serial numbers are shared across customers
shared_serials = serial_customer_mapping[serial_customer_mapping > 1]
if len(shared_serials) > 0:
    print(f"\nSerial numbers shared by multiple customers: {len(shared_serials):,}")
    print("\nSample of shared serial numbers:")
    sample_shared = device_df[device_df['serial_number'].isin(shared_serials.index.tolist()[:5])][['customer_id', 'serial_number']].sort_values('serial_number').head(10)
    print(sample_shared.to_string(index=False))

