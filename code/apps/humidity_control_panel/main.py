from gui import HumidityControlGUI
from control import HumidityController

if __name__ == "__main__":
    gui = HumidityControlGUI()
    with HumidityController(
        ui=gui, humidity_sensor_id="7402", pump_id="320"
    ) as controller:
        gui.run()
