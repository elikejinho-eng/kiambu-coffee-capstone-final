import streamlit as st
import pandas as pd
import pyotp
import sqlite3
import hashlib

st.set_page_config(page_title="KIAMBU COFFEE CAPSTONE", page_icon="🍒", layout="wide")

# --- COFFEE GRAPHICS THEME ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(255,253,245,0.85), rgba(232,245,233,0.9)), url("https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #E8F5E9 100%);
        border: 3px solid #2E7D32;
        border-left: 8px solid #B71C1C;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(46,125,50,0.2);
    }
    div[data-testid="stMetric"] label { color: #1B5E20 !important; font-weight: bold !important; }
    .stButton > button {
        background: linear-gradient(45deg, #2E7D32, #B71C1C);
        color: white !important;
        border-radius: 25px;
        font-weight: bold;
        width: 100%;
        padding: 12px;
        font-size: 18px;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 50%, #4A2511 100%);
    }
    section[data-testid="stSidebar"] * { color: white !important; }
</style>

<div style='text-align:center; background: linear-gradient(90deg, #1B5E20, #2E7D32, #B71C1C); padding:25px; border-radius:25px; margin-bottom:25px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
    <h1 style='color:#FFEBEE; font-size:3em; margin:0; text-shadow: 2px 2px 4px black;'>🌿🍒 KIAMBU COFFEE 🍒🌿</h1>
    <p style='color:#C8E6C9; font-size:1.3em; margin:5px;'>☕ From Cherry to Cup | Premium AA | Kiambu County ☕</p>
    <p style='color:#FFCDD2;'>🍒🔴 Ripe Berries • 🌿🟢 Fresh Leaves • 🟤☕ Rich Aroma</p>
</div>
""", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect('secure_users.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT, totp_secret TEXT, role TEXT)")
    users = [
        ("admin", hashlib.sha256("KiambuAdmin@2024!".encode()).hexdigest(), "DVQRSLYOH4SXNKAPECL7PES7RJQZHOFS", "admin"),
        ("Kitonyi", hashlib.sha256("Kitonyi@2024".encode()).hexdigest(), "DVQRSLYOH4SXNKAPECL7PES7RJQZHOFS", "farmer"),
    ]
    for u in users:
        try: c.execute("INSERT INTO users VALUES (?,?,?,?)", u)
        except: pass
    conn.commit(); conn.close()
init_db()

if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'step1_ok' not in st.session_state: st.session_state.step1_ok=False

def login_step1(username, password):
    conn = sqlite3.connect('secure_users.db'); c = conn.cursor()
    c.execute("SELECT password_hash, totp_secret, role FROM users WHERE username=?", (username,))
    row=c.fetchone(); conn.close()
    if row and row[0]==hashlib.sha256(password.encode()).hexdigest(): return row[1], row[2]
    return None, None

if not st.session_state.logged_in:
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style='background: white; padding:30px; border-radius:25px; border:4px solid #2E7D32; text-align:center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <div style='font-size:5em;'>☕🍒🌿</div>
            <h2 style='color:#1B5E20;'>Kiambu Coffee Login</h2>
            <p style='color:#B71C1C; font-weight:bold;'>🔴 Ripe Berries • 🟢 Fresh Leaves</p>
        </div>
        """, unsafe_allow_html=True)
        username=st.text_input("👤 Username - try Kitonyi")
        password=st.text_input("🔑 Password", type="password")
        if st.button("🌿 Login Step 1 - Green Leaves"):
            secret,role=login_step1(username,password)
            if secret:
                st.session_state.temp_secret=secret; st.session_state.temp_role=role
                st.session_state.temp_username=username; st.session_state.step1_ok=True
                st.success("✅ Step 1 OK! Now enter 2FA")
            else: st.error("❌ Wrong login")
        if st.session_state.step1_ok:
            st.markdown("### 🍒 Step 2: Enter Red Berry Code (2FA)")
            code=st.text_input("6-digit code from terminal", max_chars=6)
            if st.button("🍒 Verify & Enter Farm"):
                totp=pyotp.TOTP(st.session_state.temp_secret)
                if totp.verify(code):
                    st.session_state.logged_in=True
                    st.session_state.username=st.session_state.temp_username
                    st.session_state.role=st.session_state.temp_role
                    st.rerun()
                else: st.error("❌ Wrong code - get new one from terminal")
    st.stop()

# --- LOGGED IN DASHBOARD ---
with st.sidebar:
    st.markdown(f"# 🌿🍒 Kiambu Coffee\n### Welcome {st.session_state.username} ☕")
    st.image("https://images.unsplash.com/photo-1504630083235-1413345e8fe4?auto=format&fit=crop&w=400&q=80", caption="☕ Kiambu AA Coffee Beans")
    st.markdown("---")
    st.markdown("**🌿 Sub-Counties:**\n- Gatundu\n- Kiambaa\n- Githunguri")
    if st.button("🚪 Logout"):
        st.session_state.logged_in=False; st.session_state.step1_ok=False; st.rerun()

st.markdown(f"## 🌿 Welcome {st.session_state.username} to Your Farm 🍒")
st.markdown("### 📊 Dashboard - Green Leaves and Red Berries")

c1,c2,c3,c4=st.columns(4)
c1.metric("🌿 Yield", "450kg", "↑ 12%"); c2.metric("💰 Profit", "Ksh45k", "↑ 8%")
c3.metric("🍒 Price", "Ksh120", "↑ 5%"); c4.metric("🌧️ Rain", "150mm", "Good")

st.divider()
left,right=st.columns([2,1])
with left:
    st.subheader("📈 Sub-County Profits - Coffee Growth")
    df=pd.DataFrame({
        "Sub-County":["Gatundu","Kiambaa","Githunguri","Lari"],
        "Profit Ksh":[45000,38000,42000,36000],
        "Berries":["🍒","🌿","🍒","🌿"]
    })
    st.bar_chart(df, x="Sub-County", y="Profit Ksh", color="#B71C1C")
    st.dataframe(df, use_container_width=True)

with right:
    st.markdown("### 🚨 Farm Alerts")
    st.success("🌿✅ Fertilizer needed - Kiambaa - Apply NPK")
    st.error("🍒⚠️ Berry Alert - Gatundu - Ready to harvest!")
    st.warning("🌧️ Rain expected - Githunguri - 150mm")
    st.info("☕ Quality Check - Lari - Grade AA")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #E8F5E9, #FFEBEE); padding:15px; border-radius:15px; border:2px solid #2E7D32;'>
    <h4 style='color:#1B5E20;'>🍒 Today's Harvest</h4>
    <p>🌿 <b>Gatundu</b> - 450kg - <span style='color:green;'>Premium</span></p>
    <p>🍒 <b>Kiambaa</b> - 380kg - <span style='color:red;'>Ripe</span></p>
    <p>🌱 <b>Githunguri</b> - 420kg - <span style='color:brown;'>AA</span></p>
    </div>
    """, unsafe_allow_html=True)