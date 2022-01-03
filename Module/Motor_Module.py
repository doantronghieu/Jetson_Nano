import Jetson.GPIO as GPIO # Allows us to interface with the GPIO pins
from time import sleep # For delay
from adafruit_servokit import ServoKit
import board
import busio
###############################################################################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# On the Jetson Nano
# Bus 0 (pins 28,27) is board SCL_1, SDA_1 in the jetson board definition file
# Bus 1 (pins 5, 3) is board SCL, SDA in the jetson definition file
# Default is to Bus 1; We are using Bus 0, so we need to construct the busio first ...
print("Initializing Servos")
i2c_bus0 = (busio.I2C(board.SCL_1, board.SDA_1))
print("Initializing ServoKit")
kit = ServoKit(channels = 16, i2c = i2c_bus0)
# kit[0] is the servo number 01, kit[1] is the servo number 02
print("Done initializing")
###############################################################################
class Motor():
    # Initialization | Enable pin: Speed | Input pin: Direction
    def __init__(self, ENA, IN1, IN2, ENB, IN3, IN4):

        # self -> Referencing to this instance of the class
        # a & b for Left & Right motors
        self.ENA, self.IN1, self.IN2 = ENA, IN1, IN2
        self.ENB, self.IN3, self.IN4 = ENB, IN3, IN4

        # Declaring pins as outputs
        GPIO.setup(ENA, GPIO.OUT)
        GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ENB, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

        # PWM pin is ENBle pin. 100 if Frequency
        # Originally, speed is zero
        self.PWMa = GPIO.PWM(channel=self.ENA, frequency_hz=1000)
        self.PWMb = GPIO.PWM(channel=self.ENB, frequency_hz=1000)
        # The percent duty cycle we want
        self.PWMa.start(duty_cycle_percent=0)
        self.PWMb.start(duty_cycle_percent=0)

    def move(self, speed = 0.5, turn = 0, run_time = 0): # Using normalized value
        # Normalization: -1 -> 1. For further using ...
        # Speed: -1 -> 1 in Pos/Neg direction
        # Turn: -1 -> 1 | Pos -> Left | Neg -> Right

        kit.continuous_servo[0].throttle = turn
        
        # Bring the values back for the ChangeDutyCycle understands
        speed *= 100
        
        if (speed > 0):
            GPIO.output(channels=self.IN1, values=GPIO.HIGH)
            GPIO.output(channels=self.IN2, values=GPIO.LOW)
            GPIO.output(channels=self.IN3, values=GPIO.HIGH)
            GPIO.output(channels=self.IN4, values=GPIO.LOW)
        elif (speed < 0):
            GPIO.output(channels=self.IN1, values=GPIO.LOW)
            GPIO.output(channels=self.IN2, values=GPIO.HIGH)
            GPIO.output(channels=self.IN3, values=GPIO.LOW)
            GPIO.output(channels=self.IN4, values=GPIO.HIGH)
        
        self.PWMa.ChangeDutyCycle(duty_cycle_percent=abs(speed))
        self.PWMb.ChangeDutyCycle(duty_cycle_percent=abs(speed))
        
        sleep(run_time)

    def stop(self, time = 0):
        self.PWMa.ChangeDutyCycle(0)
        self.PWMb.ChangeDutyCycle(0)
        self.mySpeed = 0
        sleep(time)
###############################################################################
def main():
    motor.move(speed=1, turn=0.1, run_time=3)
    motor.move(speed=1, turn=0.5, run_time=3)
    motor.move(speed=1, turn=0.1, run_time=3)
    motor.move(speed=1, turn=-0.5, run_time=3)
    motor.move(speed=1, turn=0.1, run_time=3)
    

if __name__ == '__main__':
    # Creating instance
    motor = Motor(12, 16, 20, 13, 19, 26)
    main()
###############################################################################
