import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    """
    完全採用您的大寫中文版結構，但加入「遮罩修正」防止殘影，並鎖死「UTC 偏移」解決時區失效。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 10px; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 30px; width: 100%; }

        /* 城市板與時間板 */
        .city-row { display: flex; gap: 10px; width: 100%; justify-content: center; cursor: pointer; }
        .city-card { position: relative; width: 44vw; max-width: 170px; height: 75px; font-family: sans-serif; font-size: 24px; font-weight: 900; color: #fff; text-align: center; }
        .clock { display: flex; gap: 10px; justify-content: center; align-items: center; flex-wrap: wrap; }
        .flip-card { position: relative; width: 18vw; max-width: 85px; height: 110px; font-family: "Arial Black", sans-serif; font-size: 75px; font-weight: 900; color: #e0e0e0; text-align: center; }

        /* 核心修正：加入 overflow:hidden 與強制背景遮擋，杜絕殘影 */
        .top, .bottom, .leaf-front, .leaf-back {
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; border: 1px solid #111; box-sizing: border-box;
            backface-visibility: hidden; /* 防止翻轉時背面透出 */
        }
        
        /* 城市切割：強制文字只顯示一半 */
        .city-card .top, .city-card .leaf-front { top: 0; border-radius: 6px 6px 0 0; line-height: 75px; }
        .city-card .bottom, .city-card .leaf-back { bottom: 0; border-radius: 0 0 6px 6px; line-height: 0px; }

        /* 時間切割：強制文字只顯示一半 */
        .flip-card .top, .flip-card .leaf-front { top: 0; border-radius: 8px 8px 0 0; line-height: 110px; }
        .flip-card .bottom, .flip-card .leaf-back { bottom: 0; border-radius: 0 0 8px 8px; line-height: 0px; }

        /* 翻轉動作 */
        .leaf {
            position: absolute; top: 0; left: 0; width: 100%; height: 50%;
            z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .leaf-back { transform: rotateX(-180deg); background: #222; }
        .flipping .leaf { transform: rotateX(-180deg); }

        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background: #000; z-index: 20; transform: translateY(-50%); }
        .label { font-size: 18px; color: #555; align-self: flex-end; padding-bottom: 8px; font-weight: bold; }
        .unit-group { display: flex; gap: 4px; align-items: center; }
    </style>

    <div class="container">
        <div class="city-row" onclick="nextCity()">
            <div class="city-card" id="city-cn"></div>
            <div class="city-card" id="city-en"></div>
        </div>
        <div id="clock_content" class="clock"></div>
    </div>

    <script>
        const cities = [
            { cn: "臺 北", en: "Taipei", offset: 8 },
            { cn: "東 京", en: "Tokyo", offset: 9 },
            { cn: "倫 敦", en: "London", offset: 0 },
            { cn: "紐 約", en: "New York", offset: -5 },
            { cn: "洛 杉 磯", en: "Los Angeles", offset: -8 }
        ];

        let currentCityIdx = 0, prevTimeStr = "", prevCity = { cn: "", en: "" };

        function updateFlip(id, newVal, oldVal) {
            const el = document.getElementById(id);
            if (newVal === oldVal && el.innerHTML !== "") return;
            el.innerHTML = `
                <div class="top">${newVal}</div>
                <div class="bottom">${oldVal}</div>
                <div class="leaf">
                    <div class="leaf-front">${oldVal}</div>
                    <div class="leaf-back">${newVal}</div>
                </div>
                <div class="hinge"></div>
            `;
            el.classList.remove('flipping');
            void el.offsetWidth;
            el.classList.add('flipping');
        }

        function nextCity() { 
            currentCityIdx = (currentCityIdx + 1) % cities.length; 
            prevTimeStr = ""; 
            tick(); 
        }

        function tick() {
            const city = cities[currentCityIdx];
            const d = new Date();
            // 修正時區：不使用名稱，改用 UTC 絕對毫秒偏移
            const utc = d.getTime() + (d.getTimezoneOffset() * 60000);
            const local = new Date(utc + (3600000 * city.offset));
            const h = local.getHours().toString().padStart(2, '0');
            const m = local.getMinutes().toString().padStart(2, '0');
            const timeStr = h + m;

            const clockRoot = document.getElementById('clock_content');
            if (clockRoot.innerHTML === "") {
                clockRoot.innerHTML = `
                    <div class="unit-group"><div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div><div class="label">時</div></div>
                    <div class="unit-group"><div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div><div class="label">分</div></div>
                `;
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
