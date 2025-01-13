import tkinter as tk
from tkinter import ttk
from datetime import datetime
from Download_value import fetch_power_data
import subprocess
import threading

# URL API
API_URL = "http://192.168.1.140:8085/data.json"

# Stała dla kosztów energii
COST_PER_KWH = 1.29
FILE_PATH = "energy(do_not_delete).csv"  # Ścieżka do pliku CSV

class EnergyMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy Monitor")

        # Zmienne do przechowywania danych
        self.cpu_current_power = tk.StringVar(value="0.000 W")
        self.total_energy_wh_cpu = 0.0
        self.total_energy_kwh_cpu = 0.0
        self.total_cost_cpu = 0.0
        self.total_energy_wh_display_cpu = tk.StringVar(value="0.000 Wh")
        self.total_energy_kwh_display_cpu = tk.StringVar(value="0.000 kWh")
        self.total_cost_display_cpu = tk.StringVar(value="0.00 zł")
        self.gpu_current_power = tk.StringVar(value="0.000 W")
        self.total_energy_wh_gpu = 0.0
        self.total_energy_kwh_gpu = 0.0
        self.total_cost_gpu = 0.0
        self.total_energy_wh_display_gpu = tk.StringVar(value="0.000 Wh")
        self.total_energy_kwh_display_gpu = tk.StringVar(value="0.000 kWh")
        self.total_cost_display_gpu = tk.StringVar(value="0.00 zł")
        self.other_current_power = tk.StringVar(value="0.000 W")
        self.total_energy_wh_other = 0.0
        self.total_energy_kwh_other = 0.0
        self.total_cost_other = 0.0
        self.total_energy_wh_display_other = tk.StringVar(value="0.000 Wh")
        self.total_energy_kwh_display_other = tk.StringVar(value="0.000 kWh")
        self.total_cost_display_other = tk.StringVar(value="0.00 zł")
        self.all_current_power = tk.StringVar(value="0.000 W")
        self.total_energy_wh_all = 0.0
        self.total_energy_kwh_all = 0.0
        self.total_cost_all = 0.0
        self.total_energy_wh_display_all = tk.StringVar(value="0.000 Wh")
        self.total_energy_kwh_display_all = tk.StringVar(value="0.000 kWh")
        self.total_cost_display_all = tk.StringVar(value="0.00 zł")
        self.api_status = tk.StringVar(value="")
        self.elapsed_time = tk.StringVar(value="00:00:00")
        self.session_energy_today = 0.0
        self.session_cost_today = 0.0
        self.session_energy_month = 0.0
        self.session_cost_month = 0.0
        self.session_energy_year = 0.0
        self.session_cost_year = 0.0

        # Zmienne sesji
        self.session_active = False
        self.session_start_time = None
        self.session_energy_wh_cpu = 0.0
        self.session_energy_wh_gpu = 0.0
        self.session_energy_wh_other = 0.0
        self.session_energy_wh_total = 0.0
        self.session_log = []
        self.session_number = 0

        # Historia mocy dla detekcji sesji
        self.power_history = [0.0] * 3

        # Inicjalizacja czasu
        self.start_time = datetime.now()

        # Interfejs graficzny
        self.create_widgets()

        # Start odświeżania danych
        self.running = True
        self.update_data()

        # Zmiana: Uruchamiamy wątek po załadowaniu aplikacji
        self.start_background_thread()

    def start_csv(self):
        subprocess.run(['python', 'CSV.py'])

    def start_background_thread(self):
        watek = threading.Thread(target=self.start_csv)  # Używamy self.start_csv zamiast start_csv
        watek.daemon = True  # Ustawienie wątku jako demona, aby zakończył się z aplikacją
        watek.start()

    def create_widgets(self):
        # Ustawienie wagi dla siatki (grid)
        for i in range(14):  # Zakładamy 14 wierszy
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(3):  # Zakładamy 3 kolumny
            self.root.grid_columnconfigure(j, weight=1)

        # Napis "PC" na środku
        ttk.Label(self.root, text="PC", anchor="center").grid(row=0, column=0, columnspan=3, padx=0, pady=10,
                                                              sticky="nsew")

        # Etykiety i wartości dla CPU i GPU
        ttk.Label(self.root, text="Aktualny pomiar CPU:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, textvariable=self.cpu_current_power).grid(row=2, column=0, padx=50, pady=10, sticky="e")

        ttk.Label(self.root, text="Aktualny pomiar GPU:").grid(row=1, column=1, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, textvariable=self.gpu_current_power).grid(row=2, column=1, padx=50, pady=10, sticky="e")

        # Etykiety dla zużycia energii i kosztów
        ttk.Label(self.root, text="Zużycie energii CPU (Wh):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, textvariable=self.total_energy_wh_display_cpu).grid(row=4, column=0, padx=10, pady=10,
                                                                                 sticky="e")

        ttk.Label(self.root, text="Zużycie energii GPU (Wh):").grid(row=3, column=1, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, textvariable=self.total_energy_wh_display_gpu).grid(row=4, column=1, padx=10, pady=10,
                                                                                 sticky="e")

        ttk.Label(self.root, text="Koszt CPU (zł):").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, textvariable=self.total_cost_display_cpu).grid(row=6, column=0, padx=10, pady=10,
                                                                            sticky="e")

        ttk.Label(self.root, text="Koszt GPU (zł):").grid(row=5, column=1, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, textvariable=self.total_cost_display_gpu).grid(row=6, column=1, padx=10, pady=10,
                                                                            sticky="e")

        # Informacje o sesji na środku
        self.session_info = tk.StringVar(value="Sesja: 0, Czas: 00:00:00, Zużycie: 0.000 Wh, Koszt: 0.00 zł")
        ttk.Label(self.root, textvariable=self.session_info, anchor="center").grid(row=8, column=0, columnspan=3,
                                                                                   padx=10, pady=10, sticky="nsew")

        # Wyświetlanie zużycia dziennego, miesięcznego i rocznego
        self.daily_energy_display = tk.StringVar(value="Zużycie dzienne: 0.000 Wh 0.000 kWh, 0.00 zł")
        self.monthly_energy_display = tk.StringVar(value="Zużycie miesięczne: 0.000 kWh 0.00 zł")
        self.yearly_energy_display = tk.StringVar(value="Zużycie roczne: 0.000 kWh 0.00 zł")

        ttk.Label(self.root, textvariable=self.daily_energy_display, anchor="center").grid(row=9, column=0,
                                                                                           columnspan=3, padx=10,
                                                                                           pady=10, sticky="nsew")
        ttk.Label(self.root, textvariable=self.monthly_energy_display, anchor="center").grid(row=10, column=0,
                                                                                             columnspan=3, padx=10,
                                                                                             pady=10, sticky="nsew")
        ttk.Label(self.root, textvariable=self.yearly_energy_display, anchor="center").grid(row=11, column=0,
                                                                                            columnspan=3, padx=10,
                                                                                            pady=10, sticky="nsew")

        # Status API na środku
        ttk.Label(self.root, textvariable=self.api_status, foreground="red", anchor="center").grid(row=12, column=0,
                                                                                                   columnspan=3,
                                                                                                   padx=10, pady=10,
                                                                                                   sticky="nsew")

        ttk.Label(self.root, text="Total:").grid(row=13, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, textvariable=self.total_energy_wh_display_all).grid(row=13, column=1, padx=50, pady=10, sticky="e")
        # Przycisk historii
        #ttk.Button(self.root, text="Historia", command=self.show_history).grid(row=13, column=0, columnspan=3, padx=10,
        #                                                                       pady=10, sticky="nsew")

    def fetch_data(self):
        cpu_value, gpu_value, other_value = fetch_power_data()

        if cpu_value + gpu_value + other_value <= 0:
            self.api_status.set("Pc is Off")
        else:
            self.api_status.set("Połączono")
        return cpu_value, gpu_value, other_value

    def update_data(self):
        """Aktualizuje dane co sekundę """
        if not self.running:
            return


        cpu_value, gpu_value, other_value = self.fetch_data()  # Rozpakowujemy krotkę
        total_power_value = cpu_value + gpu_value + other_value
        self.cpu_current_power.set(f"{cpu_value:.3f} W")
        self.gpu_current_power.set(f"{gpu_value:.3f} W")
        self.other_current_power.set(f"{gpu_value:.3f} W")
        self.all_current_power.set(f"{total_power_value:.3f} W")
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

        self.total_energy_wh_display_cpu.set(f"{self.total_energy_wh_cpu:.3f} Wh")
        self.total_energy_wh_display_gpu.set(f"{self.total_energy_wh_gpu:.3f} Wh")
        self.total_energy_wh_display_other.set(f"{self.total_energy_wh_other:.3f} Wh")
        self.total_energy_wh_display_all.set(f"{self.total_energy_wh_all:.3f} Wh")
        self.total_energy_kwh_display_cpu.set(f"{self.total_energy_kwh_cpu:.2f} kWh")
        self.total_energy_kwh_display_gpu.set(f"{self.total_energy_kwh_gpu:.2f} kWh")
        self.total_energy_kwh_display_other.set(f"{self.total_energy_kwh_other:.2f} kWh")
        self.total_energy_kwh_display_all.set(f"{self.total_energy_kwh_all:.2f} kWh")
        self.total_cost_display_cpu.set(f"{self.total_cost_cpu:.2f} zł")
        self.total_cost_display_gpu.set(f"{self.total_cost_gpu:.2f} zł")
        self.total_cost_display_other.set(f"{self.total_cost_other:.2f} zł")
        self.total_cost_display_all.set(f"{self.total_cost_all:.2f} zł")
        self.update_elapsed_time()

        self.root.after(1000, self.update_data)  # Aktualizacja co 1000 ms (1 sekunda)

    def update_elapsed_time(self):
        """Aktualizuje czas działania aplikacji."""
        elapsed = datetime.now() - self.start_time
        self.elapsed_time.set(str(elapsed).split('.')[0])


# Uruchamianie aplikacji
def main():
    root = tk.Tk()
    app = EnergyMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
