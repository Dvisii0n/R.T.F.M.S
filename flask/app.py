from flask import Flask, Response
from flask_cors import CORS
import app_services
from detection import generate_frames
from utils import require_auth

app = Flask(__name__)
CORS(app)

base_url = "/api/v1"


@app.route(f"{base_url}/stream")
def stream():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.get(f"{base_url}/users")
@require_auth
def users_get():
    return app_services.get_users()


@app.post(f"{base_url}/users")
def users_post():
    return app_services.create_user()


@app.post(f"{base_url}/login")
def login_post():
    return app_services.login()


# crear alerta
# ver alertas


@app.errorhandler(404)
def not_found(e):
    return {"error": "404 Not Found"}, 404


@app.errorhandler(500)
def server_error(e):
    return {"error": "500 Internal server error"}, 500
