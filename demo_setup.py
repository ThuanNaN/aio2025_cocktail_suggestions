#!/usr/bin/env python3
"""
Quick demo setup using sample data
"""

import os
import sys

def setup_demo():
    print("🍹 Setting up demo with sample data...")
    
    # Check if we have the full dataset
    full_dataset = "data/cocktails.csv"
    sample_dataset = "data/sample_cocktails.csv"
    
    dataset_to_use = None
    
    if os.path.exists(full_dataset):
        print(f"✅ Found full dataset: {full_dataset}")
        dataset_to_use = full_dataset
    elif os.path.exists(sample_dataset):
        print(f"✅ Using sample dataset: {sample_dataset}")
        dataset_to_use = sample_dataset
    else:
        print("❌ No dataset found")
        return False
    
    # Set up database
    print("🗄️ Setting up database...")
    try:
        from database_setup import DatabaseSetup
        db_setup = DatabaseSetup()
        db_setup.create_database()
        db_setup.setup_pgvector()
        print("✅ Database setup complete")
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False
    
    # Process data
    print("🧠 Processing cocktail data...")
    try:
        from data_processor import CocktailDataProcessor
        processor = CocktailDataProcessor()
        processor.process_and_store(dataset_to_use)
        print("✅ Data processing complete")
    except Exception as e:
        print(f"❌ Data processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test the system
    print("🧪 Testing the system...")
    try:
        from recommender import CocktailRecommender
        recommender = CocktailRecommender()
        
        # Test random cocktails
        results = recommender.get_random_cocktails(3)
        if results:
            print(f"✅ System test successful - found {len(results)} cocktails")
            for result in results:
                cocktail = recommender.format_cocktail_result(result)
                print(f"  - {cocktail['name']}")
        else:
            print("❌ System test failed - no cocktails returned")
            return False
            
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False
    
    return True

def main():
    print("🚀 Cocktail Demo Setup")
    print("=" * 30)
    
    if setup_demo():
        print("\n🎉 Demo setup complete!")
        print("\nYou can now run:")
        print("  streamlit run app.py")
        print("\nOr test with:")
        print("  python debug.py")
        
        print("\n💡 To use the full dataset:")
        print("1. Download cocktails.csv from Kaggle")
        print("2. Place it in data/cocktails.csv")
        print("3. Run this script again")
    else:
        print("\n❌ Demo setup failed!")
        print("Please check the error messages above")

if __name__ == "__main__":
    main()
