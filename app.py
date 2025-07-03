import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("🗣️ Personalized Vocabulary Builder")
st.markdown("""
Build your vocabulary with AI-powered, personalized suggestions, examples, and quizzes!  
""")

# User inputs
level = st.selectbox("Your English level", ["Beginner", "Intermediate", "Advanced"])
interest = st.text_input("Your topics of interest (e.g., technology, travel, business)", "technology, science")

# Initialize session states
if "saved_words" not in st.session_state:
    st.session_state.saved_words = []

if "current_words" not in st.session_state:
    st.session_state.current_words = ""

# Get new words
if st.button("Get New Words"):
    prompt = f"""
    I am learning English vocabulary. My level is {level}.
    My interests are: {interest}.
    
    Please suggest 5 new words that are useful for me.
    For each word, provide:
    - Meaning in simple language
    - An example sentence
    - 2–3 synonyms
    - A short tip on when to use it
    Present this as a friendly language coach.
    """

    with st.spinner("Getting new words from Gemini..."):
        response = model.generate_content(prompt)
        words_content = response.text

    # Store in session_state
    st.session_state.current_words = words_content
    st.success("Words generated! You can now save them if you'd like.")

# Display current words
if st.session_state.current_words:
    st.subheader("✨ Your New Words")
    st.markdown(st.session_state.current_words)

    if st.button("Save These Words to My List"):
        st.session_state.saved_words.append(st.session_state.current_words)
        st.session_state.current_words = ""  # Clear after saving
        st.success("Words saved to your personal list!")

# Show saved list
st.subheader("📘 My Vocabulary List")
if st.session_state.saved_words:
    for i, entry in enumerate(st.session_state.saved_words, 1):
        with st.expander(f"Words Set {i}"):
            st.markdown(entry)
else:
    st.write("No words saved yet.")

# Generate practice exercise
if st.button("Generate Practice Exercise"):
    prompt = f"""
    I have saved these words: {st.session_state.saved_words}.
    Create a short vocabulary practice exercise or quiz using these words.
    Make it fun and interactive.
    """

    with st.spinner("Creating practice exercise..."):
        response = model.generate_content(prompt)
        exercise = response.text

    st.subheader("📝 Practice Exercise")
    st.markdown(exercise)

st.caption("✨ Built with Python, Streamlit & Gemini API")
