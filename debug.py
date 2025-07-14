#!/usr/bin/env python3
"""
Debug script to help troubleshoot the cocktail recommendation system
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def check_database():
    """Check database connection and contents"""
    print("🔍 Checking database...")
    
    try:
        from database_setup import DatabaseSetup
        db = DatabaseSetup()
        
        # Test connection
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Check if cocktails table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'cocktails'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("❌ Cocktails table doesn't exist")
            print("Run: python database_setup.py")
            return False
        
        print("✅ Cocktails table exists")
        
        # Check number of cocktails
        cursor.execute("SELECT COUNT(*) FROM cocktails")
        count = cursor.fetchone()[0]
        print(f"📊 Found {count} cocktails in database")
        
        if count == 0:
            print("❌ No cocktails in database")
            print("Run: python data_processor.py")
            return False
        
        # Check if embeddings exist
        cursor.execute("SELECT COUNT(*) FROM cocktails WHERE embedding IS NOT NULL")
        embedding_count = cursor.fetchone()[0]
        print(f"🧠 {embedding_count} cocktails have embeddings")
        
        # Test a simple query
        cursor.execute("SELECT name FROM cocktails LIMIT 3")
        samples = cursor.fetchall()
        print("📝 Sample cocktails:")
        for sample in samples:
            print(f"  - {sample[0]}")
        
        cursor.close()
        conn.close()
        
        return count > 0 and embedding_count > 0
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_recommender():
    """Test the recommendation engine"""
    print("\n🧠 Testing recommender...")
    
    try:
        from recommender import CocktailRecommender
        recommender = CocktailRecommender()
        
        # Test random cocktails (simplest query)
        print("Testing random cocktails...")
        random_results = recommender.get_random_cocktails(3)
        
        if random_results:
            print(f"✅ Random query returned {len(random_results)} results")
            for result in random_results:
                cocktail = recommender.format_cocktail_result(result)
                print(f"  - {cocktail['name']}")
        else:
            print("❌ Random query returned no results")
            return False
        
        # Test ingredient search
        print("\nTesting ingredient search...")
        ingredient_results = recommender.recommend_by_ingredients(['vodka'], limit=3)
        
        if ingredient_results:
            print(f"✅ Ingredient search returned {len(ingredient_results)} results")
            for result in ingredient_results:
                cocktail = recommender.format_cocktail_result(result)
                print(f"  - {cocktail['name']} (Similarity: {cocktail.get('similarity', 'N/A')}%)")
        else:
            print("❌ Ingredient search returned no results")
        
        return True
        
    except Exception as e:
        print(f"❌ Recommender error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_environment():
    """Check environment variables"""
    print("🔧 Checking environment...")
    
    required_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Hide password
            display_value = "***" if "PASSWORD" in var else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
    else:
        print("❌ .env file not found")
        print("Copy .env.example to .env and configure it")

def check_dataset():
    """Check if dataset exists"""
    print("\n📊 Checking dataset...")
    
    csv_path = "data/cocktails.csv"
    if os.path.exists(csv_path):
        print(f"✅ Dataset found at {csv_path}")
        
        # Check file size
        size = os.path.getsize(csv_path)
        print(f"📏 File size: {size / 1024 / 1024:.1f} MB")
        
        # Try to read first few lines
        try:
            import pandas as pd
            df = pd.read_csv(csv_path, nrows=5)
            print(f"📋 Columns: {list(df.columns)[:5]}...")
            print(f"📈 Sample rows: {len(df)}")
            return True
        except Exception as e:
            print(f"❌ Error reading dataset: {e}")
            return False
    else:
        print(f"❌ Dataset not found at {csv_path}")
        print("Download from: https://www.kaggle.com/datasets/aadyasingh55/cocktails/data")
        return False

def main():
    print("🍹 Cocktail Recommendation System - Debug Tool")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Check dataset
    dataset_ok = check_dataset()
    
    # Check database
    db_ok = check_database()
    
    # Test recommender if database is OK
    if db_ok:
        recommender_ok = test_recommender()
    else:
        recommender_ok = False
    
    print("\n📋 Summary:")
    print(f"Dataset: {'✅' if dataset_ok else '❌'}")
    print(f"Database: {'✅' if db_ok else '❌'}")
    print(f"Recommender: {'✅' if recommender_ok else '❌'}")
    
    if not dataset_ok:
        print("\n💡 Next steps:")
        print("1. Download the cocktail dataset")
        print("2. Place it as data/cocktails.csv")
    elif not db_ok:
        print("\n💡 Next steps:")
        print("1. Configure .env file")
        print("2. Run: python database_setup.py")
        print("3. Run: python data_processor.py")
    elif not recommender_ok:
        print("\n💡 Next steps:")
        print("1. Check the error messages above")
        print("2. Verify database connectivity")
    else:
        print("\n🎉 Everything looks good!")
        print("You can now run: streamlit run app.py")

if __name__ == "__main__":
    main()
