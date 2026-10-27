import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px

st.set_page_config(page_title="Kiambu Coffee - COMPLETE", layout="wide", page_icon="🍒")

# --- RED BANNER (SAME AS BEFORE) ---
st.markdown("""
<div style="background: linear-gradient(90deg, #b91c1c, #dc2626); padding:15px; border-radius:10px; text-align:center; color:white;">
<h2 style="margin:0; color:white;">🍒 Kiambu Coffee Farm Dashboard — 100% RED RIPE CHERRIES — 🍒</h2>
<p style="margin:5px 0 0 0;">FRESH • RIPE • HARVEST QUALITY FOCUS • NO GREEN • NO UNRIPE</p>
</div>
""", unsafe_allow_html=True)

# --- SESSION ---
if 'kitabu' not in st.session_state:
    st.session_state.kitabu = [
        {"Tarehe": "2025-10-20", "Jina": "Kamau", "Shamba": "Shamba 1", "Kilos RED": 45, "Quality": "98R/2G", "Maelezo": "Siku nzuri"},
        {"Tarehe": "2025-10-21", "Jina": "Wanjiku", "Shamba": "Shamba 2", "Kilos RED": 62, "Quality": "96R/4G", "Maelezo": "Pickers 5"},
    ]

df = pd.DataFrame(st.session_state.kitabu) if st.session_state.kitabu else pd.DataFrame()

# --- DASHBOARD - SAME AS YOUR PHOTO! ---
st.subheader("📊 DASHBOARD - Muhtasari")
c1,c2,c3,c4 = st.columns(4)
total_kg = df["Kilos RED"].sum() if not df.empty else 0
today_kg = df.iloc[-1]["Kilos RED"] if not df.empty else 0
avg_q = 96  # default
pickers = len(df)

c1.metric("Total Harvest", f"{total_kg} kg", "RED RIPE")
c2.metric("Yield Today", f"{today_kg} kg")
c3.metric("Quality Score", f"{avg_q}%", "Grade AA")
c4.metric("Entries in Kitabu", f"{len(df)}")

# Charts
if not df.empty:
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig = px.bar(df, x="Tarehe", y="Kilos RED", color="Jina", title="Mavuno kwa Siku - RED pekee", color_discrete_sequence=px.colors.sequential.Reds)
        st.plotly_chart(fig, use_container_width=True)
    with col_chart2:
        fig2 = px.pie(df, values="Kilos RED", names="Shamba", title="Kilo kwa Shamba", color_discrete_sequence=px.colors.sequential.Reds)
        st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- KITABU INPUT - FOR FARMERS ---
left, right = st.columns([1,1.2])

with left:
    st.subheader("📖 KITABU - Andika Hapa (From Memory)")
    with st.form("kitabu_form", clear_on_submit=True):
        farmer = st.text_input("1. Jina / Name", placeholder="Kamau")
        shamba = st.selectbox("2. Shamba gani?", ["Shamba 1", "Shamba 2", "Shamba ya juu", "Shamba ya chini", "Shamba ya mto"])
        kilos = st.number_input("3. Kilo ngapi RED pekee? (kumbuka kutoka memory)", min_value=0.0, step=0.5)
        col_r, col_g = st.columns(2)
        with col_r:
            reds = st.number_input("Red ngapi ulichuna?", min_value=0, value=95)
        with col_g:
            greens = st.number_input("Green ngapi? (faa 0)", min_value=0, value=0)
        tarehe = st.date_input("5. Tarehe", value=date.today())
        maelezo = st.text_area("6. Maelezo", placeholder="Mvua? Pickers wangapi?", height=70)
        save = st.form_submit_button("💾 ANDIKA KITABUNI - SAVE", use_container_width=True, type="primary")
        if save:
            if farmer and kilos > 0:
                st.session_state.kitabu.append({"Tarehe": str(tarehe), "Jina": farmer, "Shamba": shamba, "Kilos RED": kilos, "Quality": f"{reds}R/{greens}G", "Maelezo": maelezo})
                st.success(f"Sawa! {kilos}kg saved! Dashboard updated! ✅")
                st.balloons()
                st.rerun()
            else:
                st.error("Weka jina na kilos!")

with right:
    st.subheader("📖 Kitabu Chako - Inaonekana Kama Kitabu")
    if st.session_state.kitabu:
        st.dataframe(df, use_container_width=True, height=400)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Pakua Kitabu (Excel)", csv, "kiambu_kitabu_red_ripe.csv", "text/csv", use_container_width=True)
        if st.button("🗑️ Futa Kitabu"):
            st.session_state.kitabu = []
            st.rerun()
    else:
        st.info("Kitabu tupu - Anza kuandika kushoto 👈")

st.divider()
st.caption("COMPLETE APP: Dashboard (Top) + Kitabu Input (Bottom) | 100% RED RIPE | For Kiambu Farmers using Kitabu + Memory")