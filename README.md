# 🌍 Socio+

**Socio+** is a social volunteering platform that bridges the gap between passionate volunteers and organizations in need. It enables volunteers to discover opportunities, apply seamlessly, and track their contributions, while organizations can post opportunities and manage applications effectively. Built with **Flask**, **SQLAlchemy**, and **Bootstrap**, Socio+ is lightweight, beginner-friendly, and deployment-ready.

---

## 🚀 Features

* 🔐 **User Authentication** (Volunteers & Organizations)
* 🏢 **Role-based Dashboards** (Volunteer dashboard, Organization dashboard)
* 📌 **Opportunity Management** (create, view, and apply to volunteering opportunities)
* ✅ **Application Tracking** (accept/reject volunteer applications)
* 📊 **Database Integration** using SQLAlchemy ORM
* 🎨 **Responsive UI** powered by Bootstrap
* 🔐 **Security Features** (password hashing, CSRF protection, session management)
* 🌐 **Deployment-ready** for platforms like **Render** or **Heroku**

---

## 🛠️ Tech Stack

**Frontend:** HTML, CSS, Bootstrap, Jinja2 Templates

**Backend:** Flask (Python)

**Database:** SQLite (local) / MySQL (production) with SQLAlchemy ORM

**Authentication:** Flask-Login & Flask-WTF

**Deployment:** Render (Free Tier)

**Other Tools:** Git, GitHub, dotenv

---

## 📁 Project Structure

```
socioplus/
│
├── app.py                       # Main application entry point
├── models.py                    # Database models
├── forms.py                     # WTForms for input validation
├── config.py                    # Config & environment setup
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
│
├── static/
│   └── css/
│       └── style.css            # Custom styles
│
└── templates/
    ├── base.html                # Layout template
    ├── index.html               # Homepage
    ├── login.html               # Login page
    ├── register.html            # Registration page
    ├── opportunities.html       # Browse opportunities
    ├── opportunity_detail.html  # Single opportunity page
    ├── volunteer_dashboard.html # Volunteer dashboard
    ├── org_dashboard.html       # Organization dashboard
    └── create_opportunity.html  # Create opportunity page
```

---

## ⚡ Quick Start

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/socioplus.git
cd socioplus
```

### 2️⃣ Setup Environment

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file:

```
SECRET_KEY=dev-secret-key-123
DATABASE_URL=sqlite:///socioplus.db
```

### 4️⃣ Initialize Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 5️⃣ Run the Application

```bash
python app.py
```

Visit: 👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Testing Workflow

1. Register as **Organization** → post new opportunities.
2. Register as **Volunteer** → browse opportunities & apply.
3. Organization reviews & accepts/rejects applications.

---

## 🌐 Deployment

### Render Deployment Steps:

1. Push code to GitHub.
2. Connect repository to [Render](https://render.com/).
3. Add environment variables (`SECRET_KEY`, `DATABASE_URL`).
4. Add `Procfile` with:

   ```
   web: gunicorn app:app
   ```
5. Deploy 🚀

---

## 🔐 Security Features

* Password hashing (Werkzeug)
* CSRF protection (Flask-WTF)
* Session management (Flask-Login)
* ORM-based queries (SQLAlchemy)
* Jinja2 auto-escaping

---

## ✨ Future Improvements

* 🔍 Search & Filter opportunities
* 📩 Email notifications
* 👤 User profile pages
* 📷 Image uploads for opportunities
* 💬 Real-time chat

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork and submit PRs.

---

## 👨‍💻 Author

**Gautham Ratiraju**

📧 [Email](gauthamrs19@gmail.com)

🔗 [Linkedin](www.linkedin.com/in/gauthamratiraju)
