# wsgi.py
# This is the entry point for Gunicorn.
# It imports the 'app' instance from your main application file.
from app import app

if __name__ == "__main__":
    app.run()
