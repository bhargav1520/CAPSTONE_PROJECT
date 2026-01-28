# battery_model.py
# This module handles the modeling of battery storage for the simulation engine.

class BatteryModel:
    """
    Battery Energy Storage Model
    ----------------------------
    Models charging, discharging, and state of charge (SoC)
    """

    def __init__(
        self,
        capacity_kwh,
        max_charge_kw,
        max_discharge_kw,
        charge_efficiency=0.95,
        discharge_efficiency=0.95,
        initial_soc=0.5
    ):
        """
        Parameters
        ----------
        capacity_kwh : float
            Total battery capacity (kWh)
        max_charge_kw : float
            Maximum charging power (kW)
        max_discharge_kw : float
            Maximum discharging power (kW)
        charge_efficiency : float
            Charging efficiency (0–1)
        discharge_efficiency : float
            Discharging efficiency (0–1)
        initial_soc : float
            Initial state of charge (0–1)
        """
        self.capacity_kwh = capacity_kwh
        self.max_charge_kw = max_charge_kw
        self.max_discharge_kw = max_discharge_kw
        self.charge_efficiency = charge_efficiency
        self.discharge_efficiency = discharge_efficiency

        self.soc = initial_soc * capacity_kwh

    # --------------------------------------------------
    def charge(self, energy_kwh):
        """
        Charge the battery

        Parameters
        ----------
        energy_kwh : float
            Energy available for charging (kWh)

        Returns
        -------
        float
            Energy actually stored (kWh)
        """
        energy_kwh = min(energy_kwh, self.max_charge_kw)

        available_capacity = self.capacity_kwh - self.soc

        charged = min(
            energy_kwh * self.charge_efficiency,
            available_capacity
        )

        self.soc += charged
        return charged

    # --------------------------------------------------
    def discharge(self, energy_kwh):
        """
        Discharge the battery

        Parameters
        ----------
        energy_kwh : float
            Energy requested (kWh)

        Returns
        -------
        float
            Energy supplied (kWh)
        """
        energy_kwh = min(energy_kwh, self.max_discharge_kw)

        available_energy = self.soc

        discharged = min(
            energy_kwh / self.discharge_efficiency,
            available_energy
        )

        self.soc -= discharged
        return discharged * self.discharge_efficiency

    # --------------------------------------------------
    def get_soc(self):
        """
        Returns current State of Charge (SoC) in kWh
        """
        return self.soc

    # --------------------------------------------------
    def get_soc_percent(self):
        """
        Returns State of Charge as percentage
        """
        return (self.soc / self.capacity_kwh) * 100
