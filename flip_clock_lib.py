import streamlit as st
import streamlit.components.v1 as components
import random

def st_flip_clock():
    """
    1. 解決多出的板子：徹底刪除 unit-group 容器與時/分標籤，僅保留 4 個翻板數字。
    2. 最小化縫隙：將 hinge (轉軸) 高度設為 1px 純黑色實線。
    3. 強制刷新：使用隨機 Key 擊碎快取。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 30px; }

        /* 城市區 */
        .city-row { display: flex; gap: 10px; cursor: pointer; }
        .city-label { background: #222; color: #fff; padding: 10px 20px; border-radius: 8px; font-weight: 900; font-size: 22px; width: 140px; text-align: center; border: 1px solid #333; }

        /* 時間翻板：這是移除「多出板子」的核心，不再有 unit-group 容器 */
        .clock-row { display: flex; gap: 6px; align-items: center; perspective: 1000px; }
        .flip-card { 
            position: relative; width: 22vw; max-width: 85px; height: 110px; 
            font-family: "Arial Black", sans-serif; font-size: 80px; font-weight: 900; color: #e0e0e0; text-align: center;
        }

        /* 物理切割遮罩：杜絕殘影 */
        .up, .down { 
            position: absolute; left: 0; width: 100%; height: 50%; 
            overflow: hidden; display: flex; justify-content: center; background: #222; 
        }
        .up { top: 0; border-radius: 8px 8px 0 0; align-items: flex-end; border-bottom: 0.5px solid #000; }
        .down { bottom: 0; border-radius: 0 0 8px 8px; align-items: flex-start; }
        
        /* 文字位置修正 */
        .up span { transform: translateY(50%); }
        .down span { transform: translateY(-50%); }

        .leaf { position: absolute; top: 0; left: 0; width: 100%; height: 50%; z-index: 10; transform-origin: bottom; transition: transform 0.6s; transform-style: preserve-3d; }
        .leaf-front, .leaf-back { position: absolute; width: 100%; height: 100%; overflow: hidden; display: flex; justify-content: center; background: #222; backface-visibility: hidden; }
        .leaf-front { align-items: flex-end; border-radius: 8px 8px 0 0; }
        .leaf-back { align-items: flex-start; transform: rotateX(-180deg); border-radius: 0 0 8px 8px; }
        .leaf-front span { transform: translateY(50%); }
        .leaf-back span { transform: translateY(-50%); }

        .flipping .leaf { transform: rotateX(-180deg); }
        .hinge { position: absolute; top: 50%; width: 100%; height: 1px; background: #000; z-index: 20; transform: translateY(-50%); }
    </style>

    <div class="container">
        <div class="city-row" onclick="nextCity()">
            <div class="city-label" id="cn"></div>
            <div class="city-label" id="en"></div>
        </div>
        <div class="clock-row" id="clock"></div>
    </div>

    <script>
        const data = [
            { cn: "臺 北", en: "Taipei", off: 8 },
            { cn: "東 京", en: "Tokyo", off: 9 },
            { cn: "倫 敦", en: "London", off: 0 },
            { cn: "紐 約", en: "New York", off: -5 },
            { cn: "洛 杉 磯", en: "L.A.", off: -8 }
        ];
        let idx = 0, lastStr = "";

        function buildCard(val, old) {
            return `
                <div class="flip-card ${val!==old?'flipping':''}">
                    <div class="up"><span>${val}</span></div>
                    <div class="down"><span>${old}</span></div>
                    <div class="leaf">
                        <div class="leaf-front"><span>${old}</span></div>
                        <div class="leaf-back"><span>${val}</span></div>
                    </div>
                    <div class="hinge"></div>
                </div>`;
        }

        function nextCity() { idx = (idx + 1) % data.length; lastStr = ""; tick(); }

        function tick() {
            const city = data[idx];
            const now = new Date();
            const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            const target = new Date(utc + (city.off * 3600000));
            const h = String(target.getHours()).padStart(2, '0');
            const m = String(target.getMinutes()).padStart(2, '0');
            const str = h + m;

            document.getElementById('cn').innerText = city.cn;
            document.getElementById('en').innerText = city.en;

            let html = "";
            for(let i=0; i<4; i++) {
                html += buildCard(str[i], lastStr[i] || str[i]);
                if(i===1) html += '<div style="font-size:40px;color:#444;font-weight:bold;">:</div>';
            }
            document.getElementById('clock').innerHTML = html;
            lastStr = str;
        }
        setInterval(tick, 1000); tick();
    </script>
    """
    # 唯一 Key 確保每次執行都重新渲染，解決快取沒變化的問題
    return components.html(flip_html, height=400, key=f"v_final_{random.randint(0,99999)}")
