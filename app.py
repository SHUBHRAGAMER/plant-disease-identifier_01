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
# FUTURISTIC DARK UI
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0,255,140,0.10), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(0,255,200,0.08), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(0,255,100,0.07), transparent 30%),
        #050807;

    color: #e8fff1;
}

.block-container {
    max-width: 900px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

/* =========================================================
   REMOVE DEFAULT STREAMLIT UI
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* =========================================================
   ANIMATED BACKGROUND
   ========================================================= */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;

    background-image:
        linear-gradient(rgba(0,255,130,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,130,0.025) 1px, transparent 1px);

    background-size: 45px 45px;

    mask-image: linear-gradient(
        to bottom,
        transparent,
        black 20%,
        black 80%,
        transparent
    );

    pointer-events: none;
}

/* =========================================================
   HERO
   ========================================================= */

.hero {
    text-align: center;
    padding: 35px 10px 30px;
}

.logo-orb {
    width: 92px;
    height: 92px;

    margin: auto;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 48px;

    background:
        radial-gradient(
            circle,
            rgba(0,255,130,0.25),
            rgba(0,255,130,0.03) 65%,
            transparent
        );

    border: 1px solid rgba(0,255,130,0.45);

    box-shadow:
        0 0 20px rgba(0,255,130,0.25),
        0 0 70px rgba(0,255,130,0.10),
        inset 0 0 30px rgba(0,255,130,0.10);

    animation: pulse 3s infinite;
}

@keyframes pulse {

    0%,100% {
        box-shadow:
        0 0 20px rgba(0,255,130,0.25),
        0 0 70px rgba(0,255,130,0.10);
    }

    50% {
        box-shadow:
        0 0 35px rgba(0,255,130,0.45),
        0 0 100px rgba(0,255,130,0.20);
    }
}

.hero-title {

    font-size: 52px;
    font-weight: 900;

    margin-top: 20px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #70ffb0,
        #00ff88,
        #ffffff
    );

    background-size: 300%;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: gradientMove 6s infinite linear;

    letter-spacing: -2px;
}

@keyframes gradientMove {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }
}

.hero-subtitle {

    color: #7ea88d;

    font-size: 16px;

    letter-spacing: 4px;

    text-transform: uppercase;

    margin-top: 8px;
}

/* =========================================================
   STATUS BAR
   ========================================================= */

.status {

    display: flex;

    justify-content: center;

    gap: 10px;

    margin: 15px auto 30px;

    font-size: 12px;

    color: #7d9c88;

}

.status-dot {

    width: 8px;
    height: 8px;

    background: #00ff88;

    border-radius: 50%;

    box-shadow: 0 0 12px #00ff88;

    margin-top: 4px;

}

/* =========================================================
   GLASS CARDS
   ========================================================= */

.glass {

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.015)
        );

    border: 1px solid rgba(100,255,160,0.15);

    border-radius: 24px;

    padding: 28px;

    margin: 18px 0;

    backdrop-filter: blur(20px);

    box-shadow:
        0 20px 70px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.04);

}

/* =========================================================
   SECTION TITLE
   ========================================================= */

.section-title {

    color: #8affb6;

    font-size: 13px;

    font-weight: 800;

    letter-spacing: 3px;

    text-transform: uppercase;

    margin-bottom: 15px;

}

/* =========================================================
   UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {

    background:
        linear-gradient(
            145deg,
            rgba(0,255,130,0.06),
            rgba(0,0,0,0.2)
        );

    border: 1px dashed rgba(0,255,130,0.35);

    border-radius: 18px;

    padding: 10px;

    transition: 0.3s;

}

[data-testid="stFileUploader"]:hover {

    border-color: #00ff88;

    box-shadow:
        0 0 30px rgba(0,255,130,0.12);

}

/* =========================================================
   IMAGE
   ========================================================= */

[data-testid="stImage"] {

    border-radius: 20px;

    overflow: hidden;

}

/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {

    width: 100%;

    height: 58px;

    border-radius: 16px;

    border: 1px solid rgba(0,255,130,0.5);

    background:
        linear-gradient(
            90deg,
            #073d25,
            #08733f,
            #073d25
        );

    color: white;

    font-size: 15px;

    font-weight: 800;

    letter-spacing: 2px;

    box-shadow:
        0 0 20px rgba(0,255,130,0.12);

    transition: all 0.25s;

}

.stButton > button:hover {

    transform: translateY(-2px);

    border-color: #00ff88;

    box-shadow:
        0 0 35px rgba(0,255,130,0.35);

}

/* =========================================================
   RESULT
   ========================================================= */

.result {

    text-align: center;

    padding: 35px 20px;

    border-radius: 25px;

    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(0,255,130,0.15),
            transparent 60%
        ),

        rgba(5,15,9,0.8);

    border: 1px solid rgba(0,255,130,0.30);

    box-shadow:
        0 0 50px rgba(0,255,130,0.08),
        inset 0 0 40px rgba(0,255,130,0.025);

    margin-top: 25px;

}

.result-label {

    color: #62b87f;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 4px;

    text-transform: uppercase;

}

.result-name {

    color: #ffffff;

    font-size: 30px;

    font-weight: 900;

    margin-top: 12px;

}

.result-confidence {

    color: #65ff9f;

    font-size: 22px;

    font-weight: 700;

    margin-top: 10px;

}

/* =========================================================
   SCANNING
   ========================================================= */

.scanning {

    text-align: center;

    padding: 25px;

    color: #71ffa4;

    font-family: monospace;

    letter-spacing: 2px;

}

.scan-line {

    height: 2px;

    width: 100%;

    background: linear-gradient(
        90deg,
        transparent,
        #00ff88,
        transparent
    );

    box-shadow: 0 0 15px #00ff88;

    animation: scan 1.5s infinite;

}

@keyframes scan {

    0% {
        transform: translateX(-100%);
    }

    100% {
        transform: translateX(100%);
    }

}

/* =========================================================
   METRIC CARDS
   ========================================================= */

.metric {

    background: rgba(255,255,255,0.025);

    border: 1px solid rgba(255,255,255,0.07);

    border-radius: 15px;

    padding: 15px;

    text-align: center;

}

.metric-number {

    font-size: 20px;

    font-weight: 800;

    color: #75ffad;

}

.metric-label {

    color: #6f8b78;

    font-size: 11px;

    text-transform: uppercase;

    letter-spacing: 1px;

}

/* =========================================================
   EXPANDERS
   ========================================================= */

[data-testid="stExpander"] {

    background: rgba(255,255,255,0.02);

    border: 1px solid rgba(100,255,160,0.10);

    border-radius: 16px;

}

/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    text-align: center;

    color: #496353;

    font-size: 12px;

    margin-top: 50px;

    letter-spacing: 1px;

}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="logo-orb">
🌿
</div>

<div class="hero-title">
PlantCare AI
</div>

<div class="hero-subtitle">
Neural Plant Intelligence
</div>

<div class="status">
<div class="status-dot"></div>
AI SYSTEM ONLINE
</div>

</div>
""", unsafe_allow_html=True)

# ============================================================
# INTRO CARD
# ============================================================

st.markdown("""
<div class="glass">

<div class="section-title">
🌐 Plant Intelligence System
</div>

<div style="color:#9ab5a2; line-height:1.8;">

Upload a photograph of a plant leaf.
<br>

Our deep-learning model will analyze its visual patterns
and identify the most likely plant health condition.

</div>

</div>
""", unsafe_allow_html=True)

# ============================================================
# MODEL STATS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric">
    <div class="metric-number">38</div>
    <div class="metric-label">Classes</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric">
    <div class="metric-number">70K+</div>
    <div class="metric-label">Training Images</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric">
    <div class="metric-number">AI</div>
    <div class="metric-label">Deep Learning</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# UPLOAD
# ============================================================

st.markdown("""
<div class="glass">

<div class="section-title">
📡 Upload Biological Sample
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your leaf image here",
    type=["jpg", "jpeg", "png"],
    help="Use a clear image of a plant leaf."
)

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# IMAGE + ANALYSIS
# ============================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="SPECIMEN LOADED",
        use_container_width=True
    )

    st.write("")

    if st.button(
        "⚡ INITIATE NEURAL ANALYSIS",
        type="primary",
        use_container_width=True
    ):

        # ====================================================
        # SCANNING ANIMATION
        # ====================================================

        scan_placeholder = st.empty()

        for message in [
            "INITIALIZING VISION ENGINE...",
            "ANALYZING LEAF STRUCTURE...",
            "SCANNING VISUAL FEATURES...",
            "COMPARING NEURAL PATTERNS...",
            "CALCULATING PROBABILITIES..."
        ]:

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

        resized = image.resize((224, 224))

        image_array = np.array(
            resized
        ).astype("float32")

        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # ====================================================
        # PREDICT
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
            predictions[best_index] * 100
        )

        # ====================================================
        # RESULT
        # ====================================================

        st.markdown(
            f"""
            <div class="result">

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

        st.markdown("""
        <div class="glass">

        <div class="section-title">
        📊 Neural Probability Matrix
        </div>

        """, unsafe_allow_html=True)

        for rank, index in enumerate(top_indices):

            disease = class_names[index]

            probability = (
                predictions[index] * 100
            )

            st.write(
                f"**#{rank + 1}  {disease}**"
            )

            st.progress(
                float(predictions[index])
            )

            st.caption(
                f"{probability:.2f}% probability"
            )

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# INFORMATION
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("🧠 HOW THE AI WORKS"):

    st.markdown("""
    **1. Image Input**

    The uploaded leaf image is processed by the application.

    **2. Feature Extraction**

    The neural network analyzes visual patterns in the leaf.

    **3. Classification**

    The model compares the image against 38 learned classes.

    **4. Probability Analysis**

    The system calculates the probability of each class.

    **5. Final Prediction**

    The class with the highest probability is displayed.
    """)

with st.expander("🎯 GET BETTER RESULTS"):

    st.markdown("""
    • Use a clear photograph.

    • Keep the leaf well illuminated.

    • Avoid extreme blur.

    • Keep the main leaf visible.

    • Avoid images containing many overlapping leaves.
    """)

with st.expander("⚠️ IMPORTANT"):

    st.markdown("""
    This AI system is intended for educational and
    demonstration purposes.

    The prediction should not be considered a professional
    agricultural diagnosis.
    """)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

🌿 PLANTCARE AI

<br>

NEURAL PLANT INTELLIGENCE • 38-CLASS MODEL

<br><br>

SYSTEM ONLINE

</div>
""", unsafe_allow_html=True)
