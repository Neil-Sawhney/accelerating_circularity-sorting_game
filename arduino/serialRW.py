import logging

import serial

import defaultParameters as params
import GUI.displayTime as dTime
import GUI.errorDisplay as eDisp

ser = serial.Serial()


def RData():
    # data comes in as a string of the form "cmd,message"
    serialData = ser.readline().decode("utf-8")
    logging.debug("RX:" + serialData)
    cmd, message = serialData.split(",")

    return cmd, message


def init():
    global ser

    # if the serial port is not open, open it
    if not (ser.isOpen()):
        try:
            ser = serial.Serial(params.ARDUINO_COMPORT, 9600)
            logging.info("Opened arduino serial port: " + params.ARDUINO_COMPORT)
        except serial.SerialException:
            errormsg = "Could not open arduino serial port: " + params.ARDUINO_COMPORT
            logging.error(errormsg)
            eDisp.displayError(
                errormsg,
                "Change the COM port in the parameters menu, or alternatively in the defaultParameters.py file.",
            )
            return


def deinit():
    global ser
    if ser.isOpen():
        ser.close()
        logging.info("Serial port closed")
