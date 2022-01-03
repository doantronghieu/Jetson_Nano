from time import sleep
from Motor_Module import Motor
import Key_Press_Module as KP
from JoyStickModule import get_joystick
################################### SETTING ###################################
motor = Motor(12, 16, 20, 13, 19, 26)
KP.init()
movement = ['Keyboard', 'Joystick']
moveSelect = movement[1]
################################################################################
def main():
    # Control by Keyboard
    if (moveSelect == movement[0]):
        if KP.getKey('UP'):         motor.move(speed=0.6, turn=0, run_time=0.1)
        elif KP.getKey('DOWN'):     motor.move(speed=-0.6, turn=0, run_time=0.1)
        elif KP.getKey('LEFT'):     motor.move(speed=0.5, turn=-0.5, run_time=0.1)
        elif KP.getKey('RIGHT'):    motor.move(speed=0.5, turn=0.5, run_time=0.1)
        else:                       motor.stop(0.1)

    # Control by Joystick
    else:
        print(get_joystick())
        jsVal = get_joystick()
        motor.move(speed=-jsVal['AXIS1'], turn=jsVal['AXIS0'], run_time=0.1)

if __name__ == '__main__':
    while True:
        main()
################################################################################
