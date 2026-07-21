"""
Pose Estimation using MediaPipe
No downloads needed! Works instantly.
Actually better detection than OpenCV DNN.
"""

from flask import Flask, render_template, request, jsonify
import cv2
import mediapipe as mp
from mediapipe.python.solutions import pose as mp_pose_module
from mediapipe.python.solutions import drawing_utils as mp_drawing
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize MediaPipe Pose
print("Loading MediaPipe Pose model...")
mp_pose = mp_pose_module
pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=0,  # 0=lite, 1=full, 2=heavy
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

print("✓ MediaPipe model loaded successfully!")
print("Ready for pose estimation!")

# MediaPipe Keypoint names (33 points)
KEYPOINT_NAMES = [
    "Nose",           # 0
    "L Eye Inner",    # 1
    "L Eye",          # 2
    "L Eye Outer",    # 3
    "R Eye Inner",    # 4
    "R Eye",          # 5
    "R Eye Outer",    # 6
    "L Ear",          # 7
    "R Ear",          # 8
    "Mouth Left",     # 9
    "Mouth Right",    # 10
    "L Shoulder",     # 11
    "R Shoulder",     # 12
    "L Elbow",        # 13
    "R Elbow",        # 14
    "L Wrist",        # 15
    "R Wrist",        # 16
    "L Pinky",        # 17
    "R Pinky",        # 18
    "L Index",        # 19
    "R Index",        # 20
    "L Thumb",        # 21
    "R Thumb",        # 22
    "L Hip",          # 23
    "R Hip",          # 24
    "L Knee",         # 25
    "R Knee",         # 26
    "L Ankle",        # 27
    "R Ankle",        # 28
    "L Heel",         # 29
    "R Heel",         # 30
    "L Foot Index",   # 31
    "R Foot Index"    # 32
]

# Pose connections (skeleton)
POSE_CONNECTIONS = [
    # Face
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),
    (9, 10),
    
    # Upper body
    (11, 12),
    (11, 13), (13, 15),
    (12, 14), (14, 16),
    
    # Lower body
    (11, 23), (12, 24),
    (23, 24),
    (23, 25), (25, 27),
    (24, 26), (26, 28),
    (27, 29), (28, 30),
    (29, 31), (30, 32)
]

def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path):
    """Process image with MediaPipe pose detection"""
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        return None, None, "Failed to read image"
    
    h, w, c = image.shape
    
    # Convert BGR to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Run pose detection
    results = pose.process(image_rgb)
    
    # Copy for drawing
    output_image = image.copy()
    
    keypoints_detected = []
    
    if results.pose_landmarks:
        # Draw skeleton using MediaPipe's drawing utilities
        mp_drawing.draw_landmarks(
            output_image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(0, 255, 255),      # Yellow for keypoints
                thickness=2,
                circle_radius=2
            ),
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(0, 255, 0),        # Green for connections
                thickness=2
            )
        )
        
        # Extract keypoints with confidence
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            confidence = landmark.visibility
            
            # Only include detected keypoints (confidence > 0.3)
            if confidence > 0.3:
                keypoints_detected.append({
                    'id': idx,
                    'name': KEYPOINT_NAMES[idx],
                    'x': x,
                    'y': y,
                    'confidence': float(confidence)
                })
    
    # Prepare result data
    result_data = {
        'keypoints': keypoints_detected,
        'model': 'MediaPipe',
        'model_info': '33 keypoints - includes face, hands, and body',
        'total_detected': len(keypoints_detected)
    }
    
    return output_image, result_data, "Success"

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/result.html')
def result_page():
    return render_template('result.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle file upload"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'
            }), 400
        
        try:
            # Save uploaded file
            filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process image
            result_image, result_data, message = process_image(filepath)
            
            if result_image is None:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': message}), 400
            
            # Save result image
            result_filename = f"result_{datetime.now().timestamp()}.jpg"
            result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
            cv2.imwrite(result_path, result_image)
            
            # Clean up original
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
    
    return render_template('upload.html')

@app.route('/api/models')
def get_models():
    """Get available models"""
    return jsonify({
        'mediapipe': {
            'name': 'MediaPipe Pose',
            'keypoints': 33,
            'available': True,
            'speed': 'Very fast',
            'includes': ['Face', 'Hands', 'Body', 'Feet'],
            'download': 'None - built-in!'
        }
    })

@app.route('/status')
def status():
    """Get app status"""
    return jsonify({
        'status': 'running',
        'model': 'MediaPipe Pose',
        'keypoints': 33,
        'ready': True
    })

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large"""
    return jsonify({'error': 'File too large. Maximum size is 10MB'}), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎯 MediaPipe Pose Estimation Web App")
    print("="*60)
    print("✓ Model loaded and ready!")
    print("✓ No downloads needed!")
    print("✓ 33 keypoints detection")
    print("\nStarting server...")
    print("Open: http://localhost:5000")
    print("="*60 + "\n")
    
    # Development
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # For production:
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
