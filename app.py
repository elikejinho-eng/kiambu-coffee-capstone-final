import streamlit as st
import random
import africastalking
from datetime import datetime

# PAGE CONFIG
st.set_page_config(
    page_title="KIAMBU RED RIPE CHERRIES",
    page_icon="🔴",
    layout="wide"
)

# STYLE - 100% RED RIPE THEME
st.markdown("""
<style>
    .stApp { background: #FFFAFA; }
    .red-banner {
        background: linear-gradient(90deg, #B71C1C, #E53935, #B71C1C);
        color: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(183,28,28,0.3);
    }
    .ripe-card {
        background: white;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 6px 20px rgba(198,40,40,0.12);
        border-left: 6px solid #C62828;
        border-top: 1px solid #FFCDD2;
        height: 170px;
        transition: transform 0.2s;
    }
    .ripe-card:hover { transform: translateY(-3px); }
    .header-box {
        background: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #B71C1C; }
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "otp_code" not in st.session_state:
    st.session_state.otp_code = ""
    st.session_state.otp_sent = False
    st.session_state.logged_in = True

# AT INITIALIZE (Optional - add your key)
try:
    africastalking.initialize(username="sandbox", api_key="atsk_YOUR_KEY_HERE")
    sms = africastalking.SMS
except:
    sms = None

# HEADER
st.markdown("""
<div class="header-box">
    <h1 style="margin:0">🔴 Kiambu Coffee Farm Dashboard</h1>
    <p style="margin:5px 0">📍 Season 2024 • Kiambu County, Kenya • 🟢 Harvest in Progress • Updated: 12 Oct 2024, 14:30</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="red-banner">
    — 100% RED RIPE CHERRIES —<br>
    <span style="font-size:14px; font-weight:normal">FRESH • RIPE • HARVEST QUALITY FOCUS • NO GREEN • NO UNRIPE</span>
</div>
""", unsafe_allow_html=True)

# RED RIPE IMAGES - ALL RED!
RED_CLOSE = "https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=400"
RED_CLUSTER = "https://images.unsplash.com/photo-1511537190424-bbbab87ac5eb?w=400"
RED_BASKET = "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400"

# ROW 1 - 3 CARDS
col1, col2, col3 = st.columns(3)

with col1:
    a, b = st.columns([1.4, 0.6])
    with a:
        st.markdown("""
        <div class="ripe-card">
            <small style="color:#666">Total Harvest</small><br>
            <h1 style="margin:0; font-size:42px">2,450 kg</h1>
            <small style="color:#C62828; font-weight:bold">+12% from last week</small><br>
            <small>🔴 All Red Ripe</small>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.image(RED_CLOSE, use_container_width=True)

with col2:
    a, b = st.columns([1.4, 0.6])
    with a:
        st.markdown("""
        <div class="ripe-card">
            <small style="color:#666">Yield Today</small><br>
            <h1 style="margin:0; font-size:42px">320 kg</h1>
            <small style="color:#C62828; font-weight:bold">+45 kg vs yesterday</small><br>
            <small>🔴 Fresh Picked</small>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.image(RED_CLUSTER, use_container_width=True)

with col3:
    a, b = st.columns([1.4, 0.6])
    with a:
        st.markdown("""
        <div class="ripe-card">
            <small style="color:#666">Quality Score</small><br>
            <h1 style="margin:0; font-size:42px">96%</h1>
            <small style="color:#C62828; font-weight:bold">Premium Grade: 84%</small><br>
            <small>🔴 Ripe Quality</small>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.image(RED_CLOSE, use_container_width=True)

st.write("")

# ROW 2 - 3 CARDS
col4, col5, col6 = st.columns(3)

with col4:
    a, b = st.columns([1.4, 0.6])
    with a:
        st.markdown("""
        <div class="ripe-card">
            <small style="color:#666">Moisture Content</small><br>
            <h1 style="margin:0; font-size:42px">11.2%</h1>
            <small style="color:#C62828; font-weight:bold">Optimal for Processing</small><br>
            <small>🔴 Ready</small>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.image(RED_CLUSTER, use_container_width=True)

with col5:
    a, b = st.columns([1.4, 0.6])
    with a:
        st.markdown("""
        <div class="ripe-card">
            <small style="color:#666">Active Pickers</small><br>
            <h1 style="margin:0; font-size:42px">18</h1>
            <small style="color:#C62828; font-weight:bold">On Field Today</small><br>
            <small>🔴 Picking Ripe</small>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.image(RED_BASKET, use_container_width=True)

with col6:
    a, b = st.columns([1.4, 0.6])
    with a:
        st.markdown("""
        <div class="ripe-card">
            <small style="color:#666">Inventory Ready</small><br>
            <h1 style="margin:0; font-size:42px">1,870 kg</h1>
            <small style="color:#C62828; font-weight:bold">Ready for Milling</small><br>
            <small>🔴 Red Only</small>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.image(RED_BASKET, use_container_width=True)

st.divider()

# CHART
st.markdown("### Weekly Harvest Trend — Red Ripe Cherries (kg)")
chart_data = {
    "Mon 180": 180,
    "Tue 210": 210,
    "Wed 260": 260,
    "Thu 275": 275,
    "Fri 280": 280,
    "Sat 310": 310,
    "Sun 320": 320
}
st.line_chart(chart_data, height=200)

st.markdown("""
<div style="display:flex; justify-content:space-between; font-size:12px; color:#666">
    <span>All data reflects only red ripe cherries • No green or unripe berries included</span>
    <span>Kiambu Coffee Farm • Traceability: Lot KF-2024-RR10</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# FOOTER BANNER WITH RED BERRIES
st.image(RED_CLOSE, caption="🔴 100% RED RIPE CHERRIES - Fresh, Ripe, Ready for Milling", use_container_width=True)

# OPTIONAL LOGIN SECTION (if you want OTP)
with st.expander("🔐 Farmer OTP Login (Optional)"):
    phone = st.text_input("Phone +254...", key="phone")
    if st.button("Generate Red Ripe Code"):
        otp = str(random.randint(100000, 999999))
        st.session_state.otp_code = otp
        st.success(f"🔴 Your RED RIPE Code: {otp}")
        if sms and phone:
            try:
                sms.send(f"Your Kiambu Red Ripe Code is {otp}", [phone])
                st.info("SMS Sent!")
            except:
                st.warning("Add your Africa's Talking key")