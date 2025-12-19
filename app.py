import streamlit as st
import time
from datetime import datetime

# 設定網頁
st.set_page_config(page_title="極簡翻板鐘", layout="centered")

# CSS 樣式：模擬機械翻板外觀
st.markdown("""
    <style>
    .clock-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        background-color: #1a1a1a;
        padding: 40px;
        border-radius: 20px;
    }
    .flip-unit {
        background: linear-gradient(180deg, #333 48%, #111 50%, #333 52%);
        color: white;
        font-family: 'Courier New', Courier, monospace;
        font-size: 80px;
        font-weight: bold;
        width: 80px;
        height: 120px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 8px;
        border: 1px solid #000;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .colon {
        font-size: 60px;
        color: #555;
        line-height: 120px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🕰️ 精確版機械翻板鐘")
st.write("此版本直接由程式繪製，解決圖片裁切位移問題。")

clock_placeholder = st.empty()

while True:
    now = datetime.now().strftime("%H:%M:%S")
    
    # 建立時鐘 HTML
    html_str = '<div class="clock-container">'
    for char in now:
        if char == ":":
            html_str += f'<div class="colon">:</div>'
        else:
            html_str += f'<div class="flip-unit">{char}</div>'
    html_str += '</div>'
    
    clock_placeholder.markdown(html_str, unsafe_allow_html=True)
    time.sleep(1)
