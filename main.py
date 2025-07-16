from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/analyze', methods=['POST'])
def analyze():
    # Check if 'resume' and 'job_description' are in the request
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "Missing resume file or job description"}), 400

    resume_file = request.files['resume']
    job_desc = request.form['job_description']

    # For demo, we just simulate analysis
    # Replace this with your actual AI resume tailoring logic
    match_score = 85  # Example static score
    tailored_resume = f"Tailored resume for job description:\n{job_desc}\n\n(Resume file name: {resume_file.filename})"

    return jsonify({
        "match_score": match_score,
        "tailored_resume": tailored_resume
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
