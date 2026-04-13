"""
Objective Functions Module
Defines fitness function for evaluating candidate solutions.
"""

import sys
import os
from typing import Dict, Tuple
from .design_space import CandidateSolution

# Add simulation_engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulation_engine'))

try:
    from simulator import HybridSystemSimulator
except ImportError:
    from simulation_engine.simulator import HybridSystemSimulator


class ObjectiveFunction:
    """Defines and evaluates fitness for candidate solutions."""

    def __init__(
        self,
        load_file: str,
        weather_irradiance_file: str,
        budget: float,
        solar_weight: float = 0.6,
        grid_weight: float = 0.4
    ):
        """
        Initialize objective function.
        
        Args:
            load_file: Path to synthetic load CSV
            weather_irradiance_file: Path to weather/irradiance CSV
            budget: Budget constraint in ₹
            solar_weight: Weight for solar utilization (0-1)
            grid_weight: Weight for grid reduction (0-1)
        """
        self.load_file = load_file
        self.weather_irradiance_file = weather_irradiance_file
        self.budget = budget
        self.solar_weight = solar_weight
        self.grid_weight = grid_weight
        
        # Normalize weights
        total_weight = solar_weight + grid_weight
        self.solar_weight = solar_weight / total_weight
        self.grid_weight = grid_weight / total_weight

    def evaluate(self, candidate: CandidateSolution) -> Tuple[float, Dict]:
        """
        Evaluate fitness of a candidate solution.
        
        Args:
            candidate: CandidateSolution to evaluate
            
        Returns:
            Tuple of (fitness_score, metrics_dict)
            
        Raises:
            Exception: If budget constraint is violated
        """
        # Check budget constraint - immediately reject if over budget
        if candidate.total_cost > self.budget:
            return 0.0, {
                'grid_dependency': 100.0,
                'solar_utilization': 0.0,
                'estimated_savings': 0.0,
                'fitness': 0.0,
                'status': 'REJECTED - Over budget'
            }

        try:
            # Create simulator instance
            simulator = HybridSystemSimulator(
                load_file=self.load_file,
                solar_kw=candidate.solar_kw,
                battery_kwh=candidate.battery_kwh,
                battery_charge_kw=candidate.battery_kwh / 2,  # Assume ~2hr charge time
                battery_discharge_kw=candidate.battery_kwh / 2,  # Assume ~2hr discharge time
                weather_irradiance_csv=self.weather_irradiance_file
            )

            # Run simulation
            simulator.run()

            # Get summary metrics
            summary = simulator.summary()

            # Extract key metrics
            total_load = summary['Total Load']
            grid_used = summary['Grid Used']
            solar_used = summary['Solar Used']
            avg_soc = summary['Average SoC (%)']
            grid_dependency = summary['Grid Dependency (%)']

            # Calculate fitness components
            # 1. Solar utilization (maximize) - percentage of load met by solar
            if total_load > 0:
                solar_utilization = (solar_used / total_load) * 100
            else:
                solar_utilization = 0.0

            # 2. Grid reduction (minimize) - grid dependency percentage
            # Convert to maximization: 100 - grid_dependency
            grid_reduction = 100 - grid_dependency

            # 3. Estimated savings
            # Assume grid costs ₹8 per kWh (standard Indian industrial rate)
            grid_tariff = 8.0  # ₹/kWh
            grid_cost = grid_used * grid_tariff
            estimated_savings = grid_cost

            # Combined fitness score (maximize)
            fitness = (
                self.solar_weight * solar_utilization +
                self.grid_weight * grid_reduction
            )

            # Add bonus for better battery utilization
            soc_bonus = 0.0
            if 40 <= avg_soc <= 80:  # Ideal SoC range
                soc_bonus = 5.0

            fitness += soc_bonus

            # Normalize to 0-100 scale
            fitness = max(0.0, min(fitness, 100.0))

            metrics = {
                'grid_dependency': round(grid_dependency, 2),
                'solar_utilization': round(solar_utilization, 2),
                'estimated_savings': round(estimated_savings, 2),
                'avg_soc': round(avg_soc, 2),
                'fitness': round(fitness, 2),
                'status': 'VALID'
            }

            return fitness, metrics

        except Exception as e:
            # Return very low fitness if simulation fails
            return 0.0, {
                'grid_dependency': 100.0,
                'solar_utilization': 0.0,
                'estimated_savings': 0.0,
                'fitness': 0.0,
                'status': f'ERROR - {str(e)}'
            }

    def evaluate_batch(self, candidates: list) -> Dict:
        """
        Evaluate multiple candidates.
        
        Args:
            candidates: List of CandidateSolution objects
            
        Returns:
            Dictionary mapping candidate to (fitness, metrics)
        """
        results = {}
        
        print(f"\nEvaluating {len(candidates)} candidates...")
        for i, candidate in enumerate(candidates):
            fitness, metrics = self.evaluate(candidate)
            results[id(candidate)] = {
                'candidate': candidate,
                'fitness': fitness,
                'metrics': metrics
            }
            
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{len(candidates)} evaluated")
        
        return results

    def print_evaluation_result(self, candidate: CandidateSolution, fitness: float, metrics: Dict):
        """Print evaluation result in formatted manner."""
        print("\n" + "-"*70)
        print(f"Solar: {candidate.solar_kw:.1f}kW | Battery: {candidate.battery_kwh:.1f}kWh | Cost: ₹{candidate.total_cost:,.0f}")
        print("-"*70)
        print(f"Status: {metrics['status']}")
        if metrics['status'] == 'VALID':
            print(f"Grid Dependency: {metrics['grid_dependency']:.1f}%")
            print(f"Solar Utilization: {metrics['solar_utilization']:.1f}%")
            print(f"Avg. Battery SoC: {metrics['avg_soc']:.1f}%")
            print(f"Estimated Savings: ₹{metrics['estimated_savings']:,.0f}")
            print(f"Fitness Score: {fitness:.2f}/100")
        print("-"*70)
