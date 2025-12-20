import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    """
    提供一個高度優化的全球城市機械翻板鐘。
    """
    flip_html = """
    <style>
        /* 面板與容器設定 */
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 10px; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 30px; width: 100%; }
        
        /* 城市名稱面板 */
        .city-row { display: flex; gap: 10px; width: 100%; justify-content: center; cursor: pointer; }
        .city-card { position: relative; width: 44vw; max-width: 170px; height: 75px; perspective: 1000px; color: #fff; }
        
        /* 時間數字面板 (時、分) */
        .clock { display: flex; gap: 10px; justify-content: center; align-items: center; }
        .flip-card { position: relative; width: 18vw; max-width: 85px; height: 26vw; max-height: 125px; font-weight: 900; color: #f0f0f0; perspective: 1000px; }
        
        /* 面板背景與切割對齊 */
        .top, .bottom, .leaf-front, .leaf-back { 
            position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; 
            background: #1e1e1e; display: flex; justify-content: center; box-sizing: border-box; border: 1px solid #000; 
        }
        .top, .leaf-front { top: 0; border-radius: 8px 8px 0 0; align-items: flex-end; }
        .bottom, .leaf-back { bottom: 0; border-radius: 0 0 8px 8px; align-items: flex-start; }
        
        /* 雙倍高度容器實現完美置中 */
        .text-box { height: 200%; display: flex; align-items: center; line-height: 1; width: 100%; justify-content: center; }
        .top .text-box, .leaf-front .text-box { transform: translateY(50%); margin-bottom: -0.5px; }
        .bottom .text-box, .leaf-back .text-box { transform: translateY(-50%); margin-top: -0.5px; }
        
        /* 字體尺寸設定 */
        .city-card .text-box { font-size: 1.2rem; font-family: "Microsoft JhengHei", sans-serif; }
        .flip-card .text-box { font-size: 18vw; font-family: 'Arial Black', Gadget, sans-serif; }
        @media (min-width: 600px) { .flip-card .text-box { font-size: 95px; } .city-card .text-box { font-size: 26px; } .flip-card { width: 100px; height: 140px; } }
        
        /* 翻轉動畫 (延續您的原始邏輯) */
        .leaf { position: absolute; top: 0; left: 0; width: 100%; height: 50%; z-index: 10; transform-origin: bottom; transform-style: preserve-3d; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }
        
        /* 擬真中軸線 */
        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 1.5px; background: linear-gradient(to bottom, #000, #333, #000); z-index: 20; transform: translateY(-50%); }
        .label { font-size: 16px; color: #888; align-self: flex-end; padding-bottom: 8px; margin-left: 5px; font-weight: bold;}
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
        let currentCityIdx = 0, prevTimeStr = "", prevCity = { cn: "", en: "" };
        function createCardHTML(val) { return `<div class="text-box">${val}</div><div class="hinge"></div>`; }
        function updateFlip(id, newVal, oldVal) {
            const el = document.getElementById(id);
            if (newVal === oldVal && el.innerHTML !== "") return;
            el.innerHTML = `<div class="top">${createCardHTML(newVal)}</div><div class="bottom">${createCardHTML(oldVal)}</div><div class="leaf"><div class="leaf-front">${createCardHTML(oldVal)}</div><div class="leaf-back">${createCardHTML(newVal)}</div></div>`;
            el.classList.remove('flipping'); void el.offsetWidth; el.classList.add('flipping');
        }
        function nextCity() { currentCityIdx = (currentCityIdx + 1) % cities.length; prevTimeStr = ""; tick(); }
        function tick() {
            const city = cities[currentCityIdx];
            const now = new Date();
            const timeStr = now.toLocaleTimeString('en-GB', {timeZone: city.zone, hour12: false, hour: '2-digit', minute: '2-digit'}).replace(/:/g, '');
            if (document.getElementById('clock').innerHTML === "") {
                document.getElementById('clock').innerHTML = `<div class="unit-group"><div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div><div class="label">時</div></div><div class="unit-group"><div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div><div class="label">分</div></div>`;
            }
            updateFlip("city-cn", city.cn, prevCity.cn || city.cn);
            updateFlip("city-en", city.en, prevCity.en || city.en);
            prevCity = { cn: city.cn, en: city.en };
            for (let i = 0; i < 4; i++) {
                const nv = timeStr[i]; const ov = prevTimeStr[i] || nv;
                if (nv !== ov || prevTimeStr === "") updateFlip(`d${i}`, nv, ov);
            }
            prevTimeStr = timeStr;
        }
        setInterval(tick, 1000); tick();
    </script>
    """
    return components.html(flip_html, height=500)
