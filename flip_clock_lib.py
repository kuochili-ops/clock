import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    """
    1. 強制重繪版：切換城市時直接清空 DOM，解決時區不動的 Bug。
    2. 物理切割：移除 line-height，改用 translateY 對齊，解決殘影。
    3. 極簡佈局：移除所有 unit-group 與 label，移除多餘板塊。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 0; overflow: hidden; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 25px; width: 100%; }

        .city-row { display: flex; gap: 10px; width: 100%; justify-content: center; cursor: pointer; }
        .city-card { position: relative; width: 44vw; max-width: 170px; height: 60px; font-family: sans-serif; font-size: 24px; font-weight: 900; color: #fff; text-align: center; }

        .clock { display: flex; gap: 6px; perspective: 1000px; justify-content: center; align-items: center; }
        .flip-card { position: relative; width: 22vw; max-width: 85px; height: 110px; font-family: "Arial Black", sans-serif; font-size: 80px; font-weight: 900; color: #e0e0e0; text-align: center; }

        /* 物理切割與對齊 */
        .top, .bottom, .leaf-front, .leaf-back {
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; box-sizing: border-box;
            display: flex; justify-content: center;
        }
        .top, .leaf-front { top: 0; border-radius: 6px 6px 0 0; border-bottom: 0.5px solid #000; align-items: flex-end; }
        .bottom, .leaf-back { bottom: 0; border-radius: 0 0 6px 6px; align-items: flex-start; }
        
        /* 移除 line-height 偏移，改用位移確保文字在中央切開 */
        .top span, .leaf-front span { transform: translateY(50%); }
        .bottom span, .leaf-back span { transform: translateY(-50%); }

        .leaf { position: absolute; top: 0; left: 0; width: 100%; height: 50%; z-index: 10; transform-origin: bottom; transform-style: preserve-3d; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }
        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 1px; background: #000; z-index: 20; }
    </style>

    <div class="container">
        <div class="city-row" id="city_trigger">
            <div class="city-card" id="city-cn"></div>
            <div class="city-card" id="city-en"></div>
        </div>
        <div class="clock" id="clock_shell">
            <div class="flip-card" id="d0"></div>
            <div class="flip-card" id="d1"></div>
            <div style="font-size: 40px; color: #444; font-weight: bold; margin: 0 4px;">:</div>
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
            if (!el) return;
            // 如果值相同且不是初始狀態，不翻轉
            if (newVal === oldVal && el.innerHTML !== "") return;
            
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

        // 強制切換函數
        document.getElementById('city_trigger').onclick = function() {
            currentCityIdx = (currentCityIdx + 1) % cities.length;
            prevTimeStr = ""; // 關鍵：清空狀態，強制重繪
            tick();
        };

        function tick() {
            const city = cities[currentCityIdx];
            // 強制 UTC 偏移量計算，無視系統時區
            const now = new Date();
            const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            const target = new Date(utc + (3600000 * city.offset));
            
            const h = target.getHours().toString().padStart(2, '0');
            const m = target.getMinutes().toString().padStart(2, '0');
            const timeStr = h + m;

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

        setInterval(tick, 1000);
        tick();
    </script>
    """
    # 稍微調大 height 確保 iframe 內部不會出現滾動條
    return components.html(flip_html, height=420)
