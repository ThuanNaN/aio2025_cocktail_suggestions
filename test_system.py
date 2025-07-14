#!/usr/bin/env python3
"""
Simple test script to verify the system components
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import psycopg2
        print("✅ psycopg2 imported successfully")
    except ImportError as e:
        print(f"❌ psycopg2 import failed: {e}")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers imported successfully")
    except ImportError as e:
        print(f"❌ sentence-transformers import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_files():
    """Test if required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'app.py',
        'database_setup.py',
        'data_processor.py',
        'recommender.py',
        'requirements.txt',
        '.env.example'
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_good = False
    
    return all_good

def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import psycopg2
        
        # Try to connect to default postgres database first
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', 'your_password')
        
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'
        )
        conn.close()
        print("✅ Database connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Make sure PostgreSQL is running and credentials are correct in .env")
        return False

def test_model_loading():
    """Test if the AI model can be loaded"""
    print("\nTesting AI model loading...")
    
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ AI model loaded successfully")
        
        # Test embedding generation
        test_text = "vodka cranberry cocktail"
        embedding = model.encode([test_text])
        print(f"✅ Embedding generated successfully (shape: {embedding.shape})")
        return True
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def main():
    print("🧪 Running System Tests")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test files
    files_ok = test_files()
    
    # Test database (only if .env exists)
    db_ok = True
    if os.path.exists('.env'):
        db_ok = test_database_connection()
    else:
        print("\n⚠️  Skipping database test (.env file not found)")
    
    # Test model loading
    model_ok = test_model_loading()
    
    print("\n📊 Test Summary:")
    print(f"Imports: {'✅' if imports_ok else '❌'}")
    print(f"Files: {'✅' if files_ok else '❌'}")
    print(f"Database: {'✅' if db_ok else '❌'}")
    print(f"AI Model: {'✅' if model_ok else '❌'}")
    
    if all([imports_ok, files_ok, db_ok, model_ok]):
        print("\n🎉 All tests passed! System is ready.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
