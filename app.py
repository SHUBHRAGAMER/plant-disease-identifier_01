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

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(0, 255, 170, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(0, 180, 255, 0.07),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #050708 0%,
                #08100d 45%,
                #030505 100%
            );

        color: #e9fff5;
    }

    .main {
        padding-top: 2rem;
    }

    /* -------------------------------------------------------
       HERO
    ------------------------------------------------------- */

    .hero {
        text-align: center;
        padding: 35px 20px 25px 20px;
    }

    .hero-icon {
        font-size: 65px;
        filter: drop-shadow(
            0 0 20px rgba(0, 255, 170, 0.5)
        );
    }

    .hero-title {
        font-size: 48px;
        font-weight: 900;
        letter-spacing: 5px;
        background:
            linear-gradient(
                90deg,
                #ffffff,
                #00ffb3,
                #65ffd2,
                #ffffff
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #8aa99d;
        font-size: 16px;
        letter-spacing: 3px;
        margin-top: 8px;
    }

    /* -------------------------------------------------------
       GLASS CARDS
    ------------------------------------------------------- */

    .glass {
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.055),
                rgba(255,255,255,0.015)
            );

        border: 1px solid rgba(0,255,180,0.16);

        border-radius: 22px;

        padding: 25px;

        margin: 15px 0;

        box-shadow:
            0 10px 45px rgba(0,0,0,0.35),
            inset 0 0 25px rgba(0,255,180,0.015);

        backdrop-filter: blur(14px);
    }

    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: #00ffb3;
        letter-spacing: 2px;
    }

    .section-subtitle {
        color: #819b91;
        margin-top: 5px;
    }

    /* -------------------------------------------------------
       RESULT
    ------------------------------------------------------- */

    .result {
        margin-top: 25px;

        padding: 35px;

        text-align: center;

        border-radius: 25px;

        background:
            radial-gradient(
                circle at center,
                rgba(0,255,170,0.10),
                rgba(0,0,0,0.25)
            );

        border: 1px solid rgba(0,255,180,0.35);

        box-shadow:
            0 0 35px rgba(0,255,180,0.10),
            inset 0 0 30px rgba(0,255,180,0.04);
    }

    .result-label {
        color: #00ffb3;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 3px;
    }

    .result-name {
        font-size: 30px;
        font-weight: 900;
        margin-top: 15px;
        color: #ffffff;
    }

    .result-confidence {
        font-size: 20px;
        color: #66ffd3;
        margin-top: 12px;
        font-weight: 700;
    }

    /* -------------------------------------------------------
       SCANNING
    ------------------------------------------------------- */

    .scanning {
        text-align: center;

        padding: 30px;

        border-radius: 20px;

        color: #00ffb3;

        font-weight: 800;

        letter-spacing: 3px;

        background:
            rgba(0,255,170,0.04);

        border:
            1px solid rgba(0,255,170,0.20);

        box-shadow:
            0 0 30px rgba(0,255,170,0.08);
    }

    .scan-line {
        height: 2px;

        width: 100%;

        background:
            linear-gradient(
                90deg,
                transparent,
                #00ffb3,
                transparent
            );

        box-shadow:
            0 0 15px #00ffb3;

        animation:
            scan 1.2s infinite;
    }

    @keyframes scan {

        0% {
            transform: translateX(-30%);
            opacity: 0.2;
        }

        50% {
            opacity: 1;
        }

        100% {
            transform: translateX(30%);
            opacity: 0.2;
        }
    }

    /* -------------------------------------------------------
       INFO ROW
    ------------------------------------------------------- */

    .info-row {
        display: flex;
        justify-content: space-between;

        padding: 12px 0;

        border-bottom:
            1px solid rgba(255,255,255,0.06);
    }

    .info-name {
        color: #78948a;
    }

    .info-value {
        color: #eafff6;
        font-weight: 700;
    }

    /* -------------------------------------------------------
       BUTTONS
    ------------------------------------------------------- */

    .stButton > button {

        border-radius: 14px;

        border:
            1px solid rgba(0,255,180,0.35);

        background:
            linear-gradient(
                135deg,
                rgba(0,255,180,0.14),
                rgba(0,130,255,0.08)
            );

        color: white;

        font-weight: 800;

        letter-spacing: 1px;

        min-height: 52px;

        transition: 0.25s;
    }

    .stButton > button:hover {

        border-color: #00ffb3;

        box-shadow:
            0 0 25px rgba(0,255,180,0.25);

        transform: translateY(-2px);
    }

    /* -------------------------------------------------------
       UPLOADER
    ------------------------------------------------------- */

    [data-testid="stFileUploader"] {

        background:
            rgba(0,255,170,0.025);

        border:
            1px dashed rgba(0,255,180,0.35);

        border-radius: 18px;

        padding: 10px;
    }

    /* -------------------------------------------------------
       FOOTER
    ------------------------------------------------------- */

    .footer {
        text-align: center;

        padding: 40px 10px 20px;

        color: #668078;

        letter-spacing: 2px;

        font-size: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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
# INTRO CARD
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
        <div class="glass" style="text-align:center">

            <h2>38</h2>

            <p>DISEASE CLASSES</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="glass" style="text-align:center">

            <h2>70K+</h2>

            <p>TRAINING IMAGES</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="glass" style="text-align:center">

            <h2>AI</h2>

            <p>DEEP LEARNING</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# IMAGE INPUT
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

        st.success(
            "📸 Photo captured successfully!"
        )


# ============================================================
# CARE GUIDE
# ============================================================

CARE_GUIDE = {

    "Apple___Apple_scab": {
        "title": "🍎 Apple Scab",
        "type": "Fungal disease",
        "care": [
            "Remove and dispose of heavily infected leaves and fallen plant debris.",
            "Keep the area around the tree clean.",
            "Improve air circulation through appropriate pruning.",
            "Choose disease-resistant varieties when available.",
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
            "Continue regular watering and nutrition.",
            "Maintain good airflow.",
            "Inspect leaves and fruit regularly."
        ]
    },

    "Blueberry___healthy": {
        "title": "🫐 Healthy Blueberry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Maintain good airflow.",
            "Monitor regularly for unusual symptoms."
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
            "Maintain sunlight and airflow.",
            "Inspect leaves and fruit regularly."
        ]
    },

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "title": "🌽 Corn Gray Leaf Spot",
        "type": "Fungal disease",
        "care": [
            "Manage infected crop debris appropriately.",
            "Use crop rotation where appropriate.",
            "Choose resistant varieties when available.",
            "Maintain good crop health.",
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
            "Seek agricultural guidance for severe problems."
        ]
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "title": "🌽 Corn Northern Leaf Blight",
        "type": "Fungal disease",
        "care": [
            "Manage infected crop debris.",
            "Use crop rotation where appropriate.",
            "Choose resistant varieties when available.",
            "Avoid unnecessary plant stress.",
            "Seek agricultural advice for severe infections."
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
            "Remove infected plant material.",
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
            "Seek professional vineyard or agricultural advice."
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
            "Seek local agricultural guidance for severe disease."
        ]
    },

    "Grape___healthy": {
        "title": "🍇 Healthy Grape",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Maintain appropriate watering and nutrition.",
            "Keep vines properly supported.",
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
            "Avoid working with plants while foliage is wet.",
            "Use clean planting material.",
            "Avoid overhead watering when possible.",
            "Use resistant varieties where available."
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
            "Keep infected debris under control.",
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
            "Avoid overhead irrigation where possible.",
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
            "Water at the soil level.",
            "Choose resistant varieties when available."
        ]
    },

    "Strawberry___Leaf_scorch": {
        "title": "🍓 Strawberry Leaf Scorch",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves.",
            "Improve airflow.",
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
            "Remove dead leaves as part of normal care."
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
            "Keep foliage dry by watering at the base.",
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
            "Seek local agricultural guidance for serious infestations."
        ]
    },

    "Tomato___Target_Spot": {
        "title": "🍅 Tomato Target Spot",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves.",
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
            "Remove severely infected plants to reduce possible spread.",
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
# IMAGE PREVIEW
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

else:

    st.info(
        "🌱 Upload an image or use your camera to begin."
    )


# ============================================================
# ANALYSIS
# ============================================================

if uploaded_file is not None:

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
        # RESULT CARD
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

        st.markdown("---")

        st.markdown(
            """
            <div class="section-title">
                🌿 RECOMMENDED CARE
            </div>

            <div class="section-subtitle">
                AI-generated educational guidance based on
                the detected condition.
            </div>
            """,
            unsafe_allow_html=True
        )

        if confidence >= 60:

            if best_class in CARE_GUIDE:

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

            else:

                st.info(
                    "ℹ️ Care information for this condition "
                    "has not been added to the database yet."
                )

        else:

            st.warning(
                "⚠️ The model confidence is below 60%. "
                "A reliable disease-specific recommendation "
                "cannot be provided."
            )

            st.info(
                "💡 Try uploading a clearer photograph of "
                "the plant leaf with good lighting."
            )

        # ====================================================
        # CARE DISCLAIMER
        # ====================================================

        st.markdown(
            """
            <div class="glass">

                ⚠️ <strong>IMPORTANT</strong>

                <br><br>

                PlantCare AI provides educational guidance
                based on an AI image-classification model.

                <br><br>

                It is not a professional agricultural
                diagnosis and should not be treated as a
                guaranteed cure.

            </div>
            """,
            unsafe_allow_html=True
        )

        # ====================================================
        # TOP PREDICTIONS
        # ====================================================

        st.markdown("---")

        st.markdown(
            """
            <div class="section-title">
                📊 NEURAL PROBABILITY MATRIX
            </div>

            <div class="section-subtitle">
                Top five model predictions
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

st.markdown("---")

with st.expander(
    "🧠 HOW THE AI WORKS"
):

    st.markdown(
        """
        **1. Image Input**

        The uploaded or captured leaf image is processed
        by the application.

        **2. Feature Extraction**

        The neural network analyzes visual patterns
        within the leaf.

        **3. Classification**

        The model compares the image against
        38 learned classes.

        **4. Probability Analysis**

        The system calculates probabilities for
        each class.

        **5. Final Prediction**

        The class with the highest predicted probability
        is displayed.
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

        • Try to photograph the leaf against a
          relatively simple background.
        """
    )


with st.expander(
    "⚠️ IMPORTANT"
):

    st.markdown(
        """
        This AI system is intended for educational and
        demonstration purposes.

        Predictions should not be considered a professional
        agricultural diagnosis.

        For serious crop or plant-health problems, consult
        a qualified agricultural professional or local
        plant-health authority.
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

        ● SYSTEM ONLINE

    </div>
    """,
    unsafe_allow_html=True
)
