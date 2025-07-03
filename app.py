import streamlit as st
import google.generativeai as genai
import os

# Set your Gemini API Key
genai.configure(api_key=st.secrets["API_KEY"])

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_text(text):
    prompt = f"""
    You are a helpful vocabulary assistant. From the following text, extract words that are uncommon or may be considered advanced vocabulary for learners. 
    For each word, provide:
    - Definition
    - Example sentence
    - Synonyms

    Text: {text}
    """
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.set_page_config(page_title="Personalized Vocabulary Builder", page_icon="📚")
st.title("📚 Personalized Vocabulary Builder")

st.write("Paste or type your text below. We'll help you identify and learn new vocabulary words!")

user_input = st.text_area("Enter your text here", height=200)

if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing text with Gemini..."):
            vocab_output = analyze_text(user_input)

        st.success("Vocabulary list generated!")
        st.markdown("### 📖 Vocabulary List")
        st.markdown(vocab_output)

        # Option to save
        if st.button("Save Vocabulary"):
            with open("saved_vocabulary.txt", "a", encoding="utf-8") as f:
                f.write(vocab_output + "\n\n")
            st.success("Vocabulary saved to `saved_vocabulary.txt`")

st.sidebar.header("About")
st.sidebar.info("This app uses Google Gemini API to help you learn new words from any text you provide. 🧠✨")
