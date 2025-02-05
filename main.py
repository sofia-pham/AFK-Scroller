import cv2
import mediapipe
import numpy as np
from pynput.keyboard import Key, Controller

# Set up mediapipe
mediapipeHands = mediapipe.solutions.hands
myHands = mediapipeHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
drawHands = mediapipe.solutions.drawing_utils

keyboard = Controller()

prevIndexCx, prevIndexCy = None, None
prevMiddleCx, prevMiddleCy = None, None

# Video capture
capture = cv2.VideoCapture(0)

# Treshold of finger movement to trigger an action
thresholdIndexX, thresholdIndexY = 40, 40
thresholdMiddleX, thresholdMiddleY = 30, 30

showCamera = True
blackImg = np.zeros((500, 500, 3), dtype="uint8")  # 3-channel black image

while True:
    found, img = capture.read()
    # No image found so we exit the loop
    if not found:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    foundHands = myHands.process(imgRGB)

    if foundHands.multi_hand_landmarks:
        for landmarks in foundHands.multi_hand_landmarks:
            indexFinger = landmarks.landmark[mediapipeHands.HandLandmark.INDEX_FINGER_TIP]
            middleFinger = landmarks.landmark[mediapipeHands.HandLandmark.MIDDLE_FINGER_TIP]

            h, w, _ = img.shape

            indexCx, indexCy = int(indexFinger.x * w), int(indexFinger.y * h)
            middleCx, middleCy = int(
                middleFinger.x * w), int(middleFinger.y * h)

            # if prevIndexCx is none, all other cx + cy variables are none. skip this iteration
            if prevIndexCx is not None:
                # Calculate deltas of finger movements
                indexDx, indexDy = indexCx - prevIndexCx, indexCy - prevIndexCy
                middleDx, middleDy = middleCx - prevMiddleCx, middleCy - prevMiddleCy

                # Handle actions
                if abs(indexDy) > thresholdIndexY and abs(indexDx) < thresholdIndexX:
                    if indexDy < 0:
                        # Go down if index raised
                        keyboard.press(Key.page_down)
                        keyboard.release(Key.page_down)

                elif abs(middleDy) > thresholdMiddleY and abs(indexDy) < thresholdMiddleY:
                    if middleDy < 0:
                        # Go up if middle raised
                        keyboard.press(Key.page_up)
                        keyboard.release(Key.page_up)

            # Update previous variables
            prevIndexCx, prevIndexCy = indexCx, indexCy
            prevMiddleCx, prevMiddleCy = middleCx, middleCy

        if showCamera:
            drawHands.draw_landmarks(
                img, landmarks, mediapipeHands.HAND_CONNECTIONS)
    
    if showCamera:
        showImg = img
    else:
        showImg = blackImg

    cv2.imshow("AFK Scroller", showImg)
    key = cv2.waitKey(1) & 0xFF
    # Quit program if user presses 'q' or closes the window
    if key == ord('q') or cv2.getWindowProperty("AFK Scroller", cv2.WND_PROP_VISIBLE) < 1:
        break
    elif key == ord('1'):
        showCamera = True
    elif key == ord('2'):
        showCamera = False


# Release resources
capture.release()
cv2.destroyAllWindows()
