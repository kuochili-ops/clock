import streamlit as st
from streamlit_folium import st_folium
import folium
import json

st.set_page_config(page_title="𓃥白六世界時鐘", layout="centered")

# --- 1. 核心資料 ---
API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"
CITIES = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "q": "Taipei", "lat": 25.03, "lon": 121.56, "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
    {"zh": "高 雄", "en": "Kaohsiung", "tz": "Asia/Taipei", "q": "Kaohsiung", "lat": 22.62, "lon": 120.30, "img": "https://images.chinatimes.com/newsphoto/2023-01-06/656/20230106004870.jpg"},
    {"zh": "洛杉磯", "en": "Los Angeles", "tz": "America/Los_Angeles", "q": "Los Angeles", "lat": 34.05, "lon": -118.24, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/HollywoodSign.jpg/1280px-HollywoodSign.jpg"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "q": "Tokyo", "lat": 35.68, "lon": 139.69, "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1000&q=80"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "q": "London", "lat": 51.50, "lon": -0.12, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"},
    {"zh": "紐 約", "en": "New York", "tz": "America/New_York", "q": "New York", "lat": 40.71, "lon": -74.00, "img": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1000&q=80"}
]

# --- 2. 處理地圖彈窗 (強效邊界限制) ---
@st.dialog("🌍 全球城市探索")
def show_map_dialog():
    # 設定滑動邊界，防止滑出世界版圖
    max_bounds = [(-85, -180), (85, 180)]
    
    m = folium.Map(
        location=[20, 0], 
        zoom_start=1, 
        tiles="CartoDB dark_matter", 
        zoom_control=False,
        no_wrap=True,
        max_bounds=True, # 啟用邊界限制
        min_lat=-60, max_lat=80, # 限制緯度移動
        min_lon=-170, max_lon=170 # 限制經度移動，防止標記消失
    )
    
    for c in CITIES:
        folium.CircleMarker(
            location=[c["lat"], c["lon"]], 
            radius=12, color="#00d4ff", fill=True, 
            fill_opacity=0.6, popup=c["zh"]
        ).add_to(m)
    
    selected = st_folium(m, height=320, width=320, key="modal_map")
    if selected.get("last_object_clicked_popup"):
        name_zh = selected["last_object_clicked_popup"]
        idx = next((i for i, item in enumerate(CITIES) if item["zh"] == name_zh), None)
        if idx is not None:
            st.session_state.target_idx = idx
            st.rerun()

# --- 3. 隱藏式 Streamlit 控制 ---
st.markdown("<style>.stButton { display: none; }</style>", unsafe_allow_html=True)
if st.button("TRIGGER_MAP"):
    show_map_dialog()

# --- 4. 物理翻板渲染 ---
initial_idx = st.session_state.get('target_idx', 0)

flip_clock_html = f"""
<style>
    body {{ background-color: #0e1117; margin: 0; display: flex; justify-content: center; }}
    .app-container {{ display: flex; flex-direction: column; align-items: center; gap: 8px; width: 92vw; max-width: 500px; padding-top: 10px; }}
    .app-title {{ color: #444; font-size: 0.75rem; letter-spacing: 6px; font-weight: bold; margin-bottom: 2px; }}
    
    .flip-card {{ position: relative; background: #1a1a1a; border-radius: 6px; font-weight: 900; perspective: 1000px; color: #fff; overflow: hidden; }}
    .row-flex {{ display: flex; justify-content: space-between; width: 100%; gap: 8px; }}
    .info-card {{ flex: 1; height: 18vw; max-height: 85px; font-size: 6vw; cursor: pointer; }}
    
    .time-row {{ display: flex; gap: 4px; align-items: center; justify-content: center; width: 100%; cursor: pointer; }}
    .time-card {{ width: 21vw; height: 35vw; font-size: 26vw; }}
    .colon {{ color: #fff; font-size: 8vw; font-weight: bold; animation: blink 1s infinite steps(1); }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.2; }} }}
    
    .city-photo-banner {{ position: relative; width: 100%; height: 50vw; max-height: 280px; border-radius: 15px; margin-top: 5px; background-size: cover; background-position: center; transition: background-image 0.8s; }}
    .glass-vignette {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%); background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.5) 100%); }}

    /* 物理翻轉視覺核心 */
    .half {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
    .top {{ top: 0; border-bottom: 1.5px solid #000; align-items: flex-end; }} 
    .bottom {{ bottom: 0; align-items: flex-start; }}
    .text-box {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; }}
    .top .text-box {{ bottom: -100%; }} .bottom .text-box {{ top: -100%; }}
    
    /* 3D 翻轉葉片效果 */
    .leaf {{ position: absolute; top: 0; left: 0; width: 100%; height: 50%; z-index: 10; transform-origin: bottom; transform-style: preserve-3d; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }}
    .leaf-front, .leaf-back {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backface-visibility: hidden; }}
    .leaf-back {{ transform: rotateX(-180deg); }}
    .flipping .leaf {{ transform: rotateX(-180deg); }}
</style>

<div class="app-container">
    <div class="app-title">𓃥 白 六 世 界 時 鐘</div>
    <div class="row-flex" onclick="nextCity()">
        <div class="flip-card info-card" id="czh"></div>
        <div class="flip-card info-card" id="cen"></div>
    </div>
    <div class="time-row" onclick="nextCity()">
        <div class="flip-card time-card" id="h0"></div>
        <div class="flip-card time-card" id="h1"></div>
        <div class="colon">:</div>
        <div class="flip-card time-card" id="m0"></div>
        <div class="flip-card time-card" id="m1"></div>
    </div>
    <div class="row-flex">
        <div class="flip-card info-card" id="w_status" style="background: #121212; color: #bbb;"></div>
        <div class="flip-card info-card" id="w_temp" style="background: #121212; color: #888;"></div>
    </div>
    <div class="city-photo-banner" id="city-img">
        <div class="glass-vignette"></div>
        <div style="position:absolute; bottom:0; left:0; width:45%; height:60%; cursor:pointer; z-index:100;" 
             onclick="window.parent.document.querySelector('button[kind=secondary]').click()"></div>
    </div>
</div>

<script>
    const cities = {json.dumps(CITIES)};
    const apiKey = "{API_KEY}";
    let curIdx = {initial_idx};
    let pT = ["", ""]; let pC = {{zh: "", en: ""}}; let pW = {{status: "", temp: ""}};

    function updateFlip(id, newVal, oldVal) {{
        const el = document.getElementById(id);
        if (newVal === oldVal && el.innerHTML !== "") return;
        el.innerHTML = `
            <div class="half top"><div class="text-box">${{newVal}}</div></div>
            <div class="half bottom"><div class="text-box">${{oldVal || newVal}}</div></div>
            <div class="leaf">
                <div class="leaf-front half top"><div class="text-box">${{oldVal || newVal}}</div></div>
                <div class="leaf-back half bottom"><div class="text-box">${{newVal}}</div></div>
            </div>
        `;
        el.classList.remove('flipping'); void el.offsetWidth; el.classList.add('flipping');
    }}

    async function fetchWeather(cityQ, hour) {{
        try {{
            const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${{cityQ}}&appid=${{apiKey}}&units=metric`);
            const data = await res.json();
            const icon = (hour >= 6 && hour < 18) ? "☀️" : "🌙";
            return {{ status: icon + " " + data.weather[0].main, temp: Math.round(data.main.temp_min)+"~"+Math.round(data.main.temp_max)+"°C" }};
        }} catch (e) {{ return {{ status: "Offline", temp: "--" }}; }}
    }}

    async function renderCity() {{
        const c = cities[curIdx];
        document.getElementById('city-img').style.backgroundImage = `url('${{c.img}}')`;
        const now = new Date();
        const hour = parseInt(new Intl.DateTimeFormat('en-US', {{ timeZone: c.tz, hour: '2-digit', hour12: false }}).format(now));
        const w = await fetchWeather(c.q, hour);
        updateFlip('w_status', w.status, pW.status);
        updateFlip('w_temp', w.temp, pW.temp);
        pW = w; tick();
    }}

    function tick() {{
        const c = cities[curIdx];
        const now = new Date();
        const f = new Intl.DateTimeFormat('en-US', {{ timeZone: c.tz, hour12: false, hour: '2-digit', minute: '2-digit' }});
        const parts = f.formatToParts(now);
        const h = parts.find(p => p.type === 'hour').value;
        const m = parts.find(p => p.type === 'minute').value;
        updateFlip('czh', c.zh, pC.zh); updateFlip('cen', c.en, pC.en);
        updateFlip('h0', h[0], pT[0] ? pT[0][0] : "");
        updateFlip('h1', h[1], pT[0] ? pT[0][1] : "");
        updateFlip('m0', m[0], pT[1] ? pT[1][0] : "");
        updateFlip('m1', m[1], pT[1] ? pT[1][1] : "");
        pT = [h, m]; pC = {{zh: c.zh, en: c.en}};
    }}

    setInterval(tick, 1000); 
    renderCity();
    window.addEventListener('click', () => {{ nextCity(); }}, {{ once: false, capture: true }}); // 增加全域點擊備援
</script>
"""

st.components.v1.html(flip_clock_html, height=850)
