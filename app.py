import streamlit as st
from openai import OpenAI

# 1. NASTAVITVE STRANI IN VIDEZ (Usklajeno z Vitamin+)
st.set_page_config(page_title="Vitamin+ Pomočnik", page_icon="💊")

# Prilagoditev barv - tukaj lahko kasneje spremeniš barve, da bodo kot na tvoji strani
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .stChatMessage {
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 Vitamin+ Svetovalec")
st.markdown("Dobrodošli! Sem vaš strokovni pomočnik za vitamine in prehranska dopolnila Vitamin+.")

# 2. VARNOST: API ključ iz Streamlit Secrets
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("Napaka: API ključ ni nastavljen v Streamlit Secrets!")
    st.stop()

# 3. UPRAVLJANJE S SPOMINOM (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """Ti si strokovni svetovalec za spletno trgovino Vitamin+. 
            Tvoja pravila:
            1. Govoriš izključno v slovenščini, bodi vljuden, strokoven in prijazen.
            2. Tvoja specializacija so vitamini, minerali in prehranska dopolnila.
            3. Če te uporabnik vpraša karkoli, kar ni povezano z vitamini, zdravjem ali ponudbo Vitamin+ (npr. o športnih rezultatih, politiki ali receptih za torte), 
               moraš odgovoriti: 'Oprostite, sem specializiran svetovalec za Vitamin+, zato vam lahko pomagam le pri vprašanjih o vitaminih in prehranskih dopolnilih.'
            4. Odgovori naj bodo pregledni. Če naštevaš prednosti vitamina, uporabi alineje.
            5. Vedno poudari, da so tvoji nasveti informativni in naj se uporabnik o zdravju posvetuje z zdravnikom."""
        }
    ]

# Prikaz zgodovine klepeta
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. POLJE ZA VNOS (Interakcija)
if prompt := st.chat_input("Kako vam lahko danes pomagam pri izbiri vitaminov?"):
    # Shrani vprašanje
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Odgovor bota
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
    
    # Shrani odgovor v spomin seje
    st.session_state.messages.append({"role": "assistant", "content": msg})

    
