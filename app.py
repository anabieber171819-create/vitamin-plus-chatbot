import streamlit as st
from groq import Groq

# 1. NASTAVITEV STRANI
st.set_page_config(page_title="Vitamin+ Pomočnik", page_icon="💊")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 Vitamin+ Svetovalec")
st.markdown("Dobrodošli! Sem vaš strokovni pomočnik za vitamine in prehranska dopolnila Vitamin+.")

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
