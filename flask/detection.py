from ultralytics import YOLO
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

model_path = "test_model.pt"
class_names = ["person"]


def run_yolo(img, model_path, class_names):
    model = YOLO(model_path)
    results = model(img, stream=True)

    for result in results:
        boxes = result.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

            cls = int(box.cls[0])

            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (0, 0, 255)
            thickness = 2

            cv2.putText(img, class_names[cls], org, font, fontScale, color, thickness)


def generate_frames():
    while True:
        success, img = cap.read()

        run_yolo(img, model_path, class_names)
        _, buffer = cv2.imencode(".jpg", img)
        frame_bytes = buffer.tobytes()

        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
