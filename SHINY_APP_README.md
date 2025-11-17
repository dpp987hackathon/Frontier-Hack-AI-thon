# Device Analytics Dashboard - Shiny App

## Overview

This Shiny for Python application provides an interactive dashboard for analyzing device data with focus on Frontier Communications devices and their activity status.

## Features

### Tab 1: Device Overview
- **Hierarchical Device Breakdown**: Visual tree showing device distribution
  - Total devices split by ISP (Frontier vs Non-Frontier)
  - Each ISP category further split by Active/Inactive status
  - **TARGET GROUP**: Frontier + Active devices (highlighted in green)
- **Interactive Threshold**: Adjust the "active" threshold (default: 30 days)
- **Visual Charts**: Pie charts showing distribution for both Frontier and Non-Frontier devices
- **Real-time Statistics**: Summary panel with key metrics

### Tab 2: Customer Analysis
- Placeholder for customer-related analytics (to be implemented)

### Tab 3: Device Details
- Placeholder for detailed device metrics (to be implemented)

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure data files are in place**:
   - `Data/Data Output/customer_data.csv`
   - `Data/Data Output/device_data.csv`

## Running the App

1. **From the command line**:
   ```bash
   shiny run app.py
   ```

2. **With auto-reload during development**:
   ```bash
   shiny run app.py --reload
   ```

3. **Specify port (optional)**:
   ```bash
   shiny run app.py --port 8000
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

## Data Requirements

### device_data.csv
Required columns:
- `customer_id`: Unique customer identifier
- `serial_number`: Device serial number
- `device_model`: Model of the device
- `device_status`: Current status of the device
- `isp`: Internet Service Provider name
- `ship_date`: Date device was shipped
- `last_alive_date`: Last date device was active (YYYY-MM-DD format)
- `sqs_score`: Service quality score

### customer_data.csv
Required columns:
- `customer_id`: Unique customer identifier
- `clv_decile`: Customer lifetime value decile
- `churn_risk`: Churn risk indicator
- `current_bb_speed`: Current broadband speed
- `network_activity`: Network activity level
- `account_tenure`: Account tenure in months
- `time_of_last_broadband_upgrade`: Date of last upgrade
- `broadband_type`: Type of broadband connection
- `customer_segment`: Customer segment classification

## Key Definitions

- **Active Device**: A device whose `last_alive_date` is within the specified threshold (default: 30 days)
- **Inactive Device**: A device whose `last_alive_date` is beyond the specified threshold
- **Frontier Device**: Device with ISP = "Frontier Communications"
- **Target Group**: Frontier devices that are Active (primary focus of analysis)

## Customization

### Adjusting the Active Threshold
Use the slider in the sidebar to change the definition of "active" from 7 to 90 days.

### Adding New Tabs
To add functionality to Tab 2 or Tab 3, modify the corresponding `ui.nav_panel` sections in `app.py`.

## Troubleshooting

1. **Module not found error**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Data file not found**:
   - Verify the CSV files exist in `Data/Data Output/`
   - Check file paths are correct

3. **Port already in use**:
   ```bash
   shiny run app.py --port 8001
   ```

## Next Steps

- Implement customer analysis visualizations in Tab 2
- Add device detail tables and filters in Tab 3
- Add export functionality for filtered data
- Implement advanced filtering options

