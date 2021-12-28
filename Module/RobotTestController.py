from time import sleep
from Motor_Module import Motor
import Key_Press_Module as KP
# from JoyStickModule import get_joystick
################################### SETTING ###################################
motor = Motor(13, 22, 27, 12, 23, 24)
KP.init()
movement = ['Keyboard', 'Joystick']
moveSelect = movement[0]
################################################################################
def main():
    # Control by Keyboard
    if (moveSelect == movement[0]):
        if KP.getKey('UP'):         motor.move(speed=0.6, turn=0, delay=0.1)
        elif KP.getKey('DOWN'):     motor.move(speed=-0.6, turn=0, delay=0.1)
        elif KP.getKey('LEFT'):     motor.move(speed=0.5, turn=0.3, delay=0.1)
        elif KP.getKey('RIGHT'):    motor.move(speed=0.5, turn=-0.3, delay=0.1)
        else:                       motor.stop(0.1)

    # # Control by Joystick
    # else:
    #     print(get_joystick())
    #     jsVal = get_joystick()
    #     #motor.move(speed=jsVal['AXIS1'], turn=jsVal['AXIS0'], delay=0.1)
    #     motor.move(speed=-jsVal['AXIS1']*0.1, turn=-jsVal['AXIS0']*0.1, delay=0.1)

if __name__ == '__main__':
    while True:
        main()
################################################################################
