import streamlit as st
import streamlit.components.v1 as components

def st_flip_clock():
    """
    極簡化翻板邏輯：回歸 line-height 切割法，杜絕鏡像殘影，並修正時區失效。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 40px; width: 100%; }

        /* 城市板面板設定 */
        .city-row { display: flex; gap: 15px; width: 100%; justify-content: center; cursor: pointer; }
        .city-card { 
            position: relative; width: 42vw; max-width: 170px; height: 70px; 
            font-family: sans-serif; font-size: 24px; font-weight: bold; color: #fff; text-align: center;
        }

        /* 時間板面板設定 */
        .clock { display: flex; gap: 10px; justify-content: center; align-items: center; }
        .flip-card { 
            position: relative; width: 18vw; max-width: 85px; height: 110px; 
            font-family: "Arial Black", sans-serif; font-size: 70px; font-weight: 900; color: #eee; text-align: center;
        }

        /* 關鍵：純淨切割法 (無位移、無殘影) */
        .top, .bottom, .leaf-front, .leaf-back {
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; border: 1px solid #111; box-sizing: border-box;
        }
        
        /* 城市板文字高度對齊 */
        .city-card .top, .city-card .leaf-front { top: 0; border-radius: 6px 6px 0 0; line-height: 70px; }
        .city-card .bottom, .city-card .leaf-back { bottom: 0; border-radius: 0 0 6px 6px; line-height: 0px; }

        /* 時間板文字高度對齊 */
        .flip-card .top, .flip-card .leaf-front { top: 0; border-radius: 8px 8px 0 0; line-height: 110px; }
        .flip-card .bottom, .flip-card .leaf-back { bottom: 0; border-radius: 0 0 8px 8px; line-height: 0px; }

        .leaf {
            position: absolute; top: 0; left: 0; width: 100%; height: 50%;
            z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }

        .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background: #000; z-index: 20; transform: translateY(-50%); }
        .label { font-size: 18px; color: #555; align-self: flex-end; padding-bottom: 8px; font-weight: bold; }
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
            prevTimeStr = ""; // 強迫切換城市後重刷時間
            tick(); 
        }

        function tick() {
            const city = cities[currentCityIdx];
            
            // 解決時區問題：使用 UTC 加手動偏移
            const d = new Date();
            const utc = d.getTime() + (d.getTimezoneOffset() * 60000);
            const local = new Date(utc + (3600000 * city.offset));
            
            const h = local.getHours().toString().padStart(2, '0');
            const m = local.getMinutes().toString().padStart(2, '0');
            const timeStr = h + m;

            if (document.getElementById('clock').innerHTML === "") {
                document.getElementById('clock').innerHTML = `
                    <div style="display:flex; gap:4px; align-items:center;">
                        <div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div><div class="label">時</div>
                    </div>
                    <div style="display:flex; gap:4px; align-items:center;">
                        <div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div><div class="label">分</div>
                    </div>
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
    return components.html(flip_html, height=450)
