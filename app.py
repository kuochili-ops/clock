import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="真實翻板時鐘", layout="centered")

# CSS 注入：建立 3D 翻板視覺效果
flip_clock_html = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .clock { display: flex; gap: 15px; align-items: center; }
    
    .digit-container {
        position: relative;
        width: 80px;
        height: 120px;
        background-color: #333;
        border-radius: 8px;
        font-family: 'Helvetica', sans-serif;
        font-size: 80px;
        font-weight: bold;
        color: white;
        text-align: center;
        line-height: 120px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    /* 中間的機械摺痕 */
    .digit-container::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 3px;
        background: #000;
        z-index: 10;
    }

    /* 頂部半部陰影 */
    .digit-container::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 50%;
        background: rgba(0,0,0,0.1);
        border-radius: 8px 8px 0 0;
    }

    .colon { font-size: 60px; color: #555; font-family: sans-serif; }
</style>

<div class="clock" id="clock"></div>

<script>
    function updateClock() {
        const now = new Date();
        const timeStr = now.getHours().toString().padStart(2, '0') + 
                        now.getMinutes().toString().padStart(2, '0') + 
                        now.getSeconds().toString().padStart(2, '0');
        
        let html = '';
        for (let i = 0; i < timeStr.length; i++) {
            html += `<div class="digit-container">${timeStr[i]}</div>`;
            if (i === 1 || i === 3) html += '<div class="colon">:</div>';
        }
        document.getElementById('clock').innerHTML = html;
    }
    setInterval(updateClock, 1000);
    updateClock();
</script>
"""

st.title("🕰️ 真實感翻板數字鐘")
st.write("採用 CSS 物理渲染，解決圖片偏移與代碼顯示問題")

# 使用 components 確保 HTML 渲染
st.components.v1.html(flip_clock_html, height=300)
