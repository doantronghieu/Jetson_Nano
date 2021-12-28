import cv2
import imutils
################################################################################
cap = cv2.VideoCapture(0)
frameWidth, frameHeight = 960, 480
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def get_image(display = False, resize = False, size = [480, 240]):
    success, img = cap.read()

    if display:
        cv2.imshow('Image', img)
    if resize:
        img = imutils.resize(img, width=size[0],height=size[1])

    cv2.imwrite('/home/pi/Documents/Self_Driving_Car/Murtaza/fixImg1.jpg', img)

    return img
################################################################################
def main():
    while True:
        img = get_image(display = True)

        if (cv2.waitKey(1) and 0xFF == ord('q')):
            break

if __name__ == '__main__':
    main()
