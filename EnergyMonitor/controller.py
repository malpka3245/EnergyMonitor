from datetime import datetime


class EnergyMonitorController:
    def __init__(self, ohmc, monitor, logger, session):
        self.ohmc = ohmc
        self.logger = logger
        self.monitor = monitor
        self.session = session
        self.view = None
        self.elapsed_time = 0

    def get_data(self):
        cpu_value, gpu_value, other_value = self.ohmc.fetch_power_data()
        self.monitor.update_data(cpu_value, gpu_value, other_value)
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

    def attach_view(self, view):
        self.view = view

    def notify(self):
        self.view.update()
