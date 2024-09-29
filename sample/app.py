from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Real data for user authentication (auto replace with actual DB queries)
users = {
    'dahal@gmail.com': {
        'password': '987456321'
    }
}

# Ensure the main data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Create subdirectories for different user data types
subdirectories = ['login', 'signup', 'forgot_password', 'contact']
for subdirectory in subdirectories:
    if not os.path.exists(f'data/{subdirectory}'):
        os.makedirs(f'data/{subdirectory}')

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission for contact us and save data to JSON
@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()  # Get form data as dictionary
    contact_file_path = 'data/contact/contact_data.json'
    
    # Check if the contact file already exists and load the data
    if os.path.exists(contact_file_path):
        with open(contact_file_path, 'r') as json_file:
            try:
                contact_data = json.load(json_file)
                # Ensure contact_data is a list
                if isinstance(contact_data, dict):
                    contact_data = [contact_data]
            except json.JSONDecodeError:
                # In case the JSON is empty or invalid, start with an empty list
                contact_data = []
    else:
        contact_data = []

    # Append the new contact form data to the list
    contact_data.append(form_data)
    
    # Save the updated contact data to the JSON file
    with open(contact_file_path, 'w') as json_file:
        json.dump(contact_data, json_file, indent=4)
    
    return jsonify({"status": "success", "message": "Data saved successfully!"})

# Route to handle sign-up form submission
@app.route('/signup', methods=['POST'])
def signup_form():
    print("Sign-up form submitted!")  # Check if route is reached
    form_data = request.form.to_dict()  # Convert form data to dictionary
    email = form_data.get('email').strip()
    password = form_data.get('password').strip()

    # Check if the email is already in use
    if email in users:
        return jsonify({"status": "failure", "message": "Email already exists."}), 409

    # Save new user data (in real application, save to DB)
    users[email] = {'password': password}

    # Save to JSON in the signup folder
    filename = f"data/signup/{email.replace('@', '_at_')}.json"
    with open(filename, 'w') as json_file:
        json.dump({'email': email, 'password': password}, json_file, indent=4)

    return jsonify({"status": "success", "message": "Sign-up successful!"})

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    form_data = request.form.to_dict()  # Get form data
    email = form_data.get('email').strip()
    password = form_data.get('password').strip()

    # Check if email exists in users data and if password matches
    if email in users and users[email]['password'] == password:
        # Log successful login (optional)
        login_data = {'email': email}
        filename = f"data/login/{email.replace('@', '_at_')}.json"
        with open(filename, 'w') as json_file:
            json.dump(login_data, json_file, indent=4)

        return jsonify({"status": "success", "message": "Login successful!"})
    else:
        return jsonify({"status": "failure", "message": "Invalid email or password"}), 401

# Route for forgot password
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    form_data = request.form.to_dict()  # Get form data
    email = form_data.get('email').strip()

    # Check if the email exists in the user data
    if email in users:
        # Here you would typically send a reset email to the user
        # For now, we'll just simulate success
        return jsonify({"status": "success", "message": "Reset link sent to your email!"})
    else:
        return jsonify({"status": "failure", "message": "Email not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
