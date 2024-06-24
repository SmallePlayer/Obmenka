import RPi.GPIO as GPIO
from time import sleep
        
left_motor_forward = 13
left_motor_back = 19
right_motor_forward = 12
right_motor_back = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(left_motor_forward, GPIO.OUT)
GPIO.setup(left_motor_back, GPIO.OUT)
GPIO.setup(right_motor_forward, GPIO.OUT)
GPIO.setup(right_motor_back, GPIO.OUT)
pwml = GPIO.PWM(left_motor_forward, 50)
pwmr = GPIO.PWM(right_motor_forward, 50)
pwml.start(0)
pwmr.start(0)

def move_right():
    pwml.ChangeDutyCycle(50)
    GPIO.output(left_motor_back, GPIO.LOW)
    pwmr.ChangeDutyCycle(0)
    GPIO.output(right_motor_back, GPIO.LOW)

def move_left():
    pwml.ChangeDutyCycle(0)
    GPIO.output(left_motor_back, GPIO.LOW)
    pwmr.ChangeDutyCycle(50)
    GPIO.output(right_motor_back, GPIO.LOW)

def move_forward():
    pwml.ChangeDutyCycle(50)
    GPIO.output(left_motor_back, GPIO.LOW)
    pwmr.ChangeDutyCycle(50)
    GPIO.output(right_motor_back, GPIO.LOW)

def stop():
    pwml.ChangeDutyCycle(0)
    GPIO.output(left_motor_back, GPIO.LOW)
    pwmr.ChangeDutyCycle(0)
    GPIO.output(right_motor_back, GPIO.LOW)

def time_sleep():
    sleep(2)

move_forward()
time_sleep()
move_right()
time_sleep()
move_left()
time_sleep()
stop()





GPIO.cleanup()