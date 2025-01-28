import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
from PIL import Image
import os

# Load the pre-trained model
model = load_model('TILDA_model_efficientNet-B0.h5')

# Class labels for your textile classification
class_labels = ['good', 'hole', 'objects', 'oil spot', 'thread error']  # Adjust based on your model's output

# Function to preprocess and predict the uploaded image
def predict_image(file_path):
    try:
        # Load and preprocess the imagse
        img = load_img(file_path, target_size=(64, 64))  # Ensure this matches the model's input size
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = preprocess_input(img_array)  # Preprocess input using VGG16's method

        # Make a prediction
        predictions = model.predict(img_array)
      #  st.write(f"Raw predictions: {predictions}")  # Debugging: Check raw predictions
        predicted_class = np.argmax(predictions, axis=1)

        # Map the predicted class index to the corresponding label
        return class_labels[predicted_class[0]], predictions
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None, None


# Streamlit app UI
st.title('Textile Classification with TILDA Model')

# Image upload
uploaded_file = st.file_uploader("Choose a textile image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Save the uploaded file locally to use with load_img
    file_path = os.path.join("temp_dir", uploaded_file.name)
    os.makedirs("temp_dir", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display the uploaded image
    img = Image.open(file_path)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Predict the image
    st.write("Classifying... Please wait.")
    class_name, raw_predictions = predict_image(file_path)

    # Display results
    if class_name:
        st.write(f"Prediction: {class_name}")
        #st.write(f"Confidence Scores: {raw_predictions}")
    else:
        st.error("Prediction failed. Please check the uploaded image.")
