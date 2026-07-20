# 🎯 Human Pose Estimation Web App

A powerful web-based application for detecting human body keypoints and skeleton from images using OpenCV and Deep Learning.

## 🌟 Features

- ✅ **Real-time Keypoint Detection** - Detects 18 (COCO) or 15 (MPII) body keypoints
- 🦴 **Skeleton Visualization** - Draws connected skeleton overlay on detected poses
- ⚡ **Fast Processing** - GPU-accelerated with optimized models
- 📊 **Confidence Scores** - Shows detection confidence for each keypoint
- 🎨 **Beautiful UI** - Modern, responsive web interface
- 📱 **Mobile Friendly** - Works on desktop and mobile devices
- 🔧 **Multiple Models** - Support for both COCO and MPII models

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- 2GB+ RAM
- 500MB+ free disk space (for model weights)
- Modern web browser

## 🚀 Quick Start

### 1. Clone/Download the Project

```bash
# Clone from GitHub (if available)
git clone <your-repo-url>
cd pose_estimation_app

# Or navigate to the project directory
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Download Pre-trained Models

```bash
# Run the model download script
python download_models.py

# Follow the prompts to download COCO and/or MPII models
# Note: Each model is ~200MB, so download may take some time
```

### 4. Run the Web App

```bash
# Start the Flask development server
python app.py

# The app will be available at: http://localhost:5000
```

### 5. Open in Browser

Navigate to `http://localhost:5000` and start uploading images!

## 📂 Project Structure

```
pose_estimation_app/
│
├── app.py                      # Main Flask application
├── download_models.py          # Model download utility
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku deployment config
├── runtime.txt                 # Python version for Heroku
│
├── models/                     # Pre-trained models folder
│   ├── coco/
│   │   ├── pose_deploy_linevec.prototxt
│   │   └── pose_iter_440000.caffemodel
│   └── mpi/
│       ├── pose_deploy_linevec_faster_4_stages.prototxt
│       └── pose_iter_160000.caffemodel
│
├── static/
│   ├── uploads/               # Temporary uploaded images
│   ├── css/
│   │   └── style.css         # Styling
│   └── js/
│       └── app.js            # Frontend logic
│
├── templates/
│   ├── index.html            # Home/upload page
│   ├── result.html           # Results display page
│   └── about.html            # About page
│
└── README.md                 # This file
```

## 🎮 How to Use

1. **Open the Web App** - Visit http://localhost:5000
2. **Select a Model** - Choose between COCO or MPII model
3. **Upload an Image** - Click upload area or drag & drop
4. **Wait for Processing** - AI will detect pose in the image
5. **View Results** - See keypoints, skeleton, and confidence scores
6. **Download Results** - Save the processed image with annotations

## 🤖 Models Explained

### COCO Model (18 Keypoints)
- **Speed**: Slower (~1-2 seconds per image)
- **Accuracy**: More detailed, includes facial features (eyes, ears)
- **Best for**: Detailed pose analysis, facial keypoints
- **Keypoints**: Nose, Neck, Shoulders, Elbows, Wrists, Hips, Knees, Ankles, Eyes, Ears

### MPII Model (15 Keypoints)
- **Speed**: Faster (~0.5-1 second per image)
- **Accuracy**: Core body joints, no facial features
- **Best for**: Quick processing, general pose detection
- **Keypoints**: Head, Neck, Shoulders, Elbows, Wrists, Hips, Knees, Ankles, Chest

## 🔍 Keypoint Reference

### COCO Keypoints
```
0  - Nose
1  - Neck
2  - Right Shoulder
3  - Right Elbow
4  - Right Wrist
5  - Left Shoulder
6  - Left Elbow
7  - Left Wrist
8  - Right Hip
9  - Right Knee
10 - Right Ankle
11 - Left Hip
12 - Left Knee
13 - Left Ankle
14 - Right Eye
15 - Left Eye
16 - Right Ear
17 - Left Ear
```

### MPII Keypoints
```
0  - Head
1  - Neck
2  - Right Shoulder
3  - Right Elbow
4  - Right Wrist
5  - Left Shoulder
6  - Left Elbow
7  - Left Wrist
8  - Right Hip
9  - Right Knee
10 - Right Ankle
11 - Left Hip
12 - Left Knee
13 - Left Ankle
14 - Chest
```

## 🌐 Deployment Options

### Option 1: Heroku (Recommended for Beginners)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create a new app
heroku create your-app-name

# Push to Heroku
git push heroku main

# Open in browser
heroku open
```

### Option 2: PythonAnywhere (Free Tier Available)

1. Create account at https://www.pythonanywhere.com
2. Upload project files
3. Create virtual environment
4. Configure WSGI application
5. Deploy!

### Option 3: AWS/Google Cloud

1. Create VM instance (Ubuntu recommended)
2. Install Python and dependencies
3. Configure Nginx as reverse proxy
4. Use Gunicorn for app server
5. Set up SSL with Let's Encrypt

### Option 4: Render.com (Modern Alternative)

1. Create account at https://render.com
2. Connect GitHub repository
3. Set environment variables
4. Deploy with one click!

### Option 5: Railway.app

1. Create account at https://railway.app
2. Connect GitHub repo
3. Configure build & start commands
4. Deploy instantly

## ⚙️ Configuration

Edit `app.py` to customize:

```python
# File size limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Confidence threshold for keypoints
CONFIDENCE_THRESHOLD = 0.1

# Upload folder location
UPLOAD_FOLDER = 'static/uploads'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Models not found** | Run `python download_models.py` to download |
| **Out of memory** | Reduce image size or use MPII model |
| **Slow processing** | Use MPII model or reduce input dimensions |
| **Port 5000 in use** | Change port in app.py: `app.run(port=5001)` |
| **CORS errors** | Flask-CORS is already included |
| **File upload fails** | Check file size (max 10MB) and format |
| **No keypoints detected** | Ensure person is clearly visible in image |

## 📊 Performance Tips

1. **Use MPII Model** - Faster for real-time applications
2. **Resize Images** - Smaller images = faster processing
3. **GPU Support** - Install GPU-accelerated OpenCV for faster inference
4. **Caching** - Consider caching results for identical uploads

## 🔐 Security Considerations

- ✓ File upload validation (type & size)
- ✓ Secure filename handling
- ✓ Automatic cleanup of temporary files
- ✓ Input sanitization
- ✓ Rate limiting recommended for production

## 📚 Learning Resources

- **OpenCV Docs**: https://docs.opencv.org/
- **OpenPose GitHub**: https://github.com/CMU-Perceptual-Computing-Lab/openpose
- **LearnOpenCV Guide**: https://learnopencv.com/deep-learning-based-human-pose-estimation-using-opencv-cpp-python/
- **Flask Docs**: https://flask.palletsprojects.com/

## 🎓 Assignment Checklist

- [ ] Project setup and dependencies installed
- [ ] Models downloaded successfully
- [ ] Web app runs locally without errors
- [ ] Image upload works correctly
- [ ] Keypoint detection functioning
- [ ] Skeleton visualization displaying
- [ ] Results page showing all information
- [ ] UI is responsive and user-friendly
- [ ] Code is well-documented with comments
- [ ] README.md is complete
- [ ] Project deployed to a web server
- [ ] GitHub repository created (optional but recommended)

## 💡 Possible Enhancements

1. **Video Processing** - Detect poses in video frames
2. **Batch Processing** - Process multiple images at once
3. **Activity Recognition** - Detect activities based on poses
4. **Pose Comparison** - Compare two poses
5. **Statistics** - Track pose detection statistics
6. **Real-time Webcam** - Live pose detection from webcam
7. **3D Pose Estimation** - Reconstruct 3D pose from 2D keypoints
8. **Angle Measurement** - Calculate joint angles from keypoints

## 📝 License

This project uses open-source components:
- OpenCV (3-Clause BSD License)
- Flask (BSD License)
- COCO and MPII datasets

## 👨‍💻 Author & Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Check OpenCV documentation
4. Visit OpenPose GitHub discussions

## 🙏 Acknowledgments

- CMU Perceptual Computing Lab (OpenPose)
- OpenCV Community
- COCO Dataset team
- MPII Dataset team

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready ✓

Happy pose detecting! 🎯
