import streamlit as st
from streamlit_folium import st_folium
import folium
import flip_clock  # 確保與上面的模組檔名一致

st.set_page_config(
    page_title="𓃥白六世界時鐘", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 徹底清除 Streamlit 預設邊距，防止手機切邊 ---
st.markdown("""
    <style>
    /* 移除頂部與側邊留白 */
    .block-container { padding: 0rem 0rem !important; max-width: 100% !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    .stButton { display: none; } /* 隱藏背後觸發地圖用的按鈕 */
    div.stDialog > div { background-color: #0e1117; color: white; border: 1px solid #333; }
    iframe { width: 100vw; border: none; }
    </style>
""", unsafe_allow_html=True)

API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"

@st.dialog("🌍 全球時空導航")
def show_map_dialog():
    m = folium.Map(
        location=[20, 10], zoom_start=1.2, 
        tiles="CartoDB dark_matter", zoom_control=False,
        no_wrap=True, max_bounds=True
    )
    for c in flip_clock.ALL_CITIES:
        color = "#FF8C00" if c.get("vip") else "#00d4ff"
        folium.CircleMarker(
            location=[c["lat"], c["lon"]], 
            radius=8, color=color, fill=True, 
            fill_opacity=0.8, popup=c["zh"],
            tooltip=c["zh"]
        ).add_to(m)
    
    selected = st_folium(m, height=400, width="100%", key="modal_map", returned_objects=["last_object_clicked_popup"])
    if selected.get("last_object_clicked_popup"):
        name = selected["last_object_clicked_popup"]
        idx = next((i for i, item in enumerate(flip_clock.ALL_CITIES) if item["zh"] == name), 0)
        st.session_state.target_idx = idx
        st.rerun()

if st.button("TRIGGER_MAP"):
    show_map_dialog()

current_idx = st.session_state.get('target_idx', 0)
flip_clock.render_flip_clock(API_KEY, current_idx)
