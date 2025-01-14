from EnergyMonitor import EnergyMonitorController, EnergyMonitor, EnergyMonitorView
from OHMController import OhmController
from CsvController import CsvController
import time
from datetime import datetime
import tkinter as tk

file_path = "logs.csv"
INTERVAL = 1


def start_gui():

    root = tk.Tk()

    # Tworzymy instancje klas odpowiedzialnych za monitorowanie energii i interfejs
    csv_control = CsvController(file_path)
    last_date, last_session = csv_control.load_last_session()
    current_date = datetime.now().strftime("%Y-%m-%d")
    session = last_session + 1 if last_date == current_date else 1
    oc = OhmController()  # Tworzymy obiekt OhmController
    monitor = EnergyMonitor()  # Zmieniono nazwę na monitor
    emc = EnergyMonitorController(oc, monitor, csv_control,
                                  session)  # Przekazujemy obiekt oc do EnergyMonitorController

    # Tworzymy widok
    view = EnergyMonitorView(root, emc)

    # Funkcja odświeżająca dane
    def refresh_data():
        emc.get_data()
        emc.update_elapsed_time(INTERVAL)
        view.update_data()  # Aktualizuje widok
        root.after(INTERVAL * 1000, refresh_data)  # Ustawia odświeżanie co INTERVAL sekund

    # Rozpoczynamy odświeżanie danych
    refresh_data()

    root.mainloop()


if __name__ == "__main__":
    # Start interfejsu graficznego w osobnym wątku
    start_gui()

    # Wersja z dotychczasowym działaniem w tle
    # Zakłada, że interfejs graficzny działa w osobnym wątku
    csv_control = CsvController(file_path)
    last_date, last_session = csv_control.load_last_session()
    current_date = datetime.now().strftime("%Y-%m-%d")
    session = last_session + 1 if last_date == current_date else 1
    oc = OhmController()
    em = EnergyMonitor()
    emc = EnergyMonitorController(oc, em, csv_control, session)

    while True:
        emc.get_data()
        emc.update_elapsed_time(INTERVAL)
        time.sleep(INTERVAL)

