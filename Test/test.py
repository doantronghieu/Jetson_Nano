import Jetson.GPIO as GPIO
import time

GPIO.setwarnings = False
GPIO.setmode(GPIO.BCM)
ENA, IN1, IN2, ENB, IN3, IN4 = 12, 16, 20, 13, 19, 26

"""
- The default speed & direction of motor is LOW & Forward
- r-run: run or start the motor
- s-stop: stop the motor
- f-forward: run the motor in forward direction
- b-backward: reverse the direction of rotation
- l-low: decrease the speed to 25%
- m-medium: run the motor at medium speed 50%
- h-high: increase the speed to 75% level
- e-exit: stop the motor and exit 
"""
isForward = 1

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

# Create PWM object: Pin & How fast to go
PWMA = GPIO.PWM(channel=ENA, frequency_hz=1000)
PWMB = GPIO.PWM(channel=ENB, frequency_hz=1000)
# The percent duty cycle we want
PWMA.start(duty_cycle_percent=25)
PWMB.start(duty_cycle_percent=25)

while(1):
    x = input('>> Command: ')
    
    if (x == 'r'):
        print('RUN')
        if (isForward == 1):
            GPIO.output(channels=IN1, values=GPIO.HIGH)
            GPIO.output(channels=IN2, values=GPIO.LOW)
            GPIO.output(channels=IN3, values=GPIO.HIGH)
            GPIO.output(channels=IN4, values=GPIO.LOW)
            print('FORWARD')
            x = 'z'
            
        else:
            GPIO.output(channels=IN1, values=GPIO.LOW)
            GPIO.output(channels=IN2, values=GPIO.HIGH)
            GPIO.output(channels=IN3, values=GPIO.LOW)
            GPIO.output(channels=IN4, values=GPIO.HIGH)
            print('BACKWARD')
            x = 'z'
            
    elif (x == 's'):
        print('STOP')
        GPIO.output(channels=IN1, values=GPIO.LOW)
        GPIO.output(channels=IN2, values=GPIO.LOW)
        GPIO.output(channels=IN3, values=GPIO.LOW)
        GPIO.output(channels=IN4, values=GPIO.LOW)
        x = 'z'
    
    elif (x == 'f'):
        print('FORWARD')
        GPIO.output(channels=IN1, values=GPIO.HIGH)
        GPIO.output(channels=IN2, values=GPIO.LOW)
        GPIO.output(channels=IN3, values=GPIO.HIGH)
        GPIO.output(channels=IN4, values=GPIO.LOW)
        isForward = 1
        x = 'z'
    
    elif (x == 'b'):
        print('BACKWARD')
        GPIO.output(channels=IN1, values=GPIO.LOW)
        GPIO.output(channels=IN2, values=GPIO.HIGH)
        GPIO.output(channels=IN3, values=GPIO.LOW)
        GPIO.output(channels=IN4, values=GPIO.HIGH)
        isForward = 0
        x = 'z'
    
    elif (x == 'l'):
        print('LOW')
        PWMA.ChangeDutyCycle(duty_cycle_percent=25)
        PWMB.ChangeDutyCycle(duty_cycle_percent=25)
        x = 'z'
    
    elif (x == 'm'):
        print('MEDIUM')
        PWMA.ChangeDutyCycle(duty_cycle_percent=50)
        PWMB.ChangeDutyCycle(duty_cycle_percent=50)
        x = 'z'
    
    elif (x == 'h'):
        print('HIGH')
        PWMA.ChangeDutyCycle(duty_cycle_percent=100)
        PWMB.ChangeDutyCycle(duty_cycle_percent=75)
        x = 'z'
    
    elif (x == 'e'):
        GPIO.cleanup()
        break
    
    else:
        print('Wrong data. Please enter the defined data to continue.')
    