"""
Lightweight OpenCV Pose Estimation - MPII only
Model loaded once at startup to minimize memory usage
"""

from flask import Flask, render_template, request, jsonify
import os
import cv2
import gc
from werkzeug.utils import secure_filename
from datetime import datetime
import urllib.request

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024
CONFIDENCE_THRESHOLD = 0.1

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('models/mpi', exist_ok=True)

MPII_PROTO = "models/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
MPII_WEIGHTS = "models/mpi/pose_iter_160000.caffemodel"

MPII_WEIGHTS_URL = 'https://huggingface.co/gaijingeek/openpose-models/resolve/main/pose/mpi/pose_iter_160000.caffemodel'

MPII_KEYPOINTS = [
    "Head", "Neck", "R Shoulder", "R Elbow", "R Wrist",
    "L Shoulder", "L Elbow", "L Wrist", "R Hip", "R Knee",
    "R Ankle", "L Hip", "L Knee", "L Ankle", "Chest"
]

MPII_POSE_PAIRS = [
    (0, 1), (1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7),
    (1, 8), (8, 9), (9, 10), (1, 11), (11, 12), (12, 13), (1, 14)
]

KEYPOINT_COLOR = (0, 255, 255)
SKELETON_COLOR = (0, 255, 0)

NET = None


def download_file(url, filepath):
    print(f"Downloading model from {url} ...")
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        urllib.request.urlretrieve(url, filepath)
        print("Download complete")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def load_model_once():
    """Load the MPII model a single time at startup."""
    global NET

    if not os.path.exists(MPII_WEIGHTS):
        download_file(MPII_WEIGHTS_URL, MPII_WEIGHTS)

    if not os.path.exists(MPII_PROTO) or not os.path.exists(MPII_WEIGHTS):
        print("Model files missing, cannot load network")
        NET = None
        return

    try:
        NET = cv2.dnn.readNetFromCaffe(MPII_PROTO, MPII_WEIGHTS)
        print("MPII model loaded successfully into memory")
    except Exception as e:
        print(f"Failed to load model: {e}")
        NET = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_image(image_path):
    if NET is None:
        return None, None, "Model not loaded on server"

    frame = cv2.imread(image_path)
    if frame is None:
        return None, None, "Failed to read image"

    # Resize large images to save memory/CPU
    max_dim = 640
    h, w = frame.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
        h, w = frame.shape[:2]

    inp_blob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (184, 184), (0, 0, 0), swapRB=False, crop=False)
    NET.setInput(inp_blob)
    output = NET.forward()

    H, W = output.shape[2], output.shape[3]
    keypoints = []
    confidences = []

    for i in range(len(MPII_KEYPOINTS)):
        prob_map = output[0, i, :, :]
        _, prob, _, point = cv2.minMaxLoc(prob_map)
        x = int((w * point[0]) / W)
        y = int((h * point[1]) / H)

        if prob > CONFIDENCE_THRESHOLD:
            keypoints.append((x, y))
        else:
            keypoints.append(None)
        confidences.append(prob)

    result_frame = frame.copy()
    for partA, partB in MPII_POSE_PAIRS:
        if keypoints[partA] is not None and keypoints[partB] is not None:
            cv2.line(result_frame, keypoints[partA], keypoints[partB], SKELETON_COLOR, 2)
            cv2.circle(result_frame, keypoints[partA], 6, KEYPOINT_COLOR, -1, cv2.FILLED)
            cv2.circle(result_frame, keypoints[partB], 6, KEYPOINT_COLOR, -1, cv2.FILLED)

    result_data = {
        'keypoints': [
            {'id': idx, 'name': MPII_KEYPOINTS[idx], 'x': kp[0], 'y': kp[1], 'confidence': float(conf)}
            for idx, (kp, conf) in enumerate(zip(keypoints, confidences)) if kp is not None
        ],
        'model': 'MPII',
        'total_detected': sum(1 for kp in keypoints if kp is not None)
    }

    del output, inp_blob
    gc.collect()

    return result_frame, result_data, "Success"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result.html')
def result_page():
    return render_template('result.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        result_image, result_data, message = process_image(filepath)

        if result_image is None:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': message}), 400

        result_filename = f"result_{datetime.now().timestamp()}.jpg"
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        cv2.imwrite(result_path, result_image)

        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            'success': True,
            'message': message,
            'result_image': f"/static/uploads/{result_filename}",
            'data': result_data
        })

    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@app.route('/status')
def status():
    return jsonify({'status': 'running', 'model_loaded': NET is not None})


@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Max 10MB'}), 413


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# Load model exactly once when this module is imported (works for gunicorn and direct run)
load_model_once()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)