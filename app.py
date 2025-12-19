import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="真實感翻板鐘", layout="centered")

# CSS 動畫與樣式
st.markdown("""
<style>
    .clock { display: flex; gap: 10px; justify-content: center; background: #000; padding: 50px; border-radius: 15px; }
    
    /* 每一格數字的容器 */
    .digit-box {
        position: relative;
        width: 80px;
        height: 120px;
        background-color: #333;
        border-radius: 6px;
        overflow: hidden;
    }

    /* 模擬翻板中間的那條縫 */
    .digit-box::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 2px;
        background: rgba(0,0,0,0.6);
        z-index: 5;
    }

    /* 使用 sprite 圖片作為背景 */
    .base-img {
        position: absolute;
        width: 500%; /* 因為橫向有 5 個數字 */
        height: 200%; /* 因為縱向有 2 列 */
        background-image: url('https://raw.githubusercontent.com/your-username/your-repo/main/digits.png'); 
        background-size: 500% 200%;
    }

    /* 翻轉動畫：模擬卡片落下的感覺 */
    @keyframes flipDown {
        0% { transform: rotateX(0deg); }
        100% { transform: rotateX(-180deg); }
    }

    .animate-flip {
        animation: flipDown 0.6s ease-in-out;
        transform-origin: bottom;
    }
</style>
""", unsafe_allow_html=True)

def get_css_pos(char):
    if char == ":": return None
    n = int(char)
    # 計算 background-position 百分比
    x = (n % 5) * 25  # 0, 25, 50, 75, 100
    y = (n // 5) * 100 # 0, 100
    return f"{x}% {y}%"

st.title("🕰️ 真實感翻板數字鐘")

placeholder = st.empty()

while True:
    t = datetime.now().strftime("%H%M%S")
    
    html = '<div class="clock">'
    for i, char in enumerate(t):
        pos = get_css_pos(char)
        # 建立翻板 HTML 結構
        html += f'''
            <div class="digit-box">
                <div class="base-img" style="background-position: {pos};"></div>
            </div>
        '''
        if i in [1, 3]: # 加入冒號
            html += '<div style="color:white; font-size:40px; line-height:120px;">:</div>'
    html += '</div>'
    
    placeholder.markdown(html, unsafe_allow_html=True)
    time.sleep(1)
