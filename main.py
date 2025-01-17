from EnergyMonitor import EnergyMonitorController, EnergyMonitor, EnergyMonitorView
from OHMController import OhmController
from CsvController import CsvController
from Settings.settings import Settings
from datetime import datetime
import tkinter as tk

file_path = "logs.csv"
INTERVAL = 1

if __name__ == "__main__":
    root = tk.Tk()

    settings = Settings()
    csv_control = CsvController(file_path)
    last_date, last_session = csv_control.load_last_session()
    current_date = datetime.now().strftime("%Y-%m-%d")
    session = last_session + 1 if last_date == current_date else 1
    oc = OhmController()
    em = EnergyMonitor()
    emc = EnergyMonitorController(oc, em, csv_control, session, settings)
    view = EnergyMonitorView(root, emc)
    emc.attach_view(view)


    def update():
        emc.get_data()
        emc.update_elapsed_time(INTERVAL)
        root.after(1000, update)
    update()
    root.mainloop()
