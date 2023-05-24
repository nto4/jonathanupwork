import cv2
import numpy as np

def find_largest_rectangle(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Load the pre-trained YOLO model
    net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "yolov3.weights")

    # Get the names of the output layers
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Perform object detection
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Extract bounding boxes and class IDs of detected objects
    class_ids = []
    confidences = []
    boxes = []
    height, width, _ = image.shape

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Filter detected objects to rectangles
    rectangles = []
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in indices:
        i = i[0]
        if class_ids[i] == 0:  # Assuming class 0 represents rectangles
            x, y, w, h = boxes[i]
            rectangles.append((x, y, w, h))

    # Find the largest rectangle
    if rectangles:
        largest_rectangle = max(rectangles, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_rectangle

        # Draw the largest rectangle
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Display the result
    cv2.imshow("Largest Rectangle", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = "template2.jpg"
find_largest_rectangle(image_path)
