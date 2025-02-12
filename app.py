import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import plotly
from sqlalchemy.exc import IntegrityError
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import logging
from flask_cors import CORS
import plotly.express as px
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_development_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    disability = db.Column(db.String(50), nullable=False)
    job_field_interest = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.name}>'


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    job_field = db.Column(db.String(100), nullable=False)
    required_skills = db.Column(db.String(500), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', back_populates='jobs')

    def __repr__(self):
        return f'<Job {self.title}>'


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    job_field = db.Column(db.String(100), nullable=False)
    amenities = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    jobs = db.relationship('Job', back_populates='company')

    def __repr__(self):
        return f'<Company {self.name}>'

from flask_socketio import SocketIO, emit
import pyttsx3
import speech_recognition as sr

socketio = SocketIO(app)

tts_engine = pyttsx3.init()

def text_to_speech(text):
    """Convert text to speech."""
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        logger.error(f"TTS Error: {str(e)}")

def speech_to_text():
    """Convert speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for speech...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            logger.error(f"STT API Error: {str(e)}")
            return "An error occurred with the speech recognition API."

# Flask routes and endpoints for TTS and STT
@app.route('/api/text_to_speech', methods=['POST'])
def api_text_to_speech():
    """Endpoint to handle TTS."""
    data = request.json
    text = data.get('text', '')
    if text:
        text_to_speech(text)
        return jsonify({"message": "Text has been converted to speech"}), 200
    else:
        return jsonify({"message": "No text provided"}), 400

@app.route('/api/speech_to_text', methods=['GET'])
def speech_to_text():
    """Convert speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        text = "Listening for your command..."
        text_to_speech(text)  # Provide feedback to the user
        print(text)

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            logger.error(f"STT API Error: {str(e)}")
            return "An error occurred with the speech recognition service."


# Real-time TTS/STT communication with SocketIO
@socketio.on('speak')
def handle_speak_event(data):
    """Handle TTS request over WebSocket."""
    text = data.get('text', '')
    if text:
        text_to_speech(text)
        emit('tts_complete', {"message": "Text-to-Speech complete"})

@socketio.on('listen')
def handle_listen_event():
    """Handle STT request over WebSocket for navigation."""
    command = speech_to_text()
    emit('stt_complete', {"transcription": command})

    if "error" in command.lower() or "sorry" in command.lower():
        emit('navigate', {"url": "/", "error": "Couldn't understand your command. Please try again."})
        return

    navigation_map = {
        "home": "/",
        "jobs": "/jobs",
        "analytics": "/analytics",
        "login": "/login",
        "register": "/register",
        "companies": "/register_company"
    }

    # Find the corresponding route
    for keyword, route in navigation_map.items():
        if keyword in command.lower():
            emit('navigate', {"url": route})
            return

    # Default case if no keywords matched
    emit('navigate', {"url": "/", "error": "Sorry, I couldn't understand the destination."})


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET'])
def home():
    top_companies = Company.query.order_by(Company.rating.desc()).limit(3).all()
    featured_jobs = []
    
    for company in top_companies:
        featured_jobs.extend(company.jobs)
    
    featured_jobs = featured_jobs[:3]

    return render_template('index.html', jobs=featured_jobs)



@app.route('/job_compatibility', methods=['POST'])
def job_compatibility():
    data = request.json
    user_skills = set(data['skills'])
    job_field = data['job_field_interest']

    try:
        companies = Company.query.filter(Company.job_field.contains(job_field)).all()
        results = []

        for company in companies:
            company_skills = set(company.amenities.split(','))
            compatibility = len(user_skills & company_skills) / len(user_skills) * 100
            results.append({
                "id": company.id,
                "name": company.name,
                "rating": company.rating,
                "compatibility": round(compatibility, 2),
                "address": company.address,
                "amenities": company.amenities,
            })

        return jsonify({"results": results})
    except Exception as e:
        logger.error(f"Error calculating job compatibility: {str(e)}")
        return jsonify({"message": "An error occurred."}), 500


@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        data = request.form
        try:
            company = Company(
                name=data['name'],
                job_field=data['job_field'],
                amenities=data['amenities'],
                address=data['address'],
                rating=float(data.get('rating', 0)),
                latitude=float(data.get('latitude', 0)),
                longitude=float(data.get('longitude', 0))
            )
            db.session.add(company)
            db.session.commit()
            return jsonify({"message": "Company registered successfully!"}), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error while registering company: {str(e)}")
            return jsonify({"message": "Company registration failed due to a conflict."}), 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "An error occurred."}), 500

    return render_template('register_company.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            disability = request.form.get('disability')
            job_field_interest = request.form.get('job_field_interest')
            skills = request.form.get('skills', '').split(',')
            latitude = float(request.form.get('latitude'))
            longitude = float(request.form.get('longitude'))

            if not all([name, email, password, disability, job_field_interest, latitude, longitude]):
                flash('All fields are required', 'error')
                return redirect(url_for('register'))

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered', 'error')
                return redirect(url_for('register'))

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(
                name=name,
                email=email,
                password=hashed_password,
                disability=disability,
                job_field_interest=job_field_interest,
                skills=','.join(skills),
                latitude=latitude,
                longitude=longitude
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error while registering user: {str(e)}")
            flash('Email already registered.', 'error')
        except Exception as e:
            db.session.rollback()
            logger.error(f"Unexpected error: {str(e)}")
            flash('An error occurred during registration.', 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        logger.info(f"Login attempt for email: {data['email']}")
        
        user = User.query.filter_by(email=data['email']).first()

        if user and bcrypt.check_password_hash(user.password, data['password']):
            login_user(user)
            logger.info(f"Successful login for user: {user.email}")

            next_page = request.args.get('next')
            if next_page:
                logger.info(f"Redirecting to next page: {next_page}")
                return redirect(next_page)  
            else:
                logger.info("Redirecting to profile page")
                flash('Login successful!', 'success')
                return redirect(url_for('profile'))
        
        logger.warning(f"Failed login attempt for email: {data['email']}")
        flash('Invalid credentials!', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/analytics.html')
@login_required
def analytics():
    engine = create_engine('sqlite:///job_poortal.db')  
    Session = sessionmaker(bind=engine)
    session = Session()
    # Query the database
    users = session.execute("SELECT disability, job_field_interest FROM user").fetchall()
    df = pd.DataFrame(users, columns=['Disability', 'Job Field'])

    disability_fig = px.bar(df['Disability'].value_counts().reset_index(),
                            x='index', y='Disability',
                            title='Disabilities Distribution',
                            labels={'index': 'Disability', 'Disability': 'Count'})

    job_field_fig = px.bar(df['Job Field'].value_counts().reset_index(),
                           x='index', y='Job Field',
                           title='Job Field Interest Distribution',
                           labels={'index': 'Job Field', 'Job Field': 'Count'})

    disability_graph_json = json.dumps(disability_fig, cls=plotly.utils.PlotlyJSONEncoder)
    job_field_graph_json = json.dumps(job_field_fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('analytics.html',
                           disability_graph=disability_graph_json,
                           job_field_graph=job_field_graph_json)

@app.route('/company_details/<int:company_id>', methods=['GET'])
def company_details(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company_details.html', company=company)

@app.route('/jobs')
def jobs():
    categories = db.session.query(Job.job_field).distinct().all()
    
    all_jobs = Job.query.all()

    all_companies = Company.query.all()

    return render_template(
        'jobs_home.html', 
        categories=categories, 
        jobs=all_jobs, 
        companies=all_companies
    )



@app.route('/jobs/<category>')
@login_required
def show_jobs(category):
    if category.lower() == "all":
        jobs = Job.query.all()
    else:
        jobs = Job.query.filter_by(job_field=category).all()

    return render_template('jobs.html', jobs=jobs, category=category)



@app.route('/profile')
@login_required
def profile():
    user_skills = set(current_user.skills.split(',')) if current_user.skills else set()
    job_field = current_user.job_field_interest

    from sqlalchemy.orm import joinedload
    jobs = Job.query.options(joinedload(Job.company)).filter(Job.job_field == job_field).all()

    optimal_jobs = []
    for job in jobs:
        try:
            print(f"Job: {job.title}, Skills: {job.required_skills}")
            job_skills = set(job.required_skills.split(','))
            print(f"Job Skills: {job_skills}")
            match_percentage = len(user_skills & job_skills) / len(job_skills) * 100 if job_skills else 0
            print(f"Match Percentage: {match_percentage}")
            optimal_jobs.append({
                'job': job,
                'match': round(match_percentage, 2)
            })
        except Exception as e:
            print(f"Error processing job {job.id}: {e}")
            continue

    optimal_jobs = sorted(optimal_jobs, key=lambda x: x['match'], reverse=True)

    optimal_company = None
    if optimal_jobs:
        best_job = optimal_jobs[0]['job']
        optimal_company = best_job.company

    return render_template('profile.html', user=current_user, optimal_jobs=optimal_jobs, optimal_company=optimal_company)

@app.route('/search_companies', methods=['GET'])
def search_companies():
    query = request.args.get('query', '')
    companies = Company.query.filter(Company.name.ilike(f'%{query}%')).all()
    return jsonify([{
        'id': company.id,
        'name': company.name,
        'job_field': company.job_field,
        'amenities': company.amenities,
        'rating': company.rating,
        'address': company.address
    } for company in companies])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template('500.html'), 500


def init_db():
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)