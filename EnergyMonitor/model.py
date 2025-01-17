from datetime import datetime


class EnergyMonitor:
    def __init__(self):
        self.cost_per_kwh = 1.29
        self.api_ip = None
        self.api_port = None
        self.api_url = f"http://{self.api_ip}:{self.api_port}/data.json"

        self.total_energy_wh_cpu = 0.0
        self.total_energy_kwh_cpu = 0.0
        self.total_cost_cpu = 0.0
        self.total_energy_wh_gpu = 0.0
        self.total_energy_kwh_gpu = 0.0
        self.total_cost_gpu = 0.0
        self.total_energy_wh_other = 0.0
        self.total_energy_kwh_other = 0.0
        self.total_cost_other = 0.0
        self.total_energy_wh_all = 0.0
        self.total_energy_kwh_all = 0.0
        self.total_cost_all = 0.0
        self.session_energy_today = 0.0
        self.session_cost_today = 0.0
        self.session_energy_month = 0.0
        self.session_cost_month = 0.0
        self.session_energy_year = 0.0
        self.session_cost_year = 0.0

        self.session_active = False
        self.session_start_time = None
        self.session_energy_wh_cpu = 0.0
        self.session_energy_wh_gpu = 0.0
        self.session_energy_wh_other = 0.0
        self.session_energy_wh_total = 0.0
        self.session_log = []
        self.session_number = 0

        self.cpu_value = 0
        self.gpu_value = 0
        self.other_value = 0
        self.total_power_value = 0

        self.power_history = [0.0] * 3

        self.start_time = datetime.now()

    def update_data(self, cpu_value, gpu_value, other_value, settings):
        self.cost_per_kwh = settings.cost_per_kwh
        self.total_power_value = cpu_value + gpu_value + other_value
        self.cpu_value = cpu_value
        self.gpu_value = gpu_value
        self.other_value = other_value
        self.total_energy_wh_cpu += cpu_value / 3600
        self.total_energy_wh_gpu += gpu_value / 3600
        self.total_energy_wh_other += other_value / 3600
        self.total_energy_wh_all += self.total_power_value / 3600
        self.total_energy_kwh_cpu = self.total_energy_wh_cpu / 1000
        self.total_energy_kwh_gpu = self.total_energy_wh_gpu / 1000
        self.total_energy_kwh_other = self.total_energy_wh_other / 1000
        self.total_energy_kwh_all = self.total_energy_wh_all / 1000
        self.total_cost_cpu = (self.total_energy_wh_cpu / 1000) * self.cost_per_kwh
        self.total_cost_gpu = (self.total_energy_wh_gpu / 1000) * self.cost_per_kwh
        self.total_cost_other = (self.total_energy_wh_other / 1000) * self.cost_per_kwh
        self.total_cost_all = (self.total_energy_wh_all / 1000) * self.cost_per_kwh

    def get_logger_data(self):
        return {
                "energy_wh": f"{round(self.total_energy_wh_all, 3)} wh",
                "energy_kWh": f"{round(self.total_energy_kwh_all, 2)} kWh",
                "cost_pln": f"{round(self.total_cost_all, 2)} zl",
        }
