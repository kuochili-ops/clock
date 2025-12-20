import streamlit as st
from flip_clock_lib import st_flip_clock

st.title("🕰️ 全球機械翻板鐘")
st.write("這是封裝後的模組，支援手機直式瀏覽與時區切換。")

# 直接呼叫模組函數
st_flip_clock()

st.info("提示：點擊上方城市名稱即可切換時區。")
