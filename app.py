"""
OpenCV Pose Estimation Web App
Main Flask application with routes for uploading and processing images
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import io
from PIL import Image

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
CONFIDENCE_THRESHOLD = 0.1

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Model paths
COCO_PROTO = "models/coco/pose_deploy_linevec.prototxt"
COCO_WEIGHTS = "models/coco/pose_iter_440000.caffemodel"
MPII_PROTO = "models/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
MPII_WEIGHTS = "models/mpi/pose_iter_160000.caffemodel"

# COCO Model Parameters
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

# MPII Model Parameters
MPII_KEYPOINTS = [
    "Head", "Neck", "R Shoulder", "R Elbow", "R Wrist",
    "L Shoulder", "L Elbow", "L Wrist", "R Hip", "R Knee",
    "R Ankle", "L Hip", "L Knee", "L Ankle", "Chest"
]

MPII_POSE_PAIRS = [
    (0, 1), (1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7),
    (1, 8), (8, 9), (9, 10), (1, 11), (11, 12), (12, 13), (1, 14)
]

# Colors for visualization
KEYPOINT_COLOR = (0, 255, 255)  # Yellow
SKELETON_COLOR = (0, 255, 0)    # Green
CONF_COLOR = (255, 0, 0)        # Red for low confidence


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_model(model_type='coco'):
    """Load the pre-trained model"""
    try:
        if model_type == 'coco':
            if not os.path.exists(COCO_WEIGHTS) or not os.path.exists(COCO_PROTO):
                return None, "COCO model files not found. Please download models first."
            net = cv2.dnn.readNetFromCaffe(COCO_PROTO, COCO_WEIGHTS)
        else:  # mpii
            if not os.path.exists(MPII_WEIGHTS) or not os.path.exists(MPII_PROTO):
                return None, "MPII model files not found. Please download models first."
            net = cv2.dnn.readNetFromCaffe(MPII_PROTO, MPII_WEIGHTS)
        
        return net, "Model loaded successfully"
    except Exception as e:
        return None, f"Error loading model: {str(e)}"


def detect_keypoints(frame, net, model_type='coco'):
    """Detect keypoints in the frame"""
    frameHeight, frameWidth = frame.shape[:2]
    
    # Prepare blob for network
    inpBlob = cv2.dnn.blobFromImage(
        frame, 1.0 / 255,
        (368, 368),
        (0, 0, 0),
        swapRB=False,
        crop=False
    )
    
    net.setInput(inpBlob)
    output = net.forward()
    
    H = output.shape[2]
    W = output.shape[3]
    
    # Get keypoint count based on model
    num_keypoints = len(COCO_KEYPOINTS) if model_type == 'coco' else len(MPII_KEYPOINTS)
    keypoints = []
    confidences = []
    
    for i in range(num_keypoints):
        probMap = output[0, i, :, :]
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        
        # Scale point to original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H
        
        if prob > CONFIDENCE_THRESHOLD:
            keypoints.append((int(x), int(y)))
            confidences.append(prob)
        else:
            keypoints.append(None)
            confidences.append(prob)
    
    return keypoints, confidences


def draw_keypoints(frame, keypoints, model_type='coco'):
    """Draw keypoints on the frame"""
    frameCopy = frame.copy()
    
    for idx, point in enumerate(keypoints):
        if point is not None:
            cv2.circle(frameCopy, point, 8, KEYPOINT_COLOR, -1, cv2.FILLED)
            
            # Get keypoint name
            keypoint_names = COCO_KEYPOINTS if model_type == 'coco' else MPII_KEYPOINTS
            text = f"{keypoint_names[idx]}"
            
            cv2.putText(
                frameCopy, text,
                (point[0] + 10, point[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2
            )
    
    return frameCopy


def draw_skeleton(frame, keypoints, model_type='coco'):
    """Draw skeleton connecting keypoints"""
    frameCopy = frame.copy()
    
    pose_pairs = COCO_POSE_PAIRS if model_type == 'coco' else MPII_POSE_PAIRS
    
    for pair in pose_pairs:
        partA = pair[0]
        partB = pair[1]
        
        if keypoints[partA] is not None and keypoints[partB] is not None:
            cv2.line(
                frameCopy,
                keypoints[partA],
                keypoints[partB],
                SKELETON_COLOR,
                3
            )
            
            # Draw circles at keypoint endpoints
            cv2.circle(frameCopy, keypoints[partA], 8, KEYPOINT_COLOR, -1, cv2.FILLED)
            cv2.circle(frameCopy, keypoints[partB], 8, KEYPOINT_COLOR, -1, cv2.FILLED)
    
    return frameCopy


def process_image(image_path, model_type='coco'):
    """Process image and detect pose"""
    frame = cv2.imread(image_path)
    
    if frame is None:
        return None, None, "Failed to read image"
    
    # Load model
    net, msg = load_model(model_type)
    if net is None:
        return None, None, msg
    
    # Detect keypoints
    keypoints, confidences = detect_keypoints(frame, net, model_type)
    
    # Draw results
    frame_with_keypoints = draw_keypoints(frame, keypoints, model_type)
    frame_with_skeleton = draw_skeleton(frame_with_keypoints, keypoints, model_type)
    
    # Prepare result data
    result_data = {
        'keypoints': [],
        'model': model_type,
        'total_detected': sum(1 for kp in keypoints if kp is not None)
    }
    
    keypoint_names = COCO_KEYPOINTS if model_type == 'coco' else MPII_KEYPOINTS
    for idx, (kp, conf) in enumerate(zip(keypoints, confidences)):
        if kp is not None:
            result_data['keypoints'].append({
                'id': idx,
                'name': keypoint_names[idx],
                'x': kp[0],
                'y': kp[1],
                'confidence': float(conf)
            })
    
    return frame_with_skeleton, result_data, "Success"


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle file upload"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        model_type = request.form.get('model', 'coco')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'}), 400
        
        try:
            # Save uploaded file
            filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process image
            result_image, result_data, message = process_image(filepath, model_type)
            
            if result_image is None:
                os.remove(filepath)
                return jsonify({'error': message}), 400
            
            # Save result image
            result_filename = f"result_{datetime.now().timestamp()}.jpg"
            result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
            cv2.imwrite(result_path, result_image)
            
            # Clean up original
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'message': message,
                'result_image': f"/static/uploads/{result_filename}",
                'data': result_data
            })
        
        except Exception as e:
            return jsonify({'error': f'Processing error: {str(e)}'}), 500
    
    return render_template('upload.html')


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models and their status"""
    models = {
        'coco': {
            'name': 'COCO (18 keypoints)',
            'keypoints': len(COCO_KEYPOINTS),
            'available': os.path.exists(COCO_WEIGHTS) and os.path.exists(COCO_PROTO),
            'speed': 'Slower but more detailed'
        },
        'mpii': {
            'name': 'MPII (15 keypoints)',
            'keypoints': len(MPII_KEYPOINTS),
            'available': os.path.exists(MPII_WEIGHTS) and os.path.exists(MPII_PROTO),
            'speed': 'Faster'
        }
    }
    return jsonify(models)


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 10MB'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Development
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # For production, use:
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
