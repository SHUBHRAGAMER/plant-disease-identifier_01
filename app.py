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

    /* ================================
       GLOBAL
    ================================= */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 0%,
                rgba(0, 255, 170, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(0, 180, 255, 0.08),
                transparent 30%
            ),
            #050807;
        color: #e9fff7;
    }

    body {
        font-family: Arial, sans-serif;
    }

    /* ================================
       HIDE STREAMLIT UI
    ================================= */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ================================
       HERO
    ================================= */

    .hero {
        text-align: center;
        padding: 35px 10px 25px 10px;
    }

    .hero-icon {
        font-size: 60px;
        filter: drop-shadow(0 0 20px #27e6a0);
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 900;
        letter-spacing: 5px;
        color: #eafff7;
        text-shadow:
            0 0 10px rgba(53, 220, 167, 0.7),
            0 0 30px rgba(53, 220, 167, 0.35);
    }

    .hero-subtitle {
        color: #35dca7;
        letter-spacing: 4px;
        font-size: 13px;
        margin-top: 8px;
    }

    /* ================================
       GLASS CARDS
    ================================= */

    .glass {
        background: rgba(12, 22, 19, 0.82);
        border: 1px solid rgba(53, 220, 167, 0.22);
        border-radius: 18px;
        padding: 25px;
        margin: 18px 0;
        box-shadow:
            0 0 25px rgba(0, 255, 170, 0.06),
            inset 0 0 20px rgba(255,255,255,0.015);
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

    /* ================================
       STATS
    ================================= */

    .stat-card {
        background: linear-gradient(
            145deg,
            rgba(17, 35, 29, 0.95),
            rgba(7, 16, 13, 0.95)
        );
        border: 1px solid rgba(53,220,167,0.20);
        border-radius: 15px;
        padding: 20px 10px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0,255,170,0.04);
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

    /* ================================
       BUTTONS
    ================================= */

    .stButton > button {
        border-radius: 12px !important;
        border: 1px solid rgba(53,220,167,0.35) !important;
        background: linear-gradient(
            135deg,
            #12352b,
            #092019
        ) !important;
        color: #eafff7 !important;
        font-weight: 700 !important;
        min-height: 48px !important;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #35dca7 !important;
        box-shadow:
            0 0 20px rgba(53,220,167,0.25) !important;
        transform: translateY(-1px);
    }

    /* ================================
       UPLOADER
    ================================= */

    [data-testid="stFileUploader"] {
        background: rgba(7, 18, 14, 0.9);
        border: 1px dashed rgba(53,220,167,0.45);
        border-radius: 16px;
        padding: 10px;
    }

    /* ================================
       RESULT
    ================================= */

    .result-card {
        background:
            radial-gradient(
                circle at top right,
                rgba(53,220,167,0.13),
                transparent 40%
            ),
            rgba(8, 20, 16, 0.96);

        border: 1px solid rgba(53,220,167,0.35);
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;

        box-shadow:
            0 0 35px rgba(53,220,167,0.08);
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

    /* ================================
       CARE
    ================================= */

    .care-card {
        background: rgba(9, 21, 17, 0.95);
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

    /* ================================
       SCANNING
    ================================= */

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

    /* ================================
       FOOTER
    ================================= */

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
# CARE GUIDE
# ============================================================

CARE_GUIDE = {

    "Apple___Apple_scab": {
        "title": "🍎 Apple Scab",
        "type": "Fungal disease",
        "care": [
            "Remove infected leaves and fallen debris where practical.",
            "Improve airflow through appropriate pruning.",
            "Keep the area around the tree clean.",
            "Consider resistant apple varieties.",
            "Seek local agricultural guidance for severe disease."
        ]
    },

    "Apple___Black_rot": {
        "title": "🍎 Apple Black Rot",
        "type": "Fungal disease",
        "care": [
            "Remove infected fruit and plant debris.",
            "Prune affected branches where appropriate.",
            "Keep pruning tools clean.",
            "Maintain good tree health.",
            "Seek agricultural guidance for severe infection."
        ]
    },

    "Apple___Cedar_apple_rust": {
        "title": "🍎 Cedar Apple Rust",
        "type": "Fungal disease",
        "care": [
            "Remove infected plant material where practical.",
            "Maintain good airflow around the tree.",
            "Use resistant apple varieties when available.",
            "Manage nearby cedar or juniper hosts where practical.",
            "Seek local agricultural guidance for severe cases."
        ]
    },

    "Apple___healthy": {
        "title": "🍎 Healthy Apple",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Maintain good airflow.",
            "Monitor leaves and fruit regularly."
        ]
    },

    "Blueberry___healthy": {
        "title": "🫐 Healthy Blueberry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Maintain good airflow.",
            "Monitor plants regularly."
        ]
    },

    "Cherry_(including_sour)___Powdery_mildew": {
        "title": "🍒 Cherry Powdery Mildew",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected plant material where practical.",
            "Improve airflow around the plant.",
            "Avoid excessive humidity around foliage.",
            "Avoid overcrowding.",
            "Seek local agricultural guidance for significant infection."
        ]
    },

    "Cherry_(including_sour)___healthy": {
        "title": "🍒 Healthy Cherry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue normal watering and plant care.",
            "Maintain sunlight and airflow.",
            "Inspect leaves and fruit regularly."
        ]
    },

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "title": "🌽 Corn Gray Leaf Spot",
        "type": "Fungal disease",
        "care": [
            "Manage infected crop debris appropriately.",
            "Use crop rotation where practical.",
            "Maintain healthy crop growth.",
            "Consider resistant varieties.",
            "Follow local agricultural recommendations."
        ]
    },

    "Corn_(maize)___Common_rust_": {
        "title": "🌽 Corn Common Rust",
        "type": "Fungal disease",
        "care": [
            "Monitor the crop regularly.",
            "Maintain appropriate water and nutrition.",
            "Use resistant varieties where available.",
            "Avoid unnecessary prolonged leaf wetness.",
            "Seek agricultural guidance for severe problems."
        ]
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "title": "🌽 Corn Northern Leaf Blight",
        "type": "Fungal disease",
        "care": [
            "Manage infected crop debris.",
            "Use crop rotation where appropriate.",
            "Consider resistant varieties.",
            "Maintain good crop health.",
            "Seek agricultural advice for severe infection."
        ]
    },

    "Corn_(maize)___healthy": {
        "title": "🌽 Healthy Corn",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate irrigation and nutrition.",
            "Monitor leaves regularly.",
            "Maintain good crop management."
        ]
    },

    "Grape___Black_rot": {
        "title": "🍇 Grape Black Rot",
        "type": "Fungal disease",
        "care": [
            "Remove infected leaves and fruit where practical.",
            "Remove infected plant debris.",
            "Improve airflow around vines.",
            "Avoid prolonged moisture on foliage.",
            "Seek local agricultural guidance for severe infections."
        ]
    },

    "Grape___Esca_(Black_Measles)": {
        "title": "🍇 Grape Esca / Black Measles",
        "type": "Grape fungal disease",
        "care": [
            "Remove severely affected material where appropriate.",
            "Avoid unnecessary wounds to vines.",
            "Maintain vineyard sanitation.",
            "Use healthy planting material.",
            "Seek professional vineyard guidance."
        ]
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "title": "🍇 Grape Leaf Blight",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves.",
            "Improve airflow around vines.",
            "Avoid prolonged leaf wetness.",
            "Maintain vineyard sanitation.",
            "Seek agricultural guidance for severe disease."
        ]
    },

    "Grape___healthy": {
        "title": "🍇 Healthy Grape",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Maintain appropriate watering and nutrition.",
            "Maintain good airflow.",
            "Inspect leaves and fruit regularly."
        ]
    },

    "Orange___Haunglongbing_(Citrus_greening)": {
        "title": "🍊 Citrus Greening / Huanglongbing",
        "type": "Bacterial disease",
        "care": [
            "There is no simple cure that restores an infected tree.",
            "Use healthy certified planting material.",
            "Monitor and manage insect vectors according to local guidance.",
            "Follow local plant-health recommendations.",
            "Contact an agricultural authority for confirmation."
        ]
    },

    "Peach___Bacterial_spot": {
        "title": "🍑 Peach Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected material where practical.",
            "Avoid unnecessary injury to branches and leaves.",
            "Maintain good airflow.",
            "Use resistant varieties where available.",
            "Seek agricultural guidance for severe infection."
        ]
    },

    "Peach___healthy": {
        "title": "🍑 Healthy Peach",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue normal watering and nutrition.",
            "Maintain sunlight and airflow.",
            "Monitor leaves and fruit."
        ]
    },

    "Pepper,_bell___Bacterial_spot": {
        "title": "🫑 Bell Pepper Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected leaves and fruit.",
            "Avoid handling plants when foliage is wet.",
            "Use clean planting material.",
            "Avoid overhead watering where possible.",
            "Consider resistant varieties."
        ]
    },

    "Pepper,_bell___healthy": {
        "title": "🫑 Healthy Bell Pepper",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Keep foliage dry where practical.",
            "Monitor plants regularly."
        ]
    },

    "Potato___Early_blight": {
        "title": "🥔 Potato Early Blight",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected foliage.",
            "Keep infected debris under control.",
            "Water at the plant base.",
            "Improve airflow.",
            "Use crop rotation where appropriate."
        ]
    },

    "Potato___Late_blight": {
        "title": "🥔 Potato Late Blight",
        "type": "Water mold disease",
        "care": [
            "Remove severely infected material according to local guidance.",
            "Keep foliage as dry as practical.",
            "Avoid overhead irrigation.",
            "Use healthy certified planting material.",
            "Seek agricultural guidance promptly if strongly suspected."
        ]
    },

    "Potato___healthy": {
        "title": "🥔 Healthy Potato",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate irrigation and nutrition.",
            "Use healthy planting material.",
            "Practice crop rotation where appropriate.",
            "Monitor the crop regularly."
        ]
    },

    "Raspberry___healthy": {
        "title": "🫐 Healthy Raspberry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Maintain good airflow.",
            "Provide appropriate water and nutrition.",
            "Remove dead plant material.",
            "Inspect plants regularly."
        ]
    },

    "Soybean___healthy": {
        "title": "🌱 Healthy Soybean",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Maintain appropriate soil moisture.",
            "Maintain appropriate nutrition.",
            "Monitor the crop regularly.",
            "Follow good crop-management practices."
        ]
    },

    "Squash___Powdery_mildew": {
        "title": "🎃 Squash Powdery Mildew",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Improve airflow.",
            "Avoid excessive crowding.",
            "Water at soil level where possible.",
            "Choose resistant varieties when available."
        ]
    },

    "Strawberry___Leaf_scorch": {
        "title": "🍓 Strawberry Leaf Scorch",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves.",
            "Remove plant debris.",
            "Improve airflow.",
            "Avoid excessive leaf wetness.",
            "Maintain appropriate irrigation and nutrition."
        ]
    },

    "Strawberry___healthy": {
        "title": "🍓 Healthy Strawberry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Maintain good airflow.",
            "Remove dead leaves as part of normal care."
        ]
    },

    "Tomato___Bacterial_spot": {
        "title": "🍅 Tomato Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Avoid handling wet foliage.",
            "Water at the base of plants.",
            "Use clean seed and planting material.",
            "Improve airflow."
        ]
    },

    "Tomato___Early_blight": {
        "title": "🍅 Tomato Early Blight",
        "type": "Fungal disease",
        "care": [
            "Remove affected leaves where practical.",
            "Use mulch to reduce soil splash.",
            "Water at the base of the plant.",
            "Improve airflow.",
            "Use crop rotation where appropriate."
        ]
    },

    "Tomato___Late_blight": {
        "title": "🍅 Tomato Late Blight",
        "type": "Water mold disease",
        "care": [
            "Remove severely infected material according to local guidance.",
            "Keep leaves as dry as possible.",
            "Avoid overhead watering.",
            "Improve airflow.",
            "Seek agricultural guidance because late blight can spread rapidly."
        ]
    },

    "Tomato___Leaf_Mold": {
        "title": "🍅 Tomato Leaf Mold",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves.",
            "Increase ventilation.",
            "Reduce prolonged humidity around foliage.",
            "Avoid unnecessary overhead watering.",
            "Use resistant varieties where available."
        ]
    },

    "Tomato___Septoria_leaf_spot": {
        "title": "🍅 Tomato Septoria Leaf Spot",
        "type": "Fungal disease",
        "care": [
            "Remove affected lower leaves.",
            "Water at the plant base.",
            "Use mulch to reduce soil splash.",
            "Improve spacing and airflow.",
            "Use healthy planting material."
        ]
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "title": "🍅 Tomato Two-Spotted Spider Mite",
        "type": "Pest",
        "care": [
            "Inspect the undersides of leaves.",
            "Remove severely affected leaves where practical.",
            "Keep plants appropriately watered.",
            "Encourage natural predators where appropriate.",
            "Seek agricultural guidance for serious infestations."
        ]
    },

    "Tomato___Target_Spot": {
        "title": "🍅 Tomato Target Spot",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves.",
            "Improve airflow.",
            "Avoid prolonged leaf wetness.",
            "Water at the plant base.",
            "Use healthy planting material."
        ]
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "title": "🍅 Tomato Yellow Leaf Curl Virus",
        "type": "Viral disease",
        "care": [
            "There is no direct cure that eliminates the virus.",
            "Remove severely infected plants according to local guidance.",
            "Manage insect vectors using approved local methods.",
            "Use healthy certified planting material.",
            "Use resistant varieties when available."
        ]
    },

    "Tomato___Tomato_mosaic_virus": {
        "title": "🍅 Tomato Mosaic Virus",
        "type": "Viral disease",
        "care": [
            "There is no direct cure for an infected plant.",
            "Remove severely infected plants according to local guidance.",
            "Wash hands after handling suspected infected plants.",
            "Clean and sanitize tools.",
            "Use healthy seed and planting material."
        ]
    },

    "Tomato___healthy": {
        "title": "🍅 Healthy Tomato",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Maintain good airflow.",
            "Monitor leaves and fruit regularly."
        ]
    }
}

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
# INPUT SECTION
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
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG and PNG",
        label_visibility="collapsed"
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
                Allow camera access and photograph the plant leaf
                directly.
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

            <div style="font-size:45px;">🌱</div>

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

    # ========================================================
    # ANALYSIS BUTTON
    # ========================================================

    analyze = st.button(
        "⚡ INITIATE NEURAL ANALYSIS",
        type="primary",
        use_container_width=True
    )

    if analyze:

        # ====================================================
        # SCANNING ANIMATION
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
        # PREPROCESS IMAGE
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
        # MODEL PREDICTION
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
        # RESULT CARD
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
        # HEALTH STATUS
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
        # RECOMMENDED CARE
        # ====================================================

        st.markdown("---")

        st.markdown(
            """
            <div class="section-title">
                🌿 RECOMMENDED CARE
            </div>

            <div class="section-subtitle">
                AI-assisted care guidance based on the detected
                plant condition.
            </div>
            """,
            unsafe_allow_html=True
        )

        # ====================================================
        # CARE CONFIDENCE CHECK
        # ====================================================

        if confidence >= 60:

            if best_class in CARE_GUIDE:

                care_info = CARE_GUIDE[
                    best_class
                ]

                st.markdown(
                    f"""
                    <div class="care-card">

                        <div class="care-title">
                            {care_info["title"]}
                        </div>

                        <div class="care-type">
                            {care_info["type"].upper()}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    "### 🩺 Recommended Actions"
                )

                for item in care_info["care"]:

                    st.markdown(
                        f"""
                        <div class="care-item">
                            🌱 {item}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    "ℹ️ Care information for this condition "
                    "has not been added to the database yet."
                )

        else:

            st.warning(
                "⚠️ The model confidence is below 60%. "
                "Disease-specific care advice is not shown "
                "because the prediction may be unreliable."
            )

            st.info(
                "💡 Try uploading a clearer photograph of "
                "the plant leaf with good lighting."
            )

        # ====================================================
        # DISCLAIMER
        # ====================================================

        st.markdown(
            """
            <div class="glass">

                ⚠️ <strong>IMPORTANT</strong>

                <br><br>

                PlantCare AI provides educational guidance
                based on an AI image-classification model.

                <br><br>

                The prediction is not a professional
                agricultural diagnosis and should not be
                treated as a guaranteed cure.

            </div>
            """,
            unsafe_allow_html=True
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
                    Top five predictions generated by the
                    neural network.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        for rank, index in enumerate(
            top_indices
        ):

            disease = class_names[
                index
            ]

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

# ============================================================
# HOW AI WORKS
# ============================================================

with st.expander(
    "🧠 HOW THE AI WORKS"
):

    st.markdown(
        """
        **1. Image Input**

        The uploaded plant image is received by the
        application.

        **2. Image Preprocessing**

        The image is converted to RGB and resized to
        **224 × 224 pixels**.

        **3. Feature Extraction**

        The neural network analyzes visual patterns
        within the leaf.

        **4. Classification**

        The model compares the image against
        **38 learned classes**.

        **5. Probability Analysis**

        The model generates probabilities for the
        different classes.

        **6. Final Prediction**

        The class with the highest probability becomes
        the primary prediction.
        """
    )

# ============================================================
# BETTER RESULTS
# ============================================================

with st.expander(
    "🎯 GET BETTER RESULTS"
):

    st.markdown(
        """
        • Use a clear photograph.

        • Keep the leaf well illuminated.

        • Avoid extreme blur.

        • Keep the main leaf visible.

        • Avoid images containing many overlapping leaves.

        • Try to photograph the leaf against a simple
          background.

        • Make sure the leaf occupies a reasonable portion
          of the image.
        """
    )

# ============================================================
# IMPORTANT
# ============================================================

with st.expander(
    "⚠️ IMPORTANT"
):

    st.markdown(
        """
        PlantCare AI is an educational AI demonstration.

        The system predicts plant conditions from images,
        but image classification can make mistakes.

        Always verify important plant-health decisions
        with a qualified agricultural professional or
        reliable local agricultural guidance.
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
