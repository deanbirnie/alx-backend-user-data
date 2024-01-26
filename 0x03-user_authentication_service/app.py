#!/usr/bin/env python3
"""Flask application"""
from flask import Flask, jsonify, request, abort, redirect

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """Get method for basic route"""
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
