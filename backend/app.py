import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

IBM_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
MODEL_ID = "ibm/granite-4-h-small"
PROJECT_ID = "220422b5-05e9-47cf-b3d6-dc65461207b4"
API_KEY = "GGs4QrwSy28R0bRQP7IhNNiJtHWWiaRD1cAL5emdUKqn"
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
_cached_token = None


def get_iam_token():
    global _cached_token
    r = requests.post(IAM_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": API_KEY},
        timeout=30)
    r.raise_for_status()
    _cached_token = r.json()["access_token"]
    return _cached_token


def call_granite(prompt, retries=3):
    token = get_iam_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "model_id": MODEL_ID, "project_id": PROJECT_ID, "input": prompt,
        "parameters": {"decoding_method": "greedy", "max_new_tokens": 800, "repetition_penalty": 1.1}
    }
    for attempt in range(retries):
        r = requests.post(IBM_URL, headers=headers, json=payload, timeout=60)
        if r.status_code == 429:
            wait = 15 * (attempt + 1)  # 15s, 30s, 45s
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()["results"][0]["generated_text"].strip()
    r.raise_for_status()  # raise the final 429 if all retries exhausted


def build_travel_prompt(data):
    d = data.get("destination", "")
    o = data.get("origin", "")
    sd = data.get("start_date", "")
    ed = data.get("end_date", "")
    t = data.get("travelers", 1)
    b = data.get("budget", "")
    i = ", ".join(data.get("interests", [])) or "general sightseeing"
    sr = data.get("special_requests", "")
    dur = f"from {sd} to {ed}" if sd and ed else "not specified"
    return (
        f"You are an expert travel planner AI. Create a detailed, practical travel plan.\n"
        f"Destination: {d}\nOrigin: {o}\nDates: {dur}\nTravelers: {t}\n"
        f"Budget: {b}\nInterests: {i}\nSpecial Requests: {sr}\n\n"
        f"Provide:\n1) Trip Overview\n2) Day-by-Day Itinerary\n3) Accommodation\n"
        f"4) Local Food\n5) Transportation\n6) Packing List\n7) Budget Breakdown\n"
        f"8) Travel Tips\n9) Hidden Gems\nUse clear headers and bullet points."
    )


@app.route("/api/plan", methods=["POST"])
def plan_trip():
    try:
        data = request.get_json()
        if not data or not data.get("destination"):
            return jsonify({"error": "Destination is required."}), 400
        return jsonify({"plan": call_granite(build_travel_prompt(data)), "destination": data["destination"]})
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"IBM API error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        context = data.get("context", "")
        if not message:
            return jsonify({"error": "Message is required."}), 400
        ctx = f"Context: {context}\n" if context else ""
        prompt = f"You are TravelBot, a friendly travel planning assistant.\n{message}\nTravelBot: "
        return jsonify({"reply": call_granite(prompt)})
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"IBM API error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/suggest", methods=["POST"])
def suggest_destinations():
    try:
        data = request.get_json()
        p = data.get("preferences", "general travel")
        s = data.get("season", "any")
        bl = data.get("budget_level", "moderate")
        prompt = (
            f"You are an expert travel consultant. Suggest 5 amazing destinations.\n"
            f"Preferences: {p}\nSeason: {s}\nBudget Level: {bl}\n"
            f"For each: name and country, why it matches, best time, budget estimate, top 3 highlights. Numbered list."
        )
        return jsonify({"suggestions": call_granite(prompt)})
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"IBM API error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": MODEL_ID})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
