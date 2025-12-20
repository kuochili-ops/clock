import streamlit as st

st.set_page_config(page_title="全球翻板鐘-物理遮蔽版", layout="centered")

# 城市資料定義
CITIES = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei"},
    {"zh": "洛杉磯", "en": "Los Angeles", "tz": "America/Los_Angeles"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo"}
]

# 物理遮蔽翻板模組邏輯
flip_module_html = f"""
<style>
    body {{ background-color: #0e1117; margin: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; font-family: sans-serif; color: #eee; }}
    .main-container {{ display: flex; flex-direction: column; align-items: center; gap: 30px; padding: 20px; width: 100%; box-sizing: border-box; }}
    
    /* 基礎翻板樣式 */
    .flip-card {{ position: relative; background: #222; border-radius: 6px; font-weight: 900; perspective: 1000px; }}
    .city-row {{ display: flex; gap: 10px; width: 100%; max-width: 450px; }}
    .city-card {{ flex: 1; height: 75px; font-size: 1.2rem; cursor: pointer; }}
    .time-row {{ display: flex; gap: 8px; align-items: center; }}
    .time-card {{ width: 20vw; max-width: 85px; height: 28vw; max-height: 120px; font-size: 18vw; }}
    @media (min-width: 500px) {{ .time-card {{ font-size: 80px; }} }}

    /* 物理遮蔽核心：強制切分上下半部 */
    .half {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; display: flex; justify-content: center;
    }}
    .top {{ top: 0; border-radius: 6px 6px 0 0; align-items: flex-end; border-bottom: 1px solid rgba(0,0,0,0.4); }}
    .bottom {{ bottom: 0; border-radius: 0 0 6px 6px; align-items: flex-start; }}

    /* 文字容器偏移：強制讓文字中心對準翻板中線 */
    .text-box {{
        position: absolute; width: 100%; height: 200%;
        display: flex; align-items: center; justify-content: center;
    }}
    .top .text-box {{ bottom: -100%; }}  /* 上半部：將文字拉下一半 */
    .bottom .text-box {{ top: -100%; }}   /* 下半部：將文字拉上一半 */

    /* 翻轉葉片 */
    .leaf {{
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .leaf-front {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backface-visibility: hidden; z-index: 2; }}
    .leaf-back {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backface-visibility: hidden; transform: rotateX(-180deg); z-index: 1; }}

    .flipping .leaf {{ transform: rotateX(-180deg); }}
    .hinge {{ position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background: #000; z-index: 20; transform: translateY(-50%); }}
</style>

<div class="main-container">
    <div class="city-row" onclick="nextCity()">
        <div class="flip-card city-card" id="czh"></div>
        <div class="flip-card city-card" id="cen"></div>
    </div>
    <div class="time-row">
        <div class="flip-card time-card" id="h0"></div>
        <div class="flip-card time-card" id="h1"></div>
        <div style="color:#555; font-size: 2.5rem; font-weight:bold;">:</div>
        <div class="flip-card time-card" id="m0"></div>
        <div class="flip-card time-card" id="m1"></div>
    </div>
</div>

<script>
    const cities = {CITIES};
    let curIdx = 0;
    let pT = ["", ""];
    let pC = {{zh: "", en: ""}};

    // 物理遮蔽更新函式
    function updateFlip(id, newVal, oldVal) {{
        const el = document.getElementById(id);
        if (newVal === oldVal && el.innerHTML !== "") return;

        // 核心結構：四層半板確保物理遮蔽無殘留
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

st.components.v1.html(flip_module_html, height=500)
