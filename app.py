import streamlit as st

st.set_page_config(page_title="全球極致大字翻板鐘", layout="centered")

# 擴充城市資料：涵蓋全球主要金融/旅遊中心
CITIES = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo"},
    {"zh": "新 加 坡", "en": "Singapore", "tz": "Asia/Singapore"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London"},
    {"zh": "巴 黎", "en": "Paris", "tz": "Europe/Paris"},
    {"zh": "紐 約", "en": "New York", "tz": "America/New_York"},
    {"zh": "洛 杉 磯", "en": "Los Angeles", "tz": "America/Los_Angeles"},
    {"zh": "雪 黎", "en": "Sydney", "tz": "Australia/Sydney"}
]

flip_clock_html = f"""
<style>
    body {{ 
        background-color: #0e1117; 
        margin: 0; 
        display: flex; justify-content: center; align-items: center; 
        min-height: 100vh; 
        font-family: "Microsoft JhengHei", "PingFang TC", "Apple LiGothic", sans-serif;
    }}
    
    .main-container {{ 
        display: flex; flex-direction: column; align-items: center; 
        gap: 20px; width: 98vw; max-width: 600px; 
    }}
    
    /* 翻板基礎 */
    .flip-card {{ 
        position: relative; background: #1a1a1a; 
        border-radius: 4px; font-weight: 900; 
        perspective: 1000px; color: #ffffff; 
        overflow: hidden;
    }}
    
    /* 城市區塊：字體最大化 */
    .city-row {{ 
        display: flex; justify-content: space-between; 
        width: 100%; gap: 10px; 
    }}
    .city-card {{ 
        flex: 1; height: 100px; 
        /* 使用 clamp 讓字體在手機與電腦間自動取最大值而不變形 */
        font-size: clamp(1.4rem, 5vw, 2.5rem); 
        cursor: pointer; 
    }}

    /* 時間區塊：極致大字 */
    .time-row {{ display: flex; gap: 5px; align-items: center; width: 100%; justify-content: center; }}
    .time-card {{ 
        width: 22vw; max-width: 130px; 
        height: 32vw; max-height: 180px; 
        font-size: clamp(4rem, 24vw, 150px); 
    }}
    
    .colon {{ 
        color: #444; font-size: 3rem; font-weight: bold; 
        line-height: 1; margin: 0 2px;
    }}

    /* --- 物理遮蔽模組核心 (完全填滿) --- */
    .half {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #1a1a1a; 
        display: flex; justify-content: center;
    }}
    .top {{ top: 0; border-bottom: 1px solid rgba(0,0,0,0.8); align-items: flex-end; }}
    .bottom {{ bottom: 0; align-items: flex-start; }}

    /* 文字容器：確保 200% 高度完全覆蓋上下半部 */
    .text-box {{
        position: absolute; width: 100%; height: 200%;
        display: flex; align-items: center; justify-content: center;
        text-align: center; white-space: nowrap; /* 避免英文換行變形 */
    }}
    .top .text-box {{ bottom: -100%; }}
    .bottom .text-box {{ top: -100%; }}

    /* 翻轉動畫層 */
    .leaf {{
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .leaf-front, .leaf-back {{ 
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
        backface-visibility: hidden; 
    }}
    .leaf-back {{ transform: rotateX(-180deg); }}

    .flipping .leaf {{ transform: rotateX(-180deg); }}
    .hinge {{ 
        position: absolute; top: 50%; left: 0; width: 100%; height: 2px; 
        background: #000; z-index: 20; 
    }}
</style>

<div class="main-container">
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

        pT = [h, m]; pC = {{zh: c.zh, en: c.en}};
    }}

    setInterval(tick, 1000);
    tick();
</script>
"""

st.components.v1.html(flip_clock_html, height=600)
