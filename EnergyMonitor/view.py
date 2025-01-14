import tkinter as tk
from tkinter import ttk


class EnergyMonitorView:
    def __init__(self, root, energy_monitor_controller):
        self.root = root
        self.energy_monitor_controller = energy_monitor_controller

        self.root.title("Energy Monitor")
        self.root.geometry("400x400")

        # Etykiety do wyświetlania mocy CPU, GPU, Other i Total
        self.cpu_label = ttk.Label(self.root, text="CPU Power: 0 W")
        self.cpu_label.pack(pady=10)

        self.gpu_label = ttk.Label(self.root, text="GPU Power: 0 W")
        self.gpu_label.pack(pady=10)

        self.other_label = ttk.Label(self.root, text="Other Power: 0 W")
        self.other_label.pack(pady=10)

        self.total_label = ttk.Label(self.root, text="Total Power: 0 W")
        self.total_label.pack(pady=10)

        # Etykiety do wyświetlania numeru sesji i czasu trwania
        self.session_label = ttk.Label(self.root, text="Session Number: 0")
        self.session_label.pack(pady=10)

        self.duration_label = ttk.Label(self.root, text="Session Duration: 0 s")
        self.duration_label.pack(pady=10)

        # Etykiety do wyników obliczeń
        self.energy_wh_label = ttk.Label(self.root, text="Total Energy (Wh): 0")
        self.energy_wh_label.pack(pady=10)

        self.energy_kwh_label = ttk.Label(self.root, text="Total Energy (kWh): 0")
        self.energy_kwh_label.pack(pady=10)

        self.cost_label = ttk.Label(self.root, text="Total Cost (PLN): 0 PLN")
        self.cost_label.pack(pady=10)

        # Przycisk do aktualizacji danych
        self.update_button = ttk.Button(self.root, text="Update Data", command=self.update_data)
        self.update_button.pack(pady=20)

        # Ustawienie mechanizmu automatycznego odświeżania co 1 sekundę
        self.refresh_data()

    def refresh_data(self):

        self.update_data()
        self.root.after(1000, self.refresh_data)  # Odśwież co 1000 ms (1 sekunda)

    def update_data(self):

        # Pobieranie danych
        cpu_value, gpu_value, other_value = self.energy_monitor_controller.ohmc.fetch_power_data()  # Zmieniono na ohmc
        total_value = cpu_value + gpu_value + other_value

        # Zmieniliśmy na logger zamiast csv_controller
        session_data = self.energy_monitor_controller.logger.load_last_session()
        session_number, session_duration = session_data

        # Wyniki obliczeń (zużycie energii, koszt)
        energy_wh_all = self.energy_monitor_controller.monitor.total_energy_wh_all
        energy_kwh_all = self.energy_monitor_controller.monitor.total_energy_kwh_all
        cost_all = self.energy_monitor_controller.monitor.total_cost_all

        # Aktualizacja etykiet
        self.cpu_label.config(text=f"CPU Power: {cpu_value:.2f} W")
        self.gpu_label.config(text=f"GPU Power: {gpu_value:.2f} W")
        self.other_label.config(text=f"Other Power: {other_value:.2f} W")
        self.total_label.config(text=f"Total Power: {total_value:.2f} W")

        self.session_label.config(text=f"Session Number: {session_number}")
        self.duration_label.config(text=f"Session Duration: {session_duration} s")

        self.energy_wh_label.config(text=f"Total Energy (Wh): {energy_wh_all:.2f}")
        self.energy_kwh_label.config(text=f"Total Energy (kWh): {energy_kwh_all:.2f}")
        self.cost_label.config(text=f"Total Cost (PLN): {cost_all:.2f} PLN")


