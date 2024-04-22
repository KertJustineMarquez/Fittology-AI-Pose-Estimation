# import libraries
import math
import cv2
import numpy as np
import time
import SquatJack_PoseModule as pm
import cvzone


# Camera
cap = cv2.VideoCapture(r'C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\weightloss\squatjack.mp4')

# Import class
detector_squatjack = pm.poseDetectorSquatJack()

# Initialize Variables
count_squatjack = 0
dir = 0
start_time = time.time()  # starts time
repetition_time = 60  # duration time
display_info = True  # display features

# Main loop
while True:
    # reads camera 
    success, img = cap.read()
    # resizes video feed (can be changed depending on requirements of our Raspberry PI and Display Monitor Resolution)
    img = cv2.resize(img, (1280, 720))

    # Timer - starts timer based on set duration
    elapsed_time = time.time() - start_time
    remaining_time = max(0, repetition_time - elapsed_time)

    if display_info:  # Check if to display counter, bar, and percentage
        img = detector_squatjack.findPose(img, False)  # initializes img as variable for findpose function
        lmList_squatjack = detector_squatjack.findPosition(img, False)  # initializes lmList_squatjack as variable for findPosition function

        # Define leg angles outside the if statement
        if len(lmList_squatjack) != 0:
            distance = detector_squatjack.findSquatJack(img, 24, 26, 28, 23, 25, 27, drawpoints=True)  # Define landmark keypoints
            leftangle, rightangle = detector_squatjack.CheckUpperBody(img, 11, 13, 15, 12, 14, 16, drawpoints=True)

            #Interpolate the distance between the two ankle  to percentage and position on screen
            per_down = np.interp(distance, (60, 240), (0, 100))
            bar_down = np.interp(distance, (60, 250), (400, 200))


            if distance >= 240:
                if dir == 0:
                    count_squatjack += 0.5
                    print(count_squatjack)
                    dir = 1
            elif distance <= 60:
                if dir == 1:
                    count_squatjack +=0.5
                    print(count_squatjack)
                    dir = 0


        # Label
        cvzone.putTextRect(img, 'Ai Squat Jack Tracker', [345, 30], thickness=2, border=2, scale=2.5)

        # Draw rectangle behind the timer text
        cv2.rectangle(img, (890, 10), (1260, 80), (255, 0, 0), -2)  # Rectangle position and color

        # # Draw timer text above the rectangle
        timer_text = f"Time left: {int(remaining_time)}s"
        cv2.putText(img, timer_text, (900, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 3)

        cv2.putText(img, f"R {int(per_down)}%", (24, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (8, 200), (50, 400), (255, 255, 255), 5)
        cv2.rectangle(img, (8, int(bar_down)), (50, 400), (0, 0, 255), -1)

        cv2.putText(img, f"L {int(per_down)}%", (962, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (952, 200), (995, 400), (255, 255, 255), 5)
        cv2.rectangle(img, (952, int(bar_down)), (995, 400), (0, 0, 255), -1)

        if distance >= 240:
            cv2.rectangle(img, (952, int(bar_down)), (995, 400), (0, 255, 0), -1)
            cv2.rectangle(img, (8, int(bar_down)), (50, 400), (0, 255, 0), -1)

    # Count
    cv2.rectangle(img, (20, 20), (140, 130), (255, 0, 0), -1)
    cv2.putText(img, f"{int(count_squatjack)}/5", (30, 90), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

    if remaining_time <= 0:
        cvzone.putTextRect(img, "Time's Up", [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    if count_squatjack == 5:
        cvzone.putTextRect(img, 'All Repetitions Completed', [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
