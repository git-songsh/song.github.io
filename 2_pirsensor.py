import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pirPin = 7

GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)

detectednum = 0

while True:

    if GPIO.input(pirPin) == GPIO.LOW:

        print "Motion detected!"
        detectednum += 1

    else:

        print "No motion"

    time.sleep(0.2)