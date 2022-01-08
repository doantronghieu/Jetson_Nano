import cv2
import numpy as np
import imutils
import utlis
np.set_printoptions(threshold=np.inf)
import Webcam_Module as wcM
import math
################################################################################
# Defining Region of Interest
# The height should not be too far, we don't want to know what is the curve later on, we want to know what is the curve right now
utlis.trackbar_init_warp()
utlis.trackbar_init_HSV()
utlis.trackbar_init_params()

################################### FUNCTION ###################################
def make_coordinates(image, slopeAndIntercept):
    # Finding x & y coordinates from slope and intercept
    slope, intercept = slopeAndIntercept
    height, width, _ = image.shape

    y1 = height            # Bottom of the image
    y2 = int(y1 * (1 / 2)) # Make points from middle of the frame down

    if (intercept == float('inf')) or (intercept == float('-inf')):
        intercept = 1
    if (slope == float('inf')) or (slope == float('-inf')):
        slope = 1

    # y = mx + b
    x1, x2 = int((y1 - intercept) / slope), int((y2 - intercept) / slope)

    # Bound the coordinates within the image
    x1, x2 = max(-width, min(2 * width, x1)), max(-width, min(2 * width, x2))

    return [[x1, y1, x2, y2]]

def region_of_interest(thresholedImg):
    pointsROI = utlis.trackbar_get_value_warp()
    pointsROI = [(pointsROI[0][0], pointsROI[0][1]), (pointsROI[1][0], pointsROI[1][1]),
        (pointsROI[2][0], pointsROI[2][1]), (pointsROI[3][0], pointsROI[3][1])]
    ROI = np.array([[pointsROI[0], pointsROI[2], pointsROI[3], pointsROI[1]]], dtype=np.int32)
    # LOOK FOR LINES ONLY AT THAT REGION AND NOT IN THE ENTIRE FRAME
    mask = np.zeros_like(thresholedImg)
    cv2.fillPoly(mask, ROI, (255, 255, 255))
    croppedEdges = cv2.bitwise_and(thresholedImg, mask)
    
    cv2.circle(img=croppedEdges, center=pointsROI[0], radius=10, color=(255, 255, 255), thickness=cv2.FILLED)
    cv2.circle(img=croppedEdges, center=pointsROI[2], radius=10, color=(255, 255, 255), thickness=cv2.FILLED)
    cv2.circle(img=croppedEdges, center=pointsROI[3], radius=10, color=(255, 255, 255), thickness=cv2.FILLED)
    cv2.circle(img=croppedEdges, center=pointsROI[1], radius=10, color=(255, 255, 255), thickness=cv2.FILLED)
    
    return croppedEdges

def average_slope_intercept(image, lines):
    """
    - This part combines line segments into one or two lane lines
    - If all line slopes are < 0: then we only have detected left lane
    - If all line slopes are > 0: then we only have detected right lane
    """

    # Coordinates of the average lines on the left/right
    # Containing the slope and y intercept of the lines of left/right side
    leftMY, rightMY, laneLines = [], [], []
    boundary = 1/3
    height, width, _ = image.shape

    if (lines is None):
        return laneLines

    # Left lane line segment should be on left 2/3 of the screen
    leftRegionBoundary = width * (1 - boundary)
    # Right lane line segment should be on right 2/3 of the screen
    rightRegionBoundary = width * boundary

    if (lines is not None):
        # Unpack. Reshape each line into a one dimensional array with 4 elements
        for line in lines:
            for x1, y1, x2, y2 in line:
                """ VERTICAL LINE SEGMENTS
                - When car is turning
                - Slope of infinity, can not average them with the slopes of other line segments
                """
                if x1 == x2: continue # Skipping/Ignoring vertical line segment

                # y = mx + b, m: slope, y: intercept
                parameters = np.polyfit((x1, x2), (y1, y2), 1)
                slope, intercept = parameters[0], parameters[1]

                # Check if the slope of that line corresponding to a line on the left or right side
                # slope: y2 - y1 / x2 - x1
                if (slope < 0): # x increases, y decreases
                    if (x1 < leftRegionBoundary) and (x2 < leftRegionBoundary):
                        leftMY.append((slope, intercept))
                else: # y & x increases
                    if (x1 > rightRegionBoundary) and (x2 > rightRegionBoundary):
                        rightMY.append((slope, intercept))

    # Averaging out all of slope & y intercept into a single slope and y intercept
    # Axis = 0 -> Operating vertically
    leftMYAverage, rightMYAverage = np.average(leftMY, axis=0), np.average(rightMY, axis=0)

    # Finding x and y for each line
    if (len(leftMY) > 0):
        leftLine = make_coordinates(image, leftMYAverage)
        laneLines.append(leftLine)
    if (len(rightMY) > 0):
        rightLine = make_coordinates(image, rightMYAverage)
        laneLines.append(rightLine)

    return laneLines

def display_lines(originalImg, linesDetected):
    # Display detected lines into real image
    onlyLinesImg = np.zeros_like(originalImg)
    pts = []
    height, width, _ = originalImg.shape

    if linesDetected is not None:
        # Check if it even detected any lines
        for line in linesDetected:
            # Reshaping all the lines to a 1D array
            for x1, y1, x2, y2 in line:
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Limiting the range of point's position
                if (x1 < 0):        x1 = 0
                elif (x1 > 480):    x1 = width
                if (x2 < 0):        x2 = 0
                elif (x2 > 480):    x2 = width
                if (y1 < 0):        y1 = 0
                elif (y1 > 240):    y1 = height
                if (y2 < 0):        y2 = 0
                elif (y2 > 240):    y2 = height

                if (len(line) > 0):
                    # Drawing each line onto the black img
                    cv2.line(onlyLinesImg, (x1, y1), (x2, y2), (0, 255, 255), 10)

                pts.append((x1, y1))
                pts.append((x2, y2))

    return onlyLinesImg

def heading_line_steering_angle(originalImg, laneLinesAvg):
    """
    - Try to steer the car to stay within the middle of the lane lines
    - Compute the steering angle, given the detected lane lines
    - Compute the heading direction by averaging the far endpoints of both lane lines
    - Heading line (x1,y1) is always center bottom of the screen
    - Assume the dashcam is installed in the middle of the car and pointing straight ahead
    - The lower end of the heading line is always in the middle of the bottom of the screen
    """
    headingImg = np.zeros_like(originalImg)
    height, width, _ = originalImg.shape
    yOffset = int(height / 2)
    cameraMidOffsetPercent = 0.000
    mid = int((width / 2) * (1 + cameraMidOffsetPercent))
    xOffset = mid

    # 0.0: Pointing to center | -0.1: Pointing to left | +0.1: Pointing to right

    ##########------ TWO DETECTED LANE LINES ------##########
    if (len(laneLinesAvg) == 2):
        x1Left, y1Left, x2Left, y2Left      = laneLinesAvg[0][0]
        x1Right, y1Right, x2Right, y2Right  = laneLinesAvg[1][0]

        xOffset = int((x2Left + x2Right) / 2 - mid)

        ##########------ ONE DETECTED LANE LINES ------##########
        """
        - If we only detected one lane line, can not do an average of two endpoints
        - When we see only one lane line, say only the left (right) lane
        - This means that we need to steer hard towards the right (left) to continue to follow the lane
        - Solution: Set the heading line to be the same slope as the only lane line
        """
    elif (len(laneLinesAvg) == 1):
        x1, y1, x2, y2 = laneLinesAvg[0][0]
        xOffset = x2 - x1

    ##########------ STEERING ANGLE ------##########
    """
    - Find the steering angle based on lane line coordinate
    - Known where the car are headed -> Convert that into the steering angle -> Tell the car to turn
    - 90 degrees: Heading straight | 45 to 89 degrees: Turning left | 91 to 135 degrees: Turning right
    """
    # Angle (in radian) to center vertical line
    angleToMidRadian = math.atan(xOffset / yOffset)
    # Angle (in degree) to center vertical line
    angleToMidDeg = int(angleToMidRadian * 180.0 / math.pi)
    steeringAngleDeg = angleToMidDeg
    steeringAngleRadian = steeringAngleDeg / 180.0 * math.pi

    if (len(laneLinesAvg) == 0): steeringAngleDeg = 0

    cv2.line(headingImg, pt1=(mid, height), pt2=(mid + xOffset, height - yOffset),
                      color=(0, 0, 255), thickness=10)
    return headingImg, steeringAngleDeg

def stabilize_steering_angle(currSteer, newSteer, numOfLaneLines,
                             maxAngleDeviationTwoLines = 5,
                             maxAngleDeviationOneLines = 1):
    """
    - Steering angles computed from one video frame to the next frame are not very stable
    - Stabilize steering: Turn the steering wheel in a smooth motion
    - Steering angle is sent as a continuous value to the car
    - If the new angle is more than max_angle_deviation degree from the current angle,
        just steer up to max_angle_deviation degree in the direction of the new angle
    - Using last steering angle to stabilize the steering angle
    - If new angle is too different from current angle,
        only turn by max_angle_deviation degrees
    """
    maxAngleDeviation = 1
    stabilizedSteeringAngle = currSteer

    # If both lane lines detected, then we can deviate more
    if (numOfLaneLines == 2):   maxAngleDeviation = maxAngleDeviationTwoLines
    # If only one lane detected, do not deviate too much
    else:                       maxAngleDeviation = maxAngleDeviationOneLines

    angleDeviation = newSteer - currSteer
    if (abs(angleDeviation) > maxAngleDeviation):
        stabilizedSteeringAngle = int(currSteer + maxAngleDeviation*angleDeviation/abs(angleDeviation))
    else:
        stabilizedSteeringAngle = newSteer

    return stabilizedSteeringAngle

def detect_lane_DSP(originalImg, display = False):
    ##########------ DETECT EDGES ------##########
    params = utlis.trackbar_get_value_params()
    # If Blur Kernel size is an even number -> Set it to odd
    if (params[0] % 2 == 0):
        params[0] += 1

    originalImg = imutils.resize(originalImg, width=480,height=240)
    tempImg = np.zeros_like(originalImg)
    imgThreshed = utlis.thresholdHSV(originalImg)

    # DETECT THE EDGES USING CANNY EDGE DETECTION
    # REMOVING NOISE
    blurImg = cv2.GaussianBlur(imgThreshed, (params[0], params[0]), 0)


    thresImg = cv2.Canny(blurImg, params[1], params[2])

    ##########------ ISOLATE REGION OF INTEREST ------##########
    croppedEdges = region_of_interest(thresImg)

    ##########------ DETECT LINE SEGMENTS ------##########
    lines = cv2.HoughLinesP(croppedEdges, 1, np.pi/180, params[3], np.array([]),
                            minLineLength=params[4], maxLineGap=params[5])

    ##########------ COMBINE LINE SEGMENTS INTO TWO LANE LINES ------##########
    onlyLinesImg = display_lines(originalImg, lines)
    laneLinesImg = cv2.addWeighted(originalImg, 0.8, onlyLinesImg, 1, 1)
    laneLinesAvg = average_slope_intercept(originalImg, lines)
    onlyLinesAvgImg = display_lines(originalImg, laneLinesAvg)
    laneLinesAvgImg = cv2.addWeighted(originalImg, 1, onlyLinesAvgImg, 0.5, 1)

    ##########------ MOTION PLANNING: STEERING ------##########
    headingLineImg, steeringAngleDeg = heading_line_steering_angle(originalImg, laneLinesAvg)
    headingLineImg = cv2.addWeighted(laneLinesAvgImg, 1, headingLineImg, 1, 1)
    print(steeringAngleDeg)
    ##########------ PIPELINE ------##########
    if display:
        stackedImgs = utlis.stackImages(0.7, ([originalImg, imgThreshed, thresImg],
                                              [croppedEdges, laneLinesImg, headingLineImg]))
        cv2.imshow('Stacked Image', stackedImgs)
    else:
        cv2.imshow('Stacked Image', headingLineImg)
    cv2.waitKey(1)

    return steeringAngleDeg
##################################### MAIN #####################################
def main():
    while True:
        orgImg = wcM.get_image(display = False, resize = False, size = [480, 240])
        detect_lane_DSP(orgImg, display = True)

        if (cv2.waitKey(1) and 0xFF == ord('q')):
            break

if __name__ == '__main__':
    main()
