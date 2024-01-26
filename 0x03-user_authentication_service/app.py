#!/usr/bin/env python3
"""Flask application"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """Get method for basic route"""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=["POST"], strict_slashes=False)
def users() -> str:
    """user registration endpoint"""
    email, password = request.form.get('email'), request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")