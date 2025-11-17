# Device Analytics Dashboard - D3.js Version

## Overview

An interactive web-based dashboard built with D3.js for analyzing device data with focus on Frontier Communications devices and their activity status.

## Features

### 🎯 Tab 1: Device Overview
- **Interactive Statistics Cards**: Real-time metrics with color-coded highlights
  - Total devices count
  - **TARGET GROUP**: Frontier + Active devices (highlighted in green)
  - Frontier total devices
  - Non-Frontier total devices

- **Visual Tree Breakdown**: Hierarchical device distribution
  - Total devices → Frontier vs Non-Frontier ISP
  - Each ISP category splits into Active/Inactive status
  - Target group prominently highlighted

- **Interactive Threshold Control**: Slider to adjust "active" definition (7-90 days)

- **Beautiful Pie Charts**: Interactive D3.js visualizations
  - Frontier devices distribution (Active/Inactive)
  - Non-Frontier devices distribution (Active/Inactive)
  - Hover effects and animations
  - Percentage labels and legends

### 📊 Tab 2: Customer Analysis
- Placeholder for customer analytics (to be implemented)

### 📋 Tab 3: Device Details
- Placeholder for detailed device metrics (to be implemented)

### 🎯 Tab 4: Next Best Action
- **Smart Customer Recommendations**: AI-driven disposition recommendations based on business rules
  - Ship new device (urgent - at-risk customers)
  - Speed upgrade + new device (high-value growth opportunities)
  - Speed upgrade only (cost-effective enhancements)
  - Keep as is (satisfied stable customers)
  - No action recommended (customers needing review)

- **Action Filter Dropdown**: Filter customers by specific action type

- **Summary Statistics Cards**: Real-time metrics showing:
  - Total customers analyzed (300,000)
  - Filtered view count
  - Top 2 action distributions with percentages

- **Interactive Bar Chart**: D3.js visualization showing:
  - Action distribution across all customers
  - Color-coded by priority (red=urgent, green=high-value, etc.)
  - Percentage and count labels
  - Hover effects

- **Customer Details Table**: Searchable, filterable table with:
  - Customer ID search functionality
  - Next Best Action badges (color-coded)
  - Customer segment
  - CLV decile, churn risk, SQS score
  - Broadband type, speed, device model
  - First 100 results displayed for performance

- **CSV Download**: Export filtered data
  - Complete dataset with all filtered records
  - Includes all 13 data fields
  - Perfect for Excel analysis or CRM import
  - Filename includes filter type and timestamp
  - Example: `next_best_action_All_Actions_2025-11-17T15-30-45.csv`

## Quick Start

### Method 1: Using the Batch File (Easiest - Windows)

Simply **double-click** `run_d3_dashboard.bat` in your project folder!

The server will start and your browser will automatically open to the dashboard.

### Method 2: Using Python Command

```bash
python server.py
```

Then open your browser to: **http://localhost:8000/index.html**

### Method 3: Manual Python HTTP Server

```bash
# In the project directory
python -m http.server 8000

# Open browser to: http://localhost:8000/index.html
```

## Requirements

- **Python 3.x** (already installed on your system)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)
- No additional packages needed!

## Data Files

The dashboard loads data from:
- `Data/Data Output/customer_data.csv` - Customer information (100,000 records)
- `Data/Data Output/device_data.csv` - Device information (300,000 records)
- `Data/Data Output/nba_data.csv` - Next Best Action recommendations (300,000 records)

### Generating Next Best Action Data

Before running the dashboard with the Next Best Action tab, you must generate the NBA data:

```bash
python generate_nba_data.py
```

This script:
1. Loads customer and device data
2. Applies business rules to determine recommendations
3. Saves results to `nba_data.csv`

The NBA data will be automatically generated with the following distribution:
- Keep as is: ~46%
- Speed upgrade only: ~24%
- No action recommended: ~19%
- Speed upgrade + new device: ~10%
- Ship new device: <1%

These files must be present for the dashboard to work properly.

## Key Definitions

- **Active Device**: Device whose `last_alive_date` is within the threshold (default: 30 days)
- **Inactive Device**: Device whose `last_alive_date` is beyond the threshold
- **Frontier Device**: Device with ISP = "Frontier Communications"
- **Target Group**: 🎯 Frontier + Active devices (primary focus)

### Next Best Action Business Rules

The dashboard applies intelligent business rules to determine customer dispositions:

1. **Ship new device** (Priority 1 - Urgent)
   - SQS Score = 1 (poor service quality)
   - Churn Risk = 1 (high risk of leaving)
   - Customer Segment = "Aspirational Adopters"
   - **Action**: Immediate device replacement to retain high-value at-risk customer

2. **Speed upgrade + new device** (Priority 2 - High Value)
   - Broadband Type = Fiber
   - CLV Decile = 7-10 (high lifetime value)
   - Customer Segment = "Aspirational Adopters" OR "Peak Performers"
   - **Action**: Upsell premium speed tier with new device

3. **Speed upgrade only** (Priority 3 - Cost-Effective)
   - Broadband Type = Fiber
   - CLV Decile = 1-3 (lower lifetime value)
   - SQS Score = 3 (good service quality)
   - **Action**: Offer speed increase without device investment

4. **Keep as is** (Priority 4 - Stable)
   - SQS Score = 3 (excellent service quality)
   - Churn Risk = 0 (low risk)
   - Customer Segment = "Budget Balancers", "Foolproof Followers", or "Settled Simplifiers"
   - **Action**: No change needed - customer is satisfied

5. **No action recommended** (Default)
   - Customers not matching any specific rule
   - **Action**: Manual review or future rule development

## Features & Interactions

### Interactive Elements

1. **Threshold Slider**: 
   - Adjust the "active" definition from 7 to 90 days
   - Dashboard updates in real-time

2. **Pie Charts**:
   - Hover over slices for scale animation
   - Color-coded by status (green=active, red=inactive)
   - Shows percentages and counts

3. **Responsive Design**:
   - Works on desktop and tablet screens
   - Mobile-friendly layout

4. **Beautiful UI**:
   - Modern gradient design
   - Smooth animations and transitions
   - Professional color scheme

5. **Next Best Action Controls**:
   - **Action Filter**: Dropdown to filter by specific action type
   - **Customer Search**: Search by Customer ID in real-time
   - **Color-Coded Table**: Visual priority indicators
   - **Interactive Bar Chart**: Hover for animations
   - **Download Button**: 
     - 📥 CSV: Download complete filtered dataset

## Technology Stack

- **D3.js v7**: Data visualization library
- **HTML5/CSS3**: Modern web standards
- **Vanilla JavaScript**: No frameworks needed
- **Python HTTP Server**: Simple file serving

## Customization

### Changing Colors

Edit the CSS in `index.html`:
```css
/* Main gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Target card gradient */
background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
```

### Changing Port

Edit `server.py`:
```python
PORT = 8000  # Change to your preferred port
```

Or use command line:
```bash
python -m http.server 9000  # Use port 9000
```

### Adding New Visualizations

The dashboard is built with modular functions:
- `calculateStats()`: Computes device statistics
- `updateDashboard()`: Refreshes all visualizations
- `drawPieChart()`: Creates D3.js pie charts

Add new visualizations by creating similar functions and calling them in `updateDashboard()`.

## Troubleshooting

### Dashboard shows "Loading data..." forever

**Solution**: Make sure you're running the server (not just opening index.html directly)
```bash
python server.py
```

### "Error Loading Data" message

**Possible causes**:
1. CSV files not in correct location (`Data/Data Output/`)
2. CSV files have incorrect names
3. Server not running properly

**Solution**: 
- Verify files exist at the correct path
- Restart the server

### Port already in use

**Solution**: Use a different port
```bash
python -m http.server 8001
```
Then open: `http://localhost:8001/index.html`

### Browser shows old data

**Solution**: Hard refresh the page
- **Windows**: Ctrl + Shift + R
- **Mac**: Cmd + Shift + R

## Browser Compatibility

✅ Tested and working on:
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

## Performance

- **Fast loading**: Handles 100k+ device records smoothly
- **Real-time updates**: Instant response to threshold changes
- **Smooth animations**: 60 FPS transitions
- **Optimized rendering**: D3.js efficient data binding

## Future Enhancements

Planned features for Tabs 2 & 3:
- Customer segmentation analysis
- Device model breakdown
- Time-series trends
- Advanced filtering options
- Data export functionality
- Detailed data tables with sorting

## Architecture

```
project/
├── index.html              # Main dashboard (HTML/CSS/JS/D3)
├── server.py               # Python HTTP server
├── run_d3_dashboard.bat    # Windows launcher
├── generate_nba_data.py    # NBA data generator script
└── Data/
    └── Data Output/
        ├── customer_data.csv   # Customer records (100k)
        ├── device_data.csv     # Device records (300k)
        └── nba_data.csv        # Next Best Action data (300k)
```

## Stopping the Server

Press **Ctrl+C** in the terminal/command prompt where the server is running.

## License

This dashboard is part of your hackathon project. Use and modify as needed!

## Support

If you encounter issues:
1. Check that Python is installed: `python --version`
2. Verify CSV files are in the correct location
3. Try a different port if 8000 is busy
4. Check browser console for error messages (F12)

---

**Enjoy your beautiful D3.js dashboard! 📊✨**

