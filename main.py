from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import extract_text_from_file
from tailor_ai import generate_tailored_resume, calculate_match_score
import os

app = Flask(__name__)
CORS(app)

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/", methods=["GET"])
def home():
    return "✅ Resume Tailor Backend is live"

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        print("📩 Received POST to /analyze")
        print("Files:", request.files)
        print("Form data:", request.form)

        resume_file = request.files["resume"]
        job_description = request.form["job_description"]

        resume_text = extract_text_from_file(resume_file)
        print("📝 Extracted Resume Text:", resume_text[:300])

        if not resume_text.strip():
            return jsonify({"error": "❌ Resume content could not be extracted."}), 400

        match_score = calculate_match_score(resume_text, job_description)
        print("🎯 Match Score:", match_score)

        tailored_resume = generate_tailored_resume(resume_text, job_description)
        print("📄 Tailored Resume Generated.")

        return jsonify({
            "match_score": match_score,
            "tailored_resume": tailored_resume
        })

    except Exception as e:
        print("❌ Error in analyze_resume():", e)
        return jsonify({"error": str(e)}), 500

# ✅ Correct port binding for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
