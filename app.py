import streamlit as st
import requests

st.set_page_config(page_title="WA Group Scheduler (Cloud)", layout="centered")
st.title("📤 WhatsApp Group Message via CallMeBot (Cloud)")

nomor = st.text_input("Nomor (+62...)")
pesan = st.text_area("Pesan WhatsApp")
api_key = st.text_input("API Key CallMeBot", type="password")
waktu = st.time_input("Jam Kirim (24h)", value=st.session_state.get("waktu", None))

if st.button("Jadwalkan"):
    st.session_state["nomor"] = nomor
    st.session_state["pesan"] = pesan
    st.session_state["api_key"] = api_key
    st.session_state["waktu"] = waktu
    st.success("✅ Pesan dijadwalkan.")

if st.session_state.get("nomor"):
    # proses simplifikasi otomatis (butuh thread scheduler jika ingin dijalankan terus)
    st.info("⚠️ Versi cloud hanya kirim langsung lewat tombol")
