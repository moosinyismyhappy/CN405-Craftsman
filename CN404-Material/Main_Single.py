import cv2
import numpy as np


def trackbarCallback(x):
    pass


def mouse_click(event, x, y, flags, param):
    # Left Click to get HSV color value from image
    if event == cv2.EVENT_LBUTTONDOWN:
        hsvArray = np.array(hsvFrame[y, x], np.uint8)
        print(x, ",", y, hsvArray)
        cv2.setTrackbarPos("Lower H", "Trackbars1", int(hsvArray[0] * (0.85)))
        cv2.setTrackbarPos("Lower S", "Trackbars1", int(hsvArray[1] * (0.85)))
        cv2.setTrackbarPos("Lower V", "Trackbars1", int(hsvArray[2] * (0.85)))
        cv2.setTrackbarPos("Upper H", "Trackbars1", int(hsvArray[0] * (1.15)))
        cv2.setTrackbarPos("Upper S", "Trackbars1", int(hsvArray[1] * (1.15)))
        cv2.setTrackbarPos("Upper V", "Trackbars1", int(hsvArray[2] * (1.15)))

    if event == cv2.EVENT_MBUTTONDOWN:
        hsvArray = np.array(hsvFrame[y, x], np.uint8)
        print(x, ",", y, hsvArray)
        cv2.setTrackbarPos("Lower H", "Trackbars2", int(hsvArray[0] * (0.85)))
        cv2.setTrackbarPos("Lower S", "Trackbars2", int(hsvArray[1] * (0.85)))
        cv2.setTrackbarPos("Lower V", "Trackbars2", int(hsvArray[2] * (0.85)))
        cv2.setTrackbarPos("Upper H", "Trackbars2", int(hsvArray[0] * (1.15)))
        cv2.setTrackbarPos("Upper S", "Trackbars2", int(hsvArray[1] * (1.15)))
        cv2.setTrackbarPos("Upper V", "Trackbars3", int(hsvArray[2] * (1.15)))

    if event == cv2.EVENT_RBUTTONDOWN:
        hsvArray = np.array(hsvFrame[y, x], np.uint8)
        print(x, ",", y, hsvArray)
        cv2.setTrackbarPos("Lower H", "Trackbars3", int(hsvArray[0] * (0.85)))
        cv2.setTrackbarPos("Lower S", "Trackbars3", int(hsvArray[1] * (0.85)))
        cv2.setTrackbarPos("Lower V", "Trackbars3", int(hsvArray[2] * (0.85)))
        cv2.setTrackbarPos("Upper H", "Trackbars3", int(hsvArray[0] * (1.15)))
        cv2.setTrackbarPos("Upper S", "Trackbars3", int(hsvArray[1] * (1.15)))
        cv2.setTrackbarPos("Upper V", "Trackbars3", int(hsvArray[2] * (1.15)))


if __name__ == "__main__":

    # Capturing video through webcam
    webcam = cv2.VideoCapture(0)

    # Create Pane Window
    cv2.namedWindow("Trackbars1")
    cv2.namedWindow("Trackbars2")
    cv2.namedWindow("Trackbars3")

    cv2.createTrackbar("Lower H", "Trackbars1", 0, 179, trackbarCallback)
    cv2.createTrackbar("Lower S", "Trackbars1", 0, 255, trackbarCallback)
    cv2.createTrackbar("Lower V", "Trackbars1", 0, 255, trackbarCallback)
    cv2.createTrackbar("Upper H", "Trackbars1", 179, 179, trackbarCallback)
    cv2.createTrackbar("Upper S", "Trackbars1", 255, 255, trackbarCallback)
    cv2.createTrackbar("Upper V", "Trackbars1", 255, 255, trackbarCallback)
    cv2.createTrackbar("Area", "Trackbars1", 2000, 70000, trackbarCallback)

    cv2.createTrackbar("Lower H", "Trackbars2", 0, 179, trackbarCallback)
    cv2.createTrackbar("Lower S", "Trackbars2", 0, 255, trackbarCallback)
    cv2.createTrackbar("Lower V", "Trackbars2", 0, 255, trackbarCallback)
    cv2.createTrackbar("Upper H", "Trackbars2", 179, 179, trackbarCallback)
    cv2.createTrackbar("Upper S", "Trackbars2", 255, 255, trackbarCallback)
    cv2.createTrackbar("Upper V", "Trackbars2", 255, 255, trackbarCallback)
    cv2.createTrackbar("Area", "Trackbars2", 2000, 70000, trackbarCallback)

    cv2.createTrackbar("Lower H", "Trackbars3", 0, 179, trackbarCallback)
    cv2.createTrackbar("Lower S", "Trackbars3", 0, 255, trackbarCallback)
    cv2.createTrackbar("Lower V", "Trackbars3", 0, 255, trackbarCallback)
    cv2.createTrackbar("Upper H", "Trackbars3", 179, 179, trackbarCallback)
    cv2.createTrackbar("Upper S", "Trackbars3", 255, 255, trackbarCallback)
    cv2.createTrackbar("Upper V", "Trackbars3", 255, 255, trackbarCallback)
    cv2.createTrackbar("Area", "Trackbars3", 2000, 70000, trackbarCallback)
    cv2.createTrackbar("Area", "Trackbars3", 2000, 70000, trackbarCallback)

    while True:

        # Receive stream image from camera
        _, imageFrame = webcam.read()

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

        lowerHue3 = cv2.getTrackbarPos("Lower H", "Trackbars3")
        lowerSaturation3 = cv2.getTrackbarPos("Lower S", "Trackbars3")
        lowerValue3 = cv2.getTrackbarPos("Lower V", "Trackbars3")
        upperHue3 = cv2.getTrackbarPos("Upper H", "Trackbars3")
        upperSaturation3 = cv2.getTrackbarPos("Upper S", "Trackbars3")
        upperValue3 = cv2.getTrackbarPos("Upper V", "Trackbars3")
        detectArea3 = cv2.getTrackbarPos("Area", "Trackbars3")

        color_lower3 = np.array([lowerHue3, lowerSaturation3, lowerValue3], np.uint8)
        color_upper3 = np.array([upperHue3, upperSaturation3, upperValue3], np.uint8)
        color_mask3 = cv2.inRange(hsvFrame, color_lower3, color_upper3)

        kernal = np.ones((5, 5), "uint8")

        color_mask1 = cv2.dilate(color_mask1, kernal)
        resultColor1 = cv2.bitwise_and(hsvFrame, hsvFrame,
                                       mask=color_mask1)

        color_mask2 = cv2.dilate(color_mask2, kernal)
        resultColor2 = cv2.bitwise_and(imageFrame, imageFrame,
                                       mask=color_mask2)

        color_mask3 = cv2.dilate(color_mask3, kernal)
        resultColor3 = cv2.bitwise_and(imageFrame, imageFrame,
                                       mask=color_mask3)

        contours, hierarchy = cv2.findContours(color_mask1,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > detectArea1):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 0), 2)

                cv2.putText(imageFrame, "Detected", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 255, 255))

        contours, hierarchy = cv2.findContours(color_mask2,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > detectArea2):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 0), 2)

                cv2.putText(imageFrame, "Detected", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 255, 255))

        contours, hierarchy = cv2.findContours(color_mask3,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > detectArea3):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 0), 2)

                cv2.putText(imageFrame, "Detected", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 255, 255))

        cv2.imshow("Multiple color Detection", imageFrame)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()