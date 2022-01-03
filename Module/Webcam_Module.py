import cv2
import imutils
################################################################################
frameWidth, frameHeight = 960, 480

gst_str = ('nvarguscamerasrc ! ' + 'video/x-raw(memory:NVMM), ' +
          'width=(int)1920, height=(int)1080, ' +
          'format=(string)NV12, framerate=(fraction)30/1 ! ' + 
          'nvvidconv flip-method=2 ! ' + 
          'video/x-raw, width=(int){}, height=(int){}, ' + 
          'format=(string)BGRx ! ' +
          'videoconvert ! appsink').format(frameWidth, frameHeight)

cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER) 

def get_image(display = False, resize = False, size = [480, 240]):
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    
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