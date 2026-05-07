from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/api/vehicle", methods=["GET"])
def vehicle():
    try:
        number = request.args.get("number")

        if not number:
            return jsonify({
                "status": False,
                "error": "Vehicle number required"
            }), 400

        url = f"https://external-api.com?number={number}"

        headers = {
            "Authorization": API_KEY
        }

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        return jsonify({
            "status": True,
            "number": number,
            "data": data
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "error": "Server error",
            "message": str(e)
        }), 500
