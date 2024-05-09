import datetime
import logging
import os
from enum import Enum, auto

import arduino.serial_rw as arduino
import default_parameters as params


class GameState(Enum):
    WAITING_FOR_START = auto()
    WAITING_FOR_LOADED_MATERIAL = auto()
    WAITING_FOR_TRIGGER_PRESS = auto()
    END_STATE = auto()


class Game:
    def __init__(self, disp):
        self.disp = disp
        self.ard = arduino.SerialRW()
        self.game_state = GameState.WAITING_FOR_START

        # TODO: right now theres no way to turn the technology off via the communication with the arduino
        self.tech_on = False

        self.set_start_time()
        logging.debug("Waiting for start")
        self.ard.send_reset()

    def update(self):
        if self.game_state == GameState.WAITING_FOR_START:
            self.check_for_start()
        elif self.game_state == GameState.WAITING_FOR_LOADED_MATERIAL:
            self.update_progress()
            self.waiting_for_loaded_material()
        elif self.game_state == GameState.WAITING_FOR_TRIGGER_PRESS:
            self.update_progress()
            self.waiting_for_trigger_press()
        elif self.game_state == GameState.END_STATE:
            self.end_game()

    ############################
    # GAME LOGIC
    ############################

    def check_for_start(self):
        arduino_ready = self.ard.check_ready()
        if arduino_ready is None:
            self.disp.set_info(
                "Error: Could not open serial port: " + params.ARDUINO_COMPORT
            )
            return

        if arduino_ready:
            self.game_state = GameState.WAITING_FOR_LOADED_MATERIAL
            logging.debug("Start button pressed, waiting for loaded material")
            self.set_start_time()

    def update_progress(self):
        time = self.get_time()
        self.disp.set_time_left(params.TIME_LIMIT - time)

        if time > params.TIME_LIMIT:
            logging.debug("Time limit reached, game over")
            self.game_state = GameState.END_STATE

    def waiting_for_loaded_material(self):
        if self.tech_on:
            self.disp.set_info(
                "TECHNOLOGY: ENABLED\n\nFeel the material and shoot it into the correct button!"
            )
        else:
            self.disp.set_info(
                "TECHNOLOGY: DISABLED\n\nFeel the material and shoot it into the correct button!"
            )

        self.curr_fabric = self.ard.get_fabric()
        if self.curr_fabric is not None:
            self.ard.set_target(self.curr_fabric)

            if self.tech_on:
                self.disp.set_info(
                    "TECHNOLOGY: ENABLED\n\n" + self.curr_fabric + " was detected!"
                )

            logging.debug(
                "Fabric detected: " + self.curr_fabric + ", waiting for trigger press"
            )
            self.game_state = GameState.WAITING_FOR_TRIGGER_PRESS

    def waiting_for_trigger_press(self):
        target_hit = self.ard.get_target_hit()
        if target_hit:
            if self.tech_on:
                # TODO: change the color too
                # TODO: this dissapears immediately because there is no delay, so fix that without blocking
                self.disp.set_info(
                    "TECHNOLOGY: ENABLED\n\n"
                    + self.curr_fabric
                    + " was sorted correctly!"
                )
            else:
                self.disp.set_info(
                    "TECHNOLOGY: DISABLED\n\n"
                    + self.curr_fabric
                    + " was sorted correctly!"
                )
            logging.debug("Correct fabric sorted, waiting for loaded material")
            self.disp.set_score(self.disp.score.value() + 1)

            # update high score
            if self.disp.score.value() > self.disp.high_score.value():
                self.update_high_score()
                logging.debug("High score updated to: " + str(self.disp.score.value()))

        elif target_hit is not None:
            if self.tech_on:
                self.disp.set_info(
                    "TECHNOLOGY: ENABLED\n\n"
                    + self.curr_fabric
                    + " was sorted incorrectly!"
                )
            else:
                self.disp.set_info(
                    "TECHNOLOGY: DISABLED\n\n"
                    + self.curr_fabric
                    + " was sorted incorrectly!"
                )
            logging.debug("Incorrect fabric sorted, waiting for loaded material")

        if target_hit is not None:
            self.game_state = GameState.WAITING_FOR_LOADED_MATERIAL
            self.ard.send_ready()

    def end_game(self):
        # TODO: this will disappear immediately, so fix that (you can probably get away with blocking, but eh, not the best)
        self.disp.set_info("GAME OVER!")

        self.disp.set_info("PRESS THE FLASHING BUTTON TO BEGIN!")

        self.game_state = GameState.WAITING_FOR_START
        self.ard.send_reset()

    ############################
    # HELPER FUNCTIONS
    ############################

    def update_high_score(self):
        new_score = self.disp.score.value()
        self.disp.set_high_score(new_score)
        try:
            os.remove("./logs/high_score.log")
        except FileNotFoundError:
            pass

        with open("./logs/high_score.log", "w") as f:
            f.write(str(int(new_score)))

    def set_start_time(self):
        self.start_time = datetime.datetime.now()

    def get_time(self):
        return (datetime.datetime.now() - self.start_time).total_seconds()
