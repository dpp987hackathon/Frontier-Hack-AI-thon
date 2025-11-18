# Capability-Based Disposition Logic

## 🎯 Overview

The disposition logic is now based on **comparing customer's current speed to device capability**. This ensures customers get the right recommendation based on whether their device is a bottleneck, at capacity, or underutilized.

---

## 📱 Device Capabilities

| Device Model | Max Speed Supported |
|--------------|---------------------|
| Eero 6 | 1Gig |
| Eero 6+ | 1Gig |
| Pro 6 | 2Gig |
| Pro 6e | 5Gig |

---

## 🔄 Logic Rules (Evaluated in Order)

### 🔴 Rule 1: Ship New Device (Device Bottleneck)
**Condition**: `Current Speed > Device Max Capability`

**Example Scenarios**:
- Eero 6 (max 1Gig) with 2Gig speed → **Ship new device**
- Eero 6+ (max 1Gig) with 5Gig speed → **Ship new device**
- Pro 6 (max 2Gig) with 5Gig speed → **Ship new device**

**Rationale**: Customer is paying for faster speed than their device can deliver. Device is creating a bottleneck and must be upgraded.

**Liability**: $0 (new device, no license)
**Take Rate**: 100%

---

### 🟢 Rule 2: Speed Upgrade + New Device (Device at Max)
**Condition**: `Current Speed = Device Max Capability`

**Example Scenarios**:
- Eero 6 (max 1Gig) with 1Gig speed → **Speed upgrade + new device**
- Pro 6 (max 2Gig) with 2Gig speed → **Speed upgrade + new device**
- Pro 6e (max 5Gig) with 5Gig speed → **Speed upgrade + new device**

**Rationale**: Device is operating at maximum capacity. To upsell customer to higher speed, must also provide newer device that can handle it.

**Liability**: 
- If accepts: $0 (gets new device)
- If rejects: $6/device/year
**Take Rate**: Adjustable (default 5%)

---

### 🔵 Rule 3: Speed Upgrade Only (Device Underutilized)
**Condition**: `Current Speed < Device Max Capability`

**Example Scenarios**:
- Pro 6e (max 5Gig) with 1Gig speed → **Speed upgrade only**
- Pro 6 (max 2Gig) with 500Mbps speed → **Speed upgrade only**
- Eero 6 (max 1Gig) with 500Mbps speed → **Speed upgrade only**

**Rationale**: Device has capacity for higher speeds. Customer can be upgraded without needing new hardware.

**Liability**: $6/device/year (keeps existing device)
**Take Rate**: Adjustable (default 3%)

---

### ⚫ Rule 4: Keep As Is (Default)
**Condition**: Device not in known list or other edge cases

**Example Scenarios**:
- Devices not in our capability list
- Unknown device models
- Edge cases

**Rationale**: No action recommended for devices we don't track or manage.

**Liability**: $6/device/year
**Take Rate**: 100%

---

## 📊 Current Distribution

```
Dataset: 300,000 devices from 100,000 customers

Speed upgrade only          ███████████████ 43.3%
Keep as is                  ██████████████ 42.7%
Speed upgrade + new device  ████ 10.8%
Ship new device             █ 3.2%
```

### Breakdown:
- **Speed upgrade only**: 130,006 (43.3%) - Devices underutilized
- **Keep as is**: 128,161 (42.7%) - Unknown devices or edge cases
- **Speed upgrade + new device**: 32,382 (10.8%) - Devices at max capacity
- **Ship new device**: 9,451 (3.2%) - Devices creating bottlenecks

---

## 💡 Why This Approach Works

### 1. **Technical Accuracy**
- Based on actual device specifications
- Identifies real bottlenecks in customer experience
- Matches hardware capabilities to service levels

### 2. **Customer Experience Focus**
- **Bottleneck customers** (3.2%) get immediate relief with new device
- **At-capacity customers** (10.8%) can upgrade speed with new hardware
- **Underutilized customers** (43.3%) can get better value without new device

### 3. **Cost Optimization**
- Only ship devices when technically necessary
- Maximize speed-only upgrades where possible
- Target hardware investment to where it's needed

### 4. **Revenue Opportunity**
- **57.3% eligible for speed upgrades** (43.3% + 10.8% + 3.2%)
- Large addressable market for upsells
- Clear value proposition for each segment

---

## 📈 Detailed Examples

### Example 1: Bottleneck Customer
**Profile**:
- Device: Eero 6 (max 1Gig)
- Current Speed: 2Gig
- Status: Paying for 2Gig but only getting 1Gig performance

**Disposition**: **Ship new device**
**Why**: Device cannot support the speed customer is paying for. Immediate upgrade needed.
**Expected Outcome**: Customer satisfaction improves, gets full value of 2Gig plan

---

### Example 2: At Capacity Customer
**Profile**:
- Device: Pro 6 (max 2Gig)
- Current Speed: 2Gig
- Status: Device at maximum capacity

**Disposition**: **Speed upgrade + new device**
**Why**: To offer 5Gig upgrade, customer needs Pro 6e device.
**Expected Outcome**: Customer gets faster speed + better device, increases ARPU

---

### Example 3: Underutilized Customer
**Profile**:
- Device: Pro 6e (max 5Gig)
- Current Speed: 1Gig
- Status: Device can handle much faster speeds

**Disposition**: **Speed upgrade only**
**Why**: Existing device can handle 2Gig or 5Gig with no hardware change.
**Expected Outcome**: Cost-effective upsell, customer gets faster speed with existing device

---

### Example 4: Optimal Configuration
**Profile**:
- Device: Pro 6 (max 2Gig)
- Current Speed: 500Mbps
- Status: Device has capacity, but customer on appropriate plan

**Disposition**: **Speed upgrade only**
**Why**: Device can support faster speeds if customer wants upgrade.
**Expected Outcome**: Upsell opportunity available when customer ready

---

## 🔑 Business Logic Code

```python
# Device capabilities
device_capabilities = {
    'Eero 6': '1Gig',
    'Eero 6+': '1Gig',
    'Pro 6': '2Gig',
    'Pro 6e': '5Gig'
}

# Speed tier ordering
speed_order = {
    '50Mbps': 1,
    '100Mbps': 2,
    '200Mbps': 3,
    '500Mbps': 4,
    '1Gig': 5,
    '2Gig': 6,
    '5Gig': 7
}

# Get values for comparison
current_speed_value = speed_order[customer_speed]
device_max_value = speed_order[device_capabilities[device_model]]

# Apply rules
if current_speed_value > device_max_value:
    return 'Ship new device'  # Bottleneck!
elif current_speed_value == device_max_value:
    return 'Speed upgrade + new device'  # At max
elif current_speed_value < device_max_value:
    return 'Speed upgrade only'  # Underutilized
else:
    return 'Keep as is'  # Default
```

---

## 💰 Liability Impact

### By Disposition:

**Ship new device** (9,451 devices):
- License cost: $0 (all get new devices)
- Total: **$0**

**Speed upgrade + new device** (32,382 devices):
- 5% take rate → 1,619 accept (get new devices, $0 license)
- 95% reject → 30,763 keep old devices ($6/device)
- Total: **~$184,578/year**

**Speed upgrade only** (130,006 devices):
- All keep existing devices regardless of take rate
- Total: **$780,036/year**

**Keep as is** (128,161 devices):
- All maintain licenses
- Total: **$768,966/year**

### Grand Total Annual Liability: **~$1,733,580**

---

## 🎯 Marketing Implications

### 1. **Immediate Action Required** (3.2% - 9,451 devices)
**Message**: "Your device can't keep up with your speed. We're sending you a free upgrade!"
**Urgency**: High - customer experience is degraded
**Expected Response**: High satisfaction, retention

### 2. **Growth Opportunity** (10.8% - 32,382 devices)
**Message**: "Upgrade to 5Gig with our latest WiFi 6e device!"
**Urgency**: Medium - upsell opportunity
**Expected Response**: Moderate conversion with compelling offer

### 3. **Easy Upsell** (43.3% - 130,006 devices)
**Message**: "Your device can handle faster speeds - upgrade today!"
**Urgency**: Low - no hardware needed
**Expected Response**: Good conversion with right pricing

### 4. **Maintain** (42.7% - 128,161 devices)
**Message**: Monitor for future opportunities
**Urgency**: None currently
**Expected Response**: N/A

---

## ✅ Key Advantages

1. ✅ **Technically Sound** - Based on actual device specifications
2. ✅ **Customer-Centric** - Addresses real performance issues
3. ✅ **Clear Segmentation** - 57.3% have upgrade opportunities
4. ✅ **Cost Efficient** - 43.3% can upgrade without new hardware
5. ✅ **Revenue Generating** - Multiple upsell pathways
6. ✅ **Data-Driven** - Uses existing customer/device data
7. ✅ **Scalable** - Easy to add new device models
8. ✅ **Actionable** - Clear next steps for each segment

---

## 🔄 Adding New Devices

To add new device models, simply update the capabilities dictionary:

```python
device_capabilities = {
    'Eero 6': '1Gig',
    'Eero 6+': '1Gig',
    'Pro 6': '2Gig',
    'Pro 6e': '5Gig',
    'New Model': '10Gig'  # Add here
}
```

And ensure speed tiers are in the speed_order dictionary.

---

## 📝 Summary

The capability-based logic provides:
- **3.2%** need immediate device upgrades (bottlenecks)
- **10.8%** ready for speed + device upsell (at capacity)
- **43.3%** ready for speed-only upsell (underutilized)
- **42.7%** maintain current state

**Total addressable market for upgrades: 57.3%** of customer base!

This approach ensures customers get the right recommendation based on their actual technical needs, leading to better satisfaction and higher conversion rates. 🎯

