import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class Motor():

  pins = []

  def __init__(self, pins):
    self.pins = pins # controller inputs: in1, in2, in3, in4
    GPIO.setmode(GPIO.BCM)
    for pin in self.pins:
      GPIO.setup(pin, GPIO.OUT, initial=0)

  def delay_us(self, tus): # use microseconds to improve time resolution
    endTime = time.time() + float(tus)/ float(1E6)
    while time.time() < endTime:
      pass

  # Make a full rotation of the output shaft:
  def loop(self, dir): # dir = rotation direction (cw or ccw)
    for i in range(512): # full revolution (8 cycles/rotation * 64 gear ratio)
      for halfstep in range(8): # 8 half-steps per cycle
        for pin in range(4):    # 4 pins that need to be energized
          GPIO.output(self.pins[pin], dir[halfstep][pin])
        self.delay_us(1000)




