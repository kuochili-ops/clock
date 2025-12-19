import streamlit as st

st.set_page_config(page_title="硬核物理翻板鐘", layout="centered")

flip_html = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .clock { display: flex; gap: 15px; perspective: 1000px; }

    /* 單個數字容器 */
    .flap-unit {
        position: relative;
        width: 80px;
        height: 120px;
        background-color: #333;
        border-radius: 8px;
        font-family: 'Helvetica', sans-serif;
        font-size: 80px;
        font-weight: bold;
        line-height: 120px;
        text-align: center;
        color: white;
    }

    /* 上下半部的共通樣式 */
    .top, .bottom {
        position: absolute;
        width: 100%;
        height: 50%;
        overflow: hidden;
        background-color: #333;
        left: 0;
        z-index: 1;
    }
    .top {
        top: 0;
        border-radius: 8px 8px 0 0;
        line-height: 120px; /* 顯示上半部 */
        border-bottom: 1px solid rgba(0,0,0,0.5);
    }
    .bottom {
        bottom: 0;
        border-radius: 0 0 8px 8px;
        line-height: 0px; /* 顯示下半部 */
    }

    /* 翻轉葉片核心 */
    .leaf {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 50%;
        z-index: 5;
        transform-origin: bottom;
        transition: transform 0.6s ease-in;
        transform-style: preserve-3d;
    }

    /* 葉片正面 (舊數字上半部) */
    .leaf-front {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #333;
        backface-visibility: hidden;
        z-index: 2;
        border-radius: 8px 8px 0 0;
    }

    /* 葉片背面 (新數字下半部) */
    .leaf-back {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #333;
        transform: rotateX(-180deg);
        backface-visibility: hidden;
        border-radius: 0 0 8px 8px;
        line-height: 0px; /* 顯示下半部 */
        border-top: 1px solid rgba(0,0,0,0.5);
    }

    /* 翻轉觸發動作 */
    .flipping .leaf {
        transform: rotateX(-180deg);
    }

    .colon { font-size: 60px; color: #555; align-self: center; }
</style>

<div class="clock" id="clock"></div>

<script>
    let lastTime = "";

    function createDigit(val, lastVal) {
        const isChanged = lastVal !== undefined && val !== lastVal;
        const animationClass = isChanged ? 'flipping' : '';
        
        // 如果沒變，顯示靜態數字；如果變了，執行翻頁構造
        return `
            <div class="flap-unit ${animationClass}">
                <div class="top">${val}</div>
                <div class="bottom">${lastVal !== undefined ? lastVal : val}</div>
                <div class="leaf">
                    <div class="leaf-front">${lastVal !== undefined ? lastVal : val}</div>
                    <div class="leaf-back">${val}</div>
                </div>
            </div>
        `;
    }

    function updateClock() {
        const now = new Date();
        const timeStr = now.getHours().toString().padStart(2, '0') + 
                        now.getMinutes().toString().padStart(2, '0') + 
                        now.getSeconds().toString().padStart(2, '0');
        
        if (timeStr === lastTime) return;

        let html = '';
        for (let i = 0; i < timeStr.length; i++) {
            html += createDigit(timeStr[i], lastTime[i]);
            if (i === 1 || i === 3) html += '<div class="colon">:</div>';
        }
        
        document.getElementById('clock').innerHTML = html;
        lastTime = timeStr;
    }

    setInterval(updateClock, 1000);
    updateClock();
</script>
"""

st.title("🕰️ 物理級分葉翻板鐘")
st.write("模擬真實機械構造：上半部葉片落下並翻轉 180 度。")

st.components.v1.html(flip_html, height=400)
