"""
Routes and views for the flask application.
"""

import os
from datetime import datetime
from flask import render_template
from FlaskWebProject1 import app


def load_env_file():
    """Load local .env settings without needing shell-specific commands."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

    if not os.path.exists(env_path):
        return

    with open(env_path) as env_file:
        for line in env_file:
            line = line.strip()

            if not line or line.startswith('#') or '=' not in line:
                continue

            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip().strip('"').strip("'")


load_env_file()


def get_mysql_time():
    """Read the current timestamp from MySQL."""
    import mysql.connector

    connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', '127.0.0.1'),
        port=int(os.getenv('MYSQL_PORT', '3306')),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE') or None,
    )

    try:
        cursor = connection.cursor()
        cursor.execute('SELECT CURRENT_TIMESTAMP()')
        mysql_time = cursor.fetchone()[0]
        cursor.close()
        return mysql_time
    finally:
        connection.close()


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/mysql-time')
def mysql_time():
    """Shows the current timestamp from the MySQL container."""
    try:
        current_time = get_mysql_time()
        message = 'Docker Compose Flask app - MySQL container current time is: {}'.format(current_time)
    except Exception as error:
        message = 'Could not read MySQL time: {}'.format(error)

    return render_template(
        'about.html',
        title='MySQL Time',
        year=datetime.now().year,
        message=message
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/version')
def version():
    from flask import jsonify
    return jsonify({
        "instance": os.getenv("INSTANCE_NAME", "unknown"),
        "version": os.getenv("APP_VERSION", "500.0")
        "testStatement": "This is a test statement to trigger a new build and deployment"
    })


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
