import streamlit as st
import tensorflow as tf
import numpy as np
import json
import time
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
# FUTURISTIC DARK UI
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 20% 0%,
                rgba(0,255,170,0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(0,180,255,0.08),
                transparent 30%
            ),
            #050807;
        color: #e9fff7;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    .hero {
        text-align: center;
        padding: 35px 10px 25px;
    }

    .hero-icon {
        font-size: 60px;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 900;
        letter-spacing: 5px;
        color: #eafff7;
        text-shadow:
            0 0 10px rgba(53,220,167,0.7),
            0 0 30px rgba(53,220,167,0.35);
    }

    .hero-subtitle {
        color: #35dca7;
        letter-spacing: 4px;
        font-size: 13px;
        margin-top: 8px;
    }

    .glass {
        background: rgba(12,22,19,0.82);
        border: 1px solid rgba(53,220,167,0.22);
        border-radius: 18px;
        padding: 25px;
        margin: 18px 0;
    }

    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: #eafff7;
        letter-spacing: 1px;
    }

    .section-subtitle {
        color: #8ca9a0;
        font-size: 14px;
        margin-top: 8px;
        line-height: 1.6;
    }

    .stat-card {
        background: rgba(12,30,24,0.95);
        border: 1px solid rgba(53,220,167,0.20);
        border-radius: 15px;
        padding: 20px 10px;
        text-align: center;
    }

    .stat-number {
        font-size: 30px;
        font-weight: 900;
        color: #35dca7;
    }

    .stat-label {
        font-size: 11px;
        color: #829d94;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    .result-card {
        background: rgba(8,20,16,0.96);
        border: 1px solid rgba(53,220,167,0.35);
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
    }

    .result-label {
        font-size: 11px;
        letter-spacing: 3px;
        color: #35dca7;
        font-weight: 700;
    }

    .result-name {
        font-size: 28px;
        font-weight: 900;
        margin-top: 12px;
        color: #f0fff9;
    }

    .result-confidence {
        font-size: 18px;
        margin-top: 12px;
        color: #35dca7;
        font-weight: 800;
    }

    .care-card {
        background: rgba(9,21,17,0.95);
        border: 1px solid rgba(53,220,167,0.20);
        border-radius: 15px;
        padding: 22px;
        margin-top: 15px;
    }

    .care-title {
        font-size: 21px;
        font-weight: 800;
        color: #eafff7;
    }

    .care-type {
        color: #35dca7;
        font-size: 12px;
        letter-spacing: 1px;
        margin-top: 5px;
    }

    .care-item {
        padding: 9px 0;
        color: #c5d9d2;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        line-height: 1.5;
    }

    .scanning {
        text-align: center;
        padding: 30px;
        color: #35dca7;
        font-weight: 800;
        letter-spacing: 2px;
        border: 1px solid rgba(53,220,167,0.25);
        border-radius: 15px;
        background: rgba(5,18,13,0.9);
    }

    .scan-line {
        height: 2px;
        background: #35dca7;
        box-shadow: 0 0 15px #35dca7;
        animation: scan 1s infinite;
    }

    @keyframes scan {
        0% {
            opacity: 0.2;
            transform: scaleX(0.2);
        }

        50% {
            opacity: 1;
            transform: scaleX(1);
        }

        100% {
            opacity: 0.2;
            transform: scaleX(0.2);
        }
    }

    .footer {
        text-align: center;
        padding: 35px 10px;
        color: #6f8980;
        font-size: 12px;
        letter-spacing: 2px;
    }

    .online {
        color: #35dca7;
    }

    </style>
    """,
    unsafe_allow_html=True
)

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
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-icon">🌿</div>

        <div class="hero-title">
            PLANTCARE AI
        </div>

        <div class="hero-subtitle">
            NEURAL PLANT INTELLIGENCE
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# INTRO
# ============================================================

st.markdown(
    """
    <div class="glass">

        <div class="section-title">
            🌱 INTELLIGENT PLANT DIAGNOSTICS
        </div>

        <div class="section-subtitle">
            Upload a photograph of a plant leaf and let the
            deep-learning model analyze its visual patterns
            and identify the most likely plant health condition.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# MODEL STATS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">38</div>
            <div class="stat-label">DISEASE CLASSES</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">70K+</div>
            <div class="stat-label">TRAINING IMAGES</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">AI</div>
            <div class="stat-label">DEEP LEARNING</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# UPLOAD SECTION
# ============================================================

st.markdown(
    """
    <div class="glass">

        <div class="section-title">
            📡 PLANT SPECIMEN INPUT
        </div>

        <div class="section-subtitle">
            Upload an existing image or capture a new image
            directly using your device camera.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# INPUT TABS
# ============================================================

upload_tab, camera_tab = st.tabs(
    [
        "📁 UPLOAD IMAGE",
        "📷 OPEN CAMERA"
    ]
)

uploaded_file = None

# ============================================================
# UPLOAD TAB
# ============================================================

with upload_tab:

    st.markdown(
        """
        <div class="glass">

            <h3>📁 Upload from your device</h3>

            <p>
                Select a clear photograph of the plant leaf.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    file_upload = st.file_uploader(
        "Drop your leaf image here",
        type=["jpg", "jpeg", "png"],
        help="Use a clear image of a plant leaf.",
        label_visibility="visible"
    )

    if file_upload is not None:
        uploaded_file = file_upload


# ============================================================
# CAMERA TAB
# ============================================================

with camera_tab:

    st.markdown(
        """
        <div class="glass">

            <h3>📷 Take a photo</h3>

            <p>
                Allow camera access and photograph the
                plant leaf directly.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    camera_image = st.camera_input(
        "Take a picture of the plant leaf"
    )

    if camera_image is not None:
        uploaded_file = camera_image


# ============================================================
# NO IMAGE
# ============================================================

if uploaded_file is None:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:30px;
            color:#718b82;
        ">

            <div style="font-size:45px;">
                🌱
            </div>

            Upload an image or use your camera to begin.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# IMAGE ANALYSIS
# ============================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    st.markdown(
        """
        <div class="section-title">
            🔬 SPECIMEN PREVIEW
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        image,
        caption="SPECIMEN LOADED",
        use_container_width=True
    )

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#35dca7;
            padding:10px;
        ">
            ● IMAGE READY FOR NEURAL ANALYSIS
        </div>
        """,
        unsafe_allow_html=True
    )

    analyze = st.button(
        "⚡ INITIATE NEURAL ANALYSIS",
        type="primary",
        use_container_width=True
    )

    if analyze:

        # ====================================================
        # SCANNING
        # ====================================================

        scan_placeholder = st.empty()

        messages = [
            "INITIALIZING VISION ENGINE...",
            "ANALYZING LEAF STRUCTURE...",
            "SCANNING VISUAL FEATURES...",
            "COMPARING NEURAL PATTERNS...",
            "CALCULATING PROBABILITIES..."
        ]

        for message in messages:

            scan_placeholder.markdown(
                f"""
                <div class="scanning">

                    {message}

                    <br><br>

                    <div class="scan-line"></div>

                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(0.35)

        # ====================================================
        # PREPROCESS
        # ====================================================

        resized = image.resize(
            (224, 224)
        )

        image_array = np.array(
            resized
        ).astype("float32")

        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # ====================================================
        # PREDICTION
        # ====================================================

        predictions = model.predict(
            image_array,
            verbose=0
        )[0]

        top_indices = np.argsort(
            predictions
        )[-5:][::-1]

        scan_placeholder.empty()

        # ====================================================
        # BEST RESULT
        # ====================================================

        best_index = top_indices[0]

        best_class = class_names[
            best_index
        ]

        confidence = (
            float(predictions[best_index]) * 100
        )

        # ====================================================
        # RESULT
        # ====================================================

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    NEURAL ANALYSIS COMPLETE
                </div>

                <div class="result-name">
                    🌿 {best_class}
                </div>

                <div class="result-confidence">
                    {confidence:.2f}% CONFIDENCE
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ====================================================
        # STATUS
        # ====================================================

        if "healthy" in best_class.lower():

            st.success(
                "🟢 HEALTH STATUS: The model predicts that "
                "this plant appears healthy."
            )

        else:

            st.warning(
                "🔴 HEALTH STATUS: A possible plant disease "
                "has been detected."
            )

        # ====================================================
        # TOP PREDICTIONS
        # ====================================================

        st.markdown(
            """
            <div class="glass">

                <div class="section-title">
                    📊 NEURAL PROBABILITY MATRIX
                </div>

                <div class="section-subtitle">
                    Top five predictions generated by
                    the neural network.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        for rank, index in enumerate(top_indices):

            disease = class_names[index]

            probability = (
                float(predictions[index]) * 100
            )

            st.write(
                f"**#{rank + 1} — {disease}**"
            )

            st.progress(
                float(predictions[index])
            )

            st.caption(
                f"{probability:.2f}% probability"
            )

# ============================================================
# SYSTEM INFORMATION
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="section-title">
        🧠 SYSTEM INFORMATION
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("🧠 HOW THE AI WORKS"):

    st.markdown(
        """
        **1. Image Input**

        The uploaded leaf image is processed by the application.

        **2. Image Preprocessing**

        The image is converted to RGB and resized to
        **224 × 224 pixels**.

        **3. Feature Extraction**

        The neural network analyzes visual patterns in the leaf.

        **4. Classification**

        The model compares the image against 38 learned classes.

        **5. Probability Analysis**

        The system calculates the probability of each class.

        **6. Final Prediction**

        The class with the highest probability is displayed.
        """
    )

with st.expander("🎯 GET BETTER RESULTS"):

    st.markdown(
        """
        • Use a clear photograph.

        • Keep the leaf well illuminated.

        • Avoid extreme blur.

        • Keep the main leaf visible.

        • Avoid images containing many overlapping leaves.

        • Try to photograph the leaf against a simple background.
        """
    )

with st.expander("⚠️ IMPORTANT"):

    st.markdown(
        """
        This AI system is intended for educational and
        demonstration purposes.

        The prediction should not be considered a professional
        agricultural diagnosis.
        """
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        🌿 PLANTCARE AI

        <br><br>

        NEURAL PLANT INTELLIGENCE • 38-CLASS MODEL

        <br><br>

        <span class="online">
            ● SYSTEM ONLINE
        </span>

    </div>
    """,
    unsafe_allow_html=True
)
