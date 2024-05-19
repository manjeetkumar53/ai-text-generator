from src.app import app as gunicorn_app

# This file does not need to contain any logic. Gunicorn will use this file to locate the Flask application.
# Gunicorn expects an app callable, which is 'gunicorn_app' in this case.
