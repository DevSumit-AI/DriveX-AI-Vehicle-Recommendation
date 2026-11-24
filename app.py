
import os
import re
import shutil
from datetime import datetime, date

from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# ==========================================
# FLASK CONFIGURATION
# ==========================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "vehicle_secret_change_this_before_deployment"
)


# Database configuration
database_url = os.environ.get("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://", "postgresql://", 1
        )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ==========================================
# USER MODEL
# ==========================================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


# ==========================================
# BOOKING MODEL
# Existing columns preserved
# ==========================================

class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))
    vehicle = db.Column(db.String(100))

    # Existing date fields
    pickup = db.Column(db.String(100))
    dropoff = db.Column(db.String(100))

    # Customer information
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))

    # Identity information
    aadhaar_last4 = db.Column(db.String(4))
    driving_license = db.Column(db.String(30))

    # Travel information
    pickup_location = db.Column(db.String(200))
    destination = db.Column(db.String(200))

    pickup_time = db.Column(db.String(10))
    dropoff_time = db.Column(db.String(10))

    passengers = db.Column(db.Integer)
    trip_purpose = db.Column(db.String(50))

    # Additional information
    emergency_contact = db.Column(db.String(15))
    special_requests = db.Column(db.String(500))


# ==========================================
# SAFE DATABASE MIGRATION
# ==========================================

def migrate_database():

    database_path = os.path.join(
        app.instance_path,
        "database.db"
    )

    os.makedirs(app.instance_path, exist_ok=True)

    # New columns and their SQLite data types

    new_columns = {
        "full_name": "VARCHAR(100)",
        "phone": "VARCHAR(15)",
        "email": "VARCHAR(120)",
        "aadhaar_last4": "VARCHAR(4)",
        "driving_license": "VARCHAR(30)",
        "pickup_location": "VARCHAR(200)",
        "destination": "VARCHAR(200)",
        "pickup_time": "VARCHAR(10)",
        "dropoff_time": "VARCHAR(10)",
        "passengers": "INTEGER",
        "trip_purpose": "VARCHAR(50)",
        "emergency_contact": "VARCHAR(15)",
        "special_requests": "VARCHAR(500)"
    }

    # Check existing columns

    existing_columns = {
        column["name"]
        for column in db.inspect(db.engine).get_columns("booking")
    }

    missing_columns = {
        name: data_type
        for name, data_type in new_columns.items()
        if name not in existing_columns
    }

    if not missing_columns:
        print("DriveX database is already up to date.")
        return

    # Backup existing database before migration

    if os.path.exists(database_path):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_path = os.path.join(
            app.instance_path,
            f"database_backup_{timestamp}.db"
        )

        shutil.copy2(database_path, backup_path)

        print("Database backup created:", backup_path)

    # Add missing columns without deleting existing records

    with db.engine.begin() as connection:

        for column_name, data_type in missing_columns.items():

            connection.exec_driver_sql(
                f'ALTER TABLE booking ADD COLUMN "{column_name}" {data_type}'
            )

            print("Added database column:", column_name)

    print("DriveX database migration completed successfully.")


# ==========================================
# VEHICLE DATABASE
# ==========================================

VEHICLES = [

    {
        "name": "Maruti Swift",
        "category": "Hatchback",
        "price": 2500,
        "seats": 5,
        "image": "swift.jpg",
        "description": "Compact and affordable for everyday city travel.",
        "suitability": {
            "city": 100,
            "hill": 65,
            "highway": 75,
            "eco": 85
        }
    },

    {
        "name": "Honda City",
        "category": "Premium Sedan",
        "price": 4000,
        "seats": 5,
        "image": "city.jpeg",
        "description": "Comfortable sedan for smooth highway journeys.",
        "suitability": {
            "city": 85,
            "hill": 65,
            "highway": 100,
            "eco": 70
        }
    },

    {
        "name": "Toyota Innova",
        "category": "Family MPV",
        "price": 6000,
        "seats": 7,
        "image": "innova.jpeg",
        "description": "Spacious vehicle for family and group travel.",
        "suitability": {
            "city": 70,
            "hill": 85,
            "highway": 100,
            "eco": 55
        }
    },

    {
        "name": "Mahindra Thar",
        "category": "Adventure SUV",
        "price": 5000,
        "seats": 4,
        "image": "thar.jpeg",
        "description": "Adventure-focused SUV for challenging road trips.",
        "suitability": {
            "city": 60,
            "hill": 100,
            "highway": 75,
            "eco": 50
        }
    },

    {
        "name": "Tata Nexon",
        "category": "Compact SUV",
        "price": 4500,
        "seats": 5,
        "image": "nexon.jpeg",
        "description": "Versatile SUV for mixed driving conditions.",
        "suitability": {
            "city": 85,
            "hill": 85,
            "highway": 85,
            "eco": 80
        }
    },

    {
        "name": "Hyundai Verna",
        "category": "Luxury Sedan",
        "price": 4500,
        "seats": 5,
        "image": "verna.jpeg",
        "description": "Stylish sedan offering comfort for long journeys.",
        "suitability": {
            "city": 85,
            "hill": 65,
            "highway": 100,
            "eco": 70
        }
    }

]


# ==========================================
# PYTHON RECOMMENDATION ENGINE
# ==========================================

def recommend_vehicles(environment, budget, passengers):

    recommendations = []

    for vehicle in VEHICLES:

        journey_score = vehicle["suitability"].get(
            environment, 50
        )

        price = vehicle["price"]

        budget_score = max(
            0,
            100 - max(0, (price - budget) / budget * 100)
        )

        passenger_score = (
            100 if passengers <= vehicle["seats"]
            else max(0, 100 - (
                (passengers - vehicle["seats"]) * 30
            ))
        )

        if environment == "hill":

            suitability_score = (
                100 if vehicle["category"] in [
                    "Adventure SUV", "Compact SUV"
                ] or vehicle["name"] == "Toyota Innova"
                else 70
            )

        elif environment == "city":

            suitability_score = (
                100 if vehicle["category"] == "Hatchback"
                else 85
            )

        elif environment == "highway":

            suitability_score = (
                100 if "Sedan" in vehicle["category"]
                or vehicle["name"] == "Toyota Innova"
                else 80
            )

        else:

            suitability_score = (
                100 if vehicle["name"] in [
                    "Maruti Swift", "Tata Nexon"
                ]
                else 75
            )

        final_score = (
            journey_score * 0.40
            + budget_score * 0.30
            + passenger_score * 0.20
            + suitability_score * 0.10
        )

        reasons = []

        if journey_score >= 85:
            reasons.append("Suitable for your journey")

        if price <= budget:
            reasons.append("Within your daily budget")
        else:
            reasons.append("Above your daily budget")

        if passengers <= vehicle["seats"]:
            reasons.append("Passenger capacity matches")
        else:
            reasons.append("Insufficient passenger capacity")

        if final_score >= 75:
            match_label = "Excellent Match"
        elif final_score >= 55:
            match_label = "Good Match"
        else:
            match_label = "Alternative Option"

        recommendations.append({

            **vehicle,

            "score": round(final_score),
            "match_label": match_label,
            "reasons": reasons,

            "within_budget": price <= budget,

            "capacity_ok": passengers <= vehicle["seats"]

        })

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return recommendations


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# SIGNUP
# ==========================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get(
            "username", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        )

        if not username or not email or not password:
            return "Please fill in all required fields.", 400

        if len(password) < 8:
            return "Password must contain at least 8 characters.", 400

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return "An account with this email already exists.", 409

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")


# ==========================================
# LOGIN
# Supports existing plaintext passwords
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user:

            password_valid = False

            try:

                password_valid = check_password_hash(
                    user.password, password
                )

            except (ValueError, TypeError):

                password_valid = False

            # Upgrade old plaintext password after successful login

            if not password_valid and user.password == password:

                password_valid = True

                user.password = generate_password_hash(password)

                db.session.commit()

            if password_valid:

                session.clear()

                session["user"] = user.username

                return redirect("/vehicles")

        return "Invalid Email or Password"

    return render_template("login.html")


# ==========================================
# AI RECOMMENDATION
# ==========================================

@app.route("/recommend", methods=["GET", "POST"])
def recommend():

    if "user" not in session:
        return redirect("/login")

    recommendations = []
    search_performed = False
    error = None

    if request.method == "POST":

        try:

            environment = request.form.get("environment")

            budget = float(request.form.get("budget", 0))

            passengers = int(request.form.get("passengers", 0))

            if environment not in [
                "city", "hill", "highway", "eco"
            ]:
                raise ValueError()

            if budget <= 0 or budget > 1000000:
                raise ValueError()

            if passengers < 1 or passengers > 10:
                raise ValueError()

            recommendations = recommend_vehicles(
                environment,
                budget,
                passengers
            )

            search_performed = True

        except (ValueError, TypeError):

            error = "Please enter valid journey preferences."

    return render_template(
        "recommend.html",
        recommendations=recommendations,
        search_performed=search_performed,
        error=error
    )


# ==========================================
# VEHICLES
# ==========================================

@app.route("/vehicles")
def vehicles():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "vehicles.html",
        user=session["user"]
    )


# ==========================================
# BOOKING
# ==========================================

@app.route("/booking/<vehicle>", methods=["GET", "POST"])
def booking(vehicle):

    if "user" not in session:
        return redirect("/login")

    selected_vehicle = next(
        (
            item for item in VEHICLES
            if item["name"] == vehicle
        ),
        None
    )

    if selected_vehicle is None:
        return "Vehicle not found.", 404

    if request.method == "POST":

        # ----------------------------------
        # CUSTOMER INFORMATION
        # ----------------------------------

        full_name = request.form.get(
            "full_name", ""
        ).strip()

        phone = request.form.get(
            "phone", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip().lower()

        # ----------------------------------
        # IDENTITY INFORMATION
        # ----------------------------------

        aadhaar_last4 = request.form.get(
            "aadhaar_last4", ""
        ).strip()

        driving_license = request.form.get(
            "driving_license", ""
        ).strip().upper()

        # ----------------------------------
        # TRAVEL INFORMATION
        # ----------------------------------

        pickup_location = request.form.get(
            "pickup_location", ""
        ).strip()

        destination = request.form.get(
            "destination", ""
        ).strip()

        pickup = request.form.get(
            "pickup", ""
        ).strip()

        dropoff = request.form.get(
            "dropoff", ""
        ).strip()

        pickup_time = request.form.get(
            "pickup_time", ""
        ).strip()

        dropoff_time = request.form.get(
            "dropoff_time", ""
        ).strip()

        trip_purpose = request.form.get(
            "trip_purpose", ""
        ).strip()

        special_requests = request.form.get(
            "special_requests", ""
        ).strip()

        # ----------------------------------
        # ADDITIONAL INFORMATION
        # ----------------------------------

        emergency_contact = request.form.get(
            "emergency_contact", ""
        ).strip()

        try:

            passengers = int(
                request.form.get("passengers", 0)
            )

            # ----------------------------------
            # REQUIRED FIELD VALIDATION
            # ----------------------------------

            required_fields = [
                full_name,
                phone,
                email,
                aadhaar_last4,
                driving_license,
                pickup_location,
                destination,
                pickup,
                dropoff,
                pickup_time,
                dropoff_time,
                trip_purpose,
                emergency_contact
            ]

            if not all(required_fields):
                return "Please complete all required booking fields.", 400

            # ----------------------------------
            # CUSTOMER VALIDATION
            # ----------------------------------

            if len(full_name) > 100:
                return "Name is too long.", 400

            if not re.fullmatch(r"[6-9][0-9]{9}", phone):
                return "Enter a valid 10-digit mobile number.", 400

            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                return "Enter a valid email address.", 400

            if not re.fullmatch(r"[0-9]{4}", aadhaar_last4):
                return "Enter only the last four Aadhaar digits.", 400

            if len(driving_license) > 30:
                return "Invalid driving licence number.", 400

            if not re.fullmatch(r"[6-9][0-9]{9}", emergency_contact):
                return "Enter a valid emergency contact number.", 400

            # ----------------------------------
            # TRAVEL VALIDATION
            # ----------------------------------

            if len(pickup_location) > 200 or len(destination) > 200:
                return "Travel location is too long.", 400

            pickup_date = datetime.strptime(
                pickup, "%Y-%m-%d"
            ).date()

            dropoff_date = datetime.strptime(
                dropoff, "%Y-%m-%d"
            ).date()

            datetime.strptime(
                pickup_time, "%H:%M"
            )

            datetime.strptime(
                dropoff_time, "%H:%M"
            )

            if pickup_date < date.today():
                return "Pickup date cannot be in the past.", 400

            if dropoff_date < pickup_date:
                return "Return date cannot be before pickup date.", 400

            if dropoff_date == pickup_date and dropoff_time <= pickup_time:
                return "Return time must be later than pickup time.", 400

            if passengers < 1 or passengers > selected_vehicle["seats"]:
                return (
                    f"This vehicle can accommodate a maximum of "
                    f"{selected_vehicle['seats']} passengers."
                ), 400

            if trip_purpose not in [
                "Tourism",
                "Business",
                "Personal",
                "Family Trip",
                "Other"
            ]:
                return "Select a valid trip purpose.", 400

            if len(special_requests) > 500:
                return "Special requests are too long.", 400

            # ----------------------------------
            # SAVE BOOKING
            # ----------------------------------

            new_booking = Booking(

                username=session["user"],

                vehicle=vehicle,

                # Existing fields
                pickup=pickup,
                dropoff=dropoff,

                # Customer details
                full_name=full_name,
                phone=phone,
                email=email,

                # Identity details
                aadhaar_last4=aadhaar_last4,
                driving_license=driving_license,

                # Travel details
                pickup_location=pickup_location,
                destination=destination,

                pickup_time=pickup_time,
                dropoff_time=dropoff_time,

                passengers=passengers,
                trip_purpose=trip_purpose,

                # Additional details
                emergency_contact=emergency_contact,
                special_requests=special_requests

            )

            db.session.add(new_booking)

            db.session.commit()

            return render_template(
                "success.html",
                vehicle=vehicle,
                pickup=pickup,
                dropoff=dropoff
            )

        except ValueError:

            return "Please enter valid booking information.", 400

        except Exception:

            db.session.rollback()

            app.logger.exception("Booking could not be saved.")

            return "Something went wrong while saving your booking.", 500

    return render_template(
        "booking.html",
        vehicle=vehicle
    )


# ==========================================
# MY TRIPS
# ==========================================

@app.route("/mytrips")
def mytrips():

    if "user" not in session:
        return redirect("/login")

    trips = Booking.query.filter_by(
        username=session["user"]
    ).order_by(
        Booking.id.desc()
    ).all()

    return render_template(
        "mytrips.html",
        trips=trips
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")



# ==========================================
# DATABASE INITIALIZATION
# ==========================================

with app.app_context():

    os.makedirs(app.instance_path, exist_ok=True)

    # Create database tables
    db.create_all()

    # Safely migrate existing database columns
    migrate_database()


# ==========================================
# RUN APPLICATION
# ==========================================

with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)
    db.create_all()

    # Run the old migration helper only for local SQLite
    if db.engine.dialect.name == "sqlite":
        migrate_database()


if __name__ == "__main__":
    app.run(debug=False)
