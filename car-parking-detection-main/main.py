import cv2
import pickle
import cvzone
import numpy as np
import os

# Set the relative paths to the image and video files
image_path = os.path.join('car-parking-detection-main', 'carParkImg.png')
video_path = os.path.join('car-parking-detection-main', 'carPark.mp4')

# Check if video file exists
if not os.path.exists(video_path):
    print(f"Error: Video file '{video_path}' not found. Please ensure it exists in the current directory.")
    exit(1)

# Open video capture
cap = cv2.VideoCapture(video_path)

# Load parking positions
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
        print(f"Loaded {len(posList)} parking positions.")
except Exception as e:
    print(f"Error loading 'CarParkPos': {e}")
    exit(1)

width, height = 107, 48

def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        # Determine color based on occupancy
        if count < 900:
            color = (0, 255, 0)  # Free
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)  # Occupied
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))

while True:
    success, img = cap.read()
    if not success:
        print("Error: Unable to read the video stream.")
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    cv2.imshow("Parking Space Detection", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
