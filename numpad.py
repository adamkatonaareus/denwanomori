import RPi.GPIO as GPIO
import time

class NumPad:

    scanSleep = 0.2
    scanTimeout = 10
    hangupPin = 4
    invertKeys = True

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
    def __init__(self):

	print("Initializing NumPad...")

        GPIO.setmode(GPIO.BCM)

	for row_pin in self.rows:
	    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	for col_pin in self.cols:
	    GPIO.setup(col_pin, GPIO.OUT)

	# Hangup pin
        GPIO.setup(self.hangupPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    #
    # Method that listens to one keypress.
    #
    def getKey(self):

        key = 0

	for col_num, col_pin in enumerate(self.cols):
	    GPIO.output(col_pin, 1)
	    for row_num, row_pin in enumerate(self.rows):
		if GPIO.input(row_pin):
		    if (self.invertKeys):
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

	print("Waiting for numpad entry...")

	while True:
	    key = self.getKey()
	    if key :
		print("\tKey pressed: " + key)
		selected += key
		cycle = 0
	    time.sleep(self.scanSleep)
	    cycle += 1

	    # Check hangup key, stop if pressed
	    if (GPIO.input(self.hangupPin) == False):
		print("\tHangup.")
		return ""

	    # Return selection after a bit of waiting
	    if (cycle > self.scanTimeout and selected > ""):
		return selected



