import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import json

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# DARK FUTURISTIC THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(0,255,170,0.10), transparent 25%),
        radial-gradient(circle at 85% 15%, rgba(0,180,255,0.08), transparent 25%),
        linear-gradient(135deg, #030609 0%, #07100d 50%, #020508 100%);
    color: #ecfff8;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Hide Streamlit menu/footer */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Main title */

.main-title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    color: #00ffae;
    letter-spacing: 4px;
}

.subtitle {
    text-align: center;
    color: #76948a;
    font-size: 14px;
    letter-spacing: 3px;
    margin-bottom: 35px;
}

/* Cards */

[data-testid="stMetric"] {
    background: rgba(10,20,18,0.75);
    border: 1px solid rgba(0,255,174,0.20);
    border-radius: 16px;
    padding: 15px;
}

[data-testid="stMetricValue"] {
    color: #00ffae;
}

[data-testid="stMetricLabel"] {
    color: #789087;
}

/* Upload */

[data-testid="stFileUploader"] {
    background: rgba(5,15,12,0.85);
    border: 1px dashed rgba(0,255,174,0.5);
    border-radius: 18px;
    padding: 20px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid #00ffae;
    background: rgba(0,255,174,0.08);
    color: #00ffae;
    font-weight: 700;
}

.stButton > button:hover {
    background: rgba(0,255,174,0.18);
    border-color: #00ffae;
}

/* Headings */

h1, h2, h3 {
    color: #ecfff8 !important;
}

h2 {
    border-bottom: 1px solid rgba(0,255,174,0.15);
    padding-bottom: 10px;
}

/* Success box */

[data-testid="stAlert"] {
    border-radius: 15px;
}

/* Progress */

.stProgress > div > div > div > div {
    background-color: #00ffae;
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


# Load
model = load_model()
class_names = load_classes()

# ============================================================
# HERO
# ============================================================

st.markdown(
    '<p class="main-title">🌿 PLANTCARE AI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">INTELLIGENT PLANT DISEASE DETECTION SYSTEM</p>',
    unsafe_allow_html=True
)

# ============================================================
# SYSTEM STATUS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "AI CORE",
        "ONLINE",
        "●"
    )

with c2:
    st.metric(
        "MODEL",
        "READY"
    )

with c3:
    st.metric(
        "DISEASE CLASSES",
        "38"
    )

with c4:
    st.metric(
        "VISION ENGINE",
        "ACTIVE"
    )

st.write("")

# ============================================================
# MAIN LAYOUT
# ============================================================

left, right = st.columns(
    [1.25, 0.75],
    gap="large"
)

# ============================================================
# LEFT
# ============================================================

with left:

    st.header("📡 Scan a Plant")

    st.caption(
        "Upload a clear photograph of a plant leaf "
        "and let PlantCare AI analyze it."
    )

    uploaded_file = st.file_uploader(
        "Upload your plant leaf",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG and PNG"
    )

    if uploaded_file:

        image = Image.open(
            uploaded_file
        ).convert("RGB")

        st.image(
            image,
            caption="Uploaded plant image",
            use_container_width=True
        )

        st.write("")

        # ====================================================
        # PREDICTION
        # ====================================================

        with st.spinner(
            "🧠 PlantCare AI is analyzing your plant..."
        ):

            resized = image.resize(
                (224, 224)
            )

            img_array = np.array(
                resized
            ).astype("float32") / 255.0

            img_array = np.expand_dims(
                img_array,
                axis=0
            )

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

        clean_name = (
            predicted_class
            .replace("___", " — ")
            .replace("_", " ")
        )

        # ====================================================
        # RESULT
        # ====================================================

        st.success("AI analysis completed!")

        st.subheader("🧬 AI Diagnosis")

        st.metric(
            "Detected Condition",
            clean_name
        )

        st.metric(
            "AI Confidence",
            f"{confidence:.2f}%"
        )

        # ====================================================
        # TOP PREDICTIONS
        # ====================================================

        st.subheader("📊 AI Confidence Analysis")

        top_indices = np.argsort(
            predictions
        )[-5:][::-1]

        for index in top_indices:

            name = (
                class_names[index]
                .replace("___", " — ")
                .replace("_", " ")
            )

            score = float(
                predictions[index]
            )

            st.write(
                f"**{name}** — {score * 100:.2f}%"
            )

            st.progress(
                score
            )

    else:

        st.info(
            "🌱 Upload a leaf image to start the AI diagnosis."
        )

# ============================================================
# RIGHT
# ============================================================

with right:

    st.header("⚡ AI Diagnostic Core")

    st.caption(
        "Neural network classification engine"
    )

    st.write("")

    st.metric(
        "Architecture",
        "CNN"
    )

    st.metric(
        "Classification Classes",
        "38"
    )

    st.metric(
        "Image Input",
        "224 × 224"
    )

    st.metric(
        "Inference Mode",
        "Classification"
    )

    st.write("")

    st.header("🧬 Analysis Pipeline")

    st.write(
        "01  📷 Image Acquisition"
    )

    st.write(
        "02  ⚙️ Image Preprocessing"
    )

    st.write(
        "03  🧠 Neural Inference"
    )

    st.write(
        "04  🔬 Disease Classification"
    )

    st.write(
        "05  📊 Confidence Analysis"
    )

    st.write("")

    st.header("⚠️ Important")

    st.warning(
        "PlantCare AI is an educational AI system. "
        "Its predictions should not replace professional "
        "agricultural diagnosis."
    )

# ============================================================
# FOOTER
# ============================================================

st.write("")

st.divider()

st.caption(
    "🌿 PlantCare AI  •  Powered by TensorFlow  •  "
    "AI Plant Disease Detection"
)
