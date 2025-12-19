import streamlit as st

st.set_page_config(page_title="3D 真實翻板時鐘", layout="centered")

# CSS + JS：完整 3D 翻轉邏輯
flip_clock_html = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; }
    .clock { display: flex; gap: 10px; align-items: center; perspective: 1000px; }
    
    .flip-unit {
        position: relative;
        width: 80px;
        height: 120px;
        background-color: #333;
        border-radius: 8px;
        font-family: 'Helvetica', Arial, sans-serif;
        font-size: 80px;
        font-weight: bold;
        color: white;
        text-align: center;
        line-height: 120px;
    }

    /* 頂部與底部的分界線 */
    .flip-unit::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 2px;
        background: #000;
        z-index: 10;
        transform: translateY(-50%);
    }

    /* 翻轉動畫類別 */
    .flipping {
        animation: flip-down 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    @keyframes flip-down {
        0% { transform: rotateX(0deg); }
        50% { transform: rotateX(-90deg); background-color: #444; }
        100% { transform: rotateX(0deg); }
    }

    .colon { font-size: 60px; color: #555; padding-bottom: 10px; }
</style>

<div class="clock" id="clock"></div>

<script>
    let lastTime = "";

    function updateClock() {
        const now = new Date();
        const timeStr = now.getHours().toString().padStart(2, '0') + 
                        now.getMinutes().toString().padStart(2, '0') + 
                        now.getSeconds().toString().padStart(2, '0');
        
        const clockEl = document.getElementById('clock');
        
        // 如果時間沒變就不更新，避免重複觸發動畫
        if (timeStr === lastTime) return;

        let html = '';
        for (let i = 0; i < timeStr.length; i++) {
            // 檢查該位數是否改變，若改變則加入動畫類別
            const isChanged = lastTime && timeStr[i] !== lastTime[i];
            const animationClass = isChanged ? 'flipping' : '';
            
            html += `<div class="flip-unit ${animationClass}">${timeStr[i]}</div>`;
            if (i === 1 || i === 3) html += '<div class="colon">:</div>';
        }
        
        clockEl.innerHTML = html;
        lastTime = timeStr;
    }

    setInterval(updateClock, 1000);
    updateClock();
</script>
"""

st.title("🕰️ 3D 真實翻板鐘")
st.write("現在數字在切換時會觸發 3D 翻轉動畫")

st.components.v1.html(flip_clock_html, height=400)
