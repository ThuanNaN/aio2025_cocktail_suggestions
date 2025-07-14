from sentence_transformers import SentenceTransformer
from database_setup import DatabaseSetup
import os
from dotenv import load_dotenv

load_dotenv()

class CocktailRecommender:
    def __init__(self):
        self.model_name = os.getenv('MODEL_NAME', 'all-MiniLM-L6-v2')
        self.model = SentenceTransformer(self.model_name)
        self.db_setup = DatabaseSetup()
    
    def get_user_preferences_embedding(self, preferences):
        """Generate embedding for user preferences"""
        # Combine all preferences into a single text
        preference_text = ' '.join(preferences)
        embedding = self.model.encode([preference_text])[0]
        return embedding
    
    def search_similar_cocktails(self, query_embedding, limit=10, similarity_threshold=0.3):
        """Search for similar cocktails using vector similarity"""
        try:
            conn = self.db_setup.get_connection()
            cursor = conn.cursor()
            
            # First check if we have any cocktails in the database
            cursor.execute("SELECT COUNT(*) FROM cocktails")
            count = cursor.fetchone()[0]
            print(f"Database contains {count} cocktails")
            
            if count == 0:
                print("Warning: No cocktails found in database. Have you run data_processor.py?")
                cursor.close()
                conn.close()
                return []
            
            # Convert numpy array to list and then to string format for pgvector
            if hasattr(query_embedding, 'tolist'):
                embedding_list = query_embedding.tolist()
            else:
                embedding_list = list(query_embedding)
            
            # Use cosine similarity for search
            cursor.execute("""
                SELECT id, name, ingredients, recipe, glass, category, iba, alcoholic,
                       1 - (embedding <=> %s::vector) as similarity
                FROM cocktails
                WHERE 1 - (embedding <=> %s::vector) > %s
                ORDER BY similarity DESC
                LIMIT %s
            """, (embedding_list, embedding_list, similarity_threshold, limit))
            
            results = cursor.fetchall()
            print(f"Found {len(results)} cocktails with similarity > {similarity_threshold}")
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"Error searching cocktails: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def recommend_by_ingredients(self, ingredients, limit=10):
        """Recommend cocktails based on preferred ingredients"""
        ingredients_text = f"cocktail with {' and '.join(ingredients)}"
        query_embedding = self.get_user_preferences_embedding([ingredients_text])
        return self.search_similar_cocktails(query_embedding, limit)
    
    def recommend_by_style(self, style_preferences, limit=10):
        """Recommend cocktails based on style preferences (sweet, strong, fruity, etc.)"""
        style_text = f"cocktail that is {' and '.join(style_preferences)}"
        query_embedding = self.get_user_preferences_embedding([style_text])
        return self.search_similar_cocktails(query_embedding, limit)
    
    def recommend_by_occasion(self, occasion, limit=10):
        """Recommend cocktails based on occasion"""
        occasion_text = f"cocktail for {occasion}"
        query_embedding = self.get_user_preferences_embedding([occasion_text])
        return self.search_similar_cocktails(query_embedding, limit)
    
    def recommend_by_mixed_preferences(self, ingredients=None, style=None, occasion=None, 
                                     alcoholic_preference=None, limit=10):
        """Recommend cocktails based on mixed preferences"""
        preferences = []
        
        if ingredients:
            preferences.append(f"contains {' and '.join(ingredients)}")
        
        if style:
            preferences.append(f"is {' and '.join(style)}")
        
        if occasion:
            preferences.append(f"perfect for {occasion}")
        
        if alcoholic_preference:
            preferences.append(f"is {alcoholic_preference}")
        
        if not preferences:
            return []
        
        query_embedding = self.get_user_preferences_embedding(preferences)
        return self.search_similar_cocktails(query_embedding, limit)
    
    def get_cocktail_by_name(self, name):
        """Get a specific cocktail by name"""
        try:
            conn = self.db_setup.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, ingredients, recipe, glass, category, iba, alcoholic
                FROM cocktails
                WHERE LOWER(name) LIKE LOWER(%s)
                LIMIT 5
            """, (f'%{name}%',))
            
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"Error searching by name: {e}")
            return []
    
    def get_random_cocktails(self, limit=5):
        """Get random cocktails for discovery"""
        try:
            conn = self.db_setup.get_connection()
            cursor = conn.cursor()
            
            # Check if we have cocktails
            cursor.execute("SELECT COUNT(*) FROM cocktails")
            count = cursor.fetchone()[0]
            print(f"Database contains {count} cocktails")
            
            if count == 0:
                print("Warning: No cocktails found in database. Have you run data_processor.py?")
                cursor.close()
                conn.close()
                return []
            
            cursor.execute("""
                SELECT id, name, ingredients, recipe, glass, category, iba, alcoholic
                FROM cocktails
                ORDER BY RANDOM()
                LIMIT %s
            """, (limit,))
            
            results = cursor.fetchall()
            print(f"Retrieved {len(results)} random cocktails")
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"Error getting random cocktails: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_cocktails_by_category(self, category, limit=10):
        """Get cocktails by category"""
        try:
            conn = self.db_setup.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, ingredients, recipe, glass, category, iba, alcoholic
                FROM cocktails
                WHERE LOWER(category) LIKE LOWER(%s)
                ORDER BY name
                LIMIT %s
            """, (f'%{category}%', limit))
            
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"Error getting cocktails by category: {e}")
            return []
    
    def format_cocktail_result(self, result):
        """Format cocktail result for display"""
        if len(result) == 9:  # With similarity score
            id, name, ingredients, recipe, glass, category, iba, alcoholic, similarity = result
            return {
                'id': id,
                'name': name,
                'ingredients': ingredients,
                'recipe': recipe,
                'glass': glass,
                'category': category,
                'iba': iba,
                'alcoholic': alcoholic,
                'similarity': round(similarity * 100, 1)
            }
        else:  # Without similarity score
            id, name, ingredients, recipe, glass, category, iba, alcoholic = result
            return {
                'id': id,
                'name': name,
                'ingredients': ingredients,
                'recipe': recipe,
                'glass': glass,
                'category': category,
                'iba': iba,
                'alcoholic': alcoholic
            }

if __name__ == "__main__":
    recommender = CocktailRecommender()
    
    # Test the recommender
    print("Testing cocktail recommender...")
    
    # Test ingredient-based recommendation
    results = recommender.recommend_by_ingredients(['vodka', 'lime'], limit=3)
    print(f"\nRecommendations for vodka and lime:")
    for result in results:
        cocktail = recommender.format_cocktail_result(result)
        print(f"- {cocktail['name']} (Similarity: {cocktail.get('similarity', 'N/A')}%)")
    
    # Test random cocktails
    results = recommender.get_random_cocktails(3)
    print(f"\nRandom cocktails:")
    for result in results:
        cocktail = recommender.format_cocktail_result(result)
        print(f"- {cocktail['name']}")
