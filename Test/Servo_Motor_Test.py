from adafruit_servokit import ServoKit
import board
import busio
import time

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
while True:
    degree = float(input('>> Angle: '))
    # kit.servo[0].angle = degree
    # kit.servo[0].angle = 180
    # kit.continuous_servo[0].throttle = degree
    kit.continuous_servo[0].throttle = degree
    
    # if (angle == 0):
    #     break
    # sweep = range(0, 180)
    # for degree in sweep :
    #     kit.servo[0].angle = degree
    #     time.sleep(0.01)
        
    # sweep = range(180, 0, -1)
    # for degree in sweep :
    #     kit.servo[0].angle = degree
    #     time.sleep(0.01)
