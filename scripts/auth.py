import jwt
import datetime
from functools import wraps
from flask import Blueprint, app, request, jsonify, current_app
from database import load_database_config
import mysql.connector
from config import SECRET_KEY 
auth_bp = Blueprint('auth', __name__)

# JWT 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')  # JWT request
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = get_user_by_username(data['username'])  # get username from JWT
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated

def get_user_by_username(username):
    db_config = load_database_config()
    try:
        conn = mysql.connector.connect(**db_config['development'])
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# register
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    role = 'user'

    db_config = load_database_config()
    try:
        conn = mysql.connector.connect(**db_config['development'])
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "User registered successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)}), 500

# login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = get_user_by_username(username)
    
    print(f"Queried user: {user}")
    if user:
        if user["password"]==password:
            token= jwt.encode({
                'username': user["username"], 
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                SECRET_KEY, algorithm="HS256")
            print(f"Generated JWT token: {token}") 
            return jsonify({'token': token})
        return jsonify({'message': 'Invalid password'}), 401
    return jsonify({'message': 'User not found'}), 404

