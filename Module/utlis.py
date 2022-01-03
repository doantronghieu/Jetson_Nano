'''
- PIXEL SUMMATION:
 + Find the CENTER of the LANE
 + Add all the pixels of every column, get a value for it, each column's summation has an index

 + More number of pixel on the right -> The curve is on the right
 + Same number of pixel on the left and right -> Going straight
 + More number of pixel on the left -> The curve is on the right

- HSV is a color space that closely aligns with the way humans perceive
- Hue: Color | Saturation: How pure the color is | Value: How bright the color is
- Get a range of colors from these HSV values so we can detect a particular color
  + Range: Minimum -> Maximum for each H, S, V element
  + We don't know these values, we have to play around with them until we get the desired results
  + Using Trackbar (Slider)
  + Hue: 0 -> 179, Saturation|Value: 0 -> 255
- We want to keep the color that we want to detect in the resultant image
'''
############################################################
import cv2
import numpy as np
import imutils
np.set_printoptions(threshold=np.inf)

############################################################
trackbar_name_warp = 'Trackbar - Warping'
trackbar_name_hsv = 'Trackbar - HSV_Color'
trackbar_name_params = 'Trackbar - Parameters'

############################################################
def empty_function(a):
    pass
################## HSV ##################
def trackbar_init_params():
    gaussBLurParam_init = 9

    erodeKernelParam_init = 4 ###
    dilateKernelParam_init = 6 ###

    threshLowParam_init, threshHighParam_init = 40, 150
    threshHoughParam_init, minLineLengthHoughParam_init, maxLineGapHoughParam_init = 25, 1, 1

    # Default value for trackbar
    trackbar_init_values_params = [gaussBLurParam_init,
                                  threshLowParam_init, threshHighParam_init,
                                  threshHoughParam_init, minLineLengthHoughParam_init, maxLineGapHoughParam_init]
    cv2.namedWindow(trackbar_name_params)
    cv2.resizeWindow(trackbar_name_params, 300, 130)
    cv2.createTrackbar("Blur - Kerner Size", trackbar_name_params, trackbar_init_values_params[0], 15, empty_function)
    cv2.createTrackbar("Canny - Threshold 1", trackbar_name_params, trackbar_init_values_params[1], 100, empty_function)
    cv2.createTrackbar("Canny - Threshold 2", trackbar_name_params, trackbar_init_values_params[2], 250, empty_function)
    cv2.createTrackbar("Hough - Threshold", trackbar_name_params, trackbar_init_values_params[3], 50, empty_function)
    cv2.createTrackbar("Hough - Min Line Length", trackbar_name_params, trackbar_init_values_params[4], 20, empty_function)
    cv2.createTrackbar("Hough - Max Line Gap", trackbar_name_params, trackbar_init_values_params[5], 20, empty_function)

def trackbar_get_value_params():
    gaussBLurParam = cv2.getTrackbarPos("Blur - Kerner Size", trackbar_name_params)
    threshLowParam = cv2.getTrackbarPos("Canny - Threshold 1", trackbar_name_params)
    threshHighParam = cv2.getTrackbarPos("Canny - Threshold 2", trackbar_name_params)
    threshHoughParam = cv2.getTrackbarPos("Hough - Threshold", trackbar_name_params)
    minLineLengthHoughParam = cv2.getTrackbarPos("Hough - Min Line Length", trackbar_name_params)
    maxLineGapHoughParam = cv2.getTrackbarPos("Hough - Max Line Gap", trackbar_name_params)

    params = [gaussBLurParam, threshLowParam, threshHighParam, threshHoughParam,
             minLineLengthHoughParam, maxLineGapHoughParam]

    return params

def trackbar_init_HSV():
    trackbar_init_values_hsv = [0, 0, 130]  # Default value (min) for each H, S, V element
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
################## LANE ##################
def thresholdHSV(image):
    imgHsv, maskWhite, imgHsvResult = HSV_converter(image)

    return maskWhite

# def threshold(image):
#
#     return thresholdedImg

def warping(image, points, width, height, inverse = False):
    # Getting 'bird-eye' view. Seeing image from top view
    # Looking at the road from an angle, hard to determine the curve and how much of the curve is present
    # Looking from the top, easier to tell where the curve is and how much is curve
    # Using 'inverse' to displaying on the final result

    # Points on the original image, input from user
    pointsOrg = np.float32(points)
    # Points on the warped image
    pointsWarp = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Creating a matrix relating these two points together (Transformation matrix)
    # Easily convert any of the points from image 1 into image 2
    if inverse:
        matrix = cv2.getPerspectiveTransform(pointsWarp, pointsOrg)
    else:
        matrix = cv2.getPerspectiveTransform(pointsOrg, pointsWarp)

    # Converting pts2 from img1 to pts2 on img2
    warpedImg = cv2.warpPerspective(image, matrix, (width, height))
    return warpedImg

def empty_function(a):
    pass

def trackbar_init_warp(wT = 480, hT = 240):
    trackbar_init_values_warp = [10, 110, 10, 180]
    # T: Target
    cv2.namedWindow(trackbar_name_warp)
    cv2.resizeWindow(trackbar_name_warp, 300, 150)
    cv2.createTrackbar('Width Top', trackbar_name_warp, trackbar_init_values_warp[0], int(wT / 2), empty_function)
    cv2.createTrackbar('Height Top', trackbar_name_warp, trackbar_init_values_warp[1], int(hT), empty_function)
    cv2.createTrackbar('Width Bot', trackbar_name_warp, trackbar_init_values_warp[2], int(wT / 2), empty_function)
    cv2.createTrackbar('Height Bot', trackbar_name_warp, trackbar_init_values_warp[3], int(hT), empty_function)

# Getting the values in real time
def trackbar_get_value_warp(wT = 480, hT = 240):
    widthTop = cv2.getTrackbarPos('Width Top', trackbar_name_warp)
    heightTop = cv2.getTrackbarPos('Height Top', trackbar_name_warp)
    witdhBottom = cv2.getTrackbarPos('Width Bot', trackbar_name_warp)
    heightBottom = cv2.getTrackbarPos('Height Bot', trackbar_name_warp)

    points = np.float32([(widthTop, heightTop), (wT - widthTop, heightTop),
                         (witdhBottom, heightBottom), (wT - witdhBottom, heightBottom)])
    return points

def draw_warped_points(image, points):
    for i in range(4):
        # Drawing Top points
        if (i < 2):
            cv2.circle(image, (int(points[i][0]), int(points[i][1])), 10, (255, 0, 0), cv2.FILLED)
        # Drawing Bottom points
        else:
            cv2.circle(image, (int(points[i][0]), int(points[i][1])), 10, (0, 0, 255), cv2.FILLED)
    return image

def get_histogram(image, minPercent = 0.1, display = False, region = 1):
    # region: Percent of image for calculating. 1 -> Complete image
    # Summation of the complete image | # axis = 0, sum along the row (height) => Having `image's width` values
    if (region == 1):   histValues = np.sum(image, axis=0)
    # Summation of the amount of region. Get all x, get y from height//region to height. Axis 1: Height
    else:               histValues = np.sum(image[image.shape[0] // region:, :], axis=0)

    height = image.shape[0]

    # Finding max value of hist -> Defining Threshold
    maxHistValue = np.max(histValues)
    # Threshold: Below this value is noise, above is considered as path
    thresholdValue = minPercent * maxHistValue

    # Get the index of columns (Histogram bin)'s value  > threshold value
    indexArray = np.where(histValues >= thresholdValue)
    # Averaging all max indices values to find center of lane. `int` for plotting purpose
    basePoint = int(np.average(indexArray))

    if display:
        # Creating a new img to draw histogram and plot the base point
        histImg = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)

        for i, intensity in enumerate(histValues):
            # Plot the intensity of each image's column (index)
            # Before the variable histValues containing the sum of each image's column value
            # -> intensity//height to normalize
            if (intensity > thresholdValue):  color = (255, 0, 255)
            else:                             color = (0, 0, 255)

            cv2.line(histImg, (i, image.shape[0]), (i, image.shape[0] - intensity//height//region), color, 1)

        return basePoint, histImg

    return basePoint

def stackImages(scale, imgArray):
    # Taking the size of the first img and forces all the imgs to be of the same size
    rows = len(imgArray) # Number of all images
    cols = len(imgArray[0]) # Height of the first image
    rowsAvailable = isinstance(imgArray[0], list)
    height = imgArray[0][0].shape[0] # Height of the first image
    width = imgArray[0][0].shape[1] # Width of the first image

    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if (imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]):
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                        None, scale, scale)
                # Converting to 3-channels image
                if (len(imgArray[x][y].shape) == 2):
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

        blankImage = np.zeros((height, width, 3), dtype=np.uint8)
        hor = [blankImage] * rows
        horCon = [blankImage] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if (imgArray[x].shape[:2] == imgArray[0].shape[:2]):
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]),
                    None, scale, scale)
            if (len(imgArray[x].shape) == 2):
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver
