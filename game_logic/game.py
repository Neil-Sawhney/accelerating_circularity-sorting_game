import datetime
import logging
import os
from enum import Enum, auto

import serial

import arduino.serial_rw as arduino
import default_parameters as params
from GUI.display import MainWindow as disp

# logging
level = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
logging.basicConfig(
    filename="./logs/debug.log",
    format="%(asctime)s|%(levelname)s|%(message)s",
    filemode="w",
    level=level[params.LOG_LEVEL],
)


class GameState(Enum):
    WAITING_FOR_START = auto()
    PLAYING = auto()
    END_STATE = auto()


class Game:
    def __init__(self):
        self.ard = arduino.SerialRW()

        self.set_start_time()
        self.game_state = GameState.WAITING_FOR_START

        arduino.init()

    def update(self):
        if self.game_state == GameState.WAITING_FOR_START:
            self.check_for_start()

    ############################
    # GAME LOGIC
    ############################

    def check_for_start(self):
        # TODO: fix
        arduino_ready = False

        if not arduino_ready:
            try:
                arduino_ready = arduino.check_ready()
            except serial.SerialException:
                disp.set_info(
                    "Error: Could not open serial port: " + params.ARDUINO_COMPORT
                )

    ############################
    # HELPER FUNCTIONS
    ############################

    def update_high_score(new_score):
        try:
            os.remove("./logs/high_score.log")
        except FileNotFoundError:
            pass

        with open("./logs/high_score.log", "w") as f:
            f.write(str(new_score))

    def set_start_time(self):
        self.start_time = datetime.datetime.now()

    def get_time(self):
        return (datetime.datetime.now() - self.start_time).total_seconds()
