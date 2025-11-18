# Quick Start Guide - Pure JavaScript UI Dashboard

## 🚀 Getting Started in 3 Steps

### Step 1: Verify Data Files

Make sure these CSV files exist in `Data/Data Output/`:
- ✅ `customer_data.csv`
- ✅ `device_data.csv`
- ✅ `nba_data.csv`

If `nba_data.csv` is missing:
```bash
python generate_nba_data.py
```

### Step 2: Start the Server

**Option A: Double-click the batch file (Easiest)**
```
run_ui_dashboard.bat
```

**Option B: Use Python command**
```bash
python server.py
```

### Step 3: View the Dashboard

The dashboard will automatically open in your browser at:
```
http://localhost:8000/index.html
```

## 📁 New Project Structure

```
Hackthon/
├── UI/                          # ✨ NEW: Frontend application
│   ├── index.html               # Main entry point
│   ├── css/
│   │   ├── styles.css           # Global styles
│   │   └── components.css       # Component styles
│   ├── js/
│   │   ├── app.js               # Main controller
│   │   ├── data-loader.js       # CSV data loading
│   │   ├── charts.js            # D3.js visualizations
│   │   ├── dashboard.js         # Device overview
│   │   └── nba.js               # Next Best Action
│   └── README.md                # UI documentation
├── Data/
│   └── Data Output/             # CSV data files
│       ├── customer_data.csv
│       ├── device_data.csv
│       └── nba_data.csv
├── server.py                    # ✨ UPDATED: Serves UI folder
└── run_ui_dashboard.bat         # ✨ NEW: Launch script
```

## 🎯 What Changed?

### ✅ Pure JavaScript Implementation
- No Python Shiny app needed for frontend
- All logic runs in the browser
- Modular JavaScript architecture
- Clean separation of concerns

### ✅ Modular Structure
- **data-loader.js**: Handles all CSV loading
- **charts.js**: D3.js visualization functions
- **dashboard.js**: Device overview logic
- **nba.js**: Next Best Action features
- **app.js**: Main application controller

### ✅ Modern Design
- Clean, organized folder structure
- Separate CSS files for maintainability
- ES6+ JavaScript features
- Responsive design

## 📊 Dashboard Features

### Tab 1: Device Overview
- Interactive threshold slider (7-90 days)
- Real-time statistics cards
- Tree visualization of device hierarchy
- D3.js pie charts (Frontier vs Non-Frontier)
- Target group highlighting

### Tab 2: Customer Analysis
- Coming soon (placeholder ready)

### Tab 3: Device Details
- Coming soon (placeholder ready)

### Tab 4: Next Best Action
- Action filter dropdown
- Customer ID search
- Interactive bar chart
- Color-coded recommendations table
- CSV export functionality

## 🛠️ Troubleshooting

### Problem: Dashboard shows "Loading data..." forever

**Solution**: Verify data files exist
```bash
# Check if files exist
dir "Data\Data Output"

# Should see:
# customer_data.csv
# device_data.csv
# nba_data.csv
```

### Problem: Server won't start

**Solution 1**: Check if port is in use
```bash
# Kill existing server
# Press Ctrl+C in the terminal running the server
```

**Solution 2**: Change port in `server.py`
```python
PORT = 8001  # Change from 8000 to 8001
```

### Problem: Browser shows error

**Solution**: Hard refresh the page
- Windows: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

## 🔧 Development

### To modify styles:
Edit files in `UI/css/`:
- `styles.css` - Global layout and colors
- `components.css` - Cards, buttons, tables

### To modify functionality:
Edit files in `UI/js/`:
- `dashboard.js` - Device overview logic
- `nba.js` - Next Best Action features
- `charts.js` - Add new D3.js visualizations
- `data-loader.js` - Modify data loading
- `app.js` - Application initialization

### To add new tabs:
1. Add button in `index.html`:
   ```html
   <button class="tab" data-tab="newtab">New Tab</button>
   ```

2. Add content section:
   ```html
   <div id="newtab-content" class="tab-content">
       <!-- Your content here -->
   </div>
   ```

3. (Optional) Handle in `app.js` if needed

## 📝 Key Differences from Previous Version

| Feature | Old (Shiny) | New (Pure JS) |
|---------|-------------|---------------|
| Backend | Python Shiny | Python HTTP Server (file serving only) |
| Frontend | Shiny reactive UI | Pure JavaScript + D3.js |
| Updates | Server-side reactive | Client-side JavaScript |
| Structure | Single file | Modular architecture |
| Deployment | Python dependencies | Just Python (built-in server) |
| Customization | Limited | Full control over HTML/CSS/JS |

## 🎨 Customization Examples

### Change color scheme:
```css
/* Edit UI/css/styles.css */
body {
    background: linear-gradient(135deg, #your-color1, #your-color2);
}
```

### Change active threshold default:
```javascript
// Edit UI/js/dashboard.js
activeThreshold: 45, // Change from 30 to 45
```

### Modify NBA action colors:
```javascript
// Edit UI/js/nba.js in updateDistributionChart()
const colorMap = {
    'Ship new device': '#your-color',
    // ... other colors
};
```

## 📦 No Additional Dependencies

Unlike the Shiny version, you don't need to install any Python packages. Just:
1. Python 3.x (already on your system)
2. Modern web browser
3. The CSV data files

That's it! The dashboard runs entirely in the browser.

## 🚪 Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

## 📚 Additional Resources

- **UI Documentation**: See `UI/README.md` for detailed module documentation
- **Original Documentation**: Previous Shiny app docs still available
- **Data Generation**: Use existing data generation scripts

## ✨ Benefits of New Structure

1. **Faster Loading**: No Python backend processing
2. **Easier Deployment**: Just static files + simple server
3. **Better Performance**: D3.js runs natively in browser
4. **More Flexible**: Full control over every aspect
5. **Cleaner Code**: Modular, maintainable structure
6. **No Dependencies**: Works with just Python built-ins

---

**🎉 Enjoy your new pure JavaScript dashboard!**

Need help? Check the browser console (F12) for debugging information.

