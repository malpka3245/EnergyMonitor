import csv
import os
class CsvController:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_last_session(self):
        if not os.path.exists(self.file_path):
            return None, 0

        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            if not rows:
                return None, 0

            last_row = rows[-1]
            last_date = last_row["date"]
            last_session = int(last_row["session"])
            return last_date, last_session
    def write_session_to_csv(self, data):
        file_exists = os.path.exists(self.file_path)
        temp_rows = []

        if file_exists:
            with open(self.file_path, "r") as file:
                reader = csv.DictReader(file)
                temp_rows = list(reader)

        with open(self.file_path, "w", newline="") as file:
            writer = csv.DictWriter(file,
                                    fieldnames=["date", "session", "duration", "energy_wh", "energy_kWh", "cost_pln"])
            writer.writeheader()

            updated = False
            for row in temp_rows:
                if row["date"] == data["date"] and int(row["session"]) == data["session"]:
                    writer.writerow(data)
                    updated = True
                else:
                    writer.writerow(row)

            if not updated:
                writer.writerow(data)