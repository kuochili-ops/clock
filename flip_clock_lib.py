import streamlit as st
import streamlit.components.v1 as components
import base64
import os

def st_flip_board(text="HELLO", stay_sec=3.0, image_path=None):
    """
    將翻板訊息板封裝為模組。
    解決問題：移除所有外圍邊框、容器背景與標籤，杜絕「多出板子」的視覺感。
    """
    # 處理圖片
    img_data = ""
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
            img_data = f"data:image/png;base64,{img_b64}"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        /* 1. 徹底背景透明化，移除所有外圍視覺干擾 */
        body {{ 
            background: transparent; 
            margin: 0; padding: 0; overflow: hidden;
            display: flex; justify-content: center; align-items: center;
            font-family: sans-serif;
        }}
        
        /* 2. 移除 .acrylic-board 的背景、邊框與陰影，解決「底板多出來」的問題 */
        .main-container {{
            display: inline-flex; flex-direction: column; align-items: center; gap: 10px;
        }}

        .row-container {{ display: flex; gap: 4px; perspective: 1500px; }}

        .flip-card {{
            position: relative; background: #222; color: #e0e0e0;
            text-align: center; font-weight: 900; border-radius: 4px;
        }}

        /* 3. 移除 border，只留中間一條 hinge 黑線，解決「多出板子」的視覺線條 */
        .top, .bottom, .leaf-front, .leaf-back {{
            position: absolute; left: 0; width: 100%; height: 50%;
            overflow: hidden; background: #222; border: none !important; 
        }}
        
        .top, .leaf-front {{ top: 0; border-radius: 4px 4px 0 0; line-height: var(--h); }}
        .bottom, .leaf-back {{ bottom: 0; border-radius: 0 0 4px 4px; line-height: 0px; }}

        .leaf {{
            position: absolute; top: 0; left: 0; width: 100%; height: 50%;
            z-index: 10; transform-origin: bottom; transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .leaf-back {{ transform: rotateX(-180deg); background: #1a1a1a; }}
        .flipping .leaf {{ transform: rotateX(-180deg); }}

        /* 中間轉軸：設為極細黑線 */
        .hinge {{
            position: absolute; top: 50%; left: 0; width: 100%; height: 1px;
            background: #000; z-index: 20; transform: translateY(-50%);
        }}

        /* 尺寸定義 */
        .msg-unit {{ --w: var(--msg-w); --h: calc(var(--msg-w) * 1.5); --fs: calc(var(--msg-w) * 1.1); width: var(--w); height: var(--h); font-size: var(--fs); }}
        .small-unit {{ --w: 30px; --h: 42px; --fs: 26px; width: var(--w); height: var(--h); font-size: var(--fs); }}
    </style>
    </head>
    <body>
        <div class="main-container">
            <div id="row-msg" class="row-container"></div>
            <div id="row-date" class="row-container"></div>
            <div id="row-clock" class="row-container"></div>
        </div>

    <script>
        const fullText = "{text}".toUpperCase();
        const flapCount = Math.min(10, Math.floor(fullText.length / 2) || 6);
        let prevMsg = [], prevDate = [], prevTime = [];

        function updateDigit(el, nv, ov) {{
            if (nv === ov && el.innerHTML !== "") return;
            el.innerHTML = `
                <div class="top">${{nv}}</div>
                <div class="bottom">${{ov}}</div>
                <div class="leaf">
                    <div class="leaf-front">${{ov}}</div>
                    <div class="leaf-back">${{nv}}</div>
                </div>
                <div class="hinge"></div>
            `;
            el.classList.remove('flipping');
            void el.offsetWidth;
            el.classList.add('flipping');
        }

        function init() {{
            const vw = window.innerWidth;
            const msgW = Math.min(60, Math.floor((vw * 0.9) / flapCount));
            document.documentElement.style.setProperty('--msg-w', msgW + 'px');
            
            document.getElementById('row-msg').innerHTML = Array.from({{length: flapCount}}, (_, i) => `<div class="flip-card msg-unit" id="m${{i}}"></div>`).join('');
            document.getElementById('row-date').innerHTML = Array.from({{length: 7}}, (_, i) => `<div class="flip-card small-unit" id="d${{i}}"></div>`).join('');
            document.getElementById('row-clock').innerHTML = Array.from({{length: 8}}, (_, i) => `<div class="flip-card small-unit" id="t${{i}}"></div>`).join('');
        }}

        function tick() {{
            const n = new Date();
            const dStr = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"][n.getMonth()] + String(n.getDate()).padStart(2,'0') + " " + ["日","一","二","三","四","五","六"][n.getDay()];
            const tStr = String(n.getHours()).padStart(2,'0') + ":" + String(n.getMinutes()).padStart(2,'0') + ":" + String(n.getSeconds()).padStart(2,'0');

            dStr.split('').forEach((c, i) => {{ 
                const el = document.getElementById(`d${{i}}`);
                if(el) {{ updateDigit(el, c, prevDate[i] || " "); prevDate[i] = c; }}
            }});
            tStr.split('').forEach((c, i) => {{ 
                const el = document.getElementById(`t${{i}}`);
                if(el) {{ updateDigit(el, c, prevTime[i] || " "); prevTime[i] = c; }}
            }});
        }}

        window.onload = () => {{
            init();
            const msgPages = [];
            for (let i = 0; i < fullText.length; i += flapCount) {{
                msgPages.push(fullText.substring(i, i + flapCount).padEnd(flapCount, ' ').split(''));
            }}
            msgPages[0].forEach((c, i) => {{ 
                const el = document.getElementById(`m${{i}}`);
                if(el) {{ updateDigit(el, c, " "); prevMsg[i] = c; }}
            }});
            
            tick();
            setInterval(tick, 1000);
            
            if (msgPages.length > 1) {{
                setInterval(() => {{
                    let pIdx = (Math.floor(Date.now() / ({stay_sec} * 1000))) % msgPages.length;
                    msgPages[pIdx].forEach((c, i) => {{ 
                        const el = document.getElementById(`m${{i}}`);
                        if(el && prevMsg[i] !== c) {{
                            updateDigit(el, c, prevMsg[i]); 
                            prevMsg[i] = c; 
                        }}
                    }});
                }}, 1000);
            }}
        }};
    </script>
    </body>
    </html>
    """
    return components.html(html_code, height=350, scrolling=False)
