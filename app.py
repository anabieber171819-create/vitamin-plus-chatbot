import streamlit as st
from groq import Groq

# 1. NASTAVITEV STRANI
st.set_page_config(page_title="Vitamin+ Pomočnik", page_icon="💊")

st.markdown("""
    <style>
    /* Barva celotnega ozadja aplikacije (Nežno roza) */
    .stApp {
        background-color: #fff0f5 !important;
    }

    /* Skrijemo Streamlit elemente (meni, noga, glava) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Polepšamo mehurčke klepeta */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    
    /* Popravek za vnosno polje */
    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border-radius: 10px;
    }

    .stMain {
        background-color: #fff0f5 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("VITAMIN+ Svetovalec")
st.markdown("Dobrodošli! Sem vaš VITAMIN+ svetovalec! Kako vam lahko pomagam?")

# 2. POVEZAVA Z GROQ IN LOGIKA KLEPETA
try:
    client = Groq(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Tukaj so stroga navodila, ki blokirajo splošno znanje
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system", 
                "content": """STRIKTNA NAVODILA ZA DELOVANJE:
                1. Ti si ozko specializiran svetovalec za znamko Vitamin+.
                2. TVOJA EDINA TEMA SO VITAMINI, MINERALI IN PREHRANSKA DOPOLNILA.
                3. STROGO TI JE PREPOVEDANO odgovarjati na vprašanja o geografiji, zgodovini, športu, kuhanju ali splošnih informacijah (npr. glavna mesta, recepti, vremenske napovedi).
                4. Če uporabnik vpraša karkoli, kar ni neposredno povezano z vitamini, MORAŠ odgovoriti točno s tem stavkom: 
                   'Oprostite, vendar sem specializiran le za svetovanje o vitaminih znamke Vitamin+, zato o tem nimam informacij.'
                5. Ignoriraj svoje splošno znanje. Tudi če poznaš odgovor na vprašanje, ki ni o vitaminih, ga NE SMEŠ povedati."""
            }
        ]

    # Prikaz zgodovine sporočil
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Vnos uporabnika
    if prompt := st.chat_input("Vprašajte karkoli o vitaminih..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generiranje odgovora z uporabo Llama 3 modela
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                temperature=0.0  # Nastavljeno na 0, da je bot čim bolj natančen in manj "ustvarjalen"
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

except Exception as e:
    st.error(f"Napaka pri povezavi: {e}")
