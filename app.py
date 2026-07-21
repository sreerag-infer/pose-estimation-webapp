"""
OpenCV Pose Estimation Web App - Production Ready
Automatically downloads model weights from GitHub on startup
"""

from flask import Flask, render_template, request, jsonify
import os
import cv2
import gc
import numpy as np
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
os.makedirs('models/coco', exist_ok=True)
os.makedirs('models/mpi', exist_ok=True)

COCO_PROTO = "models/coco/pose_deploy_linevec.prototxt"
COCO_WEIGHTS = "models/coco/pose_iter_440000.caffemodel"
MPII_PROTO = "models/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
MPII_WEIGHTS = "models/mpi/pose_iter_160000.caffemodel"

MODEL_URLS = {
    'coco_weights': 'https://huggingface.co/gaijingeek/openpose-models/resolve/main/pose/coco/pose_iter_440000.caffemodel',
    'mpii_weights': 'https://huggingface.co/gaijingeek/openpose-models/resolve/main/pose/mpi/pose_iter_160000.caffemodel',
}

COCO_KEYPOINTS = [
    "Nose", "Neck", "R Shoulder", "R Elbow", "R Wrist",
    "L Shoulder", "L Elbow", "L Wrist", "R Hip", "R Knee",
    "R Ankle", "L Hip", "L Knee", "L Ankle", "R Eye",
    "L Eye", "R Ear", "L Ear"
]

COCO_POSE_PAIRS = [
    (1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7),
    (1, 8), (8, 9), (9, 10), (1, 11), (11, 12), (12, 13),
    (1, 0), (0, 14), (14, 16), (0, 15), (15, 17), (2, 17), (5, 16)
]

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

MODELS_STATUS = {'coco': False, 'mpii': False}


def download_file(url, filepath, description):
    print(f"Downloading {description} from {url} ...")
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded {description} successfully")
        return True
    except Exception as e:
        print(f"Failed to download {description}: {e}")
        return False


def check_and_download_models():
    print("Checking pose estimation models...")

    if os.path.exists(COCO_WEIGHTS) and os.path.exists(COCO_PROTO):
        print("COCO model found")
        MODELS_STATUS['coco'] = True
    else:
        if download_file(MODEL_URLS['coco_weights'], COCO_WEIGHTS, "COCO weights"):
            MODELS_STATUS['coco'] = os.path.exists(COCO_PROTO)

    if os.path.exists(MPII_WEIGHTS) and os.path.exists(MPII_PROTO):
        print("MPII model found")
        MODELS_STATUS['mpii'] = True
    else:
        if download_file(MODEL_URLS['mpii_weights'], MPII_WEIGHTS, "MPII weights"):
            MODELS_STATUS['mpii'] = os.path.exists(MPII_PROTO)

    print(f"Model status: {MODELS_STATUS}")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_model(model_type='coco'):
    try:
        if model_type == 'coco':
            if not MODELS_STATUS['coco']:
                return None, "COCO model not available"
            net = cv2.dnn.readNetFromCaffe(COCO_PROTO, COCO_WEIGHTS)
        else:
            if not MODELS_STATUS['mpii']:
                return None, "MPII model not available"
            net = cv2.dnn.readNetFromCaffe(MPII_PROTO, MPII_WEIGHTS)
        return net, "OK"
    except Exception as e:
        return None, f"Error loading model: {str(e)}"


def detect_keypoints(frame, net, model_type='coco'):
    frameHeight, frameWidth = frame.shape[:2]
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (368, 368), (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()

    H, W = output.shape[2], output.shape[3]
    num_keypoints = len(COCO_KEYPOINTS) if model_type == 'coco' else len(MPII_KEYPOINTS)
    keypoints, confidences = [], []

    for i in range(num_keypoints):
        probMap = output[0, i, :, :]
        _, prob, _, point = cv2.minMaxLoc(probMap)
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > CONFIDENCE_THRESHOLD:
            keypoints.append((int(x), int(y)))
        else:
            keypoints.append(None)
        confidences.append(prob)

    return keypoints, confidences


def draw_skeleton(frame, keypoints, model_type='coco'):
    frameCopy = frame.copy()
    pose_pairs = COCO_POSE_PAIRS if model_type == 'coco' else MPII_POSE_PAIRS

    for partA, partB in pose_pairs:
        if keypoints[partA] is not None and keypoints[partB] is not None:
            cv2.line(frameCopy, keypoints[partA], keypoints[partB], SKELETON_COLOR, 3)
            cv2.circle(frameCopy, keypoints[partA], 8, KEYPOINT_COLOR, -1, cv2.FILLED)
            cv2.circle(frameCopy, keypoints[partB], 8, KEYPOINT_COLOR, -1, cv2.FILLED)

    return frameCopy


def process_image(image_path, model_type='coco'):
    frame = cv2.imread(image_path)
    if frame is None:
        return None, None, "Failed to read image"

    # Resize large images to reduce memory usage
    max_dimension = 800
    h, w = frame.shape[:2]
    if max(h, w) > max_dimension:
        scale = max_dimension / max(h, w)
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

    net, msg = load_model(model_type)
    if net is None:
        return None, None, msg

    keypoints, confidences = detect_keypoints(frame, net, model_type)
    result_frame = draw_skeleton(frame, keypoints, model_type)

    keypoint_names = COCO_KEYPOINTS if model_type == 'coco' else MPII_KEYPOINTS
    result_data = {
        'keypoints': [
            {'id': idx, 'name': keypoint_names[idx], 'x': kp[0], 'y': kp[1], 'confidence': float(conf)}
            for idx, (kp, conf) in enumerate(zip(keypoints, confidences)) if kp is not None
        ],
        'model': model_type,
        'total_detected': sum(1 for kp in keypoints if kp is not None)
    }

    del net
    import gc
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
    default_model = 'mpii' if MODELS_STATUS['mpii'] else 'coco'
    model_type = request.form.get('model', default_model)

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    if model_type == 'coco' and not MODELS_STATUS['coco']:
        model_type = 'mpii' if MODELS_STATUS['mpii'] else None
    if model_type == 'mpii' and not MODELS_STATUS['mpii']:
        model_type = 'coco' if MODELS_STATUS['coco'] else None

    if model_type is None:
        return jsonify({'error': 'No models available on server yet. Try again in a minute.'}), 503

    try:
        filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        result_image, result_data, message = process_image(filepath, model_type)

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
    return jsonify({'status': 'running', 'models': MODELS_STATUS})


@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Max 10MB'}), 413


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


check_and_download_models()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)