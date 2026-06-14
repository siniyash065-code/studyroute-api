from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Tera PW Thor token
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3ODEwOTI5MjUuMzUsImRhdGEiOnsiX2lkIjoiNjY5NzQ4YTBjYzBkYzhhYWZkMzU0ZjAwIiwidXNlcm5hbWUiOiI5MzUxMTYzMDEzIiwiZmlyc3ROYW1lIjoiSGFyc2hpdCIsIm9yZ2FuaXphdGlvbiI6eyJfaWQiOiI1ZWIzOTNlZTk1ZmFiNzQ2OGE3OWQxODkiLCJ3ZWJzaXRlIjoicGh5c2ljc3dhbGxhaC5jb20iLCJuYW1lIjoiUGh5c2ljc3dhbGxhaCJ9LCJyb2xlcyI6WyI1YjI3YmQ5NjU4NDJmOTUwYTc3OGM2ZWYiXSwiY291bnRyeUdyb3VwIjoiSU4iLCJ0eXBlIjoiVVNFUiJ9LCJqdGkiOiJuZnRNdzRheVRIR3RmeDUwbng5RUhnXzY2OTc0OGEwY2MwZGM4YWFmZDM1NGYwMCIsImlhdCI6MTc4MDQ4ODEyNX0.Dx2lQ4kQBJfwuLbd9vqsVu8sEjj0SsoCxWl_QGmH9Q4"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

BATCHES = {
    "6984a17d4520f144c34e3745": "Commerce 11th",
    "698c4bf6f82a9d764524d6da": "Arjuna NEET 2.0"
}

SUBJECTS = {
    "6984a17d4520f144c34e3745": [
        "accountancy-491227", "business-studies-015533",
        "statistics-economics-855081", "micro-economics-489364",
        "core-maths-204037", "applied-mathematics-881282"
    ],
    "698c4bf6f82a9d764524d6da": [
        "physics-980889", "physical-chemistry-474728",
        "organic-chemistry-220063", "inorganic-chemistry-604494",
        "botany-459566", "zoology-518186"
    ]
}

@app.route('/')
def home():
    return jsonify({"status": "StudyRoute API Running!", "endpoints": ["/batches", "/videos/<batch_id>/<subject_slug>"]})

@app.route('/batches')
def get_batches():
    return jsonify({"success": True, "data": BATCHES})

@app.route('/videos/<batch_id>/<subject_slug>')
def get_videos(batch_id, subject_slug):
    url = f"https://api.penpencil.co/v2/batches/{batch_id}/subject/{subject_slug}/contents?contentType=videos&page=1"
    try:
        r = requests.get(url, headers=HEADERS)
        data = r.json()
        videos = []
        for v in data.get("data", []):
            videos.append({
                "id": v.get("_id"),
                "title": v.get("topic") or v.get("title", "Video"),
                "subject": subject_slug,
                "url": v.get("url", ""),
                "thumbnail": v.get("image", "")
            })
        return jsonify({"success": True, "data": videos})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)