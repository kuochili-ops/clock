import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="真實感翻板鐘", layout="centered")

# 這裡建議將圖片上傳到 GitHub 後，獲取其 Raw 連結
# 例如: https://raw.githubusercontent.com/您的帳號/repo名/main/digits.png
IMAGE_URL = "digits.png" 

st.markdown(f"""
<style>
    /* 修正背景與文字顯示 */
    .stApp {{ background-color: #0e1117; }}
    
    .clock-container {{
        display: flex;
        gap: 8px;
        justify-content: center;
        align-items: center;
        padding: 40px;
        background: #000;
        border-radius: 15px;
    }}

    /* 翻板外框 */
    .digit-box {{
        position: relative;
        width: 60px;   /* 根據圖片比例調整 */
        height: 90px;
        background-color: #222;
        border-radius: 4px;
        overflow: hidden;
        border: 1px solid #444;
    }}

    /* 中間的機械縫隙 */
    .digit-box::after {{
        content: "";
        position: absolute;
        top: 49%;
        left: 0;
        width: 100%;
        height: 2px;
        background: rgba(0,0,0,0.8);
        z-index: 10;
        box-shadow: 0 1px 2px rgba(255,255,255,0.1);
    }}

    /* 圖片素材定位 - 針對您的 digits.png 進行精確百分比計算 */
    .digit-img {{
        position: absolute;
        width: 540%;  /* 放大倍數以符合 5x2 網格 */
        height: 240%;
        background-image: url("{IMAGE_URL}");
        background-repeat: no-repeat;
        /* 平滑過渡動畫 */
        transition: background-position 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }}
</style>
""", unsafe_allow_html=True)

def get_position(char):
    if not char.isdigit(): return "0% 0%"
    n = int(char)
    # 根據原圖比例計算出的精確百分比位置
    # 橫向 5 個 (0,1,2,3,4) (5,6,7,8,9)
    # 由於原圖周圍有留白，這裡使用微調後的數值
    col = n % 5
    row = n // 5
    
    x_map = [12.5, 31.2, 50, 68.8, 87.5] # 0-4 的 X 軸中心點
    y_map = [32, 68] # 第一列與第二列的 Y 軸中心點
    
    return f"{x_map[col]}% {y_map[row]}%"

st.title("🕰️ 真實感翻板數字鐘")

placeholder = st.empty()

while True:
    now = datetime.now().strftime("%H%M%S")
    
    # 構建 HTML，注意：Streamlit 必須使用 unsafe_allow_html=True
    html_content = '<div class="clock-container">'
    for i, char in enumerate(now):
        pos = get_position(char)
        html_content += f'''
            <div class="digit-box">
                <div class="digit-img" style="background-position: {pos};"></div>
            </div>
        '''
        if i in [1, 3]: # 冒號
            html_content += '<div style="color:#555; font-size:30px; font-weight:bold;">:</div>'
    html_content += '</div>'
    
    # 關鍵：這裡必須使用 st.markdown 並開啟 HTML 渲染
    placeholder.markdown(html_content, unsafe_allow_html=True)
    time.sleep(1)
