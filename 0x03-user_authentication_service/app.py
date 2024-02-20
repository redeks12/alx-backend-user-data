# !/usr/bin/env python3
"""0x03. User authentication service"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello():
    """default route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def reg_users():
    """register users"""
    from auth import Auth

    AUTH = Auth()
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": f"{user.email}", "message": "user created"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
