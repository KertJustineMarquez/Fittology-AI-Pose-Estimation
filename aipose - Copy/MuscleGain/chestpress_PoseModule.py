import cv2
import mediapipe as mp
import time
import math

# Define a class for pose detection
class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True):

        # Initialize parameters for pose detection
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth

        # Initialize mediapipe drawing utilities and pose model
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth)

    # Function find pose landmarks in the image 
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    # Function to find landmarks positions
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

    # Function to calculate angle between three points for the right arm
    def findAngle(self, img, p1, p2, p3, draw=True):
        if len(self.lmList) != 0:
            # Get the landmarks for the right arm
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            x3, y3 = self.lmList[p3][1:]

            # Calculate the angle for the right arm
            angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
            
            if angle < 0:
                angle += 360

            # Draw the angle if required
            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
                cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
                cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
                cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
                cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            return angle
        else:
            return None

# Function to capture video feed and perform pose detection
def main():
    cap = cv2.VideoCapture(r'C:\Users\RID\Desktop\pose_estimation\aipose2\Exercise\gainingmuscle\dumbbell front raise.mp4')
    pTime = 0
    detector = poseDetector()
    while True:
        # Capture frame from camera
        success, img = cap.read()

        # Find and draw pose on the frame
        img = detector.findPose(img)

        # Find landmark position for specific points (e.g, shoulder)
        lmList = detector.findPosition(img, draw=False)
        
        # Calculate and display angles
        if len(lmList) != 0:
            angle_right = detector.findAngle(img, 12, 14, 16)
            angle_left = detector.findAngle(img, 11, 13, 15)
            print("Right arm angle:", angle_right)
            print("Left arm angle:", angle_left)

        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Display the annotated image
        cv2.imshow("Image", img)
        cv2.waitKey(1)

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
