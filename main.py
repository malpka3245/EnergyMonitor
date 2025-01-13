from EnergyMonitor import EnergyMonitorController, EnergyMonitor
from OHMController import OhmController
from CsvController import CsvController
import time
from datetime import datetime
file_path = "logs.csv"
INTERVAL = 1

if __name__ == "__main__":
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
