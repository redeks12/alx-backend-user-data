# !/usr/bin/env python3
"""0x03. User authentication service"""

from auth import Auth
from flask import Flask, jsonify, request, abort

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def hello():
    """default route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def reg_users():
    """register users"""

    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": f"{user.email}", "message": "user created"}), 200


@app.route("/sessions", methods=["POST"])
def login():
    """login user"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)

    ret = jsonify({"email": f"{email}", "message": "logged in"})
    ret.set_cookie("session_id", AUTH.create_session(email))
    return ret


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
