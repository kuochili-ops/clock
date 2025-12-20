#import streamlit as st
#from flip_clock_lib import st_flip_clock

#st.title("🌏 全球城市翻板鐘")
#st_flip_clock()
一樣的問題
以下程式妳改過版面，翻板運作沒問題
import streamlit as st

st.set_page_config(page_title="大寫中文翻板鐘", layout="centered")

# 根據您先前的要求，我們將此邏輯保留並封裝
flip_chinese_logic = """
<style>
    body { 
        background-color: #0e1117; 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        min-height: 100vh; 
        margin: 0; 
        padding: 10px;
    }
    
    .clock { 
        display: flex; 
        gap: 10px; 
        perspective: 1500px; 
        flex-wrap: wrap; /* 關鍵：寬度不夠時自動換行 */
        justify-content: center;
        align-items: center;
        width: 100%;
    }

    /* 響應式卡片尺寸：手機端會自動縮小 */
    .flip-card {
        position: relative;
        width: 18vw;   /* 使用寬度百分比單位 */
        max-width: 80px; 
        height: 25vw;
        max-height: 110px;
        font-family: "Microsoft JhengHei", "PingFang TC", sans-serif;
        font-size: 14vw; /* 字體大小隨寬度縮放 */
        max-font-size: 65px;
        font-weight: 900;
        color: #e0e0e0;
        text-align: center;
    }
    
    /* 桌面端大螢幕微調 */
    @media (min-width: 600px) {
        .flip-card {
            width: 100px;
            height: 140px;
            font-size: 70px;
        }
    }

    /* 靜態底板 */
    .top, .bottom {
        position: absolute; left: 0; width: 100%; height: 50%;
        overflow: hidden; background: #222; border: 1px solid #111;
    }
    .top { 
        top: 0; border-radius: 8px 8px 0 0; 
        line-height: 25vw; /* 需與 height 對齊 */
        border-bottom: 1px solid #000; 
    }
    @media (min-width: 600px) { .top { line-height: 140px; } }

    .bottom { 
        bottom: 0; border-radius: 0 0 8px 8px; 
        line-height: 0px; 
    }

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

    .leaf-front { 
        z-index: 2; border-radius: 8px 8px 0 0; 
        line-height: 25vw; 
        border-bottom: 1px solid #000; 
    }
    @media (min-width: 600px) { .leaf-front { line-height: 140px; } }

    .leaf-back { 
        transform: rotateX(-180deg); border-radius: 0 0 8px 8px; 
        line-height: 0px; border-top: 1px solid #000;
        background: linear-gradient(to top, #222 50%, #1a1a1a 100%);
    }

    .flipping .leaf { transform: rotateX(-180deg); }

    .hinge {
        position: absolute; top: 50%; left: 0; width: 100%; height: 2px;
        background: #000; z-index: 20; transform: translateY(-50%);
    }

    .label { 
        font-size: 18px; 
        color: #888; 
        align-self: flex-end; 
        padding-bottom: 5px; 
        font-weight: bold;
    }
    
    /* 每組時分秒在手機上保持在一起 */
    .unit-group {
        display: flex;
        gap: 5px;
        align-items: center;
    }
</style>

<div class="clock" id="clock"></div>

<script>
    let prevTime = ["", "", ""];
    const charMap = ["零", "壹", "貳", "參", "肆", "伍", "陸", "柒", "捌", "玖"];

    function getChinese(valStr) {
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
                <div class="unit-group">
                    <div class="flip-card" id="d0"></div><div class="flip-card" id="d1"></div><div class="label">時</div>
                </div>
                <div class="unit-group">
                    <div class="flip-card" id="d2"></div><div class="flip-card" id="d3"></div><div class="label">分</div>
                </div>
                <div class="unit-group">
                    <div class="flip-card" id="d4"></div><div class="flip-card" id="d5"></div><div class="label">秒</div>
                </div>
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

st.title("🕰️ 繁體中文翻板鐘")
st.markdown("已優化手機直式瀏覽，支援自動換行與縮放。")

# 增加高度以容納手機端換行後的高度
st.components.v1.html(flip_chinese_logic, height=450)
