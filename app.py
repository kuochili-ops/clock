import streamlit as st

st.set_page_config(page_title="城市翻板鐘", layout="centered")

# 定義城市資料
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
        min-height: 100vh; margin: 0; padding: 10px;
        font-family: "Microsoft JhengHei", sans-serif;
    }}
    
    .container {{
        display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%;
    }}

    /* 翻板通用樣式 */
    .flip-card {{
        position: relative; background: #222;
        font-weight: 900; color: #e0e0e0; text-align: center;
        perspective: 1000px;
    }}

    /* 城市翻板尺寸 (並排) */
    .city-row {{
        display: flex; gap: 10px; width: 95vw; max-width: 500px;
    }}
    .city-flip {{
        flex: 1; height: 80px; font-size: 1.2rem;
    }}

    /* 時鐘翻板尺寸 */
    .clock-row {{
        display: flex; gap: 10px;
    }}
    .time-flip {{
        width: 20vw; max-width: 90px; height: 28vw; max-height: 130px;
        font-size: 18vw; max-font-size: 80px;
    }}

    /* 翻板內部結構 */
    .top, .bottom, .leaf-front, .leaf-back {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; box-sizing: border-box;
    }}
    
    .city-flip .top, .city-flip .leaf-front {{ line-height: 80px; border-radius: 8px 8px 0 0; }}
    .city-flip .bottom, .city-flip .leaf-back {{ line-height: 0px; border-radius: 0 0 8px 8px; }}
    
    .time-flip .top, .time-flip .leaf-front {{ line-height: 28vw; border-radius: 10px 10px 0 0; }}
    .time-flip .bottom, .time-flip .leaf-back {{ line-height: 0px; border-radius: 0 0 10px 10px; }}
    
    @media (min-width: 600px) {{
        .time-flip .top, .time-flip .leaf-front {{ line-height: 130px; }}
    }}

    .top {{ border-bottom: 1px solid #000; }}
    .leaf {{
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .leaf-back {{ transform: rotateX(-180deg); border-top: 1px solid #000; }}
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
        <div style="color:#666; font-size: 2rem; align-self:center; font-weight:bold;">:</div>
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
            <div class="top">${{newVal}}</div>
            <div class="bottom">${{oldVal || newVal}}</div>
            <div class="leaf">
                <div class="leaf-front">${{oldVal || newVal}}</div>
                <div class="leaf-back">${{newVal}}</div>
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
            timeZone: city.tz,
            hour12: false,
            hour: '2-digit', minute: '2-digit'
        }});
        
        const parts = formatter.formatToParts(now);
        const h = parts.find(p => p.type === 'hour').value;
        const m = parts.find(p => p.type === 'minute').value;

        // 更新城市翻板
        updateCard('city-zh-card', city.zh, prevCity.zh);
        updateCard('city-en-card', city.en, prevCity.en);
        
        // 更新時間翻板
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

st.markdown("### 🌍 全球時光翻板")
st.write("點擊**城市翻板**可切換城市與當地時間。")

st.components.v1.html(flip_clock_module, height=400)
