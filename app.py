import streamlit as st

st.set_page_config(page_title="城市翻板鐘修復版", layout="centered")

# 城市資料模組
CITIES_DATA = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei"},
    {"zh": "洛杉磯", "en": "Los Angeles", "tz": "America/Los_Angeles"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo"},
    {"zh": "紐 約", "en": "New York", "tz": "America/New_York"}
]

flip_clock_module = f"""
<style>
    body {{ 
        background-color: #0e1117; 
        display: flex; flex-direction: column;
        justify-content: center; align-items: center; 
        min-height: 100vh; margin: 0; padding: 10px;
        font-family: "Microsoft JhengHei", sans-serif;
    }}
    
    .container {{
        display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%;
    }}

    .flip-card {{
        position: relative; background: #222;
        font-weight: 900; color: #e0e0e0; text-align: center;
        perspective: 1000px;
    }}

    /* 城市翻板優化 */
    .city-row {{ display: flex; gap: 10px; width: 90vw; max-width: 500px; }}
    .city-flip {{ flex: 1; height: 70px; font-size: 1.2rem; }}

    /* 時間翻板優化 */
    .clock-row {{ display: flex; gap: 8px; align-items: center; }}
    .time-flip {{
        width: 20vw; max-width: 85px; height: 28vw; max-height: 120px;
        font-size: 18vw; max-font-size: 75px;
    }}

    /* 核心修復：使用 Flexbox 確保文字上下半部完美對齊 */
    .top, .bottom, .leaf-front, .leaf-back {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222;
        display: flex; justify-content: center; /* 水平置中 */
    }}

    .top, .leaf-front {{
        top: 0; border-radius: 6px 6px 0 0; border-bottom: 0.5px solid #000;
        align-items: flex-end; /* 對齊底端（翻板中心） */
    }}

    .bottom, .leaf-back {{
        bottom: 0; border-radius: 0 0 6px 6px;
        align-items: flex-start; /* 對齊頂端（翻板中心） */
    }}

    /* 調整文字在上下半部的位置，解決截圖中的偏移問題 */
    .top, .leaf-front {{ padding-bottom: 0; }}
    .bottom, .leaf-back {{ padding-top: 0; }}

    /* 確保文字不會因為 overflow 被切掉過多 */
    .top, .bottom, .leaf-front, .leaf-back {{
        height: 50%;
    }}

    /* 翻轉動畫邏輯 */
    .leaf {{
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .leaf-back {{ transform: rotateX(-180deg); }}
    .flipping .leaf {{ transform: rotateX(-180deg); }}
    
    .hinge {{
        position: absolute; top: 50%; left: 0; width: 100%; height: 2px;
        background: #000; z-index: 20; transform: translateY(-50%);
    }}
</style>

<div class="container">
    <div class="city-row" onclick="nextCity()">
        <div class="flip-card city-flip" id="city-zh-card"></div>
        <div class="flip-card city-flip" id="city-en-card"></div>
    </div>

    <div class="clock-row">
        <div class="flip-card time-flip" id="h0"></div>
        <div class="flip-card time-flip" id="h1"></div>
        <div style="color:#666; font-size: 2rem; font-weight:bold;">:</div>
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

        // 將內容拆分為上半部與下半部，確保對齊
        const content = `
            <div class="top"><span>${{newVal}}</span></div>
            <div class="bottom"><span>${{oldVal || newVal}}</span></div>
            <div class="leaf">
                <div class="leaf-front"><span>${{oldVal || newVal}}</span></div>
                <div class="leaf-back"><span>${{newVal}}</span></div>
            </div>
            <div class="hinge"></div>
        `;
        
        el.innerHTML = content;
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

st.markdown("### 🌍 全球時光翻板 (修復版)")
st.components.v1.html(flip_clock_module, height=450)
