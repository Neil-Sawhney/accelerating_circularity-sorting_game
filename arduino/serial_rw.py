import logging
from enum import Enum

import serial

import default_parameters as params
import GUI.error_display as eDisp


class Cmd(Enum):
    STATUS = 0
    TARGET = 1
    CARD_INFO = 2
    TARGET_HIT = 3
    LOGGING = 4


class Status(Enum):
    READY = 0
    RESET = 1
    NONE = 2


class Button(Enum):
    BUTTON_0 = 0
    BUTTON_1 = 1
    BUTTON_2 = 2
    BUTTON_3 = 3
    BUTTON_4 = 4
    BUTTON_5 = 5
    NONE = 6


class SerialRW:
    def __init__(self):
        self.ser = serial.Serial()

        # if the serial port is not open, open it
        if not (self.ser.isOpen()):
            try:
                self.ser = serial.Serial(params.ARDUINO_COMPORT, 9600)
                logging.info("Opened arduino serial port: " + params.ARDUINO_COMPORT)
            except serial.SerialException:
                errormsg = (
                    "Could not open arduino serial port: " + params.ARDUINO_COMPORT
                )
                logging.error(errormsg)
                eDisp.displayError(
                    errormsg,
                    "Change the COM port in the defaultParameters.py file.",
                )
                return

    def read_data(self):
        """Gets one line of data from the arduino and returns the command and message,
        if no data is available, it will return none. Does not block.

        Returns:
            cmd: the command from the arduino
            message: the message from the arduino
        """
        if not self.ser.in_waiting:
            return None, None

        # get a line from the arduino
        serialData = self.ser.readline().decode("utf-8")
        logging.debug("RX:" + serialData)
        rx_cmd, rx_message = serialData.split(",")
        cmd = Cmd(int(rx_cmd))

        # while the data recievied is a logging command, print the data to the log file and get the next line
        while cmd == Cmd.LOGGING:
            logging.debug("Arduino:" + rx_message)

            # get a line from the arduino
            serialData = self.ser.readline().decode("utf-8")
            logging.debug("RX:" + serialData)
            rx_cmd, rx_message = serialData.split(",")
            cmd = Cmd(int(rx_cmd))

        if cmd == Cmd.STATUS:
            message = Status(int(rx_message))
        else:
            message = rx_message

        return cmd, message

    def check_ready(self):
        """Checks if the arduino is ready to start the game

        Returns:
            True: if the arduino is ready
            False: if the arduino is not ready (no data available)
        """

        if not self.ser.is_open:
            return None

        if not self.ser.in_waiting:
            return False

        cmd, message = self.read_data()
        if message == Status.READY:
            return True

        logging.debug("Synchronization Error!! after check_ready")
        eDisp.displayError("Synchronization Error!!", "Please restart the game.")
        return False

    def get_fabric(self):
        """Gets the fabric from the arduino
        if no data is available, it will return none. Does not block.

        Returns:
            str: the fabric from the arduino
        """
        if not self.ser.in_waiting:
            return None

        cmd, message = self.read_data()

        if cmd == Cmd.CARD_INFO:
            return message

        logging.debug("Synchronization Error!! after get_fabric")
        eDisp.displayError("Synchronization Error!!", "Please restart the game.")

    def set_target(self, fabric):
        """Sends the target to the arduino

        Args:
            fabric (str): the target to send to the arduino
        """
        target = Button(params.fabric_mapping[fabric])
        self.ser.write(
            (str(Cmd.TARGET.value) + "," + str(target.value) + "\n").encode()
        )
        logging.debug("TX:" + str(Cmd.TARGET.value) + "," + str(target.value))

    def get_target_hit(self):
        """Checks if the correct target was hit or missed by the player

        Returns:
            True: if the correct target was hit
            False: if the target was missed
            None: if no data is available
        """

        if not self.ser.in_waiting:
            return None

        cmd, message = self.read_data()

        if cmd == Cmd.TARGET_HIT:
            return bool(message)

        logging.debug("Synchronization Error!! after get_target_hit")
        eDisp.displayError("Synchronization Error!!", "Please restart the game.")
