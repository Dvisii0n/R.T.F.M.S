from flask import Flask, Response
from flask_cors import CORS
from detection import generate_frames

app = Flask(__name__)
CORS(app)

base_url = "/api/v1"


@app.route(f"{base_url}/stream")
def stream():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )
