import streamlit as st

st.set_page_config(page_title="全球時區翻板鐘", layout="centered")

# 城市資料
CITIES_DATA = [
    {"zh": "臺    北", "en": "Taipei", "tz": "Asia/Taipei"},
    {"zh": "洛 杉 磯", "en": "Los Angeles", "tz": "America/Los_Angeles"},
    {"zh": "倫    敦", "en": "London", "tz": "Europe/London"},
    {"zh": "東    京", "en": "Tokyo", "tz": "Asia/Tokyo"},
    {"zh": "紐    約", "en": "New York", "tz": "America/New_York"}
]

flip_clock_module = f"""
<style>
    body {{ 
        background-color: #0e1117; 
        display: flex; flex-direction: column;
        justify-content: center; align-items: center; 
        min-height: 100vh; margin: 0; padding: 0;
        overflow: hidden;
    }}
    
    .main-container {{
        display: flex; flex-direction: column; align-items: center; 
        gap: 30px; width: 100%; max-width: 500px;
    }}

    /* 通用翻板容器 */
    .flip-card {{
        position: relative; background: #222;
        border-radius: 8px;
        perspective: 1000px;
    }}

    /* 城市翻板 (上方兩塊) */
    .city-row {{ display: flex; gap: 12px; width: 90vw; }}
    .city-flip {{ flex: 1; height: 80px; }}

    /* 時間翻板 (下方四塊) */
    .clock-row {{ display: flex; gap: 8px; align-items: center; }}
    .time-flip {{ width: 20vw; max-width: 85px; height: 28vw; max-height: 120px; }}

    /* 修復核心：上下半部結構 */
    .top, .bottom, .leaf-front, .leaf-back {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #262626;
        display: flex; justify-content: center; align-items: center;
        box-sizing: border-box;
    }}

    .top, .leaf-front {{
        top: 0; border-radius: 8px 8px 0 0;
        align-items: flex-end; /* 文字對齊中線底部 */
    }}

    .bottom, .leaf-back {{
        bottom: 0; border-radius: 0 0 8px 8px;
        align-items: flex-start; /* 文字對齊中線頂部 */
    }}

    /* 解決文字殘缺：透過 span 控制文字溢出 */
    .flip-card span {{
        display: block; line-height: 0; 
        font-family: "Microsoft JhengHei", Arial, sans-serif;
        font-weight: 900; color: #eee;
    }}

    .city-flip span {{ font-size: 1.2rem; }}
    .time-flip span {{ font-size: 18vw; }}
    @media (min-width: 600px) {{ .time-flip span {{ font-size: 80px; }} }}

    /* 確保上下半部文字剛好切分 */
    .top span, .leaf-front span {{ transform: translateY(0); padding-bottom: 0; }}
    .bottom span, .leaf-back span {{ transform: translateY(0); padding-top: 0; }}

    /* 翻轉動畫 */
    .leaf {{
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .leaf-back {{ transform: rotateX(-180deg); }}
    .flipping .leaf {{ transform: rotateX(-180deg); }}
    
    .hinge {{
        position: absolute; top: 50%; left: 0; width: 100%; height: 2px;
        background: rgba(0,0,0,0.6); z-index: 20; transform: translateY(-50%);
    }}
</style>

<div class="main-container">
    <div class="city-row" onclick="nextCity()">
        <div class="flip-card city-flip" id="city-zh-card"></div>
        <div class="flip-card city-flip" id="city-en-card"></div>
    </div>

    <div class="clock-row">
        <div class="flip-card time-flip" id="h0"></div>
        <div class="flip-card time-flip" id="h1"></div>
        <div style="color:#444; font-size: 2rem; font-weight:bold;">:</div>
        <div class="flip-card time-flip" id="m0"></div>
        <div class="flip-card time-flip" id="m1"></div>
    </div>
</div>

<script>
    const cities = {CITIES_DATA};
    let currentCityIndex = 0;
    let prevTime = ["", ""];
    let prevCity = {{ zh: "", en: "" }};

    function updateCard(id, newVal, oldVal) {{
        const el = document.getElementById(id);
        if (newVal === oldVal && el.innerHTML !== "") return;

        el.innerHTML = `
            <div class="top"><span>${{newVal}}</span></div>
            <div class="bottom"><span>${{oldVal || newVal}}</span></div>
            <div class="leaf">
                <div class="leaf-front"><span>${{oldVal || newVal}}</span></div>
                <div class="leaf-back"><span>${{newVal}}</span></div>
            </div>
            <div class="hinge"></div>
        `;
        el.classList.remove('flipping');
        void el.offsetWidth;
        el.classList.add('flipping');
    }}

    function nextCity() {{
        currentCityIndex = (currentCityIndex + 1) % cities.length;
        tick();
    }}

    function tick() {{
        const city = cities[currentCityIndex];
        const now = new Date();
        const formatter = new Intl.DateTimeFormat('en-US', {{
            timeZone: city.tz, hour12: false,
            hour: '2-digit', minute: '2-digit'
        }});
        
        const parts = formatter.formatToParts(now);
        const h = parts.find(p => p.type === 'hour').value;
        const m = parts.find(p => p.type === 'minute').value;

        updateCard('city-zh-card', city.zh, prevCity.zh);
        updateCard('city-en-card', city.en, prevCity.en);
        updateCard('h0', h[0], prevTime[0][0]);
        updateCard('h1', h[1], prevTime[0][1]);
        updateCard('m0', m[0], prevTime[1][0]);
        updateCard('m1', m[1], prevTime[1][1]);
        
        prevTime = [h, m];
        prevCity = {{ zh: city.zh, en: city.en }};
    }}

    setInterval(tick, 1000);
    tick();
</script>
"""

st.components.v1.html(flip_clock_module, height=500)
