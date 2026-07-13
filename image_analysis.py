import streamlit as st
from PIL import Image
import ollama
import base64
from io import BytesIO


def image_page():

    st.title("🖼 Image Analyzer")

    uploaded_file = st.file_uploader(
        "Upload an Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        st.image(image, width="stretch")

        st.success("Image Uploaded Successfully ✅")

        if st.button("Analyze Image 🔍"):

            with st.spinner("AI is analyzing image..."):

                # Convert image to base64
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()

                response = ollama.chat(
                    model="llava",
                    messages=[
                        {
                            "role": "user",
                            "content": 
                            "Analyze this image and describe everything you see.",
                            "images": [img_bytes]
                        }
                    ]
                )

                result = response["message"]["content"]

                st.subheader("🤖 AI Analysis:")
                st.write(result)