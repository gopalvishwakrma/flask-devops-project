import os
from flask import Flask, jsonify, render_template, request, flash, redirect
import redis
import psycopg2
from flask_mail import Mail, Message

# Initialize Flask app
app = Flask(__name__)

# Set secret key for session handling and flash messages
app.secret_key = os.urandom(24)

# Redis connection using environment variables (default host is 'redis')
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)

# PostgreSQL connection using environment variables
db_conn = psycopg2.connect(
    host="db",  # Hostname for Postgres service
    database=os.getenv('POSTGRES_DB', 'myapp'),  # Database name
    user=os.getenv('DB_USER', 'admin'),  # Database user
    password=os.getenv('DB_PASSWORD', 'admin')  # Database password
)

# Email configuration for Flask-Mail to handle contact form submissions
app.config['MAIL_SERVER'] = 'mail.supporthives.com'  # SMTP server for sending emails
app.config['MAIL_PORT'] = 465  # Port for SSL
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'gopalvish@supporthives.com')  # Email address for sending emails
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '7kR&CQY%PN')  # Email password (should be stored in a secure environment variable)
app.config['MAIL_USE_SSL'] = True  # SSL encryption for secure email transmission

# Initialize Flask-Mail with the app's configuration
mail = Mail(app)

# Route for the homepage
@app.route('/')
def home():
    # Increment Redis 'hits' key to track visits
    cache.incr('hits')
    
    # Get current hit count from Redis and decode to string
    counter = cache.get('hits').decode('utf-8')
    
    # Project description for rendering on the home page
    project_description = (
        "This is a Flask-based DevOps project showcasing Docker Compose with Redis, PostgreSQL, and NGINX. "
        "The project demonstrates Gopal Vishwakarma's expertise in containerization and advanced DevOps tools integration for scalable application deployment."
    )
    
    # Render 'index.html' template with hit counter and project description
    return render_template('index.html', hits=counter, description=project_description)

# Route for handling 'Contact Us' form submissions
@app.route('/contact', methods=['POST'])
def contact():
    # Extract form data: name, email, and message
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Validate form fields (ensure none are empty)
    if not name or not email or not message:
        flash("Please fill out all fields", "danger")  # Show error if any field is missing
        return redirect('/')  # Redirect back to home page

    try:
        # Create email message with subject and sender information
        msg = Message(f"Contact Us Form Submission from {name}",
                      sender=os.getenv('MAIL_USERNAME', 'gopalvish@supporthives.com'),
                      recipients=[os.getenv('MAIL_USERNAME', 'gopalvish@supporthives.com')])  # Send email to project owner's address

        # Email body includes the form submission details
        msg.body = f"""
        Hello Gopal,

        You have received a new message from your project showcase contact form.

        --------------------------------
        Name: {name}
        Email: {email}
        Message:
        {message}
        --------------------------------

        Best Regards,
        Your Project Team
        """

        # Send the email using Flask-Mail
        mail.send(msg)

        flash("Your message has been sent!", "success")  # Show success message
    except Exception as e:
        # Catch any errors and show an error message
        flash(f"An error occurred: {str(e)}", "danger")

    # Redirect back to home page after form submission
    return redirect('/')

# Run the Flask app on port 5000, accessible from all network interfaces
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
