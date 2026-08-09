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
# IMAGE INPUT
# ============================================================

st.markdown("""
<div class="section-title">
📸 ADD PLANT IMAGE
</div>

<div class="section-subtitle">
Choose how you want to provide the leaf image.
</div>
""", unsafe_allow_html=True)

# Create two tabs
upload_tab, camera_tab = st.tabs([
    "📁 UPLOAD IMAGE",
    "📷 OPEN CAMERA"
])

uploaded_file = None

# ============================================================
# UPLOAD IMAGE
# ============================================================

with upload_tab:

    st.markdown("""
    <div class="glass">

    <h3>📁 Upload from your device</h3>

    <p>
    Select a clear photograph of the plant leaf.
    </p>

    </div>
    """, unsafe_allow_html=True)

    file_upload = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG and PNG",
        label_visibility="collapsed"
    )

    if file_upload is not None:

        uploaded_file = file_upload

        st.success(
            "✅ Image successfully loaded!"
        )


# ============================================================
# CAMERA
# ============================================================

with camera_tab:

    st.markdown("""
    <div class="glass">

    <h3>📷 Take a photo</h3>

    <p>
    Allow camera access and photograph the plant leaf directly.
    </p>

    </div>
    """, unsafe_allow_html=True)

    camera_image = st.camera_input(
        "Take a picture of the plant leaf"
    )

    if camera_image is not None:

        uploaded_file = camera_image

        st.success(
            "📸 Photo captured successfully!"
        )


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

        # ============================================================
# COMPLETE 38-CLASS CARE GUIDE
# ============================================================

CARE_GUIDE = {

    # --------------------------------------------------------
    # APPLE
    # --------------------------------------------------------

    "Apple___Apple_scab": {
        "title": "🍎 Apple Scab",
        "type": "Fungal disease",
        "care": [
            "Remove and dispose of heavily infected leaves and fallen plant debris.",
            "Keep the area around the tree clean to reduce sources of infection.",
            "Improve air circulation through appropriate pruning.",
            "Choose disease-resistant apple varieties when possible.",
            "For severe disease, seek local agricultural guidance for appropriate disease-control treatment."
        ]
    },

    "Apple___Black_rot": {
        "title": "🍎 Apple Black Rot",
        "type": "Fungal disease",
        "care": [
            "Remove infected fruit, leaves and dead plant material.",
            "Prune affected branches where appropriate and keep pruning tools clean.",
            "Avoid leaving mummified fruit on the tree.",
            "Maintain good tree health and reduce plant stress.",
            "Seek local agricultural guidance if the disease is severe."
        ]
    },

    "Apple___Cedar_apple_rust": {
        "title": "🍎 Cedar-Apple Rust",
        "type": "Fungal disease",
        "care": [
            "Remove infected plant material where practical.",
            "Maintain good airflow around the tree.",
            "Disease-resistant apple varieties can help reduce problems.",
            "If practical, manage nearby infected juniper or cedar hosts.",
            "Severe cases should be evaluated using local agricultural guidance."
        ]
    },

    "Apple___healthy": {
        "title": "🍎 Healthy Apple",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue regular watering and appropriate nutrition.",
            "Maintain good airflow around the tree.",
            "Inspect leaves and fruit regularly for new symptoms."
        ]
    },


    # --------------------------------------------------------
    # BLUEBERRY
    # --------------------------------------------------------

    "Blueberry___healthy": {
        "title": "🫐 Healthy Blueberry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Maintain good airflow around plants.",
            "Monitor regularly for discoloration, spots or unusual growth."
        ]
    },


    # --------------------------------------------------------
    # CHERRY
    # --------------------------------------------------------

    "Cherry_(including_sour)___Powdery_mildew": {
        "title": "🍒 Cherry Powdery Mildew",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected plant material where practical.",
            "Improve airflow by avoiding excessive crowding.",
            "Avoid excessive humidity around foliage.",
            "Choose resistant varieties when available.",
            "For significant infection, seek local agricultural guidance."
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


    # --------------------------------------------------------
    # CORN
    # --------------------------------------------------------

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "title": "🌽 Corn Gray Leaf Spot",
        "type": "Fungal disease",
        "care": [
            "Remove heavily infected plant debris where practical.",
            "Improve field airflow and avoid excessive plant stress.",
            "Use crop rotation where appropriate.",
            "Consider disease-resistant varieties for future planting.",
            "Follow local agricultural recommendations for disease management."
        ]
    },

    "Corn_(maize)___Common_rust_": {
        "title": "🌽 Corn Common Rust",
        "type": "Fungal disease",
        "care": [
            "Monitor plants regularly for increasing rust symptoms.",
            "Maintain healthy plant growth through appropriate water and nutrition.",
            "Use resistant varieties when available.",
            "Avoid unnecessary prolonged leaf wetness.",
            "For severe crop problems, consult local agricultural guidance."
        ]
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "title": "🌽 Corn Northern Leaf Blight",
        "type": "Fungal disease",
        "care": [
            "Remove or properly manage infected crop debris.",
            "Use crop rotation where appropriate.",
            "Choose resistant varieties when available.",
            "Maintain good crop health and avoid unnecessary plant stress.",
            "Seek local agricultural advice for severe infections."
        ]
    },

    "Corn_(maize)___healthy": {
        "title": "🌽 Healthy Corn",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate irrigation and nutrition.",
            "Monitor leaves regularly for spots or discoloration.",
            "Maintain good crop management practices."
        ]
    },


    # --------------------------------------------------------
    # GRAPE
    # --------------------------------------------------------

    "Grape___Black_rot": {
        "title": "🍇 Grape Black Rot",
        "type": "Fungal disease",
        "care": [
            "Remove infected leaves and fruit where practical.",
            "Remove old infected plant material from around the vines.",
            "Improve airflow through appropriate vine management.",
            "Avoid prolonged moisture on foliage.",
            "Use local agricultural guidance for severe infections."
        ]
    },

    "Grape___Esca_(Black_Measles)": {
        "title": "🍇 Grape Esca / Black Measles",
        "type": "Grape fungal disease",
        "care": [
            "Remove severely affected plant material where appropriate.",
            "Avoid unnecessary wounds to grapevines.",
            "Maintain good vineyard sanitation.",
            "Use healthy planting material for future vines.",
            "Seek professional vineyard or agricultural advice because symptoms can have multiple causes."
        ]
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "title": "🍇 Grape Leaf Blight",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves and plant debris.",
            "Improve airflow around the vines.",
            "Avoid prolonged leaf wetness where practical.",
            "Maintain good vineyard sanitation.",
            "Seek local agricultural guidance for severe disease."
        ]
    },

    "Grape___healthy": {
        "title": "🍇 Healthy Grape",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Maintain appropriate watering and nutrition.",
            "Keep vines properly supported and ventilated.",
            "Regularly inspect leaves and fruit."
        ]
    },


    # --------------------------------------------------------
    # ORANGE
    # --------------------------------------------------------

    "Orange___Haunglongbing_(Citrus_greening)": {
        "title": "🍊 Citrus Greening / Huanglongbing",
        "type": "Bacterial disease",
        "care": [
            "There is currently no simple cure that restores an infected tree.",
            "Remove severely affected trees according to local plant-health guidance when recommended.",
            "Use certified healthy planting material for new trees.",
            "Monitor and manage the insect vectors responsible for spreading the disease using approved local guidance.",
            "Contact a local agricultural or plant-health authority for confirmation and management."
        ]
    },


    # --------------------------------------------------------
    # PEACH
    # --------------------------------------------------------

    "Peach___Bacterial_spot": {
        "title": "🍑 Peach Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected plant material where practical.",
            "Avoid unnecessary injury to branches and leaves.",
            "Maintain good airflow around the tree.",
            "Use disease-resistant varieties where available.",
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


    # --------------------------------------------------------
    # BELL PEPPER
    # --------------------------------------------------------

    "Pepper,_bell___Bacterial_spot": {
        "title": "🫑 Bell Pepper Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected leaves and fruit where practical.",
            "Avoid working with plants when foliage is wet.",
            "Use clean planting material and maintain good sanitation.",
            "Avoid overhead watering when possible.",
            "Use resistant varieties and local agricultural guidance where available."
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


    # --------------------------------------------------------
    # POTATO
    # --------------------------------------------------------

    "Potato___Early_blight": {
        "title": "🥔 Potato Early Blight",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected foliage where practical.",
            "Keep infected plant debris under control.",
            "Water at the base of the plant rather than wetting foliage.",
            "Improve airflow and avoid overcrowding.",
            "Use crop rotation and resistant varieties where appropriate."
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
            "Late blight can spread rapidly, so seek local agricultural guidance promptly if strongly suspected."
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


    # --------------------------------------------------------
    # RASPBERRY
    # --------------------------------------------------------

    "Raspberry___healthy": {
        "title": "🫐 Healthy Raspberry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Maintain good airflow around plants.",
            "Provide appropriate water and nutrition.",
            "Remove dead plant material as part of normal maintenance.",
            "Inspect plants regularly for disease symptoms."
        ]
    },


    # --------------------------------------------------------
    # SOYBEAN
    # --------------------------------------------------------

    "Soybean___healthy": {
        "title": "🌱 Healthy Soybean",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Maintain appropriate soil moisture and nutrition.",
            "Monitor the crop regularly.",
            "Use good crop-management and sanitation practices."
        ]
    },


    # --------------------------------------------------------
    # SQUASH
    # --------------------------------------------------------

    "Squash___Powdery_mildew": {
        "title": "🎃 Squash Powdery Mildew",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Improve airflow around plants.",
            "Avoid excessive crowding.",
            "Water at the soil level rather than unnecessarily wetting foliage.",
            "Choose resistant varieties when available."
        ]
    },


    # --------------------------------------------------------
    # STRAWBERRY
    # --------------------------------------------------------

    "Strawberry___Leaf_scorch": {
        "title": "🍓 Strawberry Leaf Scorch",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves and plant debris.",
            "Improve airflow around strawberry plants.",
            "Avoid excessive leaf wetness.",
            "Maintain appropriate irrigation and plant nutrition.",
            "Use healthy planting material and monitor new growth."
        ]
    },

    "Strawberry___healthy": {
        "title": "🍓 Healthy Strawberry",
        "type": "Healthy",
        "care": [
            "No disease treatment is indicated by the model.",
            "Continue appropriate watering and nutrition.",
            "Maintain good airflow around plants.",
            "Remove dead leaves as part of normal plant care."
        ]
    },


    # --------------------------------------------------------
    # TOMATO
    # --------------------------------------------------------

    "Tomato___Bacterial_spot": {
        "title": "🍅 Tomato Bacterial Spot",
        "type": "Bacterial disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Avoid handling plants while foliage is wet.",
            "Water at the base of plants rather than overhead.",
            "Use clean seed and planting material.",
            "Improve airflow and avoid unnecessary leaf wetness."
        ]
    },

    "Tomato___Early_blight": {
        "title": "🍅 Tomato Early Blight",
        "type": "Fungal disease",
        "care": [
            "Remove affected leaves where practical.",
            "Mulch around plants to reduce soil splash onto leaves.",
            "Water at the base of the plant.",
            "Improve airflow through spacing and appropriate support.",
            "Use crop rotation and disease-resistant varieties where available."
        ]
    },

    "Tomato___Late_blight": {
        "title": "🍅 Tomato Late Blight",
        "type": "Water mold disease",
        "care": [
            "Remove severely infected plant material according to local guidance.",
            "Keep leaves as dry as possible.",
            "Avoid overhead watering.",
            "Improve airflow around plants.",
            "Because late blight can spread rapidly, seek local agricultural guidance if suspected."
        ]
    },

    "Tomato___Leaf_Mold": {
        "title": "🍅 Tomato Leaf Mold",
        "type": "Fungal disease",
        "care": [
            "Remove severely affected leaves where practical.",
            "Increase ventilation and airflow around plants.",
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
            "Keep foliage dry by watering at the plant base.",
            "Use mulch to reduce soil splash.",
            "Improve spacing and airflow.",
            "Do not save seed from severely infected plants."
        ]
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "title": "🍅 Tomato Two-Spotted Spider Mite",
        "type": "Pest",
        "care": [
            "Inspect the undersides of leaves carefully.",
            "Remove severely affected leaves where practical.",
            "Keep plants appropriately watered because plant stress can worsen mite problems.",
            "Encourage natural predators where appropriate.",
            "For serious infestations, seek local agricultural guidance for suitable pest-management options."
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
            "Use healthy planting material and follow local disease-management guidance."
        ]
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "title": "🍅 Tomato Yellow Leaf Curl Virus",
        "type": "Viral disease",
        "care": [
            "There is no direct cure that eliminates the virus from an infected plant.",
            "Remove severely infected plants according to local agricultural guidance.",
            "Control the insect vectors that spread the virus using approved local methods.",
            "Use healthy, certified planting material.",
            "Use resistant tomato varieties when available."
        ]
    },

    "Tomato___Tomato_mosaic_virus": {
        "title": "🍅 Tomato Mosaic Virus",
        "type": "Viral disease",
        "care": [
            "There is no direct cure for an infected plant.",
            "Remove severely infected plants to reduce possible spread.",
            "Wash hands after handling suspected infected plants.",
            "Clean and sanitize tools used around infected plants.",
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
# RECOMMENDED CARE
# ====================================================

st.markdown("---")

st.subheader("🌿 Recommended Care")

if confidence >= 60 and best_class in CARE_GUIDE:

    care_info = CARE_GUIDE[best_class]

    st.markdown(
        f"### {care_info['title']}"
    )

    st.caption(
        f"Category: {care_info['type']}"
    )

    st.markdown("#### 🩺 Recommended Actions")

    for item in care_info["care"]:

        st.markdown(
            f"• {item}"
        )

else:

    st.warning(
        "⚠️ The model is not sufficiently confident "
        "to provide disease-specific care advice. "
        "Try uploading a clearer image."
    )

st.caption(
    "Educational guidance only. AI predictions are not "
    "a professional agricultural diagnosis."
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
    # ----------------------------------------------------
    # CHECK CONFIDENCE
    # ----------------------------------------------------

if confidence >= 60:

    if best_class in CARE_GUIDE:

        care_info = CARE_GUIDE[best_class]


            # ------------------------------------------------
            # DISEASE INFORMATION
            # ------------------------------------------------

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


            # ------------------------------------------------
            # CARE RECOMMENDATIONS
            # ------------------------------------------------

            st.markdown("### 🩺 Recommended Actions")

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
            "💡 Try uploading a clearer photograph of the "
            "plant leaf with good lighting."
        )


    # ----------------------------------------------------
    # DISCLAIMER
    # ----------------------------------------------------

    st.markdown(
        """
        <div class="glass">

        ⚠️ <strong>IMPORTANT</strong><br><br>

        PlantCare AI provides educational guidance based on
        an AI image classification model. It is not a
        professional agricultural diagnosis and should not
        be treated as a guaranteed cure.

        </div>
        """,
        unsafe_allow_html=True
    )
# ====================================================
# TOP PREDICTIONS
# ====================================================
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
