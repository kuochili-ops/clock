import streamlit as st

st.set_page_config(page_title="𓃥白六世界時鐘", layout="centered")

# 擴充城市資料：加入模擬天氣數據
CITIES = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "weather": "晴時多雲", "temp": "19~22°C"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "weather": "陣雨", "temp": "8~12°C"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "weather": "陰天", "temp": "5~9°C"},
    {"zh": "紐 約", "en": "New York", "tz": "America/New_York", "weather": "多雲", "temp": "2~7°C"},
    {"zh": "巴 黎", "en": "Paris", "tz": "Europe/Paris", "weather": "晴朗", "temp": "6~11°C"},
    {"zh": "洛 杉 磯", "en": "Los Angeles", "tz": "America/Los_Angeles", "weather": "晴朗", "temp": "15~24°C"},
    {"zh": "雪 黎", "en": "Sydney", "tz": "Australia/Sydney", "weather": "雷雨", "temp": "20~26°C"}
]

flip_clock_html = f"""
<style>
    body {{ 
        background-color: #0e1117; margin: 0; 
        display: flex; justify-content: center; align-items: flex-start; /* 改為從頂部開始 */
        min-height: 100vh; font-family: "Microsoft JhengHei", sans-serif;
        padding-top: 5vh; /* 畫面上移 */
    }}
    
    .app-container {{ 
        display: flex; flex-direction: column; align-items: center; 
        gap: 20px; width: 95vw; max-width: 550px; 
    }}

    .app-title {{ color: #444; font-size: 0.9rem; letter-spacing: 5px; font-weight: bold; margin-bottom: 10px; }}
    
    .flip-card {{ position: relative; background: #1a1a1a; border-radius: 8px; font-weight: 900; perspective: 1000px; color: #fff; overflow: hidden; }}
    
    /* 城市與天氣翻板：分散對齊與統一高度 */
    .row-flex {{ display: flex; justify-content: space-between; width: 100%; gap: 12px; }}
    .info-card {{ flex: 1; height: 90px; font-size: clamp(1.2rem, 5vw, 1.8rem); cursor: pointer; }}

    /* 時間翻板：極致加高 */
    .time-row {{ display: flex; gap: 6px; align-items: center; justify-content: center; width: 100%; }}
    .time-card {{ 
        width: 22vw; max-width: 110px; 
        height: 40vw; max-height: 190px; 
        font-size: clamp(4.5rem, 26vw, 155px); 
    }}
    .colon {{ color: #333; font-size: 3.5rem; font-weight: bold; margin-bottom: 15px; }}

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
        <div class="flip-card info-card" id="w_status" style="background: #151515; font-size: 1.4rem; color: #aaa;"></div>
        <div class="flip-card info-card" id="w_temp" style="background: #151515; font-size: 1.4rem; color: #888;"></div>
    </div>
</div>

<script>
    const cities = {CITIES};
    let curIdx = 0;
    let pT = ["", ""];
    let pC = {{zh: "", en: ""}};
    let pW = {{status: "", temp: ""}};

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

        // 更新城市雙板
        updateFlip('czh', c.zh, pC.zh);
        updateFlip('cen', c.en, pC.en);
        
        // 更新時間
        updateFlip('h0', h[0], pT[0] ? pT[0][0] : "");
        updateFlip('h1', h[1], pT[0] ? pT[0][1] : "");
        updateFlip('m0', m[0], pT[1] ? pT[1][0] : "");
        updateFlip('m1', m[1], pT[1] ? pT[1][1] : "");

        // 更新天氣雙板
        updateFlip('w_status', c.weather, pW.status);
        updateFlip('w_temp', c.temp, pW.temp);

        pT = [h, m]; 
        pC = {{zh: c.zh, en: c.en}};
        pW = {{status: c.weather, temp: c.temp}};
    }}

    setInterval(tick, 1000);
    tick();
</script>
"""

st.components.v1.html(flip_clock_html, height=750)
