import arduino.serial_rw as serial_rw
import GUI.display as display
import GUI.error_display as eDisp


def main():
    try:
        display.main()
    except Exception as e:
        eDisp.displayError(e)
    finally:
        # if the program is closed, or an error occurs
        pass


if __name__ == "__main__":
    main()
