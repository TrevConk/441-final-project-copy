# This program allows a user to enter a
# Code. If the c-Button is pressed on the
# keypad, the input is reset. If the user
# hits the A-Button, the input is checked.
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

L1 = 4
L2 = 27
L3 = 17
L4 = 5

# These are the four columns
C1 = 6
C2 = 19
C3 = 26
C4 = 16
global secretCode
secretCode = '1234'
global input
input = ''

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1

class Keypad():

  def __init__(self, L1, L2, L3, L4, C1, C2, C3, C4):
    self.L1 = L1
    self.L2 = L2
    self.L3 = L3
    self.L4 = L4
    self.C1 = C1
    self.C2 = C2
    self.C3 = C3
    self.C4 = C4

    
    # Setup GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(self.L1, GPIO.OUT)
    GPIO.setup(self.L2, GPIO.OUT)
    GPIO.setup(self.L3, GPIO.OUT)
    GPIO.setup(self.L4, GPIO.OUT)

    # Use the internal pull-down resistors
    GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



  #def read():
    # **INSERTED FROM TREVOR TO READ FROM FILE**
  #  with open('pinData.txt', 'w') as pinDataRead:
  #          pinData = json.load(pinDataRead)
  #          secretCode = pinData['pin']
    #secretCode = "1234"
  #  input = ""
 # secretCode = '1234'

  # This callback registers the key that was pressed
  # if no other key is currently pressed
  def keypadCallback(self, channel):
      global keypadPressed
      if keypadPressed == -1:
          keypadPressed = channel

  def detection(self):
  # Detect the rising edges on the column lines of the
  # keypad. This way, we can detect if the user presses
  # a button when we send a pulse.
    GPIO.add_event_detect(self.C1, GPIO.RISING, callback=keypadCallback)
    GPIO.add_event_detect(self.C2, GPIO.RISING, callback=keypadCallback)
    GPIO.add_event_detect(self.C3, GPIO.RISING, callback=keypadCallback)
    GPIO.add_event_detect(self.C4, GPIO.RISING, callback=keypadCallback)

  # Sets all lines to a specific state. This is a helper
  # for detecting when the user releases a button
  def setAllLines(self, state):
      GPIO.output(self.L1, state)
      GPIO.output(self.L2, state)
      GPIO.output(self.L3, state)
      GPIO.output(self.L4, state)

  def checkSpecialKeys(self):
      input = ''
      global secretCode
      pressed = False

      GPIO.output(self.L3, GPIO.HIGH)

      if (GPIO.input(self.C4) == 1):
          print(input)
          print("Input reset!");
          pressed = True

      GPIO.output(self.L3, GPIO.LOW)
          #new code for changing secrete code (decided against this method for better secruity)
  #end of new code
      GPIO.output(self.L1, GPIO.HIGH)

      if (not pressed and GPIO.input(self.C4) == 1):
          if input == secretCode:
              print("Code correct!")
              # TODO: Unlock a door, turn a light on, etc.
          else:
              print("Incorrect code!")
              print("this is input" + input)
          pressed = True

      GPIO.output(self.L3, GPIO.LOW)

      if pressed:
          input = ""

      return pressed

  # reads the columns and appends the value, that corresponds
  # to the button, to a variable
  def readLine(self, line, characters):
      global input 
      input = '15'
      # We have to send a pulse on each line to
      # detect button presses
      GPIO.output(line, GPIO.HIGH)
      if(GPIO.input(self.C1) == 1):
          input = input + str(characters[0])
      if(GPIO.input(self.C2) == 1):
          input = input + str(characters[1])
      if(GPIO.input(self.C3) == 1):
          input = input + str(characters[2])
      if(GPIO.input(self.C4) == 1):
          input = input + str(characters[3])
      GPIO.output(line, GPIO.LOW)


key = Keypad(L1, L2, L3, L4, C1, C2, C3, C4)
try:
    while True:
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            key.setAllLines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
        # Otherwise, just read the input
        else:
            if not key.checkSpecialKeys():
                one = key.readLine(L1, ["1","2","3","A"])
                two = key.readLine(L2, ["4","5","6","B"])
                three = key.readLine(L3, ["7","8","9","C"])
                four = key.readLine(L4, ["*","0","#","D"])
                time.sleep(0.1)
            else:
                time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\nApplication stopped!")

'''
Traceback (most recent call last):
  File "keyclass.py", line 154, in <module>
    two = key.readLine(L2, ["4","5","6","B"])
  File "keyclass.py", line 133, in readLine
    input = input + characters[2]
TypeError: unsupported operand type(s) for +: 'builtin_function_or_method' and 'str'


Traceback (most recent call last):
  File "keyclass.py", line 153, in <module>
    one = key.readLine(L1, ["1","2","3","A"])
  File "keyclass.py", line 129, in readLine
    input = input + str(characters[0])
TypeError: unsupported operand type(s) for +: 'builtin_function_or_method' and 'str'
'''