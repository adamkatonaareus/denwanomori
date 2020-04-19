import pygame
import RPi.GPIO as GPIO
import time
import consts as CONSTS
import log4p


class Player:

    log = None

    def __init__(self):

	logger = log4p.GetLogger(__name__, config=CONSTS.LOG4P_CONFIG)
	self.log = logger.logger

	self.log.debug("Initializing audio player...")

	pygame.mixer.init()
	pygame.mixer.music.set_volume(1.0)

    def playFile(self, filename):

	self.playFileAsync(filename)
	self.log.debug("Waiting for audio to end...")
	while pygame.mixer.music.get_busy() == True:
	    
	    # check for hangup or retry
	    if ((GPIO.input(CONSTS.HANGUP_PIN) == CONSTS.HANG_UP) or (GPIO.input(CONSTS.RETRY_PIN) == GPIO.LOW)):
		self.log.debug("Hang up/retry while playing audio.")
		time.sleep(0.5)
		pygame.mixer.music.stop()
		return False

	return True


    def playFileAsync(self, filename):

	self.log.debug("Playing file " + filename)
	pygame.mixer.music.load(filename)
	pygame.mixer.music.play()


    def preload(self, filename):

	pygame.mixer.music.load(filename)

    def playPreloadedAsync(self):

	pygame.mixer.music.play()

    def stop(self):

	pygame.mixer.music.stop()

