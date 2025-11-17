# 🚀 Quick Start: Next Best Action Dashboard

## Launch in 2 Steps!

### Step 1: Generate the Data (First Time Only)
```bash
python generate_nba_data.py
```

### Step 2: Launch the Dashboard
Double-click: **`run_d3_dashboard.bat`**

Or run manually:
```bash
python server.py
```

---

## ✅ That's It!

Your browser will automatically open to: **http://localhost:8000/index.html**

Click the **"Next Best Action"** tab to see your customer recommendations!

---

## 📊 What You'll See

- **300,000 customer recommendations** based on intelligent business rules
- **Interactive bar chart** showing action distribution
- **Searchable table** with customer details
- **Filter dropdown** to focus on specific actions

---

## 🎯 Quick Tips

1. **Filter by Action**: Use the dropdown to see specific recommendation types
2. **Search Customers**: Type Customer ID in the search box
3. **Export Data**: Table shows first 100 results - filter to get specific lists
4. **Color Codes**:
   - 🔴 Red = Urgent (ship device)
   - 🟢 Green = High value (upgrade + device)
   - 🔵 Blue = Medium value (upgrade only)
   - ⚫ Gray = Stable (keep as is)
   - 🟡 Yellow = Review needed

---

## 🛑 Stop the Server

Press **Ctrl+C** in the terminal window

---

**Need Help?** See `NBA_IMPLEMENTATION_SUMMARY.md` for complete documentation

