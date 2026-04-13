## 🚀 QUICK START GUIDE - IEMS Optimization Engine

**Time to first result: ~2 minutes**

---

## ⚡ 30-Second Setup

### Prerequisites
Ensure these files exist:
- ✅ `Datasets/solar_panel_dataset.csv` (solar component data)
- ✅ `Datasets/battery_dataset.csv` (battery component data)

Note: Synthetic load and solar data are **auto-generated** from your inputs

### Run Command
```bash
# From project root directory
python -m optimization.main
```

---

## 📝 Input Prompts

```
1. Monthly electricity usage (kWh)
   → Enter: 350 (check your bill for Units/kWh consumed)

2. 💡 System calculates: Monthly Bill (Tiered Pricing): ₹2,175.00
   (Shows cost with realistic slab rates, no input needed)

3. Total budget for solar system (₹)
   → Enter: 600000

4. Location
   → Type: bangalore (or mumbai, delhi, etc.)

5. Number of days for load profile [default: 30]
   → Press Enter for 30 days (or type custom: 60, 90, etc.)

6. Advanced Options (press Enter for defaults)
   Population size → Press Enter
   Generations → Press Enter
   Mutation rate → Press Enter
```

**Flow:**
```
Monthly Usage: 350 kWh
    ↓ (Calculate tiered cost)
Monthly Bill: ₹2,175 (realistic slab pricing)
    ↓ (Generate 30 days synthetic load)
Synthetic hourly load profile (720 hours)
    ↓ (Fetch real solar data from NASA API)
Real irradiance data adjusted for your timezone
    ↓ (Run GA optimization)
Optimal system configuration
    ↓
Annual Savings: Exact amount based on real tariffs
```

---

## 🏆 Expected Output

```
====================================================================
OPTIMAL SYSTEM CONFIGURATION
====================================================================

Solar Capacity:       8.5 kW (21 panels)
Battery Capacity:     12.0 kWh (4 units)
Total System Cost:    ₹511,000
Budget Utilization:   85.2%

PERFORMANCE METRICS
==================
Grid Dependency:      22.5%
Solar Utilization:    68.3%
Monthly Savings:      ₹42,500
Battery SoC:          65.2%

FITNESS SCORE:        78.45/100
====================================================================
```

---

## 📊 Results File

**Location:** `results/latest_optimization_result.json`

**Contains:**
- Optimal solar size & battery capacity
- Component IDs & quantities
- Total cost & budget utilization
- Performance metrics (grid %, solar %, savings)
- Fitness score & optimization stats
- All user inputs & GA parameters
- Timestamp

---

## ⏱️ Typical Timeline

| Phase | Time |
|-------|------|
| Input prompts | 30 sec |
| Data loading | 5-10 sec |
| Design space generation | 2-3 sec |
| GA optimization (50 gen) | 30-40 sec |
| Results display & export | 5 sec |
| **Total** | **~2 minutes** |

---

## 💡 What Gets Optimized

**Objective:** Maximize savings + minimize grid dependency

**Constraints:**
- ✓ Budget limit (hard constraint)
- ✓ Solar range: 1-15 kW
- ✓ Battery range: 0-20 kWh
- ✓ Real Indian component data
- ✓ Market-aligned costs

---

## 🎛️ Tuning Parameters (Advanced)

### For Quick Results (30 seconds)
```
Population Size: 20 (default: 30)
Generations: 30 (default: 50)
Mutation Rate: 0.1 (default)
```

### For Best Results (1-2 minutes)
```
Population Size: 50 (default: 30)
Generations: 100 (default: 50)
Mutation Rate: 0.1 (default)
```

### For Large Budgets (comprehensive search)
```
Population Size: 60
Generations: 150
Mutation Rate: 0.08
```

---

## ✅ Validation Checklist

Before running:

```
□ cd to project root directory
□ outputs/cleaned_hourly.csv exists
□ Datasets/solar_panel_dataset.csv exists
□ Datasets/battery_dataset.csv exists
□ Python 3.7+ installed
□ Required packages: pandas, numpy
□ Have budget amount ready (₹)
□ Have monthly usage ready (kWh)
```

---

## 🔍 Interpreting Results

### key Metrics

**Grid Dependency: 22.5%**
- Only 22.5% of energy from grid
- 77.5% from solar + battery
- ✓ Good: <30% is target

**Solar Utilization: 68.3%**
- 68.3% of load directly from solar panels
- Rest from battery or grid
- ✓ Good: 50-70% is typical for India

**Estimated Savings: ₹42,500/month**
- Money saved by avoiding grid purchases
- Based on ₹8/kWh tariff
- Annual savings: ₹510,000

**Battery SoC: 65.2%**
- Average state of charge (0-100%)
- ✓ Good: 40-80% is healthy range
- <40%: Battery not well utilized
- >80%: System waste/curtailment

**Fitness Score: 78.45/100**
- Overall quality of solution
- ✓ 70+: Excellent optimization
- 50-70: Good configuration
- <50: Suboptimal

---

## 🚨 Troubleshooting

### "File not found" errors
```
✓ Ensure you're in project root directory
✓ Check outputs/ has cleaned_hourly.csv
✓ Check Datasets/ has both CSV files
✓ Run: ls outputs/ (or dir outputs\ on Windows)
```

### "No valid solutions found within budget"
```
✓ Increase budget amount
✓ Check component costs in CSV (may need update)
✓ Start with budget ≥ ₹350,000
```

### Slow execution
```
✓ Reduce population size (e.g., 20 instead of 30)
✓ Reduce generations (e.g., 30 instead of 50)
✓ Check if simulator data has many rows (>10k)
```

### Unexpected results
```
✓ Verify monthly usage input is realistic
✓ Check load data in outputs/cleaned_hourly.csv
✓ Verify weather data if using custom irradiance
✓ Run again with higher generations (100)
```

---

## 📈 Example Scenarios

### Scenario 1: Urban Apartment
```
Input:  Monthly usage = 300 kWh, Budget = ₹400,000
Output: 5.5 kW + 8 kWh system
Result: 35% grid dependency, ₹30k/month savings
Time:   ~105 seconds
```

### Scenario 2: House with AC
```
Input:  Monthly usage = 500 kWh, Budget = ₹700,000
Output: 10 kW + 12 kWh system
Result: 28% grid dependency, ₹50k/month savings
Time:   ~120 seconds
```

### Scenario 3: Small Office
```
Input:  Monthly usage = 800 kWh, Budget = ₹1,000,000
Output: 12.5 kW + 15 kWh system
Result: 22% grid dependency, ₹75k/month savings
Time:   ~130 seconds
```

---

## 📚 Learning More

1. **Understand how it works**
   - Read: `optimization/README.md`

2. **Install & run tests**
   - Check: `simulation_engine/simulator_test.py`

3. **Modify behavior**
   - Edit: `optimization/objective_functions.py` (fitness weights)
   - Edit: `optimization/design_space.py` (size ranges)

4. **Integrate into workflow**
   - Import: `from optimization import GeneticAlgorithmOptimizer`

---

## 🎓 Understanding the Algorithm

**Genetic Algorithm = "Evolution Simulation"**

```
Generation 0:    Random candidates (fitness = 45)
Generation 10:   Better individuals (fitness = 62)
Generation 25:   Good solutions (fitness = 74)
Generation 50:   Near-optimal (fitness = 78)

Key: Best survival, random mutations, crossbreeding
```

---

## 💾 Saving Results

Results are **automatically saved** to:
```
results/optimization_result_YYYYMMDD_HHMMSS.json
results/latest_optimization_result.json (latest run)
```

**JSON Structure:**
```json
{
  "timestamp": "2024-04-13T15:30:45",
  "user_inputs": {...},
  "optimal_system": {...},
  "performance_metrics": {...},
  "optimization_stats": {...}
}
```

---

## ✨ Pro Tips

1. **For reproducible results:** Write down the GA parameters used

2. **Compare scenarios:** Run multiple times with different budgets

3. **Fine-tune:** If first result looks good, try again with:
   - Higher generations (100)
   - Larger population (50)
   - For potential 2-3 point improvement

4. **Understand trade-offs:** 
   - Lower budget → Less solar/battery → More grid dependency
   - Higher budget → Better self-sufficiency → Higher upfront cost

5. **Share results:** JSON file includes all details for reporting/analysis

---

## 🆘 Getting Help

**Check these in order:**

1. `optimization/README.md` (70+ examples)
2. `OPTIMIZATION_ENGINE_SUMMARY.md` (complete technical guide)
3. Error message in console (usually tells you what's missing)
4. Verify input files exist (check outputs/ and Datasets/)
5. Try with simpler inputs (e.g., monthly_kwh=300, budget=500000)

---

## ✅ Checklist for Success

```
Before Running:
□ In project root directory
□ Files verified to exist
□ Inputs ready (monthly kWh, budget ₹)

After Starting:
□ Program accepts inputs
□ Shows "Initializing population..."
□ Shows generation progress (Gen 1/50, Gen 2/50, etc.)

Expected Output:
□ Optimal solar size (e.g., 8.5 kW)
□ Optimal battery size (e.g., 12.0 kWh)
□ Total cost ≤ your budget
□ Grid dependency < 100%
□ Results file created
```

---

## 🎯 One-Liner

All the magic in one command:

```bash
python -m optimization.main
```

**Then:**
1. Enter monthly usage (e.g., 350)
2. Enter budget (e.g., 600000)
3. Press Enter for advanced options
4. **Get optimal system in ~100 seconds!** ✨

---

**Happy Optimizing!** 🚀

For detailed info, see: `optimization/README.md`  
For technical deep-dive: See `OPTIMIZATION_ENGINE_SUMMARY.md`
