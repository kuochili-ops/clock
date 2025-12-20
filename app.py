import streamlit as st

st.set_page_config(page_title="翻板鐘修復版", layout="centered")

CITIES_DATA = [
    {"zh": "臺    北", "en": "Taipei", "tz": "Asia/Taipei"},
    {"zh": "洛 杉 磯", "en": "Los Angeles", "tz": "America/Los_Angeles"},
    {"zh": "倫    敦", "en": "London", "tz": "Europe/London"},
    {"zh": "東    京", "en": "Tokyo", "tz": "Asia/Tokyo"},
    {"zh": "紐    約", "en": "New York", "tz": "America/New_York"}
]

flip_logic = f"""
<style>
    body {{ 
        background-color: #0e1117; 
        margin: 0; padding: 20px 0;
        display: flex; justify-content: center;
        font-family: "Microsoft JhengHei", sans-serif;
    }}
    .container {{ display: flex; flex-direction: column; align-items: center; gap: 25px; width: 100%; }}

    /* 翻板核心尺寸控制 */
    :root {{
        --city-h: 70px;
        --time-h: 110px;
        --time-w: 75px;
    }}

    .flip-card {{
        position: relative; background: #222; border-radius: 6px;
        perspective: 1000px; color: #eee; font-weight: 900;
    }}

    /* 城市區塊 */
    .city-row {{ display: flex; gap: 10px; width: 90vw; max-width: 450px; }}
    .city-card {{ flex: 1; height: var(--city-h); font-size: 1.1rem; }}

    /* 時間區塊 */
    .clock-row {{ display: flex; gap: 6px; align-items: center; }}
    .time-card {{ width: 18vw; max-width: var(--time-w); height: 25vw; max-height: var(--time-h); font-size: 15vw; }}
    @media (min-width: 500px) {{ .time-card {{ font-size: 70px; }} }}

    /* 上下半部精確對齊 */
    .top, .bottom, .leaf-front, .leaf-back {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; text-align: center;
    }}
    
    /* 城市文字定位 */
    .city-card .top, .city-card .leaf-front {{ line-height: var(--city-h); border-radius: 6px 6px 0 0; }}
    .city-card .bottom, .city-card .leaf-back {{ line-height: 0; border-radius: 0 0 6px 6px; }}

    /* 時間文字定位 */
    .time-card .top, .time-card .leaf-front {{ line-height: 25vw; border-radius: 6px 6px 0 0; }}
    .time-card .bottom, .time-card .leaf-back {{ line-height: 0; border-radius: 0 0 6px 6px; }}
    @media (min-width: 500px) {{
        .time-card .top, .time-card .leaf-front {{ line-height: var(--time-h); }}
    }}

    /* 翻轉動畫 */
    .leaf {{
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .leaf-back {{ transform: rotateX(-180deg); background: #222; border-top: 1px solid #000; }}
    .flipping .leaf {{ transform: rotateX(-180deg); }}
    
    .hinge {{
        position: absolute; top: 50%; left: 0; width: 100%; height: 1px;
        background: #000; z-index: 20; width: 100%;
    }}
</style>

<div class="container">
    <div class="city-row" onclick="nextCity()">
        <div class="flip-card city-card" id="czh"></div>
        <div class="flip-card city-card" id="cen"></div>
    </div>
    <div class="clock-row">
        <div class="flip-card time-card" id="h0"></div>
        <div class="flip-card time-card" id="h1"></div>
        <div style="color:#555; font-size: 2rem;">:</div>
        <div class="flip-card time-card" id="m0"></div>
        <div class="flip-card time-card" id="m1"></div>
    </div>
</div>

<script>
    const cities = {CITIES_DATA};
    let currentIdx = 0;
    let pTime = ["", ""];
    let pCity = {{zh:"", en:""}};

    function update(id, nv, ov) {{
        const el = document.getElementById(id);
        if (nv === ov && el.innerHTML !== "") return;
        el.innerHTML = `
            <div class="top">${{nv}}</div>
            <div class="bottom">${{ov || nv}}</div>
            <div class="leaf">
                <div class="leaf-front">${{ov || nv}}</div>
                <div class="leaf-back">${{nv}}</div>
            </div>
            <div class="hinge"></div>
        `;
        el.classList.remove('flipping');
        void el.offsetWidth;
        el.classList.add('flipping');
    }}

    function nextCity() {{
        currentIdx = (currentIdx + 1) % cities.length;
        tick();
    }}

    function tick() {{
        const c = cities[currentIdx];
        const now = new Date();
        const f = new Intl.DateTimeFormat('en-US', {{
            timeZone: c.tz, hour12: false, hour: '2-digit', minute: '2-digit'
        }});
        const parts = f.formatToParts(now);
        const h = parts.find(p => p.type === 'hour').value;
        const m = parts.find(p => p.type === 'minute').value;

        update('czh', c.zh, pCity.zh);
        update('cen', c.en, pCity.en);
        update('h0', h[0], pTime[0][0]);
        updateCard('h1', h[1], pTime[0][1]); // 修正為 update
        update('h1', h[1], pTime[0][1]);
        update('m0', m[0], pTime[1][0]);
        update('m1', m[1], pTime[1][1]);

        pTime = [h, m];
        pCity = {{zh: c.zh, en: c.en}};
    }}
    // 修正上面小手誤，統一使用 update 函式
    function updateCard(id, nv, ov) {{ update(id, nv, ov); }}

    setInterval(tick, 1000);
    tick();
</script>
"""

st.components.v1.html(flip_logic, height=400)
