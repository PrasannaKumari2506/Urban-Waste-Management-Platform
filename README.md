# Urban Waste Management & Recycling Coordination Platform

A comprehensive Django web application connecting households with verified recyclers to promote sustainable waste management practices, featuring AI-powered waste classification.

## 🎯 Overview

This platform addresses urban waste management challenges by:
- Connecting households with verified recyclers through an intelligent matching system
- Providing AI-powered waste classification for instant recyclability analysis
- Offering comprehensive waste segregation education
- Enabling scheduled waste pickups with real-time tracking
- Facilitating community-driven recycling with rating and review systems


# 🛠️ Tech Stack

- **Backend:** Django 5.2
- **Frontend:** Django Templates + Tailwind CSS
- **Database:** SQLite3
- **Machine Learning:** PyTorch + MobileNetV2
- **Image Processing:** Pillow + NumPy
- **Authentication:** Django Authentication System

---

# ✨ Features

## 🏠 Household Features

- User registration and login
- Household dashboard
- Request waste pickups
- View pickup history
- Educational waste management content
- AI waste classification from uploaded images

---

## ♻️ Recycler Features

- Recycler dashboard
- Pickup request management
- Accept and complete pickups
- Manage availability
- Recycling guidelines

---

## 🤖 AI Waste Classification

### Features

- Upload waste images
- CNN-based image classification
- Recyclability prediction
- Confidence score display
- Waste category detection
- Disposal recommendations

### Supported Categories

- Cardboard
- Glass
- Metal
- Paper
- Plastic
- Trash

---

# 🧠 Model Training

The waste classification model was trained using a garbage image dataset from Kaggle with transfer learning based on MobileNetV2.

## Model Details

- Framework: PyTorch
- Architecture: MobileNetV2
- Technique: Transfer Learning
- Dataset Source: [Kaggle Garbage Classification Dataset](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification)

## Training Features

- Data augmentation
- Fine-tuning pretrained layers
- Cosine annealing learning rate scheduler
- Dropout regularization
- Train/Validation/Test split

## Performance

- Validation Accuracy: ~96%
- Lightweight model for faster inference
- Optimized for deployment

---

# 📁 Project Structure

```text
project/
│
├── accounts/
├── households/
├── recyclers/
├── core/
│   ├── ml_classifier.py
│   ├── garbage_classifier.pth
│   └── train_model.py
│
├── templates/
├── static/
├── media/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── Procfile
└── runtime.txt
```

---

# 🚀 Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/PrasannaKumari2506/Urban-Waste-Management-Platform
cd project-folder
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install django==5.2.12
pip install pillow
pip install numpy
pip install torch torchvision tqdm
pip install requests
pip install python-decouple
pip install gunicorn whitenoise psycopg2-binary
```

---

## 4. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 6. Start Development Server

```bash
python manage.py runserver
```

---

## 7. Open Browser

```text
http://127.0.0.1:8000/
```

Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

---

# 🧪 AI Model Training

## Dataset

Download dataset from Kaggle:

```text
https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification
```

Dataset structure:

```text
Garbage classification/
    cardboard/
    glass/
    metal/
    paper/
    plastic/
    trash/
```

---

## Train Model

Run:

```bash
python train_model.py --data_dir "path/to/Garbage classification"
```

---

## Output

Trained model file:

```text
core/garbage_classifier.pth
```

---

# 🗄️ Database Models

## User

- Email
- Password
- Role
- Address
- Phone Number

---

## WastePickupRequest

- Household
- Recycler
- Waste Category
- Pickup Date
- Status

---

## RecyclerProfile

- Service Areas
- Vehicle Type
- Availability
- Earnings

---

## Review

- Rating
- Comment
- Pickup Reference

---

# 🌐 URL Routes

## Public Routes

```text
/
accounts/login/
accounts/register/
classifier/
```

---

## Household Routes

```text
/dashboard/
/dashboard/pickup/request/
/dashboard/pickup/history/
```

---

## Recycler Routes

```text
/recycler/dashboard/
/recycler/pickup-requests/
/recycler/history/
/recycler/reviews/
```

---

# 🎨 UI Design

## Theme

- Forest Green
- Earth Brown
- Sand Background
- Responsive Layout

## Features

- Mobile responsive
- Sidebar navigation
- Modern card-based UI
- Tailwind CSS styling

---

# 🔐 Authentication

Authentication is implemented using Django’s built-in authentication system with role-based access control.

## Roles

- Household
- Recycler
- Admin

---

# 📦 Dependencies

## Core

- Django
- python-decouple

## Machine Learning

- PyTorch
- TorchVision
- NumPy
- Pillow

## Utilities

- requests
- tqdm

---

# 🚀 Deployment

This project can be deployed using:

- Railway
- Render
- PythonAnywhere
- VPS Servers

---

# 🚂 Railway Deployment

## Create Procfile

```text
web: gunicorn waste_platform.wsgi
```

---

## Create runtime.txt

```text
python-3.11.9
```

---

## Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## Push to GitHub

```bash
git init
git add .
git commit -m "Initial Commit"
git branch -M main
git remote add origin <repo-url>
git push -u origin main
```

---

## Deploy Steps

1. Login to Railway
2. Create New Project
3. Select Deploy from GitHub Repo
4. Choose your repository
5. Add environment variables
6. Deploy application

---

## Environment Variables

```env
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=*
```

---

# 📈 Future Enhancements

## Planned Features

- [ ] REST API using Django REST Framework
- [ ] Mobile application support
- [ ] Real-time notifications using WebSockets
- [ ] Advanced map-based pickup tracking
- [ ] Payment integration for recycler earnings
- [ ] Gamification and reward system
- [ ] Multi-language support
- [ ] SMS and Email notifications
- [ ] Admin analytics dashboard
- [ ] CSV/PDF report generation
- [ ] Recurring pickup scheduling
- [ ] Bulk pickup request handling

---

## AI Classifier Enhancements

- [ ] Improve model accuracy with larger datasets
- [ ] Add support for more waste categories
- [ ] Real-time webcam-based classification
- [ ] Batch image prediction
- [ ] Faster inference optimization
- [ ] Cloud-based model deployment
- [ ] Integration with live pickup recommendations

---

# 📝 Important Notes

- SQLite3 is used for development
- PostgreSQL recommended for production deployment
- CNN model trained using transfer learning
- MobileNetV2 used for waste image classification
- Lightweight model optimized for deployment
- Recycler approval managed through Django admin

---

# 📄 License

This project is developed for educational and academic purposes.

---

# 👨‍💻 Developed Using

- Django
- PyTorch
- MobileNetV2
- Machine Learning
- Tailwind CSS
- SQLite3

---

# 🌱 Project Goal

To promote sustainable waste management and smart recycling practices using Artificial Intelligence and community-driven waste coordination systems.

---

# 🚀 Version

**Version:** 2.0  
**Last Updated:** 2026
