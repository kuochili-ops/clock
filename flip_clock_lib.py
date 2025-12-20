import streamlit as st
import streamlit.components.v1 as components
import time

def st_chinese_flip_clock():
    """
    繁體中文大寫翻板鐘模組：
    1. 解決多出板子：移除所有 .top/.bottom 的 border 與 unit-group 容器。
    2. 文字校準：改用 translateY 位移文字，不依賴 line-height，確保物理切割乾淨。
    3. 自動換行：支援手機端自動排列，不會產生水平捲軸。
    """
    flip_html = f"""
    <style>
        body {{ background-color: #0e1117; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; overflow: hidden; }}
        .clock {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; perspective: 1500px; width: 100%; }}
        
        /* 移除 unit-group 的背景與標籤，只保留翻板 */
        .unit-group {{ display: flex; gap: 5px; align-items: center; }}

        .flip-card {{
            position: relative; width: 18vw; max-width: 80px; height: 25vw; max-height: 110px;
            font-family: "Microsoft JhengHei", sans-serif; font-size: 14vw; max-font-size: 65px;
            font-weight: 900; color: #e0e0e0; text-align: center;
        }}
        @media (min-width: 600px) {{ .flip-card {{ width: 100px; height: 140px; font-size: 70px; }} }}

        /* 核心修正：移除 border (解決多出板子感)，改用 translateY 對齊 */
        .top, .bottom, .leaf-front, .leaf-back {{
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; display: flex; justify-content: center;
        }}
        .top, .leaf-front {{ top: 0; border-radius: 8px 8px 0 0; align-items: flex-end; border-bottom: 0.5px solid #000; }}
        .bottom, .leaf-back {{ bottom: 0; border-radius: 0 0 8px 8px; align-items: flex-start; }}

        /* 文字精確對齊，移除 line-height 帶來的偏移 */
        .top span, .leaf-front span {{ transform: translateY(50%); }}
        .bottom span, .leaf-back span {{ transform: translateY(-50%); }}

        .leaf {{
            position: absolute; top: 0; left: 0; width: 100%; height: 50%;
            z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .leaf-back {{ transform: rotateX(-180deg); background: linear-gradient(to top, #222 50%, #1a1a1a 100%); }}
        .flipping .leaf {{ transform: rotateX(-180deg); }}
        .hinge {{ position: absolute; top: 50%; width: 100%; height: 1px; background: #000; z-index: 20; }}
    </style>

    <div class="clock" id="clock"></div>

    <script>
        let prevTime = ["", "", ""];
        const charMap = ["零", "壹", "貳", "參", "肆", "伍", "陸", "柒", "捌", "玖"];

        function updateDigit(id, nv, ov) {{
            const el = document.getElementById(id);
            if (!el || (nv === ov && el.innerHTML !== "")) return;
            el.innerHTML = `
                <div class="top"><span>${{nv}}</span></div>
                <div class="bottom"><span>${{ov}}</span></div>
                <div class="leaf">
                    <div class="leaf-front"><span>${{ov}}</span></div>
                    <div class="leaf-back"><span>${{nv}}</span></div>
                </div>
                <div class="hinge"></div>
            `;
            el.classList.remove('flipping');
            void el.offsetWidth;
            el.classList.add('flipping');
        }}

        function tick() {{
            const n = new Date();
            const h = n.getHours().toString().padStart(2, '0');
            const m = n.getMinutes().toString().padStart(2, '0');
            const s = n.getSeconds().toString().padStart(2, '0');

            if (prevTime[0] === "") {{
                document.getElementById('clock').innerHTML = `
                    <div class="unit-group"><div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div></div>
                    <div class="unit-group"><div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div></div>
                    <div class="unit-group"><div class="flip-card" id="d4"></div><div class="flip-card" id="d5"></div></div>
                `;
            }}

            const timeStr = h + m + s;
            for(let i=0; i<6; i++) {{
                const nv = charMap[parseInt(timeStr[i])];
                const ov = prevTime.join('')[i] ? charMap[parseInt(prevTime.join('')[i])] : nv;
                updateDigit('d'+i, nv, ov);
            }}
            prevTime = [h, m, s];
        }
        setInterval(tick, 1000); tick();
    </script>
    """
    return components.html(flip_html, height=450, key=f"cn_flip_{time.time()}")
