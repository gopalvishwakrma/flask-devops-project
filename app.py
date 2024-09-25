import os
from flask import Flask, jsonify, render_template, request, flash, redirect
import redis
import psycopg2
from flask_mail import Mail, Message

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for session management

# Redis and Postgres connections
# Connect to the Redis cache
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)
# Connect to the PostgreSQL database
db_conn = psycopg2.connect(
    host="db",
    database=os.getenv('POSTGRES_DB', 'myapp'),
    user=os.getenv('DB_USER', 'admin'),
    password=os.getenv('DB_PASSWORD', 'admin')
)

# Email configuration for the Contact Us form
app.config['MAIL_SERVER'] = 'mail.supporthives.com'  # Mail server address
app.config['MAIL_PORT'] = 465  # Mail server port
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'gopalvish@supporthives.com')  # Sender's email
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '7kR&CQY%PN')  # Sender's email password (consider using a secret storage in production)
app.config['MAIL_USE_SSL'] = True  # Use SSL for secure email communication
mail = Mail(app)  # Initialize the Flask-Mail instance

@app.route('/')
def home():
    # Increment the hit counter in Redis
    cache.incr('hits')
    counter = cache.get('hits').decode('utf-8')  # Get the current hit count from Redis
    project_description = (
        "This is a Flask-based DevOps project showcasing Docker Compose with Redis, PostgreSQL, and NGINX. "
        "The project demonstrates Gopal Vishwakarma's expertise in containerization and advanced DevOps tools integration for scalable application deployment."
    )
    # Render the home page with hit counter and project description
    return render_template('index.html', hits=counter, description=project_description)

@app.route('/contact', methods=['POST'])
def contact():
    # Retrieve form data from the request
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Check if any field is empty and flash a message if so
    if not name or not email or not message:
        flash("Please fill out all fields", "danger")
        return redirect('/')  # Redirect back to home

    try:
        # Save the contact message to the PostgreSQL database
        with db_conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
            db_conn.commit()  # Commit the transaction to save changes

        # Prepare and send an email notification for the contact submission
        msg = Message(f"Contact Us Form Submission from {name}",
                      sender=os.getenv('MAIL_USERNAME', 'gopalvish@supporthives.com'),
                      recipients=[os.getenv('MAIL_USERNAME', 'gopalvish@supporthives.com')])

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
        mail.send(msg)  # Send the email notification

        flash("Your message has been sent!", "success")  # Flash a success message
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")  # Flash an error message
        db_conn.rollback()  # Rollback the transaction in case of error

    return redirect('/')  # Redirect back to home

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Run the Flask application
