import streamlit as st
from streamlit_folium import st_folium
import folium

# --- 1. 核心資料：維持您影片中的預設城市 ---
if 'idx' not in st.session_state: st.session_state.idx = 0
CITIES = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "lat": 25.03, "lon": 121.56, "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "lat": 51.50, "lon": -0.12, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "lat": 35.68, "lon": 139.69, "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1000&q=80"}
]

# --- 2. 地圖對話框 (只有點擊照片左下角才會跳出) ---
@st.dialog("🌍 探索世界")
def show_map_dialog():
    m = folium.Map(location=[20, 0], zoom_start=1, tiles="CartoDB dark_matter", zoom_control=False)
    for c in CITIES:
        folium.CircleMarker(location=[c["lat"], c["lon"]], radius=10, color="#00d4ff", fill=True, popup=c["zh"]).add_to(m)
    selected = st_folium(m, height=300, width=320, key="modal_map")
    if selected.get("last_object_clicked_popup"):
        name_zh = selected["last_object_clicked_popup"]
        new_idx = next((i for i, item in enumerate(CITIES) if item["zh"] == name_zh), None)
        if new_idx is not None:
            st.session_state.idx = new_idx
            st.rerun()

# --- 3. 隱藏式邏輯觸發器 ---
st.markdown("<style>.stButton { display: none; }</style>", unsafe_allow_html=True)

# 用來處理點擊翻板切換城市
if st.button("NEXT", key="next_trigger"):
    st.session_state.idx = (st.session_state.idx + 1) % len(CITIES)
    st.rerun()

# 用來處理地圖彈出
if st.button("MAP", key="map_trigger"):
    show_map_dialog()

# --- 4. 原始物理翻板 HTML ---
curr = CITIES[st.session_state.idx]
html_code = f"""
<div id="clock-app" style="width: 100%; display: flex; flex-direction: column; align-items: center; gap: 8px;">
    <style>
        .row-flex {{ display: flex; width: 92vw; justify-content: space-between; gap: 8px; }}
        .flip-card {{ background: #1a1a1a; border-radius: 8px; color: white; font-weight: 900; position: relative; overflow: hidden; }}
        .info-card {{ flex: 1; height: 18vw; font-size: 6.5vw; display: flex; align-items: center; justify-content: center; cursor: pointer; }}
        .time-row {{ display: flex; gap: 4px; align-items: center; cursor: pointer; }}
        .time-card {{ width: 21vw; height: 35vw; font-size: 26vw; }}
        
        /* 物理遮蔽核心 */
        .half {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
        .top {{ top: 0; border-bottom: 1px solid #000; align-items: flex-end; }}
        .bottom {{ bottom: 0; align-items: flex-start; }}
        .text-box {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; }}
        .top .text-box {{ bottom: -100%; }} .bottom .text-box {{ top: -100%; }}

        .photo-banner {{ 
            width: 92vw; height: 50vw; border-radius: 15px; margin-top: 10px;
            background: url('{curr['img']}') center/cover; position: relative; overflow: hidden; 
        }}
        .glass {{ 
            position: absolute; width: 100%; height: 100%; 
            backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%); 
        }}
        .map-hotspot {{ position: absolute; bottom: 0; left: 0; width: 40%; height: 50%; cursor: pointer; z-index: 100; }}
    </style>

    <div onclick="window.parent.document.querySelectorAll('button[kind=secondary]')[0].click()">
        <div class="row-flex">
            <div class="flip-card info-card">{curr['zh']}</div>
            <div class="flip-card info-card">{curr['en']}</div>
        </div>
        <div class="time-row" style="margin-top: 10px;">
            <div class="flip-card time-card" id="h0"></div>
            <div class="flip-card time-card" id="h1"></div>
            <div style="font-size: 10vw; color: white; padding-bottom: 2vw;">:</div>
            <div class="flip-card time-card" id="m0"></div>
            <div class="flip-card time-card" id="m1"></div>
        </div>
    </div>

    <div class="photo-banner">
        <div class="glass"></div>
        <div class="map-hotspot" onclick="window.parent.document.querySelectorAll('button[kind=secondary]')[1].click(); event.stopPropagation();"></div>
    </div>
</div>

<script>
    function updateVal(id, val) {{
        document.getElementById(id).innerHTML = `<div class="half top"><div class="text-box">${{val}}</div></div><div class="half bottom"><div class="text-box">${{val}}</div></div>`;
    }}
    function tick() {{
        const now = new Date(new Date().toLocaleString("en-US", {{timeZone: "{curr['tz']}"}}));
        const h = String(now.getHours()).padStart(2, '0');
        const m = String(now.getMinutes()).padStart(2, '0');
        updateVal('h0', h[0]); updateVal('h1', h[1]); updateVal('m0', m[0]); updateVal('m1', m[1]);
    }}
    setInterval(tick, 1000); tick();
</script>
"""

st.components.v1.html(html_code, height=650)
