# import libraries
import math
import cv2
import numpy as np
import time
import chestpress_PoseModule as pm
import cvzone


#Camera
cap = cv2.VideoCapture(r'C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\chestpressvid.mp4')

#import class
detector_chestpress = pm.poseDetector()

#Initialize Variables
count_chestpress_left = 0
count_chestpress_right = 0

dir_chestpress_left = 0
dir_chestpress_right = 0

start_time = time.time() # starts time
repetition_time = 60 # duration time
display_info = True # display features

bar_left = 0
bar_right = 0
per_left = 0
per_right = 0
angle_left = 0
angle_right = 0


# main loop
while True:
    # reads camera 
    success, img = cap.read()
    # resizes video feed (can be changed depending on requirements of our Raspberry PI and Display Monitor Resolution)
    img = cv2.resize(img, (1280, 720))

    # Timer - starts timer based on set duration
    elapsed_time = time.time() - start_time
    remaining_time = max(0, repetition_time - elapsed_time)


    if display_info:  # Check if to display counter, bar, and percentage
        img = detector_chestpress.findPose(img, False) # initializes img as variable for findpose function
        lmList_bicep = detector_chestpress.findPosition(img, False) # initializes lmList_bicep as variable for findPosition function

        # Define hand angles outside the if statement
        if len(lmList_bicep) != 0:
            angle_left = detector_chestpress.findAngle(img, 11, 13, 15)
            angle_right = detector_chestpress.findAngle(img, 12, 14, 16) # defines right arm landmark keypoints
            # (refer to mediapipe landmark mapping for number equivalent)

            # Interpolate angle to percentage and position on screen
            per_left = np.interp(angle_left, (50, 155), (0, 100)) # first parenthesis, the value threshold of the angle. Second, represents the interp value
            bar_left = np.interp(angle_left, (50, 165), (400, 200)) # 

            per_right = np.interp(angle_right, (190, 300), (100, 0)) # 
            bar_right = np.interp(angle_right, (190, 300), (200, 400)) # 

            #Check for the left dumbbell curls
            if angle_left >= 155:
                if dir_chestpress_left == 0:
                    count_chestpress_left += 0.5
                    dir_chestpress_left = 1 
                    print("Count Left: ", count_chestpress_left)
            elif angle_left <= 50:
                if dir_chestpress_left == 1:
                    count_chestpress_left += 0.5
                    dir_chestpress_left = 0  
                    print("Count Left: ", count_chestpress_left)

            #Check for the right dumbbell curls
            if angle_right <= 190: 
                if dir_chestpress_right == 0:
                    count_chestpress_right += 0.5
                    dir_chestpress_right = 1 
                    print("Count Right: ", count_chestpress_right)

            if angle_right >= 270:
                if dir_chestpress_right == 1:
                    count_chestpress_right += 0.5
                    dir_chestpress_right = 0
                    print("Count Right: ", count_chestpress_right)

        # label
        cvzone.putTextRect(img, 'Ai Chest Press Tracker', [345, 30], thickness=2, border=2, scale=2.5) 

        # Draw rectangle behind the timer text
        cv2.rectangle(img, (890, 10), (1260, 80), (255, 0, 0), -2)  # Rectangle position and color

        # Draw timer text above the rectangle
        timer_text = f"Time left: {int(remaining_time)}s"
        cv2.putText(img, timer_text, (900, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 3)

        # bar
        cv2.putText(img, f"R {int(per_right)}%" , (24, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (8, 200), (50, 400), (255, 255, 255), 5)
        cv2.rectangle(img, (8, int(bar_right)), (50, 400), (0, 0, 255), -1)

        cv2.putText(img, f"L {int(per_left)}%", (962, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (952, 200), (995, 400), (255, 255, 255), 5)
        cv2.rectangle(img, (952, int(bar_left)), (995, 400), (0, 0, 255), -1)
        
        if angle_left >= 155:
            cv2.rectangle(img, (952, int(bar_left)), (995, 400), (0, 255, 0), -1)

        if angle_right <= 190:
            cv2.rectangle(img, (8, int(bar_right)), (50, 400), (0, 255, 0), -1)

    #count
    cv2.rectangle(img, (20, 20), (140, 130), (0, 0, 255), -1)
    cv2.putText(img, f"{int(count_chestpress_right)}/5", (30, 90), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (255, 0, 0), 7)

    cv2.rectangle(img, (150, 20), (270, 130), (255, 0, 0), -1)
    cv2.putText(img, f"{int(count_chestpress_right)}/5", (160, 90), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

    if remaining_time <= 0:
        cvzone.putTextRect(img, "Time's Up", [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    if count_chestpress_right == 5 and count_chestpress_left == 5:
        cvzone.putTextRect(img, 'All Repetitions Completed', [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
