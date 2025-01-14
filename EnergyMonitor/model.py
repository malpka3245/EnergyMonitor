from datetime import datetime
COST_PER_KWH = 1.29
class EnergyMonitor:
    def __init__(self):

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

        self.power_history = [0.0] * 3

        # Inicjalizacja czasu
        self.start_time = datetime.now()

    # def recive_data(self, cpu_value, gpu_value, other_value):
    #     if cpu_value + gpu_value + other_value <= 0:
    #         self.api_status.set("Pc is Off")
    #     else:
    #         self.api_status.set("Połączono")
    #     return cpu_value, gpu_value, other_value

    def update_data(self, cpu_value, gpu_value, other_value):
        total_power_value = cpu_value + gpu_value + other_value
        self.total_energy_wh_cpu += cpu_value / 3600  # Używamy wartości CPU do obliczeń
        self.total_energy_wh_gpu += gpu_value / 3600  # Używamy wartości GPU do obliczeń
        self.total_energy_wh_other += other_value / 3600  # Używamy wartości other do obliczeń
        self.total_energy_wh_all += total_power_value / 3600  # Używamy wartości total do obliczeń
        self.total_energy_kwh_cpu += self.total_energy_wh_cpu / 1000  # Używamy wartości CPU do obliczeń
        self.total_energy_kwh_gpu += self.total_energy_wh_gpu / 1000  # Używamy wartości GPU do obliczeń
        self.total_energy_kwh_other += self.total_energy_wh_other / 1000  # Używamy wartości other do obliczeń
        self.total_energy_kwh_all += self.total_energy_wh_all / 1000  # Używamy wartości total do obliczeń
        self.total_cost_cpu = (self.total_energy_wh_cpu / 1000) * COST_PER_KWH
        self.total_cost_gpu = (self.total_energy_wh_gpu / 1000) * COST_PER_KWH
        self.total_cost_other = (self.total_energy_wh_other / 1000) * COST_PER_KWH
        self.total_cost_all = (self.total_energy_wh_all / 1000) * COST_PER_KWH
        #self.update_elapsed_time()
        #self.root.after(1000, self.update_data)  # Aktualizacja co 1000 ms (1 sekunda)

    def get_logger_data(self):
        return {
                "energy_wh": f"{round(self.total_energy_wh_all, 3)} wh",
                "energy_kWh": f"{round(self.total_energy_kwh_all, 2)} kWh",
                "cost_pln": f"{round(self.total_cost_all, 2)} zł",
        }

    # def update_elapsed_time(self):
    #     """Aktualizuje czas działania aplikacji."""
    #     elapsed = datetime.now() - self.start_time
    #     self.elapsed_time.set(str(elapsed).split('.')[0])
