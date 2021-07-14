from __future__ import print_function
import time
import RPi.GPIO as GPIO

PIR = 7

GPIO.setup(PIR, GPIO.IN, GPIO.PUD_UP)

def measure():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    
    elapsed = stop - start
    distance = (elapsed * 34300) / 2
    
    return distance

def measure_average():
    distance1 = measure()
    time.sleep(1)
    distance2 = measure()
    time.sleep(1)
    distance3 = measure()
    time.sleep(1)
    distance4 = measure()
    time.sleep(1)
    distance5 = measure()
    time.sleep(1)
    distance6 = measure()
    time.sleep(1)
    distance7 = measure()
    time.sleep(1)
    distance8 = measure()
    time.sleep(1)
    distance9 = measure()
    time.sleep(1)
    distance10 = measure()
  
    distance = ( distance1 + distance2 + distance3 + distance4 + distance5 + distance6 + distance7 + distance8 + distance9 + distance10 ) / 10
    #정밀도를 높이기 위해 1초마다 거리를 측정하여 10초동안의 평균거리 계산
    
    return distance

def pirmeasure():
    if GPIO.input(pirPin) == GPIO.LOW:
                                        

while True:
    
    distance = measure_average()
    
    time.sleep(1)

    if (distance <= 30) :
        a = a+1
        if (a >= 10) : 
            pirmeasure()
            if (detectednum >= 10) :
                """"""
                
    else:
        a = 0
        continue
    

        

