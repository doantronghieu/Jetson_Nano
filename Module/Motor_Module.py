import Jetson.GPIO as GPIO
from time import sleep # For delay
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
###############################################################################
class Motor():
    # Initialization | Enable pin: Speed | Input pin: Direction
    def __init__(self, ENAa, IN1a, IN2a, ENAb, IN1b, IN2b):
        # self -> Referencing to this instance of the class
        # a & b for Left & Right motors
        self.ENAa, self.IN1a, self.IN2a = ENAa, IN1a, IN2a
        self.ENAb, self.IN1b, self.IN2b = ENAb, IN1b, IN2b

        # Declaring pins as outputs
        GPIO.setup(self.ENAa, GPIO.OUT)
        GPIO.setup(self.IN1a, GPIO.OUT)
        GPIO.setup(self.IN2a, GPIO.OUT)
        GPIO.setup(self.ENAb, GPIO.OUT)
        GPIO.setup(self.IN1b, GPIO.OUT)
        GPIO.setup(self.IN2b, GPIO.OUT)

        # PWM pin is Enable pin. 100 if Frequency
        # Originally, speed is zero
        self.PWMa, self.PWMb = GPIO.PWM(self.ENAa, 100), GPIO.PWM(self.ENAb, 100)
        self.PWMa.start(0)
        self.PWMb.start(0)
        self.mySpeed = 0

    def move(self, speed = 0.5, turn = 0, delay = 0): # Using normalized value
        # Normalization: -1 -> 1. For further using ...
        # Speed: -1 -> 1 in Pos/Neg direction
        # Turn: -1 -> 1 | Pos -> Left | Neg -> Right

        # Bring the values back for the ChangeDutyCycle understands
        speed *= 100
        turn *= 100

        # Speeds depend on our turn
        # right > left -> Turning left | left > right -> Turning right | left = right -> Moving forward
        leftSpeed = speed - turn
        rightSpeed = speed + turn

        # The value might be more than 100 and less than -100
        # Limiting the values from -100 -> 100
        if (leftSpeed > 100):       leftSpeed = 100
        elif (leftSpeed < -100):    leftSpeed = -100
        if (rightSpeed > 100):      rightSpeed = 100
        elif (rightSpeed < -100):   rightSpeed = -100


        # Changing duty cycle to run motors
        # ChangeDutyCycle does not understand negative values -> Abs
        self.PWMa.ChangeDutyCycle(abs(leftSpeed))
        self.PWMb.ChangeDutyCycle(abs(rightSpeed))

        # If the values is negative -> Change direction
        if (leftSpeed > 0):
            GPIO.output(self.IN1a, GPIO.LOW)
            GPIO.output(self.IN2a, GPIO.HIGH)
        else:
            GPIO.output(self.IN1a, GPIO.HIGH)
            GPIO.output(self.IN2a, GPIO.LOW)

        if (rightSpeed > 0):
            GPIO.output(self.IN1b, GPIO.LOW)
            GPIO.output(self.IN2b, GPIO.HIGH)
        else:
            GPIO.output(self.IN1b, GPIO.HIGH)
            GPIO.output(self.IN2b, GPIO.LOW)

        sleep(delay)

    def stop(self, time = 0):
        self.PWMa.ChangeDutyCycle(0)
        self.PWMb.ChangeDutyCycle(0)
        self.mySpeed = 0
        sleep(time)
###############################################################################
def main():
    motor.move(0.6, 0, 2)
    motor.stop(time=0)
    motor.move(-0.5, 0.2, 2)
    motor.stop(time=0)

if __name__ == '__main__':
    # Creating instance
    motor = Motor(2, 3, 4, 17, 22, 27)
    main()
###############################################################################
