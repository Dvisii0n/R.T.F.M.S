from db import cursor, conn
import bcrypt
from flask import request, abort
import traceback
from utils import create_jwt


def get_users():
    cursor.execute("SELECT id, nombre, email FROM usuarios")
    users = cursor.fetchall()
    return users


def create_user():
    try:
        form_data = dict(request.form)
        password = form_data["password"]
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(bytes, salt)
        decoded_hash = hashed.decode("utf-8")
        data = (form_data["nombre"], form_data["email"], decoded_hash)
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", data
        )
        conn.commit()
        return {"success": "Created user"}
    except Exception:
        traceback.print_exc()
        abort(500)


def login():
    try:
        form_data = dict(request.form)
        username = form_data["nombre"]
        cursor.execute(
            "SELECT id, nombre, email, password FROM usuarios WHERE nombre = %s",
            (username,),
        )

        user = cursor.fetchone()

        if not user:
            return {"error": "Invalid username"}, 401

        pw_bytes = form_data["password"].encode("utf-8")
        pw_hash = user["password"].encode("utf-8")

        pw_match = bcrypt.checkpw(pw_bytes, pw_hash)

        if not pw_match:
            return {"error": "Invalid password"}

        jwt = create_jwt(user)

        return {"token": jwt}

    except Exception:
        traceback.print_exc()
        abort(500)


def create_alert():
    try:
        req_body = request.get_json()
        data = (
            req_body["descripcion"],
            req_body["latitud"],
            req_body["longitud"],
            req_body["num_detecciones"],
            req_body["peligro"],
        )
        cursor.execute(
            "INSERT INTO alertas (descripcion, latitud, longitud, num_detecciones, peligro) VALUES (%s, %s, %s, %s, %s)",
            data,
        )
        conn.commit()
        return {"success": "Alert created"}

    except Exception:
        traceback.print_exc()
        abort(500)


def get_alerts():
    try:
        cursor.execute("SELECT * FROM alertas")
        alerts = cursor.fetchall()
        return alerts
    except Exception:
        traceback.print_exc()
        abort(500)


def get_alert(alertId):
    try:
        cursor.execute("SELECT * FROM alertas WHERE id = %s", (alertId,))
        alert = cursor.fetchone()
        return alert
    except Exception:
        traceback.print_exc()
        abort(500)
