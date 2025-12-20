import streamlit as st
import streamlit.components.v1 as components
import random

def st_flip_clock():
    """
    1. 物理移除：刪除所有 '時'、'分' 標籤與外圍 div，解決多出板塊問題。
    2. 鎖定時區：改用純數學毫秒運算，強行跳轉倫敦、紐約時間。
    3. 強制重載：使用隨機 Key 擊碎 Streamlit 伺服器快取。
    """
    # 這裡的 HTML 是完全重寫的極簡結構
    flip_html = """
    <div id="root"></div>
    <style>
        body { background-color: #0e1117; margin: 0; padding: 20px; display: flex; justify-content: center; font-family: sans-serif; overflow: hidden; }
        .clock-container { display: flex; flex-direction: column; align-items: center; gap: 30px; }
        
        /* 城市板：移除所有裝飾外框 */
        .city-box { display: flex; gap: 15px; cursor: pointer; }
        .city-label { background: #222; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 900; font-size: 22px; width: 140px; text-align: center; border: 1px solid #333; }

        /* 時間板：只有 4 個純翻板，中間一個冒號 */
        .flip-row { display: flex; gap: 8px; align-items: center; }
        .digit-card { 
            position: relative; width: 20vw; max-width: 85px; height: 110px; 
            background: #222; border-radius: 8px; font-family: "Arial Black"; 
            font-size: 80px; font-weight: 900; color: #e0e0e0; text-align: center;
        }

        /* 物理切割：杜絕殘影與多餘板面 */
        .up, .down { 
            position: absolute; left: 0; width: 100%; height: 50%; 
            overflow: hidden; display: flex; justify-content: center; box-sizing: border-box;
        }
        .up { top: 0; border-radius: 8px 8px 0 0; align-items: flex-end; border-bottom: 1px solid #000; }
        .down { bottom: 0; border-radius: 0 0 8px 8px; align-items: flex-start; }
        
        /* 文字精確位移 */
        .up span { transform: translateY(50%); }
        .down span { transform: translateY(-50%); }

        .leaf { 
            position: absolute; top: 0; left: 0; width: 100%; height: 50%; 
            z-index: 10; transform-origin: bottom; transition: transform 0.6s; transform-style: preserve-3d;
        }
        .leaf-front, .leaf-back { position: absolute; width: 100%; height: 100%; overflow: hidden; display: flex; justify-content: center; background: #222; backface-visibility: hidden; }
        .leaf-front { align-items: flex-end; border-radius: 8px 8px 0 0; }
        .leaf-back { align-items: flex-start; transform: rotateX(-180deg); border-radius: 0 0 8px 8px; }
        .leaf-front span { transform: translateY(50%); }
        .leaf-back span { transform: translateY(-50%); }
        
        .flipping .leaf { transform: rotateX(-180deg); }
        .hinge { position: absolute; top: 50%; width: 100%; height: 1px; background: #000; z-index: 20; }
    </style>

    <div class="clock-container">
        <div class="city-box" onclick="changeCity()">
            <div class="city-label" id="cn-name"></div>
            <div class="city-label" id="en-name"></div>
        </div>
        <div class="flip-row" id="clock-row"></div>
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

        function createFlip(id, val, old) {
            return `
                <div class="digit-card ${val!==old?'flipping':''}" id="${id}">
                    <div class="up"><span>${val}</span></div>
                    <div class="down"><span>${old}</span></div>
                    <div class="leaf">
                        <div class="leaf-front"><span>${old}</span></div>
                        <div class="leaf-back"><span>${val}</span></div>
                    </div>
                    <div class="hinge"></div>
                </div>`;
        }

        function changeCity() { idx = (idx + 1) % data.length; lastStr = ""; tick(); }

        function tick() {
            const city = data[idx];
            // 強制物理時區計算法
            const now = new Date();
            const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            const target = new Date(utc + (city.off * 3600000));
            const h = String(target.getHours()).padStart(2, '0');
            const m = String(target.getMinutes()).padStart(2, '0');
            const currentStr = h + m;

            document.getElementById('cn-name').innerText = city.cn;
            document.getElementById('en-name').innerText = city.en;

            let html = "";
            for(let i=0; i<4; i++) {
                html += createFlip('d'+i, currentStr[i], lastStr[i] || currentStr[i]);
                if(i===1) html += '<div style="font-size:40px;color:#444;font-weight:bold;">:</div>';
            }
            document.getElementById('clock-row').innerHTML = html;
            lastStr = currentStr;
        }
        setInterval(tick, 1000); tick();
    </script>
    """
    # 使用隨機數作為 key，徹底殺死所有快取
    random_id = random.randint(1, 1000000)
    return components.html(flip_html, height=400, key=f"clock_v3_{random_id}")
