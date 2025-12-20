import streamlit as st
from flip_clock_lib import st_flip_clock

# 設定頁面配置
st.set_page_config(
    page_title="全球城市翻板鐘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 顯示標題與說明
st.title("🌏 全球城市翻板鐘")
st.markdown("""
此版本已優化：
* **杜絕殘影**：採用響應式 `vw` 鎖定佈局，解決文字漏出問題。
* **縮小縫隙**：將轉軸縫隙減至最小 1px。
* **時區連動**：修正手機端切換時區失效的問題，點擊城市即可切換。
""")

# 呼叫封裝好的翻板鐘模組
st_flip_clock()

# 頁尾補充說明
st.info("💡 提示：點擊上方的「城市名稱」區塊，即可切換不同城市的時間。")
