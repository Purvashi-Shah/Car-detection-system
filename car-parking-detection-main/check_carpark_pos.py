import cv2
import pickle
import os

# Set the relative path to the image file
image_path = os.path.join(os.getcwd(), 'car-parking-detection-main', 'carParkImg.png')

# Check if the image file exists
if not os.path.exists(image_path):
    print(f"Error: The image file at '{image_path}' does not exist.")
    exit(1)

# Load parking positions from the CarParkPos file
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    print("Error: 'CarParkPos' file not found. Please run ParkingSpacePicker.py first.")
    exit(1)
except Exception as e:
    print(f"Error loading parking positions: {e}")
    exit(1)

# Load the image
img = cv2.imread(image_path)

if img is None:
    print("Error: Image not found or could not be loaded.")
    exit(1)

# Draw rectangles for each parking space and show coordinates
for pos in posList:
    cv2.rectangle(img, pos, (pos[0] + 107, pos[1] + 48), (255, 0, 255), 2)  # Draw rectangle
    # Display coordinates next to the rectangle
    cv2.putText(img, f"{pos}", (pos[0], pos[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Show the image with marked parking spaces
cv2.imshow("Marked Parking Spaces", img)

# Wait for 'q' key to exit
cv2.waitKey(0)  # Wait indefinitely until a key is pressed
cv2.destroyAllWindows()
