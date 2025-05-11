import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from PIL import Image

def home_page():
    st.markdown("<h2>🔬🩸 Anemia Shield: Detect & Prevent</h2>", unsafe_allow_html=True)
    st.subheader("Your Smart Health Companion for Anemia Diagnosis")
    try:
        img = Image.open(r"anemia.webp").resize((620, 400))
        st.image(img, use_container_width=500)
    except Exception as e:
        st.error(f"Error loading image: {e}")

    st.markdown("""
    ### 🚀 What You Can Do Here:
    - ✅ **Instant Anemia Diagnosis** based on WHO guidelines.
    - 💊 **Personalized Preventive Measures** to improve your health.
    - 📊 **Data Visualization & Insights** on anemia severity and trends.
    - 🔍 **Easy-to-Use & AI-Powered** for accurate results.
    """, unsafe_allow_html=True)
    st.subheader("🩺 Start Your Anemia Diagnosis Now! 🩺")
def diagnosis_page():
    with open(r"anemia_detector (1).pkl", "rb") as model_file:
        model = pickle.load(model_file)

    def classify_anemia(hemoglobin, category):
        anemia_ranges = {
            "Male": [(13.0, float("inf"), "Normal"), (11.0, 12.9, "Mild Anemia"), (8.0, 10.9, "Moderate Anemia"), (0, 7.9, "Severe Anemia")],
            "Female": [(12.0, float("inf"), "Normal"), (11.0, 11.9, "Mild Anemia"), (8.0, 10.9, "Moderate Anemia"), (0, 7.9, "Severe Anemia")],
            "Child": [(11.0, float("inf"), "Normal"), (10.0, 10.9, "Mild Anemia"), (7.0, 9.9, "Moderate Anemia"), (0, 6.9, "Severe Anemia")],
            "Pregnant Woman": [(11.0, float("inf"), "Normal"), (10.0, 10.9, "Mild Anemia"), (7.0, 9.9, "Moderate Anemia"), (0, 6.9, "Severe Anemia")]
        }
        preventive_measures = {
            "Normal": "✅ Maintain a balanced diet rich in iron, vitamin B12, and folic acid.\n✅ Stay hydrated and get regular checkups.\n✅ Exercise to improve circulation and oxygen transport.\n💊 Allopathy: Not required, but Ferrous Sulfate (325mg) can be taken if needed.\n🌿 Ayurveda: Chyawanprash daily and Triphala churna for better iron absorption.\n🍃 Naturopathy: Beetroot & carrot juice, morning sun exposure for Vitamin D.\n🏡 Homeopathy: Ferrum Phosphoricum 6X, a mild iron supplement.",
            "Mild Anemia": "⚠️ Increase intake of iron-rich foods (spinach, lentils, red meat).\n⚠️ Take vitamin C-rich foods (oranges, lemons, amla) to enhance iron absorption.\n⚠️ Avoid tea/coffee immediately after meals, as they reduce iron absorption.\n💊 Allopathy: Ferrous Sulfate tablets, Vitamin C supplements for better absorption.\n🌿 Ayurveda: Ashwagandha, Guduchi, and dates with jaggery.\n🍃 Naturopathy: Pomegranate or wheatgrass juice, deep breathing exercises.\n🏡 Homeopathy: Natrum Muriaticum 30C (useful for chronic anemia).",
            "Moderate Anemia": "⚠️ Consult a doctor for further evaluation.\n⚠️ Include iron, vitamin B12, and folate supplements if recommended.\n⚠️ Monitor your blood tests and avoid excessive alcohol consumption.\n💊 Allopathy: Ferrous Fumarate, Folic Acid, Vitamin B12 injections (Cyanocobalamin).\n🌿 Ayurveda: Punarnava Mandur tablets, Pomegranate juice daily.\n🍃 Naturopathy: Green smoothies (spinach, kale, moringa), nettle leaf tea.\n🏡 Homeopathy: China Officinalis 30C (for anemia due to blood loss).",
            "Severe Anemia": "🚨 Seek immediate medical attention.\n🚨 You may need specialized treatment like transfusions or medications.\n🚨 Maintain a high-protein, iron-rich diet with doctor supervision.\n💊 Allopathy: Iron Sucrose IV infusion, Erythropoietin injections.\n🌿 Ayurveda: Draksharishta (grape-based iron tonic), Mandoor Bhasma.\n🍃 Naturopathy: Fresh Aloe Vera juice, Beetroot juice therapy.\n🏡 Homeopathy: Ferrum Metallicum 30C (for severe weakness and pallor)."
        }
        for lower, upper, severity in anemia_ranges.get(category, []):
            if lower <= hemoglobin <= upper:
                return severity, preventive_measures.get(severity, "No recommendations available.")
        return "Unknown", "⚠️ Invalid Category or Hemoglobin Value."

    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=1, max_value=120, step=1)
    category = st.selectbox("Select Category:", ["Male", "Female", "Child", "Pregnant Woman"])
    weight = st.number_input("Enter your weight (kg):", min_value=10.0, max_value=200.0, step=0.1)
    hemoglobin = st.number_input("Enter Hemoglobin (g/dL):", min_value=4.0, max_value=18.0, step=0.1)

    if st.button("Detect Anemia"):
        anemia_type, prevention = classify_anemia(hemoglobin, category)
        st.write(f"🔹 **Patient Name:** {name}")
        st.write(f"🔹 **Age:** {age} | **Category:** {category} | **Weight:** {weight} kg")
        st.write(f"🔹 **Hemoglobin:** {hemoglobin} g/dL")
        st.write(f"🔹 **Predicted Anemia Condition:** {anemia_type}")
        st.write("🩺 **Preventive Measures:**")
        for line in prevention.split("\n"):
            st.write(line)
        # Optionally save patient data here
        st.success("✅ Diagnosis complete!")
        st.success("✅ Patient data saved successfully!")
        # Save patient data to CSV
        patient_data = pd.DataFrame([[name, age, weight, category, hemoglobin, anemia_type]],
                                columns=["Name", "Age", "Weight", "Category", "Hb Level", "Anemia Condition"])
        if os.path.exists("anemia_patient_data.csv"):
            patient_data.to_csv("anemia_patient_data.csv", mode='a', header=False, index=False)
        else:
            patient_data.to_csv("anemia_patient_data.csv", index=False)

    def patient_data_page():
        st.markdown("<h2>📋 Patient Diagnosis Records</h2>", unsafe_allow_html=True)
        try:
            df = pd.read_csv("anemia_patient_data.csv")
            st.dataframe(df)
        except FileNotFoundError:
            st.warning("⚠️ No patient records found. Diagnose a patient to see data here!")
def patient_data_page():
    st.markdown("<h2>📋 Patient Diagnosis Records</h2>", unsafe_allow_html=True)
    try:
        df = pd.read_csv("anemia_patient_data.csv")
        st.dataframe(df)
    except FileNotFoundError:
        st.warning("⚠️ No patient records found. Diagnose a patient to see data here!")
def visualization_page():
    st.markdown("<h2 style='text-align: center;'>📊 Anemia Severity Distribution</h2>", unsafe_allow_html=True)
    try:
        df = pd.read_csv("anemia_patient_data.csv").dropna(subset=["Anemia Condition"])
        anemia_counts = df["Anemia Condition"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(anemia_counts, labels=anemia_counts.index, autopct="%1.1f%%", 
               colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"], startangle=90)
        plt.figtext(0.5, -0.2, "Anemia Distribution", fontsize=14, ha="center", fontweight="bold")
        st.pyplot(fig)
        if st.button("🔄 Refresh Chart"):
            st.rerun()
    except FileNotFoundError:
        st.error("❌ No data available for visualization. Diagnose some patients first!")
PAGES = {
    "Home": home_page,
    "Diagnosis": diagnosis_page,
    "Patient Data": patient_data_page,
    "Visualization": visualization_page
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
PAGES[selection]()



    
