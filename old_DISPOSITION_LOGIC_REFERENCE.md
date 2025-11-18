# Customer/Device Disposition Logic - Complete Reference

## Overview
This document outlines the current business rules for assigning customers and their devices to each Next Best Action disposition.

## Priority Order
The rules are evaluated in this priority order (first match wins):

1. **Ship new device** (Highest Priority - At-Risk)
2. **Speed upgrade + new device** (High-Value Growth)
3. **Speed upgrade only** (Low-Value Enhancement)
4. **Keep as is** (Satisfied Stable)
5. **No action recommended** (Default/Fallback)

---

## 🔴 Rule 1: Ship New Device
**Priority**: HIGHEST (evaluated first)

### Criteria (ALL must be true):
```
✓ SQS Score = 1 (Poor service quality)
✓ Churn Risk = 1 (High risk of leaving)
✓ Customer Segment = "Aspirational Adopters"
```

### Business Logic:
```python
if (sqs_score == 1 and 
    churn_risk == 1 and 
    customer_segment == 'Aspirational Adopters'):
    return 'Ship new device'
```

### Rationale:
- **Customer Profile**: High-potential customers experiencing service issues
- **Risk**: Imminent churn without intervention
- **Action**: Immediate device replacement to improve service quality
- **Goal**: Retain valuable customers before they leave

### Liability Impact:
- **License Cost**: $0 (new device shipped, no license fee)
- **Take Rate**: 100% (all eligible customers receive device)

### Example Scenarios:
✅ **Qualifies**: Aspirational Adopter, SQS=1, Churn=1
❌ **Doesn't Qualify**: Peak Performer, SQS=1, Churn=1 (wrong segment)
❌ **Doesn't Qualify**: Aspirational Adopter, SQS=2, Churn=1 (SQS not low enough)

---

## 🟢 Rule 2: Speed Upgrade + New Device
**Priority**: HIGH (evaluated second)

### Criteria (ALL must be true):
```
✓ Broadband Type = "Fiber"
✓ CLV Decile = 7-10 (High lifetime value)
✓ Customer Segment = "Aspirational Adopters" OR "Peak Performers"
```

### Business Logic:
```python
if (broadband_type == 'Fiber' and 
    clv_decile >= 7 and clv_decile <= 10 and 
    customer_segment in ['Aspirational Adopters', 'Peak Performers']):
    return 'Speed upgrade + new device'
```

### Rationale:
- **Customer Profile**: High-value fiber customers with growth potential
- **Opportunity**: Maximize revenue from premium customers
- **Action**: Upsell to higher speed tier + provide new WiFi device
- **Goal**: Increase ARPU and improve customer experience

### Liability Impact:
- **License Cost**: 
  - **If customer accepts** (take rate %): $0 (gets new device)
  - **If customer rejects**: $6.00/device/year (keeps old device)
- **Take Rate**: Adjustable (default 5%)
- **All customer devices affected**: When customer upgrades broadband, ALL their devices get new hardware

### Example Scenarios:
✅ **Qualifies**: Fiber, CLV=8, Aspirational Adopter
✅ **Qualifies**: Fiber, CLV=10, Peak Performer
❌ **Doesn't Qualify**: Copper, CLV=9, Peak Performer (not Fiber)
❌ **Doesn't Qualify**: Fiber, CLV=5, Peak Performer (CLV too low)
❌ **Doesn't Qualify**: Fiber, CLV=9, Budget Balancer (wrong segment)

---

## 🔵 Rule 3: Speed Upgrade Only
**Priority**: MEDIUM (evaluated third)

### Criteria (ALL must be true):
```
✓ Broadband Type = "Fiber"
✓ CLV Decile = 1-3 (Lower lifetime value)
✓ SQS Score = 3 (Good service quality)
```

### Business Logic:
```python
if (broadband_type == 'Fiber' and 
    clv_decile >= 1 and clv_decile <= 3 and 
    sqs_score == 3):
    return 'Speed upgrade only'
```

### Rationale:
- **Customer Profile**: Lower-value fiber customers with good service
- **Opportunity**: Cost-effective upsell without device investment
- **Action**: Offer speed tier upgrade only (no new device)
- **Goal**: Increase revenue without hardware costs

### Liability Impact:
- **License Cost**: $6.00/device/year for ALL devices
  - **If customer accepts** (take rate %): Still need licenses (keeps old device)
  - **If customer rejects**: Still need licenses
- **Take Rate**: Adjustable (default 3%)
- **All customer devices affected**: When customer upgrades broadband speed, ALL their devices get the upgrade

### Why License Cost Applies:
Even if customer accepts the speed upgrade, they keep their existing devices, so all devices still require license renewals.

### Example Scenarios:
✅ **Qualifies**: Fiber, CLV=2, SQS=3
✅ **Qualifies**: Fiber, CLV=1, SQS=3
❌ **Doesn't Qualify**: Copper, CLV=2, SQS=3 (not Fiber)
❌ **Doesn't Qualify**: Fiber, CLV=5, SQS=3 (CLV too high)
❌ **Doesn't Qualify**: Fiber, CLV=2, SQS=2 (SQS not good enough)

---

## ⚫ Rule 4: Keep As Is
**Priority**: LOW (evaluated fourth)

### Criteria (ALL must be true):
```
✓ SQS Score = 3 (Excellent service quality)
✓ Churn Risk = 0 (Low churn risk)
✓ Customer Segment = "Budget Balancers" OR "Foolproof Followers" OR "Settled Simplifiers"
```

### Business Logic:
```python
if (sqs_score == 3 and 
    churn_risk == 0 and 
    customer_segment in ['Budget Balancers', 'Foolproof Followers', 'Settled Simplifiers']):
    return 'Keep as is'
```

### Rationale:
- **Customer Profile**: Satisfied, stable customers with good service
- **Risk**: Low - no action needed
- **Action**: Maintain current service level
- **Goal**: Cost efficiency - avoid unnecessary interventions

### Liability Impact:
- **License Cost**: $6.00/device/year for ALL devices
- **Take Rate**: 100% (all customers maintain current state)
- **No changes**: Devices remain as-is, licenses required

### Example Scenarios:
✅ **Qualifies**: Budget Balancer, SQS=3, Churn=0
✅ **Qualifies**: Foolproof Follower, SQS=3, Churn=0
✅ **Qualifies**: Settled Simplifier, SQS=3, Churn=0
❌ **Doesn't Qualify**: Budget Balancer, SQS=2, Churn=0 (SQS too low)
❌ **Doesn't Qualify**: Budget Balancer, SQS=3, Churn=1 (churn risk present)
❌ **Doesn't Qualify**: Aspirational Adopter, SQS=3, Churn=0 (wrong segment)

---

## 🟡 Rule 5: No Action Recommended
**Priority**: DEFAULT (evaluated last)

### Criteria:
```
✗ Does not match any of the above rules
```

### Business Logic:
```python
# Default catch-all
return 'No action recommended'
```

### Rationale:
- **Customer Profile**: Customers who don't fit defined patterns
- **Action**: No automated recommendation
- **Next Steps**: May require manual review or future rule development

### Liability Impact:
- **License Cost**: $6.00/device/year for ALL devices
- **Take Rate**: 100% (all remain in current state)
- **No changes**: Devices remain as-is, licenses required

### Example Scenarios:
Any customer that doesn't match Rules 1-4, such as:
- Copper customer, CLV=5, SQS=2, Churn=0
- Fiber customer, CLV=6, Peak Performer, SQS=2
- Any combination not explicitly covered above

---

## Field Definitions

### SQS Score (Service Quality Score)
- **0**: Critical issues
- **1**: Poor service quality
- **2**: Fair service quality
- **3**: Good/Excellent service quality

### CLV Decile (Customer Lifetime Value)
- **1-3**: Lower lifetime value
- **4-6**: Medium lifetime value
- **7-10**: High lifetime value

### Churn Risk
- **0**: Low risk of leaving
- **1**: High risk of leaving

### Broadband Type
- **Fiber**: Fiber optic connection
- **Copper**: Traditional copper line

### Customer Segments
1. **Aspirational Adopters**: Growth-oriented, early adopters
2. **Peak Performers**: High-value, high-usage customers
3. **Budget Balancers**: Cost-conscious, stable users
4. **Foolproof Followers**: Conservative, reliable customers
5. **Settled Simplifiers**: Simple needs, low-touch customers

---

## Decision Tree

```
START
  │
  ├─► Is SQS=1 AND Churn=1 AND Segment=Aspirational?
  │   ├─ YES → Ship new device (100% take rate, $0 license)
  │   └─ NO → Continue
  │
  ├─► Is Fiber AND CLV=7-10 AND (Aspirational OR Peak)?
  │   ├─ YES → Speed upgrade + new device (adjustable take rate)
  │   │         • Accepts: $0 license (gets new device)
  │   │         • Rejects: $6/device/year license
  │   └─ NO → Continue
  │
  ├─► Is Fiber AND CLV=1-3 AND SQS=3?
  │   ├─ YES → Speed upgrade only (adjustable take rate)
  │   │         • All devices: $6/device/year (keeps devices)
  │   └─ NO → Continue
  │
  ├─► Is SQS=3 AND Churn=0 AND (Budget OR Foolproof OR Settled)?
  │   ├─ YES → Keep as is (100%, $6/device/year)
  │   └─ NO → Continue
  │
  └─► No action recommended (100%, $6/device/year)
```

---

## Liability Summary Table

| Disposition | License Cost | Take Rate | Notes |
|-------------|--------------|-----------|-------|
| **Ship new device** | $0/device | 100% | New devices eliminate license cost |
| **Speed upgrade + new device** | $0 if accept, $6 if reject | Adjustable (default 5%) | Only non-converters need licenses |
| **Speed upgrade only** | $6/device/year | Adjustable (default 3%) | ALL devices need licenses (keeps old devices) |
| **Keep as is** | $6/device/year | 100% | Maintain current state |
| **No action recommended** | $6/device/year | 100% | No changes, licenses required |

---

## Key Insights

### 1. **Rule Priority Matters**
- Rules are evaluated in order
- First match wins
- "Ship new device" has highest priority because it addresses most urgent need

### 2. **Device Count vs Customer Count**
- Rules evaluate at **customer level** (1 recommendation per customer)
- Costs calculate at **device level** (multiple devices per customer)
- Formula: `Total Cost = (Customers × Avg Devices per Customer) × $6.00`

### 3. **Take Rates Only Apply to Upgrades**
- "Speed upgrade only" and "Speed upgrade + new device" have adjustable take rates
- Other dispositions assume 100% (ship all, keep all, or no action for all)

### 4. **License Cost Logic**
- **New device = No license**: Ship new device, Speed upgrade + new device (if accepted)
- **Keep device = License required**: All other cases

### 5. **Broadband Upgrade Impact**
- When customer upgrades broadband plan, **ALL their devices** are affected
- This applies to both "Speed upgrade only" and "Speed upgrade + new device"

---

## Data Source

**File**: `generate_nba_data.py`
**Function**: `determine_next_best_action(row)`
**Location**: Lines 9-43

The logic is applied to merged customer and device data to generate the `nba_data.csv` file used by the dashboard.

---

## Testing the Logic

To verify a customer's disposition:

1. Check customer attributes in order of priority
2. First rule that matches determines the disposition
3. Calculate license costs based on device counts and take rates

**Example Customer**:
- Fiber: Yes
- CLV: 8
- Segment: Peak Performer
- SQS: 2
- Churn: 0
- Devices: 3

**Evaluation**:
1. Ship new device? No (SQS ≠ 1, Churn ≠ 1)
2. **Speed upgrade + new device? YES** ✓ (Fiber, CLV=8, Peak Performer)
3. Result: "Speed upgrade + new device"

**License Calculation** (with 5% take rate):
- 5% accept → 3 devices get new hardware ($0 license)
- 95% reject → 3 devices need licenses (3 × $6.00 = $18/year)

