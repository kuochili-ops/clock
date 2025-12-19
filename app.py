import streamlit as st

st.set_page_config(page_title="大寫中文翻板鐘", layout="centered")

flip_chinese_logic = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .clock { display: flex; gap: 15px; perspective: 1500px; }

    .flip-card {
        position: relative;
        width: 120px; /* 中文字稍微寬一點比較美觀 */
        height: 160px;
        font-family: "Microsoft JhengHei", "PingFang TC", sans-serif;
        font-size: 85px;
        font-weight: 900;
        color: #e0e0e0;
        text-align: center;
    }

    /* 靜態底板 */
    .top, .bottom {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; border: 1px solid #111;
    }
    .top { top: 0; border-radius: 8px 8px 0 0; line-height: 160px; border-bottom: 1px solid #000; }
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

    .leaf-front { z-index: 2; border-radius: 8px 8px 0 0; line-height: 160px; border-bottom: 1px solid #000; }
    .leaf-back { 
        transform: rotateX(-180deg); border-radius: 0 0 8px 8px; 
        line-height: 0px; border-top: 1px solid #000;
        background: linear-gradient(to top, #222 50%, #1a1a1a 100%);
    }

    .flipping .leaf { transform: rotateX(-180deg); }

    /* 中軸機械線 */
    .hinge {
        position: absolute; top: 50%; left: 0; width: 100%; height: 3px;
        background: #000; z-index: 20; transform: translateY(-50%);
    }

    .label { font-size: 24px; color: #444; align-self: flex-end; padding-bottom: 15px; font-weight: bold; }
</style>

<div class="clock" id="clock"></div>

<script>
    let prevTime = ["", "", ""];
    const charMap = ["零", "壹", "貳", "參", "肆", "伍", "陸", "柒", "捌", "玖"];

    function getChinese(valStr) {
        // 將 "16" 拆解為 ["壹", "陸"]
        return [charMap[parseInt(valStr[0])], charMap[parseInt(valStr[1])]];
    }

    function updateDigitPair(startIndex, newValStr, oldValStr) {
        const newChars = getChinese(newValStr);
        const oldChars = oldValStr ? getChinese(oldValStr) : newChars;

        for (let i = 0; i < 2; i++) {
            const id = `d${startIndex + i}`;
            const nv = newChars[i];
            const ov = oldChars[i];
            const el = document.getElementById(id);

            if (nv === ov && el.innerHTML !== "") continue;

            el.innerHTML = `
                <div class="top">${nv}</div>
                <div class="bottom">${ov}</div>
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

        if (prevTime[0] === "") {
            document.getElementById('clock').innerHTML = `
                <div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div><div class="label">時</div>
                <div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div><div class="label">分</div>
                <div class="flip-card" id="d4"></div><div class="flip-card" id="d5"></div><div class="label">秒</div>
            `;
        }

        updateDigitPair(0, h, prevTime[0]);
        updateDigitPair(2, m, prevTime[1]);
        updateDigitPair(4, s, prevTime[2]);
        prevTime = [h, m, s];
    }

    setInterval(tick, 1000);
    tick();
</script>
"""

st.title("🕰️ 繁體中文機械翻板鐘")
st.markdown("當「壹、貳、參」遇上 3D 物理翻轉技術。")

st.components.v1.html(flip_chinese_logic, height=500)
