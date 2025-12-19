import streamlit as st

st.set_page_config(page_title="極致物理翻板鐘", layout="centered")

flip_js_html = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .clock { display: flex; gap: 12px; perspective: 1000px; }

    .flip-card {
        position: relative;
        width: 100px;
        height: 150px;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 110px;
        font-weight: bold;
        line-height: 150px;
        text-align: center;
        color: #ddd;
    }

    /* 靜態底板：上半部與下半部 */
    .top, .bottom {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; border-radius: 8px;
    }
    .top { top: 0; border-radius: 8px 8px 0 0; line-height: 150px; z-index: 1; border-bottom: 1px solid #000; }
    .bottom { bottom: 0; border-radius: 0 0 8px 8px; line-height: 0px; z-index: 0; }

    /* 翻轉葉片 */
    .leaf {
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .leaf-front, .leaf-back {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        backface-visibility: hidden; background: #222; border-radius: 8px 8px 0 0;
    }
    .leaf-front { z-index: 2; line-height: 150px; border-bottom: 1px solid #000; }
    .leaf-back { 
        transform: rotateX(-180deg); line-height: 0px; 
        border-radius: 0 0 8px 8px; border-top: 1px solid #000;
    }

    /* 動畫狀態 */
    .flipping .leaf { transform: rotateX(-180deg); }

    .colon { font-size: 60px; color: #444; align-self: center; margin-top: -10px; }
</style>

<div class="clock" id="clock"></div>

<script>
    let prevTime = "";

    function updateDigit(id, newVal, oldVal) {
        const el = document.getElementById(id);
        if (newVal === oldVal) return;

        // 建立四層結構
        el.innerHTML = `
            <div class="top">${newVal}</div>
            <div class="bottom">${oldVal}</div>
            <div class="leaf">
                <div class="leaf-front">${oldVal}</div>
                <div class="leaf-back">${newVal}</div>
            </div>
        `;

        // 觸發動畫
        el.classList.remove('flipping');
        void el.offsetWidth; // 強制重繪
        el.classList.add('flipping');
    }

    function initClock() {
        const clockEl = document.getElementById('clock');
        let html = '';
        for (let i = 0; i < 6; i++) {
            html += `<div class="flip-card" id="d${i}"></div>`;
            if (i === 1 || i === 3) html += '<div class="colon">:</div>';
        }
        clockEl.innerHTML = html;
    }

    function tick() {
        const now = new Date();
        const timeStr = now.getHours().toString().padStart(2, '0') + 
                        now.getMinutes().toString().padStart(2, '0') + 
                        now.getSeconds().toString().padStart(2, '0');

        for (let i = 0; i < 6; i++) {
            updateDigit(`d${i}`, timeStr[i], prevTime[i] || timeStr[i]);
        }
        prevTime = timeStr;
    }

    initClock();
    setInterval(tick, 1000);
    tick();
</script>
"""

st.title("🕰️ 真實分頁機械翻板鐘")
st.markdown("這段代碼模擬了**物理葉片掉落**：舊數字的上半部會向下翻轉，露出新數字的下半部。")

st.components.v1.html(flip_js_html, height=450)
