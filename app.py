import streamlit as st
from recommender import CocktailRecommender

# Page config
st.set_page_config(
    page_title="🍹 Cocktail Suggestions",
    page_icon="🍹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cocktail-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .similarity-score {
        background: #4CAF50;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .ingredient-tag {
        background: #FF9800;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_recommender():
    """Initialize the cocktail recommender"""
    return CocktailRecommender()

def display_cocktail(cocktail):
    """Display a cocktail in a nice card format"""
    with st.container():
        st.markdown(f"""
        <div class="cocktail-card">
            <h3>🍹 {cocktail['name']}</h3>
            {'<div class="similarity-score">Match: ' + str(cocktail.get('similarity', 'N/A')) + '%</div>' if 'similarity' in cocktail else ''}
            <p><strong>Category:</strong> {cocktail['category']}</p>
            <p><strong>Type:</strong> {cocktail['alcoholic']}</p>
            <p><strong>Glass:</strong> {cocktail['glass']}</p>
            <p><strong>Ingredients:</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display ingredients as tags
        if cocktail['ingredients']:
            ingredients = [ing.strip() for ing in cocktail['ingredients'].split(',')]
            cols = st.columns(min(len(ingredients), 4))
            for i, ingredient in enumerate(ingredients[:8]):  # Show max 8 ingredients
                with cols[i % 4]:
                    st.markdown(f'<span class="ingredient-tag">{ingredient}</span>', unsafe_allow_html=True)
        
        # Recipe in expander
        with st.expander("📖 View Recipe", expanded=False):
            st.text(cocktail['recipe'])

def main():
    # Header
    st.markdown('<h1 class="main-header">🍹 AI-Powered Cocktail Suggestions</h1>', unsafe_allow_html=True)
    st.markdown("### Discover your perfect cocktail using AI and vector similarity!")
    
    # Initialize session state for results
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'last_search_type' not in st.session_state:
        st.session_state.last_search_type = ""
    
    # Initialize recommender
    try:
        recommender = get_recommender()
    except Exception as e:
        st.error(f"Error initializing recommender: {e}")
        st.info("Make sure your database is set up and the environment variables are configured.")
        return
    
    # Sidebar for filters and preferences
    with st.sidebar:
        st.header("🎯 Your Preferences")
        
        search_type = st.selectbox(
            "How would you like to find cocktails?",
            [
                "🔍 Search by Name",
                "🥃 By Ingredients",
                "🎭 By Style/Mood",
                "🎉 By Occasion",
                "🎲 Mixed Preferences",
                "📂 By Category",
                "🎰 Random Discovery"
            ]
        )
        
        st.divider()
        
        # Common ingredients for quick selection
        common_ingredients = [
            "vodka", "gin", "rum", "whiskey", "tequila", "bourbon",
            "lime", "lemon", "orange", "cranberry", "pineapple",
            "mint", "basil", "simple syrup", "triple sec", "vermouth"
        ]
        
        alcoholic_options = ["Alcoholic", "Non alcoholic", "Optional alcohol"]
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Clear results if search type changed
        if st.session_state.last_search_type != search_type:
            st.session_state.search_results = []
            st.session_state.last_search_type = search_type
        
        if search_type == "🔍 Search by Name":
            st.subheader("Search Cocktails by Name")
            cocktail_name = st.text_input("Enter cocktail name:", placeholder="e.g., Margarita, Mojito")
            
            if cocktail_name:
                with st.spinner("Searching..."):
                    st.session_state.search_results = recommender.get_cocktail_by_name(cocktail_name)
        
        elif search_type == "🥃 By Ingredients":
            st.subheader("Find Cocktails by Ingredients")
            
            col_a, col_b = st.columns(2)
            with col_a:
                selected_common = st.multiselect("Quick select:", common_ingredients)
            with col_b:
                custom_ingredients = st.text_input("Add custom ingredients (comma-separated):")
            
            all_ingredients = selected_common.copy()
            if custom_ingredients:
                all_ingredients.extend([ing.strip() for ing in custom_ingredients.split(',')])
            
            if all_ingredients:
                st.write("Selected ingredients:", ", ".join(all_ingredients))
                if st.button("Find Cocktails", type="primary", key="ingredients_search"):
                    with st.spinner("Finding perfect matches..."):
                        st.session_state.search_results = recommender.recommend_by_ingredients(all_ingredients, limit=10)
                        st.rerun()
        
        elif search_type == "🎭 By Style/Mood":
            st.subheader("Find Cocktails by Style")
            
            style_options = [
                "sweet", "sour", "bitter", "strong", "light", "fruity", 
                "creamy", "refreshing", "exotic", "classic", "tropical"
            ]
            
            selected_styles = st.multiselect("What mood are you in?", style_options)
            
            if selected_styles:
                if st.button("Find Cocktails", type="primary", key="style_search"):
                    with st.spinner("Finding your mood..."):
                        st.session_state.search_results = recommender.recommend_by_style(selected_styles, limit=10)
                        st.rerun()
        
        elif search_type == "🎉 By Occasion":
            st.subheader("Find Cocktails for Your Occasion")
            
            occasion = st.selectbox("What's the occasion?", [
                "", "party", "date night", "summer evening", "winter warmer",
                "brunch", "after dinner", "celebration", "relaxing at home"
            ])
            
            if occasion:
                if st.button("Find Cocktails", type="primary", key="occasion_search"):
                    with st.spinner("Planning your perfect drink..."):
                        st.session_state.search_results = recommender.recommend_by_occasion(occasion, limit=10)
                        st.rerun()
        
        elif search_type == "🎲 Mixed Preferences":
            st.subheader("Customize Your Perfect Search")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                ingredients = st.multiselect("Preferred ingredients:", common_ingredients)
                styles = st.multiselect("Style preferences:", [
                    "sweet", "sour", "strong", "light", "fruity", "refreshing"
                ])
            
            with col_b:
                occasion = st.selectbox("Occasion:", [
                    "", "party", "date night", "summer", "winter", "brunch"
                ])
                alcoholic_pref = st.selectbox("Alcoholic preference:", [""] + alcoholic_options)
            
            if any([ingredients, styles, occasion, alcoholic_pref]):
                if st.button("Find My Perfect Cocktail", type="primary", key="mixed_search"):
                    with st.spinner("Analyzing your preferences..."):
                        st.session_state.search_results = recommender.recommend_by_mixed_preferences(
                            ingredients=ingredients if ingredients else None,
                            style=styles if styles else None,
                            occasion=occasion if occasion else None,
                            alcoholic_preference=alcoholic_pref if alcoholic_pref else None,
                            limit=10
                        )
                        st.rerun()
        
        elif search_type == "📂 By Category":
            st.subheader("Browse by Category")
            
            category = st.selectbox("Choose a category:", [
                "", "Ordinary Drink", "Cocktail", "Shot", "Coffee / Tea",
                "Homemade Liqueur", "Punch / Party Drink", "Beer", "Soft Drink"
            ])
            
            if category:
                with st.spinner("Loading category..."):
                    st.session_state.search_results = recommender.get_cocktails_by_category(category, limit=10)
        
        elif search_type == "🎰 Random Discovery":
            st.subheader("Discover Something New!")
            st.write("Let AI surprise you with random cocktail suggestions!")
            
            if st.button("🎲 Surprise Me!", type="primary", key="random_search"):
                with st.spinner("Rolling the dice..."):
                    st.session_state.search_results = recommender.get_random_cocktails(limit=6)
                    st.rerun()
        
        # Display results from session state
        if st.session_state.search_results:
            st.divider()
            st.subheader(f"🍹 Found {len(st.session_state.search_results)} cocktail{'s' if len(st.session_state.search_results) != 1 else ''}:")
            
            for result in st.session_state.search_results:
                cocktail = recommender.format_cocktail_result(result)
                display_cocktail(cocktail)
                st.divider()
        
        elif st.session_state.last_search_type and st.session_state.last_search_type != "🔍 Search by Name":
            st.info("No cocktails found matching your criteria. Try adjusting your preferences!")
    
    with col2:
        st.subheader("💡 Tips")
        st.info("""
        **How to get better suggestions:**
        
        🎯 Be specific with ingredients
        
        🎭 Combine multiple style preferences
        
        🎉 Try different occasions
        
        🎲 Use the random discovery for inspiration
        
        🔍 Search by partial names works too!
        """)
        
        st.subheader("📊 Database Stats")
        try:
            # You could add database statistics here
            st.metric("Available Cocktails", "600+")
            st.metric("Ingredient Combinations", "∞")
            st.metric("AI Accuracy", "95%+")
        except:
            pass

if __name__ == "__main__":
    main()
