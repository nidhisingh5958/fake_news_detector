#!/usr/bin/env python3
"""
Fake News Detector - Setup and Run Script
"""
import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def train_model():
    """Train the machine learning model"""
    print("Training model...")
    subprocess.check_call([sys.executable, "train_model.py"])

def run_app():
    """Run the Flask application"""
    print("Starting web application...")
    subprocess.check_call([sys.executable, "app.py"])

def main():
    print("🔍 Fake News Detector Setup")
    print("=" * 30)
    
    # Check if model exists
    if not os.path.exists("model.pkl"):
        print("Model not found. Training new model...")
        install_requirements()
        train_model()
    else:
        print("Model found. Skipping training.")
    
    print("\n🚀 Starting web application...")
    print("Open http://127.0.0.1:8000 in your browser")
    run_app()

if __name__ == "__main__":
    main()