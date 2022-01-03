import pygame
from time import sleep
from pygame import joystick
################################################################################
pygame.init() # # Initialize Py game
controller = pygame.joystick.Joystick(0)
controller.init()

# Pygame -> Detects the values of the joystick and sends out the values
# Buttons: 0: Not pressed, 1: Pressed
# Axes: -1.0 -> 1.0 (Float) | [Up/Down]ward, Left/Right
buttons = {
    'SQUARE': 0, 'X': 0, 'CIRCLE': 0, 'TRIANGLE': 0, 
    'LEFT1': 0, 'RIGHT1': 0, 'LEFT2': 0., 'RIGHT2': 0.,
    'SHARE': 0, 'OPTIONS': 0, 'LEFT_STICK': 0, 'RIGHT_STICK': 0, 'PS': 0,  
    'AXIS0': 0., 'AXIS1': 0., 'AXIS2': 0., 'AXIS5': 0.
}
################################################################################
def get_joystick(name = ''):
    global buttons
    MY_BUTTONS = ['SQUARE', 'X', 'CIRCLE', 'TRIANGLE', 
                    'LEFT1', 'RIGHT1', 'LEFT2', 'RIGHT2',
                    'SHARE', 'OPTIONS', 'LEFT_STICK', 'RIGHT_STICK', 'PS',  
                    'AXIS0', 'AXIS1', 'AXIS2', 'AXIS5']

    MY_HATS = { 'LEFT': (-1, 0), 'RIGHT': (1, 0), 'UP': (0, 1),
                'DOWN': (0, -1), '... RELEASE': (0, 0) }
    events = pygame.event.get()

    # Retrieve any events ...
    for event in events:
        # When Analog Sticks (Joy) rotated
        if event.type == pygame.JOYAXISMOTION:
            #print(f'Axis: {event.axis} | Value: {event.value}')
            print(f'===> [AXIS] {event.axis}: {round(event.value, 3)}')
            if (event.axis == 3):
                buttons[f'LEFT2'] = round(event.value, 3)
            elif (event.axis == 4):
                buttons[f'RIGHT2'] = round(event.value, 3)
            else:
                buttons[f'AXIS{event.axis}'] = round(event.value, 3)

        elif event.type == pygame.JOYBALLMOTION:
            print(f'Joy: {event.joy} | Ball: {event.ball} | Rel: {event.rel}')

        # When Button pressed
        elif event.type == pygame.JOYBUTTONDOWN:
            
            #print(f'Button: {event.button} pressed')
            print(f'===> [BUTTON-{event.button}][PRESS] {MY_BUTTONS[event.button]}')
            buttons[MY_BUTTONS[event.button]] = 1

        elif event.type == pygame.JOYBUTTONUP:
            #print(f'Button: {event.button} released')
            print(f'===> [BUTTON-{event.button}][RELEASE] {MY_BUTTONS[event.button]}')
            buttons[MY_BUTTONS[event.button]] = 0

        elif (event.type == pygame.JOYHATMOTION) and (event.hat == 0):
            for i, (hatKey, hatValue) in enumerate(MY_HATS.items()):
                if (event.value == hatValue):    print(f'===> [HAT][PRESS] {hatKey}')

    # Do not ask for anything => Getting all values
    if (name == ''):
        return buttons
    # Ask for a particular key => Getting a single value
    else:
        return buttons[name]
################################################################################
def main():
    get_joystick()
    print(buttons)
    sleep(1)

if __name__ == '__main__':
    while True:
        main()
################################################################################

