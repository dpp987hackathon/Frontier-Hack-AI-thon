# Quick Reference - New Disposition Logic

## 🎯 Decision Rules (Check in Order)

### 🔴 1. Ship New Device
```
Device:   Eero 6 OR Eero 6+
Speed:    1Gig OR 2Gig
SQS:      1 (poor quality)
Churn:    1 (high risk)
Segment:  Aspirational Adopters
```
**Result**: 2 devices (0.0%)

---

### 🟢 2. Speed Upgrade + New Device
```
Device:     Eero 6 OR Eero 6+ OR Pro 6
Broadband:  Fiber
CLV:        7-10 (high value)
Segment:    Aspirational Adopters OR Peak Performers
```
**Result**: 15,727 devices (5.2%)

---

### 🔵 3. Speed Upgrade Only
```
Device:     Pro 6 OR Pro 6e
Broadband:  Fiber
CLV:        1-3 (lower value)
SQS:        3 (good quality)
```
**Result**: 0 devices (0.0%)

---

### ⚫ 4. Keep As Is (Default)
```
Criteria:  Doesn't match any of the above
```
**Result**: 284,271 devices (94.8%)

---

## 💰 Liability by Action

| Action | License Cost | Take Rate |
|--------|--------------|-----------|
| Ship new device | **$0** | 100% |
| Speed upgrade + new device | **$0 if accept**, $6 if reject | 5% |
| Speed upgrade only | **$6/device/year** | 3% |
| Keep as is | **$6/device/year** | 100% |

---

## 📊 Current Distribution

```
Total: 300,000 devices from 100,000 customers

Keep as is                  ████████████████████████ 94.8%
Speed upgrade + new device  █ 5.2%
Ship new device             ▏ 0.0%
Speed upgrade only          ▏ 0.0%
```

---

## 🔄 To Refresh Data

```bash
python generate_nba_data.py
```

Then refresh dashboard at: `http://localhost:8000/UI/`

