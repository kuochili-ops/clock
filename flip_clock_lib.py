import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    """
    產生一個支援手機瀏覽、阿拉伯數字顯示與城市切換功能的機械翻板鐘。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 35px; width: 100%; }
        .city-row { display: flex; gap: 12px; width: 100%; justify-content: center; cursor: pointer; }
        .city-card { position: relative; width: 42vw; max-width: 160px; height: 75px; perspective: 1000px; color: #fff; }
        .clock { display: flex; gap: 20px; justify-content: center; align-items: center; }
        .flip-card { position: relative; width: 18vw; max-width: 85px; height: 26vw; max-height: 125px; font-weight: 900; color: #f0f0f0; perspective: 1000px; }
        .top, .bottom, .leaf-front, .leaf-back { position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; box-sizing: border-box; border: 1px solid #000; }
        .top, .leaf-front { top: 0; border-radius: 8px 8px 0 0; align-items: flex-end; }
        .bottom, .leaf-back { bottom: 0; border-radius: 0 0 8px 8px; align-items: flex-start; }
        .text-box { height: 200%; display: flex; align-items: center; line-height: 1; width: 100%; justify-content: center; }
        .top .text-box, .leaf-front .text-box { transform: translateY(50%); }
        .bottom .text-box, .leaf-back .text-box { transform: translateY(-50%); }
        .city-card .text-box { font-size: 20px; font-family: "Microsoft JhengHei", sans-serif; }
        .flip-card .text-box { font-size: 20vw; font-family: 'Courier New', Courier, monospace; }
        @media (min-width: 600px) { .flip-card .text-box { font-size: 110px; } .city-card .text-box { font-size: 28px; } .flip-card { width: 100px; height: 140px; } }
        .leaf { position: absolute; top: 0; left: 0; width: 100%; height: 50%; z-index: 10; transform-origin: bottom; transform-style: preserve-3d; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }
        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 1.5px; background: rgba(0,0,0,0.7); z-index: 20; transform: translateY(-50%); }
        .label { font-size: 18px; color: #666; align-self: flex-end; padding-bottom: 10px; font-weight: bold; }
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
            const timeStr = new Intl.DateTimeFormat('en-GB', {timeZone: city.zone, hour12: false, hour: '2-digit', minute: '2-digit'}).format(new Date()).replace(/:/g, '');
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
