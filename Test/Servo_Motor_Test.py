from adafruit_servokit import ServoKit
import board
import busio
import time
import cv2
###############################################################################
trackbarNameServo = 'Trackbar - Servo'

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
def empty_function(a):
    pass

# def trackbar_init_servo():
#     servoSteering_init = 0
#     cv2.namedWindow(trackbarNameServo)
#     cv2.resizeWindow(trackbarNameServo, 300, 130)
#     cv2.createTrackbar("Steering Angle", trackbarNameServo, servoSteering_init, 1, 
#                        empty_function)

# def trackbar_get_value_servo():
#     servoSteering = cv2.getTrackbarPos(trackbarname="Steering Angle", winname=trackbarNameServo)
#     return servoSteering
    
###############################################################################
def main():
    while True:
        steering = float(input('>> Angle: '))
        # trackbar_init_servo()

        # steering = trackbar_get_value_servo()
        kit.continuous_servo[0].throttle = steering
        
    
if __name__ == '__main__':
    main()