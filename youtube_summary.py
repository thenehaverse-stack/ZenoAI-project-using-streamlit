import os
import streamlit as st
import yt_dlp
import whisper
import ollama

from config import MODEL_NAME


# -----------------------------
# Download YouTube Audio
# -----------------------------
def download_audio(url):
    output_template = "youtube_audio.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    audio_file = "youtube_audio.mp3"

    if not os.path.exists(audio_file):
        raise FileNotFoundError(
            "MP3 file was not created. Please check FFmpeg installation."
        )

    if os.path.getsize(audio_file) == 0:
        raise ValueError("Downloaded audio file is empty.")

    return audio_file


# -----------------------------
# Load Whisper Model
# -----------------------------
@st.cache_resource
def load_model():
    return whisper.load_model("base")


# -----------------------------
# Ask Ollama
# -----------------------------
def ask_llama(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]


# -----------------------------
# Streamlit Page
# -----------------------------
def youtube_page():
    st.title("🎥 YouTube AI Assistant")

    url = st.text_input("Paste YouTube URL")

    if st.button("Generate Transcript"):

        if not url.strip():
            st.warning("Please enter a YouTube URL.")
            return

        try:
            with st.spinner("Downloading Audio..."):
                audio_file = download_audio(url)

            st.success("Audio Downloaded")

            st.write("Audio File:", audio_file)
            st.write("Size:", os.path.getsize(audio_file), "bytes")

            with st.spinner("Transcribing using Whisper..."):
                model = load_model()

                result = model.transcribe(audio_file)

                transcript = result["text"]

            st.success("Transcript Ready")

            st.text_area(
                "Transcript",
                transcript,
                height=250,
            )

            st.session_state["yt_transcript"] = transcript

        except Exception as e:
            st.error(f"Error: {e}")
            return

    if "yt_transcript" in st.session_state:

        if st.button("Generate Summary"):

            with st.spinner("Generating Summary..."):

                prompt = f"""
Summarize this YouTube transcript in simple language.

Transcript:

{st.session_state['yt_transcript']}
"""

                summary = ask_llama(prompt)

            st.subheader("Summary")

            st.write(summary)