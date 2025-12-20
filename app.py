import streamlit as st
from streamlit_folium import st_folium
import folium
import json

class PhysicalFlipClock:
    """
    𓃥 白六物理遮蔽翻板模組
    功能：
    1. 點擊翻板區：循環切換預設城市。
    2. 照片左下角：點擊「隱形熱點」彈出全球地圖選單。
    3. 響應式佈局：自動適配手機螢幕寬度 (92vw)。
    """
    def __init__(self, api_key="", cities=None):
        self.api_key = api_key
        self.cities = cities or []
        if 'idx' not in st.session_state:
            st.session_state.idx = 0

    def _get_css(self, curr_img):
        return f"""
        <style>
            body {{ background: #0e1117; margin: 0; padding: 0; display: flex; justify-content: center; }}
            .app-container {{ width: 92vw; max-width: 500px; display: flex; flex-direction: column; gap: 8px; padding-top: 10px; }}
            
            /* 基礎卡片樣式 */
            .flip-card {{ 
                position: relative; background: #1a1a1a; border-radius: 8px; 
                font-weight: 900; color: #fff; overflow: hidden; 
            }}
            .row-flex {{ display: flex; justify-content: space-between; gap: 8px; }}
            .info-card {{ flex: 1; height: 18vw; max-height: 80px; font-size: 6.5vw; display: flex; align-items: center; justify-content: center; }}
            
            .time-row {{ display: flex; gap: 4px; align-items: center; justify-content: center; margin-top: 5px; }}
            .time-card {{ width: 20vw; height: 35vw; max-width: 110px; max-height: 180px; font-size: 26vw; }}
            
            /* 物理遮蔽核心 */
            .half {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
            .top {{ top: 0; border-bottom: 1px solid #000; align-items: flex-end; }}
            .bottom {{ bottom: 0; align-items: flex-start; }}
            .text-box {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; }}
            .top .text-box {{ bottom: -100%; }} .bottom .text-box {{ top: -100%; }}

            /* 照片與隱形熱點 */
            .photo-banner {{
                position: relative; width: 100%; height: 50vw; max-height: 280px;
                background: url('{curr_img}') center/cover; border-radius: 15px; margin-top: 10px; overflow: hidden;
            }}
            .glass-vignette {{
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                backdrop-filter: blur(8px); -webkit-mask-image: radial-gradient(circle, transparent 40%, black 100%);
                background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.4) 100%);
            }}
            .map-trigger {{
                position: absolute; bottom: 0; left: 0; width: 35%; height: 45%;
                cursor: pointer; z-index: 10;
            }}
            
            /* 隱藏 Streamlit 預設組件 */
            #MainMenu, footer {{visibility: hidden;}}
        </style>
        """

    @st.dialog("🌍 全球城市探索")
    def _show_map_dialog(self):
        st.write("點擊地圖圓點切換城市")
        m = folium.Map(location=[20, 0], zoom_start=1, tiles="CartoDB dark_matter", zoom_control=False)
        for i, c in enumerate(self.cities):
            folium.CircleMarker(
                location=[c.get("lat", 0), c.get("lon", 0)], 
                radius=10, color="#00d4ff", fill=True, popup=c["zh"]
            ).add_to(m)
        
        selected = st_folium(m, height=300, width=320, key="pop_map")
        if selected.get("last_object_clicked_popup"):
            name_zh = selected["last_object_clicked_popup"]
            new_idx = next((i for i, item in enumerate(self.cities) if item["zh"] == name_zh), None)
            if new_idx is not None:
                st.session_state.idx = new_idx
                st.rerun()

    def render(self):
        curr = self.cities[st.session_state.idx]
        
        # 1. 處理 JS 通訊：捕捉地圖熱點點擊
        from streamlit_js_eval import streamlit_js_eval
        js_signal = streamlit_js_eval(
            js_expressions="window.addEventListener('message', (e) => { if(e.data === 'open_map') return 'map'; })", 
            want_output=True, key="js_map"
        )
        if js_signal == 'map':
            self._show_map_dialog()

        # 2. 處理時鐘翻板點擊 (隱形按鈕觸發)
        if st.button("NEXT_HIDDEN", key="next_btn"):
            st.session_state.idx = (st.session_state.idx + 1) % len(self.cities)
            st.rerun()

        # 3. 渲染 HTML
        html_code = f"""
        {self._get_css(curr['img'])}
        <div class="app-container">
            <div onclick="window.parent.document.querySelector('button[kind=secondary]').click()">
                <div class="row-flex">
                    <div class="flip-card info-card">{curr['zh']}</div>
                    <div class="flip-card info-card">{curr.get('en', curr['zh'])}</div>
                </div>
                <div class="time-row">
                    <div class="flip-card time-card" id="h0"></div>
                    <div class="flip-card time-card" id="h1"></div>
                    <div style="font-size: 10vw; color: white; font-weight:bold;">:</div>
                    <div class="flip-card time-card" id="m0"></div>
                    <div class="flip-card time-card" id="m1"></div>
                </div>
            </div>
            
            <div class="photo-banner">
                <div class="glass-vignette"></div>
                <div class="map-trigger" onclick="window.parent.postMessage('open_map', '*')"></div>
            </div>
        </div>

        <script>
            function updateFlip(id, val) {{
                const el = document.getElementById(id);
                el.innerHTML = `<div class="half top"><div class="text-box">${{val}}</div></div>
                                <div class="half bottom"><div class="text-box">${{val}}</div></div>`;
            }}
            function tick() {{
                const now = new Date(new Date().toLocaleString("en-US", {{timeZone: "{curr['tz']}"}}));
                const h = String(now.getHours()).padStart(2, '0');
                const m = String(now.getMinutes()).padStart(2, '0');
                updateFlip('h0', h[0]); updateFlip('h1', h[1]);
                updateFlip('m0', m[0]); updateFlip('m1', m[1]);
            }}
            setInterval(tick, 1000); tick();
        </script>
        """
        
        # 隱藏用來觸發切換的實體按鈕
        st.markdown("<style>button[kind='secondary'] { display: none; }</style>", unsafe_allow_html=True)
        st.components.v1.html(html_code, height=650)

# --- 執行範例 ---
if __name__ == "__main__":
    MY_CITIES = [
        {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "lat": 25.03, "lon": 121.56, "img": "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_2700,h_1800/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/wgnjys095pdwp1qjvh6k/%E5%8F%B0%E5%8C%97%EF%BD%9C%E7%B6%93%E5%85%B8%E4%B8%80%E6%97%A5%E9%81%8A-Klook%E5%AE%A2%E8%B7%AF.jpg"},
        {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "lat": 51.50, "lon": -0.12, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1000&q=80"},
        {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "lat": 35.68, "lon": 139.69, "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1000&q=80"}
    ]
    
    clock = PhysicalFlipClock(cities=MY_CITIES)
    clock.render()
