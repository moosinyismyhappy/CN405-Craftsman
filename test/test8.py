import cv2
import numpy as np

imageFrame = cv2.imread('../resources/images/points.png')

def trackbarCallback(x):
    pass

def mouse_click(event, x, y, flags, param):
    global  imageFrame

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

    elif event == cv2.EVENT_RBUTTONDOWN:
        imageFrame = cv2.imread('../resources/images/points.png')


if __name__ == "__main__":

    # Capturing video through webcam
    webcam = cv2.VideoCapture(0)

    # Create Pane Window
    cv2.namedWindow("Trackbars1")

    cv2.createTrackbar("Lower H", "Trackbars1", 0, 179, trackbarCallback)
    cv2.createTrackbar("Lower S", "Trackbars1", 0, 255, trackbarCallback)
    cv2.createTrackbar("Lower V", "Trackbars1", 0, 255, trackbarCallback)
    cv2.createTrackbar("Upper H", "Trackbars1", 179, 179, trackbarCallback)
    cv2.createTrackbar("Upper S", "Trackbars1", 255, 255, trackbarCallback)
    cv2.createTrackbar("Upper V", "Trackbars1", 255, 255, trackbarCallback)
    cv2.createTrackbar("Area", "Trackbars1", 1000, 2000, trackbarCallback)

    while True:

        # Receive stream image from camera
        #_, imageFrame = webcam.read()

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
