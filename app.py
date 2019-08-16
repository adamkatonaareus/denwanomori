import RPi.GPIO as GPIO
import numpad
import player
import time
import consts as CONSTS
import log4p
import os

# Init app

logger = log4p.GetLogger(__name__, config=CONSTS.LOG4P_CONFIG)
log = logger.logger

log.info("Initializing app...")
GPIO.setmode(GPIO.BCM)

GPIO.setup(CONSTS.OP_LED_PIN, GPIO.OUT)
GPIO.output(CONSTS.OP_LED_PIN, 1)

GPIO.setup(CONSTS.RETRY_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(CONSTS.HANGUP_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

player = player.Player()
np = numpad.NumPad(player)

# Wait for user to lift handle
log.debug("Waiting for lift up...")

while True:

    try:

	if (GPIO.input(4) == False):
    
	    log.info("Lift up, playing intro.")
	    time.sleep(0.5)
	    player.playFileAsync(CONSTS.AUDIO_PATH + "intro.mp3")

	    # Wait for numpad input
	    selectedNo = np.getMediaNo()
	    if (selectedNo > ""):

		if (selectedNo.endswith(("#", "*"))):
		    selectedNo = selectedNo.replace("#", "").replace("*", "")

		selectedNo = selectedNo.replace("#", "_").replace("*", "_")

		log.info("Selected: " + selectedNo)
		filename = CONSTS.AUDIO_PATH + selectedNo + ".mp3"

		if (os.path.isfile(filename)):
			if (player.playFile(filename) == True):
				time.sleep(1)
				player.playFile(CONSTS.AUDIO_PATH + "outro.mp3")
				time.sleep(1)
		else:
			player.playFile(CONSTS.AUDIO_PATH + "wrong.wav")

		log.debug("End of cycle.")

	    else:

		player.stop()

    except KeyboardInterrupt:

	log.info("Exiting...")
        GPIO.cleanup()
	quit()

    except Exception as e:

	log.error("Unexpected error: " + str(e))
	#raise




