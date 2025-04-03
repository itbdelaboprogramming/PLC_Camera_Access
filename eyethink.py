from ultralytics import YOLO
import cv2
import socket

# Load the YOLO model (pre-trained on COCO dataset)
model = YOLO('yolov8n.pt', verbose=False)  # You can use 'yolov8s.pt', 'yolov8m.pt', etc.

# Open a video capture (0 for webcam or provide a video file path)
cap = cv2.VideoCapture(3)
# Set up a socket connection
server_ip = "192.168.110.10"
server_port = 8501
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform inference
    results = model(frame, verbose=False)
    
    # Extract boxes, class IDs, and confidence scores
    boxes = results[0].boxes.xyxy  # Bounding box coordinates
    class_ids = results[0].boxes.cls  # Class IDs
    confidences = results[0].boxes.conf  # Confidence scores

    # Draw only "person" (class ID 0)
    for i in range(len(boxes)):
        if int(class_ids[i]) == 0:  # Class ID 0 corresponds to "person"
            x1, y1, x2, y2 = map(int, boxes[i])
            confidence = float(confidences[i])
            label = f"Person {confidence:.2f}"

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # Assume the average width of a person is 0.5 meters
            avg_person_width_m = 0.45

            # Calculate the perceived width in pixels
            perceived_width_px = x2 - x1

            # Focal length (in pixels) - you may need to calibrate this for your camera
            # Define resolution width in pixels
            resolution_width_px = 1920  # Resolution width in pixels (1920x1080)

            # Calculate the focal length in pixels
            focal_length_mm = 3.67  # Focal length in mm
            sensor_width_mm = 7.68  # Sensor width in mm (calculated from 1/2.88 inch sensor size)
            focal_length_px = (focal_length_mm / sensor_width_mm) * resolution_width_px

            # Calculate the distance to the person
            distance_m = (avg_person_width_m * focal_length_px) / perceived_width_px

            # Print the perceived distance
            print(f"Detected person at distance: {distance_m:.2f} meters")

            # Display the distance on the frame
            distance_label = f"Distance: {distance_m:.2f}m"
            cv2.putText(frame, distance_label, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            if distance_m < 2:
                sock.sendall(b"WR MR002 1\r")
            else:
                sock.sendall(b"WR MR002 0\r")

    # Display the frame
    cv2.imshow('People Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
