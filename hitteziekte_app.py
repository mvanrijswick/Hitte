import streamlit as st

def normaliseer(waarde, min_w, max_w):
    """Zet een waarde om naar een schaal van 0-10"""
    return max(0, min(10, ((waarde - min_w) / (max_w - min_w)) * 10))

def bereken_risico(WBGT, kleding, inspanning, vetpercentage, fitheid, hitteziekte, drinken, gegeten, slapen):
    """Bereken de hitteziekte-risicoscore (0-100)"""
    
    # Kleding score (0-10)
    kleding_scores = {
        "GVT": 3,
        "GVT met extra bedekking bovenlichaam": 6,
        "CBRN": 10
    }
    kleding_score = kleding_scores[kleding]

    # Inspanning score (0-10)
    inspanning_scores = {
        "Zeer licht": 2,
        "Licht": 4,
        "Matig": 6,
        "Zwaar": 8,
        "Zeer zwaar": 10
    }
    inspanning_score = inspanning_scores[inspanning]

    # Normaliseer overige waarden
    wbgt_score = normaliseer(WBGT, 10, 35)
    vet_score = normaliseer(vetpercentage, 5, 40)
    fitheid_score = 10 - normaliseer(fitheid, 0, 10)
    hitteziekte_score = 10 if hitteziekte == "Ja" else 0
    drinken_score = 10 - normaliseer(drinken, 0, 3)
    eten_score = 0 if gegeten == "Ja" else 5
    slaap_score = 0 if slapen == "Ja" else 5

    # Weging en berekening van de totale score
    risico = (
        wbgt_score * 3 + kleding_score * 2 + inspanning_score * 2 + vet_score * 1 + 
        fitheid_score * 1 + hitteziekte_score * 2 + drinken_score * 1.5 + eten_score * 1 + slaap_score * 1
    )

    risico_score = min(100, max(0, risico))

    return risico_score

# Streamlit Webapp Interface
st.title("🌡️ Hitteziekte Risico Calculator")

# Sidebar met invoeropties
st.sidebar.header("📋 Voer gegevens in:")

WBGT = st.sidebar.slider("WBGT (10-35°C)", min_value=10, max_value=35, value=25)
kleding = st.sidebar.selectbox("Kleding", ["GVT", "GVT met extra bedekking bovenlichaam", "CBRN"])
inspanning = st.sidebar.selectbox("Inspanningsintensiteit", ["Zeer licht", "Licht", "Matig", "Zwaar", "Zeer zwaar"])
vetpercentage = st.sidebar.slider("Vetpercentage (5-40%)", min_value=5, max_value=40, value=20)
fitheid = st.sidebar.slider("Fitheid (0=niet fit, 10=zeer fit)", min_value=0, max_value=10, value=5)
hitteziekte = st.sidebar.selectbox("Eerder hitteziekte gehad?", ["Nee", "Ja"])
drinken = st.sidebar.slider("Hydratatie (0-3+ liter/dag)", min_value=0.0, max_value=3.0, value=1.5, step=0.1)
gegeten = st.sidebar.selectbox("Voldoende gegeten?", ["Ja", "Nee"])
slapen = st.sidebar.selectbox("Voldoende slaap?", ["Ja", "Nee"])

# Berekening en output
if st.sidebar.button("Bereken Risico"):
    risico_score = bereken_risico(WBGT, kleding, inspanning, vetpercentage, fitheid, hitteziekte, drinken, gegeten, slapen)
    
    # Risico-interpretatie
    if risico_score < 20:
        kleur = "green"
        status = "Laag ✅"
    elif risico_score < 50:
        kleur = "orange"
        status = "Matig ⚠️"
    elif risico_score < 80:
        kleur = "red"
        status = "Hoog 🔥"
    else:
        kleur = "darkred"
        status = "Zeer Hoog 🚨"
    
    st.markdown(f"## **Risicoscore: {risico_score:.1f}**")
    st.markdown(f"<h3 style='color:{kleur};'> {status} </h3>", unsafe_allow_html=True)