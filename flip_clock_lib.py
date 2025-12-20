import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    """
    極簡穩定版：
    1. 移除所有多餘裝飾板與標籤，只保留核心翻板。
    2. 使用固定的時區偏移計算，解決手機版時區不跳動的 Bug。
    3. 鎖定物理高度，徹底解決殘影與佈局位移。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 0; overflow: hidden; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%; }

        /* 城市顯示區 */
        .city-row { display: flex; gap: 10px; width: 100%; justify-content: center; cursor: pointer; }
        .city-card { 
            position: relative; width: 44vw; max-width: 170px; height: 60px; 
            font-family: sans-serif; font-size: 24px; font-weight: 900; color: #fff; text-align: center;
        }

        /* 時間翻板區：移除 label 與 unit-group，保持極簡 */
        .clock { display: flex; gap: 8px; perspective: 1000px; justify-content: center; align-items: center; width: 100%; }
        .flip-card { 
            position: relative; width: 22vw; max-width: 85px; height: 110px; 
            font-family: "Arial Black", sans-serif; font-size: 80px; font-weight: 900; color: #e0e0e0; text-align: center;
        }

        /* 核心切割：移除 line-height，改用物理遮罩 */
        .top, .bottom, .leaf-front, .leaf-back {
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; box-sizing: border-box;
            display: flex; justify-content: center;
        }
        
        .top, .leaf-front { 
            top: 0; border-radius: 6px 6px 0 0; border-bottom: 0.5px solid #000;
            align-items: flex-end; /* 文字對齊底部切割線 */
        }
        .bottom, .leaf-back { 
            bottom: 0; border-radius: 0 0 6px 6px; 
            align-items: flex-start; /* 文字對齊頂部切割線 */
        }

        /* 文字容器：確保文字上下各一半 */
        .top span, .leaf-front span { transform: translateY(50%); }
        .bottom span, .leaf-back span { transform: translateY(-50%); }

        /* 翻轉動畫 */
        .leaf {
            position: absolute; top: 0; left: 0; width: 100%; height: 50%;
            z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }

        /* 最小轉軸 */
        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 1px; background: #000; z-index: 20; }
    </style>

    <div class="container">
        <div class="city-row" onclick="nextCity()">
            <div class="city-card" id="city-cn"></div>
            <div class="city-card" id="city-en"></div>
        </div>
        <div class="clock">
            <div class="flip-card" id="d0"></div>
            <div class="flip-card" id="d1"></div>
            <div style="font-size: 40px; color: #555; font-weight: bold; margin: 0 5px;">:</div>
            <div class="flip-card" id="d2"></div>
            <div class="flip-card" id="d3"></div>
        </div>
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
            if (!el || (newVal === oldVal && el.innerHTML !== "")) return;
            el.innerHTML = `
                <div class="top"><span>${newVal}</span></div>
                <div class="bottom"><span>${oldVal}</span></div>
                <div class="leaf">
                    <div class="leaf-front"><span>${oldVal}</span></div>
                    <div class="leaf-back"><span>${newVal}</span></div>
                </div>
                <div class="hinge"></div>
            `;
            el.classList.remove('flipping');
            void el.offsetWidth;
            el.classList.add('flipping');
        }

        function nextCity() { 
            currentCityIdx = (currentCityIdx + 1) % cities.length; 
            prevTimeStr = ""; // 強制刷新時間
            tick(); 
        }

        function tick() {
            const city = cities[currentCityIdx];
            // 核心時區運算：解決切換城市不動的問題
            const now = new Date();
            const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            const target = new Date(utc + (3600000 * city.offset));
            
            const h = target.getHours().toString().padStart(2, '0');
            const m = target.getMinutes().toString().padStart(2, '0');
            const timeStr = h + m;

            // 更新城市
            updateFlip("city-cn", city.cn, prevCity.cn || city.cn);
            updateFlip("city-en", city.en, prevCity.en || city.en);
            prevCity = { cn: city.cn, en: city.en };

            // 更新時間
            for (let i = 0; i < 4; i++) {
                const nv = timeStr[i];
                const ov = prevTimeStr[i] || nv;
                if (nv !== ov || prevTimeStr === "") updateFlip(`d${i}`, nv, ov);
            }
            prevTimeStr = timeStr;
        }

        setInterval(tick, 1000);
        tick();
    </script>
    """
    return components.html(flip_html, height=400)
