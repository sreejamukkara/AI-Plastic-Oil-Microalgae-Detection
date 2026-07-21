from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import os 

from datetime import datetime

def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id  
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        

        if User.query.filter_by(email=email).first():
            flash('Email address already in use. Please choose a different one.', 'danger')
            return render_template('auth.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('auth.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth.html')

@app.route('/home')
def home():
    return render_template('home.html')

# Load all three models
plastic_model = YOLO('models/plastic.pt')  # Plastic Detection model
oil_model = YOLO('models/oil.pt')         # Oil Spill Detection model  
algae_model = YOLO('models/algae.pt')     # Micro Algae Detection model

# Define target classes for each model
MODEL_CLASSES = {
    'plastic': [
        'Glass', 'Metal', 'Plastic', 'Trash'
    ],
    'oil': [
        'oil spill', 'oil_spillage'
    ],
    'algae': [
        'micro-algae'
    ]
}

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['image_file']
        model_type = request.form.get('model_type', 'plastic')  # Default to plastic detection

        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            image = cv2.imread(file_path)
            
            # Select the appropriate model based on user choice
            if model_type == 'plastic':
                model = plastic_model
                target_classes = MODEL_CLASSES['plastic']
                detection_type = "Plastic Waste"
                # Normal settings for plastic detection
                font_scale = 0.7
                thickness = 2
                show_labels = True
            elif model_type == 'oil':
                model = oil_model
                target_classes = MODEL_CLASSES['oil']
                detection_type = "Oil Spill"
                # Normal settings for oil detection
                font_scale = 0.7
                thickness = 2
                show_labels = True
            else:  # algae
                model = algae_model
                target_classes = MODEL_CLASSES['algae']
                detection_type = "Micro Algae"
                # Optimized settings for algae detection - smaller text, no background
                font_scale = 0.4  # Smaller font for algae
                thickness = 1     # Thinner text
                show_labels = False  # Don't show text labels on bounding boxes for algae
            
            # Run inference
            results = model(image)
            result = results[0]  
            boxes = result.boxes.xywh.cpu().numpy() 
            labels = result.names  
            
            detected_classes = []  # List to store detected class names
            for i, box in enumerate(boxes):
                class_id = int(result.boxes.cls[i]) 
                label_name = labels[class_id]

                if label_name in target_classes and label_name not in detected_classes:
                    detected_classes.append(label_name)  # Add class name to the list if not already present

                x_center, y_center, width, height = box  
                x1 = int((x_center - width / 2))
                y1 = int((y_center - height / 2))
                x2 = int((x_center + width / 2))
                y2 = int((y_center + height / 2))

                # Draw bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2) 

                # Only draw labels if show_labels is True (not for algae)
                if show_labels:
                    label_position = (x1 + 5, y1 + 20)  
                    (w, h), _ = cv2.getTextSize(label_name, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness) 
                    # Draw background for label
                    cv2.rectangle(image, (x1, y1), (x1 + w + 10, y1 + h + 10), (0, 255, 0), -1)  
                    # Draw text
                    cv2.putText(image, label_name, label_position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
                else:
                    # For algae, just show very small label without background if needed
                    # Or remove labels completely by commenting out the text part
                    pass

            result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + uploaded_file.filename)
            cv2.imwrite(result_image_path, image)

            # Prepare the message with detected classes
            if detected_classes:
                detection_message = f"{detection_type} Detected: " + ", ".join(detected_classes)
            else:
                detection_message = f"No {detection_type} Detected"

            print(detection_message)

            return render_template('upload.html', 
                                 result_image=url_for('uploaded_file', filename='result_' + uploaded_file.filename), 
                                 detection_message=detection_message,
                                 selected_model=model_type)

    return render_template('upload.html', selected_model='plastic')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)