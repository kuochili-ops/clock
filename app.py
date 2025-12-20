import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    """
    基於「大寫中文穩定版」佈局修正：
    1. 修正 line-height 計算，移除多餘板面邊緣。
    2. 縮小 hinge (轉軸) 縫隙至 1px。
    3. 採用 UTC 偏移計算，確保時區一定連動。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 10px; overflow: hidden; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%; }

        /* 城市板 */
        .city-row { display: flex; gap: 10px; width: 100%; justify-content: center; cursor: pointer; margin-bottom: 20px; }
        .city-card { 
            position: relative; width: 44vw; max-width: 180px; height: 18vw; max-height: 70px;
            font-family: "Microsoft JhengHei", sans-serif; font-size: 6vw; font-weight: 900; color: #fff; text-align: center;
        }
        @media (min-width: 600px) { .city-card { font-size: 26px; } }

        /* 時間板 (完全採用您提供的 vw 布局) */
        .clock { display: flex; gap: 10px; perspective: 1500px; flex-wrap: wrap; justify-content: center; align-items: center; width: 100%; }
        .flip-card {
            position: relative; width: 18vw; max-width: 80px; height: 25vw; max-height: 110px;
            font-family: "Arial Black", sans-serif; font-size: 14.5vw; font-weight: 900; color: #e0e0e0; text-align: center;
        }
        @media (min-width: 600px) { .flip-card { width: 100px; height: 140px; font-size: 70px; } }

        /* 精確切割邏輯：解決「多一塊板」問題 */
        .top, .bottom, .leaf-front, .leaf-back {
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; box-sizing: border-box;
            border: 0.5px solid #111; /* 縮小邊框感 */
        }
        
        /* 城市板切割：line-height 等於板子總高度 */
        .city-card .top, .city-card .leaf-front { top: 0; border-radius: 6px 6px 0 0; line-height: 18vw; }
        .city-card .bottom, .city-card .leaf-back { bottom: 0; border-radius: 0 0 6px 6px; line-height: 0; }
        @media (min-width: 600px) { .city-card .top, .city-card .leaf-front { line-height: 70px; } }

        /* 時間板切割：修正 line-height 確保文字置中無殘影 */
        .flip-card .top, .flip-card .leaf-front { top: 0; border-radius: 8px 8px 0 0; line-height: 25vw; }
        .flip-card .bottom, .flip-card .leaf-back { bottom: 0; border-radius: 0 0 8px 8px; line-height: 0; }
        @media (min-width: 600px) { .flip-card .top, .flip-card .leaf-front { line-height: 140px; } }

        .leaf {
            position: absolute; top: 0; left: 0; width: 100%; height: 50%;
            z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }

        /* 修正轉軸：縮小縫隙 */
        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 1px; background: rgba(0,0,0,0.8); z-index: 20; transform: translateY(-50%); }
        
        .label { font-size: 16px; color: #555; align-self: flex-end; padding-bottom: 5px; font-weight: bold; }
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
            // 強制時區修正：確保手機端切換時時間一定跳動
            const now = new Date();
            const utcTime = now.getTime() + (now.getTimezoneOffset() * 60000);
            const targetTime = new Date(utcTime + (3600000 * city.offset));
            
            const h = targetTime.getHours().toString().padStart(2, '0');
            const m = targetTime.getMinutes().toString().padStart(2, '0');
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
                const nv = timeStr[i]; 
                const ov = prevTimeStr[i] || nv;
                if (nv !== ov || prevTimeStr === "") updateFlip(`d${i}`, nv, ov);
            }
            prevTimeStr = timeStr;
        }
        setInterval(tick, 1000); tick();
    </script>
    """
    return components.html(flip_html, height=450)
