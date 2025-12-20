import streamlit as st

st.set_page_config(page_title="全球城市翻板鐘", layout="centered")

# 定義城市資料模組
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
    
    /* 城市翻板容器 */
    .city-container {{
        display: flex; gap: 10px; width: 100%; max-width: 500px;
        margin-bottom: 20px; cursor: pointer;
    }}

    .city-card {{
        position: relative; flex: 1; height: 80px;
        background: #222; border-radius: 8px;
        color: #fff; text-align: center; overflow: hidden;
        perspective: 1000px; border: 1px solid #333;
    }}

    .city-label {{
        line-height: 80px; font-weight: bold;
        font-size: 1.2rem; letter-spacing: 2px;
    }}

    /* 時鐘容器 */
    .clock {{ 
        display: flex; gap: 8px; flex-wrap: wrap;
        justify-content: center; align-items: center; width: 100%;
    }}

    .flip-card {{
        position: relative; width: 14vw; max-width: 70px; 
        height: 20vw; max-height: 100px;
        font-size: 13vw; max-font-size: 60px;
        font-weight: 900; color: #e0e0e0; text-align: center;
    }}

    /* 通用翻板樣式 */
    .top, .bottom, .leaf-front, .leaf-back {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222;
    }}
    .top, .leaf-front {{ 
        top: 0; border-radius: 6px 6px 0 0; line-height: 20vw; 
        border-bottom: 1px solid #000; 
    }}
    .bottom, .leaf-back {{ 
        bottom: 0; border-radius: 0 0 6px 6px; line-height: 0px; 
    }}
    
    @media (min-width: 600px) {{
        .top, .leaf-front {{ line-height: 100px; }}
        .city-card {{ height: 100px; }}
        .city-label {{ line-height: 100px; font-size: 1.5rem; }}
    }}

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
    .unit-label {{ color: #666; font-size: 0.8rem; margin-top: 5px; font-weight: bold; }}
</style>

<div class="city-container" onclick="nextCity()">
    <div class="city-card" id="city-zh-card">
        <div class="city-label" id="city-zh">臺 北</div>
    </div>
    <div class="city-card" id="city-en-card">
        <div class="city-label" id="city-en">Taipei</div>
    </div>
</div>

<div class="clock" id="clock"></div>

<script>
    const cities = {CITIES_DATA};
    let currentCityIndex = 0;
    let prevTime = ["", "", ""];

    function nextCity() {{
        currentCityIndex = (currentCityIndex + 1) % cities.length;
        const city = cities[currentCityIndex];
        
        // 觸發城市翻轉視覺效果（簡單淡入淡出或可擴展為翻轉）
        document.getElementById('city-zh').innerText = city.zh;
        document.getElementById('city-en').innerText = city.en;
        
        // 重置時鐘以觸發重新繪製
        prevTime = ["", "", ""];
        tick();
    }}

    function updateDigit(id, newVal, oldVal) {{
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

    function tick() {{
        const city = cities[currentCityIndex];
        // 使用 Intl.DateTimeFormat 獲取特定時區時間
        const now = new Date();
        const formatter = new Intl.DateTimeFormat('en-US', {{
            timeZone: city.tz,
            hour12: false,
            hour: '2-digit', minute: '2-digit', second: '2-digit'
        }});
        
        const parts = formatter.formatToParts(now);
        const h = parts.find(p => p.type === 'hour').value;
        const m = parts.find(p => p.type === 'minute').value;
        const s = parts.find(p => p.type === 'second').value;

        if (prevTime[0] === "") {{
            document.getElementById('clock').innerHTML = `
                <div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div>
                <div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div>
                <div class="flip-card" id="d4"></div><div class="flip-card" id="d5"></div>
            `;
        }}

        updateDigit('d0', h[0], prevTime[0][0]);
        updateDigit('d1', h[1], prevTime[0][1]);
        updateDigit('d2', m[0], prevTime[1][0]);
        updateDigit('d3', m[1], prevTime[1][1]);
        updateDigit('d4', s[0], prevTime[2][0]);
        updateDigit('d5', s[1], prevTime[2][1]);
        
        prevTime = [h, m, s];
    }}

    setInterval(tick, 1000);
    tick();
</script>
"""

st.title("🌍 全球時區翻板鐘")
st.write("點擊上方**城市名稱**可切換城市與對應時間。")

# 渲染 HTML 組件
st.components.v1.html(flip_clock_module, height=500)
