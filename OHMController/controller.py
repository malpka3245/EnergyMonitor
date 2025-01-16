import requests

API_URL = "http://localhost:8085/data.json"


class OhmController:
    def find_power_values(self, node, parent_path=""):

        power_data = {}

        if isinstance(node, dict):
            # Zbuduj ścieżkę urządzenia
            current_path = f"{parent_path} > {node.get('Text', 'Unknown')}".strip(" > ")
            value = node.get("Value", "")
            if "W" in value:
                try:
                    numeric_value = float(value.split()[0].replace(",", "."))
                    device_type = self.categorize_device(current_path)

                    if device_type not in power_data or power_data[device_type][1] < numeric_value:
                        power_data[device_type] = (current_path, numeric_value)
                except ValueError:
                    pass
            for key, child in node.items():
                if isinstance(child, (list, dict)):
                    sub_data = self.find_power_values(child, current_path)
                    for device_type, value in sub_data.items():
                        if device_type not in power_data or power_data[device_type][1] < value[1]:
                            power_data[device_type] = value
        elif isinstance(node, list):
            for child in node:
                sub_data = self.find_power_values(child, parent_path)
                for device_type, value in sub_data.items():
                    if device_type not in power_data or power_data[device_type][1] < value[1]:
                        power_data[device_type] = value

        return power_data

    def categorize_device(self, path):
        path_lower = path.lower()
        if "cpu" in path_lower:
            return "CPU"
        elif "gpu" in path_lower or "graphics" in path_lower:
            return "GPU"
        else:
            return "Other"

    def fetch_power_data(self):
        try:
            response = requests.get(API_URL, timeout=1)
            if response.status_code == 200:
                data = response.json()
                max_power_values = self.find_power_values(data)
                cpu_value = max_power_values.get("CPU", (None, 0))[1]
                gpu_value = max_power_values.get("GPU", (None, 0))[1]
                other_value = max_power_values.get("Other", (None, 0))[1]

                return cpu_value, gpu_value, other_value
            else:
                print(f"Brak komunikacji z API. Kod odpowiedzi: {response.status_code}")
        except Exception:
            pass
        return 0.0, 0.0, 0.0
