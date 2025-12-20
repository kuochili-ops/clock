import streamlit as st

st.set_page_config(page_title="全球翻板鐘-優化版", layout="centered")

# 城市資料
CITIES = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei"},
    {"zh": "洛 杉 磯", "en": "Los Angeles", "tz": "America/Los_Angeles"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo"}
]

flip_clock_html = f"""
<style>
    body {{ background-color: #0e1117; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: "Microsoft JhengHei", sans-serif; }}
    .main-container {{ display: flex; flex-direction: column; align-items: center; gap: 35px; width: 95vw; max-width: 500px; }}
    
    /* 翻板基礎設定 */
    .flip-card {{ position: relative; background: #222; border-radius: 8px; font-weight: 900; perspective: 1000px; color: #fff; }}
    
    /* 城市翻板：分散對齊優化 */
    .city-row {{ 
        display: flex; 
        justify-content: space-between; /* 分散對齊 */
        width: 100%; 
        gap: 15px;
    }}
    .city-card {{ flex: 1; height: 85px; font-size: 1.6rem; cursor: pointer; }} /* 字體放大 */

    /* 時間翻板佈局 */
    .time-row {{ display: flex; gap: 8px; align-items: center; }}
    .time-card {{ width: 20vw; max-width: 90px; height: 28vw; max-height: 130px; font-size: 20vw; }}
    @media (min-width: 500px) {{ .time-card {{ font-size: 85px; }} }}

    /* --- 物理遮蔽模組核心 --- */
    .half {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; display: flex; justify-content: center;
    }}
    .top {{ top: 0; border-radius: 8px 8px 0 0; align-items: flex-end; border-bottom: 1px solid rgba(0,0,0,0.5); }}
    .bottom {{ bottom: 0; border-radius: 0 0 8px 8px; align-items: flex-start; }}

    /* 物理位移補償：確保文字中心點鎖定在軸線上 */
    .text-box {{
        position: absolute; width: 100%; height: 200%;
        display: flex; align-items: center; justify-content: center;
        text-align: center;
    }}
    .top .text-box {{ bottom: -100%; }}
    .bottom .text-box {{ top: -100%; }}

    /* 翻轉動畫層 */
    .leaf {{
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .leaf-front {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backface-visibility: hidden; z-index: 2; }}
    .leaf-back {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backface-visibility: hidden; transform: rotateX(-180deg); z-index: 1; }}

    .flipping .leaf {{ transform: rotateX(-180deg); }}
    .hinge {{ position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background: #000; z-index: 20; }}
</style>

<div class="main-container">
    <div class="city-row" onclick="nextCity()">
        <div class="flip-card city-card" id="czh"></div>
        <div class="flip-card city-card" id="cen"></div>
    </div>

    <div class="time-row">
        <div class="flip-card time-card" id="h0"></div>
        <div class="flip-card time-card" id="h1"></div>
        <div style="color:#444; font-size: 2.5rem; font-weight:bold; margin: 0 5px;">:</div>
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

st.components.v1.html(flip_clock_html, height=500)
