import json
import os


class Settings:
    def __init__(self, config_file="settings.json"):
        self.config_file = config_file
        self.api_ip = "localhost"
        self.api_port = 8085
        self.cost_per_kwh = 0

        # Sprawdź, czy plik konfiguracyjny istnieje
        if os.path.exists(self.config_file):
            self.load()
        else:
            self.save()

    def load(self):
        """Załaduj ustawienia z pliku JSON."""
        with open(self.config_file, "r") as file:
            data = json.load(file)
            self.api_ip = data.get("api_ip", self.api_ip)
            self.api_port = data.get("api_port", self.api_port)
            self.cost_per_kwh = data.get("cost_per_kwh", self.cost_per_kwh)

    def save(self):
        """Zapisz aktualne ustawienia do pliku JSON."""
        data = {
            "api_ip": self.api_ip,
            "api_port": self.api_port,
            "cost_per_kwh": self.cost_per_kwh
        }
        with open(self.config_file, "w") as file:
            json.dump(data, file, indent=4)

    def update(self, api_ip=None, api_port=None, cost_per_kwh=None):
        """Aktualizuj ustawienia i zapisz je."""
        if api_ip is not None:
            self.api_ip = api_ip
        if api_port is not None:
            self.api_port = api_port
        if cost_per_kwh is not None:
            self.cost_per_kwh = cost_per_kwh

        self.save()
