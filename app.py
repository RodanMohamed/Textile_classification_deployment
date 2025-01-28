import streamlit as st
import os
from PIL import Image
from textile_core import predict_image  # Import the core functionality

# Set Streamlit page config
st.set_page_config(page_title="Textile Classification", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and instructions
st.markdown(
    "<h2 style='text-align: center;'>Textile Classification App</h2>",
    unsafe_allow_html=True,
)

# File uploader
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Save the uploaded file locally
    file_path = os.path.join("temp_dir", uploaded_file.name)
    os.makedirs("temp_dir", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display the uploaded image
    img = Image.open(file_path)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Predict the image
    st.write("Classifying... Please wait.")
    try:
        class_name, confidence = predict_image(file_path)
        st.markdown(
            f"<h3 style='text-align: center;'>Prediction: {class_name}</h3>",
            unsafe_allow_html=True,
        )
       # st.markdown(
        #    f"<h4 style='text-align: center;'>Confidence: {confidence * 100:.2f}%</h4>",
         #   unsafe_allow_html=True,
        #)
    except Exception as e:
        st.error(f"Prediction failed: {e}")
else:
    st.info("Please upload an image to start classification.")
