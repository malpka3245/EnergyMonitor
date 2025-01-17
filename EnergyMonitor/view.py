import pandas as pd
import calendar
from tkinter import ttk, Toplevel, messagebox, Canvas, StringVar
import json


class EnergyMonitorView:
    def __init__(self, root, controller):

        window_width = 400
        window_height = 550  # Zwiększenie wysokości okna, by pomieścić więcej elementów

        self.controller = controller
        self.root = root

        # Nowoczesne tło i czcionki
        self.root.configure(bg="#f4f4f9")  # Jasne tło
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(False, False)

        # Stylowanie dla całego okna
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10), background="#f4f4f9", foreground="#333333")
        style.configure("TEntry", font=("Segoe UI", 10), padding=5)
        style.configure("TButton", font=("Segoe UI", 10), padding=8, relief="flat", background="#333333",
                        foreground="white")
        style.map("TButton", background=[("active", "#444444")])

        self.df = None
        self.cost_per_kwh, self.api_ip, self.api_port = self.load_settings()
        self.cost_changed = False

        # Usunięcie settings_frame i values_frame
        self.restart_warning = ttk.Label(self.root, text="teeeeeeeeeeeeeeeest", foreground="red", font=("Segoe UI", 10))
        self.restart_warning.grid(row=1, column=0, sticky="w", padx=20, pady=10)

        # Cena za kWh, API IP, API Port w jednym rzędzie
        cost_label = ttk.Label(self.root, text="Cena za kWh:")
        cost_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        self.cost_entry_var = StringVar(value=str(self.cost_per_kwh))
        self.cost_entry = ttk.Entry(self.root, textvariable=self.cost_entry_var, width=15)
        self.cost_entry.grid(row=1, column=0, padx=20, pady=5)
        self.cost_entry.bind("<Return>", lambda event: self.update_settings(new_cost=self.cost_entry_var.get()))

        ip_label = ttk.Label(self.root, text="API IP:")
        ip_label.grid(row=0, column=1, padx=20, pady=5, sticky="w")

        self.ip_entry_var = StringVar(value=self.api_ip)
        self.ip_entry = ttk.Entry(self.root, textvariable=self.ip_entry_var, width=15)
        self.ip_entry.grid(row=1, column=1, padx=20, pady=5)
        self.ip_entry.bind("<Return>", lambda event: self.update_settings(new_api_ip=self.ip_entry_var.get()))

        port_label = ttk.Label(self.root, text="API Port:")
        port_label.grid(row=0, column=2, padx=20, pady=5, sticky="w")

        self.port_entry_var = StringVar(value=str(self.api_port))
        self.port_entry = ttk.Entry(self.root, textvariable=self.port_entry_var, width=15)
        self.port_entry.grid(row=1, column=2, padx=20, pady=5)
        self.port_entry.bind("<Return>", lambda event: self.update_settings(new_api_port=self.port_entry_var.get()))

        # Sekcja z wartościami Power
        power_frame = ttk.Frame(self.root, relief="solid", padding=10)
        power_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

        self.cpu_label = ttk.Label(power_frame, text=f"CPU Power: {self.controller.monitor.cpu_value} W")
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.gpu_label = ttk.Label(power_frame, text=f"GPU Power: {self.controller.monitor.gpu_value} W")
        self.gpu_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.other_label = ttk.Label(power_frame, text=f"Other Power: {self.controller.monitor.other_value} W")
        self.other_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.total_label = ttk.Label(power_frame, text=f"Total Power: {self.controller.monitor.total_power_value} W")
        self.total_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.cost_label = ttk.Label(power_frame, text=f"Cost: {self.controller.monitor.total_cost_all} PLN")
        self.cost_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Sekcja z dodatkowymi informacjami
        info_frame = ttk.Frame(self.root, relief="solid", padding=10)
        info_frame.grid(row=9, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

        self.session_label = ttk.Label(info_frame, text=f"Session Number: {self.controller.session}")
        self.session_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.duration_label = ttk.Label(info_frame, text=f"Session Duration: {self.controller.format_duration()}")
        self.duration_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.energy_wh_label = ttk.Label(info_frame,
                                         text=f"Total Energy (Wh): {self.controller.monitor.total_energy_wh_all}")
        self.energy_wh_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.energy_kwh_label = ttk.Label(info_frame,
                                          text=f"Total Energy (kWh): {self.controller.monitor.total_energy_kwh_all}")
        self.energy_kwh_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Przeniesienie napisu "PC is Off" na górę, nad ramki
        self.api_label = ttk.Label(self.root, text="PC is Off", foreground="gray", font=("Segoe UI", 10, "italic"))
        self.api_label.grid(row=3, column=1, columnspan=3, padx=33, pady=5, sticky="nsew")

        # Przycisk "History" z poprawionym wyglądem
        history_button = ttk.Button(self.root, text="History", command=self.open_history)
        history_button.grid(row=14, column=0, columnspan=3, pady=20)

        # Stylizacja przycisku "History"
        history_button.configure(width=20, style="TButton")

        # Wyrównanie kolumn
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def open_history(self):
        new_window = Toplevel(self.root)
        new_window.title("Historia")

        width = 1045
        height = 600
        new_window.geometry(f"{width}x{height}")

        new_window.resizable(False, False)

        canvas = Canvas(new_window)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        history_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=history_frame, anchor="nw")

        self.df = pd.read_csv("logs.csv")

        self.df['energy_wh'] = self.df['energy_wh'].str.replace(" wh", "").astype(float)
        self.df['energy_kWh'] = self.df['energy_kWh'].str.replace(" kWh", "").astype(float)
        self.df['cost_pln'] = self.df['cost_pln'].str.replace(" zl", "").astype(float)
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        month_combobox = ttk.Combobox(history_frame, values=months, state="readonly")
        month_combobox.set('January')
        month_combobox.grid(row=0, column=0, padx=10, pady=10)

        day_combobox = ttk.Combobox(history_frame, state="readonly")
        day_combobox.grid(row=0, column=1, padx=10, pady=10)

        year_combobox = ttk.Combobox(history_frame, values=[str(year) for year in range(2000, 2031)], state="readonly")
        year_combobox.set('2025')
        year_combobox.grid(row=0, column=2, padx=10, pady=10)

        def update_days():
            selected_month = month_combobox.get()
            month_index = months.index(selected_month)
            _, num_days = calendar.monthrange(int(year_combobox.get()), month_index + 1)
            days = [str(day) for day in range(1, num_days + 1)]
            day_combobox['values'] = days
            day_combobox.set('1')

        month_combobox.bind("<<ComboboxSelected>>", lambda event: update_days())
        update_days()

        show_button = ttk.Button(history_frame, text="Pokaż sesje", command=lambda: self.show_sessions(month_combobox,
                                                                                                       year_combobox,
                                                                                                       day_combobox,
                                                                                                       history_frame,
                                                                                                       canvas))
        show_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.summary_label = ttk.Label(history_frame, text="")
        self.summary_label.grid(row=2, column=0, columnspan=3, pady=10)

        history_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        columns = ("Session", "Duration", "Energy (Wh)", "Energy (kWh)", "Cost (PLN)")
        tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def show_sessions(self, month_combobox, year_combobox, day_combobox, history_frame, canvas):
        try:
            selected_month = month_combobox.get()
            selected_year = year_combobox.get()
            selected_day = day_combobox.get()

            self.df['date'] = pd.to_datetime(self.df['date'])
            df_filtered = self.df[(self.df['date'].dt.year == int(selected_year)) &
                                  (self.df['date'].dt.month == month_combobox.current() + 1) &
                                  (self.df['date'].dt.day == int(selected_day))]

            total_sessions = len(df_filtered)
            total_energy_wh = round(df_filtered['energy_wh'].sum(), 3)
            total_energy_kwh = round(total_energy_wh / 1000, 3)
            total_cost = round(total_energy_kwh * self.controller.monitor.cost_per_kwh, 3)

            monthly_data = self.df[(self.df['date'].dt.year == int(selected_year)) &
                                   (self.df['date'].dt.month == month_combobox.current() + 1)]
            monthly_sessions = len(monthly_data)
            monthly_energy_wh = round(monthly_data['energy_wh'].sum(), 3)
            monthly_energy_kwh = round(monthly_energy_wh / 1000, 3)
            monthly_cost = round(monthly_energy_kwh * self.controller.monitor.cost_per_kwh, 3)

            yearly_data = self.df[self.df['date'].dt.year == int(selected_year)]
            yearly_sessions = len(yearly_data)
            yearly_energy_wh = round(yearly_data['energy_wh'].sum(), 3)
            yearly_energy_kwh = round(yearly_energy_wh / 1000, 3)
            yearly_cost = round(yearly_energy_kwh * self.controller.monitor.cost_per_kwh, 3)

            self.summary_label.config(
                text=f"Sessions: {total_sessions}\nEnergy (Wh): {total_energy_wh} Wh\nEnergy (kWh): {total_energy_kwh} kWh\nCost: {total_cost} PLN")

            columns = ("Session", "Duration", "Energy (Wh)", "Energy (kWh)", "Cost (PLN)")
            tree = ttk.Treeview(history_frame, columns=columns, show="headings")
            tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

            for col in columns:
                tree.heading(col, text=col)

            for index, row in df_filtered.iterrows():
                energy_kwh = round(row['energy_wh'] / 1000, 3)
                cost = round(energy_kwh * self.controller.monitor.cost_per_kwh, 3)
                tree.insert("", "end",
                            values=(row['session'], row['duration'], round(row['energy_wh'], 3), energy_kwh, cost))

            monthly_summary = ttk.Label(history_frame, text=f"Month {selected_month}: Sessions: {monthly_sessions}, "
                                                            f"Wh: {monthly_energy_wh}, kWh: {monthly_energy_kwh}, Cost: {monthly_cost} PLN")
            monthly_summary.grid(row=4, column=0, columnspan=3, pady=10)

            yearly_summary = ttk.Label(history_frame, text=f"Year {selected_year}: Sessions: {yearly_sessions}, "
                                                           f"Wh: {yearly_energy_wh}, kWh: {yearly_energy_kwh}, Cost: {yearly_cost} PLN")
            yearly_summary.grid(row=5, column=0, columnspan=3, pady=10)

            history_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def receive_data(self):
        if self.controller.monitor.cpu_value + self.controller.monitor.gpu_value + self.controller.monitor.other_value <= 0:
            self.api_label.config(text="PC is Off", foreground="red")
        else:
            self.api_label.config(text="Połączono", foreground="green")

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                cost_per_kwh = settings.get("cost_per_kwh", 0.0)
                api_ip = settings.get("api_ip", "localhost")
                api_port = settings.get("api_port", 8080)
                return cost_per_kwh, api_ip, api_port
        except (FileNotFoundError, json.JSONDecodeError):
            return 0.0, "localhost", 8080

    def save_settings(self, cost_per_kwh=None, api_ip=None, api_port=None):
        try:
            # Load existing settings
            with open("settings.json", "r") as file:
                settings = json.load(file)

            # Update settings with provided values
            if cost_per_kwh is not None:
                settings["cost_per_kwh"] = cost_per_kwh
            if api_ip is not None:
                settings["api_ip"] = api_ip
            if api_port is not None:
                settings["api_port"] = api_port

            # Save updated settings
            with open("settings.json", "w") as file:
                json.dump(settings, file, indent=4)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save to settings.json: {str(e)}")

    def update_settings(self, new_cost=None, new_api_ip=None, new_api_port=None):
        try:
            updates_made = False

            if new_cost is not None:
                new_cost_float = float(new_cost)
                if new_cost_float != self.cost_per_kwh:
                    self.cost_per_kwh = new_cost_float
                    updates_made = True

            if new_api_ip is not None and new_api_ip != self.api_ip:
                self.api_ip = new_api_ip
                updates_made = True

            if new_api_port is not None:
                new_api_port_int = int(new_api_port)
                if new_api_port_int != self.api_port:
                    self.api_port = new_api_port_int
                    updates_made = True

            if updates_made:
                self.save_settings(cost_per_kwh=self.cost_per_kwh, api_ip=self.api_ip, api_port=self.api_port)
                self.restart_warning.config(
                    text="Zapisano zmiany. Uruchom ponownie aplikację, aby wprowadzić zmiany.",
                    foreground="red"
                )
            else:
                self.restart_warning.config(text="", foreground="")

        except ValueError:
            messagebox.showerror("Error", "Proszę wprowadzić poprawne wartości dla ustawień.")

    def draw(self):
        self.cpu_label.config(text=f"CPU Power: {self.controller.monitor.cpu_value} W")
        self.gpu_label.config(text=f"GPU Power: {self.controller.monitor.gpu_value} W")
        self.other_label.config(text=f"Other Power: {self.controller.monitor.other_value} W")
        self.duration_label.config(text=f"Session Duration: {self.controller.format_duration()}")
        self.energy_wh_label.config(text=f"Total Energy (Wh): {round(self.controller.monitor.total_energy_wh_all, 3)}")
        self.energy_kwh_label.config(
            text=f"Total Energy (kWh): {round(self.controller.monitor.total_energy_kwh_all, 2)}")
        self.cost_label.config(text=f"Total Cost (PLN): {round(self.controller.monitor.total_cost_all, 2)} PLN")
        self.session_label.config(text=f"Session Number: {self.controller.session}")
        self.total_label.config(text=f"Total Power: {round(self.controller.monitor.total_power_value, 2)} W")

    def update(self):
        self.draw()
        self.receive_data()
