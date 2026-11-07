import streamlit as st
from pipeline import OpeningRecommendationPipeline
from dotenv import load_dotenv



st.set_page_config(page_title="Chess Opening Recommender", layout="wide")

load_dotenv()

@st.cache_resource
def load_pipeline():
    return OpeningRecommendationPipeline()

#whats exactly happening above is @st.cache_resource is a decorator provided by Streamlit that caches the result of the 
# load_pipeline function. When the function is called, Streamlit checks if it has already been executed with the same parameters.
# If so, it retrieves the cached result instead of running the function again, which improves performance


pipeline = load_pipeline()

st.title("Chess Opening Recommendation System")

query = st.text_input("What kind of chess opening are you looking for?", "")

if query:
    with st.spinner("Generating recommendations..."):
        response = pipeline.recommend(query)
        st.markdown("### Opening recommendations:")
        st.write(response)