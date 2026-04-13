## 🧬 Optimization Engine - Genetic Algorithm for IEMS

This folder contains the **Genetic Algorithm (GA) based optimization engine** for the Intelligent Energy Management System (IEMS). It automatically finds the optimal combination of solar system size and battery capacity to maximize savings and minimize grid dependency.

---

## 📁 Module Structure

```
optimization/
├── component_loader.py        # Load solar panels and batteries from CSV
├── design_space.py            # Generate valid combinations of solar/battery sizes
├── objective_functions.py     # Define fitness function for evaluation
├── optimizer.py               # Genetic Algorithm implementation
├── main.py                    # CLI interface (user entry point)
├── __init__.py                # Package initialization
└── README.md                  # This file
```

---

## 🚀 Quick Start

### 1. Run the Optimization

```bash
# From project root
python -m optimization.main

# Or directly
cd optimization
python main.py
```

### 2. Follow the Interactive Prompts

```
📋 USER INPUTS

   Monthly electricity usage (kWh) [e.g., 300]: 350
   
   💡 Calculated Monthly Bill (Tiered Pricing): ₹2,175.00
   
   Total budget for solar system (₹) [e.g., 500000]: 600000
   
   Location [bangalore, mumbai, delhi...]: bangalore
   
   Number of days for load profile [default: 30]: 30
   
   Advanced Options (press Enter for defaults):
   Population size [default: 30]: 
   Generations [default: 50]: 
   Mutation rate [default: 0.1]:
```

**Input Guide:**
- **Monthly Electricity Usage (kWh)**: Your actual consumption from the meter (not bill amount)
- **Tiered Pricing**: System automatically calculates bill with realistic Indian slab rates
- **Total Budget**: Maximum budget available for solar + battery system
- **Location**: City name for solar irradiance data (Bangalore, Mumbai, Delhi, etc.)
- **Number of Days**: Duration for load profile generation in days (default 30 is recommended)
- **Advanced Options**: Tuning parameters for GA (optional, defaults are good for most cases)

### 3. Results

The system will output:
- **Optimal solar size** (kW) and **battery capacity** (kWh)
- **System cost** and **budget utilization**
- **Performance metrics**: grid dependency, solar utilization, estimated savings
- **Fitness score** and optimization statistics
- Results saved to `results/latest_optimization_result.json`

---

## 📊 Module Descriptions

### `component_loader.py`
**Purpose:** Load and manage solar panel and battery specifications from CSV datasets.

**Classes:**
- `SolarPanel`: Dataclass for solar panel specifications
  - `panel_id`, `rated_power_w`, `efficiency`, `area_m2`, `cost_per_panel`, `lifetime_years`, `degradation_rate`
  
- `Battery`: Dataclass for battery specifications
  - `battery_id`, `capacity_kwh`, `max_charge_kw`, `max_discharge_kw`, `efficiency`, `cost`, `cycle_life`, `depth_of_discharge`

- `ComponentLoader`: Loads datasets, provides lookup functions, prints summaries

**Key Methods:**
```python
loader = ComponentLoader('Datasets')
loader.load_solar_panels()        # Returns List[SolarPanel]
loader.load_batteries()           # Returns List[Battery]
loader.get_panel_by_id('SP_IND_001')
loader.get_battery_by_id('BAT_IND_001')
```

---

### `design_space.py`
**Purpose:** Generate valid combinations of solar and battery sizes constrained by budget.

**Classes:**
- `CandidateSolution`: Represents a system configuration
  - `solar_kw`, `battery_kwh`, `solar_panels_count`, `battery_units`, `total_cost`, `solar_panel_id`, `battery_id`

- `DesignSpace`: Generates and manages candidate solutions
  - Converts solar/battery sizes to component counts
  - Calculates total costs
  - Filters by budget constraints

**Key Methods:**
```python
design_space = DesignSpace(loader)

# Get random valid solution
candidate = design_space.generate_random_solution()

# Generate all combinations
all_candidates = design_space.generate_design_space()

# Filter by budget
candidates = design_space.filter_by_budget(all_candidates, budget=500000)
```

---

### `objective_functions.py`
**Purpose:** Evaluate fitness (quality) of candidate solutions using the simulator.

**Classes:**
- `ObjectiveFunction`: Calculates fitness scores

**Fitness Calculation:**
```
Fitness = (Solar Weight × Solar Utilization) + (Grid Weight × Grid Reduction)
        + SoC Bonus (if battery in ideal range)
```

- **Maximizes:** Solar utilization, savings, battery health
- **Minimizes:** Grid dependency
- **Constraint:** Budget (rejects over-budget solutions)

**Key Methods:**
```python
obj_func = ObjectiveFunction(
    load_file='outputs/cleaned_hourly.csv',
    weather_irradiance_file='outputs/weather_irradiance.csv',
    budget=500000
)

# Evaluate single candidate
fitness, metrics = obj_func.evaluate(candidate)
# Returns: (fitness_score: float, metrics: dict)

# Batch evaluation
results = obj_func.evaluate_batch(candidate_list)
```

---

### `optimizer.py`
**Purpose:** Genetic Algorithm for optimization.

**Algorithm Steps:**
1. **Initialize**: Create random population of solutions
2. **Evaluate**: Score each solution using simulator
3. **Select**: Tournament selection of best individuals
4. **Crossover**: Blend genes from two parents
5. **Mutate**: Random perturbations
6. **Elitism**: Preserve best individuals
7. **Repeat**: For N generations

**Key Features:**
- ✓ Population: 20-100 individuals
- ✓ Generations: 10-200
- ✓ Mutation rate: 1-50%
- ✓ Crossover rate: 50-99%
- ✓ Elite preservation: Top 10%

**Classes:**
- `GeneticAlgorithmOptimizer`: GA implementation

**Key Methods:**
```python
ga = GeneticAlgorithmOptimizer(
    design_space=design_space,
    objective_function=obj_func,
    budget=budget,
    population_size=30,
    generations=50,
    mutation_rate=0.1
)

results = ga.evolve()
# Returns best solution and fitness history

ga.print_results(results)
```

---

### `main.py`
**Purpose:** Interactive CLI for end-users.

**Features:**
- ✓ User-friendly prompts
- ✓ Input validation
- ✓ Data verification
- ✓ Rich formatted output
- ✓ JSON result export
- ✓ Error handling

**Run Command:**
```bash
python main.py
```

---

## 🎯 How Optimization Works

### Input Data Required

1. **Synthetic Load** (`outputs/cleaned_hourly.csv`)
   - Hourly energy consumption (kWh)

2. **Weather/Irradiance** (`outputs/weather_irradiance.csv`)
   - Optional but recommended
   - Solar irradiance data (W/m²)

3. **Component Datasets**
   - Solar panels CSV with 15 models
   - Batteries CSV with 15 models

4. **User Budget** (₹)
   - Maximum allowable system cost

### Process Flow

```
User Inputs (Monthly kWh, Budget)
              ↓
Load Components (Solar Panels, Batteries)
              ↓
Generate Design Space (All valid combinations)
              ↓
Filter by Budget (Remove expensive options)
              ↓
Initialize GA Population (Random solutions)
              ↓
+→ Evaluate Fitness (Run simulator for each)
│   ↓
│  Selection (Tournament)
│   ↓
│  Crossover (Blend sizes)
│   ↓
│  Mutation (Random changes)
│   ↓
│  Elitism (Preserve best)
│   ↓
└─ Repeat for N Generations
              ↓
Output Best Solution
              ↓
Export Results (JSON)
```

---

## 📈 Output Example

```
====================================================================
                    OPTIMIZATION RESULTS
====================================================================

🎯 OPTIMAL SYSTEM CONFIGURATION
--------------------------------------------------
  Solar Capacity: 8.5 kW (21 panels)
  Battery Capacity: 12.0 kWh (4 units)
  Total System Cost: ₹511,000
  Budget Available: ₹600,000
  Budget Utilization: 85.2%

📊 PERFORMANCE METRICS
--------------------------------------------------
  Grid Dependency: 22.5%
  Solar Utilization: 68.3%
  Avg. Battery SoC: 65.2%
  Estimated Savings: ₹42,500

🏆 FITNESS SCORE: 78.45/100
--------------------------------------------------

📈 OPTIMIZATION STATISTICS
--------------------------------------------------
  Generations: 50
  Population Size: 30
  Final Fitness: 78.45
  Initial Fitness: 45.20
  Improvement: +33.25

====================================================================
```

---

## 🔧 Configuration & Parameters

### GA Parameters (Tunable)

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| Population Size | 30 | 10-100 | More diversity, slower computation |
| Generations | 50 | 10-200 | More evolution time, longer runtime |
| Mutation Rate | 0.1 | 0.01-0.5 | Higher = more random changes |
| Crossover Rate | 0.8 | 0.5-0.99 | Higher = more mixing |
| Elite Size | 10% | 5-20% | Higher = more conservative |

### Design Space Ranges

| Parameter | Min | Max | Step |
|-----------|-----|-----|------|
| Solar Size | 1 kW | 15 kW | 1 kW |
| Battery Size | 0 kWh | 20 kWh | 2 kWh |

### Objective Function Weights

```python
solar_weight = 0.6    # 60% - Maximize solar usage
grid_weight = 0.4     # 40% - Minimize grid dependency
```

---

## 🐛 Troubleshooting

### Problem: "No valid solutions found within budget"
**Solution:**
- Increase budget
- Reduce design space ranges
- Check for realistic costs in component datasets

### Problem: "Load file not found"
**Solution:**
- Run synthetic load generation first
- Check `outputs/cleaned_hourly.csv` exists

### Problem: Slow optimization
**Solution:**
- Reduce population size (e.g., 20 instead of 30)
- Reduce generations (e.g., 30 instead of 50)
- Use smaller design space

### Problem: Results seem unrealistic
**Solution:**
- Verify input load data
- Check component costs match market rates
- Increase generations for better convergence

---

## 📋 Integration with Simulation Engine

The optimization engine directly uses `HybridSystemSimulator` for:
- Solar generation calculation
- Battery charge/discharge simulation
- Energy flow dispatch logic
- Grid dependency assessment
- SoC (State of Charge) tracking

**Simulation Parameters Auto-Calculated:**
```python
battery_charge_kw = battery_kwh / 2      # Assume 2-hour charge time
battery_discharge_kw = battery_kwh / 2   # Assume 2-hour discharge time
```

---

## 📊 Results Export Format

Results are saved as JSON with complete details:

```json
{
  "timestamp": "2024-04-13T15:30:45.123456",
  "user_inputs": {
    "monthly_kwh": 350,
    "budget_inr": 600000,
    "location": "Mumbai",
    "population_size": 30,
    "generations": 50,
    "mutation_rate": 0.1
  },
  "optimal_system": {
    "solar_size_kw": 8.5,
    "battery_size_kwh": 12.0,
    "solar_panels_count": 21,
    "battery_units": 4,
    "total_cost_inr": 511000.0,
    "solar_panel_id": "SP_IND_010",
    "battery_id": "BAT_IND_011"
  },
  "performance_metrics": {
    "grid_dependency_percent": 22.5,
    "solar_utilization_percent": 68.3,
    "avg_battery_soc_percent": 65.2,
    "estimated_savings_inr": 42500.0,
    "fitness_score": 78.45
  },
  "optimization_stats": {
    "final_generation": 50,
    "population_size": 30,
    "final_fitness": 78.45,
    "initial_fitness": 45.20,
    "total_improvement": 33.25
  }
}
```

---

## 🎓 Use Cases

### Use Case 1: Residential System Design
- Input: 300 kWh/month usage, ₹400,000 budget
- Output: 6 kW + 10 kWh optimal system
- Benefit: Reduce grid dependency to <30%, save ₹35k/year

### Use Case 2: Small Commercial System
- Input: 800 kWh/month usage, ₹1,200,000 budget
- Output: 12 kW + 15 kWh optimal system
- Benefit: Achieve 70% solar self-consumption, ROI in 5 years

### Use Case 3: Budget Optimization
- Input: 500 kWh/month usage, ₹500,000 budget (tight)
- Output: 5 kW + 5 kWh minimal system
- Benefit: 40% solar offset, expandable

---

## 📚 References & Standards

- **MNRE Benchmarks**: Solar costs ₹50-90/Wp, Battery ₹5,000-10,000/kWh
- **Indian Grid Tariff**: ₹8-12/kWh (used for savings calculation)
- **Panel Degradation**: 0.4-0.55% annually
- **Battery Efficiency**: 92-97% (Li-ion)
- **Cycle Life**: 5,000-8,500 cycles (≈20 years)

---

## ✅ Design Principles

- **Modular**: Independent, reusable components
- **Clean Code**: Well-documented, PEP-8 compliant
- **Extensible**: Easy to add new components or constraints
- **User-Friendly**: Interactive CLI with clear prompts
- **Efficient**: Reuses simulation engine, caches results
- **Realistic**: Uses real component data and market-aligned costs

---

## 📝 License & Credits

Part of IEMS Capstone Project
Integrated Energy Management System for Solar + Battery + Grid Systems

---

## 🤝 Contributing

To extend the optimizer:

1. **Add new constraints** → Modify `objective_functions.py`
2. **Add component types** → Update `component_loader.py`
3. **Tweak GA parameters** → Edit `optimizer.py`
4. **Add new output formats** → Extend `main.py`

---

**Last Updated:** April 2024
**Version:** 1.0.0
