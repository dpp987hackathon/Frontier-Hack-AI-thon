# Quick Test Guide - Liability Simulation

## What Was Fixed?

The liability simulation now correctly calculates license costs based on these rules:

| Action Type | License Fee? | Why? | Take Rate |
|-------------|--------------|------|-----------|
| **Ship new device** | ❌ NO | Customer gets new device | 100% (all shipped) |
| **Speed upgrade only** | ✅ YES | Customer keeps device, license renewed | Adjustable slider |
| **Speed upgrade + new device** | ❌ NO | Customer gets new device | Adjustable slider |
| **Keep as is** | ✅ YES | Device maintained, license required | 100% (all count) |
| **No action recommended** | ✅ YES | No action, license required | 100% (all count) |

### Important: Customer-Level Impact
- When a customer upgrades their broadband plan, **ALL their devices** are upgraded
- The simulation now groups devices by customer to accurately reflect this

## How to Test

1. **Start the Dashboard**
   ```bash
   run_ui_dashboard.bat
   ```
   - Opens in browser at http://localhost:8000

2. **Navigate to Detailed View Tab**
   - Click the "Detailed View" tab at the top

3. **Scroll to Simulation Section**
   - Look for "📊 Action Simulation & ROI Analysis"

4. **Test Scenario 1: Quarterly License Cost**
   - Keep "Quarterly" selected ($1.50 per device)
   - Set "Speed Upgrade Only" to 10%
   - Set "Speed + Device Upgrade" to 15%
   - Click "▶️ Run Simulation"
   - **Expected**: 
     - "Ship new device" shows $0 license cost
     - "Speed upgrade + new device" shows $0 license cost
     - "Speed upgrade only" shows license costs (for devices kept)
     - "Keep as is" and "No action" show full license costs

5. **Test Scenario 2: Yearly License Cost**
   - Select "Yearly" ($6.00 per device)
   - Keep other settings the same
   - Click "▶️ Run Simulation"
   - **Expected**: All license costs are 4x higher (yearly vs quarterly)

6. **Test Scenario 3: High Take Rates**
   - Set "Speed Upgrade Only" to 50%
   - Set "Speed + Device Upgrade" to 50%
   - Click "▶️ Run Simulation"
   - **Expected**: Lower total liability (more customers upgrade = fewer licenses needed)

7. **Test Scenario 4: No Take Rates**
   - Set both take rates to 0%
   - Click "▶️ Run Simulation"
   - **Expected**: Maximum liability (no one upgrades = all devices need licenses)

## What to Check

### Main KPI Card (Big Red Card)
- ✅ Shows "Estimated Total Liability"
- ✅ Shows "Per Quarter" or "Per Year" based on selection
- ✅ Shows device count requiring licenses
- ✅ Amount changes when you toggle quarterly/yearly

### Supporting Metric Cards
- ✅ **Expected Conversions**: Number of customers accepting upgrades
- ✅ **Total Devices**: Number of devices requiring licenses
- ✅ **License Cost**: Shows $1.50 or $6.00 based on selection
- ✅ **Avg Cost/Device**: Average license cost per device

### Breakdown Table
- ✅ Each action type has a row
- ✅ "Ship new device" shows $0.00 per device
- ✅ "Speed upgrade + new device" shows $0.00 per device
- ✅ "Speed upgrade only" shows license cost
- ✅ "Keep as is" and "No action" show license cost
- ✅ Device counts are shown in parentheses
- ✅ Notes explain each action's impact

## Expected Results Example

For a typical dataset with quarterly licensing:

```
Action Type                    | Eligible | Take Rate | Conversions | License Cost    | Total Cost
-------------------------------|----------|-----------|-------------|-----------------|------------
Ship new device               | 150      | 100.0%    | 150         | $0.00 (450 dev) | $0
Speed upgrade only            | 500      | 3.0%      | 15          | $1.50 (45 dev)  | $67.50
Speed upgrade + new device    | 800      | 5.0%      | 40          | $0.00 (120 dev) | $0
Keep as is                    | 2,000    | 100.0%    | 2,000       | $1.50 (6k dev)  | $9,000
No action recommended         | 1,550    | 100.0%    | 1,550       | $1.50 (4.6k dev)| $6,900

TOTAL LIABILITY: ~$15,967.50 per quarter
```

## Troubleshooting

**Q: The simulation doesn't show results**
- A: Make sure you clicked "▶️ Run Simulation" button
- A: Check browser console for JavaScript errors (F12)

**Q: All actions show $0 license cost**
- A: Check that license period is selected (Quarterly or Yearly)
- A: Verify the data loaded correctly

**Q: Liability seems too high/low**
- A: Remember this is per quarter or per year (check the period)
- A: Check that take rates are set correctly
- A: Higher take rates = lower liability (more upgrades/new devices)

**Q: Device counts don't match customer counts**
- A: This is expected! Customers can have multiple devices
- A: The simulation groups by customer, then counts all their devices

## Key Insights from Simulation

1. **New Devices Eliminate Liability**: Shipping new devices or upgrading customers to new devices removes license costs
2. **Speed Upgrades Impact All Devices**: When a customer upgrades broadband, all their devices are affected
3. **Take Rates Matter**: Higher conversion rates on upgrades reduce overall liability
4. **Quarterly vs Yearly**: Yearly is 4x quarterly cost, but represents full year obligation
5. **Keep As Is = Highest Liability**: Customers with no action generate the most ongoing license costs

## Questions or Issues?

If you notice unexpected behavior:
1. Check the browser console (F12) for errors
2. Verify the data files loaded correctly
3. Try refreshing the page
4. Review the LIABILITY_SIMULATION_FIX.md for detailed technical information

