import os

import arduino.serial_rw as serial_rw
import GUI.display as display
import GUI.error_display as eDisp


def main():
    try:
        # make a directory for logs if it doesn't exist
        if not os.path.exists("./logs"):
            os.makedirs("./logs")

        display.main()
    except Exception as e:
        eDisp.displayError(e)
    finally:
        # if the program is closed, or an error occurs
        pass


if __name__ == "__main__":
    main()
