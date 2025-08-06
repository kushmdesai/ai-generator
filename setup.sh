#!/bin/bash

# Exit if any command fails
set -e

echo "🔧 Starting Flask Chatbot App..."

# Create logs directory if it doesn't exist
mkdir -p logs

# Optional: activate virtualenv if you're using one
# source venv/bin/activate

# Export environment variables
export FLASK_APP=app.py
export FLASK_ENV=production
# export GEMINI_API_KEY="your-key-here"  # optionally uncomment if not in env

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Get current timestamp for log file
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Start the app and redirect all output to logs
echo "🚀 Launching with Gunicorn..."
gunicorn app:app \
  --bind 0.0.0.0:${PORT:-5000} \
  --workers 2 \
  --threads 2 \
  --timeout 60 \
  > logs/gunicorn_${TIMESTAMP}.log 2>&1
