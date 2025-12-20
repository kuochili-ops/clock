import streamlit as st
from streamlit_folium import st_folium
import folium
from datetime import datetime
import pytz

st.set_page_config(page_title="𓃥白六世界探索器", layout="centered")

# --- 1. 核心資料與 API 配置 ---
API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"

# 預設與地圖城市清單
DEFAULT_CITIES = [
    {"name": "Taipei", "zh": "臺 北", "tz": "Asia/Taipei", "lat": 25.0330, "lon": 121.5654, "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
    {"name": "Los Angeles", "zh": "洛杉磯", "tz": "America/Los_Angeles", "lat": 34.0522, "lon": -118.2437, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/HollywoodSign.jpg/1280px-HollywoodSign.jpg"},
    {"name": "London", "zh": "倫 敦", "tz": "Europe/London", "lat": 51.5074, "lon": -0.1278, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"},
    {"name": "Tokyo", "zh": "東 京", "tz": "Asia/Tokyo", "lat": 35.6895, "lon": 139.6917, "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1000&q=80"},
    {"name": "Paris", "zh": "巴 黎", "tz": "Europe/Paris", "lat": 48.8566, "lon": 2.3522, "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1000&q=80"}
]

# --- 2. Session State 初始化 ---
if 'current_city' not in st.session_state:
    st.session_state.current_city = DEFAULT_CITIES[0]

# --- 3. 地圖模組 (中間 1/3 佈局) ---
def map_section():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        m = folium.Map(
            location=[20, 0], zoom_start=1, 
            tiles="CartoDB dark_matter", 
            zoom_control=False, scrollWheelZoom=False
        )
        for c in DEFAULT_CITIES:
            folium.CircleMarker(
                location=[c["lat"], c["lon"]],
                radius=7, color="#00d4ff", fill=True, popup=c["name"]
            ).add_to(m)
        
        # 捕捉地圖點擊
        map_data = st_folium(m, height=200, width=300, key="main_map")
        if map_data.get("last_object_clicked_popup"):
            city_name = map_data["last_object_clicked_popup"]
            new_city = next((item for item in DEFAULT_CITIES if item["name"] == city_name), None)
            if new_city and new_city["name"] != st.session_state.current_city["name"]:
                st.session_state.current_city = new_city
                st.rerun()

# --- 4. 物理翻板時鐘 HTML/JS ---
def clock_section(city):
    flip_html = f"""
    <style>
        .app-container {{ display: flex; flex-direction: column; align-items: center; gap: 10px; font-family: sans-serif; }}
        .flip-card {{ position: relative; background: #1a1a1a; border-radius: 6px; font-weight: 900; color: #fff; overflow: hidden; }}
        .row-flex {{ display: flex; justify-content: space-between; width: 100%; gap: 10px; }}
        .info-card {{ flex: 1; height: 70px; font-size: 1.8rem; display: flex; align-items: center; justify-content: center; }}
        .time-row {{ display: flex; gap: 5px; align-items: center; }}
        .time-card {{ width: 80px; height: 120px; font-size: 80px; }}
        .city-photo {{ 
            width: 100%; height: 200px; border-radius: 12px; 
            background: url('{city["img"]}') center/cover; position: relative; overflow: hidden;
        }}
        .glass-vignette {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%);
            background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.4) 100%);
        }}
        /* 物理遮蔽關鍵 CSS */
        .half {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
        .top {{ top: 0; border-bottom: 1px solid #000; align-items: flex-end; }}
        .bottom {{ bottom: 0; align-items: flex-start; }}
        .text-box {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; }}
        .top .text-box {{ bottom: -100%; }} .bottom .text-box {{ top: -100%; }}
    </style>

    <div class="app-container">
        <div class="row-flex">
            <div class="flip-card info-card">{city["zh"]}</div>
            <div class="flip-card info-card">{city["name"]}</div>
        </div>
        <div class="time-row" id="clock-trigger">
            <div class="flip-card time-card" id="h0"></div>
            <div class="flip-card time-card" id="h1"></div>
            <div style="font-size: 40px; color: white;">:</div>
            <div class="flip-card time-card" id="m0"></div>
            <div class="flip-card time-card" id="m1"></div>
        </div>
        <div class="city-photo"><div class="glass-vignette"></div></div>
    </div>

    <script>
        function updateFlip(id, val) {{
            const el = document.getElementById(id);
            el.innerHTML = `<div class="half top"><div class="text-box">${{val}}</div></div>
                            <div class="half bottom"><div class="text-box">${{val}}</div></div>`;
        }}
        function tick() {{
            const now = new Date(new Date().toLocaleString("en-US", {{timeZone: "{city["tz"]}"}}));
            const h = String(now.getHours()).padStart(2, '0');
            const m = String(now.getMinutes()).padStart(2, '0');
            updateFlip('h0', h[0]); updateFlip('h1', h[1]);
            updateFlip('m0', m[0]); updateFlip('m1', m[1]);
        }}
        setInterval(tick, 1000); tick();
    </script>
    """
    st.components.v1.html(flip_html, height=500)

# --- 5. 渲染頁面 ---
st.markdown("<h2 style='text-align: center; color: #444;'>𓃥 白 六 世 界 探 索 器</h2>", unsafe_allow_html=True)
map_section()
st.markdown("---")
clock_section(st.session_state.current_city)
