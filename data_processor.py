import pandas as pd
from sentence_transformers import SentenceTransformer
from database_setup import DatabaseSetup
import os
from dotenv import load_dotenv

load_dotenv()

class CocktailDataProcessor:
    def __init__(self):
        self.model_name = os.getenv('MODEL_NAME', 'all-MiniLM-L6-v2')
        self.model = SentenceTransformer(self.model_name)
        self.db_setup = DatabaseSetup()
    
    def load_data(self, csv_path):
        """Load cocktail data from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            print(f"Loaded {len(df)} cocktails from {csv_path}")
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def clean_data(self, df):
        """Clean and preprocess the cocktail data"""
        # Remove duplicates
        df = df.drop_duplicates(subset=['strDrink'])
        
        # Fill missing values
        df = df.fillna('')
        
        # Create a combined text for embedding
        df['combined_text'] = (
            df['strDrink'].astype(str) + ' ' +
            df['strCategory'].astype(str) + ' ' +
            df['strAlcoholic'].astype(str) + ' ' +
            df['strGlass'].astype(str) + ' '
        )
        
        # Add ingredients
        ingredient_cols = [col for col in df.columns if col.startswith('strIngredient')]
        for col in ingredient_cols:
            df['combined_text'] += df[col].astype(str) + ' '
        
        # Clean the combined text
        df['combined_text'] = df['combined_text'].str.replace(r'\s+', ' ', regex=True).str.strip()
        
        return df
    
    def generate_embeddings(self, texts):
        """Generate embeddings for the given texts"""
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings
    
    def create_recipe_text(self, row):
        """Create a readable recipe from the row data"""
        recipe = f"Drink: {row.get('strDrink', '')}\n"
        recipe += f"Category: {row.get('strCategory', '')}\n"
        recipe += f"Type: {row.get('strAlcoholic', '')}\n"
        recipe += f"Glass: {row.get('strGlass', '')}\n"
        
        if row.get('strInstructions'):
            recipe += f"Instructions: {row['strInstructions']}\n"
        
        recipe += "Ingredients:\n"
        for i in range(1, 16):  # Assuming max 15 ingredients
            ingredient = row.get(f'strIngredient{i}')
            measure = row.get(f'strMeasure{i}')
            if ingredient and str(ingredient).strip() and str(ingredient).strip() != 'nan':
                if measure and str(measure).strip() and str(measure).strip() != 'nan':
                    recipe += f"- {measure} {ingredient}\n"
                else:
                    recipe += f"- {ingredient}\n"
        
        return recipe
    
    def get_ingredients_list(self, row):
        """Extract ingredients as a comma-separated string"""
        ingredients = []
        for i in range(1, 16):
            ingredient = row.get(f'strIngredient{i}')
            if ingredient and str(ingredient).strip() and str(ingredient).strip() != 'nan':
                ingredients.append(str(ingredient).strip())
        return ', '.join(ingredients)
    
    def store_cocktails(self, df):
        """Store cocktails with embeddings in the database"""
        try:
            conn = self.db_setup.get_connection()
            cursor = conn.cursor()
            
            # Clear existing data
            cursor.execute("DELETE FROM cocktails")
            
            print(f"Generating embeddings for {len(df)} cocktails...")
            # Generate all embeddings at once (much more efficient)
            all_embeddings = self.generate_embeddings(df['combined_text'].tolist())
            
            print("Storing cocktails in database...")
            for idx, (_, row) in enumerate(df.iterrows()):
                # Get pre-computed embedding
                embedding = all_embeddings[idx]
                
                # Prepare data
                name = row.get('strDrink', '')
                ingredients = self.get_ingredients_list(row)
                recipe = self.create_recipe_text(row)
                glass = row.get('strGlass', '')
                category = row.get('strCategory', '')
                iba = row.get('strIBA', '')
                alcoholic = row.get('strAlcoholic', '')
                
                # Insert into database
                cursor.execute("""
                    INSERT INTO cocktails (name, ingredients, recipe, glass, category, iba, alcoholic, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, ingredients, recipe, glass, category, iba, alcoholic, embedding.tolist()))
                
                if (idx + 1) % 100 == 0:
                    print(f"Stored {idx + 1} cocktails...")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Successfully stored {len(df)} cocktails in the database")
            
        except Exception as e:
            print(f"Error storing cocktails: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
    
    def process_and_store(self, csv_path):
        """Complete pipeline to process and store cocktail data"""
        # Load data
        df = self.load_data(csv_path)
        if df is None:
            return
        
        # Clean data
        df = self.clean_data(df)
        
        # Store in database
        self.store_cocktails(df)

if __name__ == "__main__":
    processor = CocktailDataProcessor()
    # Assuming the CSV file is in the data directory
    csv_path = "data/final_cocktails.csv"
    if os.path.exists(csv_path):
        processor.process_and_store(csv_path)
    else:
        print(f"Please download the cocktails dataset and place it at {csv_path}")
        print("Dataset URL: https://www.kaggle.com/datasets/aadyasingh55/cocktails/data")
