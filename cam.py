import cv2
# List all available cameras
def list_cameras():
    available_cameras = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)

        cap.release()
        i += 1
    return available_cameras

print("Available cameras:", list_cameras())
# Open a connection to the webcam (0 is usually the default camera)
available_cameras = list_cameras()
if not available_cameras:
    print("Error: No cameras detected.")
    exit()

if cv2.VideoCapture(3):
    cap = cv2.VideoCapture(3)
else:
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Display the resulting frame
    cv2.imshow('Webcam', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()