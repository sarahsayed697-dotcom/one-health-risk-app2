import streamlit as st

# =========================
# APP CONFIG
# =========================
st.set_page_config(page_title="One Health Risk Model", layout="wide")

st.title("🌍 One Health Integrated Risk Predictor")
st.markdown("""
Integrated Flurona (Influenza–COVID-19) and Bacterial / AMR risk assessment tool
based on climate, epidemiology, mobility, immunity, healthcare, and animal–human interface.
""")

tab1, tab2 = st.tabs(["🧬 Flurona Model", "🦠 Bacterial / AMR Model"])

# ======================================================
# FLURONA TAB
# ======================================================
with tab1:
    st.header("🧬 Flurona Coinfection Risk")

    temp = st.slider("🌡 Temperature (°C)", -10, 45, 15)
    humidity = st.slider("💧 Humidity (%)", 0, 100, 60)

    flu_cases = st.number_input("🤧 Influenza incidence (per 100k)", 0, 1000, 100)
    covid_cases = st.number_input("🦠 COVID-19 incidence (per 100k)", 0, 2000, 150)

    population = st.selectbox("👥 Population Density", ["Low", "Moderate", "High"])
    mobility = st.selectbox("🚶 Human Mobility", ["Low", "Moderate", "High"])

    flu_vax = st.slider("💉 Influenza vaccination (%)", 0, 100, 40)
    covid_vax = st.slider("💉 COVID-19 vaccination (%)", 0, 100, 50)

    hospital = st.selectbox("🏥 Hospital Capacity", ["Adequate", "Strained", "Overwhelmed"])

    pop = {"Low":0, "Moderate":1, "High":2}[population]
    mob = {"Low":0, "Moderate":1, "High":2}[mobility]
    hosp = {"Adequate":0, "Strained":1, "Overwhelmed":2}[hospital]

    flu_risk = (
        0.30 * (flu_cases / 1000) +
        0.25 * (1 - flu_vax / 100) +
        0.20 * (humidity / 100) +
        0.15 * (1 - temp / 45) +
        0.10 * pop
    )

    covid_risk = (
        0.30 * (covid_cases / 2000) +
        0.25 * (1 - covid_vax / 100) +
        0.20 * mob +
        0.15 * pop +
        0.10 * hosp
    )

    coinfection_risk = min(1, flu_risk * covid_risk * (1 + 0.3 * flu_risk))
    hospital_burden = coinfection_risk * (1 + hosp)

    def label(x):
        if x < 0.3: return "LOW 🟢"
        elif x < 0.6: return "MODERATE 🟠"
        else: return "HIGH 🔴"

    st.subheader("📊 Outputs")
    st.metric("Influenza Risk", label(flu_risk), f"{flu_risk:.2f}")
    st.metric("COVID-19 Risk", label(covid_risk), f"{covid_risk:.2f}")
    st.metric("Coinfection Risk Index", label(coinfection_risk), f"{coinfection_risk:.2f}")
    st.metric("Hospital Burden", label(hospital_burden / 2), f"{hospital_burden:.2f}")

# ======================================================
# BACTERIAL TAB
# ======================================================
with tab2:
    st.header("🦠 Bacterial / AMR Risk")

    temp_b = st.slider("🌡 Temperature (°C)", 0, 45, 25, key="tb")
    humidity_b = st.slider("💧 Humidity (%)", 0, 100, 60, key="hb")

    abx_use = st.selectbox("💊 Antibiotic Usage", ["Low", "Moderate", "High"])
    icu_capacity = st.selectbox("🏥 ICU Capacity", ["Adequate", "Limited", "Overloaded"])
    animal_contact = st.selectbox("🐄 Animal / Farm Contact", ["Low", "Moderate", "High"])

    abx = {"Low":0, "Moderate":1, "High":2}[abx_use]
    icu = {"Adequate":0, "Limited":1, "Overloaded":2}[icu_capacity]
    animal = {"Low":0, "Moderate":1, "High":2}[animal_contact]

    AMR_risk = (
        0.30 * abx +
        0.25 * icu +
        0.20 * animal +
        0.15 * (temp_b / 45) +
        0.10 * (humidity_b / 100)
    )

    ICU_amp = abx * icu
    zoonotic_risk = min(1, animal * (temp_b / 45) * (humidity_b / 100))
    AMR_risk = min(1, AMR_risk)

    st.subheader("📊 Outputs")
    st.metric("AMR / Bacterial Outbreak Risk", label(AMR_risk), f"{AMR_risk:.2f}")
    st.metric("ICU Amplification Risk", label(ICU_amp / 4), f"{ICU_amp}")
    st.metric("Zoonotic Spillover Risk", label(zoonotic_risk), f"{zoonotic_risk:.2f}")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("⚠ Research & policy-support tool only. Not for clinical diagnosis.") 
