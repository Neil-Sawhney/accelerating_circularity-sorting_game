######################################## GENERAL LOGGING ########################################

# Debug will print everything to the log file
# Info will print everything but the debug messages
# Warning will print everything but the debug and info messages
# Error will print everything but the debug, info, and warning messages
# Critical will print everything but the debug, info, warning, and error messages
LOG_LEVEL = "DEBUG"

######################################## GENERAL LOGGING ########################################

############################################ PORTS ##############################################
# debugging hint: socat -d -d pty,rawer,echo=0 pty,rawer,echo=0
ARDUINO_COMPORT = "/dev/ttyACM1"
############################################ PORTS ##############################################

######################################## GAME PARAMETERS ########################################
# The time in seconds that the game will run for
TIME_LIMIT = 40
######################################## GAME PARAMETERS ########################################

######################################## FABRIC MAPPINGS ########################################
fabric_mapping = {
    "NYLON": 0,
    "LINEN": 1,
    "SPANDEX": 2,
    "WOOL": 3,
    "TRASH": 4,
    "COTTON": 5,
}
######################################## FABRIC MAPPINGS ########################################
