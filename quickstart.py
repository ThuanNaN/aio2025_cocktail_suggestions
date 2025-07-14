#!/usr/bin/env python3
"""
Quick start script for the Cocktail Suggestions project
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("⚠️  Please edit .env file with your database credentials!")
        else:
            print("❌ .env.example not found")
            return False
    print("✅ .env file exists")
    return True

def create_directories():
    """Create necessary directories"""
    dirs = ['data', 'logs']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"📁 Created directory: {dir_name}")

def check_dataset():
    """Check if dataset exists"""
    csv_path = "data/cocktails.csv"
    if os.path.exists(csv_path):
        print(f"✅ Dataset found at {csv_path}")
        return True
    else:
        print(f"⚠️  Dataset not found at {csv_path}")
        print("Please download from: https://www.kaggle.com/datasets/aadyasingh55/cocktails/data")
        return False

def main():
    print("🍹 Cocktail Suggestions - Quick Start")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create directories
    create_directories()
    
    # Check/create .env file
    if not check_env_file():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check dataset
    dataset_exists = check_dataset()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Configure your database credentials in .env")
    if not dataset_exists:
        print("2. Download and place the cocktail dataset in data/cocktails.csv")
        print("3. Run: python database_setup.py")
        print("4. Run: python data_processor.py")
    else:
        print("2. Run: python database_setup.py")
        print("3. Run: python data_processor.py")
    print("4. Run: streamlit run app.py")
    
    # Try to import key dependencies to verify installation
    print("\n🔍 Verifying installations...")
    try:
        import streamlit
        print("✅ Streamlit installed")
    except ImportError:
        print("❌ Streamlit not installed")
    
    try:
        import psycopg2
        print("✅ psycopg2 installed")
    except ImportError:
        print("❌ psycopg2 not installed")
    
    try:
        import sentence_transformers
        print("✅ sentence-transformers installed")
    except ImportError:
        print("❌ sentence-transformers not installed")

if __name__ == "__main__":
    main()
