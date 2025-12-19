import streamlit as st

st.set_page_config(page_title="極致真實翻板鐘", layout="centered")

flip_ultra_html = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; }
    .clock { display: flex; gap: 10px; perspective: 1500px; }

    .flip-card {
        position: relative;
        width: 100px;
        height: 150px;
        font-family: 'Arial Black', sans-serif;
        font-size: 110px;
        color: #f0f0f0;
        border-radius: 12px;
    }

    /* 靜態背景層 */
    .static {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; border: 1px solid #111;
    }
    .top { top: 0; border-radius: 8px 8px 0 0; line-height: 150px; border-bottom: 0.5px solid #000; }
    .bottom { bottom: 0; border-radius: 0 0 8px 8px; line-height: 0px; }

    /* 動態翻轉層 */
    .leaf {
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 5; transform-origin: bottom;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
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
        background: linear-gradient(to top, #222 50%, #111 100%); /* 增加背面陰影 */
    }

    /* 動畫啟動狀態 */
    .flipping .leaf { transform: rotateX(-180deg); }

    /* 中間的中軸線 */
    .hinge {
        position: absolute; top: 50%; left: 0; width: 100%; height: 3px;
        background: #000; z-index: 10; transform: translateY(-50%);
        box-shadow: 0 1px 2px rgba(255,255,255,0.05);
    }

    .colon { font-size: 60px; color: #444; align-self: center; margin-top: -10px; }
</style>

<div class="clock" id="clock"></div>

<script>
    let prevTime = "";

    function updateDigit(id, newVal, oldVal) {
        const el = document.getElementById(id);
        if (newVal === oldVal && el.innerHTML !== "") return;

        // 真正的物理構造：
        // 1. .top: 顯示【新】上半部 (在葉片後面預備)
        // 2. .bottom: 顯示【舊】下半部 (等著被蓋住)
        // 3. .leaf-front: 顯示【舊】上半部 (開始向下翻轉)
        // 4. .leaf-back: 顯示【新】下半部 (翻過來變正面)
        
        el.innerHTML = `
            <div class="static top">${newVal}</div>
            <div class="static bottom">${oldVal}</div>
            <div class="leaf">
                <div class="leaf-front">${oldVal}</div>
                <div class="leaf-back">${newVal}</div>
            </div>
            <div class="hinge"></div>
        `;

        el.classList.remove('flipping');
        void el.offsetWidth; // 觸發 reflow
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

st.title("🕰️ 機械物理翻板鐘 (終極修正版)")
st.markdown("此版本模擬 **四層物理葉片** 的重疊邏輯，您可以清楚看到舊上半部翻下成為新下半部的過程。")

st.components.v1.html(flip_ultra_html, height=500)
