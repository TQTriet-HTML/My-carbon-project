import streamlit as st
import streamlit.components.v1 as components

def get_mission_animation_html(lang="Tiếng Việt"):
    is_en = (lang == "English")
    
    cap_1 = "1. SƠ KHAI: Những cánh rừng nguyên sinh bạt ngàn nuôi dưỡng hành tinh xanh..." if not is_en else "1. PRIMORDIAL: Ancient primeval forests breathing life into the green planet..."
    cap_2 = "2. CÔNG NGHIỆP HÓA: Nhà máy mọc lên, xả khói khí nhà kính gây ô nhiễm môi trường..." if not is_en else "2. INDUSTRIALIZATION: Factories emerge, emitting greenhouse gases and polluting the atmosphere..."
    cap_3 = "3. TÍN CHỈ CARBON: Cầu nối cân bằng giúp bảo vệ môi trường mà không cản trở công nghiệp..." if not is_en else "3. CARBON CREDITS: The balancing bridge ensuring conservation without halting industrial growth..."
    cap_4 = "4. PHÁT TRIỂN BỀN VỮNG: Thu phóng hành tinh xanh – Nơi thiên nhiên & con người hòa hợp trọn vẹn..." if not is_en else "4. SUSTAINABILITY: Zooming out to our Green Earth – Where humanity & nature coexist in harmony..."
    slogan = "MỘT CÚ CHẠM - VẠN ĐIỀU XANH" if not is_en else "ONE TOUCH - ONE GREEN WORLD"
    sub_slogan = "NỀN TẢNG KIỂM KÊ MRV & SÀN TÍN CHỈ CARBON" if not is_en else "MRV SPATIAL PLATFORM & CARBON CREDIT EXCHANGE"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
        body {{
            background: #060b13;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .player-wrapper {{
            position: relative;
            width: 100%;
            max-width: 760px;
            height: 500px;
            background: #080e1a;
            border-radius: 16px;
            border: 2px solid rgba(72, 187, 120, 0.45);
            box-shadow: 0 0 35px rgba(0, 0, 0, 0.9);
            overflow: hidden;
        }}
        canvas {{
            display: block;
            width: 100%;
            height: 100%;
        }}
        .story-badge {{
            position: absolute;
            top: 20px;
            left: 25px;
            right: 25px;
            text-align: center;
            font-size: 14px;
            font-weight: 700;
            color: #48bb78;
            background: rgba(10, 16, 29, 0.88);
            border: 1px solid rgba(72, 187, 120, 0.4);
            border-radius: 10px;
            padding: 10px 18px;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
            letter-spacing: 0.5px;
            transition: all 0.5s ease;
            z-index: 10;
        }}

        /* HIỆU ỨNG SÓNG CHỮ NHẤP NHÔ VÀ TỎA SÁNG XANH LÁ MỖI 4 GIÂY */
        .slogan-box {{
            position: absolute;
            bottom: 45px;
            left: 0;
            width: 100%;
            text-align: center;
            opacity: 0;
            transition: opacity 1s ease;
            pointer-events: none;
            z-index: 15;
        }}
        @keyframes charWave4s {{
            0%, 25%, 100% {{ transform: translateY(0); color: #48bb78; text-shadow: 0 0 10px rgba(72,187,120,0.4); }}
            12% {{ transform: translateY(-10px); color: #86efac; text-shadow: 0 0 25px rgba(72,187,120,1), 0 0 8px rgba(255,255,255,0.9); }}
        }}
        .wave-slogan-char {{
            display: inline-block;
            font-size: 23px;
            font-weight: 900;
            letter-spacing: 2px;
            animation: charWave4s 4s infinite ease-in-out;
        }}
        .sub-slogan-text {{
            font-size: 12.5px;
            font-weight: 600;
            color: #94a3b8;
            margin-top: 6px;
            letter-spacing: 1px;
        }}
    </style>
    </head>
    <body>

    <div class="player-wrapper">
        <div class="story-badge" id="storyBadge">{cap_1}</div>
        <canvas id="animCanvas" width="760" height="500"></canvas>
        <div class="slogan-box" id="sloganBox">
            <div id="waveContainer"></div>
            <div class="sub-slogan-text">{sub_slogan}</div>
        </div>
    </div>

    <script>
    const canvas = document.getElementById('animCanvas');
    const ctx = canvas.getContext('2d');
    const badge = document.getElementById('storyBadge');
    const sloganBox = document.getElementById('sloganBox');
    const waveContainer = document.getElementById('waveContainer');

    const captions = [
        "{cap_1}",
        "{cap_2}",
        "{cap_3}",
        "{cap_4}"
    ];
    const slogan = "{slogan}";

    // Tạo các phần tử chữ cho hiệu ứng sóng 4s
    let waveHtml = "";
    let delay = 0.0;
    for(let char of slogan) {{
        let c = char === " " ? "&nbsp;" : char;
        waveHtml += `<span class="wave-slogan-char" style="animation-delay: ${{delay.toFixed(2)}}s;">${{c}}</span>`;
        delay += 0.08;
    }}
    waveContainer.innerHTML = waveHtml;

    let startTime = performance.now();
    const TOTAL_DURATION = 23000; // 23 giây tổng hành trình rồi thoát

    let smokeParticles = [];
    let carbonParticles = [];
    for(let i=0; i<40; i++) {{
        smokeParticles.push({{
            x: 645,
            y: 215,
            r: 7 + Math.random() * 10,
            vx: (Math.random() - 0.5) * 0.9,
            vy: -1.2 - Math.random() * 1.6
        }});
    }}
    for(let i=0; i<50; i++) {{
        carbonParticles.push({{
            x: 100 + Math.random() * 560,
            y: 150 + Math.random() * 200,
            r: 2 + Math.random() * 3,
            vx: (Math.random() - 0.5) * 1.5,
            vy: -0.6 - Math.random() * 1.2
        }});
    }}

    let closedTriggered = false;

    function draw() {{
        const now = performance.now();
        let elapsed = now - startTime;

        // KHI KẾT THÚC ĐOẠN SỨ MỆNH: ĐÓNG DIALOG QUAY VỀ ĐĂNG NHẬP
        if (elapsed >= TOTAL_DURATION && !closedTriggered) {{
            closedTriggered = true;
            // Gửi sự kiện đóng dialog ra cửa sổ cha
            try {{
                window.parent.postMessage({{ type: "streamlit:setComponentValue", value: "CLOSE_MISSION" }}, "*");
                const closeBtn = window.parent.document.querySelector('button[aria-label="Close"]');
                if (closeBtn) closeBtn.click();
            }} catch(e) {{}}
            return;
        }}

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (elapsed < 5500) {{
            badge.innerText = captions[0];
            badge.style.color = "#48bb78";
            badge.style.borderColor = "rgba(72, 187, 120, 0.4)";
            sloganBox.style.opacity = "0";
            renderScene(elapsed, 1.0, 0.0, 0.0, 0.0);
        }} else if (elapsed < 11000) {{
            badge.innerText = captions[1];
            badge.style.color = "#f87171";
            badge.style.borderColor = "rgba(248, 113, 113, 0.4)";
            let p = (elapsed - 5500) / 5500;
            renderScene(elapsed, 1.0 - p * 0.4, p, 0.0, 0.0);
        }} else if (elapsed < 16500) {{
            badge.innerText = captions[2];
            badge.style.color = "#38bdf8";
            badge.style.borderColor = "rgba(56, 189, 248, 0.4)";
            let p = (elapsed - 11000) / 5500;
            renderScene(elapsed, 0.6 + p * 0.4, 1.0 - p * 0.3, p, 0.0);
        }} else {{
            badge.innerText = captions[3];
            badge.style.color = "#4ade80";
            badge.style.borderColor = "rgba(74, 222, 128, 0.5)";
            let zoomP = Math.min(1.0, (elapsed - 16500) / 3000);
            sloganBox.style.opacity = zoomP > 0.6 ? "1" : "0";
            renderScene(elapsed, 1.0, 0.7, 1.0, zoomP);
        }}

        requestAnimationFrame(draw);
    }}

    function renderScene(time, forestHealth, industrialLevel, carbonLevel, zoomProgress) {{
        ctx.fillStyle = "#070c16";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Sao trời nền
        if (zoomProgress > 0.05) {{
            ctx.save();
            ctx.globalAlpha = Math.min(1.0, zoomProgress * 1.5);
            for(let s=0; s<40; s++) {{
                let sx = (s * 41) % canvas.width;
                let sy = (s * 67) % canvas.height;
                ctx.fillStyle = "rgba(255, 255, 255, 0.45)";
                ctx.fillRect(sx, sy, 2, 2);
            }}
            ctx.restore();
        }}

        // CAMERA ZOOM-OUT THU PHÓNG ĐIỆN ẢNH
        ctx.save();
        let targetX = canvas.width / 2;
        let targetY = 195;
        let scale = 1.0 - zoomProgress * 0.82;
        let transY = (1.0 - zoomProgress) * 0 + zoomProgress * (targetY - 370 * scale);

        ctx.translate(targetX * (1 - scale), transY);
        ctx.scale(scale, scale);

        if (zoomProgress < 0.98) {{
            ctx.save();
            ctx.globalAlpha = 1.0 - zoomProgress * 0.85;

            // Bầu trời
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 370);
            if (industrialLevel > 0.5 && carbonLevel < 0.5) {{
                skyGrad.addColorStop(0, "#1c1917");
                skyGrad.addColorStop(1, "#362b28");
            }} else {{
                skyGrad.addColorStop(0, "#081b29");
                skyGrad.addColorStop(1, "#0d3b36");
            }}
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, canvas.width, 370);

            // Mặt đất
            ctx.fillStyle = "#111c24";
            ctx.fillRect(0, 370, canvas.width, 130);
            ctx.strokeStyle = forestHealth > 0.5 ? "#22c55e" : "#854d0e";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 370);
            ctx.lineTo(canvas.width, 370);
            ctx.stroke();

            // Rừng cây
            drawTree(70, 370, 0.9 * forestHealth, "#15803d", "#22c55e");
            drawTree(130, 370, 1.2 * forestHealth, "#166534", "#48bb78");
            drawTree(200, 370, 1.0 * forestHealth, "#14532d", "#16a34a");
            drawTree(270, 370, 1.15 * forestHealth, "#15803d", "#34d399");
            drawTree(340, 370, 0.85 * forestHealth, "#166534", "#22c55e");

            // Nhà máy
            if (industrialLevel > 0.05) {{
                ctx.fillStyle = "#334155";
                ctx.fillRect(480, 300, 140, 70);
                ctx.fillStyle = "#475569";
                ctx.beginPath();
                ctx.moveTo(480, 300); ctx.lineTo(515, 275); ctx.lineTo(515, 300);
                ctx.lineTo(550, 275); ctx.lineTo(550, 300);
                ctx.lineTo(585, 275); ctx.lineTo(585, 300);
                ctx.lineTo(620, 275); ctx.lineTo(620, 300);
                ctx.fill();
                ctx.fillRect(635, 220, 22, 150);
                ctx.fillRect(670, 245, 18, 125);

                ctx.fillStyle = "#facc15";
                ctx.fillRect(495, 315, 16, 20);
                ctx.fillRect(525, 315, 16, 20);

                if (carbonLevel < 0.8) {{
                    smokeParticles.forEach(p => {{
                        p.y += p.vy;
                        p.x += p.vx;
                        if (p.y < 90) {{ p.y = 215; p.x = 645 + (Math.random()-0.5)*10; }}
                        ctx.beginPath();
                        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                        ctx.fillStyle = "rgba(148, 163, 184, 0.4)";
                        ctx.fill();
                    }});
                }}
            }}

            // Tín chỉ Carbon
            if (carbonLevel > 0.1) {{
                ctx.strokeStyle = "rgba(72, 187, 120, 0.6)";
                ctx.lineWidth = 2;
                ctx.setLineDash([8, 8]);
                ctx.beginPath();
                ctx.moveTo(270, 280);
                ctx.bezierCurveTo(360, 200, 420, 200, 520, 290);
                ctx.stroke();

                carbonParticles.forEach(p => {{
                    p.y += p.vy;
                    p.x += p.vx;
                    if (p.y < 120) {{ p.y = 350; p.x = 100 + Math.random() * 560; }}
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    ctx.fillStyle = "rgba(74, 222, 128, 0.85)";
                    ctx.fill();
                }});
                drawTree(430, 370, 0.8 * carbonLevel, "#15803d", "#48bb78");
                drawTree(710, 370, 0.7 * carbonLevel, "#166534", "#22c55e");
            }}
            ctx.restore();
        }}
        ctx.restore();

        // ĐOẠN CUỐI: TRÁI ĐẤT ĐẠI DƯƠNG XANH TỰ NHIÊN (KHÔNG PHÁT SÁNG CHÓI) + 2 LÁ 45 ĐỘ
        if (zoomProgress > 0.1) {{
            ctx.save();
            ctx.globalAlpha = Math.min(1.0, (zoomProgress - 0.1) / 0.7);
            ctx.translate(canvas.width / 2, 200);

            const R = 72;

            // 1. ĐẠI DƯƠNG XANH BIỂN CHÂN THẬT (KHÔNG DÙNG HÀO QUANG SHADOW CHÓI LÒA)
            ctx.save();
            ctx.beginPath();
            ctx.arc(0, 0, R, 0, Math.PI * 2);
            let oceanGrad = ctx.createRadialGradient(-20, -25, 10, 0, 0, R);
            oceanGrad.addColorStop(0, "#0284c7");   // Xanh biển tươi sáng
            oceanGrad.addColorStop(0.5, "#0369a1"); // Xanh biển sâu
            oceanGrad.addColorStop(0.85, "#075985");
            oceanGrad.addColorStop(1, "#0c4a6e");   // Viền biển tối
            ctx.fillStyle = oceanGrad;
            ctx.fill();
            ctx.clip();

            // 2. CÁC MẢNG LỤC ĐỊA NGẢ XANH LÁ TỰ NHIÊN
            let rot = (time * 0.0003) % (Math.PI * 2);
            ctx.save();
            ctx.rotate(rot * 0.12);

            // Lục địa 1: Á - Âu (Màu xanh ngọc pha chút đất)
            ctx.fillStyle = "#15803d";
            ctx.beginPath();
            ctx.ellipse(10, -18, 36, 26, 0.3, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#16a34a";
            ctx.beginPath();
            ctx.ellipse(20, 8, 22, 28, -0.2, 0, Math.PI * 2);
            ctx.fill();

            // Lục địa 2: Châu Mỹ (Rừng Amazon ngả xanh lá)
            ctx.fillStyle = "#15803d";
            ctx.beginPath();
            ctx.ellipse(-36, -14, 26, 18, -0.3, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#22c55e";
            ctx.beginPath();
            ctx.ellipse(-24, 22, 15, 30, 0.25, 0, Math.PI * 2);
            ctx.fill();

            // Dải mây trắng mỏng tự nhiên
            ctx.fillStyle = "rgba(255, 255, 255, 0.2)";
            ctx.beginPath();
            ctx.ellipse(-8, -28, 42, 7, -0.1, 0, Math.PI * 2);
            ctx.ellipse(8, 30, 46, 8, 0.15, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // Bóng 3D tự nhiên (Tạo độ cong của quả địa cầu)
            let sphereShade = ctx.createRadialGradient(-25, -25, 10, 0, 0, R);
            sphereShade.addColorStop(0, "rgba(255, 255, 255, 0.2)");
            sphereShade.addColorStop(0.7, "rgba(0, 0, 0, 0)");
            sphereShade.addColorStop(1, "rgba(0, 0, 0, 0.6)");
            ctx.fillStyle = sphereShade;
            ctx.fill();

            // Đường viền địa cầu mảnh, tinh tế
            ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
            ctx.lineWidth = 1.5;
            ctx.stroke();
            ctx.restore();

            // 3. HAI CHIẾC LÁ XÒE 45 ĐỘ NÂNG ĐỠ (CÓ GÂN LÁ RÕ NÉT)
            // Lá trái (-45 độ)
            ctx.save();
            ctx.translate(-24, 70);
            ctx.rotate(-Math.PI / 4);
            drawDetailedLeaf();
            ctx.restore();

            // Lá phải (+45 độ)
            ctx.save();
            ctx.translate(24, 70);
            ctx.rotate(Math.PI / 4);
            ctx.scale(-1, 1);
            drawDetailedLeaf();
            ctx.restore();

            ctx.restore();
        }}
    }}

    function drawTree(x, baseY, scale, trunkColor, leafColor) {{
        if (scale <= 0.05) return;
        ctx.save();
        ctx.translate(x, baseY);
        ctx.scale(scale, scale);

        ctx.fillStyle = "#78350f";
        ctx.fillRect(-7, -45, 14, 45);

        ctx.fillStyle = leafColor;
        ctx.beginPath();
        ctx.arc(0, -60, 30, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = trunkColor;
        ctx.beginPath();
        ctx.arc(-10, -75, 24, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = leafColor;
        ctx.beginPath();
        ctx.arc(8, -85, 22, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }}

    function drawDetailedLeaf() {{
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.bezierCurveTo(40, -30, 48, -85, 15, -108);
        ctx.bezierCurveTo(-15, -85, -24, -30, 0, 0);

        let leafGrad = ctx.createLinearGradient(0, 0, 20, -105);
        leafGrad.addColorStop(0, "#15803d");
        leafGrad.addColorStop(0.5, "#22c55e");
        leafGrad.addColorStop(1, "#4ade80");
        ctx.fillStyle = leafGrad;
        ctx.shadowColor = "rgba(34, 197, 94, 0.4)";
        ctx.shadowBlur = 12;
        ctx.fill();

        // Sống lá chính
        ctx.strokeStyle = "rgba(255, 255, 255, 0.7)";
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.quadraticCurveTo(8, -50, 15, -104);
        ctx.stroke();

        // Gân lá nhánh
        ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
        ctx.lineWidth = 1.3;
        ctx.beginPath();
        ctx.moveTo(3, -25); ctx.lineTo(18, -36);
        ctx.moveTo(6, -48); ctx.lineTo(24, -60);
        ctx.moveTo(10, -72); ctx.lineTo(23, -82);
        ctx.moveTo(3, -25); ctx.lineTo(-10, -32);
        ctx.moveTo(6, -48); ctx.lineTo(-8, -56);
        ctx.moveTo(10, -72); ctx.lineTo(0, -78);
        ctx.stroke();
    }}

    requestAnimationFrame(draw);
    </script>
    </body>
    </html>
    """

@st.dialog("HÀNH TRÌNH SỨ MỆNH & PHÁT TRIỂN BỀN VỮNG", width="large")
def hien_thi_hop_thoai_su_menh():
    current_lang = st.session_state.get("current_lang", "Tiếng Việt")
    html_code = get_mission_animation_html(current_lang)
    components.html(html_code, height=520, scrolling=False)
    
    col_l, col_r = st.columns([0.7, 0.3])
    with col_r:
        btn_close_lbl = "ĐÓNG & TIẾP TỤC ĐĂNG NHẬP" if current_lang == "Tiếng Việt" else "CLOSE & CONTINUE TO LOGIN"
        if st.button(btn_close_lbl, use_container_width=True, type="secondary"):
            st.rerun()
