import jwt
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify

EXPIRES_AT_SECONDS = 86400  # 1 dia

load_dotenv()


def create_jwt(user):
    expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=EXPIRES_AT_SECONDS)
    payload = {
        "sub": str(user["id"]),
        "user": user["nombre"],
        "iat": datetime.now(tz=timezone.utc),
        "exp": expires_at,
    }

    token = jwt.encode(payload=payload, key=os.getenv("JWT_SECRET"), algorithm="HS256")
    return token


def verify_token(token):
    try:
        payload = jwt.decode(jwt=token, key=os.getenv("JWT_SECRET"), algorithms="HS256")
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Unauthorized"}), 401
        request.user_id = payload["sub"]
        return f(*args, **kwargs)

    return decorated
