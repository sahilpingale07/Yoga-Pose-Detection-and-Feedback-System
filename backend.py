from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from Tkinter 

@app.route("/")  # This defines a route for the root URL
def home():
    return "Welcome to the Yoga Pose App Backend!"

# ** MySQL Database Configuration **
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sproot@localhost/yoga_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ** User Model **
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    injuries = db.Column(db.Text)
    disabilities = db.Column(db.Text)

    def __init__(self, username, password, name, age, gender, injuries, disabilities):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode()
        self.name = name
        self.age = age
        self.gender = gender
        self.injuries = injuries
        self.disabilities = disabilities

# ** Create database tables if they do not exist **
with app.app_context():
    db.create_all()

# ** User Registration API **
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    injuries = data.get('injuries', "")
    disabilities = data.get('disabilities', "")

    if not all([username, password, name, age, gender]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"status": "error", "message": "Username already taken"}), 409

    new_user = User(username=username, password=password, name=name, age=age, gender=gender, injuries=injuries, disabilities=disabilities)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered successfully"}), 201


# ** User Login API **
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"status": "success", "message": "Login successful"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)     # Run on localhost

#get API    
@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    
    if user:
        return jsonify({
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "username": user.username,
            "injuries": user.injuries,
            "disabilities": user.disabilities
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

