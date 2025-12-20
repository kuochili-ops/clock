import streamlit as st

st.set_page_config(page_title="全球城市翻板鐘", layout="centered")

# 修正後的 HTML/CSS/JS 邏輯
flip_clock_html = """
<style>
    body { 
        background-color: #0e1117; 
        display: flex; flex-direction: column; align-items: center; 
        justify-content: center; min-height: 100vh; margin: 0; padding: 10px;
        overflow: hidden;
    }
    
    .container { display: flex; flex-direction: column; align-items: center; gap: 30px; width: 100%; }

    /* 城市翻板 - 寬度微調確保不重疊 */
    .city-row { display: flex; gap: 15px; width: 100%; justify-content: center; cursor: pointer; }
    .city-card {
        position: relative; width: 42vw; max-width: 160px; height: 70px;
        perspective: 1000px; text-align: center; color: #fff;
    }

    /* 時間翻板 - 阿拉伯數字置中強化 */
    .clock { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; align-items: center; }
    .flip-card {
        position: relative; width: 13vw; max-width: 60px; height: 18vw; max-height: 85px;
        font-weight: 800; color: #e0e0e0; text-align: center; perspective: 1000px;
    }

    /* 翻板基礎結構：使用 Flex 確保絕對置中 */
    .top, .bottom, .leaf-front, .leaf-back {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; border: 1px solid #111;
        display: flex; justify-content: center; box-sizing: border-box;
    }

    /* 頂部文字顯示下半部 */
    .top, .leaf-front { 
        top: 0; border-radius: 6px 6px 0 0; border-bottom: 0.5px solid #000;
        align-items: flex-start; /* 靠上對齊但透過 margin 移動文字中心 */
    }

    /* 底部文字顯示上半部 */
    .bottom, .leaf-back { 
        bottom: 0; border-radius: 0 0 6px 6px; border-top: 0.5px solid #000;
        align-items: flex-end;
    }

    /* 調整內容容器位置，解決影片中偏移的問題 */
    .content-wrapper {
        height: 200%; /* 兩倍高度 */
        display: flex; align-items: center; justify-content: center;
    }
    .top .content-wrapper { transform: translateY(0); }
    .bottom .content-wrapper { transform: translateY(-50%); }
    .leaf-front .content-wrapper { transform: translateY(0); }
    .leaf-back .content-wrapper { transform: translateY(-50%); }

    /* 城市文字大小 */
    .city-card .content-wrapper { font-size: 18px; letter-spacing: 2px; }
    /* 數字文字大小 */
    .flip-card .content-wrapper { font-size: 11vw; font-family: 'Courier New', monospace; }

    @media (min-width: 600px) {
        .flip-card { width: 70px; height: 100px; }
        .flip-card .content-wrapper { font-size: 65px; }
        .city-card { height: 80px; }
        .city-card .content-wrapper { font-size: 24px; }
    }

    .leaf {
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .leaf-back { transform: rotateX(-180deg); }
    .flipping .leaf { transform: rotateX(-180deg); }

    .label { font-size: 12px; color: #555; align-self: flex-end; padding-bottom: 5px; font-weight: bold; }
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

    function getFlipHTML(val) {
        return `<div class="content-wrapper">${val}</div>`;
    }

    function updateFlipCard(targetId, newVal, oldVal) {
        if (newVal === oldVal && document.getElementById(targetId).innerHTML !== "") return;
        const el = document.getElementById(targetId);
        
        el.innerHTML = `
            <div class="top">${getFlipHTML(newVal)}</div>
            <div class="bottom">${getFlipHTML(oldVal)}</div>
            <div class="leaf">
                <div class="leaf-front">${getFlipHTML(oldVal)}</div>
                <div class="leaf-back">${getFlipHTML(newVal)}</div>
            </div>
        `;
        el.classList.remove('flipping');
        void el.offsetWidth;
        el.classList.add('flipping');
    }

    function nextCity() {
        currentCityIdx = (currentCityIdx + 1) % cities.length;
        tick(true);
    }

    function tick(force = false) {
        const city = cities[currentCityIdx];
        const options = { timeZone: city.zone, hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
        const timeStrFull = new Intl.DateTimeFormat('en-GB', options).format(new Date());
        const parts = timeStrFull.split(':'); // [HH, MM, SS]
        
        if (document.getElementById('clock').innerHTML === "") {
            document.getElementById('clock').innerHTML = `
                <div class="unit-group"><div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div><div class="label">H</div></div>
                <div class="unit-group"><div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div><div class="label">M</div></div>
                <div class="unit-group"><div class="flip-card" id="d4"></div><div class="flip-card" id="d5"></div><div class="label">S</div></div>
            `;
        }

        updateFlipCard("city-cn", city.cn, prevCityNames.cn || city.cn);
        updateFlipCard("city-en", city.en, prevCityNames.en || city.en);
        prevCityNames = { cn: city.cn, en: city.en };

        const timeStr = parts.join("");
        const prevTimeStr = prevTime.join("");
        for (let i = 0; i < 6; i++) {
            if (force || timeStr[i] !== prevTimeStr[i]) {
                updateFlipCard(`d${i}`, timeStr[i], force ? timeStr[i] : (prevTimeStr[i] || timeStr[i]));
            }
        }
        prevTime = parts;
    }

    setInterval(tick, 1000);
    tick();
</script>
"""

st.title("🌏 全球翻板時鐘 (已修正顯示)")
st.components.v1.html(flip_clock_html, height=450)
