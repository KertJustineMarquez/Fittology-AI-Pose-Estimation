import math
import cv2
import numpy as np
import time
import bodyweightsquat_PoseModule as pm
import cvzone

cap = cv2.VideoCapture(r'C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\Leg exercise - How to bodyweight squat.mp4')
detector_BodyWeightSquat = pm.poseDetectorBodyWeightSquat()

count_body_weight_squat = 0
dir_body_weight_squat = 0

pTime = 0
start_time = time.time()
repetition_time = 60
display_info = True

leftbody = 0
rightbody = 0

per_left_body = 0
bar_left_body = 0

per_right_body = 0
bar_right_body = 0

done = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))

    elapsed_time = time.time() - start_time
    remaining_time = max(0, repetition_time - elapsed_time)

    if display_info:  # Check if to display counter, bar, and percentage
        img = detector_BodyWeightSquat.findPose(img, False)
        lmList_jumping_jacks = detector_BodyWeightSquat.findPosition(img, False)

        # Define angles for jumping jacks outside the if statement
        if len(lmList_jumping_jacks) != 0:

            # rightbody, leftbody = detector_BodyWeightSquat.WeightSquat(
            #     img, 12, 24, 26, 11, 23, 25, drawpoints= True)
            
            leftbody = detector_BodyWeightSquat.WeightSquat(img, 12, 24, 26, True)
            rightbody = detector_BodyWeightSquat.WeightSquat(img, 11, 23, 25, True)
            
            #Interpolate angle to percentage and position on screen
            per_left_body = np.interp(int(leftbody), (60, 180), (100, 0))
            bar_left_body = np.interp(int(leftbody), (70, 180), (200, 400))
    
            per_right_body = np.interp(int(rightbody), (60, 180), (100, 0))
            bar_right_body = np.interp(int(rightbody), (70, 180), (200, 400))

            if 60 <= leftbody <= 70:
                if dir_body_weight_squat == 0:
                    count_body_weight_squat += 0.5
                    dir_body_weight_squat = 1
            elif leftbody >= 170:
                if dir_body_weight_squat == 1:
                    count_body_weight_squat +=0.5
                    dir_body_weight_squat = 0

            if 60 <= rightbody <= 70:
                if dir_body_weight_squat == 0:
                    count_body_weight_squat += 1
                    dir_body_weight_squat = 1
            elif rightbody >= 170:
                if dir_body_weight_squat == 1:
                    count_body_weight_squat +=0.5
                    dir_body_weight_squat = 0

        cvzone.putTextRect(img, 'Ai Leg Lunge (alternate)', [345, 30], thickness=2, border=2, scale=2.5)

        # Draw rectangle behind the timer text
        cv2.rectangle(img, (890, 10), (1260, 80), (255, 0, 0), -2)  # Rectangle position and color

        # Draw timer text above the rectangle
        timer_text = f"Time left: {int(remaining_time)}s"
        cv2.putText(img, timer_text, (900, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 3)


        # RIGHT LEG
        cv2.putText(img, f"R {int(per_right_body)}%", (24, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (8, 200), (50, 400), (0, 255, 0), 5)
        cv2.rectangle(img, (8, int(bar_right_body)), (50, 400), (255, 0, 0), -1)

        # LEFT LEG
        cv2.putText(img, f"L {int(per_left_body)}%", (962, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
        cv2.rectangle(img, (952, 200), (995, 400), (0, 255, 0), 5)
        cv2.rectangle(img, (952, int(bar_left_body)), (995, 400), (255, 0, 0), -1)
        
        
    cv2.rectangle(img, (0, 0), (130, 120), (255, 0, 0), -1)
    cv2.putText(img, f"{int(count_body_weight_squat)}/999", (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

    if remaining_time <= 0:
        cvzone.putTextRect(img, "Time's Up", [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    if count_body_weight_squat >= 5:  # Assuming 10 jumping jacks for demonstration
        cvzone.putTextRect(img, 'Exercise Complete', [345, 30], thickness=2, border=2, scale=2.5)
        display_info = False

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



