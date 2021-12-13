import RPi.GPIO as GPIO
import multiprocessing
import time
from pir import Pir
from motor import Motor
import json

location = '/usr/lib/cgi-bin/pinData.txt'
alarmGoingOff = multiprocessing.Value('i',0)

# global pins, cw, ccw, keypadPressed

def checkHTML():
    global cstate
    global secretCode
    with open(location, 'r') as pinDataRead:
            pinData = json.load(pinDataRead)
            cstate = pinData['selection']
            secretCode = pinData['pin']
            print(cstate)
            # Three different possible states
            # 'Turn Off Alarm' -> disables alarm
            # 'Arm Alarm' -> sensing
            # 'Reset Pin' -> changes pin

def updateHTML(state):
  dataDump = {'pin':secretCode,'selection':state}
  with open(location, 'w') as f:
    json.dump(dataDump, f)
            # Three different possible states
            # 'Turn Off Alarm' -> disables alarm
            # 'Arm Alarm' -> sensing
            # 'Reset Pin' -> changes pin






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
secretCode = ""
kinput = ""
cstate = 'Arm Alarm'
CC = 0

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
    global secretCode
    global kinput 
    global CC
    global cstate
    pressed = False

    GPIO.output(L3, GPIO.HIGH)
    if (GPIO.input(C4) == 1):
        print("Input reset!")
        print("kinput: " + kinput)
        print("Line 1: " + str(GPIO.input(C1)))
        print("Line 2: " + str(GPIO.input(C2)))
        print("Line 3: " + str(GPIO.input(C3)))
        print("Line 4: " + str(GPIO.input(C4)))
        pressed = True
    GPIO.output(L3, GPIO.LOW)
        #new code for changing secrete code (decided against this method for better secruity)
  #end of new code
    GPIO.output(L1, GPIO.HIGH)
    if (not pressed and GPIO.input(C4) == 1):
        if kinput == secretCode:
            print("Code correct!")
            print("kinput: " + kinput)
            print("Line 1: " + str(GPIO.input(C1)))
            print("Line 2: " + str(GPIO.input(C2)))
            print("Line 3: " + str(GPIO.input(C3)))
            print("Line 4: " + str(GPIO.input(C4)))
            CC = 1
            print(CC)
            cstate = 'Turn Off Alarm'
            updateHTML('Turn Off Alarm')
            # TODO: stop
        elif kinput == "*":
          print("Alarm Armed")
          state = 'Arm Alarm'
          cstate = 'Arm Alarm'
        else:
            print("Incorrect code!")
            print("\"" + kinput + "\"")
            # TODO: Sound an alarm, flash light
        pressed = True
    GPIO.output(L3, GPIO.LOW)
    if pressed:
        kinput = ""
    return pressed

# reads the columns and appends the value, that corresponds
# to the button, to a variable
def readLine(line, characters):
    global kinput
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        kinput = kinput + characters[0]
    if(GPIO.input(C2) == 1):
        kinput = kinput + characters[1]
    if(GPIO.input(C3) == 1):
        kinput = kinput + characters[2]
    if(GPIO.input(C4) == 1):
        kinput = kinput + characters[3]
    GPIO.output(line, GPIO.LOW)

def runKey():
    try:
        keypadPressed = -1
        start = time.time()
        while True:
            if time.time() - start > 10:
                break
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
                    one   = readLine(L1, ["1","2","3","A"])
                    two   = readLine(L2, ["4","5","6","B"])
                    three = readLine(L3, ["7","8","9","C"])
                    four  = readLine(L4, ["*","0","#","D"])
                    time.sleep(0.2)
                else:
                    time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nApplication stopped!")
        exit()

def runMotor(): #runs the motor cw and ccw in a loop
  global CC

  stepper = Motor(pins)
  try:
    while True:
      print("runMotor CC: " + str(CC))
      stepper.loop(cw)
      stepper.loop(ccw)
  except Exception as e:
    print(e)
    exit()

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

  def __init__(self, pir, led, alarmGoingOff): #create alarm as a pir
    self.alarm = Pir(pir, led)
  
  def setup(self, led): #set up of the sensor to initialize
    global cstate
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
    #cstate = "Arm Alarm"  
  
  def runAlarm(self, pir, led, alarmGoingOff): #runs the actual alarm
    stepper = Motor(pins)
    try:
        start = time.time()
        while True:
            if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
                print ("Motion Detected!")
                alarmGoingOff = 1
                buzzer(13) #turn on buzzer to signal motion
                GPIO.output(led, GPIO.HIGH) #Turn on LED
                time.sleep(3) #Keep LED on for 3 seconds
                GPIO.output(led, GPIO.LOW) #Turn off LED
                time.sleep(.1)
            elif (time.time() - start) > 10:
                break
    except KeyboardInterrupt: #Ctrl+c
        exit()

def createAlarm(pir, led, alarmGoingOff): #create a function to create and run alarm for multiprocessing
    security = Alarm(pir,led,alarmGoingOff)
    security.setup(led)
    security.runAlarm(pir, led, alarmGoingOff)

pir = 23 #Assign pin 8 to PIR
led = 21 #Assign pin 10 to LED

meme = 0
stepper = Motor(pins)

print("cstate: " + cstate)

alarmset = multiprocessing.Process(target=createAlarm, args=(pir,led,alarmGoingOff))
alarmset.start()

try:
  while True:
        checkHTML()
        if cstate == "Arm Alarm" and alarmGoingOff == 0:
            # Wait for 1 second between loops
            time.sleep(1)

            # Look left and scan for motion for 10 seconds
            stepper.loop(cw)
            checkHTML() 
            stepper.loop(ccw)
            checkHTML()
        elif cstate == "Arm Alarm" and alarmGoingOff == 1:
            runKey()
            checkHTML()
        elif cstate == "Turn Off Alarm" or "Reset Pin":
            print("Waiting")
            #runKey()
            checkHTML()
            time.sleep(1)
            print(alarmGoingOff.value)
except Exception as e:
    print('cod ended')
    print(e)
