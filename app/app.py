import streamlit as st
from pipeline import OpeningRecommendationPipeline
from dotenv import load_dotenv


# "centered" keeps the text in a narrower column, which is easier to read than "wide"
st.set_page_config(page_title="Chess Opening Recommender", page_icon="♟️", layout="centered")

load_dotenv()


@st.cache_resource
def load_pipeline():
    return OpeningRecommendationPipeline()

# @st.cache_resource is a Streamlit decorator that caches the result of load_pipeline().
# Streamlit re-runs this whole script every time the user interacts with the page,
# so caching means the vector store and LLM are only loaded once, not on every click.


# A few sample questions the user can click instead of typing from scratch
EXAMPLE_QUERIES = [
    "Aggressive opening for White as a beginner",
    "Solid defense for Black against 1.e4",
    "Positional opening with slow, strategic play",
]


def use_example(example: str):
    # Runs when an example button is clicked: it puts that text into the input box.
    # st.session_state is Streamlit's way of remembering values between re-runs.
    st.session_state["query"] = example


# ---------- Sidebar: short help text ----------
with st.sidebar:
    st.header("How to use")
    st.markdown(
        """
        1. Describe the kind of opening you want.
        2. Click **Get recommendations**.
        3. Read the suggested openings and why they fit you.

        **Tips for better results:**
        - Say if you play **White** or **Black**
        - Mention your level (beginner, intermediate...)
        - Describe your style (aggressive, solid, tricky...)
        """
    )


# ---------- Main page ----------
st.title("♟️ Chess Opening Recommender")
st.caption("Tell me how you like to play, and I'll suggest openings that suit you.")

# Load the pipeline and show a friendly message if it fails (e.g. missing API key)
try:
    with st.spinner("Loading the opening database..."):
        pipeline = load_pipeline()
except Exception as e:
    st.error("Could not start the recommender. Check that your API key is set in the .env file.")
    st.exception(e)
    st.stop()  # stop running the rest of the page

# Example buttons, shown side by side in columns
st.write("**Not sure what to ask? Try one of these:**")
columns = st.columns(len(EXAMPLE_QUERIES))
for column, example in zip(columns, EXAMPLE_QUERIES):
    column.button(example, on_click=use_example, args=(example,), use_container_width=True)

# A form groups the input and the button, so nothing runs until the user clicks Submit
with st.form("query_form"):
    query = st.text_area(
        "What kind of chess opening are you looking for?",
        key="query",  # links this box to st.session_state["query"]
        placeholder="e.g. I'm a beginner who plays Black and likes sharp, attacking games",
        height=100,
    )
    submitted = st.form_submit_button("Get recommendations", type="primary")

if submitted:
    if not query.strip():
        st.warning("Please type a question first.")
    else:
        try:
            with st.spinner("Finding the best openings for you..."):
                response = pipeline.recommend(query)
            st.subheader("Your recommended openings")
            st.markdown(response)
        except Exception as e:
            st.error("Something went wrong while generating recommendations. Please try again.")
            with st.expander("Error details"):
                st.exception(e)
