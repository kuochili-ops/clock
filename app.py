import streamlit as st

st.set_page_config(page_title="極致擬真機械翻板鐘", layout="centered")

flip_final_html = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; }
    .clock { display: flex; gap: 12px; perspective: 1500px; }

    .flip-card {
        position: relative;
        width: 100px;
        height: 150px;
        font-family: 'Arial Black', sans-serif;
        font-size: 110px;
        font-weight: bold;
        color: #f0f0f0;
        text-align: center;
        background-color: #222;
        border-radius: 8px;
    }

    /* 靜態底層 */
    .top, .bottom {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; border: 1px solid #111;
    }
    .top { top: 0; border-radius: 8px 8px 0 0; line-height: 150px; border-bottom: 0.5px solid #000; }
    .bottom { bottom: 0; border-radius: 0 0 8px 8px; line-height: 0px; }

    /* 動態翻轉葉片 */
    .leaf {
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.3, 0, 0.2, 1);
    }

    .leaf-front, .leaf-back {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        backface-visibility: hidden; background: #222; overflow: hidden;
    }

    .leaf-front { 
        z-index: 2; border-radius: 8px 8px 0 0; line-height: 150px; 
        border-bottom: 0.5px solid #000; 
    }

    .leaf-back { 
        transform: rotateX(-180deg); border-radius: 0 0 8px 8px; 
        line-height: 0px; border-top: 0.5px solid #000;
        background: linear-gradient(to top, #222 50%, #181818 100%);
    }

    /* 動畫狀態：讓落下更有弧度感 */
    .flipping .leaf { transform: rotateX(-180deg); }

    /* 中軸陰影與光澤 */
    .hinge {
        position: absolute; top: 50%; left: 0; width: 100%; height: 3px;
        background: #000; z-index: 15; transform: translateY(-50%);
        box-shadow: 0 1px 2px rgba(255,255,255,0.08);
    }

    .colon { font-size: 60px; color: #444; align-self: center; margin-top: -10px; }
</style>

<div class="clock" id="clock"></div>

<script>
    let prevTime = "";

    function updateDigit(id, newVal, oldVal) {
        const el = document.getElementById(id);
        if (newVal === oldVal && el.innerHTML !== "") return;

        // 核心物理圖層
        el.innerHTML = `
            <div class="top static">${newVal}</div>
            <div class="bottom static">${oldVal}</div>
            <div class="leaf">
                <div class="leaf-front">${oldVal}</div>
                <div class="leaf-back">${newVal}</div>
            </div>
            <div class="hinge"></div>
        `;

        el.classList.remove('flipping');
        void el.offsetWidth; // 觸發 reflow 確保動畫重啟
        el.classList.add('flipping');
    }

    function tick() {
        const now = new Date();
        const timeStr = now.getHours().toString().padStart(2, '0') + 
                        now.getMinutes().toString().padStart(2, '0') + 
                        now.getSeconds().toString().padStart(2, '0');

        if (prevTime === "") {
            const clockEl = document.getElementById('clock');
            let html = '';
            for (let i = 0; i < 6; i++) {
                html += `<div class="flip-card" id="d${i}"></div>`;
                if (i === 1 || i === 3) html += '<div class="colon">:</div>';
            }
            clockEl.innerHTML = html;
        }

        for (let i = 0; i < 6; i++) {
            updateDigit(`d${i}`, timeStr[i], prevTime[i] || timeStr[i]);
        }
        prevTime = timeStr;
    }

    setInterval(tick, 1000);
    tick();
</script>
"""

st.title("🕰️ 極致物理翻板鐘 (Final Version)")
st.markdown("細節改進：微調了翻轉路徑與陰影，模擬實體葉片受重力落下的質感。")

st.components.v1.html(flip_final_html, height=500)
