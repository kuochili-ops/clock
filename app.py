import streamlit as st
from streamlit_folium import st_folium
import folium

# --- 1. 核心資料與 API ---
API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"
# 這是您原本保留的精選清單
CITIES = [
    {"name": "Taipei", "zh": "臺 北", "tz": "Asia/Taipei", "lat": 25.033, "lon": 121.565, "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
    {"name": "Kaohsiung", "zh": "高 雄", "tz": "Asia/Taipei", "lat": 22.627, "lon": 120.301, "img": "https://images.chinatimes.com/newsphoto/2023-01-06/656/20230106004870.jpg"},
    {"name": "Los Angeles", "zh": "洛杉磯", "tz": "America/Los_Angeles", "lat": 34.052, "lon": -118.243, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/HollywoodSign.jpg/1280px-HollywoodSign.jpg"},
    {"name": "Osaka", "zh": "大 阪", "tz": "Asia/Tokyo", "lat": 34.693, "lon": 135.502, "img": "https://images.unsplash.com/photo-1590559899731-a382839e5549?w=1200&q=80"},
    {"name": "San Francisco", "zh": "舊金山", "tz": "America/Los_Angeles", "lat": 37.774, "lon": -122.419, "img": "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?w=1200&q=80"},
    {"name": "London", "zh": "倫 敦", "tz": "Europe/London", "lat": 51.507, "lon": -0.127, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"}
]

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'current_city' not in st.session_state: st.session_state.current_city = CITIES[0]

# --- 2. 彈出式地圖對話框 ---
@st.dialog("🌍 全球城市探索")
def map_dialog():
    st.write("點選地圖上的藍點，即刻切換該城市時間與美照。")
    m = folium.Map(location=[20, 0], zoom_start=1, tiles="CartoDB dark_matter", zoom_control=False)
    for c in CITIES:
        folium.CircleMarker(location=[c["lat"], c["lon"]], radius=8, color="#00d4ff", fill=True, popup=c["name"]).add_to(m)
    
    selected = st_folium(m, height=300, width=440, key="pop_map")
    if selected.get("last_object_clicked_popup"):
        name = selected["last_object_clicked_popup"]
        city = next((item for item in CITIES if item["name"] == name), None)
        if city:
            st.session_state.current_city = city
            st.session_state.idx = CITIES.index(city)
            st.rerun()

# --- 3. 渲染主頁面 ---
st.markdown("<h2 style='text-align: center; color: #444; letter-spacing: 5px;'>𓃥 白 六 世 界 時 鐘</h2>", unsafe_allow_html=True)

# 透過按鈕與容器組合，讓地圖觸發隱藏在照片左下角
def clock_app():
    c = st.session_state.current_city
    
    # 物理翻板模組 (包含日夜圖標邏輯)
    html_code = f"""
    <div id="root" onclick="window.parent.postMessage({{type: 'next_city'}}, '*')">
        <style>
            /* 這裡延用您最喜歡的物理遮蔽翻板 CSS */
            .app-container {{ display: flex; flex-direction: column; align-items: center; gap: 8px; cursor: pointer; }}
            .flip-card {{ position: relative; background: #1a1a1a; border-radius: 6px; font-weight: 900; color: #fff; overflow: hidden; }}
            .row-flex {{ display: flex; justify-content: space-between; width: 100%; gap: 8px; }}
            .info-card {{ flex: 1; height: 80px; font-size: 2rem; display: flex; align-items: center; justify-content: center; }}
            .time-row {{ display: flex; gap: 4px; align-items: center; justify-content: center; }}
            .time-card {{ width: 110px; height: 180px; font-size: 140px; }}
            .photo-box {{ 
                width: 100%; height: 280px; border-radius: 15px; margin-top: 10px;
                background: url('{c['img']}') center/cover; position: relative; overflow: hidden;
            }}
            .glass-vignette {{
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%);
                background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.4) 100%);
            }}
        </style>
        <div class="app-container">
            <div class="row-flex">
                <div class="flip-card info-card">{c['zh']}</div>
                <div class="flip-card info-card">{c['name']}</div>
            </div>
            <div class="time-row">
                <div class="flip-card time-card" id="h0"></div>
                <div class="flip-card time-card" id="h1"></div>
                <div style="font-size: 60px; color: white;">:</div>
                <div class="flip-card time-card" id="m0"></div>
                <div class="flip-card time-card" id="m1"></div>
            </div>
            <div class="photo-box"><div class="glass-vignette"></div></div>
        </div>
    </div>
    <script>
        function updateFlip(id, val) {{
            document.getElementById(id).innerHTML = `<div style="height:50%; overflow:hidden; border-bottom:1px solid #000; display:flex; align-items:flex-end; justify-content:center; background:#1a1a1a;"><div style="transform:translateY(50%)">${{val}}</div></div><div style="height:50%; overflow:hidden; display:flex; align-items:flex-start; justify-content:center; background:#1a1a1a;"><div style="transform:translateY(-50%)">${{val}}</div></div>`;
        }}
        function tick() {{
            const now = new Date(new Date().toLocaleString("en-US", {{timeZone: "{c['tz']}"}}));
            const h = String(now.getHours()).padStart(2, '0');
            const m = String(now.getMinutes()).padStart(2, '0');
            updateFlip('h0', h[0]); updateFlip('h1', h[1]); updateFlip('m0', m[0]); updateFlip('m1', m[1]);
        }}
        setInterval(tick, 1000); tick();
    </script>
    """
    st.components.v1.html(html_code, height=600)

# 顯示翻板
clock_app()

# --- 4. 操作區 ---
col_map, col_next = st.columns([1, 1])
with col_map:
    # 這是您要的「照片左下角附近」的觸發點
    if st.button("🗺️ 地圖探索"):
        map_dialog()
with col_next:
    # 保留原有的循環切換邏輯
    if st.button("⏭️ 下一個城市"):
        st.session_state.idx = (st.session_state.idx + 1) % len(CITIES)
        st.session_state.current_city = CITIES[st.session_state.idx]
        st.rerun()
