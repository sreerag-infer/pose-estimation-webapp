# ⚡ Quick Start Guide - 10 Minutes Setup

Follow these steps to get your pose estimation web app running in under 10 minutes!

## Step 1: Install Python (2 min)

If you don't have Python installed:
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or higher
3. Run installer, **check "Add Python to PATH"**
4. Verify installation:
   ```bash
   python --version
   pip --version
   ```

## Step 2: Setup Project (1 min)

```bash
# Navigate to your project folder
cd pose_estimation_app

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line.

## Step 3: Install Dependencies (3 min)

```bash
pip install -r requirements.txt
```

This installs Flask, OpenCV, and other required packages.

## Step 4: Download Models (3 min)

```bash
python download_models.py
```

When prompted, type `y` to download models. This downloads ~400MB of pre-trained weights.
- COCO model: Better quality, slower
- MPII model: Faster, good for real-time

## Step 5: Run the App (1 min)

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

## Step 6: Open in Browser

1. Open your web browser
2. Go to: http://localhost:5000
3. You should see the upload interface!

## Step 7: Test It!

1. Find an image with a person in it
2. Upload it to the web app
3. Wait for processing
4. See the skeleton overlay!

---

## 🚀 Next Steps

### To Deploy Online:

#### **Easy Option: Render.com**
1. Go to https://render.com
2. Sign up with GitHub
3. Create new Web Service
4. Connect this repository
5. Deploy!

#### **Alternative: Heroku**
```bash
# Install Heroku CLI
# Then:
heroku login
heroku create
git push heroku main
```

#### **Simple Option: PythonAnywhere**
1. Sign up at https://www.pythonanywhere.com
2. Upload files
3. Configure WSGI
4. Done!

---

## ❓ Common Issues

**Issue**: "Python not found"
- **Solution**: Install Python from https://python.org and add to PATH

**Issue**: Models download stuck
- **Solution**: Try manual download from CMU OpenPose or use pre-downloaded versions

**Issue**: Port 5000 already in use
- **Solution**: Change port in app.py line: `app.run(port=5001)`

**Issue**: No keypoints detected
- **Solution**: Ensure person is clearly visible in image, not too small/obscured

---

## 📁 File Structure After Setup

```
pose_estimation_app/
├── app.py
├── download_models.py
├── requirements.txt
├── README.md
├── QUICK_START.md (this file)
├── models/
│   ├── coco/
│   │   ├── pose_deploy_linevec.prototxt
│   │   └── pose_iter_440000.caffemodel (after download)
│   └── mpi/
│       ├── pose_deploy_linevec_faster_4_stages.prototxt
│       └── pose_iter_160000.caffemodel (after download)
├── static/
│   └── uploads/ (created automatically)
└── templates/
    ├── index.html
    └── result.html
```

---

## 🎯 Assignment Submission Checklist

- [ ] Code runs locally without errors
- [ ] Web app accessible at localhost:5000
- [ ] Can upload images successfully
- [ ] Pose detection working
- [ ] Results display correctly
- [ ] App deployed online (with live URL)
- [ ] README.md is complete
- [ ] Code is clean and commented
- [ ] GitHub repo created (if required)

---

## 💡 Pro Tips

1. **Test with sample images first** - Download some from internet
2. **Use MPII model initially** - Faster for testing
3. **Keep images under 2MB** - Faster processing
4. **Use clear, well-lit photos** - Better detection
5. **Deploy early** - Don't wait until the last minute!

---

## 📞 Quick Help

| Problem | Command |
|---------|---------|
| Activate virtual environment | `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows) |
| Install packages | `pip install -r requirements.txt` |
| Download models | `python download_models.py` |
| Start app | `python app.py` |
| Stop app | `Ctrl + C` |
| Deactivate venv | `deactivate` |

---

## 🎉 Success!

If you've completed all steps, you now have a working pose estimation web app!

**What you can do now:**
- ✅ Upload images
- ✅ Detect human poses
- ✅ View keypoints and skeleton
- ✅ Download processed images
- ✅ Deploy to web server

---

**Estimated Time: 10 minutes**
**Difficulty: Easy ⭐**
**Result: Working Pose Estimation Web App! 🎯**

Happy coding! 🚀
