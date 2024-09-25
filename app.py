import os
from flask import Flask, jsonify, render_template, request, flash
import redis
import psycopg2
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Redis and Postgres connections
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)
db_conn = psycopg2.connect(
    host="db",
    database=os.getenv('POSTGRES_DB', 'myapp'),
    user=os.getenv('DB_USER', 'admin'),
    password=os.getenv('DB_PASSWORD', 'admin')
)

# Email configuration for Contact Us form
app.config['MAIL_SERVER'] = 'smtp'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gopalvish@supporthives.com'
app.config['MAIL_PASSWORD'] = '7kR&CQY%PN'  # Use an environment variable or secret storage in production
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def home():
    cache.incr('hits')
    counter = cache.get('hits').decode('utf-8')
    project_description = "This is a Flask-based DevOps project showcasing Docker Compose with Redis, PostgreSQL, and NGINX. \
    The project demonstrates Gopal Vishwakarma's expertise in containerization, continuous deployment with Jenkins, and \
    advanced DevOps tools integration."
    return render_template('index.html', hits=counter, description=project_description)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    if not name or not email or not message:
        flash("Please fill out all fields", "danger")
        return redirect('/')

    # Send an email notification
    msg = Message(f"Contact Us Form Submission from {name}",
                  sender='gopalvish@supporthives.com',
                  recipients=['gopalvish@supporthives.com'])
    msg.body = f"Message from {name} ({email}): {message}"
    mail.send(msg)

    flash("Your message has been sent!", "success")
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

