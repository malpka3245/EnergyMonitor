import csv
import os
import time
from datetime import datetime
from Download_value import fetch_power_data

# Ustawienia
FILE_PATH = "energy(do_not_delete).csv"  # Ścieżka do pliku CSV
COST_PER_KWH = 1.29

def fetch_data():
    cpu_value, gpu_value, other_value = fetch_power_data()
    total_energy_wh_all = (cpu_value + gpu_value + other_value) / 3600
    total_energy_kwh_all = total_energy_wh_all / 1000
    total_cost_all = total_energy_kwh_all / COST_PER_KWH
    print( round(cpu_value,3), round(gpu_value,3), round(other_value,3))
    return total_energy_wh_all, total_energy_kwh_all, total_cost_all


# Funkcje pomocnicze
def load_last_session(file_path):
    if not os.path.exists(file_path):
        return None, 0

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        if not rows:
            return None, 0

        last_row = rows[-1]
        last_date = last_row["date"]
        last_session = int(last_row["session"])
        return last_date, last_session

def write_to_csv(file_path, data):
    file_exists = os.path.exists(file_path)
    temp_rows = []

    if file_exists:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            temp_rows = list(reader)

    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "session", "duration", "energy_wh", "energy_kWh", "cost_pln"])
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


def format_duration(duration_seconds):
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60
    return f"{minutes} minut{'a' if minutes == 1 else ''} {seconds} sekund"

def csvv():
    last_date, last_session = load_last_session(FILE_PATH)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Nowa sesja
    session = last_session + 1 if last_date == current_date else 1
    session_start_time = time.time()

    # Zmienna do sumowania energii
    total_energy_wh_session = 0  # Energia całkowita w Wh w bieżącej sesji

    try:
        while True:
            current_time = time.time()
            duration_seconds = int(current_time - session_start_time)

            if duration_seconds == 0:
                continue

            # Pobierz bieżący odczyt energii
            current_energy_wh, _, _ = fetch_data()  # Bierzemy tylko bieżący odczyt Wh

            # Dodaj bieżący odczyt do sumy całkowitej
            total_energy_wh_session += current_energy_wh
            total_energy_kwh_all = total_energy_wh_session / 1000
            total_cost_all = total_energy_kwh_all * COST_PER_KWH

            duration_formatted = format_duration(duration_seconds)

            data = {
                "date": current_date,
                "session": session,
                "duration": duration_formatted,
                "energy_wh": round(total_energy_wh_session, 3),
                "energy_kWh": round(total_energy_kwh_all, 2),
                "cost_pln": round(total_cost_all, 2),
            }

            write_to_csv(FILE_PATH, data)

            print(f"Sesja {session}: {duration_formatted}, {round(total_energy_wh_session, 3)} Wh, {round(total_cost_all, 2)} PLN")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram zakończony. Dane zapisane w pliku.")




if __name__ == "__main__":
    csvv()
