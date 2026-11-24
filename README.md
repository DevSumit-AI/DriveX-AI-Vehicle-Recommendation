# 🚘 DriveX – AI-Powered Vehicle Recommendation & Rental System

<p align="center">
  A premium vehicle rental platform that helps users discover, compare, and book vehicles through an intelligent recommendation system.
</p>

## 📌 About the Project

**DriveX** is a web-based vehicle rental and recommendation platform developed as a BCA (AI & Data Science) 5th Semester Mini Project.

The platform provides users with an easy way to explore available vehicles, find suitable options based on their preferences, and manage their bookings.

It incorporates a rule-based intelligent recommendation system that evaluates user preferences such as budget, passenger capacity, and travel requirements to suggest suitable vehicles.

## ✨ Key Features

- 🔐 **User Authentication:** User registration and login functionality.
- 🚗 **Vehicle Catalogue:** Browse available vehicles with their details.
- 🤖 **AI-Based Recommendation:** Intelligent vehicle suggestions using preference-based weighted scoring.
- 📅 **Vehicle Booking:** Book vehicles through the booking interface.
- 📋 **Booking Management:** View and manage booking information.
- 🎨 **Premium UI:** Modern, responsive automotive-inspired interface.
- 🗄️ **Database Integration:** MySQL database for storing application data.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| HTML5 | Website structure |
| CSS3 | Styling and responsive design |
| JavaScript | Frontend interactivity |
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | Database management |
| Jinja2 | Dynamic HTML templating |

## 🧠 Recommendation System

DriveX implements a rule-based intelligent recommendation approach.

The system considers user preferences such as:

- Budget
- Passenger capacity
- Travel environment
- Vehicle suitability

It evaluates these preferences using weighted scoring and recommends vehicles that best match the user's requirements.

**Note:** The current recommendation engine is rule-based and does not use a separately trained machine-learning model.

## 📂 Project Structure

```text
DriveX/
│
├── app.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── vehicles.html
│   └── booking.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── database/
│
├── requirements.txt
├── .gitignore
└── README.md
```

*The structure above illustrates the main project components. Actual filenames and folders may vary.*

## ⚙️ Installation & Setup

Follow these steps to run DriveX locally.

### 1. Clone the repository

```bash
git clone https://github.com/DevSumit-AI/DriveX-AI-Vehicle-Recommendation.git
```

### 2. Navigate to the project directory

```bash
cd DriveX-AI-Vehicle-Recommendation
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure MySQL

- Install and start MySQL Server.
- Create the required project database.
- Import the project's SQL database file, if provided.
- Configure the database connection details in the Flask application.
- Keep database credentials private and never commit them to GitHub.

### 6. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```


## 🚀 Future Scope

- Integration of machine-learning-based recommendation models.
- Online payment gateway integration.
- Real-time vehicle availability tracking.
- Advanced filtering and vehicle comparison.
- Admin dashboard for fleet management.
- User reviews and ratings.

## 🎓 Academic Project

**Project Name:** DriveX – AI-Based Vehicle Recommendation & Rental System

**Course:** Bachelor of Computer Applications (BCA)

**Specialization:** Artificial Intelligence & Data Science

**Semester:** 5th Semester

## 👨‍💻 Developer

**Sumit Prajapati**

GitHub: [@DevSumit-AI](https://github.com/DevSumit-AI)

---

⭐ If you find this project interesting, consider giving the repository a star!

**DriveX – Smarter Recommendations. Better Journeys.**