"""
CLI Script for Intelligent Energy Management System Optimization
Main entry point for user interaction.
"""

import os
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

# Add paths for simulation engine and synthetic load
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulation_engine'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'synthetic_load'))

from .component_loader import ComponentLoader
from .design_space import DesignSpace
from .objective_functions import ObjectiveFunction
from .optimizer import GeneticAlgorithmOptimizer

# Import existing modules for data generation
from generate_synthetic_load import generate_synthetic_load, save_to_csv
from weather_solar_fetch import fetch_nasa_power_irradiance


class UIConstants:
    """UI constants for formatted output."""
    BANNER_WIDTH = 80
    SEPARATOR = "=" * BANNER_WIDTH
    SUB_SEP = "-" * BANNER_WIDTH


# Location coordinates for solar data fetching
LOCATION_COORDINATES = {
    'bangalore': (12.9716, 77.5946),
    'mumbai': (19.0760, 72.8777),
    'delhi': (28.6139, 77.2090),
    'chennai': (13.0827, 80.2707),
    'hyderabad': (17.3850, 78.4867),
    'pune': (18.5204, 73.8567),
    'ahmedabad': (23.0225, 72.5714),
    'jaipur': (26.9124, 75.7873),
    'indore': (22.7196, 75.8577),
    'kolkata': (22.5726, 88.3639),
}

# Electricity rates in India - Tiered/Slab Pricing (₹/kWh per consumption range)
# Based on typical Indian domestic tariff structure
ELECTRICITY_SLABS = {
    'domestic': [
        (0, 50, 3.0),       # 0-50 kWh @ ₹3/kWh
        (50, 100, 4.5),     # 50-100 kWh @ ₹4.5/kWh
        (100, 200, 6.0),    # 100-200 kWh @ ₹6/kWh
        (200, 500, 8.0),    # 200-500 kWh @ ₹8/kWh
        (500, float('inf'), 12.0),  # 500+ kWh @ ₹12/kWh
    ],
    'commercial': [
        (0, 100, 8.0),
        (100, 500, 10.0),
        (500, float('inf'), 14.0),
    ]
}

# Timezone offsets for locations (all India uses IST = UTC+5:30)
LOCATION_TIMEZONES = {
    'bangalore': 5.5,
    'mumbai': 5.5,
    'delhi': 5.5,
    'chennai': 5.5,
    'hyderabad': 5.5,
    'pune': 5.5,
    'ahmedabad': 5.5,
    'jaipur': 5.5,
    'indore': 5.5,
    'kolkata': 5.5,
}


def calculate_electricity_bill(monthly_kwh: float, category: str = 'domestic') -> float:
    """
    Calculate monthly electricity bill using tiered pricing slabs.
    
    Args:
        monthly_kwh: Monthly electricity consumption in kWh
        category: 'domestic' or 'commercial'
        
    Returns:
        Total monthly bill amount in ₹
    """
    slabs = ELECTRICITY_SLABS.get(category, ELECTRICITY_SLABS['domestic'])
    total_cost = 0.0
    remaining_kwh = monthly_kwh
    
    for slab_min, slab_max, rate in slabs:
        if remaining_kwh <= 0:
            break
        
        # Calculate how many kWh fall in this slab
        kwh_in_slab = min(remaining_kwh, slab_max - slab_min)
        
        # Add cost for this slab
        total_cost += kwh_in_slab * rate
        remaining_kwh -= kwh_in_slab
    
    return total_cost


def print_banner():
    """Print project banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                               ║
    ║            INTELLIGENT ENERGY MANAGEMENT SYSTEM (IEMS)                        ║
    ║                   Genetic Algorithm Optimization Engine                       ║
    ║                                                                               ║
    ║  Optimize Solar + Battery Sizing for Maximum Savings & Grid Independence     ║
    ║                                                                               ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{UIConstants.SEPARATOR}")
    print(f"  {title}")
    print(f"{UIConstants.SEPARATOR}\n")


def get_user_inputs() -> dict:
    """
    Get user inputs for optimization.
    
    Returns:
        Dictionary with user inputs
    """
    print_section("USER INPUTS")
    
    print("📋 Please provide the following information:\n")
    
    # Monthly electricity usage (kWh)
    while True:
        try:
            monthly_kwh = float(input("   Monthly electricity usage (kWh) [e.g., 300]: "))
            if monthly_kwh <= 0:
                print("   ❌ Please enter a positive value.")
                continue
            break
        except ValueError:
            print("   ❌ Invalid input. Please enter a number.")
    
    # Calculate and display monthly bill based on tiered pricing
    monthly_bill = calculate_electricity_bill(monthly_kwh, 'domestic')
    print(f"\n   💡 Calculated Monthly Bill (Tiered Pricing): ₹{monthly_bill:,.2f}")
    
    # Budget for solar system
    while True:
        try:
            budget = float(input("\n   Total budget for solar system (₹) [e.g., 500000]: "))
            if budget <= 0:
                print("   ❌ Please enter a positive value.")
                continue
            break
        except ValueError:
            print("   ❌ Invalid input. Please enter a number.")
    
    # Location
    valid_locations = list(LOCATION_COORDINATES.keys())
    location = None
    while location is None:
        loc_input = input(f"\n   Location [{', '.join(valid_locations[:3])}...]: ").strip().lower()
        if loc_input in valid_locations:
            location = loc_input
        else:
            print(f"   ❌ Please choose from: {', '.join(valid_locations)}")
    
    # Number of days for the load profile
    try:
        days_input = input(f"\n   Number of days for load profile [default: 30]: ").strip()
        days = int(days_input) if days_input else 30
        days = max(1, min(365, days))
    except ValueError:
        days = 30
    
    # Advanced options
    print("\n   Advanced Options (press Enter for defaults):")
    
    try:
        pop_size = input("   Population size [default: 30]: ").strip()
        population_size = int(pop_size) if pop_size else 30
        population_size = max(10, min(100, population_size))
    except ValueError:
        population_size = 30
    
    try:
        gen_count = input("   Generations [default: 50]: ").strip()
        generations = int(gen_count) if gen_count else 50
        generations = max(10, min(200, generations))
    except ValueError:
        generations = 50
    
    try:
        mut_rate = input("   Mutation rate [default: 0.1]: ").strip()
        mutation_rate = float(mut_rate) if mut_rate else 0.1
        mutation_rate = max(0.01, min(0.5, mutation_rate))
    except ValueError:
        mutation_rate = 0.1
    
    return {
        'monthly_kwh': monthly_kwh,
        'monthly_bill': monthly_bill,
        'budget': budget,
        'location': location,
        'days': days,
        'population_size': population_size,
        'generations': generations,
        'mutation_rate': mutation_rate
    }


def prepare_data(workspace_root: str, inputs: dict) -> tuple:
    """
    Generate and prepare required data files.
    
    Args:
        workspace_root: Root path of the project
        inputs: User inputs with monthly_kwh, monthly_bill, days, and location
        
    Returns:
        Tuple of (load_file, irradiance_file, dataset_dir, monthly_kwh)
    """
    print_section("DATA GENERATION & PREPARATION")
    
    outputs_dir = os.path.join(workspace_root, 'outputs')
    datasets_dir = os.path.join(workspace_root, 'Datasets')
    
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Get number of days from inputs
    days = inputs.get('days', 30)
    
    # Get monthly kWh and bill (already calculated)
    monthly_kwh = inputs['monthly_kwh']
    monthly_bill = inputs['monthly_bill']
    
    print(f"\n  💰 Monthly Consumption & Cost:")
    print(f"     Monthly Usage: {monthly_kwh:.2f} kWh")
    print(f"     Monthly Bill (Tiered): ₹{monthly_bill:,.2f}")
    print(f"     Analysis Period: {days} days")
    
    # Generate synthetic load
    print(f"\n  🔄 Generating Synthetic Load Profile:")
    try:
        synthetic_load = generate_synthetic_load(monthly_kwh, days=days, random_seed=42)
        print(f"     Generated: {len(synthetic_load)} hourly values")
        print(f"     Total: {synthetic_load.sum():.2f} kWh")
        
        # Save to CSV (uses the module's OUTPUT_DIR which is outputs/)
        load_file = save_to_csv(synthetic_load, monthly_kwh, days=days)
        print(f"     ✓ Saved: {os.path.basename(load_file)}")
    except Exception as e:
        print(f"     ❌ ERROR: Failed to generate synthetic load: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Fetch solar irradiance data
    print(f"\n  📡 Fetching Solar Irradiance Data:")
    location = inputs['location']
    if location not in LOCATION_COORDINATES:
        print(f"     ❌ ERROR: Location {location} not supported")
        sys.exit(1)
    
    lat, lon = LOCATION_COORDINATES[location]
    print(f"     Location: {location.capitalize()} ({lat:.4f}°N, {lon:.4f}°E)")
    
    try:
        # Calculate date range: Use historical month data that's guaranteed to be available
        # NASA POWER API has data up to several months back, but not future dates
        # Use a fixed recent month that's definitely available
        end_date = datetime(2025, 12, 27).date()  # December 2025 - guaranteed available
        start_date = end_date - timedelta(days=days-1)
        
        print(f"     Period: {start_date} to {end_date} ({days} days)")
        
        # Fetch from NASA POWER API (returns UTC timestamps)
        irradiance_df = fetch_nasa_power_irradiance(
            latitude=lat,
            longitude=lon,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            community="RE",
            time_standard="UTC"
        )
        
        # Convert UTC timestamps to local timezone (IST = UTC+5:30 for India)
        tz_offset = LOCATION_TIMEZONES.get(location, 5.5)
        irradiance_df['timestamp'] = pd.to_datetime(irradiance_df['timestamp']) + timedelta(hours=tz_offset)
        
        # Save to CSV
        irradiance_file = os.path.join(outputs_dir, f"weather_irradiance_{location}.csv")
        irradiance_df.to_csv(irradiance_file, index=False)
        print(f"     ✓ Records: {len(irradiance_df)} hourly values (adjusted to local timezone)")
        print(f"     ✓ Saved: {os.path.basename(irradiance_file)}")
        
    except Exception as e:
        print(f"     ❌ ERROR: Failed to fetch solar data: {str(e)}")
        print(f"     Please check your internet connection and try again.")
        sys.exit(1)
    
    # Verify component datasets exist
    print(f"\n  ✓ Verifying Component Datasets:")
    
    solar_file = os.path.join(datasets_dir, 'solar_panel_dataset.csv')
    battery_file = os.path.join(datasets_dir, 'battery_dataset.csv')
    
    if not os.path.exists(solar_file):
        print(f"     ❌ ERROR: Solar panel dataset not found at {solar_file}")
        sys.exit(1)
    print(f"     ✓ Solar panel dataset: {os.path.basename(solar_file)}")
    
    if not os.path.exists(battery_file):
        print(f"     ❌ ERROR: Battery dataset not found at {battery_file}")
        sys.exit(1)
    print(f"     ✓ Battery dataset: {os.path.basename(battery_file)}")
    
    return load_file, irradiance_file, datasets_dir, monthly_kwh


def run_optimization(inputs: dict, workspace_root: str):
    """
    Run the optimization process.
    
    Args:
        inputs: User inputs dictionary
        workspace_root: Root path of the project
    """
    print_section("INITIALIZING OPTIMIZATION")
    
    # Prepare data (generates synthetic load and fetches solar data)
    load_file, irradiance_file, datasets_dir, monthly_kwh = prepare_data(workspace_root, inputs)
    
    # Store monthly_kwh in inputs for later use
    inputs['monthly_kwh'] = monthly_kwh
    
    # Load components
    print("\n📦 Loading component datasets...")
    loader = ComponentLoader(datasets_dir)
    loader.load_solar_panels()
    loader.load_batteries()
    loader.print_summary()
    
    # Create design space
    print("📐 Generating design space...")
    design_space = DesignSpace(
        component_loader=loader,
        solar_min_kw=1.0,
        solar_max_kw=15.0,
        battery_min_kwh=0.0,
        battery_max_kwh=20.0,
        step_solar_kw=1.0,
        step_battery_kwh=2.0
    )
    candidates_all = design_space.generate_design_space()
    print(f"✓ Design space generated: {len(candidates_all)} combinations")
    
    # Filter by budget
    candidates_budget = design_space.filter_by_budget(candidates_all, inputs['budget'])
    print(f"✓ Valid candidates (within budget): {len(candidates_budget)}")
    
    if not candidates_budget:
        print("\n❌ No valid solutions found within budget!")
        print(f"   Min cost in design space: ₹{min(c.total_cost for c in candidates_all):,.0f}")
        print(f"   Your budget: ₹{inputs['budget']:,.0f}")
        return
    
    # Create objective function
    print("\n🎯 Initializing objective function...")
    obj_func = ObjectiveFunction(
        load_file=load_file,
        weather_irradiance_file=irradiance_file,
        budget=inputs['budget'],
        solar_weight=0.6,
        grid_weight=0.4
    )
    
    # Create optimizer
    print("🧬 Initializing Genetic Algorithm...")
    optimizer = GeneticAlgorithmOptimizer(
        design_space=design_space,
        objective_function=obj_func,
        budget=inputs['budget'],
        population_size=inputs['population_size'],
        generations=inputs['generations'],
        mutation_rate=inputs['mutation_rate'],
        crossover_rate=0.8,
        elite_percentage=0.1,
        random_seed=42
    )
    
    # Run optimization
    print_section("RUNNING OPTIMIZATION")
    results = optimizer.evolve()
    
    # Print results
    optimizer.print_results(results)
    
    # Export results
    export_results(results, inputs, workspace_root)


def export_results(results: dict, inputs: dict, workspace_root: str):
    """
    Export optimization results to JSON and display summary.
    
    Args:
        results: Optimization results dictionary
        inputs: User inputs
        workspace_root: Root path
    """
    print_section("RESULTS EXPORT")
    
    solution = results['best_solution']
    metrics = results['metrics']
    
    # Prepare JSON output
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'user_inputs': {
            'monthly_bill_inr': inputs['monthly_bill'],
            'calculated_monthly_kwh': inputs['monthly_kwh'],
            'budget_inr': inputs['budget'],
            'location': inputs['location'],
            'population_size': inputs['population_size'],
            'generations': inputs['generations'],
            'mutation_rate': inputs['mutation_rate']
        },
        'optimal_system': {
            'solar_size_kw': solution.solar_kw,
            'battery_size_kwh': solution.battery_kwh,
            'solar_panels_count': solution.solar_panels_count,
            'battery_units': solution.battery_units,
            'total_cost_inr': solution.total_cost,
            'solar_panel_id': solution.solar_panel_id,
            'battery_id': solution.battery_id
        },
        'performance_metrics': {
            'grid_dependency_percent': metrics['grid_dependency'],
            'solar_utilization_percent': metrics['solar_utilization'],
            'avg_battery_soc_percent': metrics['avg_soc'],
            'estimated_savings_inr': metrics['estimated_savings'],
            'fitness_score': results['best_fitness']
        },
        'optimization_stats': {
            'final_generation': results['generations'],
            'population_size': results['population_size'],
            'final_fitness': results['fitness_history'][-1],
            'initial_fitness': results['fitness_history'][0],
            'total_improvement': results['fitness_history'][-1] - results['fitness_history'][0]
        }
    }
    
    # Create results directory
    results_dir = os.path.join(workspace_root, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Save JSON
    json_file = os.path.join(results_dir, f"optimization_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(json_file, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"✓ Results saved to: {json_file}")
    
    # Save latest result
    latest_file = os.path.join(results_dir, 'latest_optimization_result.json')
    with open(latest_file, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"✓ Latest result saved to: {latest_file}")
    
    # Print summary table
    print_section("FINAL SUMMARY")
    
    print(f"  📊 SYSTEM SIZING")
    print(f"  {UIConstants.SUB_SEP}")
    print(f"    Solar System Size:        {solution.solar_kw:.1f} kW")
    print(f"    Battery Storage Capacity: {solution.battery_kwh:.1f} kWh")
    print(f"    Total System Cost:        ₹{solution.total_cost:>15,.2f}")
    print(f"    Budget Allocated:         ₹{inputs['budget']:>15,.2f}")
    print(f"    Budget Remaining:         ₹{inputs['budget'] - solution.total_cost:>15,.2f}")
    
    print(f"\n  💡 KEY BENEFITS")
    print(f"  {UIConstants.SUB_SEP}")
    print(f"    Grid Dependency:          {metrics['grid_dependency']:>15.1f}%")
    print(f"    Solar Utilization:        {metrics['solar_utilization']:>15.1f}%")
    print(f"    Annual Savings:           ₹{metrics['estimated_savings'] * 12:>15,.2f}")
    
    print(f"\n  🏆 OPTIMIZATION PERFORMANCE")
    print(f"  {UIConstants.SUB_SEP}")
    print(f"    Fitness Score:            {results['best_fitness']:>15.2f}/100")
    print(f"    Generations Evolved:      {results['generations']:>15}")
    print(f"    Fitness Improvement:      {results['fitness_history'][-1] - results['fitness_history'][0]:>15.2f}")
    
    print(f"\n{UIConstants.SEPARATOR}\n")


def main():
    """Main entry point."""
    print_banner()
    
    # Get workspace root
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Get user inputs
        inputs = get_user_inputs()
        
        # Run optimization
        run_optimization(inputs, workspace_root)
        
        print("✓ Optimization completed successfully!")
        print("  Check 'results/' directory for detailed results.\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠  Optimization cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
