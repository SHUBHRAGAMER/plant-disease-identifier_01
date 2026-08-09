import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg, #f7fff8 0%, #ffffff 45%, #f4fff6 100%);
}

/* Main container */
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hero */
.hero {
    text-align: center;
    padding: 20px 10px 25px 10px;
}

.hero-icon {
    font-size: 64px;
    margin-bottom: 5px;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    color: #176b3a;
    margin: 0;
}

.hero-subtitle {
    font-size: 19px;
    color: #5f6f64;
    margin-top: 8px;
}

/* Cards */
.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #dceee2;
    box-shadow: 0 5px 20px rgba(20, 90, 50, 0.06);
    margin: 15px 0;
}

/* Result */
.result-card {
    background: linear-gradient(135deg, #eafff0, #f8fff9);
    padding: 28px;
    border-radius: 22px;
    border: 2px solid #bce8ca;
    text-align: center;
    margin-top: 25px;
}

.result-label {
    font-size: 15px;
    font-weight: 600;
    color: #4c765b;
    letter-spacing: 1px;
}

.result-disease {
    font-size: 28px;
    font-weight: 800;
    color: #145c32;
    margin-top: 8px;
}

.result-confidence {
    font-size: 20px;
    color: #376a49;
    margin-top: 8px;
}

/* Section titles */
.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #185c35;
    margin-top: 25px;
}

/* Footer */
.footer {
    text-align: center;
    color: #718078;
    font-size: 13px;
    margin-top: 45px;
}

/* Hide Streamlit menu/footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    return tf.keras.models.load_model(
        "plant_disease_model.keras"
    )


@st.cache_data
def load_classes():

    with open("class_names.json", "r") as f:
        return json.load(f)


model = load_model()
class_names = load_classes()

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-icon">🌿</div>

<div class="hero-title">
PlantCare AI
</div>

<div class="hero-subtitle">
AI-Powered Plant Disease Detection
</div>

</div>
""", unsafe_allow_html=True)

# ============================================================
# INTRO
# ============================================================

st.markdown("""
<div class="card">

<b>🌱 Welcome to PlantCare AI</b>

<p>
Upload a clear photograph of a plant leaf and our
machine-learning model will analyze its visual features
and predict the most likely plant health condition.
</p>

</div>
""", unsafe_allow_html=True)

# ============================================================
# UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">📷 Upload Your Leaf</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a JPG, JPEG or PNG image",
    type=["jpg", "jpeg", "png"],
    help="For best results, use a clear image containing one main leaf."
)

# ============================================================
# IMAGE + PREDICTION
# ============================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Leaf",
        use_container_width=True
    )

    st.write("")

    detect = st.button(
        "🔍  DETECT DISEASE",
        type="primary",
        use_container_width=True
    )

    if detect:

        with st.spinner("🤖 AI is analyzing the leaf..."):

            # Resize
            resized_image = image.resize((224, 224))

            # Convert to array
            image_array = np.array(
                resized_image
            ).astype("float32")

            image_array = np.expand_dims(
                image_array,
                axis=0
            )

            # Prediction
            predictions = model.predict(
                image_array,
                verbose=0
            )[0]

            # Top 5 predictions
            top_indices = np.argsort(
                predictions
            )[-5:][::-1]

        # ====================================================
        # BEST RESULT
        # ====================================================

        best_index = top_indices[0]

        best_class = class_names[
            best_index
        ]

        confidence = (
            predictions[best_index] * 100
        )

        # ====================================================
        # RESULT CARD
        # ====================================================

        st.markdown(
            f"""
            <div class="result-card">

            <div class="result-label">
            AI ANALYSIS RESULT
            </div>

            <div class="result-disease">
            🌿 {best_class}
            </div>

            <div class="result-confidence">
            🎯 Confidence: <b>{confidence:.2f}%</b>
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ====================================================
        # HEALTH STATUS
        # ====================================================

        if "healthy" in best_class.lower():

            st.success(
                "✅ The AI predicts that this plant appears healthy."
            )

        else:

            st.warning(
                "⚠️ The AI detected a possible plant disease. "
                "Consider checking the plant carefully before "
                "taking any action."
            )

        # ====================================================
        # TOP PREDICTIONS
        # ====================================================

        st.markdown(
            '<div class="section-title">📊 Top Predictions</div>',
            unsafe_allow_html=True
        )

        for index in top_indices:

            disease = class_names[index]

            probability = (
                predictions[index] * 100
            )

            st.write(
                f"**{disease}** — {probability:.2f}%"
            )

            st.progress(
                float(predictions[index])
            )

# ============================================================
# ABOUT
# ============================================================

st.divider()

with st.expander("🤖 About PlantCare AI"):

    st.write(
        "PlantCare AI is an image-classification system "
        "designed to identify 38 different plant health "
        "conditions from leaf images."
    )

    st.write(
        "The model was trained using a large collection "
        "of labeled plant-leaf images and uses deep "
        "learning to recognize visual patterns."
    )

with st.expander("📌 How to Get Better Results"):

    st.write(
        "• Use a clear photograph of the leaf."
    )

    st.write(
        "• Keep the leaf reasonably well lit."
    )

    st.write(
        "• Avoid heavily blurred images."
    )

    st.write(
        "• Try to keep one main leaf visible."
    )

with st.expander("⚠️ Important Disclaimer"):

    st.write(
        "This application provides an AI-based prediction "
        "for educational and demonstration purposes. "
        "It should not replace professional agricultural "
        "diagnosis or advice."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

🌿 PlantCare AI  
AI-Powered Plant Disease Detection

</div>
""", unsafe_allow_html=True)
