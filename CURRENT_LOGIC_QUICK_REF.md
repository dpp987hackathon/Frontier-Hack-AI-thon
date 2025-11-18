# Current Disposition Logic - Quick Reference

## 🎯 Simple Rules (Check in Priority Order)

### 🔴 1. Ship New Device
```
✓ Eero 6 OR Eero 6+
✓ 1Gig OR 2Gig
✓ SQS = 1
✓ Churn = 1
✓ Aspirational Adopters
```
**Result**: 2 devices (0.0%)

---

### 🟢 2. Speed Upgrade + New Device
```
✓ Eero 6 OR Eero 6+ OR Pro 6
✓ Fiber
✓ Aspirational Adopters OR Peak Performers
```
**Result**: 39,284 devices (13.1%)

---

### 🔵 3. Speed Upgrade Only
```
✓ Pro 6 OR Pro 6e
✓ Fiber
```
**Result**: 0 devices (0.0%)

---

### ⚫ 4. Keep As Is
```
✓ Everything else
```
**Result**: 260,714 devices (86.9%)

---

## 📊 Distribution Summary

```
Total: 300,000 devices (100,000 customers)

Keep as is                  ████████████████████ 86.9%
Speed upgrade + new device  ███ 13.1%
Ship new device             ▏ 0.0%
Speed upgrade only          ▏ 0.0%
```

---

## 💡 Key Points

- **13.1%** eligible for upgrades (up from 5.2%)
- **Device model** is primary criteria
- **No CLV or SQS** requirements for speed upgrades
- **Fiber required** for speed upgrades
- **Segment-based** for device upgrades

---

## 💰 Liability

| Action | License Cost | Take Rate |
|--------|--------------|-----------|
| Ship new device | $0 | 100% |
| Speed + device | $0 if accept, $6 if reject | 5% |
| Speed only | $6/device/year | 3% |
| Keep as is | $6/device/year | 100% |

