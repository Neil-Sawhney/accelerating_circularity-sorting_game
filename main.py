import arduino.serialRW as serialRW
import GUI.display as display
import GUI.errorDisplay as eDisp


def main():
    try:
        display.main()
    except Exception as e:
        eDisp.displayError(e)
    finally:
        # if the program is closed, or an error occurs, close the serial port
        serialRW.deinit()


if __name__ == "__main__":
    main()
