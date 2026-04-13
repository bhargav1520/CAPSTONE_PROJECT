# 🏗️ IEMS Optimization Engine - Architecture & Data Flow

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     OPTIMIZATION ENGINE (IEMS)                      │
│                   Genetic Algorithm Optimizer                       │
└─────────────────────────────────────────────────────────────────────┘

                         ┌────────────────┐
                         │   CLI MAIN.PY  │  ← START HERE
                         │ (UI Interface) │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
            ┌──────────────┐ ┌──────────────┐ ┌────────────────┐
            │  COMPONENT   │ │ DESIGN SPACE │ │  OBJECTIVE     │
            │   LOADER     │ │   GENERATOR  │ │    FUNCTION    │
            │              │ │              │ │  (Evaluator)   │
            │  • Load      │ │  • Generate  │ │                │
            │    Panels    │ │    Combos    │ │  • Run Sim     │
            │  • Load      │ │  • Calculate │ │  • Score      │
            │    Batteries │ │    Costs     │ │    Fitness    │
            │  • Lookup    │ │  • Random    │ │  • Check      │
            │    by ID     │ │    Solutions │ │    Budget     │
            └─────┬────────┘ └──────┬───────┘ └────────┬───────┘
                  │                 │                   │
                  └─────────────────┼──────────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │ GA OPTIMIZER           │
                        │                        │
                        │ • Initialize Pop       │
                        │ • Evaluate (1000x+)    │
                        │ • Select (Tournament)  │
                        │ • Crossover (Blend)    │
                        │ • Mutate (Random)      │
                        │ • Elitism (Keep Best)  │
                        │ • Iterate 50 times     │
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │  SIMULATOR INTEGRATION │
                        │                        │
                        │ HybridSystemSimulator  │
                        │ (simulation_engine/)   │
                        │                        │
                        │ • Load Model           │
                        │ • Solar Generation     │
                        │ • Battery Dispatch     │
                        │ • Energy Flow Logic    │
                        │ • Grid Purchase        │
                        │ • SoC Tracking         │
                        └────────────┬───────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │ Grid Usage   │ │ Solar Used   │ │ Battery SoC  │
            │ (kWh)        │ │ (kWh)        │ │ (%)          │
            │              │ │              │ │              │
            │ ↓ Metrics ↓  │ │ ↓ Metrics ↓  │ │ ↓ Metrics ↓  │
            │              │ │              │ │              │
            └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
                   │                │                │
                   └────────────────┼────────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │  FITNESS CALCULATION   │
                        │                        │
                        │ Fitness = 0.6 × Util  │
                        │         + 0.4 × Reduction
                        │         + SoC Bonus   │
                        │ Range: 0-100           │
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │  BEST SOLUTION        │
                        │                       │
                        │ • Solar Size (kW)     │
                        │ • Battery Size (kWh)  │
                        │ • Component IDs       │
                        │ • Total Cost (₹)      │
                        │ • Fitness Score       │
                        │ • Performance Metrics │
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │  RESULTS EXPORT        │
                        │  (JSON + Print)        │
                        │                        │
                        │ results/latest_       │
                        │ optimization_result   │
                        │ .json                 │
                        └────────────────────────┘
```

---

## 🔄 Genetic Algorithm Flow Diagram

```
START
  │
  ├─→ Initialize Population (30 random solutions)
  │
  └─→ FOR each generation (1 to 50):
      │
      ├─→ EVALUATE
      │   └─→ For each individual:
      │       ├─→ Run HybridSystemSimulator
      │       ├─→ Get summary metrics
      │       └─→ Calculate fitness (0-100)
      │
      ├─→ SELECT (Tournament)
      │   └─→ Pick best 3, winner goes to mating pool
      │
      ├─→ CROSSOVER
      │   └─→ For parent pairs:
      │       ├─→ Child1.solar = 0.6 × P1.solar + 0.4 × P2.solar
      │       ├─→ Child1.battery = 0.6 × P1.battery + 0.4 × P2.battery
      │       └─→ Clamp to valid ranges (1-15kW, 0-20kWh)
      │
      ├─→ MUTATE
      │   └─→ For each offspring (10% chance):
      │       ├─→ Randomly add ±2 to solar size
      │       └─→ Randomly add ±2 to battery size
      │
      ├─→ ELITISM
      │   └─→ Keep top 10% best individuals (3 out of 30)
      │
      └─→ Update population with new generation
           └─→ Track best fitness (convergence)
                │
                └─→ Print: "Gen 25/50 | Best: 74.35 | Avg: 68.20"
  │
  └─→ RETURN Best solution found
       ├─→ Solar size: 8.5 kW
       ├─→ Battery size: 12.0 kWh
       ├─→ Total cost: ₹511,000
       ├─→ Fitness: 78.45/100
       └─→ Metrics: Grid%, Solar%, Savings

END → Export to JSON
```

---

## 📂 Data Flow Diagram

```
INPUTS
══════════════════════════════════════════════════════════════════

CSV Files:
┌─────────────────────────────────────┐
│ Datasets/                           │
├─────────────────────────────────────┤
│ ✓ solar_panel_dataset.csv           │  15 models (400-550W)
│   • panel_id, rated_power_w         │  ₹16,000-23,500/panel
│   • efficiency, area_m2             │
│   • cost_per_panel, lifetime        │
│   • degradation_rate                │
├─────────────────────────────────────┤
│ ✓ battery_dataset.csv               │  15 models (2-15 kWh)
│   • battery_id, capacity_kwh        │  ₹120k-900k/unit
│   • max_charge_kw, efficiency       │
│   • cost, cycle_life                │
│   • depth_of_discharge              │
└─────────────────────────────────────┘

Simulation Data:
┌─────────────────────────────────────┐
│ outputs/                            │
├─────────────────────────────────────┤
│ ✓ cleaned_hourly.csv                │  8760+ rows
│   • Load per hour (kWh)             │  (Synthetic)
├─────────────────────────────────────┤
│ ✓ weather_irradiance.csv (optional) │  8760+ rows
│   • Solar irradiance (W/m²)         │  (Realistic)
└─────────────────────────────────────┘

User Inputs:
┌─────────────────────────────────────┐
│ monthly_kwh: 350                    │
│ budget: ₹600,000                    │
│ location: Mumbai                    │
│ population_size: 30                 │
│ generations: 50                     │
│ mutation_rate: 0.1                  │
└─────────────────────────────────────┘

                    ▼ PROCESSING

COMPONENT LOADING
═════════════════════════════════════════════════════════════════

component_loader.py
    │
    ├─→ Load solar_panel_dataset.csv
    │   └─→ Create 15 SolarPanel objects
    │       ├─→ SP_IND_001: 400W, ₹16,000, 19.5% eff
    │       ├─→ SP_IND_002: 410W, ₹16,500, 19.8% eff
    │       ├─→ ...
    │       └─→ SP_IND_015: 550W, ₹23,500, 23.0% eff
    │
    └─→ Load battery_dataset.csv
        └─→ Create 15 Battery objects
            ├─→ BAT_IND_001: 2.0 kWh, ₹120,000
            ├─→ BAT_IND_002: 3.0 kWh, ₹180,000
            ├─→ ...
            └─→ BAT_IND_015: 15.0 kWh, ₹900,000

DESIGN SPACE GENERATION
═════════════════════════════════════════════════════════════════

design_space.py
    │
    ├─→ Generate solar sizes: 1, 2, 3, ..., 15 kW (15 options)
    │
    ├─→ Generate battery sizes: 0, 2, 4, ..., 20 kWh (11 options)
    │
    ├─→ For each combination (15 × 11 = 165):
    │   ├─→ Calculate panels needed: ceil(solar_kw × 1000 / 400)
    │   │   Example: 8.5 kW → 21 panels (SP_IND_010 @ 400W)
    │   │
    │   ├─→ Calculate battery units: ceil(battery_kwh / 2)
    │   │   Example: 12 kWh → 4 units (BAT_IND_011 @ 3kWh)
    │   │
    │   └─→ Calculate total cost: panels_cost + batteries_cost
    │       Example: (21 × 20,500) + (4 × 720,000) = ₹3.315M
    │
    └─→ Create 165 CandidateSolution objects

BUDGET FILTERING
═════════════════════════════════════════════════════════════════

design_space.filter_by_budget(budget=600,000)
    │
    ├─→ Check each candidate
    │   ├─→ If cost ≤ ₹600,000 → Keep
    │   └─→ If cost > ₹600,000 → Remove
    │
    └─→ Result: ~85 valid candidates (within budget)

                    ▼ OPTIMIZATION

GENETIC ALGORITHM
═════════════════════════════════════════════════════════════════

optimizer.py (50 generations)

Gen 1:
┌───────────────────────────────────┐
│ Individual 1: 2.5 kW + 2 kWh      │ ← Random
│ Individual 2: 4.0 kW + 8 kWh      │ ← Random
│ Individual 3: 6.0 kW + 5 kWh      │ ← Random
│ ...   (30 total)                  │
│                                   │
│ FITNESS: [34, 48, 42, ..., 38]    │
│ BEST: 48.2                        │
└───────────────────────────────────┘

Gen 10:
┌───────────────────────────────────┐
│ Individual 1: 7.2 kW + 10 kWh     │ ← Improved
│ Individual 2: 8.1 kW + 11 kWh     │ ← Improved
│ Individual 3: 6.8 kW + 9 kWh      │ ← Improved
│ ...   (30 total)                  │
│                                   │
│ FITNESS: [62, 65, 59, ..., 58]    │
│ BEST: 65.3                        │
└───────────────────────────────────┘

Gen 25:
┌───────────────────────────────────┐
│ Individual 1: 8.4 kW + 12 kWh     │ ← Very good
│ Individual 2: 8.6 kW + 12 kWh     │ ← Very good
│ Individual 3: 8.5 kW + 11 kWh     │ ← Very good
│ ...   (30 total)                  │
│                                   │
│ FITNESS: [74, 76, 73, ..., 70]    │
│ BEST: 76.1                        │
└───────────────────────────────────┘

Gen 50:
┌───────────────────────────────────┐
│ Individual 1: 8.5 kW + 12.0 kWh   │ ← Optimal
│ Individual 2: 8.5 kW + 12.0 kWh   │ ← Optimal
│ Individual 3: 8.4 kW + 11.8 kWh   │ ← Near-optimal
│ ...   (30 total)                  │
│                                   │
│ FITNESS: [78.45, 78.45, 77.2, ...│
│ BEST: 78.45                       │
└───────────────────────────────────┘

EACH ITERATION RUNS SIMULATOR:
    │
    ├─→ HybridSystemSimulator(
    │       solar_kw=8.5,
    │       battery_kwh=12.0,
    │       load_file='cleaned_hourly.csv',
    │       irradiance_csv='weather_irradiance.csv'
    │   )
    │   │
    │   └─→ For each hour (0-8759):
    │       ├─→ Load = Load Model
    │       ├─→ Solar = Solar Model
    │       ├─→ Battery State = Battery Model
    │       ├─→ Dispatch = Energy Flow Logic
    │       │   ├─→ Solar → Load
    │       │   ├─→ Extra Solar → Battery Charge
    │       │   ├─→ Battery → Remaining Load
    │       │   └─→ Grid → Remaining Load
    │       └─→ Store: load, solar, battery, grid, soc
    │
    └─→ Calculate summary:
        ├─→ Total Load: 8,400 kWh
        ├─→ Solar Used: 5,735 kWh (68.3%)
        ├─→ Battery Discharge: 940 kWh
        ├─→ Grid Used: 1,890 kWh (22.5%)
        └─→ Average SoC: 65.2%

FITNESS EVALUATION:
    │
    ├─→ Solar Utilization = 5,735 / 8,400 = 68.3%
    ├─→ Grid Reduction = 100 - 22.5 = 77.5%
    ├─→ SoC Bonus = +5 (65% is in ideal 40-80% range)
    │
    └─→ Fitness = (0.6 × 68.3) + (0.4 × 77.5) + 5
                = 40.98 + 31.0 + 5
                = 76.98 ≈ 76.98

                    ▼ RESULTS

FINAL SOLUTION
═════════════════════════════════════════════════════════════════

CandidateSolution:
    │
    ├─→ solar_kw: 8.5
    ├─→ battery_kwh: 12.0
    ├─→ solar_panels_count: 21
    ├─→ battery_units: 4
    ├─→ total_cost: ₹511,000
    ├─→ solar_panel_id: SP_IND_010 (400W @ ₹20,500)
    └─→ battery_id: BAT_IND_011 (3.0 kWh @ ₹180,000)

Metrics:
    │
    ├─→ grid_dependency: 22.5%
    ├─→ solar_utilization: 68.3%
    ├─→ avg_battery_soc: 65.2%
    ├─→ estimated_savings: ₹15,120/month
    └─→ fitness: 78.45/100

Optimization Stats:
    │
    ├─→ generations: 50
    ├─→ population_size: 30
    ├─→ fitness_improvement: +33.25 (45.20 → 78.45)
    └─→ convergence: Better than random (78.45 vs avg 58)

OUTPUTS
═════════════════════════════════════════════════════════════════

Console Output (Formatted):
┌──────────────────────────────────────┐
│ OPTIMAL SYSTEM CONFIGURATION         │
├──────────────────────────────────────┤
│ Solar: 8.5 kW (21 panels)            │
│ Battery: 12.0 kWh (4 units)          │
│ Cost: ₹511,000 (85.2% of budget)     │
│                                      │
│ PERFORMANCE                          │
│ Grid Dependency: 22.5%               │
│ Solar Utilization: 68.3%             │
│ Monthly Savings: ₹15,120             │
│                                      │
│ FITNESS SCORE: 78.45/100             │
└──────────────────────────────────────┘

JSON Export:
```json
{
  "timestamp": "2024-04-13T15:30:45",
  "optimal_system": {
    "solar_size_kw": 8.5,
    "battery_size_kwh": 12.0,
    "total_cost_inr": 511000
  },
  "performance_metrics": {
    "grid_dependency_percent": 22.5,
    "solar_utilization_percent": 68.3,
    "estimated_savings_inr": 15120
  },
  "optimization_stats": {
    "final_generation": 50,
    "total_improvement": 33.25
  }
}
```

File Location:
    └─→ results/latest_optimization_result.json
    └─→ results/optimization_result_20240413_153045.json
```

---

## 🔗 Module Dependencies

```
main.py
  │
  ├─→ component_loader.py
  │   ├─→ pandas (CSV loading)
  │   └─→ dataclasses (SolarPanel, Battery)
  │
  ├─→ design_space.py
  │   ├─→ component_loader (ComponentLoader)
  │   └─→ math (ceil for counting)
  │
  ├─→ objective_functions.py
  │   ├─→ simulator.HybridSystemSimulator
  │   └─→ design_space (CandidateSolution)
  │
  └─→ optimizer.py
      ├─→ design_space (DesignSpace, CandidateSolution)
      ├─→ objective_functions (ObjectiveFunction)
      └─→ random, copy, math (GA operations)

simulation_engine/simulator.py
  │
  ├─→ load_model.py
  ├─→ solar_model.py
  ├─→ battery_model.py
  └─→ energy_flow.py
```

---

## ⚡ Computational Complexity

```
Design Space Generation: O(S × B × C)
  S = solar sizes (15)
  B = battery sizes (11)
  C = component lookup cost (O(n), n≤15)
  Total: ~2,500 operations (milliseconds)

GA Optimization: O(G × P × E + G × P × S)
  G = generations (50)
  P = population (30)
  E = evaluation (simulation, ~1-2 sec)
  S = selection/crossover/mutation (~ms)
  Total: 50 × 30 × 2 sec = ~100 seconds (dominant)

Total Runtime: ~1-2 minutes (mostly simulator)
```

---

## 📊 Fitness Convergence Example

```
Fitness Score Over Generations

100 |                              ╔════════════╗
    |                              ║            ║
 80 |                        ╔══════╝            ║
    |                        ║                   ║
 60 |        ╔═══════════════╝                   ║
    |        ║                                   ║
 40 |╔═══════╝                                   ║
    |║                                           ║
 20 |║                                           ║
    |║                                           ║
  0 |╚═══════════════════════════════════════════╩────
    └──────────────────────────────────────────────────
    0    10    20    30    40    50 (Generations)

Line: Best Fitness (per generation)
  Gen 0:   45.2 (random)
  Gen 10:  62.4 (improvement)
  Gen 25:  74.2 (convergence begins)
  Gen 50:  78.5 (final)
  
Improvement: +33.3 (73% better than random)
```

---

This architecture enables:
✅ **Efficient Search** - GA explores smartly, not exhaustively
✅ **Real Evaluation** - Uses actual simulator, not approximations  
✅ **User-Friendly** - Simple CLI hides complexity
✅ **Scalable** - Easy to add constraints, components, objectives
✅ **Production-Ready** - Robust error handling, clear outputs
