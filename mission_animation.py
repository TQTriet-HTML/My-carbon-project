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
            box-shadow: 0 0 35px rgba(0, 0, 0, 0.9), inset 0 0 25px rgba(72, 187, 120, 0.12);
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
        .replay-tag {{
            position: absolute;
            bottom: 15px;
            right: 20px;
            font-size: 11px;
            color: #64748b;
            font-weight: 600;
            letter-spacing: 1px;
        }}
    </style>
    </head>
    <body>

    <div class="player-wrapper">
        <div class="story-badge" id="storyBadge">{cap_1}</div>
        <canvas id="animCanvas" width="760" height="500"></canvas>
        <div class="replay-tag">AUTO LOOPING (60 FPS)</div>
    </div>

    <script>
    const canvas = document.getElementById('animCanvas');
    const ctx = canvas.getContext('2d');
    const badge = document.getElementById('storyBadge');

    const captions = [
        "{cap_1}",
        "{cap_2}",
        "{cap_3}",
        "{cap_4}"
    ];
    const sloganText = "{slogan}";
    const subSloganText = "{sub_slogan}";

    let startTime = performance.now();
    const CYCLE_DURATION = 28000; // 28s mỗi chu kỳ

    // Hạt khói và hạt carbon
    let smokeParticles = [];
    let carbonParticles = [];
    for(let i=0; i<45; i++) {{
        smokeParticles.push({{
            x: 645,
            y: 215,
            r: 7 + Math.random() * 10,
            vx: (Math.random() - 0.5) * 0.9,
            vy: -1.2 - Math.random() * 1.6,
            alpha: 0.5
        }});
    }}
    for(let i=0; i<60; i++) {{
        carbonParticles.push({{
            x: 100 + Math.random() * 560,
            y: 150 + Math.random() * 200,
            r: 2 + Math.random() * 3,
            vx: (Math.random() - 0.5) * 1.5,
            vy: -0.6 - Math.random() * 1.2
        }});
    }}

    function draw() {{
        const now = performance.now();
        let elapsed = (now - startTime) % CYCLE_DURATION;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (elapsed < 6000) {{
            badge.innerText = captions[0];
            badge.style.color = "#48bb78";
            badge.style.borderColor = "rgba(72, 187, 120, 0.4)";
            renderFullWorld(elapsed, 1.0, 0.0, 0.0, 0.0);
        }} else if (elapsed < 12000) {{
            badge.innerText = captions[1];
            badge.style.color = "#f87171";
            badge.style.borderColor = "rgba(248, 113, 113, 0.4)";
            let p = (elapsed - 6000) / 6000;
            renderFullWorld(elapsed, 1.0 - p * 0.4, p, 0.0, 0.0);
        }} else if (elapsed < 18000) {{
            badge.innerText = captions[2];
            badge.style.color = "#38bdf8";
            badge.style.borderColor = "rgba(56, 189, 248, 0.4)";
            let p = (elapsed - 12000) / 6000;
            renderFullWorld(elapsed, 0.6 + p * 0.4, 1.0 - p * 0.3, p, 0.0);
        }} else {{
            badge.innerText = captions[3];
            badge.style.color = "#4ade80";
            badge.style.borderColor = "rgba(74, 222, 128, 0.5)";
            let zoomP = Math.min(1.0, (elapsed - 18000) / 4000);
            renderFullWorld(elapsed, 1.0, 0.7, 1.0, zoomP);
        }}

        requestAnimationFrame(draw);
    }}

    function renderFullWorld(time, forestHealth, industrialLevel, carbonLevel, zoomProgress) {{
        // Bầu trời sâu thẳm vũ trụ
        ctx.fillStyle = "#070c16";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Sao lấp lánh khi zoom xa
        if (zoomProgress > 0.05) {{
            ctx.save();
            ctx.globalAlpha = Math.min(1.0, zoomProgress * 1.5);
            for(let s=0; s<45; s++) {{
                let sx = (s * 41) % canvas.width;
                let sy = (s * 67) % canvas.height;
                ctx.fillStyle = "rgba(255, 255, 255, 0.45)";
                ctx.fillRect(sx, sy, 2, 2);
            }}
            ctx.restore();
        }}

        // ĐỘNG TÁC THU NHỎ CINEMATIC: Camera lùi xa dần thành một quả cầu Trái Đất
        ctx.save();
        let targetX = canvas.width / 2;
        let targetY = 195;
        let scale = 1.0 - zoomProgress * 0.82; // Thu nhỏ dần về tỉ lệ quả cầu
        let transY = (1.0 - zoomProgress) * 0 + zoomProgress * (targetY - 370 * scale);

        ctx.translate(targetX * (1 - scale), transY);
        ctx.scale(scale, scale);

        // VÙNG KHÔNG GIAN BỀ MẶT ĐỊA CẦU
        if (zoomProgress < 0.98) {{
            ctx.save();
            ctx.globalAlpha = 1.0 - zoomProgress * 0.85;

            // Bầu khí quyển & Đường chân trời
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
            ctx.arc(140, 110, 40, 0, Math.PI * 2);
            let sunGrad = ctx.createRadialGradient(140, 110, 10, 140, 110, 40);
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

            // RỪNG NGUYÊN SINH
            drawTree(70, 370, 0.9 * forestHealth, "#15803d", "#22c55e");
            drawTree(130, 370, 1.2 * forestHealth, "#166534", "#48bb78");
            drawTree(200, 370, 1.0 * forestHealth, "#14532d", "#16a34a");
            drawTree(270, 370, 1.15 * forestHealth, "#15803d", "#34d399");
            drawTree(340, 370, 0.85 * forestHealth, "#166534", "#22c55e");

            // NHÀ MÁY CÔNG NGHIỆP
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

                // Cửa sổ
                ctx.fillStyle = "#facc15";
                ctx.fillRect(495, 315, 16, 20);
                ctx.fillRect(525, 315, 16, 20);
                ctx.fillRect(555, 315, 16, 20);

                // Khói xả
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

            // Tín chỉ Carbon liên kết
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
                    ctx.shadowColor = "#48bb78";
                    ctx.shadowBlur = 8;
                    ctx.fill();
                }});
                drawTree(430, 370, 0.8 * carbonLevel, "#15803d", "#48bb78");
                drawTree(710, 370, 0.7 * carbonLevel, "#166534", "#22c55e");
            }}
            ctx.restore();
        }}
        ctx.restore();

        // KHI THU PHÓNG ĐẾN ĐOẠN KẾT: QUẢ CẦU TRÁI ĐẤT XANH CHÂN THẬT & 2 LÁ CÂY 45 ĐỘ
        if (zoomProgress > 0.1) {{
            ctx.save();
            ctx.globalAlpha = Math.min(1.0, (zoomProgress - 0.1) / 0.7);
            ctx.translate(canvas.width / 2, 205);

            const R = 75; // Bán kính Trái Đất

            // 1. ĐẠI DƯƠNG XANH NGỌC SÂU THẲM
            ctx.save();
            ctx.beginPath();
            ctx.arc(0, 0, R, 0, Math.PI * 2);
            let oceanGrad = ctx.createRadialGradient(-25, -25, 10, 0, 0, R);
            oceanGrad.addColorStop(0, "#059669");
            oceanGrad.addColorStop(0.5, "#047857");
            oceanGrad.addColorStop(0.85, "#064e3b");
            oceanGrad.addColorStop(1, "#022c22");
            ctx.fillStyle = oceanGrad;
            ctx.shadowColor = "#34d399";
            ctx.shadowBlur = 32;
            ctx.fill();
            ctx.clip(); // Cắt mọi lục địa gọn trong hình cầu

            // 2. CÁC MẢNG LỤC ĐỊA & RỪNG XANH TƯƠI MÁT (Xoay nhẹ theo thời gian)
            let rot = (time * 0.0003) % (Math.PI * 2);
            ctx.save();
            ctx.rotate(rot * 0.15);

            // Mảng lục địa 1 (Á - Âu - Phi phủ rừng)
            ctx.fillStyle = "#22c55e";
            ctx.beginPath();
            ctx.ellipse(12, -18, 38, 28, 0.3, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#15803d";
            ctx.beginPath();
            ctx.ellipse(22, 10, 24, 30, -0.2, 0, Math.PI * 2);
            ctx.fill();

            // Mảng lục địa 2 (Châu Mỹ & Rừng nhiệt đới)
            ctx.fillStyle = "#4ade80";
            ctx.beginPath();
            ctx.ellipse(-38, -12, 28, 20, -0.3, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#16a34a";
            ctx.beginPath();
            ctx.ellipse(-26, 25, 16, 32, 0.25, 0, Math.PI * 2);
            ctx.fill();

            // Các dải mây trắng mỏng bồng bềnh
            ctx.fillStyle = "rgba(255, 255, 255, 0.22)";
            ctx.beginPath();
            ctx.ellipse(-5, -30, 45, 8, -0.1, 0, Math.PI * 2);
            ctx.ellipse(10, 32, 50, 9, 0.15, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // Hiệu ứng khối cầu 3D (Bóng đổ viền để quả cầu tròn trịa như mắt nhìn từ vũ trụ)
            let sphereShade = ctx.createRadialGradient(-30, -30, 10, 0, 0, R);
            sphereShade.addColorStop(0, "rgba(255, 255, 255, 0.25)");
            sphereShade.addColorStop(0.7, "rgba(0, 0, 0, 0)");
            sphereShade.addColorStop(1, "rgba(0, 0, 0, 0.65)");
            ctx.fillStyle = sphereShade;
            ctx.fill();

            // Vầng hào quang khí quyển mỏng (Atmosphere Halo)
            ctx.strokeStyle = "rgba(167, 243, 208, 0.55)";
            ctx.lineWidth = 3.5;
            ctx.stroke();
            ctx.restore();

            // 3. HAI CHIẾC LÁ XÒE GÓC 45 ĐỘ NÂNG ĐỠ TRÁI ĐẤT (CÓ GÂN LÁ RÕ NÉT)
            // Lá bên trái (-45 độ)
            ctx.save();
            ctx.translate(-24, 72);
            ctx.rotate(-Math.PI / 4); // -45 độ
            drawDetailedLeaf();
            ctx.restore();

            // Lá bên phải (+45 độ)
            ctx.save();
            ctx.translate(24, 72);
            ctx.rotate(Math.PI / 4); // +45 độ
            ctx.scale(-1, 1); // Đối xứng hoàn hảo
            drawDetailedLeaf();
            ctx.restore();

            // 4. TIÊU ĐỀ SLOGAN BỀN VỮNG
            ctx.textAlign = "center";
            ctx.font = "900 22px -apple-system, BlinkMacSystemFont, sans-serif";
            ctx.fillStyle = "#48bb78";
            ctx.shadowColor = "rgba(72, 187, 120, 0.9)";
            ctx.shadowBlur = 16;
            ctx.fillText(sloganText, 0, 185);

            ctx.font = "600 12px -apple-system, BlinkMacSystemFont, sans-serif";
            ctx.fillStyle = "#94a3b8";
            ctx.shadowBlur = 0;
            ctx.fillText(subSloganText, 0, 212);

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

    // VẼ CHI TIẾT LÁ CÂY CÓ SỐNG LÁ VÀ CÁC GÂN LÁ NHÁNH
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
        ctx.shadowColor = "#22c55e";
        ctx.shadowBlur = 20;
        ctx.fill();

        // Sống lá chính giữa
        ctx.strokeStyle = "rgba(255, 255, 255, 0.65)";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.quadraticCurveTo(8, -50, 15, -104);
        ctx.stroke();

        // Các gân lá nhánh tỏa sang hai bên
        ctx.strokeStyle = "rgba(255, 255, 255, 0.35)";
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        // Nhánh bên phải
        ctx.moveTo(3, -25); ctx.lineTo(18, -36);
        ctx.moveTo(6, -48); ctx.lineTo(24, -60);
        ctx.moveTo(10, -72); ctx.lineTo(23, -82);
        // Nhánh bên trái
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
