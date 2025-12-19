import streamlit as st

st.set_page_config(page_title="中文字機械翻板鐘", layout="centered")

flip_chinese_html = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; }
    .clock { display: flex; gap: 15px; perspective: 1500px; }

    .flip-card {
        position: relative;
        width: 120px; /* 中文字較寬，稍微加大 */
        height: 160px;
        font-family: "Microsoft JhengHei", "PMingLiU", sans-serif;
        font-size: 80px; /* 字體縮小一點以容納複雜筆畫 */
        font-weight: 900;
        color: #f0f0f0;
        text-align: center;
        background-color: #222;
        border-radius: 8px;
    }

    /* 靜態底板 */
    .top, .bottom {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; border: 1px solid #111;
    }
    .top { top: 0; border-radius: 8px 8px 0 0; line-height: 160px; border-bottom: 0.5px solid #000; }
    .bottom { bottom: 0; border-radius: 0 0 8px 8px; line-height: 0px; }

    /* 翻轉葉片 */
    .leaf {
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .leaf-front, .leaf-back {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        backface-visibility: hidden; background: #222; overflow: hidden;
    }

    .leaf-front { z-index: 2; border-radius: 8px 8px 0 0; line-height: 160px; border-bottom: 0.5px solid #000; }
    .leaf-back { 
        transform: rotateX(-180deg); border-radius: 0 0 8px 8px; 
        line-height: 0px; border-top: 0.5px solid #000;
        background: linear-gradient(to top, #222 50%, #111 100%);
    }

    .flipping .leaf { transform: rotateX(-180deg); }
    .hinge { position: absolute; top: 50%; left: 0; width: 100%; height: 3px; background: #000; z-index: 15; transform: translateY(-50%); }
    .unit-text { font-size: 30px; color: #666; align-self: flex-end; padding-bottom: 20px; }
</style>

<div class="clock" id="clock"></div>

<script>
    let prevTime = ["", "", ""]; // 儲存時、分、秒

    function toChinese(num) {
        const charMap = ["零", "壹", "貳", "參", "肆", "伍", "陸", "柒", "捌", "玖"];
        let s = num.toString().padStart(2, '0');
        return [charMap[parseInt(s[0])], charMap[parseInt(s[1])]];
    }

    function updateGroup(startIdx, newValStr, oldValStr) {
        for (let i = 0; i < 2; i++) {
            const id = `d${startIdx + i}`;
            const nv = newValStr[i];
            const ov = oldValStr[i] || nv;
            const el = document.getElementById(id);
            
            if (nv === ov && el.innerHTML !== "") continue;

            el.innerHTML = `
                <div class="top static">${nv}</div>
                <div class="bottom static">${ov}</div>
                <div class="leaf">
                    <div class="leaf-front">${ov}</div>
                    <div class="leaf-back">${nv}</div>
                </div>
                <div class="hinge"></div>
            `;
            el.classList.remove('flipping');
            void el.offsetWidth;
            el.classList.add('flipping');
        }
    }

    function tick() {
        const now = new Date();
        const h = now.getHours().toString().padStart(2, '0');
        const m = now.getMinutes().toString().padStart(2, '0');
        const s = now.getSeconds().toString().padStart(2, '0');
        const currentTime = [h, m, s];

        if (prevTime[0] === "") {
            const clockEl = document.getElementById('clock');
            clockEl.innerHTML = `
                <div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div><div class="unit-text">時</div>
                <div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div><div class="unit-text">分</div>
                <div class="flip-card" id="d4"></div><div class="flip-card" id="d5"></div><div class="unit-text">秒</div>
            `;
        }

        updateGroup(0, h, prevTime[0]);
        updateGroup(2, m, prevTime[1]);
        updateGroup(4, s, prevTime[2]);
        
        prevTime = currentTime;
    }

    setInterval(tick, 1000);
    tick();
</script>
"""

st.title("🕰️ 繁體中文翻板鐘")
st.markdown("將「壹貳參肆」等中文字融入機械翻板結構。")
st.components.v1.html(flip_chinese_html, height=500)
