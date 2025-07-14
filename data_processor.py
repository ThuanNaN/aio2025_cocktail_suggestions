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
        # Auto-detect column names (handle both old and new formats)
        name_col = 'name' if 'name' in df.columns else 'strDrink'
        category_col = 'category' if 'category' in df.columns else 'strCategory'
        alcoholic_col = 'alcoholic' if 'alcoholic' in df.columns else 'strAlcoholic'
        glass_col = 'glassType' if 'glassType' in df.columns else 'strGlass'
        instructions_col = 'instructions' if 'instructions' in df.columns else 'strInstructions'
        
        print(f"Detected columns: name='{name_col}', category='{category_col}', alcoholic='{alcoholic_col}', glass='{glass_col}'")
        
        # Remove duplicates based on name
        if name_col in df.columns:
            df = df.drop_duplicates(subset=[name_col])
            print(f"After removing duplicates: {len(df)} cocktails")
        
        # Fill missing values
        df = df.fillna('')
        
        # Create a combined text for embedding
        df['combined_text'] = ''
        
        if name_col in df.columns:
            df['combined_text'] += df[name_col].astype(str) + ' '
        if category_col in df.columns:
            df['combined_text'] += df[category_col].astype(str) + ' '
        if alcoholic_col in df.columns:
            df['combined_text'] += df[alcoholic_col].astype(str) + ' '
        if glass_col in df.columns:
            df['combined_text'] += df[glass_col].astype(str) + ' '
        
        # Handle ingredients (could be in different formats)
        if 'ingredients' in df.columns:
            # New format: ingredients as string/list
            df['combined_text'] += df['ingredients'].astype(str) + ' '
        else:
            # Old format: strIngredient1, strIngredient2, etc.
            ingredient_cols = [col for col in df.columns if col.startswith('strIngredient')]
            for col in ingredient_cols:
                df['combined_text'] += df[col].astype(str) + ' '
        
        # Add instructions if available
        if instructions_col in df.columns:
            df['combined_text'] += df[instructions_col].astype(str) + ' '
        
        # Clean the combined text
        df['combined_text'] = df['combined_text'].str.replace(r'\s+', ' ', regex=True).str.strip()
        
        print(f"Sample combined text: {df['combined_text'].iloc[0][:100]}...")
        
        return df
    
    def generate_embeddings(self, texts):
        """Generate embeddings for the given texts"""
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings
    
    def create_recipe_text(self, row):
        """Create a readable recipe from the row data"""
        # Auto-detect column names
        name_col = 'name' if 'name' in row else 'strDrink'
        category_col = 'category' if 'category' in row else 'strCategory'
        alcoholic_col = 'alcoholic' if 'alcoholic' in row else 'strAlcoholic'
        glass_col = 'glassType' if 'glassType' in row else 'strGlass'
        instructions_col = 'instructions' if 'instructions' in row else 'strInstructions'
        
        recipe = f"Drink: {row.get(name_col, '')}\n"
        recipe += f"Category: {row.get(category_col, '')}\n"
        recipe += f"Type: {row.get(alcoholic_col, '')}\n"
        recipe += f"Glass: {row.get(glass_col, '')}\n"
        
        if row.get(instructions_col):
            recipe += f"Instructions: {row[instructions_col]}\n"
        
        recipe += "Ingredients:\n"
        
        # Handle new format (ingredients as string/list)
        if 'ingredients' in row and row['ingredients']:
            try:
                import ast
                ingredients_str = row['ingredients']
                
                # Parse ingredients list
                if ingredients_str.startswith('['):
                    ingredients = ast.literal_eval(ingredients_str)
                else:
                    ingredients = [ingredients_str]
                
                # Parse measures if available
                measures = []
                if 'ingredientMeasures' in row and row['ingredientMeasures']:
                    measures_str = row['ingredientMeasures']
                    if measures_str.startswith('['):
                        measures = ast.literal_eval(measures_str)
                    else:
                        measures = [measures_str]
                
                # Combine ingredients with measures
                for i, ingredient in enumerate(ingredients):
                    if ingredient and str(ingredient).strip() and str(ingredient).strip() != 'None':
                        if i < len(measures) and measures[i] and str(measures[i]).strip() != 'None':
                            recipe += f"- {measures[i]} {ingredient}\n"
                        else:
                            recipe += f"- {ingredient}\n"
                            
            except Exception as e:
                # Fallback: treat as simple string
                recipe += f"- {row['ingredients']}\n"
        
        else:
            # Handle old format (strIngredient1, strIngredient2, etc.)
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
        
        # Handle new format (ingredients as string/list)
        if 'ingredients' in row and row['ingredients']:
            try:
                import ast
                ingredients_str = row['ingredients']
                
                # Parse ingredients list
                if ingredients_str.startswith('['):
                    ingredients_list = ast.literal_eval(ingredients_str)
                    for ingredient in ingredients_list:
                        if ingredient and str(ingredient).strip() and str(ingredient).strip() != 'None':
                            ingredients.append(str(ingredient).strip())
                else:
                    # Single ingredient as string
                    if ingredients_str.strip():
                        ingredients.append(ingredients_str.strip())
                        
            except Exception as e:
                # Fallback: treat as simple string
                if row['ingredients'].strip():
                    ingredients.append(row['ingredients'].strip())
        
        else:
            # Handle old format (strIngredient1, strIngredient2, etc.)
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
                
                # Prepare data with auto-detected column names
                name_col = 'name' if 'name' in row else 'strDrink'
                category_col = 'category' if 'category' in row else 'strCategory'
                alcoholic_col = 'alcoholic' if 'alcoholic' in row else 'strAlcoholic'
                glass_col = 'glassType' if 'glassType' in row else 'strGlass'
                
                name = row.get(name_col, '')
                ingredients = self.get_ingredients_list(row)
                recipe = self.create_recipe_text(row)
                glass = row.get(glass_col, '')
                category = row.get(category_col, '')
                iba = row.get('strIBA', '')  # This might not exist in new format
                alcoholic = row.get(alcoholic_col, '')
                
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
