import streamlit as st

st.set_page_config(page_title="極致細節翻板鐘", layout="centered")

flip_final_html = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .clock { display: flex; gap: 12px; perspective: 1500px; }

    .flip-card {
        position: relative;
        width: 100px;
        height: 150px;
        font-family: 'Arial Black', sans-serif;
        font-size: 110px;
        color: #f0f0f0;
        text-align: center;
        background-color: #222;
        border-radius: 8px;
    }

    /* 頂部與底部靜態底板 */
    .top, .bottom {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #252525; border-radius: 8px;
    }
    .top { top: 0; border-radius: 8px 8px 0 0; line-height: 150px; z-index: 1; border-bottom: 1px solid #000; }
    .bottom { bottom: 0; border-radius: 0 0 8px 8px; line-height: 0px; z-index: 0; }

    /* 翻轉葉片容器 */
    .leaf {
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .leaf-front, .leaf-back {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        backface-visibility: hidden; background: #252525;
    }
    
    .leaf-front { 
        z-index: 2; border-radius: 8px 8px 0 0; line-height: 150px; 
        border-bottom: 1px solid #000; 
    }
    
    .leaf-back { 
        transform: rotateX(-180deg); border-radius: 0 0 8px 8px; 
        line-height: 0px; border-top: 1px solid #000;
        background: linear-gradient(to bottom, #222 0%, #333 100%); /* 增加背面陰影感 */
    }

    /* 翻轉動畫觸發時的葉片動作 */
    .flipping .leaf {
        transform: rotateX(-180deg);
    }

    /* 陰影遮罩：讓翻轉更有深度 */
    .top::after {
        content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.15); z-index: 2;
    }

    .colon { font-size: 60px; color: #444; align-self: center; margin-top: -10px; font-weight: bold; }
</style>

<div class="clock" id="clock"></div>

<script>
    let prevTime = "";

    function updateDigit(id, newVal, oldVal) {
        const el = document.getElementById(id);
        if (newVal === oldVal && el.innerHTML !== "") return;

        // 結構邏輯：
        // .top: 新數字上半部
        // .bottom: 舊數字下半部 (等著被蓋掉)
        // .leaf-front: 舊數字上半部 (開始翻下來)
        // .leaf-back: 新數字下半部 (翻過來變正面)
        
        el.innerHTML = `
            <div class="top">${newVal}</div>
            <div class="bottom">${oldVal}</div>
            <div class="leaf">
                <div class="leaf-front">${oldVal}</div>
                <div class="leaf-back">${newVal}</div>
            </div>
        `;

        // 觸發物理動畫
        el.classList.remove('flipping');
        void el.offsetWidth; 
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

st.title("🕰️ 真實物理構造翻板鐘")
st.markdown("此版本修正了葉片正反面的座標對比，並加入了漸變陰影，模擬實體葉片落下的重量感。")

st.components.v1.html(flip_final_html, height=450)
