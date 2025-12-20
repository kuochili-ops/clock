import streamlit as st
import requests

st.set_page_config(page_title="𓃥白六世界時鐘", layout="centered")

# 城市資料與 OpenWeather 搜尋關鍵字
API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"
CITIES = [
    {"zh": "臺 北", "en": "Taipei", "tz": "Asia/Taipei", "q": "Taipei"},
    {"zh": "高 雄", "en": "Kaohsiung", "tz": "Asia/Taipei", "q": "Kaohsiung"},
    {"zh": "東 京", "en": "Tokyo", "tz": "Asia/Tokyo", "q": "Tokyo"},
    {"zh": "倫 敦", "en": "London", "tz": "Europe/London", "q": "London"},
    {"zh": "紐 約", "en": "New York", "tz": "America/New_York", "q": "New York"},
    {"zh": "洛 杉 磯", "en": "Los Angeles", "tz": "America/Los_Angeles", "q": "Los Angeles"},
    {"zh": "巴 黎", "en": "Paris", "tz": "Europe/Paris", "q": "Paris"}
]

# 天氣中文化對照表
WEATHER_DESC = {
    "clear sky": "天 氣 晴", "few clouds": "多 雲 晴", "scattered clouds": "多 雲",
    "broken clouds": "多 雲 陰", "overcast clouds": "陰 天", "light rain": "微 雨",
    "moderate rain": "有 雨", "heavy intensity rain": "大 雨", "thunderstorm": "雷 雨",
    "snow": "下 雪", "mist": "薄 霧"
}

flip_clock_html = f"""
<style>
    body {{ 
        background-color: #0e1117; margin: 0; 
        display: flex; justify-content: center; align-items: flex-start; 
        min-height: 100vh; font-family: "Microsoft JhengHei", "PingFang TC", sans-serif;
        padding-top: 3vh;
    }}
    
    .app-container {{ display: flex; flex-direction: column; align-items: center; gap: 15px; width: 98vw; max-width: 600px; }}
    .app-title {{ color: #444; font-size: 0.8rem; letter-spacing: 6px; font-weight: bold; margin-bottom: 5px; }}
    
    .flip-card {{ position: relative; background: #1a1a1a; border-radius: 6px; font-weight: 900; perspective: 1000px; color: #fff; overflow: hidden; }}
    
    /* 統一分散對齊佈局 */
    .row-flex {{ display: flex; justify-content: space-between; width: 100%; gap: 10px; }}
    
    /* 城市與天氣板：字體盡量放大 */
    .info-card {{ 
        flex: 1; height: 95px; 
        font-size: clamp(1.5rem, 6vw, 2.4rem); /* 字體極大化 */
        cursor: pointer; 
    }}

    /* 時間板：加高且極大字 */
    .time-row {{ display: flex; gap: 5px; align-items: center; justify-content: center; width: 100%; }}
    .time-card {{ 
        width: 22vw; max-width: 130px; 
        height: 42vw; max-height: 200px; 
        font-size: clamp(5rem, 30vw, 170px); 
    }}
    .colon {{ color: #333; font-size: 4rem; font-weight: bold; margin-bottom: 10px; }}

    /* --- 物理遮蔽核心 --- */
    .half {{
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #1a1a1a; display: flex; justify-content: center;
    }}
    .top {{ top: 0; border-radius: 6px 6px 0 0; align-items: flex-end; border-bottom: 1px solid rgba(0,0,0,0.7); }}
    .bottom {{ bottom: 0; border-radius: 0 0 6px 6px; align-items: flex-start; }}

    .text-box {{
        position: absolute; width: 100%; height: 200%;
        display: flex; align-items: center; justify-content: center;
        text-align: center; white-space: nowrap;
    }}
    .top .text-box {{ bottom: -100%; }}
    .bottom .text-box {{ top: -100%; }}

    .leaf {{
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .leaf-front, .leaf-back {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; backface-visibility: hidden; }}
    .leaf-back {{ transform: rotateX(-180deg); }}
    .flipping .leaf {{ transform: rotateX(-180deg); }}
    .hinge {{ position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background: #000; z-index: 20; }}
</style>

<div class="app-container">
    <div class="app-title">𓃥 白 六 世 界 時 鐘</div>

    <div class="row-flex" onclick="nextCity()">
        <div class="flip-card info-card" id="czh"></div>
        <div class="flip-card info-card" id="cen"></div>
    </div>

    <div class="time-row">
        <div class="flip-card time-card" id="h0"></div>
        <div class="flip-card time-card" id="h1"></div>
        <div class="colon">:</div>
        <div class="flip-card time-card" id="m0"></div>
        <div class="flip-card time-card" id="m1"></div>
    </div>

    <div class="row-flex">
        <div class="flip-card info-card" id="w_status" style="background: #121212; color: #ddd;"></div>
        <div class="flip-card info-card" id="w_temp" style="background: #121212; color: #ccc;"></div>
    </div>
</div>

<script>
    const cities = {CITIES};
    const apiKey = "{API_KEY}";
    const weatherMap = {WEATHER_DESC};
    let curIdx = 0;
    let pT = ["", ""];
    let pC = {{zh: "", en: ""}};
    let pW = {{status: "加載中", temp: "--~--°C"}};

    function updateFlip(id, newVal, oldVal) {{
        const el = document.getElementById(id);
        if (newVal === oldVal && el.innerHTML !== "") return;
        el.innerHTML = `
            <div class="half top"><div class="text-box">${{newVal}}</div></div>
            <div class="half bottom"><div class="text-box">${{oldVal || newVal}}</div></div>
            <div class="leaf">
                <div class="leaf-front half top"><div class="text-box">${{oldVal || newVal}}</div></div>
                <div class="leaf-back half bottom"><div class="text-box">${{newVal}}</div></div>
            </div>
            <div class="hinge"></div>
        `;
        el.classList.remove('flipping');
        void el.offsetWidth;
        el.classList.add('flipping');
    }}

    async function fetchWeather(cityQ) {{
        try {{
            const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${{cityQ}}&appid=${{apiKey}}&units=metric&lang=zh_tw`);
            const data = await res.json();
            const desc = weatherMap[data.weather[0].description] || data.weather[0].description;
            const temp = Math.round(data.main.temp_min) + "~" + Math.round(data.main.temp_max) + "°C";
            return {{ status: desc, temp: temp }};
        }} catch (e) {{
            return {{ status: "連線失敗", temp: "誤差中" }};
        }}
    }}

    async function nextCity() {{
        curIdx = (curIdx + 1) % cities.length;
        const newWeather = await fetchWeather(cities[curIdx].q);
        updateFlip('w_status', newWeather.status, pW.status);
        updateFlip('w_temp', newWeather.temp, pW.temp);
        pW = newWeather;
        tick();
    }}

    function tick() {{
        const c = cities[curIdx];
        const now = new Date();
        const f = new Intl.DateTimeFormat('en-US', {{
            timeZone: c.tz, hour12: false, hour: '2-digit', minute: '2-digit'
        }});
        const parts = f.formatToParts(now);
        const h = parts.find(p => p.type === 'hour').value;
        const m = parts.find(p => p.type === 'minute').value;

        updateFlip('czh', c.zh, pC.zh);
        updateFlip('cen', c.en, pC.en);
        updateFlip('h0', h[0], pT[0] ? pT[0][0] : "");
        updateFlip('h1', h[1], pT[0] ? pT[0][1] : "");
        updateFlip('m0', m[0], pT[1] ? pT[1][0] : "");
        updateFlip('m1', m[1], pT[1] ? pT[1][1] : "");

        pT = [h, m]; pC = {{zh: c.zh, en: c.en}};
    }}

    // 初始化天氣
    fetchWeather(cities[0].q).then(w => {{
        updateFlip('w_status', w.status, "");
        updateFlip('w_temp', w.temp, "");
        pW = w;
    }});

    setInterval(tick, 1000);
    tick();
</script>
"""

st.components.v1.html(flip_clock_html, height=800)
