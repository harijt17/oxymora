import streamlit as st
import google.generativeai as genai
from PIL import Image
import re
import random
import io

# Configure Gemini API
genai.configure(api_key="AIzaSyAj9F-VaYvvnT0Y_pddOgJA4cCOLl1FEZs")  # Replace with your actual API key

def extract_plant_features(image):
    """Analyze plant image using Gemini API."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        image,
        "Analyze this plant image and extract features like leaf area (in square centimeters as an approximate integer range), size, and health status. Ensure the leaf area is provided as an approximate integer range (e.g., 200-300 cm²)."
    ])
    
    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "Error: No response from Gemini API."

def extract_leaf_area(features_text):
    """Extract leaf area from Gemini's response."""
    if not features_text:
        return None
    match = re.search(r"leaf area.*?(\d+)\s*-\s*(\d+)\s*cm", features_text, re.IGNORECASE)
    if match:
        try:
            min_area = int(match.group(1))
            max_area = int(match.group(2))
            approx_leaf_area_cm2 = random.randint(min_area, max_area)
        except ValueError:
            return None
    else:
        return None
    return approx_leaf_area_cm2 / 10000  # Convert cm² to m²

def estimate_oxygen_production(leaf_area_m2, photosynthesis_rate=10, sunlight_hours=10):
    """Estimate daily oxygen production."""
    if leaf_area_m2 is None:
        return "Leaf area data not found. Unable to estimate oxygen production."
    conversion_factor = 0.72
    grams_per_liter_o2 = 1.429
    estimated_oxygen_grams = (leaf_area_m2 * photosynthesis_rate * sunlight_hours * conversion_factor) * grams_per_liter_o2
    return f"Estimated Oxygen Production: {estimated_oxygen_grams:.2f} grams/day"

# Streamlit UI
st.title("🌿 OXYMORA")
st.write("Upload a plant image to get the plant description and estimated oxygen production per day.")

uploaded_file = st.file_uploader("Choose a plant image", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Analyzing...")
    
    plant_features = extract_plant_features(image)
    if "Error" in plant_features:
        st.error(plant_features)
    else:
        leaf_area = extract_leaf_area(plant_features)
        oxygen_estimate = estimate_oxygen_production(leaf_area)
        
        st.subheader("📊 Plant Analysis Report:")
        st.text(plant_features)
        st.subheader("🌿 Oxygen Production Estimate:")
        st.success(oxygen_estimate)
