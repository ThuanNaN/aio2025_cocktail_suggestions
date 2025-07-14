# 🍹 Cocktail Suggestions - Project Setup Guide

## 📁 What We Built

A complete AI-powered cocktail recommendation system with:

### Core Components

1. **`database_setup.py`** - PostgreSQL + pgvector setup
2. **`data_processor.py`** - Kaggle dataset processing and embedding generation
3. **`recommender.py`** - AI-powered recommendation engine
4. **`app.py`** - Beautiful Streamlit web interface

### Supporting Files

- **`requirements.txt`** - All Python dependencies
- **`docker-compose.yml`** - Complete Docker setup
- **`quickstart.py`** - Automated setup script
- **`test_system.py`** - System verification
- **`.env.example`** - Configuration template

## 🚀 Getting Started (Choose One Method)

### Method 1: Docker (Easiest) 🐳

```bash
# 1. Download the cocktail dataset
# Go to: https://www.kaggle.com/datasets/aadyasingh55/cocktails/data
# Download and place cocktails.csv in data/ folder

# 2. Start everything with Docker
docker-compose up -d

# 3. Initialize the database (one-time setup)
docker-compose exec cocktail-app python database_setup.py
docker-compose exec cocktail-app python data_processor.py

# 4. Open http://localhost:8501 in your browser
```

### Method 2: Local Setup 💻

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 3. Download dataset to data/cocktails.csv

# 4. Set up database
python database_setup.py

# 5. Process data and generate embeddings
python data_processor.py

# 6. Start the web app
streamlit run app.py
```

### Method 3: Quick Setup Script 🔧

```bash
# Run the automated setup
python quickstart.py

# Follow the instructions shown
```

## 📋 Prerequisites

### For Docker

- Docker and Docker Compose
- The cocktail dataset (cocktails.csv)

### For Local Setup

- Python 3.8+
- PostgreSQL with pgvector extension
- The cocktail dataset (cocktails.csv)

## 🎯 How to Use the App

### Search Options

1. **🔍 By Name** - Search for specific cocktails
2. **🥃 By Ingredients** - Get suggestions based on what you have
3. **🎭 By Style** - Find drinks by mood (sweet, strong, fruity, etc.)
4. **🎉 By Occasion** - Perfect drinks for parties, dates, etc.
5. **🎲 Mixed Preferences** - Combine multiple criteria
6. **📂 By Category** - Browse drink categories
7. **🎰 Random Discovery** - Let AI surprise you

### Features

- Real-time similarity matching
- Beautiful, responsive interface
- Detailed recipes and ingredients
- Similarity scores for each recommendation

## 🔧 Troubleshooting

### Common Issues

1. **"Import errors"** - Install requirements: `pip install -r requirements.txt`

2. **"Database connection failed"** - Check PostgreSQL is running and .env file

3. **"pgvector extension not found"** - Install pgvector in PostgreSQL

4. **"Dataset not found"** - Download cocktails.csv to data/ folder

5. **"Memory issues"** - The AI model needs ~2GB RAM for embeddings

### Test Your Setup

```bash
python test_system.py
```

## 🎉 What's Next?

After setup, you can

- Explore 600+ cocktail recipes
- Get personalized recommendations
- Discover new drinks based on your preferences
- Learn about cocktail ingredients and preparation

## 🆘 Need Help?

1. Check the detailed README.md
2. Run the test script: `python test_system.py`
3. Check logs in the logs/ directory
4. Ensure all dependencies are installed correctly

---

**Enjoy discovering your perfect cocktail! 🍹**
