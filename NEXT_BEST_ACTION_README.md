# Next Best Action Feature

## Overview
The Next Best Action tab provides intelligent customer disposition recommendations based on business rules analyzing customer value, service quality, churn risk, and current service levels.

## Business Rules Implemented

### 1. **Ship new device** (Highest Priority - At-Risk Customers)
- **Criteria**: SQS Score = 1, Churn Risk = 1, Customer Segment = "Aspirational Adopters"
- **Rationale**: Immediate intervention needed for high-potential customers at risk of leaving
- **Action**: Ship replacement device to improve service quality and retain customer

### 2. **Speed upgrade + new device** (High-Value Growth)
- **Criteria**: 
  - Fiber customer
  - CLV Decile: 7-10 (high lifetime value)
  - Customer Segment: "Aspirational Adopters" OR "Peak Performers"
- **Rationale**: Upsell opportunity to maximize revenue from high-value customers
- **Action**: Offer speed tier upgrade with new WiFi device

### 3. **Speed upgrade only** (Low-Value Enhancement)
- **Criteria**:
  - Fiber customer
  - CLV Decile: 1-3 (lower lifetime value)
  - SQS Score = 3 (good service quality)
- **Rationale**: Cost-effective upsell without device investment
- **Action**: Offer speed tier upgrade only

### 4. **Keep as is** (Satisfied Stable Customers)
- **Criteria**:
  - SQS Score = 3 (excellent service quality)
  - Churn Risk = 0 (low churn risk)
  - Customer Segment: "Budget Balancers", "Foolproof Followers", OR "Settled Simplifiers"
- **Rationale**: Satisfied customers with stable usage patterns
- **Action**: No action needed - maintain current service

### 5. **No action recommended** (Default)
- Customers who don't fit any of the above criteria
- May require manual review or future rule development

## Features

### Dashboard Components

1. **Action Filter** (Sidebar)
   - Filter customers by specific action type
   - View summary statistics for all actions
   - See customer counts and percentages

2. **Distribution Chart**
   - Visual bar chart showing action distribution
   - Color-coded by priority:
     - 🔴 Red: Ship new device (urgent)
     - 🟢 Green: Speed upgrade + new device (high value)
     - 🔵 Blue: Speed upgrade only (medium value)
     - ⚫ Gray: Keep as is (no action)
     - 🟡 Yellow: No action recommended (review)

3. **Customer Details Table**
   - Sortable, searchable data grid
   - Key columns:
     - Customer ID
     - Next Best Action
     - Customer Segment
     - CLV Decile
     - Churn Risk
     - SQS Score
     - Broadband Type
     - Current Speed
     - Device Model
     - Device Status
     - ISP
   - Sorted by action priority (urgent first)

## How to Use

1. **Launch the Dashboard**
   ```bash
   python app.py
   ```
   Or use the batch file:
   ```bash
   run_app.bat
   ```

2. **Navigate to "Next Best Action" Tab**
   - Click on the "Next Best Action" tab in the navigation bar

3. **Filter Customers**
   - Use the dropdown in the sidebar to filter by specific action
   - View summary statistics in the sidebar

4. **Analyze Results**
   - Review the distribution chart to understand action breakdown
   - Export customer lists for targeted campaigns
   - Prioritize high-urgency actions (ship new device) first

## Data Requirements

The feature requires both customer and device data:

### Customer Data Fields
- `customer_id`
- `clv_decile` (1-10)
- `churn_risk` (0 or 1)
- `broadband_type` (Fiber/Copper)
- `customer_segment`
- `current_bb_speed`

### Device Data Fields
- `customer_id`
- `sqs_score` (0-3)
- `device_model`
- `device_status`
- `isp`

## Technical Details

### File Modified
- `app.py` - Added Next Best Action logic and UI components

### Key Functions
- `determine_next_best_action()` - Applies business rules to each customer
- `filtered_nba_data()` - Filters data based on user selection
- `nba_stats()` - Calculates summary statistics
- `nba_distribution_chart()` - Creates visualization
- `nba_table()` - Displays customer details

### Dependencies
All existing dependencies from `requirements.txt` are sufficient:
- shiny
- pandas
- matplotlib
- plotly

## Business Impact

### Expected Outcomes
1. **Reduced Churn**: Proactive device replacement for at-risk customers
2. **Increased ARPU**: Targeted upsell to high-value customers
3. **Cost Optimization**: Avoid unnecessary device shipments to satisfied customers
4. **Improved Efficiency**: Automated segmentation reduces manual analysis time

### Metrics to Track
- Conversion rate by action type
- Churn reduction for "Ship new device" segment
- ARPU increase from speed upgrades
- Customer satisfaction scores post-action

## Future Enhancements

Potential improvements:
- Add export functionality for customer lists
- Include estimated revenue impact per action
- Add time-based urgency indicators
- Integrate with CRM systems for automated campaigns
- Machine learning model to refine rules over time

## Support

For questions or issues with the Next Best Action feature, refer to:
- Main dashboard README: `SHINY_APP_README.md`
- Data generation guide: `data_generation_summary.md`

