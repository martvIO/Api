import os
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("database-b81ee-firebase-adminsdk-6w3fp-05d9a01c2d.json")  # Replace with your credentials file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://database-b81ee-default-rtdb.firebaseio.com/'  # Replace with your Firebase database URL
})

# Route to add username and password to Firebase Realtime Database
@app.route('/register', methods=['POST'])
def register_user():
    # Get JSON data from the request
    data = request.get_json()

    # Validate that 'username' and 'password' are in the request
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data['username']
    password = data['password']

    # Reference to the Realtime Database
    ref = db.reference('users')

    # Push new user data to Firebase under a unique key
    ref.push({
        'username': username,
        'password': password
    })

    return jsonify({"message": "User registered successfully"}), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port,debug=True)
