import streamlit as st
import os
import base64
from PIL import Image
from textile_core import predict_image  # Import the core functionality

# Helper function to encode image to base64
def _get_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Set Streamlit page config
st.set_page_config(page_title="Textile Classification", layout="centered")

# Custom CSS for styling
# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
        padding-top: 100px;  /* Push content below fixed header */
    }

    /* Header Banner */
    .header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #24005e;
        padding: 30px;  /* Adjusted padding */
        border-radius: 10px;
        color: white;
        font-size: 24px;  /* Adjusted font size */
        font-weight: bold;
        display: flex;
        justify-content: center;  /* Center the title */
        align-items: center;
        z-index: 1000;  /* Ensures header is always on top */
    }

    .header-title {
        text-align: center;
        color: white;
        font-size: 40px;
        margin-top: 23px;
    }

    .header-logo {
        position: absolute;
        left: 15px;  /* Keeps the logo fixed on the left */
        width: 150px;  /* Adjusted logo size */
        margin-top: 30px;
        padding: 15px;
        
    }

    /* Main Content */
    .main-content {
        margin-top: 100px; /* Push content below header */
    }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #24005e;
        color: white;
        padding: 10px;
        text-align: center;
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 50px;
        z-index: 1000; /* Keeps footer above content */
    }

    .footer-icons {
        display: flex;
        margin-left:-400px;
        margin-top:10px;
    }

    .footer-icons img {
        width: 30px;
        margin-right: 26px;
    }

    .prediction-box {
        width: 60%;
        margin: auto;
        padding: 15px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        color: black;
    }

    .spacer {
        margin-top: 80px;
    }

    .info-box {
        margin-bottom: 0px !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Get the current directory and logo path
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

# Display header with logo and centered title
st.markdown(
    f"""
    <div class="header">
        <img src="data:image/png;base64,{_get_image_base64(logo_path)}" class="header-logo">
        <h1 class="header-title">Textile Classification App</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Main Content Wrapper
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

# Add extra space between title and instruction
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# Instruction for the file uploader
st.info("📂 Please upload an image to start classification.", icon="📂")

# File uploader
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    # Save uploaded file locally
    temp_dir = "temp_dir"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display uploaded image
    img = Image.open(file_path)
    st.image(img, caption="📌 Uploaded Image", use_column_width=True)

    # Classify the image
    st.write(" **Classifying... Please wait.**")
    with st.spinner("⏳ Processing..."):
        try:
            # Prediction
            class_name, confidence = predict_image(file_path)

            # Color map for different classes
            color_map = {
                "Good": "#2ECC71",  # Green
                "Hole": "#F1C40F",  # Yellow
                "Objects": "#E67E22",  # Orange
                "Oil Spot": "#E74C3C",  # Red
                "Thread Error": "#9B59B6"  # Purple
            }

            # Get the color based on the class
            prediction_color = color_map.get(class_name, "#3498DB")  # Default blue

            # Display prediction result in a styled box
            st.markdown(
                f"""
                <div class='prediction-box' style='background-color: {prediction_color};'>
                    🏷️ Prediction: {class_name}
                </div>
                """,
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

# Encode the logo for use in the footer
logo_base64 = _get_image_base64(logo_path)

# Footer with Contact Us section
st.markdown(
    f"""
    <div class="footer">
        <p style="margin:20px 30px;"><strong><u>Contact Us</u></strong></p>
        <div class="footer-icons">
            <a href="https://www.facebook.com/InsightMindMatrix" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook">
            </a>
            <a href="https://www.linkedin.com/company/insight-mind-matrix/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_all%3BQ1SdG%2FXITMCIh1yKZo3YRw%3D%3D" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg" alt="LinkedIn">
            </a>
            <a href="mailto:info@insightmindmatrix.com" target="_blank"style="margin-right:20px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png" alt="Gmail">
            </a>
            </a>
            <!-- Clickable Logo Linking to the Website -->
            <a href="https://insightmindmatrix.com/" target="_blank" style="color:white;"><strong id="about">about us</strong>
                <img src="data:image/png;base64,{logo_base64}" style="margin-left: 10px; width:45px; "> 
            </a>
        </div>
        <p><i>© 2025 Textile Classification App. | All Rights Reserved to Insight Mind Matrix </i></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Close main content wrapper
st.markdown("</div>", unsafe_allow_html=True)
