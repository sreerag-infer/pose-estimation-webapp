# OpenCV Pose Estimation Web App - Complete Project Guide

## Project Overview
Build a web-based human pose estimation application that:
- Accepts image/video uploads from users
- Detects human body keypoints using pre-trained models
- Draws skeleton overlays on detected poses
- Supports both COCO and MPII models

## System Requirements
- Python 3.7+
- 2GB+ RAM
- ~500MB disk space for models
- Modern web browser

## Step-by-Step Implementation

### Phase 1: Setup & Dependencies

#### Step 1.1: Create Project Structure
```
pose_estimation_app/
│
├── app.py                    # Flask main app
├── requirements.txt          # Dependencies
├── config.py                 # Configuration
├── models/                   # Pre-trained models folder
│   ├── coco/
│   ├── mpi/
│   └── download_models.py
├── utils/
│   ├── __init__.py
│   ├── pose_detector.py      # Core pose detection logic
│   └── helpers.py            # Utility functions
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── uploads/              # Temporary uploads folder
├── templates/
│   ├── index.html
│   ├── upload.html
│   └── result.html
└── README.md
```

#### Step 1.2: Install Dependencies
Create `requirements.txt`:
```
Flask==2.3.0
opencv-python==4.8.0
numpy==1.24.0
Werkzeug==2.3.0
Pillow==10.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

### Phase 2: Download Pre-trained Models

#### Step 2.1: Model Files Needed

**For COCO Model (18 keypoints):**
- Prototxt: `pose_deploy_linevec.prototxt`
- Weights: `pose_iter_440000.caffemodel` (~200MB)
- From: http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/coco/

**For MPII Model (15 keypoints):**
- Prototxt: `pose_deploy_linevec_faster_4_stages.prototxt`
- Weights: `pose_iter_160000.caffemodel` (~200MB)
- From: http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/mpi/

#### Step 2.2: Model Download Script
Create a script to download models automatically.

### Phase 3: Core Python Implementation

#### Step 3.1: Pose Detection Utility
Core logic for detecting poses from images.

#### Step 3.2: Configuration
Define model paths, keypoint mappings, and color schemes.

#### Step 3.3: Flask Application
Create the main web app with routes for:
- Home page
- Upload file handler
- Image processing endpoint
- Result display

### Phase 4: Frontend (HTML/CSS/JavaScript)

#### Step 4.1: HTML Templates
- Index: Upload interface
- Result: Display processed images with pose overlays

#### Step 4.2: CSS Styling
Modern, responsive design with progress indicators.

#### Step 4.3: JavaScript
Handle file uploads, image previews, and result display.

### Phase 5: Testing

#### Step 5.1: Local Testing
```bash
python app.py
# Visit http://localhost:5000
```

#### Step 5.2: Test Cases
- Single image upload
- Multiple keypoint detection
- Skeleton visualization
- Error handling

### Phase 6: Deployment

#### Option A: Heroku Deployment
1. Create `Procfile`
2. Create `runtime.txt` (Python version)
3. Push to GitHub
4. Connect Heroku to GitHub repo

#### Option B: AWS/Azure
1. Create EC2/VM instance
2. Deploy Flask app
3. Use Gunicorn + Nginx

#### Option C: PythonAnywhere
1. Free Python hosting
2. Upload files directly
3. Configure WSGI app

#### Option D: Render/Railway
Modern, easy deployment platforms with free tier.

### Phase 7: Optimization & Features

#### 7.1: Performance
- Image resizing before processing
- Caching processed results
- Asynchronous processing for large files

#### 7.2: Additional Features
- Video processing capability
- Pose sequence analysis
- Confidence score display
- Skeleton line thickness control
- Multiple model selection

## Key Concepts

### COCO Model Keypoints (18 points):
0-Nose, 1-Neck, 2-RShoulder, 3-RElbow, 4-RWrist,
5-LShoulder, 6-LElbow, 7-LWrist, 8-RHip, 9-RKnee,
10-RAnkle, 11-LHip, 12-LKnee, 13-LAnkle, 14-REye,
15-LEye, 16-REar, 17-LEar

### MPII Model Keypoints (15 points):
0-Head, 1-Neck, 2-RShoulder, 3-RElbow, 4-RWrist,
5-LShoulder, 6-LElbow, 7-LWrist, 8-RHip, 9-RKnee,
10-RAnkle, 11-LHip, 12-LKnee, 13-LAnkle, 14-Chest

### COCO Pose Pairs (Skeleton Connections):
Connect keypoints to form skeleton structure:
- (1,2), (1,5), (2,3), (3,4), (5,6), (6,7)
- (1,8), (8,9), (9,10), (1,11), (11,12), (12,13)
- (1,0), (0,14), (14,16), (0,15), (15,17)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Models not downloading | Manual download from CMU-Perceptual-Computing-Lab |
| Out of memory | Reduce input image size or use smaller model |
| Slow processing | Use MPII model instead of COCO |
| CORS errors | Add Flask-CORS package |
| Model weights not found | Check file paths in config.py |

## Timeline

- **Day 1-2**: Setup, dependencies, model download
- **Day 3-4**: Core Python implementation
- **Day 5-6**: Frontend development
- **Day 7**: Testing and debugging
- **Day 8-9**: Deployment and optimization

## Additional Resources

- OpenPose GitHub: https://github.com/CMU-Perceptual-Computing-Lab/openpose
- LearnOpenCV Guide: https://learnopencv.com/deep-learning-based-human-pose-estimation-using-opencv-cpp-python/
- OpenCV DNN Documentation: https://docs.opencv.org/master/d6/d0f/group__dnn.html

## Assignment Checklist

- [ ] Project runs locally without errors
- [ ] Can upload and process images
- [ ] Displays detected keypoints
- [ ] Shows skeleton visualization
- [ ] Handles multiple people (if applicable)
- [ ] Web interface is user-friendly
- [ ] Code is well-documented
- [ ] Project is deployed and accessible online
- [ ] README.md is complete
- [ ] Source code is on GitHub (recommended)
