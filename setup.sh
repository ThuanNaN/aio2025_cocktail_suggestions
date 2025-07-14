#!/bin/bash

# Setup script for the Cocktail Suggestions project

echo "🍹 Setting up Cocktail Suggestions Project..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p logs

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your database credentials!"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Set up PostgreSQL with pgvector extension"
echo "3. Download the cocktail dataset from:"
echo "   https://www.kaggle.com/datasets/aadyasingh55/cocktails/data"
echo "4. Place the CSV file in the data/ directory"
echo "5. Run: python database_setup.py"
echo "6. Run: python data_processor.py"
echo "7. Run: streamlit run app.py"
