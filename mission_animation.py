import streamlit as st
import streamlit.components.v1 as components
from i18n import t

def get_mission_animation_html(lang="Tiếng Việt"):
    is_en = (lang == "English")
    
    # Kịch bản phụ đề chuyển đổi tự động
    cap_1 = "1. SƠ KHAI: Những cánh rừng nguyên sinh bạt ngàn nuôi dưỡng hành tinh xanh..." if not is_en else "1. PRIMORDIAL: Ancient primeval forests breathing life into the green planet..."
    cap_2 = "2. CÔNG NGHIỆP HÓA: Nhà máy mọc lên, xả khói khí nhà kính gây ô nhiễm môi trường..." if not is_en else "2. INDUSTRIALIZATION: Factories emerge, emitting greenhouse gases and polluting the atmosphere..."
    cap_3 = "3. TÍN CHỈ CARBON: Cầu nối cân bằng giúp bảo vệ môi trường mà không cản trở công nghiệp..." if not is_en else "3. CARBON CREDITS: The balancing bridge ensuring conservation without halting industrial growth..."
    cap_4 = "4. PHÁT TRIỂN BỀN VỮNG: Con người và thiên nhiên cùng chung sống hài hòa..." if not is_en else "4. SUSTAINABILITY: Humanity and nature coexisting in perfect harmony..."
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
            background: #0a0f1d;
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
            background: rgba(10, 16, 29, 0.85);
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
    const CYCLE_DURATION = 26000; // 26 giây lặp lại 1 vòng

    // Dữ liệu hạt khói & hạt sinh thái
    let smokeParticles = [];
    let carbonParticles = [];
    for(let i=0; i<40; i++) {{
        smokeParticles.push({{
            x: 530 + Math.random() * 60,
            y: 260 - Math.random() * 40,
            r: 8 + Math.random() * 12,
            vx: (Math.random() - 0.5) * 0.8,
            vy: -1.2 - Math.random() * 1.5,
            alpha: Math.random() * 0.6
        }});
    }}
    for(let i=0; i<60; i++) {{
        carbonParticles.push({{
            x: 100 + Math.random() * 560,
            y: 150 + Math.random() * 200,
            r: 2 + Math.random() * 3,
            vx: (Math.random() - 0.5) * 1.5,
            vy: -0.5 - Math.random() * 1.2,
            alpha: 0.2 + Math.random() * 0.8
        }});
    }}

    function draw() {{
        const now = performance.now();
        let elapsed = (now - startTime) % CYCLE_DURATION;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // GIAI ĐOẠN 1: 0s - 6s (Thời sơ khai)
        // GIAI ĐOẠN 2: 6s - 12s (Công nghiệp hóa, ô nhiễm)
        // GIAI ĐOẠN 3: 12s - 18s (Tín chỉ Carbon phục hồi bền vững)
        // GIAI ĐOẠN 4: 18s - 26s (Thu nhỏ thành Trái Đất xanh và Logo 2 lá 45 độ)

        if (elapsed < 6000) {{
            badge.innerText = captions[0];
            badge.style.color = "#48bb78";
            badge.style.borderColor = "rgba(72, 187, 120, 0.4)";
            drawScene(elapsed, 1.0, 0.0, 0.0, false);
        }} else if (elapsed < 12000) {{
            badge.innerText = captions[1];
            badge.style.color = "#f87171";
            badge.style.borderColor = "rgba(248, 113, 113, 0.4)";
            let progress = (elapsed - 6000) / 6000;
            drawScene(elapsed, 1.0 - progress * 0.5, progress, 0.0, false);
        }} else if (elapsed < 18000) {{
            badge.innerText = captions[2];
            badge.style.color = "#38bdf8";
            badge.style.borderColor = "rgba(56, 189, 248, 0.4)";
            let progress = (elapsed - 12000) / 6000;
            drawScene(elapsed, 0.5 + progress * 0.5, 1.0 - progress * 0.3, progress, false);
        }} else {{
            badge.innerText = captions[3];
            badge.style.color = "#4ade80";
            badge.style.borderColor = "rgba(74, 222, 128, 0.5)";
            let zoomProgress = Math.min(1.0, (elapsed - 18000) / 3000);
            drawFinale(zoomProgress, elapsed);
        }}

        requestAnimationFrame(draw);
    }}

    // Vẽ cảnh giới tự nhiên & công nghiệp (Không đè chồng nhau)
    function drawScene(time, forestHealth, industrialLevel, carbonLevel, isZooming) {{
        // Bầu trời thay đổi theo độ ô nhiễm
        let skyGradient = ctx.createLinearGradient(0, 0, 0, 380);
        if (industrialLevel > 0.4 && carbonLevel < 0.6) {{
            skyGradient.addColorStop(0, "#1c1917");
            skyGradient.addColorStop(1, "#362b28");
        }} else if (carbonLevel >= 0.6) {{
            skyGradient.addColorStop(0, "#0c1f24");
            skyGradient.addColorStop(1, "#063529");
        }} else {{
            skyGradient.addColorStop(0, "#081b29");
            skyGradient.addColorStop(1, "#0d3b36");
        }}
        ctx.fillStyle = skyGradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Mặt trời sinh thái
        ctx.save();
        ctx.beginPath();
        ctx.arc(140, 110, 42, 0, Math.PI * 2);
        let sunGrad = ctx.createRadialGradient(140, 110, 10, 140, 110, 42);
        if (industrialLevel > 0.4 && carbonLevel < 0.6) {{
            sunGrad.addColorStop(0, "rgba(251, 146, 60, 0.6)");
            sunGrad.addColorStop(1, "rgba(251, 146, 60, 0)");
        }} else {{
            sunGrad.addColorStop(0, "rgba(74, 222, 128, 0.8)");
            sunGrad.addColorStop(1, "rgba(56, 189, 248, 0)");
        }}
        ctx.fillStyle = sunGrad;
        ctx.fill();
        ctx.restore();

        // Núi phía xa
        ctx.fillStyle = "rgba(15, 30, 45, 0.7)";
        ctx.beginPath();
        ctx.moveTo(0, 360);
        ctx.lineTo(120, 240);
        ctx.lineTo(260, 360);
        ctx.lineTo(420, 260);
        ctx.lineTo(580, 360);
        ctx.lineTo(760, 270);
        ctx.lineTo(760, 380);
        ctx.lineTo(0, 380);
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

        // 1. VẼ RỪNG (Đặt ở nửa bên trái từ x=40 đến x=380, không đè lên nhà máy)
        drawTree(70, 370, 0.9 * forestHealth, "#15803d", "#22c55e");
        drawTree(130, 370, 1.2 * forestHealth, "#166534", "#48bb78");
        drawTree(200, 370, 1.0 * forestHealth, "#14532d", "#16a34a");
        drawTree(270, 370, 1.15 * forestHealth, "#15803d", "#34d399");
        drawTree(340, 370, 0.85 * forestHealth, "#166534", "#22c55e");

        // 2. VẼ KHU NHÀ MÁY (Đặt hoàn toàn ở nửa bên phải từ x=480 đến x=710)
        if (industrialLevel > 0.05) {{
            ctx.save();
            ctx.globalAlpha = Math.min(1.0, industrialLevel * 1.5);

            // Tòa nhà xưởng chính
            ctx.fillStyle = "#334155";
            ctx.fillRect(480, 300, 140, 70);

            // Mái răng cưa
            ctx.fillStyle = "#475569";
            ctx.beginPath();
            ctx.moveTo(480, 300); ctx.lineTo(515, 275); ctx.lineTo(515, 300);
            ctx.lineTo(550, 275); ctx.lineTo(550, 300);
            ctx.lineTo(585, 275); ctx.lineTo(585, 300);
            ctx.lineTo(620, 275); ctx.lineTo(620, 300);
            ctx.fill();

            // Ống khói cao
            ctx.fillStyle = "#475569";
            ctx.fillRect(635, 220, 22, 150);
            ctx.fillRect(670, 245, 18, 125);
            ctx.fillStyle = "#64748b";
            ctx.fillRect(632, 215, 28, 6);
            ctx.fillRect(668, 240, 22, 6);

            // Cửa sổ công nghiệp phát sáng
            ctx.fillStyle = "#facc15";
            ctx.fillRect(495, 315, 16, 20);
            ctx.fillRect(525, 315, 16, 20);
            ctx.fillRect(555, 315, 16, 20);
            ctx.fillRect(585, 315, 16, 20);

            ctx.restore();

            // Khói bốc lên từ ống khói
            if (carbonLevel < 0.8) {{
                smokeParticles.forEach(p => {{
                    p.y += p.vy;
                    p.x += p.vx;
                    if (p.y < 80) {{
                        p.y = 215;
                        p.x = 645 + (Math.random() - 0.5) * 10;
                    }}
                    ctx.save();
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    let smokeAlpha = (1.0 - carbonLevel * 0.8) * 0.45;
                    ctx.fillStyle = `rgba(148, 163, 184, ${{smokeAlpha}})`;
                    ctx.fill();
                    ctx.restore();
                }});
            }}
        }}

        // 3. TÍN CHỈ CARBON (Luồng hạt năng lượng xanh kết nối giữa Rừng và Nhà máy)
        if (carbonLevel > 0.1) {{
            ctx.save();
            ctx.globalAlpha = carbonLevel;
            // Vẽ các dải năng lượng kết nối
            ctx.strokeStyle = "rgba(72, 187, 120, 0.6)";
            ctx.lineWidth = 2;
            ctx.setLineDash([8, 8]);
            ctx.beginPath();
            ctx.moveTo(270, 280);
            ctx.bezierCurveTo(360, 200, 420, 200, 520, 290);
            ctx.stroke();

            // Các hạt carbon bay lên
            carbonParticles.forEach(p => {{
                p.y += p.vy;
                p.x += p.vx;
                if (p.y < 120) {{
                    p.y = 350;
                    p.x = 100 + Math.random() * 560;
                }}
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = "rgba(74, 222, 128, 0.85)";
                ctx.shadowColor = "#48bb78";
                ctx.shadowBlur = 8;
                ctx.fill();
            }});
            ctx.restore();

            // Trồng thêm rừng mới ngay cạnh công nghiệp (thể hiện phát triển bền vững)
            drawTree(430, 370, 0.8 * carbonLevel, "#15803d", "#48bb78");
            drawTree(710, 370, 0.7 * carbonLevel, "#166534", "#22c55e");
        }}
    }}

    // Hàm vẽ cây thông minh theo tỷ lệ scale
    function drawTree(x, baseY, scale, trunkColor, leafColor) {{
        if (scale <= 0.05) return;
        ctx.save();
        ctx.translate(x, baseY);
        ctx.scale(scale, scale);

        // Thân cây
        ctx.fillStyle = "#78350f";
        ctx.fillRect(-7, -45, 14, 45);

        // Các tầng lá
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

    // GIAI ĐOẠN 4: THU NHỎ THÀNH TRÁI ĐẤT XANH & LOGO 2 LÁ 45 ĐỘ
    function drawFinale(progress, time) {{
        // Nền đen vũ trụ sâu thẳm phát quang
        ctx.fillStyle = "#070c16";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Các ngôi sao lấp lánh nền
        for(let s=0; s<35; s++) {{
            let sx = (s * 37) % canvas.width;
            let sy = (s * 61) % canvas.height;
            ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
            ctx.fillRect(sx, sy, 2, 2);
        }}

        ctx.save();
        ctx.translate(canvas.width / 2, canvas.height / 2 - 25);
        ctx.scale(progress, progress);

        // 1. TRÁI ĐẤT XANH LÁ (Bao gồm lục địa, rừng cây, đại dương ngả xanh lam)
        const earthRadius = 70;
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, -35, earthRadius, 0, Math.PI * 2);
        
        // Đại dương màu xanh ngọc lục bảo (Emerald Green Ocean)
        let oceanGrad = ctx.createRadialGradient(-20, -55, 10, 0, -35, earthRadius);
        oceanGrad.addColorStop(0, "#10b981");
        oceanGrad.addColorStop(0.6, "#047857");
        oceanGrad.addColorStop(1, "#064e3b");
        ctx.fillStyle = oceanGrad;
        ctx.shadowColor = "#34d399";
        ctx.shadowBlur = 35;
        ctx.fill();
        ctx.clip();

        // Các mảng lục địa & rừng cây trên Trái Đất (Vẽ vector màu xanh lá tươi sáng)
        ctx.fillStyle = "#22c55e";
        // Lục địa Á - Âu - Phi
        ctx.beginPath();
        ctx.ellipse(15, -45, 30, 22, 0.4, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.ellipse(35, -20, 20, 25, -0.2, 0, Math.PI * 2);
        ctx.fill();
        // Lục địa Mỹ
        ctx.fillStyle = "#4ade80";
        ctx.beginPath();
        ctx.ellipse(-35, -40, 22, 18, -0.3, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.ellipse(-25, -15, 14, 28, 0.2, 0, Math.PI * 2);
        ctx.fill();

        // Khí quyển phát sáng mỏng
        ctx.strokeStyle = "rgba(167, 243, 208, 0.4)";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(0, -35, earthRadius - 2, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();

        // 2. HAI CHIẾC LÁ MÀU XANH LÁ XÒE 45 ĐỘ NÂNG ĐỠ TRÁI ĐẤT
        // Lá bên trái (Xòe góc -45 độ)
        ctx.save();
        ctx.translate(-22, 45);
        ctx.rotate(-Math.PI / 4); // -45 độ
        drawSingleLeaf();
        ctx.restore();

        // Lá bên phải (Xòe góc +45 độ)
        ctx.save();
        ctx.translate(22, 45);
        ctx.rotate(Math.PI / 4); // +45 độ
        ctx.scale(-1, 1); // Đối xứng
        drawSingleLeaf();
        ctx.restore();

        // 3. CÂU SLOGAN VÀ TIÊU ĐỀ THƯƠNG HIỆU
        ctx.textAlign = "center";
        ctx.font = "900 22px -apple-system, BlinkMacSystemFont, sans-serif";
        ctx.fillStyle = "#48bb78";
        ctx.shadowColor = "rgba(72, 187, 120, 0.8)";
        ctx.shadowBlur = 15;
        ctx.fillText(sloganText, 0, 145);

        ctx.font = "600 12px -apple-system, BlinkMacSystemFont, sans-serif";
        ctx.fillStyle = "#94a3b8";
        ctx.shadowBlur = 0;
        ctx.fillText(subSloganText, 0, 172);

        ctx.restore();
    }}

    // Vẽ từng chiếc lá xanh uốn cong tự nhiên
    function drawSingleLeaf() {{
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.bezierCurveTo(35, -25, 45, -75, 15, -95);
        ctx.bezierCurveTo(-15, -75, -20, -25, 0, 0);
        
        let leafGrad = ctx.createLinearGradient(0, 0, 20, -90);
        leafGrad.addColorStop(0, "#15803d");
        leafGrad.addColorStop(0.5, "#22c55e");
        leafGrad.addColorStop(1, "#4ade80");
        ctx.fillStyle = leafGrad;
        ctx.shadowColor = "#22c55e";
        ctx.shadowBlur = 18;
        ctx.fill();

        // Gân lá chính
        ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.quadraticCurveTo(8, -45, 15, -92);
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
