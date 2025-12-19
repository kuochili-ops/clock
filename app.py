import streamlit as st
from PIL import Image
import time
from datetime import datetime

# 設定網頁標題
st.set_page_config(page_title="Flip Clock App", layout="centered")

def get_digit(digit_char, sprite_sheet):
    """
    從圖片中根據數字字元裁切對應的區塊
    """
    try:
        n = int(digit_char)
    except ValueError:
        return None
        
    w, h = sprite_sheet.size
    unit_w = w / 5
    unit_h = h / 2
    
    row = n // 5
    col = n % 5
    
    left = col * unit_w
    top = row * unit_h
    right = left + unit_w
    bottom = top + unit_h
    
    return sprite_sheet.crop((left, top, right, bottom))

def create_clock_image(time_str, sprite_path):
    """
    將時間字串(如 12:30:45) 轉換為拼接後的圖片
    """
    sprite_sheet = Image.open(sprite_path)
    digits = []
    
    for char in time_str:
        if char == ":":
            # 建立一個簡單的冒號分隔塊
            colon = Image.new('RGBA', (20, int(sprite_sheet.size[1]/2)), (0,0,0,0))
            digits.append(colon)
        else:
            digit_img = get_digit(char, sprite_sheet)
            if digit_img:
                digits.append(digit_img)
    
    # 水平拼接
    total_width = sum(d.size[0] for d in digits)
    max_height = max(d.size[1] for d in digits)
    
    combined_img = Image.new('RGBA', (int(total_width), int(max_height)))
    current_x = 0
    for d in digits:
        combined_img.paste(d, (current_x, 0))
        current_x += d.size[0]
        
    return combined_img

# --- Streamlit UI ---
st.title("🕰️ 機械翻板數字鐘")
st.write("利用上傳的素材圖動態生成的即時時鐘")

# 建立預留空間以便每秒刷新
clock_placeholder = st.empty()

while True:
    # 獲取現在時間 HH:MM:SS
    now = datetime.now().strftime("%H:%M:%S")
    
    # 產生圖片
    img = create_clock_image(now, "digits.png")
    
    # 顯示圖片
    clock_placeholder.image(img, use_container_width=True)
    
    # 每秒更新一次
    time.sleep(1)
