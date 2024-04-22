import cv2
import mediapipe as mp
import time
import math
import numpy as np

class poseDetectorBodyWeightSquat():

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

    #to be used for restrictions
    # def WeightSquat(self, img, p1, p2, p3, p4, p5, p6, drawpoints):
    #     if len(self.lmList) != 0:
    #         for point in [p1, p2, p3, p4, p5, p6]:
    #             if len(self.lmList[point]) < 3:
    #                 print(f"Error: Landmark {point} doesn't have enough values")
    #                 return None, None

    #         x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
    #         x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
    #         x3, y3 = self.lmList[p3][1], self.lmList[p3][2]
    #         x4, y4 = self.lmList[p4][1], self.lmList[p4][2]
    #         x5, y5 = self.lmList[p5][1], self.lmList[p5][2]
    #         x6, y6 = self.lmList[p6][1], self.lmList[p6][2]


    #         leftbody = math.degrees(math.atan2(y3 - y2, x3 - x2) -
    #                                     math.atan2(y1 - y2, x1 - x2))

    #         rightbody = math.degrees(math.atan2(y6 - y5, x6 - x5) -
    #                                     math.atan2(y4 - y5, x4 - x5))

    #         if drawpoints == True:
    #             cv2.circle(img, (x1, y1), 10, (255, 0, 255), 5)
    #             cv2.circle(img, (x1, y1), 15, (0, 255, 0), 5)
    #             cv2.circle(img, (x2, y2), 10, (255, 0, 255), 5)
    #             cv2.circle(img, (x2, y2), 15, (0, 255, 0), 5)
    #             cv2.circle(img, (x3, y3), 10, (255, 0, 255), 5)
    #             cv2.circle(img, (x3, y3), 15, (0, 255, 0), 5)
    #             cv2.circle(img, (x4, y4), 10, (255, 0, 255), 5)
    #             cv2.circle(img, (x4, y4), 15, (0, 255, 0), 5)
    #             cv2.circle(img, (x5, y5), 10, (255, 0, 255), 5)
    #             cv2.circle(img, (x5, y5), 15, (0, 255, 0), 5)
    #             cv2.circle(img, (x6, y6), 10, (255, 0, 255), 5)
    #             cv2.circle(img, (x6, y6), 15, (0, 255, 0), 5)
  
    #             # RIGHT BODY
    #             cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 6) # left arm wrist to elbow
    #             cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 6) # left arm elbow to shoulder
    #             cv2.line(img, (x1, y1), (x4, y4), (0, 0, 255), 6)

    #             # LEFT BODY
    #             cv2.line(img, (x4, y4), (x5, y5), (0, 0, 255), 6) # right arm second line
    #             cv2.line(img, (x5, y5), (x6, y6), (0, 0, 255), 6) # right arm second line
    #             cv2.line(img, (x2, y2), (x5, y5), (0, 0, 255), 6) # right arm second line

    #             cv2.putText(img, str(int(rightbody)), (x5 - 50, y5 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    #             cv2.putText(img, str(int(leftbody)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    #             return rightbody, leftbody
    #         else:
    #             return None, None

    def WeightSquat(self, img, p1, p2, p3, drawpoints):
            if len(self.lmList) != 0:
                for point in [p1, p2, p3]:
                    if len(self.lmList[point]) < 3:
                        print(f"Error: Landmark {point} doesn't have enough values")
                        return None, None

                x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
                x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
                x3, y3 = self.lmList[p3][1], self.lmList[p3][2]
     

                angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                            math.atan2(y1 - y2, x1 - x2))

                if drawpoints == True:
                    cv2.circle(img, (x1, y1), 10, (255, 0, 255), 5)
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), 5)
                    cv2.circle(img, (x2, y2), 10, (255, 0, 255), 5)
                    cv2.circle(img, (x2, y2), 15, (0, 255, 0), 5)
                    cv2.circle(img, (x3, y3), 10, (255, 0, 255), 5)
                    cv2.circle(img, (x3, y3), 15, (0, 255, 0), 5)

                    # RIGHT BODY
                    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 6) # left arm wrist to elbow
                    cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 6) # left arm elbow to shoulder

                    cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

                    return angle
                else:
                    return None, None

def main():
    cap = cv2.VideoCapture(1)
    pTime = 0
    detector = poseDetectorBodyWeightSquat()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

if __name__ == "__main__":
    main()

