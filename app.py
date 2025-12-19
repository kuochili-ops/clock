import streamlit as st

st.set_page_config(page_title="硬核機械翻板鐘", layout="centered")

flip_html = """
<style>
    body { background-color: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .clock { display: flex; gap: 15px; perspective: 1500px; }

    .flip-unit {
        position: relative;
        width: 100px;
        height: 150px;
        font-family: 'Arial Black', sans-serif;
        font-size: 100px;
        color: white;
        text-align: center;
    }

    /* 底層：新數字上半部 + 舊數字下半部 */
    .static-top {
        position: absolute; top: 0; width: 100%; height: 50%;
        background: #222; border-radius: 8px 8px 0 0;
        overflow: hidden; line-height: 150px;
        z-index: 1; border-bottom: 1px solid #000;
    }
    .static-bottom {
        position: absolute; bottom: 0; width: 100%; height: 50%;
        background: #222; border-radius: 0 0 8px 8px;
        overflow: hidden; line-height: 0px;
        z-index: 0;
    }

    /* 動態翻轉片：舊數字上半部(正) -> 新數字下半部(反) */
    .leaf {
        position: absolute; top: 0; left: 0; width: 100%; height: 50%;
        z-index: 10; transform-origin: bottom;
        transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
    }

    .leaf-front, .leaf-back {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        backface-visibility: hidden; background: #222;
    }
    .leaf-front {
        z-index: 2; border-radius: 8px 8px 0 0; line-height: 150px;
        border-bottom: 1px solid #000;
    }
    .leaf-back {
        transform: rotateX(-180deg); border-radius: 0 0 8px 8px;
        line-height: 0px; z-index: 1; border-top: 1px solid #000;
    }

    /* 動畫狀態：向下翻轉 180 度 */
    .flipping .leaf {
        transform: rotateX(-180deg);
    }

    /* 裝飾線 */
    .hinge {
        position: absolute; top: 50%; width: 100%; height: 4px;
        background: #000; transform: translateY(-50%); z-index: 20;
    }

    .colon { font-size: 60px; color: #555; align-self: center; margin-top: -20px; }
</style>

<div class="clock" id="clock"></div>

<script>
    let lastTime = "";

    function updateClock() {
        const now = new Date();
        const h = now.getHours().toString().padStart(2, '0');
        const m = now.getMinutes().toString().padStart(2, '0');
        const s = now.getSeconds().toString().padStart(2, '0');
        const timeStr = h + m + s;
        
        if (timeStr === lastTime) return;

        const clockEl = document.getElementById('clock');
        let finalHtml = '';

        for (let i = 0; i < timeStr.length; i++) {
            const newVal = timeStr[i];
            const oldVal = lastTime[i] || newVal;
            const isChanged = newVal !== oldVal;

            // 核心物理結構：
            // 1. static-top: 顯示新數字上半部 (等待翻轉片落下)
            // 2. static-bottom: 顯示舊數字下半部 (等待被覆蓋)
            // 3. leaf-front: 舊數字上半部 (開始向下掉)
            // 4. leaf-back: 新數字下半部 (翻過來變正面)
            
            finalHtml += `
                <div class="flip-unit ${isChanged ? 'flipping' : ''}">
                    <div class="static-top">${newVal}</div>
                    <div class="static-bottom">${oldVal}</div>
                    <div class="leaf">
                        <div class="leaf-front">${oldVal}</div>
                        <div class="leaf-back">${newVal}</div>
                    </div>
                    <div class="hinge"></div>
                </div>
            `;
            if (i === 1 || i === 3) finalHtml += '<div class="colon">:</div>';
        }

        clockEl.innerHTML = finalHtml;
        lastTime = timeStr;
    }

    setInterval(updateClock, 1000);
    updateClock();
</script>
"""

st.title("🕰️ 物理重力翻板鐘 (修正版)")
st.markdown("現在您可以清楚看到：**上半部板子像書頁一樣翻下來**。")

st.components.v1.html(flip_html, height=450)
