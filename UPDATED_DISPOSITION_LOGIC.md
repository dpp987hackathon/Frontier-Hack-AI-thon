# Updated Disposition Logic - Complete Reference

## Overview
The disposition logic has been updated to focus on **device model** as a primary criteria for determining customer actions. This document outlines the new business rules.

---

## Priority Order
Rules are evaluated in this priority order (first match wins):

1. **Ship new device** (Device Replacement - Highest Priority)
2. **Speed upgrade + new device** (High-Value Growth)
3. **Speed upgrade only** (Cost-Effective Enhancement)
4. **Keep as is** (Default for all others)

**Note**: "No action recommended" has been removed - all customers now fall into one of these four categories.

---

## 🔴 Rule 1: Ship New Device (Device Replacement)
**Priority**: HIGHEST (evaluated first)

### Criteria (ALL must be true):
```
✓ Device Model = "Eero 6" OR "Eero 6+"
✓ Current Speed = "1Gig" OR "2Gig"
✓ SQS Score = 1 (Poor service quality)
✓ Churn Risk = 1 (High risk of leaving)
✓ Customer Segment = "Aspirational Adopters"
```

### Business Logic:
```python
if (device_model in ['Eero 6', 'Eero 6+'] and
    current_bb_speed in ['1Gig', '2Gig'] and
    sqs_score == 1 and 
    churn_risk == 1 and 
    customer_segment == 'Aspirational Adopters'):
    return 'Ship new device'
```

### Rationale:
- **Target Devices**: Older Eero 6/6+ models with performance issues
- **High-Speed Customers**: Already paying for premium speeds (1Gig/2Gig)
- **At-Risk**: Poor service quality + high churn risk
- **High-Value Segment**: Aspirational Adopters worth retaining
- **Action**: Immediate device replacement to resolve service issues
- **Goal**: Prevent churn of valuable customers on premium plans

### Liability Impact:
- **License Cost**: $0 (new device shipped, no license fee)
- **Take Rate**: 100% (all eligible customers receive device)

### Example Scenarios:
✅ **Qualifies**: Eero 6, 1Gig, SQS=1, Churn=1, Aspirational Adopter
✅ **Qualifies**: Eero 6+, 2Gig, SQS=1, Churn=1, Aspirational Adopter
❌ **Doesn't Qualify**: Pro 6, 1Gig, SQS=1, Churn=1, Aspirational Adopter (wrong device)
❌ **Doesn't Qualify**: Eero 6, 500Mbps, SQS=1, Churn=1, Aspirational Adopter (speed too low)
❌ **Doesn't Qualify**: Eero 6, 1Gig, SQS=2, Churn=1, Aspirational Adopter (SQS not critical)

---

## 🟢 Rule 2: Speed Upgrade + New Device
**Priority**: HIGH (evaluated second)

### Criteria (ALL must be true):
```
✓ Device Model = "Eero 6" OR "Eero 6+" OR "Pro 6"
✓ Broadband Type = "Fiber"
✓ CLV Decile = 7-10 (High lifetime value)
✓ Customer Segment = "Aspirational Adopters" OR "Peak Performers"
```

### Business Logic:
```python
if (device_model in ['Eero 6', 'Eero 6+', 'Pro 6'] and
    broadband_type == 'Fiber' and 
    clv_decile >= 7 and clv_decile <= 10 and 
    customer_segment in ['Aspirational Adopters', 'Peak Performers']):
    return 'Speed upgrade + new device'
```

### Rationale:
- **Target Devices**: Customers with older device models that could benefit from upgrade
- **Fiber Infrastructure**: Fast network capable of higher speeds
- **High-Value Customers**: CLV 7-10 indicates strong revenue potential
- **Growth Segments**: Aspirational/Peak customers likely to adopt premium services
- **Action**: Upsell to higher speed tier + provide latest WiFi device
- **Goal**: Maximize ARPU from high-value customers, improve satisfaction

### Liability Impact:
- **License Cost**: 
  - **If customer accepts** (take rate %): $0 (gets new device)
  - **If customer rejects**: $6.00/device/year (keeps old device)
- **Take Rate**: Adjustable (default 5%)
- **All customer devices affected**: When customer upgrades broadband, ALL their devices get new hardware

### Example Scenarios:
✅ **Qualifies**: Eero 6, Fiber, CLV=8, Aspirational Adopter
✅ **Qualifies**: Pro 6, Fiber, CLV=10, Peak Performer
✅ **Qualifies**: Eero 6+, Fiber, CLV=7, Peak Performer
❌ **Doesn't Qualify**: Pro 6e, Fiber, CLV=9, Peak Performer (wrong device model)
❌ **Doesn't Qualify**: Eero 6, Copper, CLV=9, Peak Performer (not Fiber)
❌ **Doesn't Qualify**: Eero 6, Fiber, CLV=5, Peak Performer (CLV too low)
❌ **Doesn't Qualify**: Eero 6, Fiber, CLV=9, Budget Balancer (wrong segment)

---

## 🔵 Rule 3: Speed Upgrade Only
**Priority**: MEDIUM (evaluated third)

### Criteria (ALL must be true):
```
✓ Device Model = "Pro 6" OR "Pro 6e"
✓ Broadband Type = "Fiber"
✓ CLV Decile = 1-3 (Lower lifetime value)
✓ SQS Score = 3 (Good service quality)
```

### Business Logic:
```python
if (device_model in ['Pro 6', 'Pro 6e'] and
    broadband_type == 'Fiber' and 
    clv_decile >= 1 and clv_decile <= 3 and 
    sqs_score == 3):
    return 'Speed upgrade only'
```

### Rationale:
- **Target Devices**: Customers with Pro devices (newer models that work well)
- **Good Service Quality**: SQS=3 indicates device is performing adequately
- **Lower CLV**: Don't justify cost of new device hardware
- **Fiber Infrastructure**: Can support higher speeds
- **Action**: Offer speed tier upgrade only (no new device needed)
- **Goal**: Cost-effective revenue increase without hardware investment

### Liability Impact:
- **License Cost**: $6.00/device/year for ALL devices
  - **If customer accepts** (take rate %): Still need licenses (keeps old device)
  - **If customer rejects**: Still need licenses
- **Take Rate**: Adjustable (default 3%)
- **All customer devices affected**: When customer upgrades broadband speed, ALL their devices get the upgrade

### Why License Cost Applies:
Even if customer accepts the speed upgrade, they keep their existing Pro 6/6e devices (which are performing well), so all devices still require license renewals.

### Example Scenarios:
✅ **Qualifies**: Pro 6, Fiber, CLV=2, SQS=3
✅ **Qualifies**: Pro 6e, Fiber, CLV=1, SQS=3
❌ **Doesn't Qualify**: Eero 6, Fiber, CLV=2, SQS=3 (wrong device model)
❌ **Doesn't Qualify**: Pro 6, Copper, CLV=2, SQS=3 (not Fiber)
❌ **Doesn't Qualify**: Pro 6, Fiber, CLV=5, SQS=3 (CLV too high)
❌ **Doesn't Qualify**: Pro 6, Fiber, CLV=2, SQS=2 (SQS not good enough)

---

## ⚫ Rule 4: Keep As Is
**Priority**: DEFAULT (evaluated last)

### Criteria:
```
✗ Does not match any of the above rules
```

### Business Logic:
```python
# Default catch-all
return 'Keep as is'
```

### Rationale:
- **Customer Profile**: All customers who don't fit the specific upgrade criteria
- **Action**: Maintain current service level
- **Examples**:
  - Customers with Pro 6e devices and CLV 4-10 (good devices, various value tiers)
  - Copper customers (infrastructure doesn't support speed upgrades)
  - Customers with poor service but not meeting all ship criteria
  - Customers with low SQS but not at-risk (no churn signal)
  
### Liability Impact:
- **License Cost**: $6.00/device/year for ALL devices
- **Take Rate**: 100% (all remain in current state)
- **No changes**: Devices remain as-is, licenses required

### Example Scenarios:
Examples of customers who fall into this category:
- Pro 6e, Fiber, CLV=8, SQS=3 (good device, high value, but SQS=3 with CLV>3 doesn't match Rule 3)
- Eero 6, Copper, CLV=8, Aspirational Adopter (wrong broadband type)
- Pro 6, Fiber, CLV=2, SQS=2 (device model matches Rule 3 but SQS isn't 3)
- Any customer on Copper network (no Fiber)
- Customers with newer models not in the upgrade device lists

---

## Key Changes from Previous Logic

### 1. **Device Model is Now Primary Criteria**
**Previous**: Focused primarily on customer attributes (segment, CLV, SQS)
**New**: Device model is checked first for each rule

### 2. **Speed Criteria for Device Replacement**
**Previous**: No speed requirement for device replacement
**New**: Must have 1Gig or 2Gig to qualify for device replacement

**Rationale**: Focus device replacement on customers already paying for premium speeds

### 3. **Different Device Sets per Action**
- **Ship new device**: Only Eero 6, Eero 6+ (older models needing replacement)
- **Speed + Device upgrade**: Eero 6, Eero 6+, Pro 6 (ready for premium service)
- **Speed only**: Pro 6, Pro 6e (newer devices that work well)

### 4. **Removed "No Action Recommended"**
**Previous**: Had a separate category for customers not matching any rules
**New**: All non-matching customers go to "Keep as is"

**Rationale**: Simplifies segmentation and recognizes that all customers require some level of service management (even if it's maintaining status quo)

### 5. **Segment Requirements More Focused**
- **Device Replacement**: Only Aspirational Adopters (narrower focus)
- **Speed + Device**: Aspirational Adopters OR Peak Performers (high-value segments)
- **Speed only**: No segment requirement (broadens eligibility)
- **Keep as is**: Any segment (catch-all)

---

## Device Model Reference

### Eero 6 / Eero 6+
- **Generation**: Older models
- **Performance**: Mid-range, may struggle with newer high-speed plans
- **Target for**: Replacement or upgrade with new device
- **Found in Rules**: Ship new device, Speed upgrade + new device

### Pro 6
- **Generation**: Mid-tier professional model
- **Performance**: Good performance, can handle most speeds
- **Target for**: Speed upgrade opportunities (with or without device)
- **Found in Rules**: Speed upgrade + new device, Speed upgrade only

### Pro 6e
- **Generation**: Newer professional model
- **Performance**: Excellent performance with WiFi 6e support
- **Target for**: Speed-only upgrades (device is already good)
- **Found in Rules**: Speed upgrade only

---

## Decision Tree

```
START - Check Customer/Device
  │
  ├─► Has Eero 6/6+ AND 1Gig/2Gig AND SQS=1 AND Churn=1 AND Aspirational?
  │   ├─ YES → Ship new device (100% take rate, $0 license)
  │   └─ NO → Continue
  │
  ├─► Has Eero 6/6+/Pro 6 AND Fiber AND CLV=7-10 AND (Aspirational OR Peak)?
  │   ├─ YES → Speed upgrade + new device (adjustable take rate)
  │   │         • Accepts: $0 license (gets new device)
  │   │         • Rejects: $6/device/year license
  │   └─ NO → Continue
  │
  ├─► Has Pro 6/Pro 6e AND Fiber AND CLV=1-3 AND SQS=3?
  │   ├─ YES → Speed upgrade only (adjustable take rate)
  │   │         • All devices: $6/device/year (keeps devices)
  │   └─ NO → Continue
  │
  └─► Keep as is (100%, $6/device/year)
      • Any customer not matching above rules
```

---

## Liability Summary Table

| Disposition | Device Models | License Cost | Take Rate | Notes |
|-------------|---------------|--------------|-----------|-------|
| **Ship new device** | Eero 6, Eero 6+ | $0/device | 100% | Must also have 1Gig/2Gig speed |
| **Speed upgrade + new device** | Eero 6, Eero 6+, Pro 6 | $0 if accept, $6 if reject | Adjustable (5%) | Must be on Fiber, CLV 7-10 |
| **Speed upgrade only** | Pro 6, Pro 6e | $6/device/year | Adjustable (3%) | Must be on Fiber, CLV 1-3, SQS=3 |
| **Keep as is** | Any model | $6/device/year | 100% | Default for all non-matches |

---

## Regenerating Data

After updating the logic, you need to regenerate the NBA data:

```bash
python generate_nba_data.py
```

This will:
1. Load customer and device data
2. Apply the new business rules
3. Generate updated `Data/Data Output/nba_data.csv`
4. Show distribution statistics

Then refresh the dashboard to see the new classifications.

---

## Testing the New Logic

### Test Case 1: Device Replacement
**Customer Profile**:
- Device: Eero 6
- Speed: 2Gig
- SQS: 1
- Churn: 1
- Segment: Aspirational Adopters

**Expected Result**: ✅ Ship new device

### Test Case 2: High-Value Upgrade
**Customer Profile**:
- Device: Pro 6
- Broadband: Fiber
- CLV: 9
- Segment: Peak Performers

**Expected Result**: ✅ Speed upgrade + new device

### Test Case 3: Cost-Effective Upgrade
**Customer Profile**:
- Device: Pro 6e
- Broadband: Fiber
- CLV: 2
- SQS: 3

**Expected Result**: ✅ Speed upgrade only

### Test Case 4: No Match
**Customer Profile**:
- Device: Pro 6e
- Broadband: Copper
- CLV: 5
- SQS: 2

**Expected Result**: ✅ Keep as is (doesn't match any upgrade criteria)

---

## Business Impact

### Expected Distribution Changes

**Previous Logic** (broader criteria):
- Ship new device: ~3-5% of customers
- Speed upgrade + new device: ~15-20%
- Speed upgrade only: ~10-15%
- Keep as is: ~30-40%
- No action recommended: ~20-30%

**New Logic** (device-focused criteria):
- Ship new device: ~1-3% (more targeted)
- Speed upgrade + new device: ~10-15% (similar, but device-filtered)
- Speed upgrade only: ~8-12% (Pro devices only)
- Keep as is: ~70-80% (includes all non-matches)

### Benefits of New Approach

1. ✅ **Device-Driven**: Targets customers with specific hardware that benefits from upgrades
2. ✅ **Speed-Qualified**: Device replacement focuses on premium-speed customers
3. ✅ **Cost Optimization**: Speed-only upgrades limited to customers with good devices
4. ✅ **Simpler Segmentation**: Four clear categories instead of five
5. ✅ **Better ROI**: More targeted recommendations based on actual device capabilities

---

## Key Insights

### 1. **Device Model Matters**
- Different devices have different upgrade paths
- Older Eero 6/6+ models are candidates for replacement or upgrade
- Newer Pro 6/6e models primarily get speed-only upgrades

### 2. **Speed Tiers Indicate Value**
- Device replacement requires 1Gig/2Gig (premium customers)
- Focus hardware investment on customers already paying for high speeds

### 3. **Infrastructure Dependency**
- Speed upgrades require Fiber infrastructure
- Copper customers automatically go to "Keep as is"

### 4. **Segmentation Precision**
- Device replacement: Very targeted (only Aspirational + specific criteria)
- Speed upgrades: Broader, but still filtered by device model
- Keep as is: Default for everyone else

### 5. **Liability Management**
- Most customers now in "Keep as is" = higher baseline liability
- But upgrades are more targeted = better conversion rates expected
- Focus is on quality over quantity of upgrade recommendations

---

This updated logic provides more precise, device-centric recommendations while simplifying the overall segmentation structure.

