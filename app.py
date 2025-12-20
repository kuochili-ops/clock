import streamlit as st

st.set_page_config(page_title="𓃥白六世界時鐘", layout="centered")

# 擴充城市資料：加入建物圖示
CITIES = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "icon": "🗼 101"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "icon": "🗼 Tower"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "icon": "🎡 BigBen"},
    {"zh": "紐 約", "en": "New York", "tz": "America/New_York", "icon": "🗽 Statue"},
    {"zh": "巴 黎", "en": "Paris", "tz": "Europe/Paris", "icon": "🗼 Eiffel"},
    {"zh": "洛 杉 磯", "en": "Los Angeles", "tz": "America/Los_Angeles", "icon": "🎬 Hollywood"},
    {"zh": "雪 黎", "en": "Sydney", "tz": "Australia/Sydney", "icon": "⛵ Opera"}
]

flip_clock_html = f"""
<style>
    body {{ 
        background-color: #0e1117; margin: 0; 
        display: flex; justify-content: center; align-items: center; 
        min-height: 100vh; font-family: "Microsoft JhengHei", sans-serif;
    }}
    
    .app-container {{ 
        display: flex; flex-direction: column; align-items: center; 
        gap: 25px; width: 95vw; max-width: 550px; 
    }}

    .app-title {{ color: #555; font-size: 1rem; letter-spacing: 4px; font-weight: bold; }}
    
    .flip-card {{ position: relative; background: #1a1a1a; border-radius: 8px; font-weight: 900; perspective: 1000px; color: #fff; }}
    
    /* 城市翻板佈局 */
    .city-row {{ display: flex; justify-content: space-between; width: 100%; gap: 15px; }}
    .city-card {{ flex: 1; height: 110px; font-size: clamp(1.5rem, 6vw, 2.2rem); cursor: pointer; }}

    /* 時間翻板佈局：面板加高 */
    .time-row {{ display: flex; gap: 8px; align-items: center; justify-content: center; }}
    .time-card {{ 
        width: 21vw; max-width: 110px; 
        height: 38vw; max-height: 180px; /* 面板加高 */
        font-size: clamp(5rem, 28vw, 160px); 
    }}
    .colon {{ color: #333; font-size: 4rem; font-weight: bold; margin-bottom: 20px; }}

    /* 建物圖示區塊 */
    .landmark-container {{
        margin-top: 10px;
        padding: 10px 30px;
        background: rgba(255,255,255,0.05);
        border-radius: 50px;
        color: #888;
        font-size: 1.4rem;
        display: flex; align-items: center; gap: 10px;
        border: 1px solid #222;
    }}

    /* --- 物理遮蔽核心 --- */
    .half {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #1a1a1a; display: flex; justify-content: center;
    }}
    .top {{ top: 0; border-radius: 8px 8px 0 0; align-items: flex-end; border-bottom: 1px solid rgba(0,0,0,0.6); }}
    .bottom {{ bottom: 0; border-radius: 0 0 8px 8px; align-items: flex-start; }}

    .text-box {{
        position: absolute; width: 100%; height: 200%;
        display: flex; align-items: center; justify-content: center;
        text-align: center; white-space: nowrap;
    }}
    .top .text-box {{ bottom: -100%; }}
    .bottom .text-box {{ top: -100%; }}

    .leaf {{
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .leaf-front, .leaf-back {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backface-visibility: hidden; }}
    .leaf-back {{ transform: rotateX(-180deg); }}
    .flipping .leaf {{ transform: rotateX(-180deg); }}
    .hinge {{ position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background: #000; z-index: 20; }}
</style>

<div class="app-container">
    <div class="app-title">𓃥 白 六 世 界 時 鐘</div>

    <div class="city-row" onclick="nextCity()">
        <div class="flip-card city-card" id="czh"></div>
        <div class="flip-card city-card" id="cen"></div>
    </div>

    <div class="time-row">
        <div class="flip-card time-card" id="h0"></div>
        <div class="flip-card time-card" id="h1"></div>
        <div class="colon">:</div>
        <div class="flip-card time-card" id="m0"></div>
        <div class="flip-card time-card" id="m1"></div>
    </div>

    <div class="landmark-container" id="landmark">
        <span id="l-icon">🗼</span> <span id="l-name">台北 101</span>
    </div>
</div>

<script>
    const cities = {CITIES};
    let curIdx = 0;
    let pT = ["", ""];
    let pC = {{zh: "", en: ""}};

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
            <div class="hinge"></div>
        `;
        el.classList.remove('flipping');
        void el.offsetWidth;
        el.classList.add('flipping');
    }}

    function nextCity() {{ curIdx = (curIdx + 1) % cities.length; tick(); }}

    function tick() {{
        const c = cities[curIdx];
        const now = new Date();
        const f = new Intl.DateTimeFormat('en-US', {{
            timeZone: c.tz, hour12: false, hour: '2-digit', minute: '2-digit'
        }});
        const parts = f.formatToParts(now);
        const h = parts.find(p => p.type === 'hour').value;
        const m = parts.find(p => p.type === 'minute').value;

        updateFlip('czh', c.zh, pC.zh);
        updateFlip('cen', c.en, pC.en);
        updateFlip('h0', h[0], pT[0] ? pT[0][0] : "");
        updateFlip('h1', h[1], pT[0] ? pT[0][1] : "");
        updateFlip('m0', m[0], pT[1] ? pT[1][0] : "");
        updateFlip('m1', m[1], pT[1] ? pT[1][1] : "");

        document.getElementById('l-icon').innerText = c.icon.split(' ')[0];
        document.getElementById('l-name').innerText = c.zh.replace(/ /g, '') + " Landmark";

        pT = [h, m]; pC = {{zh: c.zh, en: c.en}};
    }}

    setInterval(tick, 1000);
    tick();
</script>
"""

st.components.v1.html(flip_clock_html, height=700)
