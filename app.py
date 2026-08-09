import streamlit as st
import tensorflow as tf
import numpy as np
import json
import time
import re
from PIL import Image

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# MODEL
# ============================================================

@st.cache_resource(show_spinner=False)
def load_model():
    return tf.keras.models.load_model("plant_disease_model.keras")


@st.cache_data(show_spinner=False)
def load_class_names():

    with open("class_names.json", "r") as f:
        data = json.load(f)

    # Supports either:
    # ["Apple___Apple_scab", ...]
    # or
    # {"0": "Apple___Apple_scab", ...}

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        try:
            return [data[str(i)] for i in range(len(data))]
        except:
            return list(data.values())

    return data


model = load_model()
class_names = load_class_names()

# ============================================================
# HELPERS
# ============================================================

def pretty_name(name):

    name = str(name)

    name = name.replace("___", " • ")
    name = name.replace("_", " ")
    name = name.replace(",", ", ")

    return name


def plant_name(name):

    name = str(name)

    if "___" in name:
        plant = name.split("___")[0]
    else:
        plant = name.split(" ")[0]

    plant = plant.replace("_", " ")

    return plant


def disease_name(name):

    name = str(name)

    if "___" in name:
        disease = name.split("___", 1)[1]
    else:
        disease = name

    disease = disease.replace("_", " ")

    return disease


def is_healthy(name):

    return "healthy" in str(name).lower()


def confidence_label(value):

    if value >= 90:
        return "VERY HIGH"

    if value >= 75:
        return "HIGH"

    if value >= 50:
        return "MODERATE"

    return "LOW"


# ============================================================
# FUTURISTIC CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   CORE
   ========================================================= */

html, body, [class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(0,255,140,0.09),
            transparent 25%
        ),
        radial-gradient(
            circle at 85% 10%,
            rgba(0,220,255,0.07),
            transparent 25%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(0,255,120,0.06),
            transparent 30%
        ),
        #030706;

    color: #eafff1;

    overflow-x: hidden;
}

/* =========================================================
   GRID
   ========================================================= */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    background-image:
        linear-gradient(
            rgba(0,255,140,0.018) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(0,255,140,0.018) 1px,
            transparent 1px
        );

    background-size: 42px 42px;

    pointer-events: none;

    z-index: 0;
}

/* =========================================================
   REMOVE STREAMLIT
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {

    max-width: 1250px;

    padding-top: 25px;

    padding-bottom: 80px;

    position: relative;

    z-index: 2;
}

/* =========================================================
   TOP NAV
   ========================================================= */

.navbar {

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 12px 18px;

    border:

        1px solid
        rgba(120,255,170,0.10);

    border-radius: 18px;

    background:
        rgba(4,12,8,0.72);

    backdrop-filter: blur(20px);

    margin-bottom: 45px;

}

.brand {

    display: flex;

    align-items: center;

    gap: 12px;

    font-weight: 800;

    letter-spacing: 1px;

}

.brand-icon {

    width: 36px;

    height: 36px;

    display: flex;

    justify-content: center;

    align-items: center;

    border-radius: 10px;

    background:

        radial-gradient(
            circle,
            rgba(0,255,130,0.30),
            rgba(0,255,130,0.05)
        );

    border: 1px solid rgba(0,255,130,0.35);

    font-size: 20px;

}

.online {

    display: flex;

    align-items: center;

    gap: 8px;

    color: #75d99a;

    font-size: 11px;

    letter-spacing: 2px;

}

.online-dot {

    width: 7px;

    height: 7px;

    border-radius: 50%;

    background: #00ff88;

    box-shadow: 0 0 12px #00ff88;

}

/* =========================================================
   HERO
   ========================================================= */

.hero {

    text-align: center;

    padding: 20px 0 45px;

}

.hero-orb {

    width: 115px;

    height: 115px;

    margin: auto;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    font-size: 58px;

    background:

        radial-gradient(
            circle,
            rgba(0,255,140,0.20),
            rgba(0,255,140,0.025) 65%,
            transparent 70%
        );

    border:

        1px solid
        rgba(0,255,140,0.38);

    box-shadow:

        0 0 35px
        rgba(0,255,140,0.18),

        0 0 110px
        rgba(0,255,140,0.08),

        inset 0 0 30px
        rgba(0,255,140,0.10);

    animation:
        floatOrb 4s ease-in-out infinite;

}

@keyframes floatOrb {

    0%,100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-8px);
    }

}

.hero-title {

    margin-top: 25px;

    font-size: clamp(42px, 6vw, 76px);

    line-height: 1;

    font-weight: 950;

    letter-spacing: -4px;

    background:

        linear-gradient(
            100deg,
            #ffffff,
            #a6ffc9,
            #00ff88,
            #73eaff,
            #ffffff
        );

    background-size: 300% 100%;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    animation:
        gradientShift 7s linear infinite;

}

@keyframes gradientShift {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }

}

.hero-subtitle {

    margin-top: 18px;

    color: #719281;

    font-size: 12px;

    letter-spacing: 5px;

    text-transform: uppercase;

}

/* =========================================================
   STATS
   ========================================================= */

.stats {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 12px;

    margin-bottom: 28px;

}

.stat {

    position: relative;

    overflow: hidden;

    padding: 22px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.045),
            rgba(255,255,255,0.012)
        );

    border:
        1px solid
        rgba(130,255,180,0.10);

}

.stat::after {

    content: "";

    position: absolute;

    width: 80px;

    height: 80px;

    right: -30px;

    bottom: -30px;

    border-radius: 50%;

    background:
        rgba(0,255,130,0.08);

    filter: blur(15px);

}

.stat-number {

    font-size: 25px;

    font-weight: 900;

    color: #b9ffd1;

}

.stat-label {

    margin-top: 5px;

    color: #5d7768;

    font-size: 9px;

    letter-spacing: 2px;

    text-transform: uppercase;

}

/* =========================================================
   MAIN GRID
   ========================================================= */

.main-grid {

    display: grid;

    grid-template-columns:
        1.1fr
        0.9fr;

    gap: 18px;

}

/* =========================================================
   PANELS
   ========================================================= */

.panel {

    background:

        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.012)
        );

    border:

        1px solid
        rgba(120,255,170,0.12);

    border-radius: 25px;

    padding: 28px;

    box-shadow:

        0 25px 80px
        rgba(0,0,0,0.28),

        inset 0 1px 0
        rgba(255,255,255,0.035);

    backdrop-filter: blur(20px);

}

.panel-title {

    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 20px;

}

.panel-title-main {

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 3px;

    color: #8ef7ae;

    text-transform: uppercase;

}

.panel-tag {

    font-size: 9px;

    padding: 6px 9px;

    border-radius: 20px;

    color: #67e99a;

    background:
        rgba(0,255,130,0.07);

    border:
        1px solid
        rgba(0,255,130,0.16);

    letter-spacing: 1px;

}

/* =========================================================
   UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {

    border:

        1px dashed
        rgba(0,255,140,0.35);

    border-radius: 20px;

    padding: 20px;

    background:

        radial-gradient(
            circle at center,
            rgba(0,255,140,0.05),
            rgba(0,0,0,0.15)
        );

    transition: 0.3s;

}

[data-testid="stFileUploader"]:hover {

    border-color: #00ff88;

    box-shadow:

        0 0 35px
        rgba(0,255,130,0.10);

}

[data-testid="stFileUploader"] section {

    background: transparent !important;

}

/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {

    width: 100%;

    height: 60px;

    border-radius: 16px;

    border:

        1px solid
        rgba(0,255,140,0.55);

    background:

        linear-gradient(
            100deg,
            #062d1c,
            #087a42,
            #062d1c
        );

    background-size: 200% 100%;

    color: #ffffff;

    font-weight: 900;

    letter-spacing: 2px;

    box-shadow:

        0 0 25px
        rgba(0,255,130,0.10);

    transition: all 0.25s;

}

.stButton > button:hover {

    transform: translateY(-3px);

    background-position: 100%;

    border-color: #00ff88;

    box-shadow:

        0 0 45px
        rgba(0,255,130,0.28);

}

/* =========================================================
   IMAGE
   ========================================================= */

[data-testid="stImage"] {

    border-radius: 20px;

    overflow: hidden;

    border:
        1px solid
        rgba(0,255,140,0.15);

    box-shadow:

        0 15px 50px
        rgba(0,0,0,0.35);

}

/* =========================================================
   SCANNER
   ========================================================= */

.scanner {

    margin-top: 20px;

    padding: 22px;

    border-radius: 18px;

    background:
        rgba(0,0,0,0.30);

    border:
        1px solid
        rgba(0,255,140,0.12);

    font-family: monospace;

}

.scanner-status {

    color: #72ffa7;

    font-size: 11px;

    letter-spacing: 2px;

    margin-bottom: 15px;

}

.scan-track {

    width: 100%;

    height: 3px;

    background: #12251a;

    overflow: hidden;

    border-radius: 10px;

}

.scan-beam {

    width: 35%;

    height: 100%;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00ff88,
            #b6ffd2,
            #00ff88,
            transparent
        );

    box-shadow:
        0 0 15px #00ff88;

    animation:
        scanBeam 1.2s infinite;

}

@keyframes scanBeam {

    from {
        transform: translateX(-150%);
    }

    to {
        transform: translateX(400%);
    }

}

/* =========================================================
   DIAGNOSIS
   ========================================================= */

.diagnosis {

    margin-top: 25px;

    text-align: center;

    padding: 35px 20px;

    border-radius: 22px;

    background:

        radial-gradient(
            circle at 50% 0%,
            rgba(0,255,130,0.14),
            transparent 65%
        ),

        rgba(0,12,7,0.65);

    border:

        1px solid
        rgba(0,255,130,0.22);

    box-shadow:

        inset 0 0 45px
        rgba(0,255,130,0.025);

}

.diagnosis-kicker {

    color: #54bd79;

    font-size: 9px;

    font-weight: 900;

    letter-spacing: 4px;

}

.diagnosis-name {

    margin-top: 12px;

    color: #ffffff;

    font-size: clamp(22px, 3vw, 34px);

    line-height: 1.2;

    font-weight: 950;

}

.diagnosis-confidence {

    margin-top: 10px;

    font-size: 30px;

    font-weight: 950;

    color: #63ffa0;

    text-shadow:
        0 0 25px
        rgba(0,255,130,0.30);

}

.confidence-label {

    color: #527563;

    font-size: 9px;

    letter-spacing: 3px;

}

/* =========================================================
   ANALYSIS ROW
   ========================================================= */

.analysis-row {

    display: flex;

    align-items: center;

    gap: 12px;

    margin: 12px 0;

}

.analysis-dot {

    width: 8px;

    height: 8px;

    border-radius: 50%;

    background: #00ff88;

    box-shadow:
        0 0 10px #00ff88;

}

.analysis-text {

    color: #829e8c;

    font-size: 11px;

}

/* =========================================================
   PREDICTION BARS
   ========================================================= */

.prediction {

    margin: 17px 0;

}

.prediction-head {

    display: flex;

    justify-content: space-between;

    gap: 10px;

    font-size: 11px;

    color: #a4b9aa;

}

.prediction-value {

    color: #65fca0;

    font-weight: 800;

}

.bar {

    height: 5px;

    margin-top: 8px;

    border-radius: 10px;

    background: #102018;

    overflow: hidden;

}

.bar-fill {

    height: 100%;

    border-radius: 10px;

    background:

        linear-gradient(
            90deg,
            #00a85c,
            #00ff88,
            #8affa9
        );

    box-shadow:
        0 0 12px
        rgba(0,255,130,0.25);

}

/* =========================================================
   INFO CARDS
   ========================================================= */

.info-grid {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 12px;

    margin-top: 18px;

}

.info-card {

    padding: 20px;

    border-radius: 18px;

    background:
        rgba(255,255,255,0.025);

    border:
        1px solid
        rgba(255,255,255,0.06);

}

.info-icon {

    font-size: 20px;

}

.info-title {

    margin-top: 12px;

    font-size: 11px;

    font-weight: 800;

    color: #b8d6c1;

}

.info-text {

    margin-top: 6px;

    color: #5c7564;

    font-size: 10px;

    line-height: 1.6;

}

/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    text-align: center;

    margin-top: 60px;

    color: #3e5948;

    font-size: 9px;

    letter-spacing: 3px;

}

/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 850px) {

    .main-grid {

        grid-template-columns: 1fr;

    }

    .stats {

        grid-template-columns:
            repeat(2,1fr);

    }

}

@media (max-width: 550px) {

    .hero-title {

        letter-spacing: -2px;

    }

    .stats {

        grid-template-columns: 1fr 1fr;

    }

    .info-grid {

        grid-template-columns: 1fr;

    }

    .navbar {

        margin-bottom: 25px;

    }

}

</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# NAVBAR
# ============================================================

st.markdown(
    """
<div class="navbar">

    <div class="brand">

        <div class="brand-icon">
            🌿
        </div>

        <div>
            PLANTCARE <span style="color:#00ff88;">AI</span>
        </div>

    </div>

    <div class="online">

        <div class="online-dot"></div>

        SYSTEM ONLINE

    </div>

</div>
""",
    unsafe_allow_html=True
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

    <div class="hero-orb">
        🌱
    </div>

    <div class="hero-title">
        PlantCare AI
    </div>

    <div class="hero-subtitle">
        Neural Plant Health Intelligence
    </div>

</div>
""",
    unsafe_allow_html=True
)

# ============================================================
# STATS
# ============================================================

st.markdown(
    """
<div class="stats">

    <div class="stat">
        <div class="stat-number">38</div>
        <div class="stat-label">Disease Classes</div>
    </div>

    <div class="stat">
        <div class="stat-number">70K+</div>
        <div class="stat-label">Training Images</div>
    </div>

    <div class="stat">
        <div class="stat-number">AI</div>
        <div class="stat-label">Vision Engine</div>
    </div>

    <div class="stat">
        <div class="stat-number">LIVE</div>
        <div class="stat-label">Neural Analysis</div>
    </div>

</div>
""",
    unsafe_allow_html=True
)

# ============================================================
# MAIN LAYOUT
# ============================================================

left, right = st.columns(
    [1.08, 0.92],
    gap="large"
)

# ============================================================
# LEFT — SCANNER
# ============================================================

with left:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-title">

                <div class="panel-title-main">
                    ◉ Biological Scanner
                </div>

                <div class="panel-tag">
                    INPUT
                </div>

            </div>

            <div style="
                color:#647e6d;
                font-size:11px;
                line-height:1.7;
                margin-bottom:18px;
            ">

                Upload a clear photograph of a plant leaf.
                The neural vision engine will analyze its
                visual characteristics and classify its
                most probable condition.

            </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Drop specimen image",
        type=["jpg", "jpeg", "png"],
        label_visibility="visible"
    )

    if uploaded_file:

        image = Image.open(
            uploaded_file
        ).convert("RGB")

        st.image(
            image,
            use_container_width=True
        )

        st.markdown(
            f"""
            <div style="
                margin-top:10px;
                color:#557363;
                font-family:monospace;
                font-size:9px;
                letter-spacing:1px;
            ">
                SPECIMEN LOADED ::
                {uploaded_file.name}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        analyze = st.button(
            "⚡ INITIATE NEURAL SCAN",
            use_container_width=True
        )

        if analyze:

            scanner = st.empty()

            stages = [
                "INITIALIZING VISION ENGINE",
                "CALIBRATING BIOLOGICAL SCANNER",
                "EXTRACTING VISUAL FEATURES",
                "ANALYZING LEAF STRUCTURE",
                "MATCHING DISEASE PATTERNS",
                "CALCULATING PROBABILITIES",
                "FINALIZING DIAGNOSIS"
            ]

            for stage in stages:

                scanner.markdown(
                    f"""
                    <div class="scanner">

                        <div class="scanner-status">
                            {stage}...
                        </div>

                        <div class="scan-track">

                            <div class="scan-beam">
                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(0.22)

            # ----------------------------------------------
            # PREPROCESS
            # ----------------------------------------------

            resized = image.resize(
                (224, 224)
            )

            image_array = np.asarray(
                resized
            ).astype("float32")

            image_array = np.expand_dims(
                image_array,
                axis=0
            )

            # ----------------------------------------------
            # PREDICTION
            # ----------------------------------------------

            predictions = model.predict(
                image_array,
                verbose=0
            )[0]

            top_indices = np.argsort(
                predictions
            )[-5:][::-1]

            best_index = top_indices[0]

            best_class = class_names[
                best_index
            ]

            confidence = (
                float(predictions[best_index])
                * 100
            )

            st.session_state["result"] = {
                "class": best_class,
                "confidence": confidence,
                "predictions": predictions,
                "top_indices": top_indices
            }

            scanner.empty()

# ============================================================
# RIGHT — DIAGNOSIS
# ============================================================

with right:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-title">

                <div class="panel-title-main">
                    ◈ Neural Diagnostics
                </div>

                <div class="panel-tag">
                    AI CORE
                </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    if "result" not in st.session_state:

        st.markdown(
            """
            <div style="
                min-height:380px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                text-align:center;
            ">

                <div style="
                    font-size:55px;
                    opacity:0.55;
                    filter:
                        drop-shadow(
                            0 0 20px
                            rgba(0,255,130,0.25)
                        );
                ">
                    🧬
                </div>

                <div style="
                    margin-top:20px;
                    color:#769281;
                    font-size:12px;
                    letter-spacing:2px;
                ">
                    AWAITING SPECIMEN
                </div>

                <div style="
                    margin-top:10px;
                    color:#405748;
                    font-size:10px;
                ">
                    Upload a leaf to begin neural analysis
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        result = st.session_state["result"]

        best_class = result["class"]

        confidence = result["confidence"]

        predictions = result["predictions"]

        top_indices = result["top_indices"]

        # ----------------------------------------------
        # DIAGNOSIS CARD
        # ----------------------------------------------

        st.markdown(
            f"""
            <div class="diagnosis">

                <div class="diagnosis-kicker">
                    NEURAL ANALYSIS COMPLETE
                </div>

                <div class="diagnosis-name">
                    {pretty_name(best_class)}
                </div>

                <div class="diagnosis-confidence">
                    {confidence:.2f}%
                </div>

                <div class="confidence-label">
                    {confidence_label(confidence)}
                    CONFIDENCE
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------
        # ANALYSIS STATUS
        # ----------------------------------------------

        status_text = (
            "PLANT APPEARS HEALTHY"
            if is_healthy(best_class)
            else "POSSIBLE DISEASE DETECTED"
        )

        status_icon = (
            "🟢"
            if is_healthy(best_class)
            else "🟠"
        )

        st.markdown(
            f"""
            <div style="
                margin-top:20px;
                padding:15px;
                border-radius:15px;
                background:rgba(255,255,255,0.025);
                border:1px solid rgba(255,255,255,0.06);
                text-align:center;
                color:#91aa99;
                font-size:10px;
                letter-spacing:2px;
            ">

                {status_icon}
                &nbsp;
                {status_text}

            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------
        # TOP PREDICTIONS
        # ----------------------------------------------

        st.markdown(
            """
            <div style="
                margin-top:28px;
                color:#72e69b;
                font-size:10px;
                font-weight:800;
                letter-spacing:3px;
            ">
                PROBABILITY MATRIX
            </div>
            """,
            unsafe_allow_html=True
        )

        for rank, index in enumerate(top_indices):

            name = pretty_name(
                class_names[index]
            )

            probability = (
                float(predictions[index])
                * 100
            )

            st.markdown(
                f"""
                <div class="prediction">

                    <div class="prediction-head">

                        <span>
                            #{rank + 1}
                            &nbsp;
                            {name}
                        </span>

                        <span class="prediction-value">
                            {probability:.2f}%
                        </span>

                    </div>

                    <div class="bar">

                        <div
                            class="bar-fill"
                            style="width:{min(probability,100)}%;"
                        ></div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# ============================================================
# INFORMATION
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="panel">

        <div class="panel-title">

            <div class="panel-title-main">
                ◇ Intelligence Core
            </div>

            <div class="panel-tag">
                SYSTEM
            </div>

        </div>

        <div class="info-grid">

            <div class="info-card">

                <div class="info-icon">
                    👁️
                </div>

                <div class="info-title">
                    VISUAL ANALYSIS
                </div>

                <div class="info-text">
                    The neural network examines
                    visual characteristics within
                    the uploaded leaf image.
                </div>

            </div>

            <div class="info-card">

                <div class="info-icon">
                    🧬
                </div>

                <div class="info-title">
                    38-CLASS ENGINE
                </div>

                <div class="info-text">
                    The model evaluates the image
                    against 38 learned plant-health
                    categories.
                </div>

            </div>

            <div class="info-card">

                <div class="info-icon">
                    📊
                </div>

                <div class="info-title">
                    PROBABILITY ENGINE
                </div>

                <div class="info-text">
                    Multiple possible classifications
                    are evaluated before presenting
                    the strongest prediction.
                </div>

            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HOW IT WORKS
# ============================================================

with st.expander("🧠  HOW THE NEURAL ENGINE WORKS"):

    st.markdown(
        """
### 01 — IMAGE INPUT

Your leaf photograph enters the vision pipeline.

### 02 — FEATURE EXTRACTION

The trained neural network analyzes visual patterns
within the image.

### 03 — CLASSIFICATION

The image is compared against the 38 classes
learned during training.

### 04 — PROBABILITY MATRIX

The model produces a probability for each class.

### 05 — DIAGNOSIS

The highest-probability class becomes the primary
prediction shown in the diagnostic interface.
"""
    )

# ============================================================
# DISCLAIMER
# ============================================================

with st.expander("⚠️  IMPORTANT INFORMATION"):

    st.markdown(
        """
This application is an educational AI demonstration.

Its prediction should not be treated as a professional
agricultural diagnosis. For real crop-management decisions,
consult an agricultural expert.
"""
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">

    PLANTCARE AI
    &nbsp; • &nbsp;
    NEURAL PLANT HEALTH INTELLIGENCE
    &nbsp; • &nbsp;
    38-CLASS VISION SYSTEM

    <br><br>

    SYSTEM STATUS: ONLINE

</div>
""",
    unsafe_allow_html=True
)
