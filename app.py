import streamlit as st
import tensorflow as tf
import numpy as np
import json
import time
from PIL import Image

# ============================================================

# PAGE CONFIG

# ============================================================

st.set\_page\_config(
page\_title="PlantCare AI",
page\_icon="🌿",
layout="centered",
initial\_sidebar\_state="collapsed"
)

# ============================================================

# LOAD MODEL

# ============================================================

@st.cache\_resource
def load\_model():
return tf.keras.models.load\_model(
"plant\_disease\_model.keras"
)

@st.cache\_data
def load\_classes():
with open("class\_names.json", "r") as f:
return json.load(f)

model = load\_model()
class\_names = load\_classes()

# ============================================================

# FUTURISTIC DARK UI

# ============================================================

st.markdown("""

""", unsafe\_allow\_html=True)

# ============================================================

# HERO

# ============================================================

st.markdown("""

# ============================================================

# INTRO CARD

# ============================================================

st.markdown("""

Upload a photograph of a plant leaf.


Our deep-learning model will analyze its visual patterns
and identify the most likely plant health condition.

# ============================================================

# MODEL STATS

# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
st.markdown("""

38
Classes

""", unsafe\_allow\_html=True)

with col2:
st.markdown("""

70K+
Training Images

""", unsafe\_allow\_html=True)

with col3:
st.markdown("""

AI
Deep Learning

""", unsafe\_allow\_html=True)

# ============================================================

# UPLOAD

# ============================================================

st.markdown("""

uploaded\_file = st.file\_uploader(
"Drop your leaf image here",
type=["jpg", "jpeg", "png"],
help="Use a clear image of a plant leaf."
)

st.markdown("", unsafe\_allow\_html=True)

# ============================================================

# IMAGE + ANALYSIS

# ============================================================

if uploaded\_file is not None:

```
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
```

# ============================================================

# INFORMATION

# ============================================================

st.markdown("", unsafe\_allow\_html=True)

with st.expander("🧠 HOW THE AI WORKS"):

```
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
```

with st.expander("🎯 GET BETTER RESULTS"):

```
st.markdown("""
• Use a clear photograph.

• Keep the leaf well illuminated.

• Avoid extreme blur.

• Keep the main leaf visible.

• Avoid images containing many overlapping leaves.
""")
```

with st.expander("⚠️ IMPORTANT"):

```
st.markdown("""
This AI system is intended for educational and
demonstration purposes.

The prediction should not be considered a professional
agricultural diagnosis.
""")
```

# ============================================================

# FOOTER

# ============================================================

st.markdown("""

🌿 PLANTCARE AI

NEURAL PLANT INTELLIGENCE • 38-CLASS MODEL



SYSTEM ONLINE
