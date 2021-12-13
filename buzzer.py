import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BUZZER= 13
buzzState = False
GPIO.setup(BUZZER, GPIO.OUT)

while True:
    buzzState = not buzzState
    GPIO.output(BUZZER, buzzState)
    time.sleep(1)

# def buzzer(BUZZER):
#     GPIO.setwarnings(False)
#     #BUZZER= 13
#     buzzState = True
#     GPIO.setup(BUZZER, GPIO.OUT)
#     for i in range (3):
#         GPIO.output(BUZZER, buzzState)
#         time.sleep(.1)
#         GPIO.output(BUZZER, False)