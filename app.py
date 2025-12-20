import streamlit as st
from streamlit_folium import st_folium
import folium
import json

st.set_page_config(page_title="𓃥白六世界時鐘", layout="centered")

# --- 1. 定義 VIP 城市清單 (依您要求的順序) ---
API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"

MY_VIP_LIST = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "q": "Taipei", "lat": 25.03, "lon": 121.56},
    {"zh": "高 雄", "en": "Kaohsiung", "tz": "Asia/Taipei", "q": "Kaohsiung", "lat": 22.62, "lon": 120.30},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "q": "Tokyo", "lat": 35.68, "lon": 139.69},
    {"zh": "大 阪", "en": "Osaka", "tz": "Asia/Tokyo", "q": "Osaka", "lat": 34.69, "lon": 135.50},
    {"zh": "札 幌", "en": "Sapporo", "tz": "Asia/Tokyo", "q": "Sapporo", "lat": 43.06, "lon": 141.35},
    {"zh": "上 海", "en": "Shanghai", "tz": "Asia/Shanghai", "q": "Shanghai", "lat": 31.23, "lon": 121.47},
    {"zh": "羅 馬", "en": "Rome", "tz": "Europe/Rome", "q": "Rome", "lat": 41.90, "lon": 12.49},
    {"zh": "阿姆斯特丹", "en": "Amsterdam", "tz": "Europe/Amsterdam", "q": "Amsterdam", "lat": 52.36, "lon": 4.89},
    {"zh": "法蘭克福", "en": "Frankfurt", "tz": "Europe/Berlin", "q": "Frankfurt", "lat": 50.11, "lon": 8.68},
    {"zh": "哥本哈根", "en": "Copenhagen", "tz": "Europe/Copenhagen", "q": "Copenhagen", "lat": 55.67, "lon": 12.56},
    {"zh": "紐 約", "en": "New York", "tz": "America/New_York", "q": "New York", "lat": 40.71, "lon": -74.00},
    {"zh": "舊金山", "en": "San Francisco", "tz": "America/Los_Angeles", "q": "San Francisco", "lat": 37.77, "lon": -122.41},
    {"zh": "洛杉磯", "en": "Los Angeles", "tz": "America/Los_Angeles", "q": "Los Angeles", "lat": 34.05, "lon": -118.24},
    {"zh": "多倫多", "en": "Toronto", "tz": "America/Toronto", "q": "Toronto", "lat": 43.65, "lon": -79.38},
]

# 標記為 VIP 並給予預設圖片
for c in MY_VIP_LIST:
    c["vip"] = True
    c["img"] = f"https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1000&q=80"

# 其他全球補充城市 (作為背景導航)
GLOBAL_CITIES = [
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "q": "London", "lat": 51.50, "lon": -0.12, "vip": False},
    {"zh": "巴 黎", "en": "Paris", "tz": "Europe/Paris", "q": "Paris", "lat": 48.85, "lon": 2.35, "vip": False},
    {"zh": "首 爾", "en": "Seoul", "tz": "Asia/Seoul", "q": "Seoul", "lat": 37.56, "lon": 126.97, "vip": False},
    {"zh": "雪 梨", "en": "Sydney", "tz": "Australia/Sydney", "q": "Sydney", "lat": -33.86, "lon": 151.20, "vip": False},
    {"zh": "杜 拜", "en": "Dubai", "tz": "Asia/Dubai", "q": "Dubai", "lat": 25.20, "lon": 55.27, "vip": False},
    {"zh": "新加玻", "en": "Singapore", "tz": "Asia/Singapore", "q": "Singapore", "lat": 1.35, "lon": 103.81, "vip": False},
]

for c in GLOBAL_CITIES:
    c["img"] = "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?w=1000&q=80"

ALL_CITIES = MY_VIP_LIST + GLOBAL_CITIES

# --- 2. 地圖對話框 ---
@st.dialog("🌍 全球時空導航")
def show_map_dialog():
    m = folium.Map(
        location=[20, 10], zoom_start=1, 
        tiles="CartoDB dark_matter", zoom_control=False,
        no_wrap=True, max_bounds=True,
        min_lat=-65, max_lat=85, min_lon=-175, max_lon=175
    )
    for c in ALL_CITIES:
        color = "#FF8C00" if c["vip"] else "#00d4ff"
        radius = 10 if c["vip"] else 6
        label = f"⭐ {c['zh']}" if c.get("vip") else c["zh"]
        folium.CircleMarker(
            location=[c["lat"], c["lon"]], 
            radius=radius, color=color, fill=True, 
            fill_opacity=0.8, popup=label
        ).add_to(m)
    
    selected = st_folium(m, height=350, width=320, key="modal_map")
    if selected.get("last_object_clicked_popup"):
        name = selected["last_object_clicked_popup"].replace("⭐ ", "")
        idx = next((i for i, item in enumerate(ALL_CITIES) if item["zh"] == name), None)
        if idx is not None:
            st.session_state.target_idx = idx
            st.rerun()

# --- 3. 介面按鈕 ---
st.markdown("<style>.stButton { display: none; }</style>", unsafe_allow_html=True)
if st.button("TRIGGER_MAP"):
    show_map_dialog()

# --- 4. 物理翻板 HTML ---
initial_idx = st.session_state.get('target_idx', 0)

flip_clock_html = f"""
<div class="app-container">
    <div class="app-title">𓃥 白 六 世 界 時 鐘</div>
    <div id="click-zone">
        <div class="row-flex">
            <div class="flip-card info-card" id="czh"></div>
            <div class="flip-card info-card" id="cen"></div>
        </div>
        <div class="time-row">
            <div class="flip-card time-card" id="h0"></div>
            <div class="flip-card time-card" id="h1"></div>
            <div class="colon">:</div>
            <div class="flip-card time-card" id="m0"></div>
            <div class="flip-card time-card" id="m1"></div>
        </div>
        <div class="row-flex">
            <div class="flip-card info-card weather-card" id="w_status"></div>
            <div class="flip-card info-card weather-card" id="w_temp"></div>
        </div>
    </div>
    <div class="attribution">Data by OpenWeather</div>
    <div class="city-photo-banner" id="city-img">
        <div class="glass-vignette"></div>
        <div class="map-trigger" id="map-btn"></div>
    </div>
</div>

<style>
    body {{ background-color: #0e1117; margin: 0; display: flex; justify-content: center; }}
    .app-container {{ display: flex; flex-direction: column; align-items: center; gap: 8px; width: 92vw; max-width: 500px; padding-top: 10px; }}
    .app-title {{ color: #444; font-size: 0.75rem; letter-spacing: 6px; font-weight: bold; margin-bottom: 2px; }}
    .flip-card {{ position: relative; background: #1a1a1a; border-radius: 6px; font-weight: 900; perspective: 1000px; color: #fff; overflow: hidden; }}
    .row-flex {{ display: flex; justify-content: space-between; width: 100%; gap: 8px; }}
    .info-card {{ flex: 1; height: 18vw; max-height: 85px; font-size: 6vw; display: flex; align-items: center; justify-content: center; }}
    .weather-card {{ background: #121212 !important; color: #aaa !important; font-size: 5vw; }}
    .time-row {{ display: flex; gap: 4px; align-items: center; justify-content: center; width: 100%; margin-top: 5px; }}
    .time-card {{ width: 21vw; height: 35vw; font-size: 26vw; }}
    .colon {{ color: #fff; font-size: 8vw; font-weight: bold; animation: blink 1s infinite steps(1); }}
    .attribution {{ color: #333; font-size: 0.6rem; align-self: flex-end; margin-right: 5px; margin-top: -4px; }}
    .city-photo-banner {{ position: relative; width: 100%; height: 50vw; max-height: 280px; border-radius: 15px; margin-top: 5px; background-size: cover; background-position: center; transition: background-image 0.8s; }}
    .glass-vignette {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%); }}
    .map-trigger {{ position: absolute; bottom: 0; left: 0; width: 45%; height: 60%; cursor: pointer; z-index: 100; }}

    /* 物理翻轉 */
    .half {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
    .top {{ top: 0; border-bottom: 1.5px solid #000; align-items: flex-end; }} 
    .bottom {{ bottom: 0; align-items: flex-start; }}
    .text-box {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; }}
    .top .text-box {{ bottom: -100%; }} .bottom .text-box {{ top: -100%; }}
    .leaf {{ position: absolute; top: 0; left: 0; width: 100%; height: 50%; z-index: 10; transform-origin: bottom; transform-style: preserve-3d; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }}
    .leaf-front, .leaf-back {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backface-visibility: hidden; }}
    .leaf-back {{ transform: rotateX(-180deg); }}
    .flipping .leaf {{ transform: rotateX(-180deg); }}
</style>

<script>
    const cities = {json.dumps(ALL_CITIES)};
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
        const f = new Intl.DateTimeFormat('en-US', {{ timeZone: c.tz, hour12: false, hour: '2-digit' }});
        const hour = parseInt(f.format(now));
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

    document.getElementById('click-zone').addEventListener('click', () => {{
        curIdx = (curIdx + 1) % cities.length;
        renderCity();
    }});

    document.getElementById('map-btn').addEventListener('click', (e) => {{
        e.stopPropagation();
        window.parent.document.querySelector('button[kind=secondary]').click();
    }});

    setInterval(tick, 1000); 
    renderCity();
</script>
"""

st.components.v1.html(flip_clock_html, height=850)
