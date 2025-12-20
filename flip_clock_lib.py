import streamlit as st
import streamlit.components.v1 as components
import time

def st_flip_clock():
    """
    極簡修正版：
    1. 移除上下板子：刪除所有 border、padding 與背景容器，讓翻板緊貼文字。
    2. 時區鎖死：改用 toLocaleString 指定時區名稱，解決 offset 失效問題。
    3. 強制刷新：使用 key=time.time() 徹底殺死 Streamlit 緩存。
    """
    flip_html = """
    <style>
        body { background-color: #0e1117; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
        .container { display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%; }

        /* 城市區：移除多餘板塊感 */
        .city-row { display: flex; gap: 10px; cursor: pointer; justify-content: center; }
        .city-card { 
            position: relative; width: 44vw; max-width: 170px; height: 50px; 
            font-family: sans-serif; font-size: 24px; font-weight: 900; color: #fff; text-align: center;
        }

        /* 時間區：移除 '時' '分' 標籤與所有 unit-group 容器 */
        .clock-row { display: flex; gap: 5px; align-items: center; perspective: 1000px; justify-content: center; }
        .flip-card { 
            position: relative; width: 22vw; max-width: 85px; height: 100px; 
            font-family: "Arial Black", sans-serif; font-size: 80px; font-weight: 900; color: #e0e0e0; 
        }

        /* 切割核心：移除所有 border 與多餘的 background-color */
        .top, .bottom, .leaf-front, .leaf-back {
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; /* 僅在文字區塊顯示深色 */
            display: flex; justify-content: center;
        }
        
        /* 移除所有邊框線，避免視覺上多出一塊板子 */
        .top, .leaf-front { top: 0; border-radius: 6px 6px 0 0; align-items: flex-end; }
        .bottom, .leaf-back { bottom: 0; border-radius: 0 0 6px 6px; align-items: flex-start; }

        /* 文字精確位移：讓文字上下切分，不留垂直空隙 */
        .top span, .leaf-front span { transform: translateY(50%); }
        .bottom span, .leaf-back span { transform: translateY(-50%); }

        .leaf { position: absolute; top: 0; left: 0; width: 100%; height: 50%; z-index: 10; transform-origin: bottom; transition: transform 0.6s; transform-style: preserve-3d; }
        .leaf-back { transform: rotateX(-180deg); }
        .flipping .leaf { transform: rotateX(-180deg); }
        
        /* 轉軸設為透明或極細，消除「板子感」 */
        .hinge { position: absolute; top: 50%; width: 100%; height: 1px; background: rgba(0,0,0,0.5); z-index: 20; }
    </style>

    <div class="container">
        <div class="city-row" onclick="nextCity()">
            <div class="city-card" id="c_cn"></div>
            <div class="city-card" id="c_en"></div>
        </div>
        <div class="clock-row" id="main_clock"></div>
    </div>

    <script>
        // 使用具體時區名稱，確保手機端 Intl 引擎能正確轉換
        const cities = [
            { cn: "臺 北", en: "Taipei", tz: "Asia/Taipei" },
            { cn: "東 京", en: "Tokyo", tz: "Asia/Tokyo" },
            { cn: "倫 敦", en: "London", tz: "Europe/London" },
            { cn: "紐 約", en: "New York", tz: "America/New_York" },
            { cn: "洛 杉 磯", en: "L.A.", tz: "America/Los_Angeles" }
        ];

        let idx = 0, lastTime = "";

        function buildCard(val, old) {
            return `
                <div class="flip-card ${val!==old?'flipping':''}">
                    <div class="top"><span>${val}</span></div>
                    <div class="bottom"><span>${old}</span></div>
                    <div class="leaf">
                        <div class="leaf-front"><span>${old}</span></div>
                        <div class="leaf-back"><span>${val}</span></div>
                    </div>
                    <div class="hinge"></div>
                </div>`;
        }

        function nextCity() { idx = (idx + 1) % cities.length; lastTime = ""; tick(); }

        function tick() {
            const city = cities[idx];
            // 使用 toLocaleString 強制轉換時區，解決「時區沒作用」
            const timeParts = new Date().toLocaleString("en-US", {timeZone: city.tz, hour12: false}).split(", ")[1].split(":");
            const h = timeParts[0].padStart(2, '0');
            const m = timeParts[1].padStart(2, '0');
            const str = h + m;

            document.getElementById('c_cn').innerText = city.cn;
            document.getElementById('c_en').innerText = city.en;

            // 只有當時間字串改變時才重繪，避免閃爍
            if (str !== lastTime) {
                let html = "";
                for(let i=0; i<4; i++) {
                    html += buildCard(str[i], lastTime[i] || str[i]);
                    if(i===1) html += '<div style="font-size:40px;color:#444;font-weight:bold;margin:0 4px;">:</div>';
                }
                document.getElementById('main_clock').innerHTML = html;
                lastTime = str;
            }
        }
        setInterval(tick, 1000); tick();
    </script>
    """
    # 這裡的 key=time.time() 是解決「完全沒變化」的關鍵
    return components.html(flip_html, height=350, key=f"v_fix_{time.time()}")
