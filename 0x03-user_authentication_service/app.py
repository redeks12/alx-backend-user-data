#!/usr/bin/env python3
"""0x03. User authentication service"""

from auth import Auth
from flask import Flask, abort, jsonify, redirect, request

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
        return (
            jsonify(
                {
                    "email": f"{user.email}",
                    "message": "user \
created",
                }
            ),
            200,
        )


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


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logout from the admin"""
    sess_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(sess_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("hello")

    return jsonify({"error": "user not found"}), 403


@app.route("/profile", methods=["GET"])
def profile():
    """return profile information"""
    sess_id = request.cookies.get("session_id")
    if sess_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(sess_id)
    if user:
        ret = jsonify({"email": user.email})
        ret.set_cookie("session_id", sess_id)
        return ret, 200
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """get reset password token"""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """update password for user"""
    email = request.form.get("email")
    password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")

    try:
        AUTH.update_password(reset_token, password)
        return jsonify({"email": f"{email}", "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
