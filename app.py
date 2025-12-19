import streamlit as st

st.set_page_config(page_title="全球城市翻板鐘", layout="centered")

# 定義 HTML/CSS/JS 邏輯
flip_clock_html = """
<style>
    body { 
        background-color: #0e1117; 
        display: flex; flex-direction: column; align-items: center; 
        justify-content: center; min-height: 100vh; margin: 0; padding: 10px;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    
    .container { display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%; }

    /* 城市翻板樣式 - 較寬 */
    .city-row { display: flex; gap: 10px; width: 100%; justify-content: center; cursor: pointer; }
    .city-card {
        position: relative; width: 45%; max-width: 180px; height: 80px;
        perspective: 1000px; text-align: center; color: #fff;
    }

    /* 時間翻板樣式 - 阿拉伯數字 */
    .clock { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; align-items: center; }
    .flip-card {
        position: relative; width: 14vw; max-width: 60px; height: 20vw; max-height: 90px;
        font-size: 12vw; font-weight: 700; color: #e0e0e0; text-align: center;
    }
    @media (min-width: 600px) {
        .flip-card { width: 80px; height: 110px; font-size: 70px; }
        .city-card { height: 100px; }
    }

    /* 通用翻板結構 */
    .top, .bottom, .leaf-front, .leaf-back {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; border: 1px solid #111; box-sizing: border-box;
    }
    .top, .leaf-front { 
        top: 0; border-radius: 6px 6px 0 0; border-bottom: 0.5px solid #000;
        display: flex; align-items: flex-end; justify-content: center;
    }
    .bottom, .leaf-back { 
        bottom: 0; border-radius: 0 0 6px 6px; border-top: 0.5px solid #000;
        display: flex; align-items: flex-start; justify-content: center;
    }
    
    /* 文字垂直置中修正 */
    .city-card .top, .city-card .leaf-front { line-height: 80px; font-size: 20px; padding-bottom: 0; align-items: center; }
    .city-card .bottom, .city-card .leaf-back { line-height: 0px; font-size: 20px; padding-top: 0; align-items: center; }
    .flip-card .top, .flip-card .leaf-front { line-height: 20vw; }
    @media (min-width: 600px) { .flip-card .top, .flip-card .leaf-front { line-height: 110px; } }

    .leaf {
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.5s ease-in;
    }
    .leaf-back { transform: rotateX(-180deg); }
    .flipping .leaf { transform: rotateX(-180deg); }

    .label { font-size: 14px; color: #666; align-self: flex-end; padding-bottom: 5px; }
    .unit-group { display: flex; gap: 4px; align-items: center; }
</style>

<div class="container">
    <div class="city-row" onclick="nextCity()">
        <div class="city-card" id="city-cn"></div>
        <div class="city-card" id="city-en"></div>
    </div>

    <div class="clock" id="clock"></div>
</div>

<script>
    const cities = [
        { cn: "臺 北", en: "Taipei", zone: "Asia/Taipei" },
        { cn: "東 京", en: "Tokyo", zone: "Asia/Tokyo" },
        { cn: "倫 敦", en: "London", zone: "Europe/London" },
        { cn: "紐 約", en: "New York", zone: "America/New_York" },
        { cn: "洛 杉 磯", en: "Los Angeles", zone: "America/Los_Angeles" }
    ];

    let currentCityIdx = 0;
    let prevTime = ["", "", ""];
    let prevCityNames = { cn: "", en: "" };

    function createFlipContent(targetId, newVal, oldVal, isCity = false) {
        if (newVal === oldVal) return;
        const el = document.getElementById(targetId);
        el.innerHTML = `
            <div class="top"><div>${newVal}</div></div>
            <div class="bottom"><div>${oldVal}</div></div>
            <div class="leaf">
                <div class="leaf-front"><div>${oldVal}</div></div>
                <div class="leaf-back"><div>${newVal}</div></div>
            </div>
        `;
        el.classList.remove('flipping');
        void el.offsetWidth;
        el.classList.add('flipping');
    }

    function nextCity() {
        currentCityIdx = (currentCityIdx + 1) % cities.length;
        tick(true); // 強制更新
    }

    function tick(force = false) {
        const city = cities[currentCityIdx];
        
        // 取得該城市目前時間
        const now = new Date(new Intl.DateTimeFormat('en-US', {
            timeZone: city.zone, hour12: false, 
            hour: '2-digit', minute: '2-digit', second: '2-digit'
        }).format(new Date()));

        const h = now.getHours().toString().padStart(2, '0');
        const m = now.getMinutes().toString().padStart(2, '0');
        const s = now.getSeconds().toString().padStart(2, '0');

        // 初始化時間結構
        if (document.getElementById('clock').innerHTML === "") {
            document.getElementById('clock').innerHTML = `
                <div class="unit-group"><div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div><div class="label">H</div></div>
                <div class="unit-group"><div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div><div class="label">M</div></div>
                <div class="unit-group"><div class="flip-card" id="d4"></div><div class="flip-card" id="d5"></div><div class="label">S</div></div>
            `;
        }

        // 更新城市翻板
        createFlipContent("city-cn", city.cn, prevCityNames.cn, true);
        createFlipContent("city-en", city.en, prevCityNames.en, true);
        prevCityNames = { cn: city.cn, en: city.en };

        // 更新時間數字 (0-9)
        const timeStr = h + m + s;
        const prevTimeStr = prevTime.join("");
        for (let i = 0; i < 6; i++) {
            if (force || timeStr[i] !== prevTimeStr[i]) {
                createFlipContent(`d${i}`, timeStr[i], force ? timeStr[i] : prevTimeStr[i]);
            }
        }
        prevTime = [h, m, s];
    }

    setInterval(tick, 1000);
    tick();
</script>
"""

st.title("🌏 全球城市翻板時鐘")
st.write("點擊「城市翻板」可切換不同時區。")

# 調整元件高度以適應城市+時間
st.components.v1.html(flip_clock_html, height=400)
