import streamlit as st

from config import APP_NAME, APP_VERSION
from modules.chatbot import chatbot_page
from modules.pdf_summary import pdf_page
from modules.youtube_summary import youtube_page
from modules.image_analysis import image_page
from modules.snake_game import snake_page




st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)

st.sidebar.title(APP_NAME)
st.sidebar.write(f"Version{APP_VERSION}")

page = st.sidebar.radio(
    "Menu",
    [
        "🏠 Home",
        "🤖 Chatbot",
        "📄 PDF Summarizer",
        "🎥 YouTube Summarizer",
        "🖼 Image Analyzer",
        "🐍 Snake Game"
    ]
)


if page == "🏠 Home":

    st.title("🤖 ZenoAI")

    st.subheader("Your Smart AI Assistant")

    st.markdown("---")

    st.success("💬 AI Chatbot")
    st.success("📄 PDF Summarizer (Coming Soon)")
    st.success("🎤 Voice Assistant (Coming Soon)")
    st.success("🖼 Image Analyzer (Coming Soon)")
    st.success("📝 Quiz Generator (Coming Soon)")
    st.success("📊 PPT Generator (Coming Soon)")
    st.success("🐍 Snake Game (Coming Soon)")

elif page == "🤖 Chatbot":

    chatbot_page()
elif page == "📄 PDF Summarizer":
    
    pdf_page() 
    
elif page == "🎥 YouTube Summarizer":    
    youtube_page()

elif page == "🖼 Image Analyzer":
    
    image_page()    

elif page == "🐍 Snake Game":

    snake_page()