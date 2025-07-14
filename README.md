# 🍹 AI-Powered Cocktail Suggestions

An intelligent cocktail recommendation system using vector databases and AI embeddings to suggest the perfect drinks based on your preferences.

## 🎯 Project Overview

This project creates a smart cocktail recommendation system that

- Stores cocktail recipes in a vector database using pgvector
- Uses AI embeddings to understand cocktail characteristics
- Provides personalized suggestions based on user preferences
- Features a beautiful Streamlit web interface

## 🏗️ Architecture

- **Database**: PostgreSQL with pgvector extension for vector similarity search
- **AI Model**: SentenceTransformers for generating embeddings
- **Web Framework**: Streamlit for the user interface
- **Dataset**: Kaggle cocktails dataset with 600+ recipes

## 📊 Dataset

**Source**: https://www.kaggle.com/datasets/aadyasingh55/cocktails/data

## 🛠️ Technology Stack

- **Vector Database**: [pgvector](https://github.com/pgvector/pgvector)
- **Web Framework**: Streamlit
- **AI/ML**: SentenceTransformers, scikit-learn
- **Database**: PostgreSQL
- **Language**: Python 3.8+

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/ThuanNaN/aio2025_cocktail_suggestions
cd aio2025_cocktail_suggestions

# Download the dataset
# Place cocktails.csv in the data/ directory

# Start with Docker Compose
docker-compose up -d

# Set up the database (first time only)
docker-compose exec cocktail-app python database_setup.py
docker-compose exec cocktail-app python data_processor.py

# Access the app at http://localhost:8501
```

### Option 2: Local Setup

```bash
# Clone the repository
git clone <repository-url>
cd aio2025_cocktail_suggestions

# Run the quick setup
python quickstart.py

# Or manual setup:
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials

# Set up PostgreSQL with pgvector
# Run the database setup
python database_setup.py

# Process and store the cocktail data
python data_processor.py

# Start the Streamlit app
streamlit run app.py
```

## 📋 Prerequisites

### For Local Setup

- Python 3.8+
- PostgreSQL with pgvector extension
- Git

### For Docker Setup

- Docker and Docker Compose

## 🔧 Configuration

1. **Environment Variables** (`.env` file):

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=cocktails_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   MODEL_NAME=all-MiniLM-L6-v2
   ```

2. **Database Setup**:
   - Install PostgreSQL
   - Install pgvector extension
   - Create database and user

3. **Dataset**:
   - Download from Kaggle
   - Place `cocktails.csv` in `data/` directory

## 🎮 Features

### 🔍 Search Options

- **By Name**: Find specific cocktails
- **By Ingredients**: Get suggestions based on available ingredients
- **By Style/Mood**: Find drinks matching your mood (sweet, strong, refreshing, etc.)
- **By Occasion**: Perfect drinks for parties, date nights, etc.
- **Mixed Preferences**: Combine multiple criteria
- **By Category**: Browse by drink categories
- **Random Discovery**: Let AI surprise you

### 🎨 User Interface

- Modern, responsive design
- Real-time search and filtering
- Similarity scores for recommendations
- Detailed recipe information
- Ingredient highlighting

### 🧠 AI Features

- Vector similarity search
- Semantic understanding of preferences
- Contextual recommendations
- Personalized suggestions

## 📁 Project Structure

```text
aio2025_cocktail_suggestions/
├── app.py                 # Main Streamlit application
├── database_setup.py      # Database initialization
├── data_processor.py      # Data processing and embedding generation
├── recommender.py         # Recommendation engine
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker setup
├── Dockerfile            # Docker configuration
├── quickstart.py         # Quick setup script
├── setup.sh             # Bash setup script
├── .env.example         # Environment variables template
├── data/                # Dataset directory
│   ├── README.md
│   └── final_cocktails.csv    # (Download required)
└── README.md           # This file
```

## 🔬 How It Works

1. **Data Processing**: Cocktail recipes are processed and converted into high-dimensional vectors using SentenceTransformers
2. **Vector Storage**: Embeddings are stored in PostgreSQL with pgvector for efficient similarity search
3. **Recommendation**: User preferences are converted to vectors and matched against the database using cosine similarity
4. **Ranking**: Results are ranked by similarity score and presented through the web interface

## 🎯 Use Cases

- **Home Bartenders**: Discover new cocktails based on available ingredients
- **Cocktail Enthusiasts**: Explore drinks by style and preference
- **Event Planning**: Find perfect drinks for specific occasions
- **Learning**: Understand cocktail composition and flavor profiles

## 🔮 Future Enhancements

- User rating system
- Personal cocktail collection
- Ingredient substitution suggestions
- Nutritional information
- Social sharing features
- Mobile app version

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

**Common Issues:**

1. **Database Connection Error**: Check your `.env` file and ensure PostgreSQL is running
2. **pgvector Extension**: Make sure pgvector is properly installed in PostgreSQL
3. **Dataset Not Found**: Download the cocktails.csv file and place it in the data/ directory
4. **Memory Issues**: The embedding generation can be memory-intensive; consider processing in batches

**Support:**

- Check the logs in the `logs/` directory
- Ensure all dependencies are installed correctly
- Verify database credentials and connectivity
