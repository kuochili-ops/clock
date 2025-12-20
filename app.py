import streamlit as st
from streamlit_folium import st_folium
import folium

class PhysicalFlipClock:
    """
    𓃥 白六物理遮蔽翻板模組
    功能：恢復極致大字、上下切割的物理翻轉視覺。
    操作：點擊上半部切換城市，點擊照片左下角彈出地圖。
    """
    def __init__(self, api_key="", cities=None):
        self.api_key = api_key
        self.cities = cities or []
        if 'idx' not in st.session_state:
            st.session_state.idx = 0

    def _get_css(self, curr_img):
        # 這裡精確還原您影片中「切割感」的 CSS
        return f"""
        <style>
            .app-container {{ width: 92vw; max-width: 500px; display: flex; flex-direction: column; gap: 8px; }}
            .flip-card {{ position: relative; background: #1a1a1a; border-radius: 8px; color: white; font-weight: 900; overflow: hidden; }}
            .info-card {{ flex: 1; height: 18vw; font-size: 6.5vw; display: flex; align-items: center; justify-content: center; }}
            .time-row {{ display: flex; gap: 4px; align-items: center; justify-content: center; margin-top: 10px; }}
            .time-card {{ width: 21vw; height: 35vw; position: relative; }}

            /* 物理遮蔽關鍵：上下半部與文字位移 */
            .half {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
            .top {{ top: 0; border-bottom: 1px solid #000; align-items: flex-end; }}
            .bottom {{ bottom: 0; align-items: flex-start; }}
            .text-box {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; font-size: 26vw; }}
            .top .text-box {{ bottom: -100%; }}
            .bottom .text-box {{ top: -100%; }}

            .photo-banner {{ 
                width: 100%; height: 50vw; border-radius: 15px; margin-top: 10px;
                background: url('{curr_img}') center/cover; position: relative; overflow: hidden; 
            }}
            .glass {{ position: absolute; width: 100%; height: 100%; backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%); }}
            .map-hotspot {{ position: absolute; bottom: 0; left: 0; width: 40%; height: 50%; cursor: pointer; z-index: 100; }}
            
            /* 隱藏 Streamlit 的 Button 介面 */
            .stButton {{ display: none; }}
        </style>
        """

    @st.dialog("🌍 全球探索")
    def _show_map_dialog(self):
        m = folium.Map(location=[20, 0], zoom_start=1, tiles="CartoDB dark_matter", zoom_control=False)
        for c in self.cities:
            folium.CircleMarker(location=[c["lat"], c["lon"]], radius=10, color="#00d4ff", fill=True, popup=c["zh"]).add_to(m)
        selected = st_folium(m, height=300, width=320, key="pop_map")
        if selected.get("last_object_clicked_popup"):
            name_zh = selected["last_object_clicked_popup"]
            new_idx = next((i for i, item in enumerate(self.cities) if item["zh"] == name_zh), None)
            if new_idx is not None:
                st.session_state.idx = new_idx
                st.rerun()

    def render(self):
        curr = self.cities[st.session_state.idx]
        
        # 隱藏按鈕：[0] 是換城市, [1] 是開地圖
        if st.button("NEXT", key="n"):
            st.session_state.idx = (st.session_state.idx + 1) % len(self.cities)
            st.rerun()
        if st.button("MAP", key="m"):
            self._show_map_dialog()

        html_code = f"""
        <div class="app-container">
            {self._get_css(curr['img'])}
            <div onclick="window.parent.document.querySelectorAll('button[kind=secondary]')[0].click()">
                <div style="display: flex; gap: 8px;">
                    <div class="flip-card info-card">{curr['zh']}</div>
                    <div class="flip-card info-card">{curr['en']}</div>
                </div>
                <div class="time-row">
                    <div class="time-card" id="h0"></div>
                    <div class="time-card" id="h1"></div>
                    <div style="font-size: 10vw; color: white;">:</div>
                    <div class="time-card" id="m0"></div>
                    <div class="time-card" id="m1"></div>
                </div>
            </div>
            <div class="photo-banner">
                <div class="glass"></div>
                <div class="map-hotspot" onclick="window.parent.document.querySelectorAll('button[kind=secondary]')[1].click(); event.stopPropagation();"></div>
            </div>
        </div>
        <script>
            function setVal(id, val) {{
                document.getElementById(id).innerHTML = `
                    <div class="half top"><div class="text-box">${{val}}</div></div>
                    <div class="half bottom"><div class="text-box">${{val}}</div></div>`;
            }}
            function tick() {{
                const now = new Date(new Date().toLocaleString("en-US", {{timeZone: "{curr['tz']}"}}));
                const h = String(now.getHours()).padStart(2, '0');
                const m = String(now.getMinutes()).padStart(2, '0');
                setVal('h0', h[0]); setVal('h1', h[1]); setVal('m0', m[0]); setVal('m1', m[1]);
            }}
            setInterval(tick, 1000); tick();
        </script>
        """
        st.components.v1.html(html_code, height=650)

# --- 執行區 ---
if __name__ == "__main__":
    MY_CITIES = [
        {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "lat": 25.03, "lon": 121.56, "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
        {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "lat": 51.50, "lon": -0.12, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"},
        {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "lat": 35.68, "lon": 139.69, "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1000&q=80"}
    ]
    clock = PhysicalFlipClock(cities=MY_CITIES)
    clock.render()
