import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv


st.set_page_config(layout="wide")

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ API Key Groq belum ditemukan. Pastikan file .env berisi GROQ_API_KEY.")
    st.stop()

client = Groq(api_key=api_key)

# --- Inisialisasi session ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Tampilan CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #E3F2F1 0%, #D7E8F5 100%);
    color: black;
}

[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 10px 15px;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: #000000;
}

[data-testid="stChatInput"] textarea {
    border-radius: 10px !important;
    border: 1px solid #A3D5D3;
    background-color: #fefefe;
}

textarea {
    color: black !important;        /* teks user jadi hitam */
    background-color: #fefefe;      /* latar belakang kotak input */
    border-radius: 10px !important;
    border: 1px solid #A3D5D3;      /* optional, biar kotak terlihat */
}


button[kind="primary"] {
    background-color: #A3D5D3 !important;
    color: #003f3c !important;
    border-radius: 10px !important;
    font-weight: bold !important;
}
button[kind="primary"]:hover {
    background-color: #7DC9C7 !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# --- Judul ---
col1, col2 = st.columns([1, 3])  # [1,3] = rasio lebar kolom (gambar:teks)

with col1:
    st.image("images/mental_health1.jpg", width=300)

with col2:
    st.title("🧠💬 Chatbot Psikologi : ")
    st.title("Ruang Cerita dan Refleksi  ")
    st.subheader("Hai! Aku Minsi 🙋‍♀️")
    st.subheader("Aku di sini untuk mendengarkan cerita Kamu😊")

# --- Tampilkan seluruh riwayat chat ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input chat interaktif ---
user_input = st.chat_input("Ceritakan perasaan kamu hari ini...")

if user_input:
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Balasan chatbot
    with st.chat_message("assistant"):
        with st.spinner("Chatbot sedang mengetik..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Kamu adalah konselor virtual yang empatik dan membantu pengguna memahami perasaannya seperti seorang konselor psikologi."},
                    *st.session_state.messages
                ]
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)

    # Simpan balasan ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
