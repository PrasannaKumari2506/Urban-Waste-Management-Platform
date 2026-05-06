# Urban Waste Management & Recycling Coordination Platform

A comprehensive Django web application connecting households with verified recyclers to promote sustainable waste management practices, featuring AI-powered waste classification.

## 🎯 Overview

This platform addresses urban waste management challenges by:
- Connecting households with verified recyclers through an intelligent matching system
- Providing AI-powered waste classification for instant recyclability analysis
- Offering comprehensive waste segregation education
- Enabling scheduled waste pickups with real-time tracking
- Facilitating community-driven recycling with rating and review systems

## 🛠️ Tech Stack

- **Backend:** Django 5.2.12
- **Frontend:** Django Templates + Tailwind CSS (CDN)
- **Database:** SQLite (development) / PostgreSQL (production-ready)
- **Authentication:** Email/Password (OAuth removed)
- **AI/ML:** NumPy + PIL for image classification
- **Styling:** Custom organic & earthy theme with responsive design

## 📋 Complete Feature Set

### 🏠 For Households

#### Core Features
- ✅ **Dashboard** - Overview of pickup stats, upcoming schedules, nearby recyclers
- ✅ **Request Waste Pickup** - Schedule pickups with date, time, waste type selection
- ✅ **Pickup History** - Track all past requests with status updates
- ✅ **Rate & Review** - Provide feedback on completed pickups (1-5 star system)
- ✅ **Educational Content** - Access articles, guides, and videos on waste management
- ✅ **Waste Segregation Guidelines** - Learn proper sorting for 6 waste categories

#### NEW: AI Waste Classifier 🤖
- ✅ **Image Upload** - Take photo or upload waste image
- ✅ **AI Classification** - Instant waste type identification
- ✅ **Recyclability Detection** - Determines if item is recyclable
- ✅ **Confidence Scoring** - Shows prediction accuracy percentage
- ✅ **Smart Recommendations** - Category-specific disposal instructions
- ✅ **Direct Pickup Request** - Quick link to schedule pickup for classified waste

### ♻️ For Recyclers (ENHANCED)

#### Dashboard & Stats
- ✅ **Enhanced Dashboard** - At-a-glance metrics with 4-card stat display
  - Total completed pickups
  - Pending accepted pickups  
  - Average rating with star visual
  - Availability status toggle
- ✅ **Quick Actions** - Direct links to all major features

#### Pickup Management (NEW)
- ✅ **Pickup Requests Page** - Dedicated page for all available requests
  - **Advanced Filters:**
    - By waste category (Plastic, E-Waste, Organic, Paper, Glass, Metal)
    - By date range (from/to)
    - By service area (city/location search)
  - Sort by pickup date and time
  - Visual category indicators
  
- ✅ **Pickup Detail Page** - Full request information before accepting
  - Household contact details
  - Waste description and photos
  - Exact pickup location with address
  - Scheduled date and time
  - Waste category with color coding
  - Accept/Decline actions

#### History & Performance (NEW)
- ✅ **Pickup History Page** - Complete record of all past pickups
  - **Filters:**
    - By status (Accepted, Completed, Cancelled)
    - By waste category
    - By date range
  - Shows household name, review received, and earnings
  - Export-ready data presentation

- ✅ **Reviews Page** - Dedicated reviews management
  - All reviews from households in one place
  - Average rating calculation with distribution
  - Rating breakdown (5-star, 4-star, etc.)
  - Individual review cards with household name, date, and comments
  - Filter and search capabilities

#### Notifications System (NEW)
- ✅ **Notifications Page** - Real-time updates
  - **Notification Types:**
    - New pickup requests in service area
    - Household cancelled pickup
    - New review received
    - Account approval status
  - Unread badge counter in sidebar
  - Mark as read functionality
  - Timestamp for each notification
  - Direct links to related pickups

#### Analytics & Earnings (NEW)
- ✅ **Stats & Earnings Page** - Performance dashboard
  - Total completed pickups (lifetime)
  - This month's pickups count
  - Pickups by waste category (chart-ready data)
  - Total earnings tracker
  - Recent activity log (last 10 pickups)
  - Monthly performance trends

#### Education & Guidelines (NEW)
- ✅ **Recycling Guidelines Page** - Professional resources
  - Detailed handling instructions per waste category
  - Hazardous waste safety protocols
  - Electronics recycling best practices
  - Organic waste composting guidelines
  - Compliance and regulatory information
  - Safety tips for collectors
  - Sorting techniques and efficiency tips

#### Profile Management
- ✅ **Edit Profile** - Comprehensive profile customization
  - Bio and description
  - Service areas (comma-separated)
  - Vehicle type
  - Availability toggle
  - Contact information (phone, address, city)

### 👨‍💼 For Admins

- ✅ **Django Admin Panel** - Full administrative control
- ✅ **User Management** - View, edit, delete all users
- ✅ **Recycler Approval** - Approve/reject recycler registrations
- ✅ **Pickup Monitoring** - Track all requests system-wide
- ✅ **Content Management** - Add/edit educational articles and videos
- ✅ **Waste Categories** - Manage recyclable categories
- ✅ **Bulk Actions** - Approve multiple recyclers at once

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Windows Installation

1. **Install Python**
   - Download from https://python.org/downloads/
   - ✅ Check \"Add Python to PATH\" during installation

2. **Create Project Directory**
   ```cmd
   mkdir django-waste-app
   cd django-waste-app
   ```

3. **Create Virtual Environment**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```cmd
   pip install django==5.2.12
   pip install django-allauth
   pip install pillow
   pip install numpy
   pip install requests
   pip install python-decouple
   ```

5. **Create .env File**
   ```env
   SECRET_KEY=django-insecure-dev-key-change-in-production-12345
   DEBUG=True
   ALLOWED_HOSTS=*
   GOOGLE_MAPS_API_KEY=
   ```

6. **Run Migrations**
   ```cmd
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create Admin User**
   ```cmd
   python manage.py createsuperuser
   ```
   - Email: admin@ecowaste.com
   - Password: admin123 (or your choice)

8. **Load Sample Data (Optional)**
   ```cmd
   python manage.py shell
   ```
   Then paste seed data commands (see documentation)

9. **Start Server**
   ```cmd
   python manage.py runserver 8000
   ```

10. **Access Application**
    - Main site: http://localhost:8000/
    - Admin panel: http://localhost:8000/admin/
    - AI Classifier: http://localhost:8000/classifier/

## 👥 Test Accounts

### Pre-created Users

**Admin Account:**
- Email: `admin@ecowaste.com`
- Password: `admin123`
- Access: Full admin panel + all features

**Household User:**
- Email: `household@test.com`
- Password: `test123`
- Role: Household
- Access: Dashboard, pickup requests, classifier

**Recycler:**
- Email: `recycler@test.com`
- Password: `test123`
- Role: Recycler (Approved)
- Access: Full recycler dashboard with all new features

### Creating New Users

**Via Registration Form** (`/accounts/register/`):
1. Fill in: Name, Email, Password
2. Select Role: Household or Recycler
3. Click \"Create Account\"
4. **Note:** Recyclers need admin approval before accessing dashboard

## 📁 Project Structure

```
/app/
├── manage.py
├── db.sqlite3                      # SQLite database
├── .env                            # Environment variables
├── waste_platform/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                       # Authentication
│   ├── models.py                  # User, UserSession
│   ├── views.py                   # Login, register, logout
│   ├── urls.py
│   └── admin.py
├── households/                     # Household features
│   ├── models.py                  # WastePickupRequest
│   ├── views.py                   # Dashboard, pickup requests, history
│   ├── urls.py
│   └── admin.py
├── recyclers/                      # Recycler features (ENHANCED)
│   ├── models.py                  # RecyclerProfile, Review, Notifications
│   ├── views.py                   # All recycler views (10+ pages)
│   ├── urls.py
│   └── admin.py
├── core/                           # Shared functionality
│   ├── models.py                  # WasteCategory, EducationalContent
│   ├── ml_classifier.py           # AI waste classifier
│   ├── views.py                   # Home, classifier
│   ├── urls.py
│   └── admin.py
├── templates/                      # Django templates
│   ├── base.html
│   ├── core/
│   │   ├── home.html
│   │   └── waste_classifier.html
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   ├── households/
│   │   ├── dashboard.html
│   │   ├── request_pickup.html
│   │   ├── pickup_history.html
│   │   ├── add_review.html
│   │   └── educational_content.html
│   └── recyclers/                 # All recycler templates
│       ├── dashboard.html          # Enhanced with 4 stats
│       ├── pickup_requests.html    # NEW: All requests with filters
│       ├── pickup_detail.html      # NEW: Detailed request view
│       ├── pickup_history.html     # NEW: Complete history
│       ├── notifications.html      # NEW: Notification center
│       ├── reviews.html            # NEW: All reviews received
│       ├── earnings_stats.html     # NEW: Stats & analytics
│       ├── recycling_guidelines.html # NEW: Educational content
│       ├── edit_profile.html
│       └── pending_approval.html
├── static/                         # Static assets
└── media/                          # User uploads
```

## 🗄️ Database Models

### User (Custom Auth Model)
```python
- email, name, role (household/recycler/admin)
- location fields (address, city, pincode, lat/lng)
- profile_picture, phone
- date_joined, is_active, is_staff
```

### RecyclerProfile (UPDATED)
```python
- user (OneToOne with User)
- is_approved, is_available
- bio, service_areas, vehicle_type
- total_earnings (NEW)
- created_at
```

### WastePickupRequest
```python
- household, recycler (optional)
- waste_category, description
- pickup_date, pickup_time
- status (pending/accepted/completed/cancelled)
- address, latitude, longitude
- created_at, updated_at
```

### Review
```python
- recycler, household, pickup_request
- rating (1-5 stars)
- comment, created_at
```

### RecyclerNotification (NEW)
```python
- recycler, notification_type
- title, message
- pickup_request (optional reference)
- is_read, created_at
```

### WasteCategory
```python
- name, description, icon, color
- Categories: Plastic, E-Waste, Organic, Paper, Glass, Metal
```

### EducationalContent
```python
- title, content_type (article/video/guide)
- description, content, video_url, thumbnail
- is_published, created_at, updated_at
```

## 🌐 URL Routing

### Public URLs
```
/                              → Home page with hero section
/accounts/login/               → Login (email/password only)
/accounts/register/            → Registration with role selection
/accounts/logout/              → Logout
/classifier/                   → AI Waste Classifier (public access)
```

### Household URLs (Auth Required)
```
/dashboard/                    → Household dashboard
/dashboard/pickup/request/     → Request pickup form
/dashboard/pickup/history/     → Pickup history
/dashboard/pickup/<id>/review/ → Add review form
/dashboard/educational/        → Educational content library
```

### Recycler URLs (Auth + Approval Required)
```
/recycler/dashboard/           → Enhanced recycler dashboard
/recycler/pickup-requests/     → All available requests (NEW)
/recycler/pickup/<id>/         → Pickup detail view (NEW)
/recycler/pickup/<id>/accept/  → Accept pickup
/recycler/pickup/<id>/complete/ → Mark as completed
/recycler/history/             → Complete pickup history (NEW)
/recycler/notifications/       → Notification center (NEW)
/recycler/reviews/             → All reviews received (NEW)
/recycler/earnings/            → Stats & earnings page (NEW)
/recycler/guidelines/          → Recycling guidelines (NEW)
/recycler/profile/edit/        → Edit profile
```

### Admin URLs
```
/admin/                        → Django admin panel
```

## 🎨 Design System

### Theme: Organic & Earthy
- **Primary:** Forest Green (#2C5530)
- **Background:** Sand (#F4F4F1)
- **Accent:** Earth (#D4A373)
- **Text:** Charcoal (#1A1A1A)
- **Danger:** #D9534F

### Typography
- **Headings:** Manrope (extrabold, bold)
- **Body:** DM Sans (regular, medium)
- **Style:** Generous spacing, clean hierarchy

### Components
- Rounded corners (rounded-lg, rounded-xl)
- Subtle shadows and borders
- Hover animations (-translate-y-1)
- Responsive toggle sidebar
- Data-testid attributes for testing

## 🧪 Testing Workflow

### Manual Testing Checklist

**Household Features:**
- [ ] Register as household user
- [ ] Login with email/password
- [ ] View dashboard with stats
- [ ] Upload image to AI classifier
- [ ] Get classification result
- [ ] Request pickup from classifier result
- [ ] Request pickup manually
- [ ] View pickup history
- [ ] Rate completed pickup
- [ ] Browse educational content

**Recycler Features (NEW):**
- [ ] Register as recycler
- [ ] Admin approves recycler
- [ ] Login and view enhanced dashboard (4 stats)
- [ ] Browse all pickup requests with filters
- [ ] Filter by category, date, area
- [ ] View detailed pickup information
- [ ] Accept pickup request
- [ ] Mark pickup as completed
- [ ] View pickup history with filters
- [ ] Check notifications page
- [ ] View all reviews received
- [ ] Check stats & earnings page
- [ ] Read recycling guidelines
- [ ] Update profile and availability

**Admin Features:**
- [ ] Login to admin panel
- [ ] Approve pending recycler
- [ ] View all users
- [ ] Monitor pickup requests
- [ ] Add educational content
- [ ] Manage waste categories
- [ ] Bulk approve recyclers

**AI Classifier:**
- [ ] Access from home page button
- [ ] Upload various waste images
- [ ] Verify classification accuracy
- [ ] Check confidence scores
- [ ] Read recommendations
- [ ] Test with different waste types

## 🔐 Authentication

**Method:** Email + Password (OAuth removed as per user request)

**Flow:**
1. User enters email and password
2. Django authenticates and validates
3. Creates session
4. Redirects based on role:
   - Household → `/dashboard/`
   - Recycler → `/recycler/dashboard/` (if approved)
   - Admin → `/admin/`

## 🤖 AI Waste Classifier

**Technology:** Custom ML algorithm using NumPy + PIL

**Supported Waste Types:**
- ♻️ Plastic bottles & bags
- ♻️ Glass bottles
- ♻️ Aluminum cans
- ♻️ Cardboard & paper
- ♻️ Electronics & batteries
- ❌ Food waste (organic/compostable)
- ❌ Styrofoam (non-recyclable)

**Features:**
- Color-based image analysis
- Confidence scoring (percentage)
- Category detection
- Recycling recommendations
- Mobile-friendly interface

**Enhancement Options:**
- Train with real waste dataset
- Use pre-trained CNN (ResNet, MobileNet)
- Integrate TensorFlow/PyTorch
- Add more waste categories

## 🌐 Deployment (For Production)

### Pre-Deployment Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Migrate to PostgreSQL (from SQLite)
- [ ] Set up static file serving (WhiteNoise/CDN)
- [ ] Configure secure cookies (HTTPS)
- [ ] Generate strong `SECRET_KEY`
- [ ] Set up backup strategy
- [ ] Configure logging

### Environment Variables (Production)
```env
SECRET_KEY=strong-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:port/dbname
GOOGLE_MAPS_API_KEY=your-maps-api-key
```

### Deployment Platforms
- **Heroku** - Easy Django deployment
- **PythonAnywhere** - Simple hosting
- **DigitalOcean** - Full control
- **AWS/GCP/Azure** - Enterprise scale

**Note:** Current SQLite setup not suitable for Emergent cloud (requires MongoDB). Use for local development or deploy to Django-friendly platforms.

## 📦 Dependencies

**Core:**
- Django 5.2.12
- django-allauth 65.15.0
- python-decouple 3.8

**ML/Image Processing:**
- Pillow 12.1.1
- NumPy 2.4.3

**Utilities:**
- requests 2.32.5

## 🛣️ Roadmap / Future Enhancements

### Planned Features
- [ ] REST API using Django REST Framework
- [ ] Mobile app (React Native / Flutter)
- [ ] Real-time notifications (Django Channels + WebSocket)
- [ ] Advanced Google Maps with route optimization
- [ ] Payment integration (Stripe/PayPal) for earnings
- [ ] Gamification (badges, leaderboards)
- [ ] Multi-language support (i18n)
- [ ] SMS notifications (Twilio)
- [ ] Email notifications (SendGrid)
- [ ] Analytics dashboard for admins
- [ ] Data export (CSV/PDF reports)
- [ ] Schedule recurring pickups
- [ ] Bulk pickup requests

### AI Classifier Enhancements
- [ ] Train custom CNN on waste dataset
- [ ] Support for more waste categories
- [ ] Real-time classification via webcam
- [ ] Batch image processing
- [ ] Integration with pickup requests

## 📝 Important Notes

- **Port:** Default Django runs on 8000, not 3000 (no conflict on Windows)
- **Database:** SQLite for local development, migrate to PostgreSQL for production
- **Authentication:** Pure email/password, no OAuth/Google login
- **AI Classifier:** Color-based algorithm, enhance with CNN for production
- **Recycler Approval:** Manual via Django admin, can be automated
- **Notifications:** In-app only, can add email/SMS
- **Session Expiry:** Django default (2 weeks), configurable

## 🤝 Contributing

For production enhancements:
1. Add comprehensive test coverage (pytest-django)
2. Implement proper error handling and logging
3. Add API rate limiting
4. Set up monitoring (Sentry, New Relic)
5. Implement email notifications
6. Add data validation and sanitization
7. Create API documentation (Swagger/OpenAPI)

## 📄 License

This project is provided as-is for educational/demonstration purposes.

---

## 🎉 What's New in This Version

### Major Updates:
1. ✨ **AI Waste Classifier** - ML-powered image classification
2. 🚀 **Enhanced Recycler Dashboard** - 10+ new pages and features
3. 📊 **Advanced Analytics** - Stats, earnings, performance tracking
4. 🔔 **Notification System** - Real-time updates for recyclers
5. ⭐ **Reviews Management** - Dedicated page for ratings
6. 📚 **Recycling Guidelines** - Professional educational content
7. 🎯 **Advanced Filters** - Search and filter across all pages
8. 🔄 **Complete History** - Comprehensive pickup tracking

### Total Features:
- **25+ Pages** across all user roles
- **8 New Recycler Pages** (mirroring household features + extras)
- **AI-Powered Classification** with instant results
- **Full CRUD Operations** for all entities
- **Role-Based Access Control** with 3 user types
- **Responsive Design** with toggle sidebar
- **Professional UI** following design guidelines

---

**Built with Django & Tailwind CSS | AI-Powered Waste Classification | Community-Driven Sustainability**

**Version:** 2.0 - Enhanced Recycler Dashboard Edition
**Last Updated:** 2026
