import streamlit as st
import streamlit.components.v1 as components

def get_mission_animation_html(lang="Tiếng Việt"):
    is_en = (lang == "English")
    
    cap_1 = "1. KHỞI NGUYÊN: Những cánh rừng nguyên sinh bạt ngàn nuôi dưỡng hành tinh xanh" if not is_en else "1. PRIMORDIAL: Ancient primeval forests breathing life into our green planet"
    cap_2 = "2. CÔNG NGHIỆP HÓA: Nhà máy mọc lên, xả khói khí nhà kính gây ô nhiễm môi trường" if not is_en else "2. INDUSTRIALIZATION: Factories emerge, emitting greenhouse gases and polluting nature"
    cap_3 = "3. TÍN CHỈ CARBON: Cầu nối cân bằng kinh tế và tái tạo rừng mà không kìm hãm công nghiệp" if not is_en else "3. CARBON CREDITS: Balancing economic growth and forest restoration sustainably"
    cap_4 = "4. PHÁT TRIỂN BỀN VỮNG: Con người và Trái Đất xanh cùng chung sống hòa hợp trọn vẹn" if not is_en else "4. SUSTAINABILITY: Humanity and our Living Earth coexisting in joyful harmony"
    slogan = "MỘT CÚ CHẠM - VẠN ĐIỀU XANH" if not is_en else "ONE TOUCH - ONE GREEN WORLD"
    mission_2050 = "Phấn đấu tới năm 2050 phủ sạch tín chỉ carbon toàn cầu là nhiệm vụ tất yếu của nền tảng" if not is_en else "Striving for global net-zero carbon coverage by 2050 is our core mission"

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
            top: 18px;
            left: 20px;
            right: 20px;
            text-align: center;
            font-size: 13.5px;
            font-weight: 700;
            color: #48bb78;
            background: rgba(10, 16, 29, 0.9);
            border: 1px solid rgba(72, 187, 120, 0.4);
            border-radius: 10px;
            padding: 9px 15px;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
            letter-spacing: 0.3px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            z-index: 10;
        }}

        /* KHỐI SLOGAN & SỨ MỆNH 2050 ĐƯỢC KÉO GẦN LẠI LOGO */
        .slogan-box {{
            position: absolute;
            bottom: 22px;
            left: 0;
            width: 100%;
            text-align: center;
            opacity: 0;
            transition: opacity 1s ease;
            pointer-events: none;
            z-index: 15;
        }}
        @keyframes waveChar4s {{
            0%, 25%, 100% {{ transform: translateY(0); color: #48bb78; text-shadow: 0 0 10px rgba(72,187,120,0.4); }}
            12% {{ transform: translateY(-7px); color: #86efac; text-shadow: 0 0 25px rgba(72,187,120,1), 0 0 8px rgba(255,255,255,0.9); }}
        }}
        .wave-slogan-char {{
            display: inline-block;
            font-size: 21px;
            font-weight: 900;
            letter-spacing: 2px;
            animation: waveChar4s 4s infinite ease-in-out;
        }}
        .mission-2050-text {{
            font-size: 12px;
            font-weight: 600;
            color: #94a3b8;
            margin-top: 6px;
            letter-spacing: 0.5px;
            max-width: 90%;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.4;
        }}
        .mission-2050-text b {{
            color: #38bdf8;
            font-weight: 800;
        }}
    </style>
    </head>
    <body>

    <div class="player-wrapper">
        <div class="story-badge" id="storyBadge">{cap_1}</div>
        <canvas id="animCanvas" width="760" height="500"></canvas>
        <div class="slogan-box" id="sloganBox">
            <div id="waveContainer"></div>
            <div class="mission-2050-text">{mission_2050}</div>
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

    let waveHtml = "";
    let delay = 0.0;
    for(let char of slogan) {{
        let c = char === " " ? "&nbsp;" : char;
        waveHtml += `<span class="wave-slogan-char" style="animation-delay: ${{delay.toFixed(2)}}s;">${{c}}</span>`;
        delay += 0.08;
    }}
    waveContainer.innerHTML = waveHtml;

    let startTime = performance.now();
    const TOTAL_DURATION = 25000; // 25 giây tổng thời lượng

    let smokeParticles = [];
    let carbonParticles = [];
    for(let i=0; i<35; i++) {{
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

        if (elapsed >= TOTAL_DURATION && !closedTriggered) {{
            closedTriggered = true;
            try {{
                window.parent.postMessage({{ type: "streamlit:setComponentValue", value: "CLOSE_MISSION" }}, "*");
                const closeBtn = window.parent.document.querySelector('button[aria-label="Close"]');
                if (closeBtn) closeBtn.click();
            }} catch(e) {{}}
            return;
        }}

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (elapsed < 6000) {{
            badge.innerText = captions[0];
            badge.style.color = "#48bb78";
            badge.style.borderColor = "rgba(72, 187, 120, 0.4)";
            sloganBox.style.opacity = "0";
            renderScene(elapsed, 1.0, 0.0, 0.0, 0.0);
        }} else if (elapsed < 12000) {{
            badge.innerText = captions[1];
            badge.style.color = "#f87171";
            badge.style.borderColor = "rgba(248, 113, 113, 0.4)";
            let p = (elapsed - 6000) / 6000;
            renderScene(elapsed, 1.0 - p * 0.4, p, 0.0, 0.0);
        }} else if (elapsed < 17500) {{
            badge.innerText = captions[2];
            badge.style.color = "#38bdf8";
            badge.style.borderColor = "rgba(56, 189, 248, 0.4)";
            let p = (elapsed - 12000) / 5500;
            renderScene(elapsed, 0.6 + p * 0.4, 1.0 - p * 0.3, p, 0.0);
        }} else {{
            badge.innerText = captions[3];
            badge.style.color = "#4ade80";
            badge.style.borderColor = "rgba(74, 222, 128, 0.5)";
            let zoomP = Math.min(1.0, (elapsed - 17500) / 3500);
            sloganBox.style.opacity = zoomP > 0.6 ? "1" : "0";
            renderScene(elapsed, 1.0, 0.7, 1.0, zoomP);
        }}

        requestAnimationFrame(draw);
    }}

    function renderScene(time, forestHealth, industrialLevel, carbonLevel, zoomProgress) {{
        ctx.fillStyle = "#070c16";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // THU PHÓNG ZOOM-OUT: Đưa tâm đích thấp xuống để logo và slogan gần nhau
        ctx.save();
        let targetX = canvas.width / 2;
        let targetY = 225; // Hạ thấp vị trí đích để thu hẹp khoảng cách với slogan
        let scale = 1.0 - zoomProgress * 0.85;
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

            // Mặt trời
            ctx.beginPath();
            ctx.arc(140, 110, 38, 0, Math.PI * 2);
            let sunGrad = ctx.createRadialGradient(140, 110, 10, 140, 110, 38);
            sunGrad.addColorStop(0, "rgba(74, 222, 128, 0.8)");
            sunGrad.addColorStop(1, "rgba(56, 189, 248, 0)");
            ctx.fillStyle = sunGrad;
            ctx.fill();

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

        // KHI KẾT THÚC: LOGO VÀ SLOGAN GẮN BÓ GẦN NHAU
        if (zoomProgress > 0.1) {{
            ctx.save();
            ctx.globalAlpha = Math.min(1.0, (zoomProgress - 0.1) / 0.7);
            ctx.translate(canvas.width / 2, 225); // Vị trí tâm logo được hạ gần slogan

            const R = 75;

            // 1. QUẢ ĐỊA CẦU HOẠT HÌNH
            ctx.save();
            ctx.beginPath();
            ctx.arc(0, 0, R, 0, Math.PI * 2);
            ctx.fillStyle = "#7dd3fc";
            ctx.fill();
            ctx.lineWidth = 4;
            ctx.strokeStyle = "#0f172a";
            ctx.stroke();
            ctx.clip();

            // Mảng lục địa
            ctx.fillStyle = "#4ade80";
            ctx.strokeStyle = "#0f172a";
            ctx.lineWidth = 3;

            // Lục địa phía Bắc
            ctx.beginPath();
            ctx.moveTo(-15, -R);
            ctx.bezierCurveTo(-10, -50, 15, -45, 20, -R);
            ctx.closePath();
            ctx.fill(); ctx.stroke();

            // Lục địa góc trên trái
            ctx.beginPath();
            ctx.moveTo(-R, -45);
            ctx.bezierCurveTo(-45, -55, -35, -20, -55, 0);
            ctx.bezierCurveTo(-75, 10, -R, 15, -R, -45);
            ctx.closePath();
            ctx.fill(); ctx.stroke();

            // Lục địa góc dưới trái
            ctx.beginPath();
            ctx.moveTo(-50, 20);
            ctx.bezierCurveTo(-20, 25, -25, 65, -45, 75);
            ctx.bezierCurveTo(-65, 75, -60, 45, -50, 20);
            ctx.closePath();
            ctx.fill(); ctx.stroke();

            // Lục địa bên phải
            ctx.beginPath();
            ctx.moveTo(40, -50);
            ctx.bezierCurveTo(30, -20, 60, -10, 40, 15);
            ctx.bezierCurveTo(30, 35, 60, 45, R, 20);
            ctx.bezierCurveTo(R, -40, 65, -55, 40, -50);
            ctx.closePath();
            ctx.fill(); ctx.stroke();

            // Mảng nước trang trí đáy
            ctx.fillStyle = "#38bdf8";
            ctx.beginPath();
            ctx.ellipse(20, 55, 25, 12, 0, 0, Math.PI * 2);
            ctx.fill();

            // Mắt & Miệng hoạt hình
            ctx.fillStyle = "#0f172a";
            ctx.beginPath();
            ctx.arc(-22, 0, 4.5, 0, Math.PI * 2);
            ctx.arc(22, 0, 4.5, 0, Math.PI * 2);
            ctx.fill();

            ctx.beginPath();
            ctx.arc(0, 8, 7, 0.15 * Math.PI, 0.85 * Math.PI);
            ctx.lineWidth = 3.5;
            ctx.strokeStyle = "#0f172a";
            ctx.lineCap = "round";
            ctx.stroke();

            ctx.fillStyle = "#f87171";
            ctx.beginPath();
            ctx.arc(-36, 15, 6.5, 0, Math.PI * 2);
            ctx.arc(36, 15, 6.5, 0, Math.PI * 2);
            ctx.fill();

            // Điểm sáng phản quang
            ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
            ctx.beginPath();
            ctx.ellipse(-50, -35, 14, 5, -Math.PI / 4, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(-60, -22, 3.5, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();

            // Viền ngoài quả địa cầu
            ctx.beginPath();
            ctx.arc(0, 0, R, 0, Math.PI * 2);
            ctx.lineWidth = 4;
            ctx.strokeStyle = "#0f172a";
            ctx.stroke();

            // 2. MẦM CÂY TRÊN ĐẦU: LÀM RÕ NÉT VỚI MÀU SÁNG, VIỀN ĐẬM VÀ PHẢN QUANG
            ctx.save();
            ctx.translate(0, -R);

            // Thân mầm
            ctx.strokeStyle = "#0f172a";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(0, 0); ctx.lineTo(0, -16);
            ctx.stroke();

            // Lá mầm trái
            ctx.beginPath();
            ctx.ellipse(-12, -20, 11, 7.5, -Math.PI / 5, 0, Math.PI * 2);
            ctx.fillStyle = "#86efac"; // Màu xanh lá non tươi sáng nổi bật trên nền tối
            ctx.fill();
            ctx.lineWidth = 3;
            ctx.strokeStyle = "#0f172a";
            ctx.stroke();

            // Điểm sáng trắng trên lá mầm trái
            ctx.fillStyle = "rgba(255, 255, 255, 0.75)";
            ctx.beginPath();
            ctx.ellipse(-14, -22, 4.5, 2.5, -Math.PI / 5, 0, Math.PI * 2);
            ctx.fill();

            // Lá mầm phải
            ctx.beginPath();
            ctx.ellipse(12, -20, 11, 7.5, Math.PI / 5, 0, Math.PI * 2);
            ctx.fillStyle = "#86efac";
            ctx.fill();
            ctx.lineWidth = 3;
            ctx.strokeStyle = "#0f172a";
            ctx.stroke();

            // Điểm sáng trắng trên lá mầm phải
            ctx.fillStyle = "rgba(255, 255, 255, 0.75)";
            ctx.beginPath();
            ctx.ellipse(10, -22, 4.5, 2.5, Math.PI / 5, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();

            // 3. HAI CHIẾC LÁ XÒE 45 ĐỘ NÂNG ĐỠ (GÂN LÁ RÕ NÉT)
            ctx.save();
            ctx.translate(-26, 75);
            ctx.rotate(-Math.PI / 4);
            drawDetailedLeaf();
            ctx.restore();

            ctx.save();
            ctx.translate(26, 75);
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
        ctx.bezierCurveTo(42, -30, 50, -90, 16, -112);
        ctx.bezierCurveTo(-16, -90, -25, -30, 0, 0);

        let leafGrad = ctx.createLinearGradient(0, 0, 20, -110);
        leafGrad.addColorStop(0, "#15803d");
        leafGrad.addColorStop(0.5, "#22c55e");
        leafGrad.addColorStop(1, "#4ade80");
        ctx.fillStyle = leafGrad;
        ctx.strokeStyle = "#0f172a";
        ctx.lineWidth = 3.5;
        ctx.fill();
        ctx.stroke();

        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.quadraticCurveTo(8, -55, 16, -108);
        ctx.stroke();

        ctx.strokeStyle = "rgba(255, 255, 255, 0.75)";
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.moveTo(3, -25); ctx.lineTo(19, -38);
        ctx.moveTo(6, -50); ctx.lineTo(25, -63);
        ctx.moveTo(10, -75); ctx.lineTo(24, -86);
        ctx.moveTo(3, -25); ctx.lineTo(-11, -33);
        ctx.moveTo(6, -50); ctx.lineTo(-9, -58);
        ctx.moveTo(10, -75); ctx.lineTo(1, -81);
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
    
    col_l, col_r = st.columns([0.65, 0.35])
    with col_r:
        btn_close_lbl = "ĐÓNG & TIẾP TỤC ĐĂNG NHẬP" if current_lang == "Tiếng Việt" else "CLOSE & CONTINUE TO LOGIN"
        if st.button(btn_close_lbl, use_container_width=True, type="secondary"):
            st.rerun()
