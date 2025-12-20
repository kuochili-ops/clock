import streamlit as st
from streamlit_folium import st_folium
import folium
import pytz

st.set_page_config(page_title="𓃥白六世界時鐘", layout="centered")

# --- 1. 核心資料 ---
CITIES = [
    {"name": "Taipei", "zh": "臺 北", "tz": "Asia/Taipei", "lat": 25.033, "lon": 121.565, "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
    {"name": "Kaohsiung", "zh": "高 雄", "tz": "Asia/Taipei", "lat": 22.627, "lon": 120.301, "img": "https://images.chinatimes.com/newsphoto/2023-01-06/656/20230106004870.jpg"},
    {"name": "Los Angeles", "zh": "洛杉磯", "tz": "America/Los_Angeles", "lat": 34.052, "lon": -118.243, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/HollywoodSign.jpg/1280px-HollywoodSign.jpg"},
    {"name": "Osaka", "zh": "大 阪", "tz": "Asia/Tokyo", "lat": 34.693, "lon": 135.502, "img": "https://images.unsplash.com/photo-1590559899731-a382839e5549?w=1200&q=80"},
    {"name": "San Francisco", "zh": "舊金山", "tz": "America/Los_Angeles", "lat": 37.774, "lon": -122.419, "img": "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?w=1200&q=80"},
    {"name": "Sapporo", "zh": "札 幌", "tz": "Asia/Tokyo", "lat": 43.061, "lon": 141.354, "img": "https://hokkaido-labo.com/wp-content/uploads/2014/09/140964647192343.jpg"},
    {"name": "Shanghai", "zh": "上 海", "tz": "Asia/Shanghai", "lat": 31.230, "lon": 121.473, "img": "https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2?w=1000&q=80"},
    {"name": "London", "zh": "倫 敦", "tz": "Europe/London", "lat": 51.507, "lon": -0.127, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"}
]

# 初始化狀態
if 'idx' not in st.session_state: st.session_state.idx = 0

# --- 2. 彈出式地圖組件 ---
@st.dialog("🌍 全球城市探索器")
def pop_map():
    st.write("點擊藍色錨點切換城市，選中後會自動更新時鐘。")
    m = folium.Map(location=[20, 0], zoom_start=1, tiles="CartoDB dark_matter", zoom_control=False)
    for i, c in enumerate(CITIES):
        folium.CircleMarker(
            location=[c["lat"], c["lon"]], radius=8, color="#00d4ff", fill=True, popup=c["name"]
        ).add_to(m)
    
    selected = st_folium(m, height=300, width=440, key="modal_map")
    
    # 邏輯：從地圖點選城市
    if selected.get("last_object_clicked_popup"):
        city_name = selected["last_object_clicked_popup"]
        new_idx = next((i for i, item in enumerate(CITIES) if item["name"] == city_name), None)
        if new_idx is not None:
            st.session_state.idx = new_idx
            st.rerun()

# --- 3. 核心介面 (主時鐘) ---
c = CITIES[st.session_state.idx]

# 點擊翻板切換城市的橋樑：利用 invisible button 或 JS postMessage
# 這裡最直接的方式是保留您的 HTML 點擊切換邏輯
html_clock = f"""
<div id="clock-container" style="cursor: pointer;">
    <style>
        .app-container {{ display: flex; flex-direction: column; align-items: center; gap: 8px; font-family: sans-serif; }}
        .flip-card {{ position: relative; background: #1a1a1a; border-radius: 6px; font-weight: 900; color: #fff; overflow: hidden; }}
        .row-flex {{ display: flex; justify-content: space-between; width: 100%; gap: 8px; }}
        .info-card {{ flex: 1; height: 80px; font-size: 2rem; display: flex; align-items: center; justify-content: center; }}
        .time-row {{ display: flex; gap: 4px; align-items: center; justify-content: center; }}
        .time-card {{ width: 110px; height: 180px; font-size: 140px; }}
        
        .photo-banner {{
            position: relative; width: 100%; height: 280px; border-radius: 15px; margin-top: 10px;
            background: url('{c['img']}') center/cover; overflow: hidden;
        }}
        .glass-vignette {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%);
            background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.4) 100%);
        }}
        
        /* 物理遮蔽核心 */
        .half {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
        .top {{ top: 0; border-bottom: 1px solid #000; align-items: flex-end; }}
        .bottom {{ bottom: 0; align-items: flex-start; }}
        .text-box {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; }}
        .top .text-box {{ bottom: -100%; }} .bottom .text-box {{ top: -100%; }}
    </style>

    <div class="app-container" onclick="window.parent.postMessage('next_city', '*')">
        <div class="row-flex">
            <div class="flip-card info-card">{c['zh']}</div>
            <div class="flip-card info-card">{c['name']}</div>
        </div>
        <div class="time-row">
            <div class="flip-card time-card" id="h0"></div>
            <div class="flip-card time-card" id="h1"></div>
            <div style="font-size: 60px; color: white; font-weight: bold; margin-bottom: 15px;">:</div>
            <div class="flip-card time-card" id="m0"></div>
            <div class="flip-card time-card" id="m1"></div>
        </div>
        <div class="photo-banner"><div class="glass-vignette"></div></div>
    </div>

    <script>
        function updateFlip(id, val) {{
            const el = document.getElementById(id);
            el.innerHTML = `<div class="half top"><div class="text-box">${{val}}</div></div>
                            <div class="half bottom"><div class="text-box">${{val}}</div></div>`;
        }}
        function tick() {{
            const now = new Date(new Date().toLocaleString("en-US", {{timeZone: "{c['tz']}"}}));
            const h = String(now.getHours()).padStart(2, '0');
            const m = String(now.getMinutes()).padStart(2, '0');
            updateFlip('h0', h[0]); updateFlip('h1', h[1]);
            updateFlip('m0', m[0]); updateFlip('m1', m[1]);
        }}
        setInterval(tick, 1000); tick();
    </script>
</div>
"""

# 渲染翻板時鐘
st.components.v1.html(html_clock, height=580)

# --- 4. 透明/隱藏的地圖觸發按鈕 ---
# 利用 CSS 絕對定位，將 Streamlit 按鈕疊加在照片左下角附近
st.markdown("""
    <style>
    div[st-vertical-layout="true"] > div:nth-child(3) {
        position: relative;
    }
    .stButton>button {
        position: absolute;
        bottom: 80px;  /* 剛好在照片區塊的左下角 */
        left: 20px;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        font-size: 0.7rem !important;
        border-radius: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("🗺️ EXPLORE"):
    pop_map()

# 監聽來自 HTML 的點擊事件（循環切換城市）
from streamlit_js_eval import streamlit_js_eval
# 這裡簡單處理：點擊翻板切換到下一個 idx
# 註：如果您之前是用 st.button 循環，這段邏輯會直接觸發
if st.button("切換下一個城市 (隱藏版)", key="hidden_next", help="點擊時鐘翻板即可切換"):
    st.session_state.idx = (st.session_state.idx + 1) % len(CITIES)
    st.rerun()
