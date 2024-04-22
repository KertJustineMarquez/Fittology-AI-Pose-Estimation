 # import libraries
import math
import cv2
import numpy as np
import time
import PushUp_PoseModule as pm
import cvzone

#Camera
cap = cv2.VideoCapture(r'C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\pushup2.mp4')

# Import class
detector = pm.poseDetectorPushUp()

# Initialize variables
count = 0  # Count of reps



dir = 0  # Direction
pTime = 0  # Time
start_time = time.time()  # Start time
repetition_time = 60  # Repetition time

# Display info
display_info = True

per_right = 0
per_left = 0
bar_left = 0
bar_right = 0 

leftangle = 0
rightangle = 0

#main loop
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))

    elapsed_time = time.time() - start_time
    remaining_time = max(0, repetition_time - elapsed_time)

    if display_info:  # Check if to display counter, bar, and percentage

        img = detector.findPose(img, False) # initializes img as variable for findpose function
        lmList = detector.findPosition(img, False) # initializes lmList_bicep as variable for findPosition function

        # Define hand angles outside the if statement
        if len(lmList) != 0:
            # Check if the person is in a proper push-up posture
            leftangle, rightangle = detector.findPushupAngle(img, 11, 13, 15, 12, 14, 16, drawpoints=True)  # defines left  and right arm landmark keypoints 

            #Interpolate angles to percentage and position on screen
            per_left = np.interp(leftangle, (170, 300), (100, 0)) # first parenthesis, the value threshold of the angle. Second, represents the interp value
            bar_left = np.interp(leftangle, (180, 300), (200, 400))

            per_right = np.interp(rightangle, (30, 170), (0, 100))
            bar_right = np.interp(rightangle, (30, 180), (400, 200))

            if detector.isPushUpPosture(lmList):
                if leftangle >= 260 and rightangle <= 45:
                    if dir == 1:
                        count += 0.5
                        dir = 0
                        print("Count: ", count )
                elif leftangle <= 190 and rightangle <= 190: 
                    if dir == 0:
                        count += 0.5
                        dir = 1
                        print("Count: ", count )

        cvzone.putTextRect(img, 'Ai Push-Up Counter', [345, 30], thickness=2, border=2, scale=2.5)

        # Draw rectangle behind the timer text
        cv2.rectangle(img, (890, 10), (1260, 80), (255, 0, 0), -2)  # Rectangle position and color

        # Draw timer text above the rectangle
        timer_text = f"Time left: {int(remaining_time)}s"
        cv2.putText(img, timer_text, (900, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 3)

        # Draw bars for left and right angles
        cv2.putText(img, f"R {int(per_right)}%", (24, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (8, 200), (50, 400), (255, 255, 255), 5)
        cv2.rectangle(img, (8, int(bar_right)), (50, 400), (0, 0, 255), -1)

        cv2.putText(img, f"L {int(per_left)}%", (962, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (952, 200), (995, 400), (255, 255, 255), 5)
        cv2.rectangle(img, (952, int(bar_left)), (995, 400), (0, 0, 255), -1)

        if leftangle <= 190:
            cv2.rectangle(img, (952, int(bar_left)), (995, 400), (0, 255, 0), -1)

        if rightangle >= 170:
            cv2.rectangle(img, (8, int(bar_right)), (50, 400), (0, 255, 0), -1)

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


