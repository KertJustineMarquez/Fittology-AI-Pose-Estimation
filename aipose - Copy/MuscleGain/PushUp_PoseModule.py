import cv2
import mediapipe as mp
import time
import math
import numpy as np

class poseDetectorPushUp():

    def __init__(self, mode=False, upBody=False, smooth=True):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findPushupAngle(self, img, p1,p2,p3,p4,p5,p6, drawpoints):

        if len(self.lmList)!= 0:

            for point in [p1, p2, p3, p4, p5, p6]:
                if len(self.lmList[point]) < 3:
                    print(f"Error: Landmark {point} doesn't have enough values")
                    return None, None

            x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
            x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
            x3, y3 = self.lmList[p3][1], self.lmList[p3][2]
            x4, y4 = self.lmList[p4][1], self.lmList[p4][2]
            x5, y5 = self.lmList[p5][1], self.lmList[p5][2]
            x6, y6 = self.lmList[p6][1], self.lmList[p6][2]


            lefthandangle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                         math.atan2(y1 - y2, x1 - x2))
            
            if lefthandangle < 0:
                lefthandangle += 360

            righthandangle = math.degrees(math.atan2(y6 - y5, x6 - x5) -
                                          math.atan2(y4 - y5, x4 - x5))
            
            if righthandangle < 0:
                righthandangle += 360

            if drawpoints == True:
                cv2.circle(img,(x1,y1),10,(255,0,255),5)
                cv2.circle(img, (x1, y1), 15, (0,255, 0),5)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), 5)
                cv2.circle(img, (x2, y2), 15, (0, 255, 0), 5)
                cv2.circle(img, (x3, y3), 10, (255, 0, 255), 5)
                cv2.circle(img, (x3, y3), 15, (0, 255, 0), 5)
                cv2.circle(img, (x4, y4), 10, (255, 0, 255), 5)
                cv2.circle(img, (x4, y4), 15, (0, 255, 0), 5)
                cv2.circle(img, (x5, y5), 10, (255, 0, 255), 5)
                cv2.circle(img, (x5, y5), 15, (0, 255, 0), 5)
                cv2.circle(img, (x6, y6), 10, (255, 0, 255), 5)
                cv2.circle(img, (x6, y6), 15, (0, 255, 0), 5)

                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 6)
                cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 6)
                cv2.line(img, (x4, y4), (x5, y5), (0, 0, 255), 6)
                cv2.line(img, (x5, y5), (x6, y6), (0, 0, 255), 6)
                cv2.line(img, (x1, y1), (x4, y4), (0, 0, 255), 6)

                cv2.putText(img, str(int(lefthandangle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                cv2.putText(img, str(int(righthandangle)), (x5 - 50, y5 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

                return int(lefthandangle), int(righthandangle)
            else:
                return None, None
            

    def isPushUpPosture(self, lmList):
        # Check if keypoints are available
        if len(lmList) < 5:
            return False

        # Extract keypoint coordinates
        x_values = [lm[1] for lm in lmList]
        y_values = [lm[2] for lm in lmList]

        # Calculate torso height as the distance between the shoulders and the hips
        torso_height = np.abs(y_values[11] - y_values[23])

        # Calculate average arm length as the distance between the shoulder and elbow joints
        avg_arm_length = np.mean([np.abs(y_values[11] - y_values[13]), np.abs(y_values[12] - y_values[14])])

        # Calculate the angle of the torso relative to the ground
        torso_angle = np.arctan2(y_values[11] - y_values[23], x_values[11] - x_values[23])

        # Check if the person is in a push-up posture based on the approximate shape of the body
        # and the angle of the torso
        if torso_height > 0.2 * avg_arm_length and torso_angle < np.pi / 5:  # Adjust the thresholds as needed
            return True
        else:
            return False

def main():
    cap = cv2.VideoCapture(1)
    pTime = 0
    detector = poseDetectorPushUp()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)

        if lmList:
            angle = detector.findPushupAngle(img)
            if angle is not None:
                print("Angle:", angle)


        if lmList:
            if detector.isPushUpPosture(lmList):  # Check if the detected posture resembles a push-up posture
                angle = detector.findPushupAngle(img)
                if angle is not None:
                    print("Angle:", angle)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()

