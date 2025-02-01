import streamlit as st
import os
import base64
import tempfile
from PIL import Image
from textile_core import predict_image
import cv2
from streamlit_option_menu import option_menu


# Helper function to encode image to base64
def _get_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# Set Streamlit page config
st.set_page_config(page_title="Textile Classification", layout="centered")


# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
        padding-top: 100px;
    }

    /* Header Banner */
    .header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #24005e;
        padding: 30px;  
        border-radius: 10px;
        color: white;
        font-size: 24px;  
        font-weight: bold;
        display: flex;
        justify-content: center;  
        align-items: center;
        z-index: 1000;
    }

    .header-title {
        text-align: center;
        color: white;
        font-size: 40px;
        margin-top: 23px;
    }

    .header-logo {
        position: absolute;
        left: 15px;  
        width: 150px;
        margin-top: 30px;
        padding-top: 15px;
    }

    .main-content {
        margin-top: 100px;
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
        z-index: 1000;
    }

    .footer-icons {
        display: flex;
        margin-top:10px;
        position: absolute;
        left: 15px;
        padding-left:100px;
        padding-top:15px;
    }

    .footer-icons img {
        width: 26px;
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


# Webcam classification function
def classify_frame(frame):
    """Process frame and classify using the model."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    cv2.imwrite(temp_file.name, frame)
    class_name, confidence = predict_image(temp_file.name)
    return class_name, confidence


# Sidebar using streamlit_option_menu
with st.sidebar:
    selected_option = option_menu(
        menu_title="Navigation",  # Sidebar title
        options=["Upload Image", "Live Classification"],  # Menu options
        icons=["upload", "camera"],  # Icons for each option
        menu_icon="cast",  # Sidebar menu icon
        default_index=0,  # Default selected option
        styles={
            "nav-link-selected": {"background-color": "#7f00bf"},
            "nav-link": {
                "color": "#24005e",
                "font-size": "16px",
            },
        },
    )

# Main Content Wrapper
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

# Add extra space between title and instruction
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)


# Option 1: Upload Image
if selected_option == "Upload Image":
    
    st.info("📂 Please upload an image to start classification.", icon="📂")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        # Convert uploaded file to OpenCV format
        temp_dir = "temp_dir"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display uploaded image
        img = Image.open(file_path)
        st.image(img,   use_container_width=True)

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

# Option 2: Live Classification
# Option 2: Live Classification
elif selected_option == "Live Classification":
    st.title("🎥 Live Textile Classification")

    # Add start/stop buttons for live classification
    if 'live_classifying' not in st.session_state:
        st.session_state.live_classifying = False  # Initialize the state

    # Button to start the live classification
    start_button = st.button("Start Classification")
    if start_button:
        st.session_state.live_classifying = True  # Start live classification

    # Button to stop the live classification
    stop_button = st.button("Stop Classification")
    if stop_button:
        st.session_state.live_classifying = False  # Stop live classification

    if st.session_state.live_classifying:
        cap = cv2.VideoCapture(0)  # Open webcam
        stframe = st.empty()  # Placeholder for video feed

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture video")
                break

            # Resize frame for consistent processing
            frame_resized = cv2.resize(frame, (64, 64))

            # Predict class
            class_name, confidence = classify_frame(frame_resized)

            # Overlay text on frame
            cv2.putText(frame, f"{class_name} ({confidence:.2f})", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Convert OpenCV image to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame_rgb, channels="RGB", use_container_width=True)

        cap.release()
      #  cv2.destroyAllWindows()

    else:
        st.info("please,Press Start Classification to begin.")



# Close main content wrapper
st.markdown("</div>", unsafe_allow_html=True)

# Footer with Contact Us section
st.markdown(
    f"""
    <div class="footer">
        <p style="margin-bottom:12px;"><strong><u>Contact Us</u></strong></p>
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
            <a href="https://insightmindmatrix.com/" target="_blank" style="color:white;margin-left:70px;"><strong id="about">about us</strong>
                <img src="data:image/png;base64,{_get_image_base64(logo_path)}" style="margin-left: 10px; width:70px; margin-bottom:15px;"> 
            </a>
        </div>
        <p><i>© 2025 Textile Classification App. | All Rights Reserved to Insight Mind Matrix </i></p>
    </div>
    """,
    unsafe_allow_html=True,
)
