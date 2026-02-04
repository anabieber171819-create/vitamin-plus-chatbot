import streamlit as st
from groq import Groq

# 1. NASTAVITEV STRANI
st.set_page_config(page_title="Vitamin+ Pomočnik", page_icon="💊")

st.markdown("""
    <style>
    /* 1. Barva celotnega ozadja aplikacije (Nežno roza) */
    .stApp {
        background-color: #fff0f5 !important;
    }

    /* 2. Skrijemo vse Streamlit elemente (meni, noga, glava) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 3. Odstranimo belo barvo iz ozadja klepeta in polepšamo mehurčke */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    
    /* 4. Popravek za vnosno polje na dnu - da ni belega roba */
    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border-radius: 10px;
    }

    /* 5. Prisila roza barve za stranske dele */
    .stMain {
        background-color: #fff0f5 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("VITAMIN+ Svetovalec")
st.markdown("Dobrodošli! Sem vaš VITAMIN+ svetovalec! Kako vam lahko pomagam?")

# 2. POVEZAVA Z GROQ (Zastonj alternativa)
try:
    client = Groq(api_key=st.secrets["OPENAI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Ti si strokovni svetovalec za vitamine znamke Vitamin+. Odgovarjaj prijazno, strokovno in v slovenščini."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Vprašajte karkoli o vitaminih..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

except Exception as e:
    st.error(f"Napaka: {e}")


