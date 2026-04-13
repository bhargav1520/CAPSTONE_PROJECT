"""
Design Space Module
Generate valid combinations of solar system sizes and battery capacities.
"""

import math
from typing import List, Dict
from dataclasses import dataclass
from .component_loader import ComponentLoader, SolarPanel, Battery


@dataclass
class CandidateSolution:
    """Represents a candidate system configuration."""
    solar_kw: float
    battery_kwh: float
    solar_panels_count: int
    battery_units: int
    total_cost: float
    solar_panel_id: str
    battery_id: str

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'solar_kw': round(self.solar_kw, 2),
            'battery_kwh': round(self.battery_kwh, 2),
            'solar_panels_count': self.solar_panels_count,
            'battery_units': self.battery_units,
            'total_cost': round(self.total_cost, 2),
            'solar_panel_id': self.solar_panel_id,
            'battery_id': self.battery_id
        }


class DesignSpace:
    """Generate and manage design space of candidate solutions."""

    def __init__(
        self,
        component_loader: ComponentLoader,
        solar_min_kw: float = 1.0,
        solar_max_kw: float = 15.0,
        battery_min_kwh: float = 0.0,
        battery_max_kwh: float = 20.0,
        step_solar_kw: float = 1.0,
        step_battery_kwh: float = 2.0
    ):
        """
        Initialize design space generator.
        
        Args:
            component_loader: ComponentLoader instance
            solar_min_kw: Minimum solar system size (kW)
            solar_max_kw: Maximum solar system size (kW)
            battery_min_kwh: Minimum battery capacity (kWh)
            battery_max_kwh: Maximum battery capacity (kWh)
            step_solar_kw: Step size for solar generation (default 1 kW)
            step_battery_kwh: Step size for battery capacity (default 2 kWh)
        """
        self.component_loader = component_loader
        self.solar_min_kw = solar_min_kw
        self.solar_max_kw = solar_max_kw
        self.battery_min_kwh = battery_min_kwh
        self.battery_max_kwh = battery_max_kwh
        self.step_solar_kw = step_solar_kw
        self.step_battery_kwh = step_battery_kwh
        
        self.solar_panels = component_loader.get_solar_panels()
        self.batteries = component_loader.get_batteries()

    def calculate_solar_panels_needed(self, solar_kw: float) -> Dict:
        """
        Calculate number of solar panels needed for a given capacity.
        
        Args:
            solar_kw: Required solar capacity in kW
            
        Returns:
            Dictionary with panel counts and costs for each panel model
        """
        results = {}
        solar_w = solar_kw * 1000  # Convert to Watts
        
        for panel in self.solar_panels:
            panels_needed = math.ceil(solar_w / panel.rated_power_w)
            actual_capacity_w = panels_needed * panel.rated_power_w
            actual_capacity_kw = actual_capacity_w / 1000
            total_cost = panels_needed * panel.cost_per_panel
            
            results[panel.panel_id] = {
                'panels_count': panels_needed,
                'actual_capacity_kw': actual_capacity_kw,
                'total_cost': total_cost
            }
        
        return results

    def calculate_battery_units_needed(self, battery_kwh: float) -> Dict:
        """
        Calculate number of battery units needed for a given capacity.
        
        Args:
            battery_kwh: Required battery capacity in kWh
            
        Returns:
            Dictionary with battery counts and costs for each battery model
        """
        results = {}
        
        # If 0 kWh, no batteries needed
        if battery_kwh == 0:
            for battery in self.batteries:
                results[battery.battery_id] = {
                    'units': 0,
                    'actual_capacity_kwh': 0,
                    'total_cost': 0
                }
            return results
        
        for battery in self.batteries:
            units_needed = math.ceil(battery_kwh / battery.capacity_kwh)
            actual_capacity_kwh = units_needed * battery.capacity_kwh
            total_cost = units_needed * battery.cost
            
            results[battery.battery_id] = {
                'units': units_needed,
                'actual_capacity_kwh': actual_capacity_kwh,
                'total_cost': total_cost
            }
        
        return results

    def generate_design_space(self) -> List[CandidateSolution]:
        """
        Generate all valid candidate solutions within design space.
        
        Returns:
            List of CandidateSolution objects
        """
        candidates = []
        
        # Iterate through solar sizes
        solar_values = self._generate_range(
            self.solar_min_kw,
            self.solar_max_kw,
            self.step_solar_kw
        )
        
        # Iterate through battery sizes (including 0)
        battery_values = self._generate_range(
            self.battery_min_kwh,
            self.battery_max_kwh,
            self.step_battery_kwh
        )
        
        for solar_kw in solar_values:
            solar_results = self.calculate_solar_panels_needed(solar_kw)
            
            for battery_kwh in battery_values:
                battery_results = self.calculate_battery_units_needed(battery_kwh)
                
                # Select cheapest option for each size
                best_solar = min(
                    solar_results.items(),
                    key=lambda x: x[1]['total_cost']
                )
                best_battery = min(
                    battery_results.items(),
                    key=lambda x: x[1]['total_cost']
                )
                
                solar_panel_id = best_solar[0]
                battery_id = best_battery[0]
                
                candidate = CandidateSolution(
                    solar_kw=solar_kw,
                    battery_kwh=battery_kwh,
                    solar_panels_count=best_solar[1]['panels_count'],
                    battery_units=best_battery[1]['units'],
                    total_cost=best_solar[1]['total_cost'] + best_battery[1]['total_cost'],
                    solar_panel_id=solar_panel_id,
                    battery_id=battery_id
                )
                candidates.append(candidate)
        
        return candidates

    def generate_random_solution(self) -> CandidateSolution:
        """
        Generate a random valid solution within design space.
        
        Returns:
            Random CandidateSolution
        """
        import random
        
        solar_values = self._generate_range(
            self.solar_min_kw,
            self.solar_max_kw,
            self.step_solar_kw
        )
        battery_values = self._generate_range(
            self.battery_min_kwh,
            self.battery_max_kwh,
            self.step_battery_kwh
        )
        
        solar_kw = random.choice(solar_values)
        battery_kwh = random.choice(battery_values)
        
        solar_results = self.calculate_solar_panels_needed(solar_kw)
        battery_results = self.calculate_battery_units_needed(battery_kwh)
        
        best_solar = min(
            solar_results.items(),
            key=lambda x: x[1]['total_cost']
        )
        best_battery = min(
            battery_results.items(),
            key=lambda x: x[1]['total_cost']
        )
        
        return CandidateSolution(
            solar_kw=solar_kw,
            battery_kwh=battery_kwh,
            solar_panels_count=best_solar[1]['panels_count'],
            battery_units=best_battery[1]['units'],
            total_cost=best_solar[1]['total_cost'] + best_battery[1]['total_cost'],
            solar_panel_id=best_solar[0],
            battery_id=best_battery[0]
        )

    def filter_by_budget(self, candidates: List[CandidateSolution], budget: float) -> List[CandidateSolution]:
        """
        Filter candidates that exceed budget.
        
        Args:
            candidates: List of candidate solutions
            budget: Budget constraint in ₹
            
        Returns:
            Filtered list of candidates within budget
        """
        return [c for c in candidates if c.total_cost <= budget]

    @staticmethod
    def _generate_range(start: float, end: float, step: float) -> List[float]:
        """Generate range of values with given step."""
        values = []
        current = start
        while current <= end + 1e-6:  # Add small epsilon for floating point comparison
            values.append(round(current, 2))
            current += step
        return values

    def print_sample_solutions(self, count: int = 5):
        """Print sample candidate solutions."""
        candidates = self.generate_design_space()
        print("\n" + "="*80)
        print("DESIGN SPACE SAMPLE (First {} candidates)".format(min(count, len(candidates))))
        print("="*80)
        print(f"{'Solar (kW)':<12} {'Battery (kWh)':<15} {'Panels':<8} {'Units':<8} {'Cost (₹)':<15}")
        print("-"*80)
        for candidate in candidates[:count]:
            print(f"{candidate.solar_kw:<12.1f} {candidate.battery_kwh:<15.1f} {candidate.solar_panels_count:<8} {candidate.battery_units:<8} ₹{candidate.total_cost:>12,.0f}")
        print("="*80 + "\n")
