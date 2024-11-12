import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import firebase_admin
from firebase_admin import credentials, db

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Firebase Admin SDK
cred = credentials.Certificate("database-b81ee-firebase-adminsdk-6w3fp-05d9a01c2d.json")  # Replace with your credentials file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://database-b81ee-default-rtdb.firebaseio.com/'  # Replace with your Firebase database URL
})

# Route to add username and password to Firebase Realtime Database
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()  # Retrieve JSON data from the request
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # Reference to the Realtime Database
        ref = db.reference('users').child(username)

        # Store password (as example, ideally should be hashed for security)
        ref.set({
            'password': password
        })

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/l/{u}/{p}',methods=['POST'])
def register_user(u,p):
    username = u
    password = p

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # Reference to the Realtime Database
        ref = db.reference('users').child(username)

        # Store password (as example, ideally should be hashed for security)
        ref.set({
            'password': password
        })

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
