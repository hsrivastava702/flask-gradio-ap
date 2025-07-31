from flask import Flask, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

API_KEY = 'my_secure_api_key'
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'wav', 'json', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process_files', methods=['POST'])
def process_files():
    if request.headers.get('X-API-KEY') != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 403

    uuid_value = request.form.get('uuid')
    try:
        uuid_obj = uuid.UUID(uuid_value)
    except:
        return jsonify({"error": "Invalid UUID"}), 400

    files = {}
    for key in ['audio', 'config', 'avatar']:
        if key not in request.files:
            return jsonify({"error": f"Missing {key} file"}), 400
        f = request.files[key]
        if not allowed_file(f.filename):
            return jsonify({"error": f"Invalid {key} file type"}), 400
        filename = secure_filename(f.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(path)
        files[key] = filename

    return jsonify({
        "uuid": uuid_value,
        "files": files,
        "message": "Files processed successfully"
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
