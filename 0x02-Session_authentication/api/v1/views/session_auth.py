#!/usr/bin/env python3
""" Module of Index views
"""
from os import getenv

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route("/auth_session/login/", methods=["POST"])
@app_views.route("/auth_session/login", methods=["POST"])
def auth_login():
    """handle login request from flask"""

    email = request.form.get("email")
    pwd = request.form.get("password")

    if email is None:
        return jsonify({"error": "email missing"}), 400

    if pwd is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user[0].id)
    session_name = getenv("SESSION_NAME")
    auth.session_cookie(request)
    ret_sta = jsonify(user[0].to_json())
    ret_sta.set_cookie(session_name, session_id)
    return ret_sta


@app_views.route("/auth_session/logout/", methods=["DELETE"])
@app_views.route("/auth_session/logout", methods=["DELETE"])
def auth_logout():
    """handle logout request from flask"""

    from api.v1.app import auth

    destroyed_sess = auth.destroy_session(request)
    if destroyed_sess:
        return jsonify({}), 200

    abort(404)
