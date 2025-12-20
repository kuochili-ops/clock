import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    # 這裡的 HTML 代碼做了大幅度簡化
    flip_html = """
    <style>
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 0; overflow: hidden; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 30px; width: 100%; }

        /* 城市板 */
        .city-row { display: flex; gap: 10px; width: 100%; justify-content: center; cursor: pointer; }
        .city-card { position: relative; width: 44vw; max-width: 170px; height: 60px; font-family: sans-serif; font-size: 24px; font-weight: 900; color: #fff; text-align: center; }

        /* 時間板：徹底移除 label 與 unit-group，只剩 4 個數字 */
        .clock { display: flex; gap: 6px; perspective: 1000px; justify-content: center; align-items: center; }
        .flip-card { position: relative; width: 22vw; max-width: 85px; height: 110px; font-family: "Arial Black", sans-serif; font-size: 80px; font-weight: 900; color: #e0e0e0; text-align: center; }

        /* 物理切割：確保無殘影 */
        .top, .bottom, .leaf-front, .leaf-back {
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; box-sizing: border-box;
            display: flex; justify-content: center;
        }
        .top, .leaf-front { top: 0; border-radius: 6px 6px 0 0; border-bottom: 1px solid #000; align-items: flex-end; }
        .bottom, .leaf-back { bottom: 0; border-radius: 0 0 6px 6px; align-items: flex-start; }
        
        /* 物理偏移對齊文字 */
        .top span, .leaf-front span { transform: translateY(50%); }
        .bottom span, .leaf-back span { transform: translateY(-50%); }

        .leaf { position: absolute; top: 0; left: 0; width: 100%; height: 50%; z-index: 10; transform-origin: bottom; transform-style: preserve-3d; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }
        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 1px; background: #000; z-index: 20; }
    </style>

    <div class="container">
        <div class="city-row" id="click_area">
            <div class="city-card" id="city-cn"></div>
            <div class="city-card" id="city-en"></div>
        </div>
        <div class="clock">
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

        let cityIdx = 0, prevTime = "", prevCity = { cn: "", en: "" };

        function updateFlip(id, newVal, oldVal) {
            const el = document.getElementById(id);
            if (!el || (newVal === oldVal && el.innerHTML !== "")) return;
            el.innerHTML = `<div class="top"><span>${newVal}</span></div><div class="bottom"><span>${oldVal}</span></div><div class="leaf"><div class="leaf-front"><span>${oldVal}</span></div><div class="leaf-back"><span>${newVal}</span></div></div><div class="hinge"></div>`;
            el.classList.remove('flipping');
            void el.offsetWidth;
            el.classList.add('flipping');
        }

        document.getElementById('click_area').onclick = () => {
            cityIdx = (cityIdx + 1) % cities.length;
            prevTime = ""; // 強制刷新
            tick();
        };

        function tick() {
            const city = cities[cityIdx];
            // 絕對時區計算：避免設備 locale 干擾
            const d = new Date();
            const utc = d.getTime() + (d.getTimezoneOffset() * 60000);
            const target = new Date(utc + (city.offset * 3600000));
            const h = String(target.getHours()).padStart(2, '0');
            const m = String(target.getMinutes()).padStart(2, '0');
            const timeStr = h + m;

            updateFlip("city-cn", city.cn, prevCity.cn || city.cn);
            updateFlip("city-en", city.en, prevCity.en || city.en);
            prevCity = { cn: city.cn, en: city.en };

            for (let i = 0; i < 4; i++) {
                const nv = timeStr[i];
                const ov = prevTime[i] || nv;
                if (nv !== ov || prevTime === "") updateFlip(`d${i}`, nv, ov);
            }
            prevTime = timeStr;
        }
        setInterval(tick, 1000); tick();
    </script>
    """
    # 修正：給予唯一的 key 避免 Streamlit 緩存舊的 iframe
    import time
    return components.html(flip_html, height=400, key=f"flip_clock_{time.time()}")
