import RPi.GPIO as GPIO
import time
from pir import Pir
from motor import Motor
GPIO.setmode(GPIO.BCM)
import multiprocessing
global pins, cw, ccw, keypadPressed
pins = [18,20,22,24] # controller inputs: in1, in2, in3, in4
ccw = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
        [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
cw = ccw[:]  # use slicing to copy list 
cw.reverse()
# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 4
L2 = 27
L3 = 17
L4 = 5
# These are the four columns
C1 = 6
C2 = 19
C3 = 26
C4 = 16
# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1
secretCode = "1234"
input = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# This callback registers the key that was pressed
# if no other key is currently pressed
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)

def checkSpecialKeys():
    global input
    global secretCode
    pressed = False

    GPIO.output(L3, GPIO.HIGH)
    if (GPIO.input(C4) == 1):
        print(input)
        print("Input reset!");
        pressed = True
    GPIO.output(L3, GPIO.LOW)
        #new code for changing secrete code (decided against this method for better secruity)
  #end of new code
    GPIO.output(L1, GPIO.HIGH)
    if (not pressed and GPIO.input(C4) == 1):
        if input == secretCode:
            print("Code correct!")
            # TODO: Unlock a door, turn a light on, etc.
        else:
            print("Incorrect code!")
            print(input)
            # TODO: Sound an alarm, send an email, etc.
        pressed = True
    GPIO.output(L3, GPIO.LOW)
    if pressed:
        input = ""
    return pressed

# reads the columns and appends the value, that corresponds
# to the button, to a variable
def readLine(line, characters):
    global input
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        input = input + characters[0]
    if(GPIO.input(C2) == 1):
        input = input + characters[1]
    if(GPIO.input(C3) == 1):
        input = input + characters[2]
    if(GPIO.input(C4) == 1):
        input = input + characters[3]
    GPIO.output(line, GPIO.LOW)

def runKey():
  try:
      keypadPressed = -1
      while True:
          # If a button was previously pressed,
          # check, whether the user has released it yet
          if keypadPressed != -1:
              setAllLines(GPIO.HIGH)
              if GPIO.input(keypadPressed) == 0:
                  keypadPressed = -1
              else:
                  time.sleep(0.2)
          # Otherwise, just read the input
          else:
              if not checkSpecialKeys():
                  one= readLine(L1, ["1","2","3","A"])
                  two= readLine(L2, ["4","5","6","B"])
                  three= readLine(L3, ["7","8","9","C"])
                  four= readLine(L4, ["*","0","#","D"])
                  time.sleep(0.2)
              else:
                  time.sleep(0.2)
          
  except KeyboardInterrupt:
      print("\nApplication stopped!")

def runMotor(): #runs the motor cw and ccw in a loop
  stepper = Motor(pins)
  try:
    while True:
      stepper.loop(cw)
      stepper.loop(ccw)
  except e:
    print(e)
    pass

  GPIO.cleanup()

def buzzer(BUZZER): #turns on the buzzer and beeps 4 times
    GPIO.setwarnings(False)
    #BUZZER= 13
    buzzState = True
    GPIO.setup(BUZZER, GPIO.OUT)
    for i in range (4):               
      GPIO.output(BUZZER, 0)# set output to 0
      time.sleep(0.1)# wait 0.5 sec
      GPIO.output(BUZZER, 1)# set output to 3.3V
      time.sleep(0.1)
      GPIO.output(BUZZER, 0)

class Alarm():

  def __init__(self, pir, led): #create alarm as a pir
    self.alarm = Pir(pir, led)
  
  def setup(self, led): #set up of the sensor to initialize
    GPIO.output(led, GPIO.LOW)
    print ("Sensor initializing . . .")
    #time.sleep(30) #Give sensor time to startup
    print ("50% . . .")
    time.sleep(10) #Give sensor time to startup
    print ("Active")
    print ("Press Ctrl+c to end program")
    GPIO.output(led, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led, GPIO.LOW)  
  
  def runAlarm(self, pir, led): #runs the actual alarm
    stepper = Motor(pins)
    try:
      while True:
        if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
          print ("Motion Detected!")
          buzzer(13) #turn on buzzer to signal motion
          print("Buzzer on")
          GPIO.output(led, GPIO.HIGH) #Turn on LED
          time.sleep(3) #Keep LED on for 3 seconds
          print ("led on!")
          GPIO.output(led, GPIO.LOW) #Turn off LED
          time.sleep(.1)
    except KeyboardInterrupt: #Ctrl+c
      pass #Do nothing, continue to finally
    GPIO.cleanup() 
    print ("Program ended")

def createAlarm(pir, led): #create a function to create and run alarm for multiprocessing
  security = Alarm(pir,led)
  security.setup(led)
  security.runAlarm(pir, led)

pir = 23 #Assign pin 8 to PIR
led = 21 #Assign pin 10 to LED
#run functions continuously with multiprocessing
keycheck = multiprocessing.Process(target=runKey) 
keycheck.start() 
motorcont = multiprocessing.Process(target=runMotor) 
motorcont.start() 
alarmset = multiprocessing.Process(target=createAlarm, args=(pir,led))
alarmset.start()
