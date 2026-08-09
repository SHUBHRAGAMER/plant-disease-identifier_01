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

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(0,255,170,0.08), transparent 25%),
            radial-gradient(circle at 85% 20%, rgba(0,150,255,0.08), transparent 25%),
            linear-gradient(135deg, #030807 0%, #06110e 45%, #020505 100%);
        color: #e8fff7;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- TEXT ---------- */

    h1, h2, h3, p, label {
        color: #e8fff7 !important;
    }

    /* ---------- HERO ---------- */

    .hero {
        text-align: center;
        padding: 45px 20px 35px 20px;
        border: 1px solid rgba(0,255,180,0.18);
        border-radius: 28px;
        background:
            linear-gradient(
                145deg,
                rgba(8,30,25,0.92),
                rgba(3,12,10,0.75)
            );
        box-shadow:
            0 0 60px rgba(0,255,170,0.06),
            inset 0 0 40px rgba(0,255,170,0.025);
        margin-bottom: 28px;
    }

    .hero-icon {
        font-size: 65px;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 18px rgba(0,255,170,0.5));
    }

    .hero-title {
        font-size: 48px;
        font-weight: 900;
        letter-spacing: 6px;
        color: #dffff4;
        text-shadow: 0 0 25px rgba(0,255,170,0.35);
    }

    .hero-subtitle {
        margin-top: 8px;
        font-size: 15px;
        letter-spacing: 5px;
        color: #61e8bd;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-top: 28px;
        color: #baffea;
    }

    .section-subtitle {
        color: #86aaa1;
        margin-top: 6px;
        margin-bottom: 20px;
        font-size: 15px;
    }

    /* ---------- GLASS ---------- */

    .glass {
        background: rgba(8,24,20,0.72);
        border: 1px solid rgba(0,255,180,0.15);
        border-radius: 20px;
        padding: 24px;
        margin: 12px 0;
        box-shadow:
            0 10px 35px rgba(0,0,0,0.25),
            inset 0 0 25px rgba(0,255,180,0.025);
    }

    /* ---------- STATS ---------- */

    .stat-card {
        text-align: center;
        padding: 22px 10px;
        border-radius: 18px;
        background: linear-gradient(
            145deg,
            rgba(10,35,29,0.9),
            rgba(4,16,13,0.9)
        );
        border: 1px solid rgba(0,255,180,0.13);
        box-shadow: 0 0 25px rgba(0,255,170,0.04);
    }

    .stat-card h2 {
        margin: 0;
        font-size: 32px;
        color: #68f2c3 !important;
    }

    .stat-card p {
        margin: 5px 0 0 0;
        font-size: 11px;
        letter-spacing: 2px;
        color: #779b92 !important;
    }

    /* ---------- UPLOAD ---------- */

    [data-testid="stFileUploader"] {
        background: rgba(4,18,15,0.65);
        border: 1px dashed rgba(0,255,180,0.3);
        border-radius: 18px;
        padding: 12px;
    }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        border-radius: 14px;
        min-height: 52px;
        font-weight: 800;
        letter-spacing: 1px;
        border: 1px solid rgba(0,255,180,0.3);
        background: linear-gradient(
            135deg,
            #063d2d,
            #08734f
        );
        color: white;
        box-shadow: 0 0 25px rgba(0,255,170,0.1);
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #54f5c0;
        box-shadow: 0 0 30px rgba(0,255,170,0.25);
        transform: translateY(-1px);
    }

    /* ---------- RESULT ---------- */

    .result {
        margin-top: 28px;
        padding: 32px;
        border-radius: 24px;
        text-align: center;
        background:
            radial-gradient(
                circle at center,
                rgba(0,255,170,0.12),
                transparent 65%
            ),
            rgba(5,25,20,0.9);
        border: 1px solid rgba(0,255,180,0.28);
        box-shadow:
            0 0 45px rgba(0,255,170,0.08),
            inset 0 0 30px rgba(0,255,170,0.025);
    }

    .result-label {
        color: #62eabd;
        font-size: 12px;
        letter-spacing: 3px;
        font-weight: 700;
    }

    .result-name {
        margin-top: 15px;
        font-size: 30px;
        font-weight: 900;
        color: white;
    }

    .result-confidence {
        margin-top: 12px;
        font-size: 22px;
        font-weight: 800;
        color: #69f5c5;
    }

    /* ---------- SCANNER ---------- */

    .scanning {
        text-align: center;
        padding: 28px;
        border-radius: 18px;
        border: 1px solid rgba(0,255,180,0.25);
        background: rgba(0,30,22,0.8);
        color: #69f5c5;
        font-weight: 800;
        letter-spacing: 2px;
        box-shadow: 0 0 30px rgba(0,255,170,0.08);
    }

    .scan-line {
        height: 2px;
        width: 100%;
        background: #55efbc;
        box-shadow: 0 0 15px #55efbc;
    }

    /* ---------- CARE ---------- */

    .care-box {
        background: linear-gradient(
            145deg,
            rgba(8,35,28,0.9),
            rgba(3,17,14,0.9)
        );
        border: 1px solid rgba(0,255,180,0.2);
        border-radius: 22px;
        padding: 28px;
        margin-top: 15px;
    }

    .care-title {
        font-size: 25px;
        font-weight: 900;
        color: #8ff8d3;
    }

    .care-type {
        color: #72988f;
        margin-top: 5px;
        margin-bottom: 18px;
    }

    .care-item {
        padding: 12px 14px;
        margin: 8px 0;
        border-radius: 12px;
        background: rgba(0,255,170,0.035);
        border-left: 3px solid #36dca7;
        color: #d8eee8;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        margin-top: 55px;
        padding: 28px;
        color: #5d8278;
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
            "Remove affected leaves and fallen infected debris where practical.",
            "Improve airflow through appropriate pruning.",
            "Keep the area around the tree clean.",
            "Use disease-resistant varieties when available.",
            "For severe cases, seek local agricultural guidance."
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
            "Seek local agricultural guidance for severe disease."
        ]
    },

    "Apple___Cedar_apple_rust": {
        "title": "🍎 Cedar-Apple Rust",
        "type": "Fungal disease",
        "care": [
            "Remove infected plant material where practical.",
            "Maintain good airflow around the tree.",
            "Use resistant varieties when available.",
            "Manage nearby cedar or juniper hosts where appropriate.",
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
            "Continue normal watering and nutrition.",
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
            "Choose resistant varieties when available.",
            "Maintain good crop health.",
            "Follow local agricultural recommendations."
        ]
    },

    "Corn_(maize)___Common_rust_": {
        "title": "🌽 Corn Common Rust",
        "type": "Fungal disease",
        "care": [
            "Monitor the crop regularly.",
            "Maintain appropriate water and nutrition.",
            "Use resistant varieties when available.",
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
            "Choose resistant varieties.",
            "Maintain good crop health.",
            "Seek local agricultural guidance for severe infection."
        ]
    },

    "Corn_(maize)___healthy": {
        "title": "🌽 Healthy Corn",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate irrigation and nutrition.",
            "Monitor leaves regularly.",
            "Maintain good crop-management practices."
        ]
    },

    "Grape___Black_rot": {
        "title": "🍇 Grape Black Rot",
        "type": "Fungal disease",
        "care": [
            "Remove infected leaves and fruit where practical.",
            "Remove infected plant debris.",
            "Improve airflow through appropriate vine management.",
            "Avoid prolonged moisture on foliage.",
            "Seek agricultural guidance for severe infection."
        ]
    },

    "Grape___Esca_(Black_Measles)": {
        "title": "🍇 Grape Esca / Black Measles",
        "type": "Grape fungal disease",
        "care": [
            "Remove severely affected plant material where appropriate.",
            "Avoid unnecessary wounds to vines.",
            "Maintain vineyard sanitation.",
            "Use healthy planting material.",
            "Seek professional agricultural advice."
        ]
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "title": "🍇 Grape Leaf Blight",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves.",
            "Remove infected plant debris.",
            "Improve airflow around vines.",
            "Avoid prolonged leaf wetness.",
            "Seek agricultural guidance for severe disease."
        ]
    },

    "Grape___healthy": {
        "title": "🍇 Healthy Grape",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Maintain appropriate watering and nutrition.",
            "Keep vines properly supported and ventilated.",
            "Inspect leaves and fruit regularly."
        ]
    },

    "Orange___Haunglongbing_(Citrus_greening)": {
        "title": "🍊 Citrus Greening / Huanglongbing",
        "type": "Bacterial disease",
        "care": [
            "There is no simple cure that restores an infected tree.",
            "Use certified healthy planting material.",
            "Monitor and manage insect vectors using approved local guidance.",
            "Follow local plant-health recommendations.",
            "Contact an agricultural or plant-health authority for confirmation."
        ]
    },

    "Peach___Bacterial_spot": {
        "title": "🍑 Peach Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected plant material where practical.",
            "Avoid unnecessary injury to branches and leaves.",
            "Maintain good airflow.",
            "Use resistant varieties where available.",
            "Seek local agricultural guidance for severe infections."
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
            "Remove severely affected leaves and fruit where practical.",
            "Avoid handling plants while foliage is wet.",
            "Use clean planting material.",
            "Avoid overhead watering when possible.",
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
            "Remove severely infected plant material according to local guidance.",
            "Keep foliage as dry as practical.",
            "Avoid overhead irrigation where possible.",
            "Use healthy certified planting material.",
            "Seek agricultural guidance promptly because late blight can spread rapidly."
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
            "Remove dead plant material during normal maintenance.",
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
            "Remove dead leaves as normal maintenance."
        ]
    },

    "Tomato___Bacterial_spot": {
        "title": "🍅 Tomato Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Avoid handling plants while foliage is wet.",
            "Water at the plant base.",
            "Use clean seed and planting material.",
            "Improve airflow around plants."
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
            "Remove severely infected plant material according to local guidance.",
            "Keep leaves as dry as possible.",
            "Avoid overhead watering.",
            "Improve airflow.",
            "Seek agricultural guidance promptly if suspected."
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
            "Remove severely affected leaves where practical.",
            "Improve airflow.",
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
            "Remove severely infected plants according to local guidance.",
            "Manage insect vectors using approved local methods.",
            "Use healthy certified planting material.",
            "Use resistant tomato varieties where available."
        ]
    },

    "Tomato___Tomato_mosaic_virus": {
        "title": "🍅 Tomato Mosaic Virus",
        "type": "Viral disease",
        "care": [
            "There is no direct cure for an infected plant.",
            "Remove severely infected plants to reduce possible spread.",
            "Clean and sanitize tools used around infected plants.",
            "Wash hands after handling suspected infected plants.",
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
    <div class="section-title">
        🌱 INTELLIGENT PLANT DIAGNOSTICS
    </div>

    <div class="section-subtitle">
        Upload a photograph of a plant leaf and let the
        deep-learning model analyze its visual patterns.
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
            <h2>38</h2>
            <p>DISEASE CLASSES</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="stat-card">
            <h2>70K+</h2>
            <p>TRAINING IMAGES</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="stat-card">
            <h2>AI</h2>
            <p>DEEP LEARNING</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        📡 PLANT SPECIMEN INPUT
    </div>

    <div class="section-subtitle">
        Upload an existing image or capture a new image
        directly using your device camera.
    </div>
    """,
    unsafe_allow_html=True
)


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
        <div class="glass">
            🌿 <strong>Specimen ready.</strong><br>
            The image can now be analyzed by the neural network.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

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
        # BEST PREDICTION
        # ====================================================

        best_index = int(
            top_indices[0]
        )

        best_class = class_names[
            best_index
        ]

        confidence = float(
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

        st.markdown(
            """
            <div class="section-title">
                🌿 RECOMMENDED CARE
            </div>

            <div class="section-subtitle">
                AI-assisted care guidance based on the detected condition
            </div>
            """,
            unsafe_allow_html=True
        )

        if (
            confidence >= 60
            and best_class in CARE_GUIDE
        ):

            care_info = CARE_GUIDE[
                best_class
            ]

            st.markdown(
                f"""
                <div class="care-box">

                    <div class="care-title">
                        {care_info["title"]}
                    </div>

                    <div class="care-type">
                        Category: {care_info["type"]}
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

        elif confidence < 60:

            st.warning(
                "⚠️ The model confidence is below 60%. "
                "Disease-specific care guidance is not being "
                "shown because the prediction may be unreliable."
            )

            st.info(
                "💡 Try uploading a clearer photograph of "
                "the plant leaf with good lighting."
            )

        else:

            st.info(
                "ℹ️ Care information for this condition "
                "is not available in the current guide."
            )

        st.caption(
            "Educational guidance only. PlantCare AI is not "
            "a professional agricultural diagnosis."
        )

        # ====================================================
        # TOP PREDICTIONS
        # ====================================================

        st.markdown(
            """
            <div class="section-title">
                📊 NEURAL PROBABILITY MATRIX
            </div>

            <div class="section-subtitle">
                Top five classifications generated by the model
            </div>
            """,
            unsafe_allow_html=True
        )

        for rank, index in enumerate(
            top_indices
        ):

            disease = class_names[
                int(index)
            ]

            probability = float(
                predictions[index] * 100
            )

            st.markdown(
                f"**#{rank + 1}  {disease}**"
            )

            st.progress(
                float(
                    predictions[index]
                )
            )

            st.caption(
                f"{probability:.2f}% probability"
            )


# ============================================================
# INFORMATION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        🧠 SYSTEM INFORMATION
    </div>
    """,
    unsafe_allow_html=True
)


with st.expander(
    "🧠 HOW THE AI WORKS"
):

    st.markdown(
        """
        **1. Image Input**

        The uploaded plant image is received by the application.

        **2. Image Preprocessing**

        The image is resized to 224 × 224 pixels.

        **3. Feature Analysis**

        The neural network analyzes visual patterns in the leaf.

        **4. Classification**

        The model compares the image against 38 learned classes.

        **5. Probability Analysis**

        The model calculates a probability for each class.

        **6. Final Prediction**

        The class with the highest probability is displayed.
        """
    )


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

        • Try to photograph the affected leaf closely.
        """
    )


with st.expander(
    "⚠️ IMPORTANT"
):

    st.markdown(
        """
        PlantCare AI is an educational AI demonstration.

        Its predictions are generated by an image-classification
        model and should not be treated as a guaranteed professional
        agricultural diagnosis.

        If a plant appears seriously affected, consult an appropriate
        agricultural professional or local plant-health authority.
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
