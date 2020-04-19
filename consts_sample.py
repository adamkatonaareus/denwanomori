import RPi.GPIO as GPIO

# Common constants

# Numpad or rotary dial mode
# numpad
# rotary1: "kurbli", counting number of impluses, only one number to dial
# rotary2: rotary dial with more than one number to dial. Not implemented yet!
DIAL_MODE = "rotary1"

# Hang up switch pin
HANGUP_PIN = 4

# What to expect on the pin when user lifts up or hangs up.
LIFT_UP = GPIO.HIGH
HANG_UP = GPIO.LOW

# Retry switch pin
RETRY_PIN = 11

# Operation led pin
OP_LED_PIN = 14

# Sleep after scanning the numpad.
SCAN_SLEEP = 0.1

# Returning numpad result after this cycles of scanning.
SCAN_TIMEOUT = 8

# Invert numpad pins?
INVERT_KEYS = True

# Max selection length
MAX_SELECTION_LENGTH = 3

# Audio source folder
AUDIO_PATH = "/home/pi/denwanomori/media/"

# Logger config
LOG4P_CONFIG = "/home/pi/denwanomori/log4p.json"

# Device No. and REST API key
DEVICE_NO = 100
API_KEY = "12345"


