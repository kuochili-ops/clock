import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    """
    1. 移除多餘板塊：簡化 HTML 結構，移除 unit-group 與 label，讓畫面只剩純翻板。
    2. 鎖定時區連動：在 tick() 內強行計算 UTC 偏移，不依賴設備本地時區設定。
    3. 最小化縫隙：轉軸改為 1px 純黑色實線。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 0; overflow: hidden; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 30px; width: 100%; }

        /* 城市板：移除多餘外框，僅保留翻板核心 */
        .city-row { display: flex; gap: 12px; width: 100%; justify-content: center; cursor: pointer; }
        .city-card { 
            position: relative; width: 42vw; max-width: 160px; height: 65px; 
            font-family: sans-serif; font-size: 24px; font-weight: 900; color: #fff; text-align: center;
        }

        /* 時間板：移除所有外圍 label，解決「多出一塊板」問題 */
        .clock { display: flex; gap: 6px; perspective: 1000px; justify-content: center; align-items: center; }
        .flip-card { 
            position: relative; width: 21vw; max-width: 85px; height: 110px; 
            font-family: "Arial Black", sans-serif; font-size: 80px; font-weight: 900; color: #e0e0e0; text-align: center;
        }

        /* 物理切割：確保無殘影 */
        .top, .bottom, .leaf-front, .leaf-back {
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; box-sizing: border-box;
            display: flex; justify-content: center;
        }
        .top, .leaf-front { top: 0; border-radius: 6px 6px 0 0; border-bottom: 0.5px solid #000; align-items: flex-end; }
        .bottom, .leaf-back { bottom: 0; border-radius: 0 0 6px 6px; align-items: flex-start; }

        /* 文字位移對齊 */
        .top span, .leaf-front span { transform: translateY(50%); }
        .bottom span, .leaf-back span { transform: translateY(-50%); }

        .leaf {
            position: absolute; top: 0; left: 0; width: 100%; height: 50%;
            z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }

        /* 最小化轉軸 */
        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 1px; background: #000; z-index: 20; }
        
        /* 桌面端字體微調 */
        @media (min-width: 600px) {
            .city-card { font-size: 26px; height: 75px; }
            .flip-card { font-size: 75px; height: 140px; }
            .top span, .leaf-front span { transform: translateY(50%); }
            .bottom span, .leaf-back span { transform: translateY(-50%); }
        }
    </style>

    <div class="container">
        <div class="city-row" onclick="nextCity()">
            <div class="city-card" id="city-cn"></div>
            <div class="city-card" id="city-en"></div>
        </div>
        <div class="clock" id="clock_main">
            <div class="flip-card" id="d0"></div>
            <div class="flip-card" id="d1"></div>
            <div style="font-size: 40px; color: #444; font-weight: bold; margin: 0 5px;">:</div>
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
            prevTimeStr = ""; // 關鍵：清空舊時間字串，強迫 JavaScript 重新計算與翻轉
            tick(); 
        }

        function tick() {
            const city = cities[currentCityIdx];
            // 強制時區修正：完全不依賴瀏覽器 locale，改用 UTC 絕對毫秒偏移量
            const now = new Date();
            const utcMillis = now.getTime() + (now.getTimezoneOffset() * 60000);
            const targetDate = new Date(utcMillis + (3600000 * city.offset));
            
            const h = targetDate.getHours().toString().padStart(2, '0');
            const m = targetDate.getMinutes().toString().padStart(2, '0');
            const timeStr = h + m;

            // 更新城市板
            updateFlip("city-cn", city.cn, prevCity.cn || city.cn);
            updateFlip("city-en", city.en, prevCity.en || city.en);
            prevCity = { cn: city.cn, en: city.en };

            // 更新時間數字
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
    return components.html(flip_html, height=450)
