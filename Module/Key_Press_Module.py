import pygame
################################################################################
def init():
    # Creating a window of 100x100
    # We cannot detect the keypress unless we have a window to detect on
    pygame.init()
    win = pygame.display.set_mode((100, 100))

def getKey(keyName):
    answer = False
    # Getting all the events
    for eve in pygame.event.get():
        pass
    # Detecting the get pressed event
    keyInput = pygame.key.get_pressed()
    # Check the keyName
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    # Checking which key was press
    if keyInput [myKey]:
        answer = True
    pygame.display.update()
    return answer
################################################################################
def main():
    if getKey('UP'):
        print('Key UP was pressed')
    if getKey('DOWN'):
        print('Key DOWN was pressed')
    if getKey('LEFT'):
        print('Key LEFT was pressed')
    if getKey('RIGHT'):
        print('Key RIGHT was pressed')

if __name__ == '__main__':
    init()
    while True:
        main()
