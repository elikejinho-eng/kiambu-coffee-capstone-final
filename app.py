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
        # ================= START LINE 91 =================
        if st.session_state.step1_ok:
            st.markdown("### 🔴 Step 2: Red Berry Phone Verification")
            st.info("Enter your phone to get M-Pesa style OTP code")

            # Phone number input
            phone = st.text_input(
                "📱 Enter your Safaricom number",
                placeholder="+254712345678",
                value=st.session_state.get("temp_phone", "")
            )

            # Button 1: Send OTP
            if st.button("📱 Send Red Berry Code via SMS"):
                if not phone.startswith("+254"):
                    st.error("Use format +254712345678")
                else:
                    import africastalking
                    import random

                    # Initialize Africa's Talking
                    africastalking.initialize("sandbox", "YOUR_NEW_API_KEY_HERE")
                    sms = africastalking.SMS

                    # Generate 6-digit code
                    otp_code = str(random.randint(100000, 999999))
                    st.session_state.phone_otp = otp_code
                    st.session_state.temp_phone = phone
                    st.session_state.otp_sent = True

                    # Send SMS (in sandbox, check Dashboard > SMS > Logs)
                    try:
                        response = sms.send(f"KIAMBU COFFEE: Your Red Berry code is {otp_code}. Valid 5 min.", [phone])
                        st.success(f"✅ Code sent to {phone}")
                        st.warning(f"SANDBOX MODE: Your code is {otp_code} (Check AT Dashboard -> SMS -> Logs)")
                    except Exception as e:
                        # Even if SMS fails, show code for testing
                        st.success(f"✅ Code Generated!")
                        st.warning(f"SANDBOX MODE: Your code is {otp_code}")
                        st.write(f"Error (normal in sandbox): {e}")

            # Show OTP input only if code was sent
            if st.session_state.get("otp_sent"):
                st.divider()
                sms_code = st.text_input(
                    "🔑 Enter 6-digit code from SMS",
                    placeholder="e.g. 834921",
                    type="password"
                )

                # Button 2: Verify and Enter Farm
                if st.button("🔐 Verify & Enter Farm"):
                    if sms_code == st.session_state.get("phone_otp"):
                        # SUCCESS - LOG FARMER IN
                        st.session_state.logged_in = True
                        st.session_state.username = st.session_state.temp_username
                        st.session_state.role = st.session_state.temp_role
                        st.session_state.step1_ok = False
                        st.session_state.otp_sent = False

                        st.success(f"✅ Welcome {st.session_state.username} to Kiambu Coffee Farm!")
                        st.balloons()
                        st.rerun()
                    elif sms_code == "":
                        st.error("Please enter the code")
                    else:
                        st.error("❌ Wrong code. You entered {sms_code}, expected {st.session_state.get('phone_otp')}")
                        st.info("Click 'Send Red Berry Code via SMS' to get new code")
        # ================= END OF FILE =================