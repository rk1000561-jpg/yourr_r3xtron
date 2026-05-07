from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
# Original API details
ORIGINAL_API_URL = "https://tabbo-vehicle2number.vercel.app/api"
ORIGINAL_API_KEY = "TABBO-7X9D"  # Jo key aapne link mein di hai

@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Vehicle Masking Server is Live"
    })

@app.route("/api/vehicle", methods=["GET"])
def vehicle():
    try:
        # User se input lena (Example: ?number=MP09XC6982)
        v_number = request.args.get("number")

        if not v_number:
            return jsonify({"status": False, "error": "Please provide a vehicle number"}), 400

        # Original API ko call karna
        # Hum apni key hide karke server-side se bhej rahe hain
        params = {
            "key": ORIGINAL_API_KEY,
            "number": v_number
        }
        
        response = requests.get(ORIGINAL_API_URL, params=params, timeout=15)
        raw_data = response.json()

        if not raw_data.get("status"):
            return jsonify({"status": False, "message": "Vehicle details not found"}), 404

        # --- DATA MASKING ---
        # Original API se sirf zaruri info nikalna
        vh_info = raw_data.get("data", {}).get("vehicle_info", {}).get("data", {})
        
        # Apna customized response format
        custom_response = {
            "success": True,
            "owner_details": {
                "name": vh_info.get("owner_name"),
                "father_name": vh_info.get("father_name"),
                "mobile": raw_data.get("data", {}).get("mobile_no", "N/A")
            },
            "vehicle_details": {
                "reg_no": vh_info.get("reg_no"),
                "model": vh_info.get("maker_modal"),
                "engine": vh_info.get("engine_no"),
                "chassis": vh_info.get("chasi_no"),
                "rto": vh_info.get("rto"),
                "age": vh_info.get("vehicle_age")
            },
            "insurance": {
                "company": vh_info.get("insurance_company"),
                "expiry": vh_info.get("insurance_upto")
            },
            "masked_by": "R3XTRON" # Aapka Brand Name
        }

        return jsonify(custom_response)

    except Exception as e:
        return jsonify({"status": False, "error": "Internal Server Error", "msg": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
