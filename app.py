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

    /* ==============================
       GLOBAL
    ============================== */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 10%,
                rgba(20, 255, 170, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 80% 20%,
                rgba(0, 180, 255, 0.07),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #050807 0%,
                #07110d 45%,
                #020403 100%
            );

        color: #eafff5;
    }

    .main .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ==============================
       REMOVE STREAMLIT UI
    ============================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* ==============================
       HERO
    ============================== */

    .hero {
        text-align: center;
        padding: 45px 20px 35px 20px;
        border-radius: 28px;

        background:
            linear-gradient(
                145deg,
                rgba(12, 35, 27, 0.95),
                rgba(4, 15, 11, 0.92)
            );

        border: 1px solid rgba(55, 220, 167, 0.25);

        box-shadow:
            0 0 50px rgba(30, 220, 150, 0.08),
            inset 0 0 40px rgba(30, 220, 150, 0.025);

        margin-bottom: 25px;
    }

    .hero-icon {
        font-size: 55px;
        margin-bottom: 10px;

        filter:
            drop-shadow(
                0 0 18px rgba(53, 220, 167, 0.65)
            );
    }

    .hero-title {
        font-size: 48px;
        font-weight: 900;
        letter-spacing: 5px;

        background:
            linear-gradient(
                90deg,
                #35dca7,
                #8affd2,
                #35dca7
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        text-shadow:
            0 0 30px rgba(53, 220, 167, 0.18);
    }

    .hero-subtitle {
        color: #91b9aa;
        letter-spacing: 5px;
        font-size: 13px;
        margin-top: 8px;
    }

    /* ==============================
       SECTION
    ============================== */

    .section-title {
        color: #62e9bb;
        font-size: 21px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-top: 20px;
    }

    .section-subtitle {
        color: #8ca99e;
        font-size: 14px;
        line-height: 1.7;
        margin-top: 7px;
    }

    /* ==============================
       GLASS CARDS
    ============================== */

    .glass {
        background:
            linear-gradient(
                145deg,
                rgba(15, 34, 27, 0.85),
                rgba(4, 14, 10, 0.85)
            );

        border:
            1px solid rgba(53, 220, 167, 0.18);

        border-radius: 20px;

        padding: 25px;

        margin: 18px 0;

        box-shadow:
            0 12px 45px rgba(0, 0, 0, 0.25),
            inset 0 0 30px rgba(53, 220, 167, 0.025);
    }

    /* ==============================
       STATS
    ============================== */

    .stat-card {
        text-align: center;

        background:
            linear-gradient(
                145deg,
                rgba(13, 35, 27, 0.9),
                rgba(4, 14, 10, 0.9)
            );

        border:
            1px solid rgba(53, 220, 167, 0.16);

        border-radius: 18px;

        padding: 22px 10px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.2);
    }

    .stat-value {
        font-size: 30px;
        font-weight: 900;
        color: #55e7b5;
    }

    .stat-label {
        font-size: 11px;
        color: #76988d;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    /* ==============================
       UPLOAD
    ============================== */

    [data-testid="stFileUploader"] {
        background:
            rgba(8, 22, 16, 0.8);

        border:
            1px dashed rgba(53, 220, 167, 0.45);

        border-radius: 18px;

        padding: 10px;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #35dca7;

        box-shadow:
            0 0 25px rgba(53, 220, 167, 0.08);
    }

    /* ==============================
       BUTTON
    ============================== */

    .stButton > button {
        border-radius: 14px !important;

        border:
            1px solid rgba(53, 220, 167, 0.4) !important;

        background:
            linear-gradient(
                90deg,
                #0d6b51,
                #15906b
            ) !important;

        color: white !important;

        font-weight: 800 !important;

        letter-spacing: 1px;

        min-height: 50px;

        box-shadow:
            0 0 25px rgba(53, 220, 167, 0.12);
    }

    .stButton > button:hover {
        border-color: #63efbf !important;

        box-shadow:
            0 0 30px rgba(53, 220, 167, 0.25);
    }

    /* ==============================
       RESULT
    ============================== */

    .result {
        margin-top: 25px;

        padding: 30px;

        border-radius: 24px;

        text-align: center;

        background:
            radial-gradient(
                circle at center,
                rgba(27, 112, 82, 0.35),
                rgba(5, 17, 12, 0.95)
            );

        border:
            1px solid rgba(53, 220, 167, 0.4);

        box-shadow:
            0 0 50px rgba(53, 220, 167, 0.1);
    }

    .result-label {
        color: #6eeec2;
        font-size: 11px;
        letter-spacing: 3px;
        font-weight: 800;
    }

    .result-name {
        font-size: 27px;
        font-weight: 900;
        margin-top: 14px;
        color: #effff8;
    }

    .result-confidence {
        margin-top: 12px;
        color: #54e8b5;
        font-size: 18px;
        font-weight: 800;
    }

    /* ==============================
       SCANNING
    ============================== */

    .scanning {
        text-align: center;

        padding: 30px;

        margin: 20px 0;

        border-radius: 18px;

        background:
            rgba(5, 25, 17, 0.9);

        border:
            1px solid rgba(53, 220, 167, 0.3);

        color: #62e9bb;

        font-weight: 800;

        letter-spacing: 2px;
    }

    .scan-line {
        height: 2px;

        width: 100%;

        background:
            linear-gradient(
                90deg,
                transparent,
                #35dca7,
                transparent
            );

        box-shadow:
            0 0 15px #35dca7;

        animation: scan 1s infinite;
    }

    @keyframes scan {
        0% {
            opacity: 0.2;
            transform: scaleX(0.4);
        }

        50% {
            opacity: 1;
            transform: scaleX(1);
        }

        100% {
            opacity: 0.2;
            transform: scaleX(0.4);
        }
    }

    /* ==============================
       INFO ROW
    ============================== */

    .info-row {
        display: flex;
        justify-content: space-between;

        padding: 13px 0;

        border-bottom:
            1px solid rgba(255,255,255,0.05);
    }

    .info-name {
        color: #76988d;
    }

    .info-value {
        color: #d9fff0;
        font-weight: 700;
    }

    /* ==============================
       FOOTER
    ============================== */

    .footer {
        text-align: center;

        margin-top: 60px;

        padding: 30px;

        color: #628176;

        font-size: 12px;

        letter-spacing: 2px;
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


# ============================================================
# LOAD CLASS NAMES
# ============================================================

@st.cache_data
def load_classes():

    with open(
        "class_names.json",
        "r"
    ) as f:

        return json.load(f)


# ============================================================
# LOAD AI
# ============================================================

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
            "Remove heavily infected leaves and fallen plant debris.",
            "Keep the area around the tree clean.",
            "Improve air circulation through appropriate pruning.",
            "Choose disease-resistant apple varieties when possible.",
            "Seek local agricultural guidance for severe disease."
        ]
    },

    "Apple___Black_rot": {
        "title": "🍎 Apple Black Rot",
        "type": "Fungal disease",
        "care": [
            "Remove infected fruit, leaves and dead plant material.",
            "Prune affected branches where appropriate.",
            "Keep pruning tools clean.",
            "Remove mummified fruit from the tree.",
            "Seek local agricultural guidance if severe."
        ]
    },

    "Apple___Cedar_apple_rust": {
        "title": "🍎 Cedar-Apple Rust",
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
            "Continue regular watering and appropriate nutrition.",
            "Maintain good airflow around the tree.",
            "Inspect leaves and fruit regularly."
        ]
    },

    "Blueberry___healthy": {
        "title": "🫐 Healthy Blueberry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Maintain good airflow around plants.",
            "Monitor regularly for unusual growth or discoloration."
        ]
    },

    "Cherry_(including_sour)___Powdery_mildew": {
        "title": "🍒 Cherry Powdery Mildew",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected plant material where practical.",
            "Improve airflow around the plant.",
            "Avoid excessive humidity around foliage.",
            "Choose resistant varieties when available.",
            "Seek local agricultural guidance for significant infection."
        ]
    },

    "Cherry_(including_sour)___healthy": {
        "title": "🍒 Healthy Cherry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue normal watering and plant care.",
            "Maintain good sunlight and airflow.",
            "Inspect leaves and fruit regularly."
        ]
    },

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "title": "🌽 Corn Gray Leaf Spot",
        "type": "Fungal disease",
        "care": [
            "Manage infected crop debris where practical.",
            "Maintain good crop airflow.",
            "Use crop rotation where appropriate.",
            "Consider resistant varieties.",
            "Follow local agricultural recommendations."
        ]
    },

    "Corn_(maize)___Common_rust_": {
        "title": "🌽 Corn Common Rust",
        "type": "Fungal disease",
        "care": [
            "Monitor plants regularly.",
            "Maintain healthy plant growth.",
            "Use resistant varieties when available.",
            "Avoid unnecessary prolonged leaf wetness.",
            "Seek agricultural guidance for severe crop problems."
        ]
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "title": "🌽 Corn Northern Leaf Blight",
        "type": "Fungal disease",
        "care": [
            "Manage infected crop debris.",
            "Use crop rotation where appropriate.",
            "Choose resistant varieties.",
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
            "Remove old infected plant material.",
            "Improve airflow around vines.",
            "Avoid prolonged moisture on foliage.",
            "Seek local agricultural guidance for severe infections."
        ]
    },

    "Grape___Esca_(Black_Measles)": {
        "title": "🍇 Grape Esca / Black Measles",
        "type": "Grape fungal disease",
        "care": [
            "Remove severely affected plant material where appropriate.",
            "Avoid unnecessary wounds to grapevines.",
            "Maintain vineyard sanitation.",
            "Use healthy planting material.",
            "Seek professional vineyard advice."
        ]
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "title": "🍇 Grape Leaf Blight",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves and debris.",
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
            "Keep vines supported and ventilated.",
            "Regularly inspect leaves and fruit."
        ]
    },

    "Orange___Haunglongbing_(Citrus_greening)": {
        "title": "🍊 Citrus Greening / Huanglongbing",
        "type": "Bacterial disease",
        "care": [
            "There is no simple cure that restores an infected tree.",
            "Follow local plant-health guidance regarding severely affected trees.",
            "Use certified healthy planting material.",
            "Monitor and manage insect vectors using approved local guidance.",
            "Contact a local agricultural or plant-health authority."
        ]
    },

    "Peach___Bacterial_spot": {
        "title": "🍑 Peach Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected plant material where practical.",
            "Avoid unnecessary injury to branches and leaves.",
            "Maintain good airflow around the tree.",
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
            "Maintain good sunlight and airflow.",
            "Monitor leaves and fruit regularly."
        ]
    },

    "Pepper,_bell___Bacterial_spot": {
        "title": "🫑 Bell Pepper Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected leaves and fruit.",
            "Avoid working with plants while foliage is wet.",
            "Use clean planting material.",
            "Avoid overhead watering where possible.",
            "Use resistant varieties when available."
        ]
    },

    "Pepper,_bell___healthy": {
        "title": "🫑 Healthy Bell Pepper",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Keep foliage dry when practical.",
            "Monitor plants regularly."
        ]
    },

    "Potato___Early_blight": {
        "title": "🥔 Potato Early Blight",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected foliage where practical.",
            "Keep infected plant debris under control.",
            "Water at the base of the plant.",
            "Improve airflow and avoid overcrowding.",
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
            "Remove dead plant material normally.",
            "Inspect plants regularly."
        ]
    },

    "Soybean___healthy": {
        "title": "🌱 Healthy Soybean",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Maintain appropriate soil moisture and nutrition.",
            "Monitor the crop regularly.",
            "Use good crop-management practices."
        ]
    },

    "Squash___Powdery_mildew": {
        "title": "🎃 Squash Powdery Mildew",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Improve airflow around plants.",
            "Avoid excessive crowding.",
            "Water at soil level.",
            "Choose resistant varieties when available."
        ]
    },

    "Strawberry___Leaf_scorch": {
        "title": "🍓 Strawberry Leaf Scorch",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves and debris.",
            "Improve airflow around plants.",
            "Avoid excessive leaf wetness.",
            "Maintain appropriate irrigation and nutrition.",
            "Use healthy planting material."
        ]
    },

    "Strawberry___healthy": {
        "title": "🍓 Healthy Strawberry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Maintain good airflow.",
            "Remove dead leaves during normal maintenance."
        ]
    },

    "Tomato___Bacterial_spot": {
        "title": "🍅 Tomato Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Avoid handling plants while foliage is wet.",
            "Water at the base of plants.",
            "Use clean seed and planting material.",
            "Improve airflow and avoid unnecessary leaf wetness."
        ]
    },

    "Tomato___Early_blight": {
        "title": "🍅 Tomato Early Blight",
        "type": "Fungal disease",
        "care": [
            "Remove affected leaves where practical.",
            "Use mulch to reduce soil splash.",
            "Water at the base of the plant.",
            "Improve spacing and airflow.",
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
            "Improve airflow around plants.",
            "Seek agricultural guidance because late blight can spread rapidly."
        ]
    },

    "Tomato___Leaf_Mold": {
        "title": "🍅 Tomato Leaf Mold",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Increase ventilation and airflow.",
            "Reduce prolonged humidity around foliage.",
            "Avoid unnecessary overhead watering.",
            "Use resistant varieties where available."
        ]
    },

    "Tomato___Septoria_leaf_spot": {
        "title": "🍅 Tomato Septoria Leaf Spot",
        "type": "Fungal disease",
        "care": [
            "Remove affected lower leaves where practical.",
            "Water at the plant base.",
            "Use mulch to reduce soil splash.",
            "Improve spacing and airflow.",
            "Avoid saving seed from severely infected plants."
        ]
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "title": "🍅 Tomato Two-Spotted Spider Mite",
        "type": "Pest",
        "care": [
            "Inspect the undersides of leaves carefully.",
            "Remove severely affected leaves where practical.",
            "Keep plants appropriately watered.",
            "Encourage natural predators where appropriate.",
            "Seek local agricultural guidance for serious infestations."
        ]
    },

    "Tomato___Target_Spot": {
        "title": "🍅 Tomato Target Spot",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Improve airflow around plants.",
            "Avoid prolonged leaf wetness.",
            "Water at the base of the plant.",
            "Use healthy planting material."
        ]
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "title": "🍅 Tomato Yellow Leaf Curl Virus",
        "type": "Viral disease",
        "care": [
            "There is no direct cure that eliminates the virus.",
            "Follow local agricultural guidance for severely infected plants.",
            "Control insect vectors using approved local methods.",
            "Use healthy certified planting material.",
            "Use resistant tomato varieties when available."
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
            "Maintain good airflow around the plant.",
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
            deep-learning model analyze its visual patterns.
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
            <div class="stat-value">38</div>
            <div class="stat-label">DISEASE CLASSES</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-value">70K+</div>
            <div class="stat-label">TRAINING IMAGES</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-value">AI</div>
            <div class="stat-label">DEEP LEARNING</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# INPUT HEADER
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
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        help="Supported formats: JPG, JPEG and PNG",
        label_visibility="collapsed"
    )

    if file_upload is not None:

        uploaded_file = file_upload

        st.success(
            "✅ Image successfully loaded!"
        )


# ============================================================
# CAMERA TAB
# ============================================================

with camera_tab:

    st.markdown(
        """
        <div class="glass">

            <h3>📷 Take a photo</h3>

            <p>
                Allow camera access and photograph the plant leaf directly.
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

        st.success(
            "📸 Photo captured successfully!"
        )


# ============================================================
# ANALYSIS
# ============================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    st.markdown(
        "### 🔬 SPECIMEN PREVIEW"
    )

    st.image(
        image,
        caption="SPECIMEN LOADED",
        use_container_width=True
    )

    st.success(
        "🌿 Ready for neural analysis."
    )

    st.write("")

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


        # ====================================================
        # TOP 5
        # ====================================================

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


        scan_placeholder.empty()


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
        # HEALTH STATUS
        # ====================================================

        if "healthy" in best_class.lower():

            st.success(
                "🟢 HEALTH STATUS: The model predicts "
                "that this plant appears healthy."
            )

        else:

            st.warning(
                "🔴 HEALTH STATUS: A possible plant "
                "disease has been detected."
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
                AI-assisted care guidance based on the detected condition.
            </div>
            """,
            unsafe_allow_html=True
        )


        if confidence >= 60 and best_class in CARE_GUIDE:

            care_info = CARE_GUIDE[
                best_class
            ]

            st.markdown(
                f"""
                <div class="glass">

                    <h2>
                        {care_info["title"]}
                    </h2>

                    <p>
                        <strong>Category:</strong>
                        {care_info["type"]}
                    </p>

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
                    <div class="info-row">

                        <span class="info-value">
                            🌱 {item}
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        elif confidence < 60:

            st.warning(
                "⚠️ The model confidence is below 60%. "
                "Disease-specific care guidance may not be reliable."
            )

            st.info(
                "💡 Try uploading a clearer photograph "
                "with good lighting and the leaf clearly visible."
            )

        else:

            st.info(
                "ℹ️ Care information for this detected "
                "condition is not currently available."
            )


        # ====================================================
        # TOP PREDICTIONS
        # ====================================================

        st.markdown("---")

        st.markdown(
            """
            <div class="glass">

                <div class="section-title">
                    📊 NEURAL PROBABILITY MATRIX
                </div>

                <div class="section-subtitle">
                    Top classifications generated by the neural network.
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
                predictions[index] * 100
            )

            st.write(
                f"**#{rank + 1} — {disease}**"
            )

            st.progress(
                float(
                    predictions[index]
                )
            )

            st.caption(
                f"{probability:.2f}% probability"
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

                It is not a professional agricultural diagnosis
                and should not be treated as a guaranteed cure.

            </div>
            """,
            unsafe_allow_html=True
        )


else:

    st.info(
        "🌱 Upload an image or use your camera to begin."
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
        **01 — Image Input**

        The uploaded plant image is received by PlantCare AI.

        **02 — Image Preprocessing**

        The image is converted to RGB and resized to
        **224 × 224 pixels**.

        **03 — Feature Extraction**

        The neural network analyzes visual patterns
        contained in the image.

        **04 — Classification**

        The model compares the image against its
        **38 learned classes**.

        **05 — Probability Analysis**

        The neural network produces probabilities
        for the possible classes.

        **06 — Final Prediction**

        The class with the highest probability is
        presented as the primary prediction.
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

        • Keep the main leaf clearly visible.

        • Avoid images containing many overlapping leaves.

        • Try to photograph the leaf against a simple background.

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

        Predictions are generated from an image-classification
        model and may be incorrect.

        The result should not replace professional agricultural
        diagnosis or expert advice.
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

        <span style="color:#35dca7;">
            ● SYSTEM ONLINE
        </span>

    </div>
    """,
    unsafe_allow_html=True
)
