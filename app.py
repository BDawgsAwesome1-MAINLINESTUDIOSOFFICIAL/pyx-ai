"""
Pyx API — WSGI app for gunicorn / Cloud Run (pyxaiapi).

  POST /score   Body: {"text": "..."}   → {"score", "bad", "censored"}
  GET  /health  → {"status": "ok", "service": "pyx"}
"""

import json
import os

from flask import Flask, request, jsonify

from pyx_ai import PyxAI, BAN_LINE, censor_letters

app = Flask(__name__)
pyx = PyxAI()


@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/health")
@app.route("/")
def health():
    return jsonify({"status": "ok", "service": "pyx"})


@app.route("/score", methods=["GET", "POST", "OPTIONS"])
def score():
    if request.method == "OPTIONS":
        return "", 204
    if request.method != "POST":
        return jsonify({"error": "Method not allowed"}), 405
    data = request.get_json(silent=True) or {}
    text = data.get("text")
    if text is None:
        return jsonify({"error": "Missing \"text\" in body"}), 400
    if not isinstance(text, str):
        return jsonify({"error": "\"text\" must be a string"}), 400
    if len(text) > 1_000_000:
        return jsonify({"error": "Text too long"}), 413
    s = pyx.score(text)
    bad = s >= BAN_LINE
    censored = censor_letters(text) if bad else text
    return jsonify({
        "score": round(s, 4),
        "bad": bad,
        "censored": censored,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
