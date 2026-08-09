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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# FUTURISTIC DARK UI
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0, 255, 170, 0.10), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(0, 140, 255, 0.10), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(120, 0, 255, 0.08), transparent 35%),
        #05070b;
    color: #f2f7f5;
}

/* Hide default Streamlit elements */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Main container */
.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;
    padding: 35px 20px 25px;
}

.logo {
    font-size: 55px;
    filter: drop-shadow(0 0 18px rgba(0,255,170,.5));
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(36px, 6vw, 70px);
    font-weight: 800;
    letter-spacing: -2px;
    margin: 8px 0 8px;
    background: linear-gradient(
        90deg,
        #ffffff,
        #6affc9,
        #00ff9d,
        #7bdcff,
        #ffffff
    );
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 7s ease infinite;
}

.hero-sub {
    color: #8b9b9a;
    font-size: 16px;
    letter-spacing: 2px;
}

@keyframes gradientMove {
    0% { background-position: 0%; }
    50% { background-position: 100%; }
    100% { background-position: 0%; }
}

/* ============================================================
   STATUS BAR
   ============================================================ */

.status {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin: 10px 0 35px;
}

.status-item {
    padding: 8px 15px;
    border-radius: 999px;
    border: 1px solid rgba(0,255,170,.22);
    background: rgba(0,255,170,.05);
    color: #7fffd4;
    font-size: 12px;
    letter-spacing: .5px;
    box-shadow: 0 0 20px rgba(0,255,170,.04);
}

/* ============================================================
   DASHBOARD CARDS
   ============================================================ */

.card {
    background: linear-gradient(
        145deg,
        rgba(18,24,32,.92),
        rgba(7,11,16,.92)
    );
    border: 1px solid rgba(120,255,210,.13);
    border-radius: 22px;
    padding: 28px;
    box-shadow:
        0 20px 60px rgba(0,0,0,.35),
        inset 0 1px rgba(255,255,255,.035);
    margin-bottom: 20px;
}

.card:hover {
    border-color: rgba(0,255,170,.28);
}

.card-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 6px;
    color: #dffff3;
}

.card-sub {
    color: #70817f;
    font-size: 13px;
    margin-bottom: 20px;
}

/* ============================================================
   UPLOAD AREA
   ============================================================ */

.upload-card {
    background:
        linear-gradient(135deg, rgba(0,255,170,.055), rgba(0,100,255,.035)),
        #080d13;
    border: 1px dashed rgba(0,255,170,.35);
    border-radius: 25px;
    padding: 35px;
    text-align: center;
    margin-bottom: 25px;
}

.upload-icon {
    font-size: 48px;
    margin-bottom: 8px;
    filter: drop-shadow(0 0 15px rgba(0,255,170,.35));
}

.upload-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 22px;
    color: #dffff3;
    margin-bottom: 7px;
}

.upload-text {
    color: #71817e;
    font-size: 13px;
}

/* ============================================================
   RESULT
   ============================================================ */

.result-card {
    background:
        radial-gradient(circle at 0% 0%, rgba(0,255,170,.12), transparent 35%),
        #09100f;
    border: 1px solid rgba(0,255,170,.25);
    border-radius: 25px;
    padding: 30px;
    box-shadow: 0 0 45px rgba(0,255,170,.06);
}

.result-label {
    color: #71817e;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-name {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(24px, 4vw, 42px);
    font-weight: 800;
    color: #72ffca;
    margin: 8px 0;
}

.confidence {
    color: #d8e4e1;
    font-size: 16px;
}

.confidence strong {
    color: #00ff9d;
}

/* ============================================================
   METRICS
   ============================================================ */

.metric {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 16px;
    padding: 18px;
    text-align: center;
}

.metric-number {
    font-family: 'Orbitron', sans-serif;
    font-size: 24px;
    color: #73ffd0;
    font-weight: 700;
}

.metric-label {
    color: #687673;
    font-size: 11px;
    margin-top: 5px;
}

/* ============================================================
   TOP PREDICTIONS
   ============================================================ */

.prediction {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 13px 15px;
    margin: 8px 0;
    border-radius: 13px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.045);
}

.prediction-rank {
    color: #00ff9d;
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    width: 30px;
}

.prediction-name {
    flex: 1;
    color: #d9e3e0;
    font-size: 13px;
}

.prediction-confidence {
    color: #76a89a;
    font-size: 12px;
}

/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 12px !important;
    border: 1px solid rgba(0,255,170,.3) !important;
    background: rgba(0,255,170,.08) !important;
    color: #8affd5 !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background: rgba(0,255,170,.16) !important;
    border-color: rgba(0,255,170,.6) !important;
    box-shadow: 0 0 25px rgba(0,255,170,.12);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(0,0,0,.15);
    border-radius: 15px;
}

/* Images */
[data-testid="stImage"] img {
    border-radius: 18px;
}

/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    margin-top: 50px;
    padding-top: 25px;
    border-top: 1px solid rgba(255,255,255,.05);
    color: #465351;
    font-size: 11px;
    letter-spacing: 1px;
}

.footer span {
    color: #00c987;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("plant_disease_model.keras")


@st.cache_data
def load_classes():
    with open("class_names.json", "r") as f:
        data = json.load(f)

    # Supports either:
    # ["Apple___Apple_scab", ...]
    # OR {"0": "Apple___Apple_scab", ...}

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        try:
            return [data[str(i)] for i in range(len(data))]
        except:
            return list(data.values())

    return data


# ============================================================
# SAFE MODEL LOADING
# ============================================================

try:
    model = load_model()
    class_names = load_classes()
    model_ready = True
except Exception as e:
    model_ready = False
    model_error = str(e)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <div class="logo">🌿</div>

    <div class="hero-title">
        PLANTCARE AI
    </div>

    <div class="hero-sub">
        INTELLIGENT PLANT DISEASE DETECTION SYSTEM
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SYSTEM STATUS
# ============================================================

if model_ready:

    st.markdown("""
    <div class="status">

        <div class="status-item">● AI CORE ONLINE</div>
        <div class="status-item">● MODEL READY</div>
        <div class="status-item">● 38 CLASSES</div>
        <div class="status-item">● IMAGE ANALYSIS READY</div>

    </div>
    """, unsafe_allow_html=True)

else:

    st.error("⚠️ AI model could not be loaded.")

    st.code(model_error)

    st.stop()


# ============================================================
# MAIN LAYOUT
# ============================================================

left, right = st.columns([1.05, 0.95], gap="large")


# ============================================================
# LEFT SIDE — UPLOAD
# ============================================================

with left:

    st.markdown("""
    <div class="upload-card">

        <div class="upload-icon">📡</div>

        <div class="upload-title">
            SCAN A PLANT
        </div>

        <div class="upload-text">
            Upload a clear image of a plant leaf.
            The AI will analyze visual patterns and identify
            the most likely condition.
        </div>

    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload leaf image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Image received by PlantCare AI",
            use_container_width=True
        )


# ============================================================
# RIGHT SIDE — SYSTEM INFO
# ============================================================

with right:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            🧠 AI DIAGNOSTIC CORE
        </div>

        <div class="card-sub">
            Neural network classification engine
        </div>

    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="metric">
            <div class="metric-number">38</div>
            <div class="metric-label">DISEASE CLASSES</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric">
            <div class="metric-number">AI</div>
            <div class="metric-label">VISION ENGINE</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="card">

        <div class="card-title">
            ⚡ ANALYSIS PIPELINE
        </div>

        <div class="card-sub">
            How PlantCare AI processes your image
        </div>

        <p>01 &nbsp; ◉ Image acquisition</p>
        <p>02 &nbsp; ◉ Visual preprocessing</p>
        <p>03 &nbsp; ◉ Neural inference</p>
        <p>04 &nbsp; ◉ Disease classification</p>
        <p>05 &nbsp; ◉ Confidence analysis</p>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PREDICTION
# ============================================================

if uploaded_file:

    st.write("")

    # --------------------------------------------------------
    # PREPROCESS IMAGE
    # --------------------------------------------------------

    img_array = np.array(image)

    # Most PlantVillage-style models use 224x224.
    # Resize according to model input when possible.
    try:
        input_shape = model.input_shape

        if isinstance(input_shape, list):
            input_shape = input_shape[0]

        target_h = input_shape[1] or 224
        target_w = input_shape[2] or 224

    except:
        target_h = 224
        target_w = 224

    resized = image.resize((target_w, target_h))

    img_array = np.array(resized).astype("float32")

    img_array = np.expand_dims(img_array, axis=0)

    # Most standard image classification models expect 0-255
    # images when trained using image_dataset_from_directory.
    # If your model was trained with rescaling, change this to /255.
    prediction = model.predict(img_array, verbose=0)

    probabilities = prediction[0]

    # Softmax if required
    if np.max(probabilities) > 1.0 or abs(np.sum(probabilities) - 1.0) > 0.05:
        probabilities = tf.nn.softmax(probabilities).numpy()

    top_indices = np.argsort(probabilities)[::-1][:5]

    best_index = top_indices[0]

    best_probability = float(probabilities[best_index])

    best_class = class_names[best_index]


    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    st.markdown("""
    <div class="result-card">

        <div class="result-label">
            AI DIAGNOSIS
        </div>

    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="result-name">
            {best_class.replace("___", " — ").replace("_", " ")}
        </div>

        <div class="confidence">
            Confidence score:
            <strong>{best_probability * 100:.2f}%</strong>
        </div>

        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # TOP PREDICTIONS
    # ========================================================

    st.write("")

    st.markdown("""
    <div class="card">

        <div class="card-title">
            📊 TOP AI PREDICTIONS
        </div>

        <div class="card-sub">
            Highest probability classifications generated by the model
        </div>

    """, unsafe_allow_html=True)

    for rank, index in enumerate(top_indices, start=1):

        disease = class_names[index].replace("___", " — ").replace("_", " ")

        confidence = float(probabilities[index]) * 100

        st.markdown(
            f"""
            <div class="prediction">

                <div class="prediction-rank">
                    #{rank}
                </div>

                <div class="prediction-name">
                    {disease}
                </div>

                <div class="prediction-confidence">
                    {confidence:.2f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown("""
<div class="card">

    <div class="card-title">
        ⚠️ IMPORTANT
    </div>

    <div class="card-sub">
        PlantCare AI is an educational AI system.
    </div>

    <div style="color:#687673; font-size:13px; line-height:1.7;">
        Predictions are generated from visual patterns learned
        from the training dataset. For real agricultural decisions,
        consult a qualified agricultural professional.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <span>PLANTCARE AI</span>
    &nbsp; • &nbsp;
    NEURAL VISION SYSTEM
    &nbsp; • &nbsp;
    BUILT WITH TENSORFLOW + STREAMLIT

</div>
""", unsafe_allow_html=True)
