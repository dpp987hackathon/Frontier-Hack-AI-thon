# 📥 Download Feature - Quick Reference

## Overview
The Next Best Action dashboard now includes **CSV and PDF export capabilities** for filtered customer data!

---

## 🟢 CSV Download Button

### What It Does
- Exports **ALL** filtered records (no limit!)
- Creates a comma-separated values file
- Perfect for Excel, Google Sheets, or CRM imports

### Data Included (13 Fields)
1. Customer ID
2. Next Best Action
3. Customer Segment
4. CLV Decile (1-10)
5. Churn Risk (0 or 1)
6. SQS Score (0-3)
7. Broadband Type (Fiber/Copper)
8. Current Speed (500mb, 1Gig, 2Gig)
9. Network Activity (light, medium, heavy)
10. Account Tenure (months)
11. Device Model (Eero 6, Eero Pro, etc.)
12. Device Status (Provisioned, etc.)
13. ISP (Frontier/Not Frontier)

### Filename Format
```
next_best_action_[FILTER]_[TIMESTAMP].csv
```

**Examples:**
- `next_best_action_All_Actions_2025-11-17T15-30-45.csv`
- `next_best_action_Ship_new_device_2025-11-17T15-30-45.csv`
- `next_best_action_Keep_as_is_2025-11-17T15-30-45.csv`

### Use Cases
✅ Import into CRM systems  
✅ Bulk email campaign lists  
✅ Advanced analysis in Excel  
✅ Database imports  
✅ Archive complete datasets  

---

## 🔴 PDF Download Button

### What It Does
- Generates a **professional formatted report**
- Exports **first 1,000 records** (alerts if more exist)
- Includes summary statistics and branding

### Report Structure

#### Page 1 Header
- **Title**: "Next Best Action Report"
- **Timestamp**: When report was generated
- **Filter Applied**: Current filter selection
- **Record Count**: Total records (and how many shown)

#### Summary Statistics Section
Shows distribution of all actions:
- Keep as is: 138,841 (46.3%)
- Speed upgrade only: 72,953 (24.3%)
- No action recommended: 58,196 (19.4%)
- Speed upgrade + new device: 29,999 (10.0%)
- Ship new device: 11 (0.0%)

#### Data Table
**9 Columns:**
1. Customer ID
2. **Next Best Action** (color-coded!)
3. Customer Segment
4. CLV (centered)
5. Churn (centered)
6. SQS (centered)
7. Broadband Type
8. Current Speed
9. Device Model

**Formatting:**
- Landscape orientation for readability
- Striped rows (alternating gray/white)
- Color-coded action badges matching dashboard
- Professional fonts and spacing
- Page numbers on all pages

#### Color Coding in PDF
- 🔴 **Red**: Ship new device
- 🟢 **Green**: Speed upgrade + new device
- 🔵 **Blue**: Speed upgrade only
- ⚫ **Gray**: Keep as is
- 🟡 **Yellow**: No action recommended

### Filename Format
```
next_best_action_[FILTER]_[TIMESTAMP].pdf
```

**Examples:**
- `next_best_action_All_Actions_2025-11-17T15-30-45.pdf`
- `next_best_action_Ship_new_device_2025-11-17T15-30-45.pdf`

### Use Cases
✅ Executive presentations  
✅ Management reports  
✅ Client deliverables  
✅ Print-ready documents  
✅ Email attachments  
✅ Archive summaries  

### Performance Note
PDF limited to 1,000 records for performance reasons. Use CSV for complete datasets.

---

## 🚀 How to Use

### Step 1: Filter Your Data
1. Select action from dropdown (or leave as "All Actions")
2. Optionally search for specific Customer ID
3. Review filtered results in table

### Step 2: Choose Export Format

**For Complete Data → Use CSV**
```
Click: 📥 Download CSV
```
- Gets ALL filtered records
- No record limit
- Best for analysis or imports

**For Reports → Use PDF**
```
Click: 📄 Download PDF
```
- First 1,000 records
- Professional formatting
- Best for presentations

### Step 3: Save File
- File downloads automatically
- Timestamped filename prevents overwriting
- Opens in default application

---

## 💡 Pro Tips

### Tip 1: Filter Before Downloading
**Bad:** Download all 300k records → filter in Excel  
**Good:** Filter in dashboard → download targeted list

**Example Workflow:**
1. Select "Ship new device" in filter
2. Download CSV with just 11 urgent customers
3. Import directly into outreach campaign

### Tip 2: Use Both Formats
- **CSV for analysis**: Import into BI tools, CRM
- **PDF for sharing**: Send to managers, stakeholders

### Tip 3: Timestamp in Filename
Files include timestamp so you can:
- Track when data was exported
- Keep historical snapshots
- Compare changes over time

### Tip 4: PDF for Quick Overview
If you just need to see what's in a segment:
1. Apply filter
2. Download PDF
3. Review summary stats at top
4. Scan first page of records

### Tip 5: CSV for Large Exports
Exporting "Keep as is" (138k records)?
- **Don't use PDF** (limited to 1k)
- **Use CSV** (handles all records)

---

## 📊 Export Examples

### Example 1: Urgent Action List
**Goal:** Get list of customers needing immediate device replacement

**Steps:**
1. Filter: "Ship new device"
2. Click CSV download
3. Result: `next_best_action_Ship_new_device_2025-11-17T15-30-45.csv`
4. Contains: 11 customer records
5. Import into CRM for immediate outreach

### Example 2: Management Report
**Goal:** Show executive team recommendation breakdown

**Steps:**
1. Filter: "All Actions"
2. Click PDF download
3. Result: Professional report with:
   - Summary statistics
   - First 1,000 customer details
   - Color-coded actions
   - Multi-page formatted document
4. Email to leadership or present in meeting

### Example 3: Campaign List
**Goal:** Create targeted upsell campaign

**Steps:**
1. Filter: "Speed upgrade + new device"
2. Click CSV download
3. Result: 29,999 high-value customers
4. Import into marketing automation tool
5. Launch targeted email campaign

### Example 4: Weekly Archive
**Goal:** Keep historical snapshot of recommendations

**Steps:**
1. Every Monday, export "All Actions" as CSV
2. Filename includes date: `next_best_action_All_Actions_2025-11-24T09-00-00.csv`
3. Store in archive folder
4. Compare week-over-week changes

---

## 🔧 Technical Details

### CSV Format
- **Encoding**: UTF-8
- **Delimiter**: Comma (,)
- **Text Qualifier**: Quotes (") for fields with commas
- **Line Ending**: \n (Unix style)
- **File Size**: ~50KB per 1,000 records

### PDF Format
- **Library**: jsPDF v2.5.1
- **Table Plugin**: jsPDF-AutoTable v3.5.31
- **Orientation**: Landscape
- **Page Size**: Letter (8.5" × 11")
- **Font**: Helvetica
- **File Size**: ~100KB per 1,000 records

### Browser Support
✅ Chrome 90+  
✅ Firefox 88+  
✅ Edge 90+  
✅ Safari 14+  

### Performance
- **CSV**: Instant download (any size)
- **PDF**: 1-2 seconds for 1,000 records
- **Memory**: Minimal (client-side generation)

---

## ❓ Troubleshooting

### Issue: Download button not working
**Solution:** Make sure data is loaded (check if table shows records)

### Issue: Empty file downloaded
**Solution:** 
1. Check if filter returned any results
2. Try "All Actions" filter
3. Clear search box

### Issue: PDF shows fewer records than expected
**Solution:** PDF limited to 1,000 records for performance. Use CSV for complete export.

### Issue: CSV won't open in Excel
**Solution:**
1. Right-click file
2. Open With → Excel
3. Or import as CSV data in Excel

### Issue: Special characters look wrong in CSV
**Solution:** When opening in Excel:
1. Use "Import Data" feature
2. Select UTF-8 encoding
3. Don't double-click CSV file

### Issue: PDF formatting looks off
**Solution:**
1. Try opening in different PDF viewer
2. Adobe Acrobat recommended
3. Browser PDF viewers may vary

---

## 🎯 Best Practices

### For Data Analysis
1. Filter to relevant segment
2. Download CSV
3. Import into analysis tool
4. Create pivot tables or visualizations

### For Reporting
1. Review summary statistics in dashboard
2. Download PDF for visual presentation
3. Include in PowerPoint or meeting materials
4. Reference color coding in discussions

### For Campaign Execution
1. Filter to target segment
2. Download CSV
3. Validate data quality
4. Import into CRM/marketing tool
5. Track campaign results

### For Archiving
1. Export weekly/monthly snapshots
2. Store both CSV and PDF versions
3. Include metadata in filename
4. Keep in organized folder structure

---

## 📈 Use Case Scenarios

### Scenario 1: Sales Team Kickoff
**Situation:** Monthly sales meeting needs prioritized customer list

**Action:**
1. Filter: "Speed upgrade + new device"
2. Download PDF
3. Distribute to sales team
4. Review 29,999 high-value opportunities
5. Assign territories/quotas

### Scenario 2: Retention Campaign
**Situation:** Prevent churn from at-risk customers

**Action:**
1. Filter: "Ship new device"
2. Download CSV (11 customers)
3. Import into ticketing system
4. Create urgent support tickets
5. Track resolution

### Scenario 3: Executive Dashboard
**Situation:** C-level wants quarterly review

**Action:**
1. Filter: "All Actions"
2. Download PDF
3. Include in quarterly deck
4. Reference summary statistics
5. Show action distribution

### Scenario 4: Budget Planning
**Situation:** Need to estimate device shipment costs

**Action:**
1. Filter: "Ship new device" + "Speed upgrade + new device"
2. Download CSV
3. Calculate total devices needed
4. Estimate costs
5. Present budget proposal

---

## 🎉 Summary

The download feature provides **professional-grade data export** capabilities:

✅ **CSV**: Complete datasets for analysis  
✅ **PDF**: Beautiful reports for sharing  
✅ **Flexible**: Works with all filters  
✅ **Fast**: Client-side generation  
✅ **Professional**: Auto-formatted and timestamped  

**Download counts so far:** Check browser downloads folder!

---

**Ready to export?** Head to the Next Best Action tab and click those download buttons! 📥📄

