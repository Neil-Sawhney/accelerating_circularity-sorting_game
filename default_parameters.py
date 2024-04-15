######################################## GENERAL LOGGING ########################################

# Debug will print everything to the log file
# Info will print everything but the debug messages
# Warning will print everything but the debug and info messages
# Error will print everything but the debug, info, and warning messages
# Critical will print everything but the debug, info, warning, and error messages
LOG_LEVEL = "DEBUG"

######################################## GENERAL LOGGING ########################################

############################################ PORTS ##############################################
ARDUINO_COMPORT = (
    "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313131351D042A1-if00"
)
############################################ PORTS ##############################################

######################################## GAME PARAMETERS ########################################
# The time in seconds that the game will run for
TIME_LIMIT = 180
######################################## GAME PARAMETERS ########################################

######################################## FABRIC MAPPINGS ########################################
fabric_mapping = {
    "denim": 0,
    "linen": 1,
}
######################################## FABRIC MAPPINGS ########################################
