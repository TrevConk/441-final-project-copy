import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #Set GPIO to pin numbering
pir = 23 #Assign pin 8 to PIR
led = 21 #Assign pin 10 to LED
GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
GPIO.setup(led, GPIO.OUT) #Setup GPIO pin for LED as output
GPIO.output(led, GPIO.LOW)
print ("Sensor initializing . . .")
time.sleep(30) #Give sensor time to startup
print ("50% . . .")
time.sleep(30) #Give sensor time to startup
print ("Active")
print ("Press Ctrl+c to end program")
GPIO.output(led, GPIO.HIGH)
time.sleep(1)
GPIO.output(led, GPIO.LOW)
try:
  while True:
    if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
      print ("Motion Detected!")
      GPIO.output(led, GPIO.HIGH) #Turn on LED
      time.sleep(3) #Keep LED on for 3 seconds
      print ("led on!")
      GPIO.output(led, GPIO.LOW) #Turn off LED
      time.sleep(.1)
      #some chanfes
    #print("not detected")
    #time.sleep(3)

except KeyboardInterrupt: #Ctrl+c
  pass #Do nothing, continue to finally

#finally:
  #GPIO.output(led, False) #Turn off LED in case left on
GPIO.cleanup() #reset all GPIO
print ("Program ended")


'''
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #Set GPIO to pin numbering
GPIO.setwarnings(False)
pir = 23 #Assign pin 8 to PIR
led = 21 #Assign pin 10 to LED
tled = 17
buz= 13
buzzState = False
GPIO.setup(buz, GPIO.OUT)
GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
GPIO.setup(led, GPIO.OUT) #Setup GPIO pin for LED as output
GPIO.setup(tled, GPIO.OUT)
GPIO.output(led, GPIO.LOW)
GPIO.output(tled, GPIO.LOW)
print ("Sensor initializing . . .")
time.sleep(30) #Give sensor time to startup
print ("50% . . .")
time.sleep(30) #Give sensor time to startup
print ("Active")
print ("Press Ctrl+c to end program")
GPIO.output(led, GPIO.HIGH)
time.sleep(1)
GPIO.output(led, GPIO.LOW)
try:
  while True:
    if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
      print ("Motion Detected!")
      GPIO.output(led, GPIO.HIGH) #Turn on LED
      time.sleep(4) #Keep LED on for 4 seconds
      print ("led on!")
      print (GPIO.input(pir))
      GPIO.output(led, GPIO.LOW) #Turn off LED
      time.sleep(.5)
      #some chanfes
      while True:
        buzzState = not buzzState
        GPIO.output(buz, buzzState)
        time.sleep(1)
    else:
      print ("No Motion Detected!")
      print (GPIO.input(pir))
      GPIO.output(tled, GPIO.HIGH) #Turn on LED
      time.sleep(4) #Keep LED on for 4 seconds
      #print ("led on!")
      GPIO.output(tled, GPIO.LOW) #Turn off LED
      time.sleep(.5)
      #some chanfes

except KeyboardInterrupt: #Ctrl+c
  pass #Do nothing, continue to finally

#finally:
  #GPIO.output(led, False) #Turn off LED in case left on
GPIO.cleanup() #reset all GPIO
print ("Program ended")
'''