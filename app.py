import streamlit as st

st.set_page_config(page_title="全球城市翻板鐘", layout="centered")

flip_clock_final = """
<style>
    body { 
        background-color: #0e1117; 
        display: flex; flex-direction: column; align-items: center; 
        justify-content: center; min-height: 100vh; margin: 0; padding: 20px;
        font-family: 'Courier New', Courier, monospace;
    }
    
    .container { display: flex; flex-direction: column; align-items: center; gap: 30px; width: 100%; }

    .city-row { display: flex; gap: 10px; width: 100%; justify-content: center; cursor: pointer; }
    .city-card {
        position: relative; width: 44vw; max-width: 170px; height: 70px;
        perspective: 1000px; color: #fff;
    }

    .clock { display: flex; gap: 6px; flex-wrap: wrap; justify-content: center; align-items: center; }
    .flip-card {
        position: relative; width: 13vw; max-width: 60px; height: 20vw; max-height: 90px;
        font-weight: 900; color: #f0f0f0; perspective: 1000px;
    }

    .top, .bottom, .leaf-front, .leaf-back {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #1a1a1a;
        display: flex; justify-content: center; align-items: center;
        box-sizing: border-box; border: 1px solid #000;
    }

    .top, .leaf-front { top: 0; border-radius: 6px 6px 0 0; align-items: flex-end; }
    .bottom, .leaf-back { bottom: 0; border-radius: 0 0 6px 6px; align-items: flex-start; }

    .text-box {
        height: 200%; 
        display: flex; align-items: center;
        line-height: 1;
    }
    
    .top .text-box, .leaf-front .text-box { transform: translateY(50%); }
    .bottom .text-box, .leaf-back .text-box { transform: translateY(-50%); }

    .city-card .text-box { font-size: 20px; font-family: "Microsoft JhengHei", sans-serif; }
    .flip-card .text-box { font-size: 14vw; }
    
    @media (min-width: 600px) {
        .flip-card .text-box { font-size: 75px; }
        .city-card .text-box { font-size: 26px; }
    }

    .leaf {
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .leaf-back { transform: rotateX(-180deg); }
    .flipping .leaf { transform: rotateX(-180deg); }

    .hinge {
        position: absolute; top: 50%; left: 0; width: 100%; height: 1px;
        background: rgba(0,0,0,0.6); z-index: 20; transform: translateY(-50%);
    }

    .label { font-size: 12px; color: #444; align-self: flex-end; padding-bottom: 5px; }
    .unit-group { display: flex; gap: 2px; align-items: center; }
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
    let prevTimeStr = ""; 
    let prevCity = { cn: "", en: "" };

    function createCardHTML(val) {
        return `<div class="text-box">${val}</div><div class="hinge"></div>`;
    }

    function updateFlip(id, newVal, oldVal) {
        // 如果新舊值一樣，且已經有內容，則不觸發動畫（除非強制更新）
        const el = document.getElementById(id);
        if (newVal === oldVal && el.innerHTML !== "") return;
        
        el.innerHTML = `
            <div class="top">${createCardHTML(newVal)}</div>
            <div class="bottom">${createCardHTML(oldVal)}</div>
            <div class="leaf">
                <div class="leaf-front">${createCardHTML(oldVal)}</div>
                <div class="leaf-back">${createCardHTML(newVal)}</div>
            </div>
        `;
        el.classList.remove('flipping');
        void el.offsetWidth;
        el.classList.add('flipping');
    }

    function nextCity() {
        currentCityIdx = (currentCityIdx + 1) % cities.length;
        // 關鍵修正：切換城市時清空 prevTimeStr，強迫 tick 重新比對所有位數
        prevTimeStr = ""; 
        tick();
    }

    function tick() {
        const city = cities[currentCityIdx];
        
        // 取得該時區目前的正確時間字串
        const formatter = new Intl.DateTimeFormat('en-GB', {
            timeZone: city.zone,
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        const timeStr = formatter.format(new Date()).replace(/:/g, '');

        // 初始化結構
        if (document.getElementById('clock').innerHTML === "") {
            document.getElementById('clock').innerHTML = `
                <div class="unit-group"><div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div><div class="label">H</div></div>
                <div class="unit-group"><div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div><div class="label">M</div></div>
                <div class="unit-group"><div class="flip-card" id="d4"></div><div class="flip-card" id="d5"></div><div class="label">S</div></div>
            `;
        }

        // 更新城市文字
        updateFlip("city-cn", city.cn, prevCity.cn || city.cn);
        updateFlip("city-en", city.en, prevCity.en || city.en);
        prevCity = { cn: city.cn, en: city.en };

        // 更新數字位數
        for (let i = 0; i < 6; i++) {
            const nv = timeStr[i];
            const ov = prevTimeStr[i] || nv;
            // 只有當數字真正改變，或是 prevTimeStr 被清空時才翻轉
            if (nv !== ov || prevTimeStr === "") {
                updateFlip(`d${i}`, nv, ov);
            }
        }
        prevTimeStr = timeStr;
    }

    setInterval(tick, 1000);
    tick();
</script>
"""

st.title("🌏 全球翻板時鐘")
st.markdown("點擊上方城市名稱切換時區。")
st.components.v1.html(flip_clock_final, height=500)
