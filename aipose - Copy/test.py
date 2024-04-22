

import math
import cv2
import numpy as np
import time
import aipose2.PushUp_PoseModule as pm
import cvzone

cap = cv2.VideoCapture(r'C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\pushup2.mp4')

detector = pm.poseDetectorPushUp()
count = 0
direction = 0
pTime = 0
start_time = time.time()
repetition_time = 60
display_info = True

# Initialize hand angles
leftHandAngle = 0
rightHandAngle = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))

    elapsed_time = time.time() - start_time
    remaining_time = max(0, repetition_time - elapsed_time)

    if display_info:  # Check if to display counter, bar, and percentage
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        # Define hand angles outside the if statement
        if len(lmList) != 0:
            leftangle, rightangle = detector.findPushupAngle(img, 11, 13, 15, 12, 14, 16, drawpoints=True)

            if leftangle is not None and rightangle is not None and not math.isnan(leftangle) and not math.isnan(
                    rightangle):
                leftHandAngle = int(np.interp(leftangle, [-30, 180], [100, 0]))
                rightHandAngle = int(np.interp(rightangle, [34, 173], [100, 0]))
            else:
                leftHandAngle = 0
                rightHandAngle = 0

            if detector.isPushUpPosture(lmList):
                # Increment count if the person is in a proper push-up posture and hand angles are appropriate
                if leftHandAngle >= 70 and rightHandAngle >= 70:
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    direction = 0

        cvzone.putTextRect(img, 'Ai Push-Up Counter', [345, 30], thickness=2, border=2, scale=2.5)

        # Draw rectangle behind the timer text
        cv2.rectangle(img, (890, 10), (1250, 60), (255, 0, 0), -2)  # Rectangle position and color

        # Draw timer text above the rectangle
        timer_text = f"Time left: {int(remaining_time)}s"
        cv2.putText(img, timer_text, (900, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 3)

        # get values of rightHandAngle to put in the bar value
        leftval = np.interp(rightHandAngle, [0, 100], [400, 200])
        rightval = np.interp(rightHandAngle, [0, 100], [400, 200])

        cv2.putText(img, 'R', (24, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (8, 200), (50, 400), (0, 255, 0), 5)
        cv2.rectangle(img, (8, int(rightval)), (50, 400), (255, 0, 0), -1)

        cv2.putText(img, 'L', (962, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (952, 200), (995, 400), (0, 255, 0), 5)
        cv2.rectangle(img, (952, int(leftval)), (995, 400), (255, 0, 0), -1)

        if leftHandAngle > 70:
            cv2.rectangle(img, (952, int(leftval)), (995, 400), (0, 0, 255), -1)

        if rightHandAngle > 70:
            cv2.rectangle(img, (8, int(leftval)), (50, 400), (0, 0, 255), -1)

    cv2.rectangle(img, (0, 0), (130, 120), (255, 0, 0), -1)
    cv2.putText(img, f"{int(count)}/5", (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

    if remaining_time <= 0:
        cvzone.putTextRect(img, "Time's Up", [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    if count >= 5:
        cvzone.putTextRect(img, 'Repetition completed', [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()