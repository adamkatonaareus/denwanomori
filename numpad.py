import RPi.GPIO as GPIO
import time
import player
import consts as CONSTS
import log4p

class NumPad:

    player = None
    log = None

    rows = [17, 25, 24, 23]
    cols = [27, 18, 22]
    keys = [
	['1', '2', '3'],
	['4', '5', '6'],
	['7', '8', '9'],
	['*', '0', '#']]

    #
    # Configure GPIO
    #
    def __init__(self, playerInstance):

	logger = log4p.GetLogger(__name__, config=CONSTS.LOG4P_CONFIG)
	self.log = logger.logger

	self.log.debug("Initializing NumPad...")
	self.player = playerInstance;

	for row_pin in self.rows:
	    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	for col_pin in self.cols:
	    GPIO.setup(col_pin, GPIO.OUT)

    #
    # Method that listens to one keypress.
    #
    def getKey(self):

        key = 0

	for col_num, col_pin in enumerate(self.cols):
	    GPIO.output(col_pin, 1)
	    for row_num, row_pin in enumerate(self.rows):
		if GPIO.input(row_pin):
		    if (CONSTS.INVERT_KEYS):
			key = self.keys[3-row_num][2-col_num]
		    else:
			key = self.keys[row_num][col_num]
	    GPIO.output(col_pin, 0)
	return key

    #
    # Method that waits for a number of keypresses so a number larger than 9 can be selected.
    #
    def getMediaNo(self):

        selected = ""
        cycle = 0
	#self.player.preload("audio/beep.wav")

	self.log.debug("Waiting for numpad entry...")

	while True:
	    key = self.getKey()
	    if key :
		self.log.debug("\tKey pressed: " + key)
		selected += key
		cycle = 0
		self.player.playFileAsync(CONSTS.AUDIO_PATH + "beep.wav")

		# Limit length so we will eventually return something
		if (len(selected) >= CONSTS.MAX_SELECTION_LENGTH):
		    return selected

	    time.sleep(CONSTS.SCAN_SLEEP)
	    cycle += 1

	    # Check hangup key, stop if pressed
	    if (GPIO.input(CONSTS.HANGUP_PIN) == True):
		self.log.debug("\tHangup.")
		return ""

	    # Return selection after a bit of waiting
	    if (cycle > CONSTS.SCAN_TIMEOUT and selected > ""):
		return selected



