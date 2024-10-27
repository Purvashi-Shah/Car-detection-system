import cv2
import pickle
import os

# Set the relative path to the image file
image_path = os.path.join(os.getcwd(), 'car-parking-detection-main', 'carParkImg.png')

# Check if the image file exists
if not os.path.exists(image_path):
    print(f"Error: The image file at '{image_path}' does not exist.")
    exit(1)  # Exit if the image does not exist

width, height = 107, 48

# Load previously saved positions or initialize an empty list
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []  # If the file doesn't exist, start with an empty list
except Exception as e:
    print(f"Error loading parking positions: {e}")
    posList = []

# Function to handle mouse clicks
def mouseClick(events, x, y, flags, params):
    global posList  # Ensure we use the global posList
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))  # Add position on left click
        print(f"Added position: {(x, y)}")
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)  # Remove position on right click
                print(f"Removed position: {(x1, y1)}")
                break  # Exit the loop after removal

    # Save updated positions when they change
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)  # Save updated positions
        print("Saved updated parking positions.")

# Main loop to display the image and handle interactions
while True:
    img = cv2.imread(image_path)  # Read the image from the specified path
    if img is None:
        print("Error: Image not found or could not be loaded.")
        break  # Exit the loop if the image cannot be loaded

    # Draw rectangles for parking spaces
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    # Show instructions to the user
    cv2.putText(img, "Left-click to mark, Right-click to remove. Press 'q' to exit.", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Image", img)  # Show the image
    cv2.setMouseCallback("Image", mouseClick)  # Set mouse callback

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key press
        print("Exiting without saving changes.")
        break

cv2.destroyAllWindows()  # Close all OpenCV windows
