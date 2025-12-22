import streamlit as st
import json

# --- 1. 定義全域城市資料庫 (將變數移出函式，供外部存取) ---
MY_VIP_LIST = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "q": "Taipei", "lat": 25.03, "lon": 121.56, "vip": True, "img": "https://stage.taipei101mall.com.tw/uploads/content/4dd4930f-694c-5253-dd8f-ae903ea461a2.jpg"},
    {"zh": "高 雄", "en": "Kaohsiung", "tz": "Asia/Taipei", "q": "Kaohsiung", "lat": 22.62, "lon": 120.30, "vip": True, "img": "https://enews.tw/photo/original/linecontent/5573/b90cda6ef5fd5a8c1cf5dfeab92d7417.jpeg"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "q": "Tokyo", "lat": 35.68, "lon": 139.69, "vip": True, "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1200&q=80"},
    {"zh": "大 阪", "en": "Osaka", "tz": "Asia/Tokyo", "q": "Osaka", "lat": 34.69, "lon": 135.50, "vip": True, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnTJlEIfSmA6kP3ND4eh3rkhPLNgrBrYGOkj_k5EdsK-oUZACAsqDKUio3&s=10"},
    {"zh": "札 幌", "en": "Sapporo", "tz": "Asia/Tokyo", "q": "Sapporo", "lat": 43.06, "lon": 141.35, "vip": True, "img": "https://hokkaido-labo.com/wp-content/uploads/2014/09/140964647192343.jpg"},
    {"zh": "上 海", "en": "Shanghai", "tz": "Asia/Shanghai", "q": "Shanghai", "lat": 31.23, "lon": 121.47, "vip": True, "img": "https://imgb10.photophoto.cn/20160612/shanghaiwaitanjiejing-24089814_3.jpg"},
    {"zh": "羅 馬", "en": "Rome", "tz": "Europe/Rome", "q": "Rome", "lat": 41.90, "lon": 12.49, "vip": True, "img": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1200&q=80"},
    {"zh": "阿姆斯特丹", "en": "Amsterdam", "tz": "Europe/Amsterdam", "q": "Amsterdam", "lat": 52.36, "lon": 4.89, "vip": True, "img": "https://images.unsplash.com/photo-1512470876302-972faa2aa9a4?w=1200&q=80"},
    {"zh": "法蘭克福", "en": "Frankfurt", "tz": "Europe/Berlin", "q": "Frankfurt", "lat": 50.11, "lon": 8.68, "vip": True, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Skyline_Frankfurt_am_Main_2015.jpg/330px-Skyline_Frankfurt_am_Main_2015.jpg"},
    {"zh": "哥本哈根", "en": "Copenhagen", "tz": "Europe/Copenhagen", "q": "Copenhagen", "lat": 55.67, "lon": 12.56, "vip": True, "img": "https://images.unsplash.com/photo-1513622470522-26c3c8a854bc?w=1200&q=80"},
    {"zh": "紐 約", "en": "New York", "tz": "America/New_York", "q": "New York", "lat": 40.71, "lon": -74.00, "vip": True, "img": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1200&q=80"},
    {"zh": "舊金山", "en": "San Francisco", "tz": "America/Los_Angeles", "q": "San Francisco", "lat": 37.77, "lon": -122.41, "vip": True, "img": "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?w=1200&q=80"},
    {"zh": "洛杉磯", "en": "Los Angeles", "tz": "America/Los_Angeles", "q": "Los Angeles", "lat": 34.05, "lon": -118.24, "vip": True, "img": "https://images.unsplash.com/photo-1534190760961-74e8c1c5c3da?w=1200&q=80"},
    {"zh": "多倫多", "en": "Toronto", "tz": "America/Toronto", "q": "Toronto", "lat": 43.65, "lon": -79.38, "vip": True, "img": "https://images.unsplash.com/photo-1517090504586-fde19ea6066f?w=1200&q=80"},
]

GLOBAL_CITIES = [
    {"zh": "巴 黎", "en": "Paris", "tz": "Europe/Paris", "q": "Paris", "lat": 48.85, "lon": 2.35, "vip": False, "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200&q=80"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "q": "London", "lat": 51.50, "lon": -0.12, "vip": False, "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1200&q=80"},
    {"zh": "雪 梨", "en": "Sydney", "tz": "Australia/Sydney", "q": "Sydney", "lat": -33.86, "lon": 151.20, "vip": False, "img": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=1200&q=80"},
    {"zh": "首 爾", "en": "Seoul", "tz": "Asia/Seoul", "q": "Seoul", "lat": 37.56, "lon": 126.97, "vip": False, "img": "https://images.unsplash.com/photo-1538485399081-7191377e8241?w=1200&q=80"},
    {"zh": "杜 拜", "en": "Dubai", "tz": "Asia/Dubai", "q": "Dubai", "lat": 25.20, "lon": 55.27, "vip": False, "img": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200&q=80"},
    {"zh": "新加玻", "en": "Singapore", "tz": "Asia/Singapore", "q": "Singapore", "lat": 1.35, "lon": 103.81, "vip": False, "img": "https://images.unsplash.com/photo-1525625239513-997328132c68?w=1200&q=80"},
    {"zh": "曼 谷", "en": "Bangkok", "tz": "Asia/Bangkok", "q": "Bangkok", "lat": 13.75, "lon": 100.50, "vip": False, "img": "https://images.unsplash.com/photo-1508004526072-3be43a5005f6?w=1200&q=80"},
    {"zh": "柏 林", "en": "Berlin", "tz": "Europe/Berlin", "q": "Berlin", "lat": 52.52, "lon": 13.40, "vip": False, "img": "https://images.unsplash.com/photo-1560969184-10fe8719e047?w=1200&q=80"},
    {"zh": "馬德里", "en": "Madrid", "tz": "Europe/Madrid", "q": "Madrid", "lat": 40.41, "lon": -3.70, "vip": False, "img": "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=1200&q=80"},
    {"zh": "孟 買", "en": "Mumbai", "tz": "Asia/Kolkata", "q": "Mumbai", "lat": 19.07, "lon": 72.87, "vip": False, "img": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?w=1200&q=80"},
    {"zh": "墨西哥城", "en": "Mexico City", "tz": "America/Mexico_City", "q": "Mexico City", "lat": 19.43, "lon": -99.13, "vip": False, "img": "https://images.unsplash.com/photo-1585464231875-d9ef1f5ad396?w=1200&q=80"},
    {"zh": "維也納", "en": "Vienna", "tz": "Europe/Vienna", "q": "Vienna", "lat": 48.20, "lon": 16.37, "vip": False, "img": "https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=1200&q=80"},
    {"zh": "里斯本", "en": "Lisbon", "tz": "Europe/Lisbon", "q": "Lisbon", "lat": 38.72, "lon": -9.13, "vip": False, "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=1200&q=80"},
    {"zh": "開羅", "en": "Cairo", "tz": "Africa/Cairo", "q": "Cairo", "lat": 30.04, "lon": 31.23, "vip": False, "img": "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80"},
    {"zh": "香港", "en": "Hong Kong", "tz": "Asia/Hong_Kong", "q": "Hong Kong", "lat": 22.31, "lon": 114.16, "vip": False, "img": "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?w=1200&q=80"}
]

ALL_CITIES = MY_VIP_LIST + GLOBAL_CITIES

def render_flip_clock(api_key, target_idx=0):
    # --- 2. 轉換資料為 JSON 格式供 JavaScript 使用 ---
    city_json = json.dumps(ALL_CITIES)
    vip_json = json.dumps(MY_VIP_LIST)

    # ... (其餘 HTML/CSS/JS 代碼保持不變，與上個版本一致) ...
    html_code = f"""
    <div class="main-container">
        <div class="brand-text">𓃥 白 六 世 界 時 鐘</div>
        <div id="clock-board" class="clock-board">
            <div class="card-row">
                <div class="card info-card" id="czh"></div>
                <div class="card info-card" id="cen"></div>
            </div>
            <div class="card-row">
                <div class="card time-card" id="h0"></div>
                <div class="card time-card" id="h1"></div>
                <div class="separator">:</div>
                <div class="card time-card" id="m0"></div>
                <div class="card time-card" id="m1"></div>
            </div>
            <div class="card-row">
                <div class="card info-card weather-card" id="w_desc"></div>
                <div class="card info-card weather-card" id="w_temp"></div>
            </div>
        </div>
        <div id="city-banner" class="city-banner">
            <div class="vignette"></div>
            <div id="map-target" class="map-overlay-btn"></div>
        </div>
    </div>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ background: #0e1117; margin: 0; display: flex; justify-content: center; font-family: "Impact", sans-serif; color: white; overflow: hidden; }}
        .main-container {{ width: 440px; display: flex; flex-direction: column; align-items: center; padding: 20px 0; gap: 15px; }}
        .brand-text {{ color: #555; font-size: 13px; letter-spacing: 6px; font-weight: bold; }}
        .clock-board {{ width: 100%; display: flex; flex-direction: column; gap: 12px; cursor: pointer; }}
        .card-row {{ display: flex; width: 100%; gap: 10px; justify-content: center; align-items: center; }}
        .card {{ background: #1a1a1a; border-radius: 8px; position: relative; overflow: hidden; perspective: 1000px; }}
        .info-card {{ flex: 1; height: 75px; font-size: 32px; display: flex; align-items: center; justify-content: center; text-align: center; }}
        .weather-card {{ background: #141414; color: #888; font-size: 22px; font-family: sans-serif; height: 55px; }}
        .time-card {{ width: 90px; height: 135px; font-size: 105px; }}
        .separator {{ font-size: 45px; color: white; width: 20px; text-align: center; animation: blink 1s infinite; }}
        @keyframes blink {{ 50% {{ opacity: 0.3; }} }}
        .panel {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; }}
        .top-p {{ top: 0; border-bottom: 1px solid rgba(0,0,0,0.5); align-items: flex-end; border-radius: 8px 8px 0 0; }}
        .bottom-p {{ bottom: 0; align-items: flex-start; border-radius: 0 0 8px 8px; }}
        .text-node {{ position: absolute; width: 100%; height: 200%; display: flex; align-items: center; justify-content: center; line-height: 0; }}
        .top-p .text-node {{ bottom: -100%; }} .bottom-p .text-node {{ top: -100%; }}
        .leaf-node {{ position: absolute; top: 0; left: 0; width: 100%; height: 50%; z-index: 10; transform-origin: bottom; transition: transform 0.4s ease-in; transform-style: preserve-3d; }}
        .leaf-side {{ position: absolute; inset: 0; backface-visibility: hidden; background: #1a1a1a; display: flex; justify-content: center; overflow: hidden; }}
        .side-back {{ transform: rotateX(-180deg); }}
        .flipping .leaf-node {{ transform: rotateX(-180deg); }}
        .city-banner {{ width: 100%; height: 210px; border-radius: 12px; background-size: cover; background-position: center; transition: 1s; position: relative; }}
        .vignette {{ position: absolute; inset: 0; background: radial-gradient(circle, transparent 30%, rgba(0,0,0,0.8) 100%); }}
        .map-overlay-btn {{ position: absolute; bottom: 0; left: 0; width: 60px; height: 60px; cursor: pointer; z-index: 50; }}
    </style>
    <script>
        const allCities = {city_json};
        const vipCities = {vip_json};
        const API_KEY = "{api_key}";
        let curIdx = {target_idx};
        let memory = {{'h0':null,'h1':null,'m0':null,'m1':null,'czh':null,'cen':null,'w_desc':null,'w_temp':null}};
        let isBusy = {{}};
        function performFlip(id, nextVal, prevVal) {{
            const el = document.getElementById(id);
            if(!el) return;
            el.innerHTML = ""; el.classList.remove('flipping');
            const n = String(nextVal || " "), p = String(prevVal || " ");
            el.innerHTML = `<div class="panel top-p"><div class="text-node">${{n}}</div></div><div class="panel bottom-p"><div class="text-node">${{p}}</div></div><div class="leaf-node"><div class="leaf-side top-p"><div class="text-node">${{p}}</div></div><div class="leaf-side side-back bottom-p"><div class="text-node">${{n}}</div></div></div>`;
            requestAnimationFrame(() => {{ void el.offsetWidth; requestAnimationFrame(() => el.classList.add('flipping')); }});
        }}
        async function smartUpdate(id, target) {{
            const tStr = String(target);
            if (memory[id] === tStr || isBusy[id]) return;
            isBusy[id] = true;
            const oldStr = memory[id];
            if (oldStr === null) {{ performFlip(id, tStr, tStr); }}
            else if (!isNaN(tStr) && tStr.length === 1 && !isNaN(oldStr)) {{
                let curN = parseInt(oldStr), tarN = parseInt(tStr);
                while (curN !== tarN) {{ let prev = String(curN); curN = (curN + 1) % 10; performFlip(id, String(curN), prev); await new Promise(r => setTimeout(r, 400)); }}
            }} else {{ performFlip(id, tStr, oldStr); }}
            memory[id] = tStr; isBusy[id] = false;
        }}
        async function updateWeather() {{
            const c = allCities[curIdx];
            try {{
                const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${{c.q}}&appid=${{API_KEY}}&units=metric`);
                const data = await res.json();
                smartUpdate('w_desc', data.weather[0].main);
                smartUpdate('w_temp', Math.round(data.main.temp_min) + "~" + Math.round(data.main.temp_max) + "°C");
            }} catch(e) {{ smartUpdate('w_desc', 'Error'); }}
        }}
        function refreshClock() {{
            const c = allCities[curIdx];
            document.getElementById('city-banner').style.backgroundImage = "url('" + c.img + "')";
            const now = new Date();
            const timeStr = now.toLocaleTimeString('en-GB', {{ timeZone: c.tz, hour12: false, hour: '2-digit', minute: '2-digit' }});
            const [hh, mm] = timeStr.split(':');
            smartUpdate('czh', c.zh); smartUpdate('cen', c.en);
            smartUpdate('h0', hh[0]); smartUpdate('h1', hh[1]);
            smartUpdate('m0', mm[0]); smartUpdate('m1', mm[1]);
        }}
        document.getElementById('clock-board').onclick = () => {{
            const current = allCities[curIdx];
            let vIdx = vipCities.findIndex(v => v.zh === current.zh);
            vIdx = (vIdx + 1) % vipCities.length;
            curIdx = allCities.findIndex(a => a.zh === vipCities[vIdx].zh);
            refreshClock(); updateWeather();
        }};
        document.getElementById('map-target').onclick = (e) => {{
            e.stopPropagation();
            const btn = window.parent.document.querySelector('button[kind=secondary]');
            if(btn) btn.click();
        }};
        setInterval(refreshClock, 1000); setInterval(updateWeather, 600000);
        refreshClock(); updateWeather();
    </script>
    """
    st.components.v1.html(html_code, height=720)
