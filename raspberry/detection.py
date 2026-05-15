from ultralytics import YOLO
import cv2
import urllib.request
import json

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

model_path = "fire_model.pt"
class_names = ["fire"]

default_location = {"lat": 23.2435, "lon": -106.4294}

model = YOLO(model_path)


def run_yolo(img, class_names):
    results = model(img, stream=True)

    for result in results:
        boxes = result.boxes

        send_detection_event(len(boxes))

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

        run_yolo(img, class_names)
        _, buffer = cv2.imencode(".jpg", img)
        frame_bytes = buffer.tobytes()

        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")


def send_detection_event(num_detections):
    risk = get_risk(num_detections)
    data = json.dumps(
        {
            "type": "DETECCION",
            "num_detecciones": num_detections,
            "ubicacion": default_location,
            "nivel_riesgo": risk,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:8081/send_event",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as response:
            print("Response:", response.read().decode())
    except Exception as e:
        print("Error:", e)


def get_risk(num_detections):
    if num_detections == 0:
        return "SEGURO"

    if num_detections == 1:
        return "BAJO"

    if num_detections == 2:
        return "MEDIO"

    if num_detections >= 3:
        return "ALTO"


# for i in range(1, 30):
#     img = cv2.imread("test_fuego.png")
#     run_yolo(img, class_names)
