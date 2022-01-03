import Jetson.GPIO as GPIO
from time import sleep # For delay
from adafruit_servokit import ServoKit
import board
import busio
from numpy import interp
###############################################################################
GPIO.setwarnings = False
# ENA, IN1, IN2, ENB, IN3, IN4 = 12, 16, 20, 13, 19, 26

"""
- On the Jetson Nano
- Bus 0 (pins 28,27) is board SCL_1, SDA_1 in the jetson board definition file
- Bus 1 (pins 5, 3) is board SCL, SDA in the jetson definition file
- Default is to Bus 1; We are using Bus 0, so we need to construct the busio first ...
"""
print("Initializing Servos")
i2c_bus0 = (busio.I2C(board.SCL_1, board.SDA_1))
print("Initializing ServoKit")
kit = ServoKit(channels = 16, i2c = i2c_bus0)
# kit[0] is the servo number 01, kit[1] is the servo number 02
print("Done initializing ServoKit")
###############################################################################
class Motor():
    # Initialization | Enable pin: Speed | Input pin: Direction
    def __init__(self, ENA, IN1, IN2, ENB, IN3, IN4):
        GPIO.setmode(GPIO.BCM)
        # GPIO.setmode(GPIO.BOARD)

        # self -> Referencing to this instance of the class
        # a & b for Left & Right motors
        self.ENA, self.IN1, self.IN2 = ENA, IN1, IN2
        self.ENB, self.IN3, self.IN4 = ENB, IN3, IN4

        # Declaring pins as outputs
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENB, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)

        # PWM pin is Enable pin
        # Originally, speed is zero
        self.PWMa = GPIO.PWM(channel=self.ENA, frequency_hz=1000)
        self.PWMb = GPIO.PWM(channel=self.ENB, frequency_hz=1000)
        self.PWMa.start(duty_cycle_percent=0)
        self.PWMb.start(duty_cycle_percent=0)
        self.mySpeed = 0
    
    def move(self, speed = 0.5, turn = 0, runTime = 0): # Using normalized value
        
        # Normalization: -1 -> 1. For further using ...
        # Speed: -1 -> 1 in Pos/Neg direction
        # Turn: -1 -> 1 | Pos -> Right | Neg -> Left

        # Bring the values back for the ChangeDutyCycle understands
        # Changing duty cycle to run motors
        speed *= 100
        self.PWMa.ChangeDutyCycle(abs(speed))
        self.PWMb.ChangeDutyCycle(abs(speed))
        GPIO.output(channels=self.IN1, values=GPIO.HIGH)
        GPIO.output(channels=self.IN2, values=GPIO.LOW)
        GPIO.output(channels=self.IN3, values=GPIO.HIGH)
        GPIO.output(channels=self.IN4, values=GPIO.LOW)
        
        systemSteering = [-0.75, 0.95]  # Real steering of the system
        normalizedSteering = [-1, 1]    # Normalized steering value for easily using
        turn = round(number=interp(turn, normalizedSteering, systemSteering), ndigits=3)
        kit.continuous_servo[0].throttle = turn
        
        sleep(runTime)

    def stop(self, time = 0):
        self.PWMa.ChangeDutyCycle(0)
        self.PWMb.ChangeDutyCycle(0)
        self.mySpeed = 0
        sleep(time)

###############################################################################
def main():
    # Creating instance
    motor = Motor(12, 16, 20, 13, 19, 26)
    # motor = Motor(32, 36, 38, 33, 35, 37)
    motor.move(speed=1, turn=0.1, runTime=5)
    motor.move(speed=1, turn=-0.5, runTime=5)
    motor.move(speed=1, turn=0.1, runTime=5)
    motor.move(speed=1, turn=0.5, runTime=5)
    motor.move(speed=1, turn=0.05, runTime=5)

if (__name__ == '__main__'):
    main()
    