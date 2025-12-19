import streamlit as st
from PIL import Image
import time
from datetime import datetime

# 設定網頁
st.set_page_config(page_title="機械翻板數字鐘", layout="centered")

def get_digit(digit_char, sprite_sheet):
    """
    精確裁切數字，解決偏移問題
    """
    try:
        n = int(digit_char)
    except ValueError:
        return None
        
    w, h = sprite_sheet.size
    
    # --- 關鍵修正：根據素材圖比例設定邊界 ---
    # 這裡的數值是根據您的素材圖微調過的比例
    top_pad = 0.28    # 頂部留白
    bottom_pad = 0.28 # 底部留白
    left_pad = 0.12   # 左側留白
    right_pad = 0.12  # 右側留白
    
    # 計算數字區域
    draw_w = w * (1 - left_pad - right_pad)
    draw_h = h * (1 - top_pad - bottom_pad)
    
    unit_w = draw_w / 5
    unit_h = draw_h / 2
    
    row = n // 5
    col = n % 5
    
    # 計算裁切座標
    left = (w * left_pad) + (col * unit_w)
    top = (h * top_pad) + (row * unit_h)
    right = left + unit_w
    bottom = top + unit_h
    
    # 稍微向內縮 1 像素，避免抓到鄰近數字的邊緣
    return sprite_sheet.crop((left + 1, top + 1, right - 1, bottom - 1))

def create_clock_image(time_str, sprite_path):
    sprite_sheet = Image.open(sprite_path).convert("RGBA")
    digits = []
    
    for char in time_str:
        if char == ":":
            # 建立一個寬度較窄的空格作為冒號分隔（或自行畫兩個圓點）
            colon = Image.new('RGBA', (30, 200), (0,0,0,0)) 
            digits.append(colon)
        else:
            digit_img = get_digit(char, sprite_sheet)
            if digit_img:
                # 統一縮放高度，保持整齊
                digit_img = digit_img.resize((120, 180), Image.Resampling.LANCZOS)
                digits.append(digit_img)
    
    # 水平拼接所有數字
    total_width = sum(d.size[0] for d in digits)
    combined_img = Image.new('RGBA', (total_width, 180), (0,0,0,0))
    
    current_x = 0
    for d in digits:
        combined_img.paste(d, (current_x, 0), d)
        current_x += d.size[0]
        
    return combined_img

# --- UI 介面 ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕰️ 機械翻板數字鐘")
st.caption("即時讀取 digits.png 素材並動態裁切顯示")

clock_placeholder = st.empty()

# 運行時鐘
while True:
    now = datetime.now().strftime("%H:%M:%S")
    try:
        img = create_clock_image(now, "digits.png")
        clock_placeholder.image(img)
    except Exception as e:
        st.error(f"找不到圖片或發生錯誤: {e}")
        break
    time.sleep(1)
