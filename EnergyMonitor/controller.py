from datetime import datetime


class EnergyMonitorController:
    def __init__(self, ohmc, monitor, logger, session, settings):
        self.ohmc = ohmc
        self.logger = logger
        self.monitor = monitor
        self.session = session
        self.settings = settings
        self.view = None
        self.elapsed_time = 0

    def get_data(self):
        if self.settings.api_ip != self.ohmc.api_ip or self.settings.api_port != self.ohmc.api_port:
            self.ohmc.update_api_url(self.settings.api_ip, self.settings.api_port)
        cpu_value, gpu_value, other_value = self.ohmc.fetch_power_data()
        self.monitor.update_data(cpu_value, gpu_value, other_value, self.settings)
        data = self.monitor.get_logger_data()
        data["session"] = self.session
        data["date"] = datetime.now().strftime("%Y-%m-%d")
        data["duration"] = self.format_duration()
        self.logger.write_session_to_csv(data)

    def update_elapsed_time(self, elapsed_time):
        self.elapsed_time += elapsed_time
        self.notify()

    def format_duration(self):
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        return f"{minutes} minut{'a' if minutes == 1 else ''} {seconds} sekund"

    def update_settings(self, api_ip=None, api_port=None, cost_per_kwh=None):
        """Aktualizowanie ustawień i zapisanie ich."""
        if api_ip is not None:
            self.settings.api_ip = api_ip
        if api_port is not None:
            self.settings.api_port = api_port
        if cost_per_kwh is not None:
            self.settings.cost_per_kwh = cost_per_kwh

        # Zapisanie nowych ustawień
        self.settings.save()
        print("Settings updated and saved.")

    def attach_view(self, view):
        self.view = view

    def notify(self):
        self.view.update()
