import streamlit as st

st.set_page_config(page_title="𓃥白六世界時鐘", layout="centered")

API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"
CITIES = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "q": "Taipei", "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
    {"zh": "高 雄", "en": "Kaohsiung", "tz": "Asia/Taipei", "q": "Kaohsiung", "img": "https://images.chinatimes.com/newsphoto/2023-01-06/656/20230106004870.jpg"},
    {"zh": "洛杉磯", "en": "Los Angeles", "tz": "America/Los_Angeles", "q": "Los Angeles", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/HollywoodSign.jpg/1280px-HollywoodSign.jpg"},
    {"zh": "大 阪", "en": "Osaka", "tz": "Asia/Tokyo", "q": "Osaka", "img": "https://images.unsplash.com/photo-1590559899731-a382839e5549?w=1200&q=80"},
    {"zh": "舊金山", "en": "San Francisco", "tz": "America/Los_Angeles", "q": "San Francisco", "img": "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?w=1200&q=80"},
    {"zh": "札 幌", "en": "Sapporo", "tz": "Asia/Tokyo", "q": "Sapporo", "img": "https://hokkaido-labo.com/wp-content/uploads/2014/09/140964647192343.jpg"},
    {"zh": "上 海", "en": "Shanghai", "tz": "Asia/Shanghai", "q": "Shanghai", "img": "https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2?w=1000&q=80"},
    {"zh": "哥本哈根", "en": "Copenhagen", "tz": "Europe/Copenhagen", "q": "Copenhagen", "img": "https://images.unsplash.com/photo-1513106580091-1d82408b8cd6?w=1000&q=80"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "q": "Tokyo", "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1000&q=80"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "q": "London", "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"},
    {"zh": "紐 約", "en": "New York", "tz": "America/New_York", "q": "New York", "img": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1000&q=80"}
]

flip_clock_html = f"""
<style>
    body {{ 
        background-color: #0e1117; margin: 0; 
        display: flex; justify-content: center; align-items: flex-start; 
        min-height: 100vh; font-family: "Microsoft JhengHei", sans-serif;
        padding-top: 0.5vh;
    }}
    .app-container {{ display: flex; flex-direction: column; align-items: center; gap: 8px; width: 98vw; max-width: 600px; }}
    .app-title {{ color: #444; font-size: 0.7rem; letter-spacing: 8px; font-weight: bold; margin-bottom: 2px; }}
    
    .flip-card {{ position: relative; background: #1a1a1a; border-radius: 6px; font-weight: 900; perspective: 1000px; color: #fff; overflow: hidden; }}
    .row-flex {{ display: flex; justify-content: space-between; width: 100%; gap: 8px; }}
    .info-card {{ flex: 1; height: 85px; font-size: clamp(1.4rem, 5.8vw, 2.3rem); cursor: pointer; }}

    .time-row {{ display: flex; gap: 4px; align-items: center; justify-content: center; width: 100%; }}
    .time-card {{ width: 22vw; max-width: 125px; height: 42vw; max-height: 195px; font-size: clamp(5rem, 30vw, 160px); }}
    
    .colon {{ 
        color: #fff; font-size: 4rem; font-weight: bold; margin-bottom: 15px;
        text-shadow: 0 0 15px rgba(255,255,255,1);
        animation: blink-strong 1s infinite steps(1); 
    }}
    @keyframes blink-strong {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.1; }} 100% {{ opacity: 1; }} }}

    /* 焦點霧化影像橫幅 */
    .city-photo-banner {{
        position: relative; width: 100%; height: 32vh; max-height: 280px;
        border-radius: 15px; margin-top: 5px;
        background-size: cover; background-position: center;
        transition: background-image 1s ease-in-out;
        border: 1px solid rgba(255, 255, 255, 0.05);
        overflow: hidden;
    }}
    
    /* 四邊霧化遮罩核心 */
    .glass-vignette {{
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        backdrop-filter: blur(8px); /* 霧化強度 */
        /* 徑向漸變遮罩：中央透明(100%清晰)，周邊不透明(觸發blur) */
        -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%);
        mask-image: radial-gradient(circle, transparent 40%, black 100%);
        background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.5) 100%);
    }}

    /* 物理遮蔽模組核心 */
    .half {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
    .top {{ top: 0; border-bottom: 1px solid rgba(0,0,0,0.8); align-items: flex-end; }}
    .bottom {{ bottom: 0; align-items: flex-start; }}
    .text-box {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; text-align: center; white-space: nowrap; }}
    .top .text-box {{ bottom: -100%; }} .bottom .text-box {{ top: -100%; }}
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
    <div class="time-row">
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
    </div>
</div>

<script>
    const cities = {CITIES};
    const apiKey = "{API_KEY}";
    let curIdx = 0;
    let pT = ["", ""]; let pC = {{zh: "", en: ""}}; let pW = {{status: "Loading", temp: ""}};

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

    async function nextCity() {{
        curIdx = (curIdx + 1) % cities.length;
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

    setInterval(tick, 1000); tick();
    document.getElementById('city-img').style.backgroundImage = `url('${{cities[0].img}}')`;
    fetchWeather(cities[0].q, new Date().getHours()).then(w => {{
        updateFlip('w_status', w.status, "");
        updateFlip('w_temp', w.temp, "");
        pW = w;
    }});
</script>
"""

st.components.v1.html(flip_clock_html, height=920)
