"""
- HSV is a color space that closely aligns with the way humans perceive
- Hue: Color | Saturation: How pure the color is | Value: How bright the color is
- Get a range of colors from these HSV values so we can detect a particular color
  + Range: Minimum -> Maximum for each H, S, V element
  + We don't know these values, we have to play around with them until we get the desired results
  + Using Trackbar (Slider)
  + Hue: 0 -> 179, Saturation|Value: 0 -> 255
- We want to keep the color that we want to detect in the resultant image 
"""
############################################
import cv2
import numpy as np
import utlis

############################################
trackbar_name_hsv = "Trackbar - HSV_Color"
trackbar_init_values_hsv = [0, 0, 185]  # Default value (min) for each H, S, V element
############################################
def empty_function(a):
    pass

def trackbar_init_HSV():
    cv2.namedWindow(trackbar_name_hsv)
    cv2.resizeWindow(trackbar_name_hsv, 300, 130)
    cv2.createTrackbar("Hue",        trackbar_name_hsv, trackbar_init_values_hsv[0], 179, empty_function)
    cv2.createTrackbar("Saturation", trackbar_name_hsv, trackbar_init_values_hsv[1], 255, empty_function)
    cv2.createTrackbar("Value",      trackbar_name_hsv, trackbar_init_values_hsv[2], 255, empty_function)

def trackbar_get_value_HSV():
    hue = cv2.getTrackbarPos("Hue",               trackbar_name_hsv)
    saturation = cv2.getTrackbarPos("Saturation", trackbar_name_hsv)
    value = cv2.getTrackbarPos("Value",           trackbar_name_hsv)

    return hue, saturation, value

def HSV_converter(originalImg):
    # Converting image from BGR -> HSV. Getting white area
    imgHsv = cv2.cvtColor(originalImg, cv2.COLOR_BGR2HSV)
    hue, saturation, value = trackbar_get_value_HSV()

    # Create a mask only has the values that are in range 
    # Applying a range in which we want the color to be
    lowerWhite = np.array([hue, saturation, value])
    upperWhite = np.array([179, 255, 255])
    # Give only the values that are in range of these variables. Get the values from this HSV image 
    # Use this mask to output the the final results of colored object 
    maskWhite = cv2.inRange(imgHsv, lowerWhite, upperWhite)
    
    # Keep whatever is present in both of them, skip the rest of the things
    imgHsvResult = cv2.bitwise_and(originalImg, originalImg, mask=maskWhite)

    return imgHsv, maskWhite, imgHsvResult

############################################
trackbar_init_HSV()
############################################
def main():
    cap = cv2.VideoCapture(r'C:\Users\Doan Trong Hieu\Downloads\IMPORTANT\SPECIALIZATION\Self_Driving_Cars\MURTAZA\SOURCE\test_lane_rasp_pi.mp4')
    frameCounter = 0
    cap.set(3, 480)
    cap.set(4, 240)

    while True:
        # Capture frame-by-frame of video
        _, img = cap.read()
        frameCounter += 1

        # If the last frame is reached, reset the capture and the frameCounter
        if (frameCounter == cap.get(cv2.CAP_PROP_FRAME_COUNT)):
            # Or whatever as long as it is the same as next line
            frameCounter = 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        imgHsv, maskWhite, imgHsvResult = HSV_converter(img)

        imgHsvStack = utlis.stackImages(0.6, ([img, imgHsv], [maskWhite, imgHsvResult]))
        cv2.imshow("Stacked Images", imgHsvStack)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
############################################