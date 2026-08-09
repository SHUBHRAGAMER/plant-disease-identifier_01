import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Plant Disease Identifier",
    page_icon="🌱",
    layout="centered"
)

# -----------------------------
# Load model
# -----------------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("plant_disease_model.keras")


@st.cache_data
def load_class_names():
    with open("class_names.json", "r") as f:
        return json.load(f)


model = load_model()
class_names = load_class_names()


# -----------------------------
# Prediction function
# -----------------------------
def predict_disease(image):

    image = image.convert("RGB")
    image = image.resize((224, 224))

    image_array = np.array(image).astype("float32")
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(
        image_array,
        verbose=0
    )[0]

    top_indices = np.argsort(predictions)[-5:][::-1]

    results = {}

    for index in top_indices:
        results[class_names[index]] = float(predictions[index])

    return results


# -----------------------------
# User Interface
# -----------------------------
st.title("🌱 Plant Disease Identifier")

st.write(
    "Upload a photo of a plant leaf and the AI "
    "will identify the most likely disease."
)

st.divider()

uploaded_file = st.file_uploader(
    "📷 Upload a plant leaf image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Leaf",
        use_container_width=True
    )

    if st.button("🔍 Detect Disease", type="primary"):

        with st.spinner("🤖 Analyzing the leaf..."):

            results = predict_disease(image)

        best_prediction = list(results.keys())[0]
        confidence = results[best_prediction] * 100

        st.success(
            f"🌿 Prediction: {best_prediction}"
        )

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        st.divider()

        st.subheader("📊 Top Predictions")

        for disease, probability in results.items():

            st.write(
                f"**{disease}** — "
                f"{probability * 100:.2f}%"
            )

            st.progress(
                float(probability)
            )

st.divider()

st.caption(
    "Plant Disease Identifier • AI Image Classification"
)
