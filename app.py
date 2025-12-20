import streamlit as st
from streamlit_folium import st_folium
import folium

# --- 1. 初始化資料 (延用之前的清單) ---
API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"
DEFAULT_CITIES = [
    {"name": "Taipei", "zh": "臺 北", "tz": "Asia/Taipei", "lat": 25.0330, "lon": 121.5654, "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
    {"name": "Los Angeles", "zh": "洛杉磯", "tz": "America/Los_Angeles", "lat": 34.0522, "lon": -118.2437, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/HollywoodSign.jpg/1280px-HollywoodSign.jpg"},
    {"name": "London", "zh": "倫 敦", "tz": "Europe/London", "lat": 51.5074, "lon": -0.1278, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"},
    {"name": "Tokyo", "zh": "東 京", "tz": "Asia/Tokyo", "lat": 35.6895, "lon": 139.6917, "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1000&q=80"},
    {"name": "Paris", "zh": "巴 黎", "tz": "Europe/Paris", "lat": 48.8566, "lon": 2.3522, "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1000&q=80"}
]

if 'current_city' not in st.session_state:
    st.session_state.current_city = DEFAULT_CITIES[0]

# --- 2. 跳出式地圖函數 ---
@st.dialog("🌍 選擇探索城市")
def show_map_dialog():
    st.write("點擊藍色圓點切換城市，地圖支援左右滑動探索。")
    # 地圖寬度與高度調整為適合對話框
    m = folium.Map(
        location=[20, 0], zoom_start=1, 
        tiles="CartoDB dark_matter", 
        zoom_control=False
    )
    for c in DEFAULT_CITIES:
        folium.CircleMarker(
            location=[c["lat"], c["lon"]],
            radius=8, color="#00d4ff", fill=True, popup=c["name"]
        ).add_to(m)
    
    map_data = st_folium(m, height=300, width=400, key="modal_map")
    
    if map_data.get("last_object_clicked_popup"):
        city_name = map_data["last_object_clicked_popup"]
        new_city = next((item for item in DEFAULT_CITIES if item["name"] == city_name), None)
        if new_city:
            st.session_state.current_city = new_city
            st.rerun() # 選完後自動重新整理並收起地圖

# --- 3. 介面佈局 ---
st.markdown("<h2 style='text-align: center; color: #444;'>𓃥 白 六 世 界 時 鐘</h2>", unsafe_allow_html=True)

# 渲染翻板時鐘區塊 (延用之前的時鐘邏輯)
# ... (這裡放 clock_section 程式碼)

# --- 4. 關鍵：點擊觸發區 ---
col_map, col_empty = st.columns([1, 5])
with col_map:
    # 我們在地圖左下方放一個透明或精緻的按鈕
    if st.button("🗺️ 探索"):
        show_map_dialog()

# 照片區塊 (保留邊際霧化效果)
st.markdown(f"""
    <div style="position: relative; width: 100%; height: 260px; border-radius: 12px; 
                background: url('{st.session_state.current_city['img']}') center/cover; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                    backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%);
                    background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.4) 100%);">
        </div>
        <div style="position: absolute; bottom: 10px; left: 10px; color: rgba(255,255,255,0.5); font-size: 0.8rem;">
            按上方 [探索] 開啟地圖
        </div>
    </div>
""", unsafe_allow_html=True)
