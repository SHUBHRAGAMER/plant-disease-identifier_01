import streamlit as st
import tensorflow as tf
from PIL import Image
import json
import numpy as np

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("plant_disease_model.keras")

@st.cache_data
def load_classes():
    with open("class_names.json", "r") as f:
        return json.load(f)

model = load_model()
class_names = load_classes()

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0,255,170,0.10), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(0,180,255,0.08), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(0,255,120,0.05), transparent 30%),
        #05070b;
    color: #e8fff5;
}

/* Remove default top spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* HERO */

.hero {
    text-align: center;
    padding: 35px 20px 25px;
}

.logo {
    width: 76px;
    height: 76px;
    margin: auto;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 42px;

    background:
        linear-gradient(145deg, #10251d, #07110d);

    border: 1px solid rgba(0,255,170,0.35);

    box-shadow:
        0 0 30px rgba(0,255,170,0.15),
        inset 0 0 20px rgba(0,255,170,0.06);
}

.hero-title {
    margin-top: 18px;
    font-family: 'Orbitron', sans-serif;
    font-size: 44px;
    font-weight: 700;

    background: linear-gradient(
        90deg,
        #ffffff,
        #57ffc4,
        #00eaff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #7d948d;
    font-size: 14px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 8px;
}

/* STATUS BAR */

.status-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 25px 0;
}

.status {
    background: rgba(13,18,25,0.75);
    border: 1px solid rgba(0,255,170,0.15);
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    backdrop-filter: blur(15px);
}

.status-value {
    color: #00ffb0;
    font-family: 'Orbitron';
    font-size: 16px;
    font-weight: 600;
}

.status-label {
    color: #667a75;
    font-size: 10px;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* CARDS */

.card {
    background:
        linear-gradient(
            145deg,
            rgba(19,26,34,0.92),
            rgba(8,13,18,0.92)
        );

    border: 1px solid rgba(0,255,170,0.16);
    border-radius: 18px;
    padding: 25px;

    box-shadow:
        0 15px 50px rgba(0,0,0,0.30);

    margin-bottom: 20px;
}

.card-title {
    font-family: 'Orbitron';
    font-size: 13px;
    color: #00ffb0;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.card-subtitle {
    color: #72837e;
    font-size: 12px;
    margin-top: 7px;
}

/* UPLOAD */

.upload-card {
    border: 1px dashed rgba(0,255,170,0.45);
    background:
        radial-gradient(
            circle at center,
            rgba(0,255,170,0.07),
            transparent 60%
        ),
        rgba(8,15,13,0.85);

    border-radius: 20px;
    padding: 35px 25px;
    text-align: center;
}

.upload-icon {
    font-size: 45px;
    margin-bottom: 10px;
}

.upload-title {
    font-family: 'Orbitron';
    font-size: 20px;
    color: #eafff8;
}

.upload-text {
    color: #6e837c;
    font-size: 12px;
    margin-top: 8px;
}

/* IMAGE */

.preview {
    border-radius: 18px;
    border: 1px solid rgba(0,255,170,0.25);
    box-shadow: 0 0 40px rgba(0,255,170,0.08);
}

/* RESULT */

.result-box {
    padding: 25px;
    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(0,255,170,0.08),
            rgba(0,100,255,0.04)
        );

    border: 1px solid rgba(0,255,170,0.28);
}

.result-label {
    color: #6f8b82;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-name {
    color: #ffffff;
    font-family: 'Orbitron';
    font-size: 25px;
    margin-top: 8px;
}

.confidence {
    color: #00ffb0;
    font-size: 15px;
    margin-top: 10px;
}

/* INFO */

.info-row {
    display: flex;
    justify-content: space-between;
    padding: 11px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.info-name {
    color: #8b9b96;
}

.info-value {
    color: #eafff8;
    font-weight: 600;
}

/* FOOTER */

.footer {
    text-align: center;
    margin-top: 50px;
    color: #40514b;
    font-size: 11px;
}

.footer span {
    color: #00ffb0;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

    <div class="logo">🌿</div>

    <div class="hero-title">
        PLANTCARE AI
    </div>

    <div class="hero-subtitle">
        Intelligent Plant Disease Detection System
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# STATUS
# =========================================================

st.markdown("""
<div class="status-grid">

    <div class="status">
        <div class="status-value">● ONLINE</div>
        <div class="status-label">AI CORE</div>
    </div>

    <div class="status">
        <div class="status-value">READY</div>
        <div class="status-label">MODEL STATUS</div>
    </div>

    <div class="status">
        <div class="status-value">38</div>
        <div class="status-label">DISEASE CLASSES</div>
    </div>

    <div class="status">
        <div class="status-value">AI</div>
        <div class="status-label">VISION ENGINE</div>
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# MAIN COLUMNS
# =========================================================

left, right = st.columns([1.15, 0.85], gap="large")

# =========================================================
# LEFT SIDE
# =========================================================

with left:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            📡 SCAN A PLANT
        </div>

        <div class="card-subtitle">
            Upload a clear photograph of a plant leaf
            and let the neural network analyze it.
        </div>

    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload leaf image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is None:

        st.markdown("""
        <div class="upload-card">

            <div class="upload-icon">🌱</div>

            <div class="upload-title">
                DROP YOUR LEAF IMAGE
            </div>

            <div class="upload-text">
                JPG / JPEG / PNG • Maximum 200 MB
            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Uploaded plant image",
            use_container_width=True
        )

        # =================================================
        # PREDICTION
        # =================================================

        with st.spinner("🧠 AI is analyzing the plant..."):

            img = image.resize((224, 224))

            img_array = np.array(img) / 255.0

            img_array = np.expand_dims(img_array, axis=0)

            predictions = model.predict(
                img_array,
                verbose=0
            )[0]

        predicted_index = int(
            np.argmax(predictions)
        )

        confidence = float(
            predictions[predicted_index]
        ) * 100

        predicted_class = class_names[
            predicted_index
        ]

        # =================================================
        # RESULT
        # =================================================

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box">

            <div class="result-label">
                AI DIAGNOSIS
            </div>

            <div class="result-name">
                {predicted_class.replace("___", " — ").replace("_", " ")}
            </div>

            <div class="confidence">
                Confidence: {confidence:.2f}%
            </div>

        </div>
        """, unsafe_allow_html=True)

        # =================================================
        # TOP PREDICTIONS
        # =================================================

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card-title">
            📊 TOP AI PREDICTIONS
        </div>
        """, unsafe_allow_html=True)

        top_indices = np.argsort(
            predictions
        )[-5:][::-1]

        for idx in top_indices:

            name = class_names[idx]
            score = predictions[idx] * 100

            st.progress(
                float(predictions[idx]),
                text=f"{name.replace('___', ' — ').replace('_', ' ')}   {score:.2f}%"
            )

# =========================================================
# RIGHT SIDE
# =========================================================

with right:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            ⚡ AI DIAGNOSTIC CORE
        </div>

        <div class="card-subtitle">
            Neural network classification engine
        </div>

        <br>

        <div class="info-row">
            <span class="info-name">Architecture</span>
            <span class="info-value">CNN</span>
        </div>

        <div class="info-row">
            <span class="info-name">Classes</span>
            <span class="info-value">38</span>
        </div>

        <div class="info-row">
            <span class="info-name">Input</span>
            <span class="info-value">224 × 224</span>
        </div>

        <div class="info-row">
            <span class="info-name">Mode</span>
            <span class="info-value">Classification</span>
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">

        <div class="card-title">
            🧬 ANALYSIS PIPELINE
        </div>

        <div class="card-subtitle">
            How PlantCare AI processes your image
        </div>

        <br>

        <div class="info-row">
            <span class="info-name">01</span>
            <span class="info-value">Image Acquisition</span>
        </div>

        <div class="info-row">
            <span class="info-name">02</span>
            <span class="info-value">Image Preprocessing</span>
        </div>

        <div class="info-row">
            <span class="info-name">03</span>
            <span class="info-value">Neural Inference</span>
        </div>

        <div class="info-row">
            <span class="info-name">04</span>
            <span class="info-value">Disease Classification</span>
        </div>

        <div class="info-row">
            <span class="info-name">05</span>
            <span class="info-value">Confidence Analysis</span>
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">

        <div class="card-title">
            ⚠️ IMPORTANT
        </div>

        <div class="card-subtitle">
            PlantCare AI is an educational AI system.
            Predictions should not replace professional
            agricultural diagnosis.
        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    🌿 <span>PlantCare AI</span>
    &nbsp;•&nbsp;
    AI-Powered Plant Disease Detection
    &nbsp;•&nbsp;
    Built with TensorFlow + Streamlit
</div>
""", unsafe_allow_html=True)
