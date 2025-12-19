import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="真實翻板鐘", layout="centered")

# --- 1. 定義精確座標 (基於您的 digits.png) ---
# 這些數值是根據 5x2 網格微調後的像素偏移量
digit_map = {
    '0': '0px 0px',      '1': '-60px 0px',    '2': '-120px 0px',   '3': '-180px 0px',   '4': '-240px 0px',
    '5': '0px -90px',    '6': '-60px -90px',  '7': '-120px -90px', '8': '-180px -90px', '9': '-240px -90px'
}

# --- 2. 注入 CSS 樣式 ---
st.markdown("""
<style>
    .clock-container {
        display: flex;
        gap: 10px;
        justify-content: center;
        align-items: center;
        background-color: #111;
        padding: 30px;
        border-radius: 15px;
    }
    .flip-card {
        position: relative;
        width: 60px;   /* 單個數字寬度 */
        height: 90px;  /* 單個數字高度 */
        background-color: #222;
        border-radius: 4px;
        overflow: hidden;
        border: 1px solid #333;
    }
    .digit-sprite {
        width: 300px;  /* 總寬度 (60*5) */
        height: 180px; /* 總高度 (90*2) */
        background-image: url("https://raw.githubusercontent.com/your-username/your-repo/main/digits.png");
        background-size: 300px 180px;
        background-repeat: no-repeat;
        transition: background-position 0.4s ease-in-out;
    }
    /* 中間那條真實的縫隙 */
    .flap-line {
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 2px;
        background: rgba(0,0,0,0.7);
        z-index: 10;
        box-shadow: 0 1px 1px rgba(255,255,255,0.1);
    }
    .colon { color: #555; font-size: 40px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🕰️ 真實感翻板數字鐘")

# 建立顯示容器
placeholder = st.empty()

while True:
    t = datetime.now().strftime("%H:%M:%S")
    
    # 構建 HTML
    html = '<div class="clock-container">'
    for i, char in enumerate(t):
        if char == ":":
            html += '<div class="colon">:</div>'
        else:
            pos = digit_map.get(char, "0px 0px")
            html += f'''
                <div class="flip-card">
                    <div class="flap-line"></div>
                    <div class="digit-sprite" style="background-position: {pos};"></div>
                </div>
            '''
    html += '</div>'
    
    # 核心修正：使用 unsafe_allow_html=True 確保渲染 HTML
    placeholder.markdown(html, unsafe_allow_html=True)
    time.sleep(1)
