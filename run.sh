#!/bin/bash

echo "🚀 Starting AI Fake News Detector..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start the Flask application
echo "🌐 Starting Flask server..."
echo "📱 Open http://localhost:5000 in your browser"
python app.py