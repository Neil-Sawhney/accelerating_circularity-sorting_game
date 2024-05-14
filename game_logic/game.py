import datetime
import logging
import os
from enum import Enum, auto

from PyQt5.QtCore import QFileInfo, QTimer, QUrl
from PyQt5.QtMultimedia import QSound, QSoundEffect

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

        self.background_music = QSound("assets/sounds/background_music.wav")
        self.correct_sound = QSound("assets/sounds/correct.wav")
        self.wrong_sound = QSound("assets/sounds/wrong.wav")
        self.scanned_sound = QSound("assets/sounds/scanned.wav")
        self.start_sound = QSound("assets/sounds/start.wav")

        self.ard = arduino.SerialRW()
        self.game_state = GameState.WAITING_FOR_START

        # tech trigger is used to ensure the technology enabled message is only displayed once
        self.init_tech_trigger = False
        self.tech_on = False

        self.set_start_time()
        logging.debug("Waiting for start")
        self.ard.send_reset()
        self.disp.set_info("PRESS THE FLASHING BUTTON TO BEGIN!")

    def update(self):
        if self.game_state == GameState.WAITING_FOR_START:
            self.waiting_for_start()
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

    def waiting_for_start(self):
        arduino_ready = self.ard.check_ready()
        if arduino_ready is None:
            self.disp.set_info(
                "Error: Could not open serial port: " + params.ARDUINO_COMPORT
            )
            return

        if arduino_ready:
            self.play_start_sound()

            self.game_state = GameState.WAITING_FOR_LOADED_MATERIAL
            logging.debug("Start button pressed, waiting for loaded material")
            self.set_start_time()

            self.disp.set_info(
                "FEEL THE MATERIAL\n AND SHOOT IT INTO THE CORRECT BUTTON!"
            )

    def update_progress(self):
        time = self.get_time()

        self.disp.set_time_left(params.TIME_LIMIT - time)

        if time > params.TIME_LIMIT / 2 and not self.tech_on:
            self.init_tech_trigger = True
            self.tech_on = True

        if time > params.TIME_LIMIT:
            logging.debug("Time limit reached, game over")
            self.game_state = GameState.END_STATE

    def waiting_for_loaded_material(self):
        self.curr_fabric = self.ard.get_fabric()
        if self.curr_fabric is not None:
            self.ard.set_target(self.curr_fabric)

            if self.tech_on and not self.init_tech_trigger:
                self.disp.set_info(self.curr_fabric + " detected!"),
                logging.debug(
                    "Fabric detected: "
                    + self.curr_fabric
                    + ", waiting for trigger press"
                )

            self.play_scanned_sound()
            self.game_state = GameState.WAITING_FOR_TRIGGER_PRESS

    def waiting_for_trigger_press(self):
        target_hit = self.ard.get_target_hit()
        if target_hit:
            # TODO: change the color too
            self.disp.set_info(
                "CORRECT!\n YOU SORTED " + self.curr_fabric + " CORRECTLY!"
            )
            logging.debug("Correct fabric sorted, waiting for loaded material")
            self.play_correct_sound()
            self.disp.set_score(self.disp.score.value() + 1)

            # update high score
            if self.disp.score.value() > self.disp.high_score.value():
                self.update_high_score()
                logging.debug("High score updated to: " + str(self.disp.score.value()))

        elif target_hit is not None:
            self.disp.set_info(
                "INCORRECT!\n THE PREVIOUS MATERIAL WAS " + self.curr_fabric + "!"
            )
            self.disp.set_score(self.disp.score.value() - 1)
            self.play_wrong_sound()
            logging.debug("incorrect fabric sorted, waiting for loaded material")

        if target_hit is None:
            return

        if self.init_tech_trigger:
            self.init_tech_trigger = False
            logging.debug("Enabling technology")
            self.ard.send_TECH_ON()

            self.disp.set_info(
                "TECHNOLOGY ENABLED!!!\nTHE SCANNER WILL DETECT THE MATERIAL BEFORE YOU SHOOT!"
            )
            self.set_text_with_delay(
                "FEEL THE MATERIAL\n AND SHOOT IT INTO THE CORRECT BUTTON!",
                5000,
            )
        else:
            if self.tech_on:
                self.ard.send_TECH_ON()
            else:
                self.ard.send_TECH_OFF()

            self.set_text_with_delay(
                "FEEL THE MATERIAL\n AND SHOOT IT INTO THE CORRECT BUTTON!",
                2000,
            )

        self.game_state = GameState.WAITING_FOR_LOADED_MATERIAL

    def end_game(self):
        self.disp.set_info("GAME OVER!")
        self.set_start_time()
        self.disp.set_score(0)
        self.disp.set_info("INITIALIZING...")
        self.disp.set_time_left(params.TIME_LIMIT)
        self.tech_on = False
        self.init_tech_trigger = False
        self.ard.send_reset()
        self.set_text_with_delay("PRESS THE FLASHING BUTTON TO BEGIN!", 5000)
        self.game_state = GameState.WAITING_FOR_START

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

    def set_text_with_delay(self, text, delay):
        """sets the text on the display for a certain amount of time

        Args:
            text (str): the text to display
            display_time (int): the time in milliseconds to display the text
        """
        QTimer.singleShot(delay, lambda: self.disp.set_info(text))

    def play_correct_sound(self):
        self.correct_sound.play()

    def play_wrong_sound(self):
        self.wrong_sound.play()

    def play_scanned_sound(self):
        self.scanned_sound.play()

    def play_start_sound(self):
        self.start_sound.play()
