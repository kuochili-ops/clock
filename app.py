import streamlit as st
from streamlit_folium import st_folium
import folium
import flip_clock  # 確保您的檔名是 flip_clock.py

st.set_page_config(page_title="𓃥白六世界時鐘", layout="centered")

# --- 隱藏 Streamlit 預設元件與自定義按鈕樣式 ---
st.markdown("""
    <style>
    .stButton { display: none; } /* 隱藏觸發按鈕 */
    div.stDialog > div { background-color: #1a1a1a; color: white; } /* 彈窗背景深色化 */
    </style>
""", unsafe_allow_html=True)

API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"

@st.dialog("🌍 全球時空導航")
def show_map_dialog():
    # 建立深色地圖
    m = folium.Map(
        location=[25, 10], zoom_start=1.5, 
        tiles="CartoDB dark_matter", zoom_control=False,
        no_wrap=True, max_bounds=True
    )
    
    # 遍歷全城市並加上標記
    for c in flip_clock.ALL_CITIES:
        # VIP 城市用橘色，一般城市用藍色
        color = "#FF8C00" if c.get("vip") else "#00d4ff"
        folium.CircleMarker(
            location=[c["lat"], c["lon"]], 
            radius=6, 
            color=color, 
            fill=True, 
            fill_opacity=0.9, 
            popup=c["zh"],
            tooltip=c["zh"] # 加入提示文字，滑鼠經過就會顯示
        ).add_to(m)
    
    # 渲染地圖
    selected = st_folium(m, height=400, width=400, key="modal_map", returned_objects=["last_object_clicked_popup"])
    
    # 偵測點擊
    if selected.get("last_object_clicked_popup"):
        name = selected["last_object_clicked_popup"]
        idx = next((i for i, item in enumerate(flip_clock.ALL_CITIES) if item["zh"] == name), 0)
        st.session_state.target_idx = idx
        st.rerun()

# 這是隱藏的觸發機制，當 JS 點擊隱藏按鈕時啟動
if st.button("TRIGGER_MAP"):
    show_map_dialog()

# 取得當前城市索引並渲染時鐘
current_idx = st.session_state.get('target_idx', 0)
flip_clock.render_flip_clock(API_KEY, current_idx)
