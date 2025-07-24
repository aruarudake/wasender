import streamlit as st
import schedule
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Konfigurasi Streamlit
st.set_page_config(page_title="WhatsApp Group Scheduler", layout="centered")
st.title("📤 WhatsApp Group Message Scheduler")

# Form input pengguna
group_names_input = st.text_area("🧑‍🤝‍🧑 Nama Grup WhatsApp (satu grup per baris)")
message = st.text_area("💬 Pesan yang ingin dikirim")
schedule_time = st.text_input("🕐 Waktu Kirim (format: HH:MM)", value="07:00")
kirim_button = st.button("🚀 Jadwalkan Kirim")

# Ubah input grup menjadi list
group_names = [name.strip() for name in group_names_input.split('\n') if name.strip()]

# Inisialisasi WebDriver
@st.cache_resource
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=./user_data")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com")
    return driver

# Fungsi kirim ke semua grup
def kirim_pesan_ke_grup(group_names, message):
    for group_name in group_names:
        try:
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.clear()
            search_box.send_keys(group_name)
            time.sleep(2)

            grup = driver.find_element(By.XPATH, f'//span[@title="{group_name}"]')
            grup.click()
            time.sleep(1)

            msg_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            msg_box.send_keys(message)
            msg_box.send_keys(Keys.ENTER)
            print(f"✅ Pesan terkirim ke grup: {group_name}")
        except Exception as e:
            print(f"❌ Gagal kirim ke grup {group_name}: {e}")

# Jalankan scheduler di background
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Saat tombol ditekan
if kirim_button:
    if not group_names or not message or not schedule_time:
        st.warning("Mohon lengkapi semua field input.")
    else:
        driver = init_driver()
        st.info("Silakan scan kode QR WhatsApp jika belum login.")
        schedule.clear()
        schedule.every().day.at(schedule_time).do(kirim_pesan_ke_grup, group_names, message)
        st.success(f"Pesan akan dikirim ke {len(group_names)} grup pada {schedule_time}")

        # Jalankan scheduler di thread terpisah
        thread = threading.Thread(target=run_scheduler)
        thread.daemon = True
        thread.start()
