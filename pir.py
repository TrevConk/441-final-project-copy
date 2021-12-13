import RPi.GPIO as GPIO
import time

class Pir():

  def __init__(self, pir, led):
    self.pir, self.led = pir,led
    GPIO.setmode(GPIO.BCM) #Set GPIO to pin numbering
    #pir = 23 #Assign pin 8 to PIR
    #led = 21 #Assign pin 10 to LED
    GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
    GPIO.setup(led, GPIO.OUT) #Setup GPIO pin for LED as output
  
  # def setup(self, led):
  #   GPIO.output(led, GPIO.LOW)
  #   print ("Sensor initializing . . .")
  #   time.sleep(30) #Give sensor time to startup
  #   print ("50% . . .")
  #   time.sleep(30) #Give sensor time to startup
  #   print ("Active")
  #   print ("Press Ctrl+c to end program")
  #   GPIO.output(led, GPIO.HIGH)
  #   time.sleep(1)
  #   GPIO.output(led, GPIO.LOW)
  # try:
  #   while True:
  #     if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
  #       print ("Motion Detected!")
  #       GPIO.output(led, GPIO.HIGH) #Turn on LED
  #       time.sleep(3) #Keep LED on for 3 seconds
  #       print ("led on!")
  #       GPIO.output(led, GPIO.LOW) #Turn off LED
  #       time.sleep(.1)
  #       #some chanfes
  #     #print("not detected")
  #     #time.sleep(3)

  # except KeyboardInterrupt: #Ctrl+c
  #   pass #Do nothing, continue to finally

  # #finally:
  #   #GPIO.output(led, False) #Turn off LED in case left on
  # GPIO.cleanup() #reset all GPIO
  # print ("Program ended")