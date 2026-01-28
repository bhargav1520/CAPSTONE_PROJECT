# simulator.py
# This module runs the overall simulation using the models and logic defined in other modules.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd

from simulation_engine.load_model import LoadModel
from simulation_engine.solar_model import SolarModel
from simulation_engine.battery_model import BatteryModel
from simulation_engine.energy_flow import EnergyFlow


class HybridSystemSimulator:
    """
    Hybrid Solar-Battery System Simulator
    -------------------------------------
    Runs full hour-by-hour simulation and
    produces energy performance metrics
    """

    def __init__(
        self,
        load_file,
        solar_kw,
        battery_kwh,
        battery_charge_kw,
        battery_discharge_kw
    ):
        # Initialize models
        self.load_model = LoadModel(load_source="real", file_path=load_file)

        self.solar_model = SolarModel(
            solar_capacity_kw=solar_kw
        )

        self.battery_model = BatteryModel(
            capacity_kwh=battery_kwh,
            max_charge_kw=battery_charge_kw,
            max_discharge_kw=battery_discharge_kw
        )

        self.energy_flow = EnergyFlow(
            self.load_model,
            self.solar_model,
            self.battery_model
        )

    # --------------------------------------------------
    def run(self, hours):
        """
        Run full system simulation
        """
        self.energy_flow.simulate(hours)
        self.results = self.energy_flow.get_results()

    # --------------------------------------------------
    def export_results(self, output_csv):
        """
        Export simulation results to CSV. Creates output directory if needed.
        """
        df = pd.DataFrame(self.results)
        output_dir = os.path.dirname(output_csv)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        df.to_csv(output_csv, index=False)

    # --------------------------------------------------
    def summary(self):
        """
        Return key system metrics
        """
        total_load = sum(self.results["load"])
        total_grid = sum(self.results["grid"])
        total_solar_used = sum(self.results["solar"])
        avg_soc = sum(self.results["soc"]) / len(self.results["soc"])

        return {
            "Total Load (kWh)": round(total_load, 2),
            "Grid Energy (kWh)": round(total_grid, 2),
            "Solar Used (kWh)": round(total_solar_used, 2),
            "Grid Dependency (%)": round(
                (total_grid / total_load) * 100, 2
            ),
            "Average Battery SoC (%)": round(avg_soc, 2)
        }
# Example usage:
# simulator = HybridSystemSimulator(
#     load_file="outputs/cleaned_hourly.csv",
#     solar_kw=5,
#     battery_kwh=10,
#     battery_charge_kw=3,
#     battery_discharge_kw=3
# )
# simulator.run(hours=48)
# print(simulator.summary())
# simulator.export_results("outputs/simulation_results.csv")