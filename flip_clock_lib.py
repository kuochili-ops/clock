import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    """
    基於原始大寫中文翻板邏輯優化的全球城市翻板鐘模組。
    解決了手機版時區失效與面板文字偏離問題。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 10px; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 30px; width: 100%; }

        /* 城市翻板面板 */
        .city-row { display: flex; gap: 10px; width: 100%; justify-content: center; cursor: pointer; }
        .city-card { 
            position: relative; width: 44vw; max-width: 170px; height: 75px; 
            font-family: "Microsoft JhengHei", sans-serif; font-size: 24px; font-weight: 900; color: #fff; 
        }

        /* 時間面板 (僅時、分) */
        .clock { display: flex; gap: 10px; justify-content: center; align-items: center; }
        .flip-card { 
            position: relative; width: 18vw; max-width: 85px; height: 120px; 
            font-family: "Arial Black", sans-serif; font-size: 70px; font-weight: 900; color: #e0e0e0;
        }

        /* 繼承您提供的原始切割邏輯 */
        .top, .bottom, .leaf-front, .leaf-back {
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; border: 1px solid #111; text-align: center; box-sizing: border-box;
        }
        
        /* 修正文字切割點：城市卡片與時間卡片高度不同，需分開設定 line-height */
        .city-card .top, .city-card .leaf-front { top: 0; border-radius: 6px 6px 0 0; line-height: 75px; }
        .city-card .bottom, .city-card .leaf-back { bottom: 0; border-radius: 0 0 6px 6px; line-height: 0px; }
        
        .flip-card .top, .flip-card .leaf-front { top: 0; border-radius: 8px 8px 0 0; line-height: 120px; }
        .flip-card .bottom, .flip-card .leaf-back { bottom: 0; border-radius: 0 0 8px 8px; line-height: 0px; }

        .leaf {
            position: absolute; top: 0; left: 0; width: 100%; height: 50%;
            z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }

        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background: #000; z-index: 20; transform: translateY(-50%); }
        .label { font-size: 18px; color: #555; align-self: flex-end; padding-bottom: 10px; font-weight: bold; }
        .unit-group { display: flex; gap: 4px; align-items: center; }
        
        @media (max-width: 600px) {
            .flip-card { height: 100px; font-size: 55px; }
            .flip-card .top, .flip-card .leaf-front { line-height: 100px; }
        }
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

        function nextCity() { currentCityIdx = (currentCityIdx + 1) % cities.length; prevTimeStr = ""; tick(); }

        function tick() {
            const city = cities[currentCityIdx];
            // 手動計算 UTC 偏移，確保時區一定起作用
            const d = new Date();
            const localTime = new Date(d.getTime() + (d.getTimezoneOffset() * 60000) + (city.offset * 3600000));
            const h = localTime.getHours().toString().padStart(2, '0');
            const m = localTime.getMinutes().toString().padStart(2, '0');
            const timeStr = h + m;

            if (document.getElementById('clock').innerHTML === "") {
                document.getElementById('clock').innerHTML = `
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
