from timeseries import *
from Phidget22.Devices.VoltageRatioInput import *
from pathlib import Path
import time


class PhidgetInterface:
    # Phidget API
    __voltage_ratio_input_0 = VoltageRatioInput()
    __voltage_ratio_input_1 = VoltageRatioInput()
    __connected = False

    # Data Management
    __file_name = "PhidgetData"
    data = [Timeseries(__file_name + "_channel_0"), Timeseries(__file_name + "_channel_1")]
    __start_time = 0
    __start_time_set = False

    def connect(self):
        self.__voltage_ratio_input_0.setDeviceSerialNumber(716773)
        self.__voltage_ratio_input_0.setDeviceSerialNumber(716773)
        self.__voltage_ratio_input_0.setChannel(0)
        self.__voltage_ratio_input_0.setChannel(1)
        self.__voltage_ratio_input_0.setOnVoltageRatioChangeHandler(self.__on_voltage_change)
        self.__voltage_ratio_input_1.setOnVoltageRatioChangeHandler(self.__on_voltage_change)
        self.__voltage_ratio_input_0.openWaitForAttachment(1000)
        self.__voltage_ratio_input_1.openWaitForAttachment(1000)
        self.data[0].set_filename("./data/" + self.__file_name + "_channel_0")
        self.data[1].set_filename("./data/" + self.__file_name + "_channel_1")
        self.__connected = True
        Path("./data").mkdir(parents=True, exist_ok=True)
        if not self.__start_time_set:
            self.__start_time = int(round(time.time() * 1000))
            self.__start_time_set = True

    def disconnect(self):
        self.__voltage_ratio_input_0.close()
        self.__voltage_ratio_input_1.close()
        self.__connected = False

    def get_connected(self):
        return self.__connected

    def save_data(self):
        self.data[0].save_data()
        self.data[1].save_data()

    def clear_data(self):
        self.data[0].reset()
        self.data[1].reset()

        if self.get_connected():
            self.__start_time_set = True
            self.__start_time = int(round(time.time() * 1000))
        else:
            self.__start_time_set = False

    def __on_voltage_change(self, phidget_vri, voltage_ratio):
        self.data[phidget_vri.getChannel()].update_data(int(round(time.time() * 1000)) - self.__start_time,
                                                        voltage_ratio)

    def set_file_name(self, file_name: str):
        self.__file_name = file_name

        self.data[0].set_filename("./data/" + self.__file_name + "_channel_0")
        self.data[1].set_filename("./data/" + self.__file_name + "_channel_1")
