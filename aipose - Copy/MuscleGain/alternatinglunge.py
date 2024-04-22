import math
import cv2
import numpy as np
import time
import alternatinglunge_PoseModule as pm
import cvzone

# C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\weightloss\jumpingjack.mp4

cap = cv2.VideoCapture(r'C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\lungefinal.mp4')
detector_alternatingleftlunge = pm.poseDetectorAlternatingleftlunge()

count_alternating_right_lunge = 0
count_alternating_left_lunge = 0

dir_alternating_left_lunge = 0
dir_alternating_right_lunge = 0

pTime = 0
start_time = time.time()
repetition_time = 60
display_info = True

per_left_leg = 0
bar_left_leg = 0

per_right_leg = 0
bar_right_leg = 0

leftleg= 0
rightleg = 0

right = 0
left = 0

done = 0

perform_interpolation = True

cooldown_duration = 3
cooldown_timer = 0


while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))

    elapsed_time = time.time() - start_time
    remaining_time = max(0, repetition_time - elapsed_time)

    if display_info:  # Check if to display counter, bar, and percentage
        img = detector_alternatingleftlunge.findPose(img, False)
        lmList_jumping_jacks = detector_alternatingleftlunge.findPosition(img, False)

        # Define angles for jumping jacks outside the if statement
        if len(lmList_jumping_jacks) != 0:

            # Right and Left keypoints
            rightleg  = detector_alternatingleftlunge.CheckerLeg(img, 24, 26, 28, True)
            leftleg = detector_alternatingleftlunge.CheckerLeg(img, 23, 25, 27, True)

            # Percentage and Bar Interpolation
            per_right_leg = np.interp(rightleg, (90, 170), (100, 0))
            bar_right_leg = np.interp(rightleg, (90, 180), (480, 680))
            per_left_leg = np.interp(leftleg, (90, 170), (100, 0))
            bar_left_leg = np.interp(leftleg, (90, 180), (480, 680))


            # Pose Estimation Counting Threshold
            if rightleg <= 90:
                if dir_alternating_right_lunge == 0:
                    count_alternating_right_lunge += 0.5
                    dir_alternating_right_lunge = 1
                    cooldown_timer = cooldown_duration
                    print("right1", count_alternating_right_lunge)
            elif rightleg >= 150:
                if dir_alternating_right_lunge == 1:
                    count_alternating_right_lunge += 0.5
                    dir_alternating_right_lunge = 0
                    cooldown_timer = cooldown_duration
                    print("right2 ", count_alternating_right_lunge)
            if leftleg <= 90:
                if dir_alternating_left_lunge == 0:
                    count_alternating_left_lunge += 0.5
                    dir_alternating_left_lunge = 1
                    cooldown_timer = cooldown_duration
                    print("left1", count_alternating_left_lunge)
            elif rightleg >= 150:
                if dir_alternating_left_lunge == 1:
                    count_alternating_left_lunge += 0.5
                    dir_alternating_left_lunge = 0
                    cooldown_timer = cooldown_duration
                    print("left2 ", count_alternating_left_lunge)

        # Delay Timer for Pose Estimation
        fps = cap.get(cv2.CAP_PROP_FPS)
        if cooldown_timer > 0:
            cooldown_timer -= 1 / fps

        cvzone.putTextRect(img, 'Ai Leg Lunge (alternate)', [345, 30], thickness=2, border=2, scale=2.5)

        # Draw rectangle behind the timer text
        cv2.rectangle(img, (890, 10), (1260, 80), (255, 0, 0), -2)  # Rectangle position and color

        # Draw timer text above the rectangle
        timer_text = f"Time left: {int(remaining_time)}s"
        cv2.putText(img, timer_text, (900, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 3)


        # RIGHT LEG
        cv2.putText(img, f"R {int(per_right_leg)}%", (24, 470), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (8, 480), (50, 680), (0, 255, 0), 5)
        cv2.rectangle(img, (8, int(bar_right_leg)), (50, 680), (0, 0, 255), -1)

        # LEFT LEG
        cv2.putText(img, f"L {int(per_left_leg)}%", (962, 470), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (952, 480), (995, 680), (0, 255, 0), 5)
        cv2.rectangle(img, (952, int(bar_left_leg)), (995, 680), (0, 0, 255), -1)

        # Green Indicator
        if rightleg <= 90:
            cv2.rectangle(img, (8, int(bar_right_leg)), (50, 680), (0, 255, 0), -1)

        if leftleg <= 90:
            cv2.rectangle(img, (952, int(bar_left_leg)), (995, 680), (0, 255, 0), -1)


    # Counter 
    cv2.rectangle(img, (20, 20), (140, 130), (0, 0, 255), -1)
    cv2.putText(img, f"{int(count_alternating_right_lunge)}/5", (30, 90), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (255, 0, 0), 7)

    cv2.rectangle(img, (150, 20), (270, 130), (255, 0, 0), -1)
    cv2.putText(img, f"{int(count_alternating_left_lunge)}/5", (160, 90), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

    # Timer
    if remaining_time <= 0:
        cvzone.putTextRect(img, "Time's Up", [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    # Repetition
    if count_alternating_left_lunge >= 5:  # Assuming 10 jumping jacks for demonstration
        cvzone.putTextRect(img, 'Exercise Complete', [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



