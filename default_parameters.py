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
ARDUINO_COMPORT = "/dev/pts/15"
############################################ PORTS ##############################################

######################################## GAME PARAMETERS ########################################
# The time in seconds that the game will run for
TIME_LIMIT = 10
######################################## GAME PARAMETERS ########################################

######################################## FABRIC MAPPINGS ########################################
fabric_mapping = {
    "nylon": 0,
    "linen": 1,
    "spandex": 2,
    "wool": 3,
    "trash": 4,
    "cotton": 5,
}
######################################## FABRIC MAPPINGS ########################################
