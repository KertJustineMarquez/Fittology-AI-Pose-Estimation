
# #to be continued, for completion with front view and side view

# import math
# import cv2
# import numpy as np
# import time
# import bws_PoseModule as pm
# import cvzone

# # Initialize pose detector for bodyweight squat

# #Videos

# # Sideway
# # C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\Leg exercise - How to bodyweight squat.mp4
# # Front
# # C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\bodyweight squat(1).mp4

# cap = cv2.VideoCapture(r'C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\Leg exercise - How to bodyweight squat.mp4')
# detector_BodyWeightSquat = pm.poseDetectorBodyWeightSquat()

# # Initialize counting variables
# count_body_weight_squat = 0
# dir_body_weight_squat = 0

# # Initialize timing variables
# start_time = time.time()
# repetition_time = 60  # Total exercise duration in seconds
# display_info = True

# # Initialize variables for interpolation
# per_body_left = 0
# bar_body_right = 0

# # Define interpolation ranges for side view and front view
# # These values are just placeholders; adjust them as needed based on your camera setup
# side_view_range_left = (60, 180)
# side_view_range_right = (70, 180)

# front_view_range_left = (90, 200)
# front_view_range_right = (90, 200)

# # Placeholder variable for camera angle detection
# # You need to replace this with actual code to detect the camera angle
# is_side_view = True  # Assume side view by default

# while True:
#     success, img = cap.read()
#     img = cv2.resize(img, (1280, 720))

#     elapsed_time = time.time() - start_time
#     remaining_time = max(0, repetition_time - elapsed_time)

#     if display_info:
#         img = detector_BodyWeightSquat.findPose(img, False)
#         lmList_jumping_jacks = detector_BodyWeightSquat.findPosition(img, False)

#         if len(lmList_jumping_jacks) != 0:
#             # Determine camera angle and use appropriate interpolation range
#             if is_side_view:
#                 angle_range_left = side_view_range_left
#                 angle_range_right = side_view_range_right
#             else:
#                 angle_angle_left = front_view_range_left
#                 angle_range_right = front_view_range_right

#             # Calculate angle and interpolate values
#             rightwing = detector_BodyWeightSquat.WeightSquat(img, 12, 24, 26, True)
#             leftwing = detector_BodyWeightSquat.WeightSquat(img, 11, 23, 25, True)

#             if rightwing is not None and leftwing is not None:
#                     # Check if the person is facing sideways or towards the camera
#                     if is_side_view:
#                         # Interpolate values based on side view interpolation ranges
#                         per_body_left = np.interp(rightwing, angle_range_left, (100, 0))
#                         bar_body_right = np.interp(leftwing, angle_range_right, (200, 400))
#                     else:
#                         # Interpolate values based on front view interpolation ranges
#                         per_body_left = np.interp(leftwing, angle_range_left, (100, 0))
#                         bar_body_right = np.interp(rightwing, angle_range_right, (200, 400))

#                     # Perform counting based on angle and direction
#                     # Adjust this logic based on your counting requirements
#                     if rightwing >= angle_range_left[0] and rightwing <= angle_range_left[1]:
#                         if dir_body_weight_squat == 0:
#                             count_body_weight_squat += 0.5
#                             dir_body_weight_squat = 1
#                     elif rightwing >= angle_range_left[1]:
#                         if dir_body_weight_squat == 1:
#                             count_body_weight_squat += 0.5
#                             dir_body_weight_squat = 0

#         #     # Side View
#         #     per_body_left = np.interp(int(angle), angle_range, (100, 0))
#         #     bar_body_right = np.interp(int(angle), angle_range, (200, 400))



#         #     # Perform counting based on angle and direction
#         #     if angle >= angle_range[0] and angle <= angle_range[1]:
#         #         if dir_body_weight_squat == 0:
#         #             count_body_weight_squat += 0.5
#         #             dir_body_weight_squat = 1
#         #     elif angle >= angle_range[1]:
#         #         if dir_body_weight_squat == 1:
#         #             count_body_weight_squat += 0.5
#         #             dir_body_weight_squat = 0

#         # # Display counting and other information
#         # cv2.rectangle(img, (0, 0), (130, 120), (255, 0, 0), -1)
#         # cv2.putText(img, f"{int(count_body_weight_squat)}/5", (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

#         # if remaining_time <= 0:
#         #     cvzone.putTextRect(img, "Time's Up", [345, 30], thickness=2, border=2, scale=2.5)
#         #     display_info = False

#         # if count_body_weight_squat >= 5:
#         #     cvzone.putTextRect(img, 'Exercise Complete', [345, 30], thickness=2, border=2, scale=2.5)
#         #     display_info = False

#     cv2.imshow("Image", img)
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



import math
import cv2
import numpy as np
import time
import bws_PoseModule as pm
import cvzone

# Initialize pose detector for bodyweight squat

# Videos

# Front View
# C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\bodyweight squat(1).mp4
# Side View
# C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\Leg exercise - How to bodyweight squat.mp4

cap = cv2.VideoCapture(r'C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\bodyweight squat(1).mp4')
detector_BodyWeightSquat = pm.poseDetectorBodyWeightSquat()

# Initialize counting variables
count_body_weight_squat = 0
dir_body_weight_squat = 0

# Initialize timing variables
start_time = time.time()
repetition_time = 60  # Total exercise duration in seconds
display_info = True

# Initialize variables for interpolation
per_body_left = 0
bar_body_right = 0

# Define interpolation ranges for side view and front view
# These values are just placeholders; adjust them as needed based on your camera setup
side_view_range_left = (60, 180)
side_view_range_right = (70, 180)

front_view_range_left = (90, 200)
front_view_range_right = (90, 200)

# Placeholder variable for camera angle detection
# You need to replace this with actual code to detect the camera angle
is_side_view = True  # Assume side view by default

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))

    elapsed_time = time.time() - start_time
    remaining_time = max(0, repetition_time - elapsed_time)

    if display_info:
        img = detector_BodyWeightSquat.findPose(img, False)
        lmList_jumping_jacks = detector_BodyWeightSquat.findPosition(img, False)

        if len(lmList_jumping_jacks) != 0:
            # Determine camera angle and use appropriate interpolation range
            if is_side_view:
                angle_range_left = side_view_range_left
                angle_range_right = side_view_range_right
                print("side view achieved")
            else:
                angle_range_left = front_view_range_left
                angle_range_right = front_view_range_right
                print("front view achieved")


            # Calculate angle and interpolate values
            angle_side, angle_front = detector_BodyWeightSquat.WeightSquat(img, 11, 23, 25, True)

            print("Side Angle: ", angle_side, "Front Angle: ", angle_front)

        #     if angle_side is not None and angle_front is not None:
        #         if is_side_view:
        #             # Interpolate values based on side view interpolation ranges
        #             per_body_left = np.interp(angle_side, angle_range_left, (100, 0))
        #             bar_body_right = np.interp(angle_side, angle_range_right, (200, 400))
        #         else:
        #             # Interpolate values based on front view interpolation ranges
        #             per_body_left = np.interp(angle_front, angle_range_left, (100, 0))
        #             bar_body_right = np.interp(angle_front, angle_range_right, (200, 400))
        #             print("front view achieved")


        #         # Perform counting based on angle and direction
        #         # Adjust this logic based on your counting requirements
        #         if angle_side >= angle_range_left[0] and angle_side <= angle_range_left[1]:
        #             if dir_body_weight_squat == 0:
        #                 count_body_weight_squat += 0.5
        #                 dir_body_weight_squat = 1
        #         elif angle_side >= angle_range_left[1]:
        #             if dir_body_weight_squat == 1:
        #                 count_body_weight_squat += 0.5
        #                 dir_body_weight_squat = 0

        # # Display counting and other information
        # cv2.rectangle(img, (0, 0), (130, 120), (255, 0, 0), -1)
        # cv2.putText(img, f"{int(count_body_weight_squat)}/5", (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

        # if remaining_time <= 0:
        #     cvzone.putTextRect(img, "Time's Up", [345, 30], thickness=2, border=2, scale=2.5)
        #     display_info = False

        # if count_body_weight_squat >= 5:
        #     cvzone.putTextRect(img, 'Exercise Complete', [345, 30], thickness=2, border=2, scale=2.5)
        #     display_info = False

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
