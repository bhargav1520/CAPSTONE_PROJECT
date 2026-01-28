# energy_flow.py
# This module handles the energy flow logic for the simulation engine.

class EnergyFlow:
    """
    Energy Flow Controller
    ----------------------
    Handles hour-by-hour power flow between
    Solar, Battery, Load, and Grid
    """

    def __init__(self, load_model, solar_model, battery_model):
        """
        Parameters
        ----------
        load_model : LoadModel
        solar_model : SolarModel
        battery_model : BatteryModel
        """
        self.load_model = load_model
        self.solar_model = solar_model
        self.battery_model = battery_model

        # Logs
        self.results = {
            "load": [],
            "solar": [],
            "battery_charge": [],
            "battery_discharge": [],
            "grid": [],
            "soc": []
        }

    # --------------------------------------------------
    def simulate(self, hours):
        """
        Run energy flow simulation

        Parameters
        ----------
        hours : int
            Number of hours to simulate
        """
        for h in range(hours):
            load = self.load_model.get_load(h)
            solar = self.solar_model.get_generation(h)

            remaining_load = load
            battery_charge = 0
            battery_discharge = 0
            grid = 0

            # 1️⃣ Solar → Load
            solar_to_load = min(solar, remaining_load)
            remaining_load -= solar_to_load
            solar -= solar_to_load

            # 2️⃣ Excess Solar → Battery
            if solar > 0:
                battery_charge = self.battery_model.charge(solar)

            # 3️⃣ Battery → Load
            if remaining_load > 0:
                battery_discharge = self.battery_model.discharge(
                    remaining_load
                )
                remaining_load -= battery_discharge

            # 4️⃣ Grid → Load
            if remaining_load > 0:
                grid = remaining_load

            # Store results
            self.results["load"].append(load)
            self.results["solar"].append(solar_to_load)
            self.results["battery_charge"].append(battery_charge)
            self.results["battery_discharge"].append(battery_discharge)
            self.results["grid"].append(grid)
            self.results["soc"].append(
                self.battery_model.get_soc_percent()
            )

    # --------------------------------------------------
    def get_results(self):
        """
        Returns simulation results dictionary
        """
        return self.results
    

# def calculate_energy_flow(load, solar, battery_model):
#     """
#     Calculate energy flow for a single timestep

#     Parameters
#     ----------
#     load : float
#         Load demand (kWh)
#     solar : float
#         Solar generation (kWh)
#     battery_model : BatteryModel
#         Battery model instance

#     Returns
#     -------
#     dict
#         Energy flow breakdown
#     """
#     remaining_load = load
#     battery_charge = 0
#     battery_discharge = 0
#     grid = 0

#     # 1️⃣ Solar → Load
#     solar_to_load = min(solar, remaining_load)
#     remaining_load -= solar_to_load
#     solar -= solar_to_load

#     # 2️⃣ Excess Solar → Battery
#     if solar > 0:
#         battery_charge = battery_model.charge(solar)

#     # 3️⃣ Battery → Load
#     if remaining_load > 0:
#         battery_discharge = battery_model.discharge(remaining_load)
#         remaining_load -= battery_discharge

#     # 4️⃣ Grid → Load
#     if remaining_load > 0:
#         grid = remaining_load

#     return {
#         "solar_to_load": solar_to_load,
#         "battery_charge": battery_charge,
#         "battery_discharge": battery_discharge,
#         "grid_used": grid
#     }
 