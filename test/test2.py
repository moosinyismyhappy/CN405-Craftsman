# Test Tracking

import cv2
import numpy as np

is_left_first = True
prev = -1
curr = -1
prev_status = None
curr_status = None

is_right_first = True
prev_right = -1
curr_right = -1
prev_status_right = None
curr_status_right = None

count = 0
imageFrame = None
newImageFrame = cv2.imread('../resources/images/black_background.png')


def trackingLeft(input):
    global is_left_first, prev, curr, prev_status, curr_status
    # print('Prev :',prev,'Curr :',curr)
    diff_x = curr[0] - prev[0]
    diff_y = curr[1] - prev[1]
    # print('diff_x :',diff_x,'diff_y :',diff_y,'curr_status',curr_status,'prev_status',prev_status)

    if diff_x and diff_y > 0:
        curr_status = (1, 1)
    elif diff_x and diff_y < 0:
        curr_status = (-1, -1)
    elif diff_x > 0 and diff_y < 0:
        curr_status = (1, -1)
    elif diff_x < 0 and diff_y > 0:
        curr_status = (-1, 1)

    if prev_status != curr_status:
        # print('Change Direction from', prev_status, prev, 'to', curr_status, curr, 'with diff', diff_x, diff_y)
        cv2.circle(newImageFrame, input, 1, (0, 0, 255), 2)


def trackingRight(input):
    global is_right_first, prev_right, curr_right, prev_status_right, curr_status_right
    # print('Prev :',prev,'Curr :',curr)
    diff_x = curr[0] - prev[0]
    diff_y = curr[1] - prev[1]
    # print('diff_x :',diff_x,'diff_y :',diff_y,'curr_status',curr_status,'prev_status',prev_status)

    if diff_x and diff_y > 0:
        curr_status_right = (1, 1)
    elif diff_x and diff_y < 0:
        curr_status_right = (-1, -1)
    elif diff_x > 0 and diff_y < 0:
        curr_statu_right = (1, -1)
    elif diff_x < 0 and diff_y > 0:
        curr_status_right = (-1, 1)

    if prev_status_right != curr_status_right:
        # print('Change Direction from', prev_status, prev, 'to', curr_status, curr, 'with diff', diff_x, diff_y)
        cv2.circle(newImageFrame, input, 1, (0, 255, 255), 2)


def trackbarCallback(x):
    pass


def mouse_click(event, x, y, flags, param):
    global is_left_first, prev, curr, prev_status, curr_status

    # Left Click to get HSV color value from image
    if event == cv2.EVENT_LBUTTONDOWN:
        hsvArray = np.array(hsvFrame[y, x], np.uint8)
        # print(x, ",", y, hsvArray)
        cv2.setTrackbarPos("Lower H", "Trackbars1", int(hsvArray[0] * (0.85)))
        cv2.setTrackbarPos("Lower S", "Trackbars1", int(hsvArray[1] * (0.85)))
        cv2.setTrackbarPos("Lower V", "Trackbars1", int(hsvArray[2] * (0.85)))
        cv2.setTrackbarPos("Upper H", "Trackbars1", int(hsvArray[0] * (1.15)))
        cv2.setTrackbarPos("Upper S", "Trackbars1", int(hsvArray[1] * (1.15)))
        cv2.setTrackbarPos("Upper V", "Trackbars1", int(hsvArray[2] * (1.15)))

    if event == cv2.EVENT_RBUTTONDOWN:
        hsvArray = np.array(hsvFrame[y, x], np.uint8)
        # print(x, ",", y, hsvArray)
        cv2.setTrackbarPos("Lower H", "Trackbars2", int(hsvArray[0] * (0.85)))
        cv2.setTrackbarPos("Lower S", "Trackbars2", int(hsvArray[1] * (0.85)))
        cv2.setTrackbarPos("Lower V", "Trackbars2", int(hsvArray[2] * (0.85)))
        cv2.setTrackbarPos("Upper H", "Trackbars2", int(hsvArray[0] * (1.15)))
        cv2.setTrackbarPos("Upper S", "Trackbars2", int(hsvArray[1] * (1.15)))
        cv2.setTrackbarPos("Upper V", "Trackbars2", int(hsvArray[2] * (1.15)))


if __name__ == "__main__":

    # Capturing video through webcam
    webcam = cv2.VideoCapture('../resources/videos/Fast_Working.mp4')

    # Create Pane Window
    cv2.namedWindow("Trackbars1")
    cv2.namedWindow("Trackbars2")

    cv2.createTrackbar("Lower H", "Trackbars1", 0, 179, trackbarCallback)
    cv2.createTrackbar("Lower S", "Trackbars1", 0, 255, trackbarCallback)
    cv2.createTrackbar("Lower V", "Trackbars1", 0, 255, trackbarCallback)
    cv2.createTrackbar("Upper H", "Trackbars1", 179, 179, trackbarCallback)
    cv2.createTrackbar("Upper S", "Trackbars1", 255, 255, trackbarCallback)
    cv2.createTrackbar("Upper V", "Trackbars1", 255, 255, trackbarCallback)
    cv2.createTrackbar("Area", "Trackbars1", 500, 5000, trackbarCallback)

    cv2.createTrackbar("Lower H", "Trackbars2", 0, 179, trackbarCallback)
    cv2.createTrackbar("Lower S", "Trackbars2", 0, 255, trackbarCallback)
    cv2.createTrackbar("Lower V", "Trackbars2", 0, 255, trackbarCallback)
    cv2.createTrackbar("Upper H", "Trackbars2", 179, 179, trackbarCallback)
    cv2.createTrackbar("Upper S", "Trackbars2", 255, 255, trackbarCallback)
    cv2.createTrackbar("Upper V", "Trackbars2", 255, 255, trackbarCallback)
    cv2.createTrackbar("Area", "Trackbars2", 500, 5000, trackbarCallback)

    while True:

        try:
            # Receive stream image from camera
            _, imageFrame = webcam.read()

            imageFrame = cv2.resize(imageFrame, (640, 480))

            # Change color space from RGB to HSV
            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

            lowerHue1 = cv2.getTrackbarPos("Lower H", "Trackbars1")
            lowerSaturation1 = cv2.getTrackbarPos("Lower S", "Trackbars1")
            lowerValue1 = cv2.getTrackbarPos("Lower V", "Trackbars1")
            upperHue1 = cv2.getTrackbarPos("Upper H", "Trackbars1")
            upperSaturation1 = cv2.getTrackbarPos("Upper S", "Trackbars1")
            upperValue1 = cv2.getTrackbarPos("Upper V", "Trackbars1")
            detectArea1 = cv2.getTrackbarPos("Area", "Trackbars1")

            color_lower1 = np.array([lowerHue1, lowerSaturation1, lowerValue1], np.uint8)
            color_upper1 = np.array([upperHue1, upperSaturation1, upperValue1], np.uint8)
            color_mask1 = cv2.inRange(hsvFrame, color_lower1, color_upper1)

            lowerHue2 = cv2.getTrackbarPos("Lower H", "Trackbars2")
            lowerSaturation2 = cv2.getTrackbarPos("Lower S", "Trackbars2")
            lowerValue2 = cv2.getTrackbarPos("Lower V", "Trackbars2")
            upperHue2 = cv2.getTrackbarPos("Upper H", "Trackbars2")
            upperSaturation2 = cv2.getTrackbarPos("Upper S", "Trackbars2")
            upperValue2 = cv2.getTrackbarPos("Upper V", "Trackbars2")
            detectArea2 = cv2.getTrackbarPos("Area", "Trackbars2")

            color_lower2 = np.array([lowerHue2, lowerSaturation2, lowerValue2], np.uint8)
            color_upper2 = np.array([upperHue2, upperSaturation2, upperValue2], np.uint8)
            color_mask2 = cv2.inRange(hsvFrame, color_lower2, color_upper2)

            kernal = np.ones((5, 5), "uint8")

            color_mask1 = cv2.dilate(color_mask1, kernal)
            resultColor1 = cv2.bitwise_and(hsvFrame, hsvFrame,
                                           mask=color_mask1)

            contours, hierarchy = cv2.findContours(color_mask1,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if (area > detectArea1):
                    x, y, w, h = cv2.boundingRect(contour)

                    center = int((2 * x + w) / 2), int((2 * y + h) / 2)

                    if not is_left_first:
                        prev = curr
                        curr = center

                        if prev == curr:
                            continue

                        trackingLeft(center)

                    else:
                        curr = center
                        prev = center
                        prev_status = (0, 0)
                        curr_status = (0, 0)
                        print('First Time', prev, curr)
                        is_left_first = False

                    imageFrame = cv2.rectangle(imageFrame, (x, y),
                                               (x + w, y + h),
                                               (0, 255, 0), 2)

                    # imageFrame = cv2.circle(imageFrame, center, 2, (255, 255, 0), 2)

                    cv2.putText(imageFrame, "Detected Left", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (255, 255, 255))

            contours, hierarchy = cv2.findContours(color_mask2,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if (area > detectArea2):
                    x, y, w, h = cv2.boundingRect(contour)

                    center = int((2 * x + w) / 2), int((2 * y + h) / 2)

                    if not is_right_first:
                        prev_right = curr_right
                        curr_right = center

                        if prev_right == curr_right:
                            continue

                        trackingRight(center)

                    else:
                        curr_right = center
                        prev_right = center
                        prev_statu_right = (0, 0)
                        curr_status_right = (0, 0)
                        print('First Time', prev_right, curr_right)
                        is_right_first = False

                    imageFrame = cv2.rectangle(imageFrame, (x, y),
                                               (x + w, y + h),
                                               (0, 255, 0), 2)

                    # imageFrame = cv2.circle(imageFrame, center, 2, (255, 255, 0), 2)

                    cv2.putText(imageFrame, "Detected Right", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (255, 255, 255))

            cv2.imshow("Multiple color Detection", imageFrame)
            cv2.imshow("Result", newImageFrame)
            cv2.setMouseCallback("Multiple color Detection", mouse_click)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                    break

        except:
            webcam = cv2.VideoCapture('../resources/videos/Fast_Working.mp4')

    webcam.release()
    cv2.destroyAllWindows()
