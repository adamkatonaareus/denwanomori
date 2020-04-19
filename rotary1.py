import RPi.GPIO as GPIO
import time
import player
import consts as CONSTS
import log4p

class Rotary:

    player = None
    log = None

    ROTARY_PIN = 17

    #
    # Configure GPIO
    #
    def __init__(self, playerInstance):

	logger = log4p.GetLogger(__name__, config=CONSTS.LOG4P_CONFIG)
	self.log = logger.logger

	self.log.debug("Initializing Rotary (1)...")
	self.player = playerInstance;

        GPIO.setup(self.ROTARY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    #
    # Method that waits for a number of rotations
    #
    def getMediaNo(self):

        selected = 0
        cycle = 0

	self.log.debug("Waiting for rotary entry...")

	while True:

	    rot = GPIO.input(self.ROTARY_PIN)
	    #self.log.debug("Rotary pin: " + str(rot))

	    if (rot == 0):

		# Wait until leaving the switch
		self.waitForEdge()
		#GPIO.wait_for_edge(self.ROTARY_PIN, GPIO_FALLING, timeout=5000)

		# Beep!
		self.player.playFileAsync(CONSTS.AUDIO_PATH + "beep.wav")
		selected += 1
		
		self.log.debug("Current selection: " + str(selected))

	    time.sleep(CONSTS.SCAN_SLEEP)
	    cycle += 1

	    # Check hangup key, stop if pressed
	    if (GPIO.input(CONSTS.HANGUP_PIN) == CONSTS.HANG_UP):
		self.log.debug("\tHangup.")
		return ""

	    # Return selection after a bit of waiting
	    if (cycle * CONSTS.SCAN_SLEEP >= CONSTS.SCAN_TIMEOUT and selected > 0):
		self.log.debug("Returning: " + str(selected))
		return str(selected)


    def waitForEdge(self):

	self.log.debug("Waiting for leaving the switch...")
	cycle = 0

	while (cycle * CONSTS.SCAN_SLEEP < CONSTS.SCAN_TIMEOUT):

	    if (GPIO.input(self.ROTARY_PIN) == 1):
		self.log.debug("Done.")
		return

	    time.sleep(CONSTS.SCAN_SLEEP)
	    cycle += 1
