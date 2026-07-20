# 🌐 Deployment Guide - Host Your Web App Online

Choose one of these platforms to make your pose estimation app accessible online!

---

## 🟢 Option 1: Render.com (EASIEST - RECOMMENDED)

**Time**: 10 minutes
**Cost**: Free tier available
**Difficulty**: ⭐ (Very Easy)

### Steps:

1. **Create Account**
   - Go to https://render.com
   - Sign up with GitHub account

2. **Connect Repository**
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repo

3. **Configure**
   ```
   Name: pose-estimation-app
   Environment: Python 3.11
   Build Command: pip install -r requirements.txt && python download_models.py
   Start Command: gunicorn -w 1 -b 0.0.0.0:$PORT app:app
   ```

4. **Environment Variables**
   - Add PYTHON_VERSION=3.11
   - Add PORT=5000

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes
   - Get your live URL!

### Pros:
- ✅ Free tier
- ✅ GitHub integration
- ✅ Auto-deploy on push
- ✅ Easy to use
- ✅ No credit card initially

### Cons:
- ❌ Model download may timeout (solution: pre-download)
- ❌ Free tier has limitations

---

## 🟠 Option 2: Railway.app (MODERN & EASY)

**Time**: 15 minutes
**Cost**: $5/month free credits
**Difficulty**: ⭐ (Very Easy)

### Steps:

1. **Sign Up**
   - Go to https://railway.app
   - Click "Login with GitHub"
   - Authorize Railway

2. **Create Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - Railway auto-detects Python
   - Auto-generates start command
   - Sets PORT automatically

4. **Add Environment**
   - Go to Variables
   - Add any custom variables if needed

5. **Deploy**
   - Automatic on push to GitHub
   - Check "Deployments" tab
   - Click generated URL

### Pros:
- ✅ Modern interface
- ✅ Easy configuration
- ✅ Free credits ($5/month)
- ✅ GitHub auto-deploy
- ✅ Good documentation

### Cons:
- ❌ Not completely free
- ❌ Credits run out monthly

---

## 🔵 Option 3: Heroku (CLASSIC)

**Time**: 20 minutes
**Cost**: Free tier discontinued
**Difficulty**: ⭐⭐ (Easy)

### Steps:

1. **Install Heroku CLI**
   - Download from https://devcenter.heroku.com/articles/heroku-cli
   - Verify: `heroku --version`

2. **Login**
   ```bash
   heroku login
   # Opens browser, authenticate
   ```

3. **Create App**
   ```bash
   heroku create your-app-name
   # Creates app and adds remote
   ```

4. **Configure buildpacks**
   ```bash
   # Usually auto-detected, but you can set:
   heroku buildpacks:set heroku/python
   ```

5. **Deploy**
   ```bash
   git push heroku main
   # Deploys and starts app
   ```

6. **Open App**
   ```bash
   heroku open
   # Opens your live app!
   ```

### Useful Commands:
```bash
heroku logs --tail              # View logs
heroku config:set KEY=VALUE     # Set environment variables
heroku apps:info                # App information
heroku ps:scale web=1           # Scale dynos
```

### Pros:
- ✅ Industry standard
- ✅ Reliable
- ✅ Good documentation
- ✅ CLI tools

### Cons:
- ❌ Free tier removed
- ❌ Paid service now
- ❌ More complex setup

---

## 🟡 Option 4: PythonAnywhere (SIMPLEST FOR BEGINNERS)

**Time**: 15 minutes
**Cost**: Free tier available
**Difficulty**: ⭐ (Very Easy)

### Steps:

1. **Sign Up**
   - Go to https://www.pythonanywhere.com
   - Sign up (free account available)

2. **Upload Files**
   - Go to "Files"
   - Create folder: `pose_estimation_app`
   - Upload all your files:
     - app.py
     - requirements.txt
     - templates/
     - models/ (or download there)
     - static/

3. **Create Virtual Environment**
   - Open "Web" tab
   - Click "Add a new web app"
   - Select "Python 3.10"
   - Select "Flask"
   - Confirm

4. **Configure WSGI**
   - Open WSGI file
   - Replace with:
   ```python
   import sys
   path = '/home/yourusername/pose_estimation_app'
   sys.path.insert(0, path)
   
   from app import app as application
   ```

5. **Install Packages**
   - Open Bash console
   - Navigate to your folder
   - Run: `pip install -r requirements.txt`

6. **Download Models**
   - In Bash: `python download_models.py`
   - Choose to download when prompted

7. **Reload App**
   - Go to Web tab
   - Click "Reload" button
   - Visit your URL!

### Pros:
- ✅ Free tier available
- ✅ Simple file upload
- ✅ Built-in console
- ✅ Good for learning
- ✅ No command line needed

### Cons:
- ❌ Limited free resources
- ❌ Slower than others
- ❌ Manual configuration

---

## 🟣 Option 5: AWS EC2 (FOR ADVANCED USERS)

**Time**: 45 minutes
**Cost**: Free tier available (12 months)
**Difficulty**: ⭐⭐⭐ (Advanced)

### Quick Setup:

1. **Create EC2 Instance**
   - Ubuntu 20.04 LTS
   - t2.micro (free tier eligible)
   - Configure security groups (allow 80, 443, 5000)

2. **SSH into Server**
   ```bash
   ssh -i key.pem ec2-user@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv git nginx
   ```

4. **Clone Repository**
   ```bash
   git clone your-repo-url
   cd pose_estimation_app
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 1 -b 127.0.0.1:5000 app:app
   ```

6. **Setup Nginx Reverse Proxy**
   - Configure nginx to forward requests to Gunicorn
   - Enable SSL with Let's Encrypt

7. **Use Systemd**
   - Create service file for auto-start
   - Enable with systemctl

---

## 🟤 Option 6: Google Cloud Run (SERVERLESS)

**Time**: 20 minutes
**Cost**: Free tier available
**Difficulty**: ⭐⭐ (Moderate)

### Steps:

1. **Setup**
   - Create Google Cloud account
   - Enable Cloud Run API

2. **Containerize App**
   ```dockerfile
   FROM python:3.11
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "app:app"]
   ```

3. **Deploy**
   - Upload Docker image
   - Or connect GitHub for auto-deploy

4. **Configure**
   - Set memory to 2GB
   - Set timeout to 3600s

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All files included:
  - [ ] app.py
  - [ ] requirements.txt
  - [ ] templates/index.html
  - [ ] templates/result.html
  - [ ] Procfile (if using Heroku)
  - [ ] runtime.txt

- [ ] Code ready:
  - [ ] No debug=True in production
  - [ ] No hardcoded paths
  - [ ] Error handling complete
  - [ ] All imports working

- [ ] Models:
  - [ ] Models downloaded locally (optional pre-download)
  - [ ] Models folder created on server
  - [ ] File paths correct in app.py

- [ ] Testing:
  - [ ] Works locally on different machine
  - [ ] Tested with multiple images
  - [ ] No console errors
  - [ ] All features working

---

## 🔧 Common Deployment Issues

### Issue: Models Not Download on Server

**Solution**: Pre-download models locally and commit to Git:
```bash
# Locally (do NOT commit full models, too large)
# Instead, add download_models.py to build process
# Or manually download and store on server
```

### Issue: Out of Memory During Deployment

**Solution**: Use MPII model only initially
```python
# In app.py, comment out COCO for now
# COCO_WEIGHTS = None  # Disable COCO
```

### Issue: Static Files Not Loading

**Solution**: Ensure static folder is in root directory
```
project/
├── app.py
├── static/
│   └── uploads/
└── templates/
```

### Issue: Timeout During Processing

**Solution**: Increase timeout limit in deployment
- Render: Set to 3600 seconds
- Heroku: Set in Procfile
- Railway: Configure timeouts

### Issue: Port Already in Use

**Solution**: Use environment variable
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

---

## 🚀 After Deployment

### Monitor Your App:
1. Check logs regularly
2. Test all features
3. Monitor performance
4. Set up error alerts (optional)

### Maintain Your App:
1. Keep dependencies updated
2. Monitor disk space
3. Clean up old files
4. Back up data if needed

### Improve Your App:
1. Add analytics
2. Optimize images
3. Add caching
4. Monitor errors

---

## 📊 Deployment Comparison

| Platform | Ease | Cost | Speed | Setup Time | Free Tier |
|----------|------|------|-------|-----------|-----------|
| Render | ⭐⭐⭐⭐⭐ | $ | Fast | 10 min | Yes |
| Railway | ⭐⭐⭐⭐⭐ | $ | Very Fast | 15 min | $5/mo |
| Heroku | ⭐⭐⭐⭐ | $$ | Fast | 20 min | No |
| PythonAnywhere | ⭐⭐⭐⭐⭐ | $ | Slow | 15 min | Yes |
| AWS | ⭐⭐ | $-$$ | Fast | 45 min | 12mo |
| Google Cloud | ⭐⭐⭐ | $ | Very Fast | 20 min | Yes |

---

## 💡 Recommendation for Beginners

**Use Render.com** because:
1. ✅ Completely free tier
2. ✅ GitHub integration (1-click deploy)
3. ✅ Auto-deploys on push
4. ✅ Modern interface
5. ✅ Good documentation
6. ✅ Easy to understand

---

## 🎯 Getting Your Live URL

After deploying, you'll get a URL like:
- Render: `https://pose-estimation-app.onrender.com`
- Railway: `https://yourapp-production.up.railway.app`
- Heroku: `https://yourappname.herokuapp.com`
- PythonAnywhere: `https://username.pythonanywhere.com`

**Share this URL for your assignment submission!**

---

## 🔐 Security Reminders

For production:
- [ ] Remove debug mode
- [ ] Set SECRET_KEY
- [ ] Enable HTTPS (free with Let's Encrypt)
- [ ] Validate all inputs
- [ ] Set proper CORS headers
- [ ] Monitor logs for errors
- [ ] Update dependencies regularly
- [ ] Use environment variables for secrets

---

## 📞 Deployment Help

### If Deployment Fails:
1. Check the logs
2. Verify all files uploaded
3. Check requirements.txt syntax
4. Ensure Python version compatible
5. Try re-deploying

### Common Log Errors:
- `ModuleNotFoundError` → Missing package in requirements.txt
- `No such file` → File not uploaded or path wrong
- `Memory exceeded` → App too large for free tier
- `Connection refused` → Port configuration issue

---

## ✅ Success Indicators

Deployment successful if:
- ✅ App loads in browser
- ✅ Upload page displays
- ✅ Can upload images
- ✅ Processing works
- ✅ Results display correctly
- ✅ No 500 errors

---

**Now pick your platform and deploy! 🚀**

Recommended for beginners: **Render.com**
