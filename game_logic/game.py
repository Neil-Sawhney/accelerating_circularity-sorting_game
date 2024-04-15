import datetime
import logging
import os
from enum import Enum, auto

import serial

import arduino.serial_rw as arduino
import default_parameters as params


class GameState(Enum):
    WAITING_FOR_START = auto()
    PLAYING = auto()
    END_STATE = auto()


class Game:
    def __init__(self, disp):
        self.disp = disp
        self.ard = arduino.SerialRW()
        self.game_state = GameState.WAITING_FOR_START

        self.tech_on = False

        self.set_start_time()

    def update(self):
        if self.game_state == GameState.WAITING_FOR_START:
            self.check_for_start()
        elif self.game_state == GameState.PLAYING:
            self.update_progress()
            self.gameplay()
        elif self.game_state == GameState.END_STATE:
            self.end_game()

    ############################
    # GAME LOGIC
    ############################

    def check_for_start(self):
        try:
            arduino_ready = self.ard.check_ready()
        except serial.SerialException:
            self.disp.set_info(
                "Error: Could not open serial port: " + params.ARDUINO_COMPORT
            )

        if arduino_ready:
            self.game_state = GameState.PLAYING
            self.set_start_time()

    def update_progress(self):
        time = self.get_time()
        self.disp.set_time_left(params.TIME_LIMIT - time)

        if time > params.TIME_LIMIT:
            self.game_state = GameState.END_STATE

    def gameplay(self):
        # TODO: right now theres no way to turn the technology off via the communication with the arduino

        if self.tech_on:
            self.disp.set_info(
                "TECHNOLOGY: ENABLED\n\nFeel the material and shoot it into the correct button!"
            )
        else:
            self.disp.set_info(
                "TECHNOLOGY: DISABLED\n\nFeel the material and shoot it into the correct button!"
            )

        fabric = self.ard.get_fabric()
        if self.tech_on:
            self.disp.set_info("TECHNOLOGY: ENABLED\n\n" + fabric + " was detected!")
        self.ard.set_target(fabric)

        # self.disp.set_info(
        #     "TECHNOLOGY: DISABLED\n\nFeel the material and shoot it into the correct button!"
        # )

    def end_game(self):
        self.disp.set_info("GAME OVER!")

        # update the high score if necessary
        if self.disp.score.value() > self.disp.high_score.value():
            self.disp.set_high_score(self.disp.score.value())
            self.update_high_score(self.disp.score.value())

        self.game_state = GameState.WAITING_FOR_START

    ############################
    # HELPER FUNCTIONS
    ############################

    def update_high_score(self, new_score):
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
