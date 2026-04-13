## 📋 OPTIMIZATION INPUTS - COMPLETE GUIDE

This document explains each input parameter in the IEMS Optimization Engine and what they mean.

---

## **Part 1: Basic Inputs**

### **1. Monthly Electricity Usage (kWh)**

**What is it?**
- Total electrical energy consumed per month in kilowatt-hours (kWh)
- This is the actual consumption from your electricity meter

**How to find it?**
- Check your electricity bill (labeled as "Units" or "kWh consumed")
- Typical Indian residential usage: 100-500 kWh/month
- Typical small business: 500-1500 kWh/month

**Examples:**
```
Urban apartment (AC + lights + appliances): 250-350 kWh
House with AC: 350-500 kWh
Small office: 600-1000 kWh
Retail shop: 800-1200 kWh
```

**Tiered Pricing Calculation:**
The system automatically calculates your monthly bill using Indian domestic tiered pricing:
```
0-50 kWh      @ ₹3.0/kWh   = ₹150 max
50-100 kWh    @ ₹4.5/kWh   = ₹225 max
100-200 kWh   @ ₹6.0/kWh   = ₹600 max
200-500 kWh   @ ₹8.0/kWh   = ₹2,400 max
500+ kWh      @ ₹12.0/kWh  = Variable

Example for 350 kWh:
50 × ₹3 + 50 × ₹4.5 + 100 × ₹6 + 150 × ₹8
= ₹150 + ₹225 + ₹600 + ₹1,200 = ₹2,175/month
```

**Impact on Sizing:**
```
100 kWh/month → ₹375/month → 2-4 kW solar needed
200 kWh/month → ₹1,050/month → 4-6 kW solar needed
350 kWh/month → ₹2,175/month → 6-9 kW solar needed
500 kWh/month → ₹3,375/month → 8-12 kW solar needed
```

**Input Example:**
```
Monthly electricity usage (kWh) [e.g., 300]: 350
```

The system will automatically display: **Calculated Monthly Bill (Tiered Pricing): ₹2,175.00**

---

### **2. Total Budget (₹)**

**What is it?**
- Maximum money you can spend on the entire solar + battery system
- Includes panels, batteries, inverter, wiring, installation

**Budget Breakdown (Typical):**
```
₹300,000 budget →
  Solar (₹200k) + Battery (₹100k)
  = 5 kW + 5 kWh system

₹500,000 budget →
  Solar (₹300k) + Battery (₹200k)
  = 7.5 kW + 8 kWh system

₹1,000,000 budget →
  Solar (₹600k) + Battery (₹400k)
  = 12 kW + 12 kWh system
```

**Cost References (₹):**
```
Solar Panels:
  400W panel: ₹16,000-18,000
  500W panel: ₹20,000-23,500
  Per Watt: ₹40-50

Batteries (Li-ion):
  2 kWh unit: ₹120,000
  5 kWh unit: ₹300,000
  10 kWh unit: ₹600,000
  Per kWh: ₹60,000-90,000

Inverter + Installation: ₹50,000-150,000
```

**Impact on Results:**
- Higher budget → Larger system → Lower grid dependency
- Lower budget → Smaller system → Higher grid dependency

**Input Example:**
```
Total budget (₹) [e.g., 500000]: 600000
```

---

### **3. Location/Region (Optional)**

**What is it?**
- Geographic location for your system
- Helps understand solar irradiance patterns
- India has different solar potential by region

**Typical Values:**
```
North India:  Delhi, Chandigarh, Punjab
             Solar: 4-5 kWh/m²/day

Central India: Mumbai, Pune, Indore
              Solar: 5-5.5 kWh/m²/day

South India:   Bangalore, Chennai, Hyderabad
              Solar: 5-6 kWh/m²/day (Best)

Coastal:      Goa, Kerala
             Solar: 4.5-5 kWh/m²/day
```

**Impact:**
- Better solar regions need smaller system size
- Worse solar regions need larger system size

**Input Example:**
```
Location/Region [optional, e.g., Mumbai]: Mumbai
```

(If you press Enter, it's optional)

---

### **4. Number of Days for Load Profile**

**What is it?**
- Duration for which synthetic load profile is generated
- Defines the time period for solar and load analysis
- Default: 30 days (recommended)

**How It Works:**
```
Monthly Bill (₹5,000 at ₹12/kWh) = 416.67 kWh

User inputs number of days:
  - 30 days → Simulates 416.67 kWh over 30 days
  - 60 days → Simulates 416.67 kWh over 60 days
  - 90 days → Simulates 416.67 kWh over 90 days

Usage:
  - For monthly analysis: Use 30 days (default)
  - For quarterly analysis: Use 90 days
  - For annual patterns: Use 365 days
```

**Valid Range:** 1 to 365 days

**Impact on Results:**
- Longer periods capture seasonal variations
- Shorter periods focus on near-term optimization
- Default 30 days balances speed and accuracy

**Input Example:**
```
Number of days for load profile [default: 30]: 30
(Press Enter for 30 days, or type: 60, 90, 180, etc.)
```

---

## **Part 2: Advanced Inputs**

### **5. Population Size**

**What is it?**
- Number of different solutions evaluated per generation
- Default: 30 (recommended)

**What It Means:**

```
Population = Number of candidate systems per "round"

Example with population=20:
Round 1: Tries 20 different configurations
Round 2: Tries 20 improved configurations
Round 3: Tries 20 more improved configurations
...
```

**Options:**

| Size | Time | Quality | Use Case |
|------|------|---------|----------|
| 10 | 20-30 sec | Fair | Quick results |
| 20 | 30-40 sec | Good | Standard (Recommended) |
| 30 | 40-50 sec | Better | **DEFAULT** |
| 50 | 60-80 sec | Excellent | When time permits |
| 100 | 2+ min | Best | Research/Analysis |

**Input Example:**
```
Population size [default: 30]: 
(Press Enter for 30, or type: 20, 50, 100, etc.)
```

---

### **6. Generations**

**What is it?**
- Number of evolutionary cycles
- More generations = more optimization rounds

**What It Means:**

```
Generation = One complete cycle of:
  - Evaluate all candidates
  - Select best ones
  - Create offspring (crossover)
  - Apply mutations
  - Form new population

Gen 1:   Initial (Fitness: ~40-50)
Gen 10:  Better (Fitness: ~60-65)
Gen 30:  Good (Fitness: ~75-78)
Gen 50:  Excellent (Fitness: ~78-80)
Gen 100: Maximum (Fitness: ~79-81)
```

**Options:**

| Generations | Time | Quality | Benefit |
|-------------|------|---------|---------|
| 20 | 20-30 sec | Fair | Quick prototype |
| 30 | 30-40 sec | Good | Fast results |
| 50 | 40-60 sec | Better | **RECOMMENDED** |
| 100 | 80-120 sec | Excellent | Best optimization |
| 150 | 2+ min | Maximum | Research |

**Input Example:**
```
Generations [default: 50]: 
(Press Enter for 50, or type: 30, 100, etc.)
```

---

### **7. Mutation Rate**

**What is it?**
- Probability of random changes in solutions
- Range: 0.01 to 0.5 (1% to 50%)
- Default: 0.1 (10%)

**What It Means:**

```
Mutation = Random change to a solution

10% Mutation:
  - 90% of time: No change
  - 10% of time: Randomly adjust solar/battery by ±2

This helps:
  ✓ Escape local optima
  ✓ Explore more options
  ✓ Avoid getting stuck
```

**Effect:**

| Rate | Effect | Use Case |
|------|--------|----------|
| 0.01 (1%) | Conservative - very little randomness | Tight constraints |
| 0.05 (5%) | Low - focused search | Standard |
| 0.10 (10%) | Medium - good balance | **RECOMMENDED** |
| 0.20 (20%) | High - more exploration | Complex problem |
| 0.50 (50%) | Very high - mostly random | Research |

**Input Example:**
```
Mutation rate [default: 0.1]: 
(Press Enter for 0.1, or type: 0.05, 0.2, etc.)
```

---

## **Part 3: Understanding the Output**

### **Key Metrics Explained**

**A. Solar Capacity (kW)**
```
What: Size of solar panel system
Example: 8.5 kW = 21 panels @ 400W each

Higher = More solar energy, less grid dependency
```

**B. Battery Capacity (kWh)**
```
What: Energy storage capacity
Example: 12 kWh = 4 battery units @ 3kWh each

Higher = More energy stored, more self-sufficiency at night
```

**C. Total System Cost (₹)**
```
What: Complete cost (panels + batteries + installation)
Example: ₹511,000

Must be ≤ Budget limit
```

**D. Grid Dependency (%)**
```
What: Percentage of energy from grid (lower is better)
Example: 22.5% grid dependency
         = 77.5% from solar + battery

Interpretation:
  <20%: Excellent (very independent)
  20-40%: Good (mostly self-sufficient)
  40-60%: Fair (balanced)
  >60%: Poor (still grid-dependent)
```

**E. Solar Utilization (%)**
```
What: Percentage of load directly powered by solar
Example: 68.3% solar utilization
         = 68.3% of daily energy from panels directly

Interpretation:
  50-70%: Typical (normal for Indian climate)
  <50%: Low (underutilized system)
  >70%: Excellent (good solar coverage)
```

**F. Estimated Savings (₹)**
```
What: Monthly money saved by avoiding grid purchases
Example: ₹15,120/month saved
         = ₹15,120 × 12 = ₹181,440/year

Calculation: (Grid energy) × (₹8/kWh)
```

**G. Fitness Score (0-100)**
```
What: Overall quality of the solution
Example: 78.45/100

Scale:
  0-50: Poor
  50-70: Fair
  70-85: Good
  85-100: Excellent

Combines:
  - Solar utilization (60% weight)
  - Grid reduction (40% weight)
  - Battery health bonus
```

---

## **Part 4: Input Quick Reference Table**

| Input | Example | Range | Impact |
|-------|---------|-------|--------|
| **Monthly Usage** | 350 kWh | 100-2000 | Determines system size |
| **Budget** | ₹600,000 | ₹200k-2M | Limits options |
| **Location** | Mumbai | Any place | Reference only |
| **Population** | 30 | 10-100 | Speed vs quality |
| **Generations** | 50 | 10-200 | Optimization depth |
| **Mutation Rate** | 0.1 | 0.01-0.5 | Exploration level |

---

## **Part 5: Recommended Input Combinations**

### **Scenario 1: Quick Result (1 minute)**
```
Monthly usage: 350 kWh
Budget: ₹600,000
Population: 20
Generations: 30
Mutation rate: 0.1
```
Result: Fast, reasonable solution

### **Scenario 2: Balanced (2 minutes)**
```
Monthly usage: 350 kWh
Budget: ₹600,000
Population: 30
Generations: 50
Mutation rate: 0.1
```
Result: Good balance of speed & quality ✓ RECOMMENDED

### **Scenario 3: Best Result (3+ minutes)**
```
Monthly usage: 350 kWh
Budget: ₹600,000
Population: 50
Generations: 100
Mutation rate: 0.1
```
Result: Excellent optimization, very thorough

### **Scenario 4: Tight Budget (1-2 minutes)**
```
Monthly usage: 350 kWh
Budget: ₹300,000
Population: 20
Generations: 50
Mutation rate: 0.15 (higher for better search)
```
Result: More exploration for limited options

---

## **Part 6: Troubleshooting Input Issues**

**Problem: "No valid solutions found within budget"**

**Causes:**
- Budget too low for given usage
- Design space too limited

**Solution:**
- Increase budget by 20-30%
- Or reduce monthly usage estimate
- Minimum budget: ₹250k for 200 kWh/month
                 ₹400k for 350 kWh/month
                 ₹700k for 500 kWh/month

**Problem: "Grid dependency is still 80%+"**

**Causes:**
- Budget constraints system too small
- Monthly usage is high

**Solution:**
- Increase budget for larger system
- Consider reducing consumption first
- Or accept the limitation

**Problem: "Fitness score is very low (<30)"**

**Causes:**
- System severely undersized (tight budget)
- Load data might be unrealistic

**Solution:**
- Run simulation with more budget
- Verify monthly usage is correct
- Check load data in outputs/cleaned_hourly.csv

---

## **Part 7: Input Validation Rules**

| Input | Min | Max | Type | Required |
|-------|-----|-----|------|----------|
| Monthly Usage | 50 | 2000 | Float | ✓ YES |
| Budget | 100,000 | 10,000,000 | Float | ✓ YES |
| Location | - | - | String | ✗ No |
| Population | 10 | 100 | Integer | ✗ No (def: 30) |
| Generations | 10 | 200 | Integer | ✗ No (def: 50) |
| Mutation Rate | 0.01 | 0.5 | Float | ✗ No (def: 0.1) |

---

## **Summary**

✓ Always enter: **Monthly usage** + **Budget**  
✓ Optional: **Location** (for reference)  
✓ Advanced: Population, Generations, Mutation (press Enter for defaults)  

**For best results:**
- Use realistic monthly usage (check electricity bill)
- Budget should be 30-40% of annual savings target
- Start with defaults, tune if needed

---

**Created:** April 2024  
**Version:** 1.0
