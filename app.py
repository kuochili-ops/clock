import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="𓃥白六世界時鐘", layout="centered")

# --- 1. 核心資料 ---
if 'idx' not in st.session_state: st.session_state.idx = 0
CITIES = [
    {"name": "Taipei", "zh": "臺 北", "tz": "Asia/Taipei", "lat": 25.033, "lon": 121.565, "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
    {"name": "Kaohsiung", "zh": "高 雄", "tz": "Asia/Taipei", "lat": 22.627, "lon": 120.301, "img": "https://images.chinatimes.com/newsphoto/2023-01-06/656/20230106004870.jpg"},
    {"name": "Los Angeles", "zh": "洛杉磯", "tz": "America/Los_Angeles", "lat": 34.052, "lon": -118.243, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/HollywoodSign.jpg/1280px-HollywoodSign.jpg"},
    {"name": "London", "zh": "倫 敦", "tz": "Europe/London", "lat": 51.507, "lon": -0.127, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"},
    {"name": "Tokyo", "zh": "東 京", "tz": "Asia/Tokyo", "lat": 35.689, "lon": 139.691, "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1000&q=80"}
]

# --- 2. 跳出式地圖對話框 ---
@st.dialog("🌍 全球城市探索")
def show_map_dialog():
    m = folium.Map(location=[20, 0], zoom_start=1, tiles="CartoDB dark_matter", zoom_control=False)
    for c in CITIES:
        folium.CircleMarker(location=[c["lat"], c["lon"]], radius=10, color="#00d4ff", fill=True, popup=c["name"]).add_to(m)
    # 地圖寬度適配手機
    selected = st_folium(m, height=300, width=320, key="pop_map")
    if selected.get("last_object_clicked_popup"):
        name = selected["last_object_clicked_popup"]
        idx = next((i for i, item in enumerate(CITIES) if item["name"] == name), None)
        if idx is not None:
            st.session_state.idx = idx
            st.rerun()

# --- 3. 處理點擊翻板切換邏輯 ---
# 透過一個隱形的切換器來捕捉 JS 傳來的訊息
if st.button("TRIGGER_NEXT", key="t_next", help="隱藏觸發器"):
    st.session_state.idx = (st.session_state.idx + 1) % len(CITIES)
    st.rerun()

# --- 4. 主視覺 HTML (修正寬度並整合隱藏熱點) ---
curr = CITIES[st.session_state.idx]
flip_html = f"""
<style>
    body {{ background: #0e1117; margin: 0; padding: 0; display: flex; justify-content: center; }}
    .app-container {{ width: 92vw; max-width: 500px; display: flex; flex-direction: column; gap: 10px; padding-top: 10px; }}
    .flip-card {{ position: relative; background: #1a1a1a; border-radius: 8px; font-weight: 900; color: #fff; overflow: hidden; }}
    .row-flex {{ display: flex; justify-content: space-between; gap: 8px; }}
    .info-card {{ flex: 1; height: 18vw; max-height: 80px; font-size: 6vw; display: flex; align-items: center; justify-content: center; }}
    
    .time-row {{ display: flex; gap: 4px; align-items: center; justify-content: center; }}
    .time-card {{ width: 20vw; height: 35vw; max-width: 100px; max-height: 160px; font-size: 25vw; }}
    
    .photo-banner {{
        position: relative; width: 100%; height: 50vw; max-height: 280px;
        background: url('{curr['img']}') center/cover; border-radius: 12px; overflow: hidden;
    }}
    .glass-vignette {{
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%);
    }}
    
    /* 地圖觸發熱點：位於照片左下角 */
    .map-hotspot {{
        position: absolute; bottom: 0; left: 0; width: 30%; height: 40%;
        cursor: pointer; z-index: 100;
    }}

    /* 物理翻板樣式 */
    .half {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
    .top {{ top: 0; border-bottom: 1px solid #000; align-items: flex-end; }}
    .bottom {{ bottom: 0; align-items: flex-start; }}
    .text-box {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; }}
    .top .text-box {{ bottom: -100%; }} .bottom .text-box {{ top: -100%; }}
</style>

<div class="app-container">
    <div onclick="window.parent.document.querySelector('button[kind=secondary]').click()">
        <div class="row-flex">
            <div class="flip-card info-card">{curr['zh']}</div>
            <div class="flip-card info-card">{curr['name']}</div>
        </div>
        <div class="time-row" style="margin-top:10px;">
            <div class="flip-card time-card" id="h0"></div>
            <div class="flip-card time-card" id="h1"></div>
            <div style="font-size: 10vw; color: white;">:</div>
            <div class="flip-card time-card" id="m0"></div>
            <div class="flip-card time-card" id="m1"></div>
        </div>
    </div>

    <div class="photo-banner">
        <div class="glass-vignette"></div>
        <div class="map-hotspot" onclick="window.parent.postMessage('open_map', '*')"></div>
    </div>
</div>

<script>
    function updateFlip(id, val) {{
        const el = document.getElementById(id);
        el.innerHTML = `<div class="half top"><div class="text-box">${{val}}</div></div>
                        <div class="half bottom"><div class="text-box">${{val}}</div></div>`;
    }}
    function tick() {{
        const now = new Date(new Date().toLocaleString("en-US", {{timeZone: "{curr['tz']}"}}));
        const h = String(now.getHours()).padStart(2, '0');
        const m = String(now.getMinutes()).padStart(2, '0');
        updateFlip('h0', h[0]); updateFlip('h1', h[1]); updateFlip('m0', m[0]); updateFlip('m1', m[1]);
    }}
    setInterval(tick, 1000); tick();
</script>
"""

# --- 5. 隱藏式地圖喚醒機制 ---
# 監聽來自 HTML 的 PostMessage
from streamlit_js_eval import streamlit_js_eval
event = streamlit_js_eval(js_expressions="window.addEventListener('message', (e) => { if(e.data === 'open_map') return 'map'; })", want_output=True)

if event == 'map':
    show_map_dialog()

st.components.v1.html(flip_html, height=650)

# 隱藏那顆用來切換城市的 Streamlit 實體按鈕，使其不影響版面
st.markdown("""<style> button[kind="secondary"] { display: none; } </style>""", unsafe_allow_html=True)
