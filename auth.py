import streamlit as st
import streamlit.components.v1 as components
import re
from mission_animation import hien_thi_hop_thoai_su_menh

def get_particle_logo_html(lang="Tiếng Việt"):
    is_en = (lang == "English")
    text_slogan = "Vì một ngày mai tươi sáng!" if not is_en else "For a brighter tomorrow!"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      * {{ box-sizing: border-box; margin: 0; padding: 0; }}
      body {{
        background: transparent;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }}
      canvas {{
        display: block;
        background: transparent;
      }}
    </style>
    </head>
    <body>
    <canvas id="logoCanvas"></canvas>
    <script>
    const canvas = document.getElementById('logoCanvas');
    const ctx = canvas.getContext('2d');

    const logicalW = 420;
    const logicalH = 150;
    const dpr = window.devicePixelRatio || 2;
    canvas.width = logicalW * dpr;
    canvas.height = logicalH * dpr;
    canvas.style.width = logicalW + 'px';
    canvas.style.height = logicalH + 'px';
    ctx.scale(dpr, dpr);

    const cx = logicalW / 2;
    const cy = 72;
    const R = 38;
    const phrase = "{text_slogan}";

    function renderVectorLogo(c, alpha = 1.0, scale = 1.0) {{
      if (alpha <= 0.001) return;
      c.save();
      c.globalAlpha = alpha;
      c.translate(cx, cy);
      c.scale(scale, scale);
      c.translate(-cx, -cy);

      // Quả cầu Trái Đất
      c.save();
      c.beginPath();
      c.arc(cx, cy, R, 0, Math.PI * 2);
      c.fillStyle = '#7dd3fc';
      c.fill();
      c.lineWidth = 3.8;
      c.strokeStyle = '#0f172a';
      c.stroke();
      c.clip();

      // Mảng lục địa
      c.fillStyle = '#4ade80';
      c.strokeStyle = '#0f172a';
      c.lineWidth = 2.8;

      c.beginPath();
      c.moveTo(cx - 9, cy - R);
      c.bezierCurveTo(cx - 6, cy - 26, cx + 9, cy - 24, cx + 12, cy - R);
      c.closePath();
      c.fill(); c.stroke();

      c.beginPath();
      c.moveTo(cx - R, cy - 22);
      c.bezierCurveTo(cx - 20, cy - 28, cx - 18, cy - 8, cx - 30, cy + 2);
      c.bezierCurveTo(cx - 38, cy + 6, cx - R, cy + 8, cx - R, cy - 22);
      c.closePath();
      c.fill(); c.stroke();

      c.beginPath();
      c.moveTo(cx - 26, cy + 10);
      c.bezierCurveTo(cx - 8, cy + 12, cx - 12, cy + 32, cx - 22, cy + 36);
      c.bezierCurveTo(cx - 32, cy + 36, cx - 30, cy + 22, cx - 26, cy + 10);
      c.closePath();
      c.fill(); c.stroke();

      c.beginPath();
      c.moveTo(cx + 20, cy - 26);
      c.bezierCurveTo(cx + 14, cy - 8, cx + 32, cy - 4, cx + 20, cy + 8);
      c.bezierCurveTo(cx + 14, cy + 18, cx + 32, cy + 22, cx + R, cy + 10);
      c.bezierCurveTo(cx + R, cy - 20, cx + 32, cy - 30, cx + 20, cy - 26);
      c.closePath();
      c.fill(); c.stroke();

      c.fillStyle = '#38bdf8';
      c.beginPath();
      c.ellipse(cx + 10, cy + 28, 14, 6.5, 0, 0, Math.PI * 2);
      c.fill();

      // Khuôn mặt đáng yêu
      c.fillStyle = '#0f172a';
      c.beginPath();
      c.arc(cx - 11, cy + 2, 2.8, 0, Math.PI * 2);
      c.arc(cx + 11, cy + 2, 2.8, 0, Math.PI * 2);
      c.fill();

      c.beginPath();
      c.arc(cx, cy + 6, 4.0, 0.15 * Math.PI, 0.85 * Math.PI);
      c.lineWidth = 2.4;
      c.lineCap = 'round';
      c.stroke();

      c.fillStyle = '#f87171';
      c.beginPath();
      c.arc(cx - 19, cy + 9, 3.5, 0, Math.PI * 2);
      c.arc(cx + 19, cy + 9, 3.5, 0, Math.PI * 2);
      c.fill();
      c.restore();

      c.beginPath();
      c.arc(cx, cy, R, 0, Math.PI * 2);
      c.lineWidth = 3.8;
      c.strokeStyle = '#0f172a';
      c.stroke();

      // Mầm cây trên đầu
      c.save();
      c.translate(cx, cy - R);
      c.strokeStyle = '#0f172a';
      c.lineWidth = 6.5;
      c.lineCap = 'round';
      c.beginPath();
      c.moveTo(0, 2); c.lineTo(0, -11);
      c.stroke();

      c.strokeStyle = '#78350f';
      c.lineWidth = 4.2;
      c.beginPath();
      c.moveTo(0, 1); c.lineTo(0, -10);
      c.stroke();

      c.beginPath();
      c.ellipse(-8, -13, 7.8, 5.0, -Math.PI / 5, 0, Math.PI * 2);
      c.fillStyle = '#14532d';
      c.fill();
      c.lineWidth = 2.2;
      c.strokeStyle = '#0f172a';
      c.stroke();

      c.beginPath();
      c.ellipse(8, -13, 7.8, 5.0, Math.PI / 5, 0, Math.PI * 2);
      c.fillStyle = '#14532d';
      c.fill();
      c.lineWidth = 2.2;
      c.strokeStyle = '#0f172a';
      c.stroke();
      c.restore();

      // 2 Lá bự 45 độ nâng đỡ
      function drawBigLeaf(angle, isFlipped) {{
        c.save();
        c.translate(cx + (isFlipped ? 13 : -13), cy + 29);
        c.rotate(angle);
        if (isFlipped) c.scale(-1, 1);

        c.beginPath();
        c.moveTo(0, 0);
        c.bezierCurveTo(19, -13, 24, -42, 7, -52);
        c.bezierCurveTo(-7, -42, -11, -13, 0, 0);
        c.fillStyle = '#22c55e';
        c.fill();
        c.strokeStyle = '#0f172a';
        c.lineWidth = 2.8;
        c.stroke();

        c.strokeStyle = '#ffffff';
        c.lineWidth = 1.7;
        c.beginPath();
        c.moveTo(0, 0);
        c.quadraticCurveTo(3, -25, 7, -50);
        c.stroke();

        c.strokeStyle = 'rgba(255, 255, 255, 0.85)';
        c.lineWidth = 1.1;
        c.beginPath();
        c.moveTo(1, -12); c.lineTo(8, -18);
        c.moveTo(3, -24); c.lineTo(11, -31);
        c.moveTo(5, -36); c.lineTo(11, -42);
        c.moveTo(1, -12); c.lineTo(-5, -16);
        c.moveTo(3, -24); c.lineTo(-4, -28);
        c.stroke();
        c.restore();
      }}

      drawBigLeaf(-Math.PI / 4, false);
      drawBigLeaf(Math.PI / 4, true);

      c.restore();
    }}

    // DÒNG CHỮ LƯỢN SÓNG ĐÚNG 1 LẦN DUY NHẤT KÈM ÁNH SÁNG XANH QUÉT
    function renderWavingTextOnce(c, alpha = 1.0, elapsed = 0) {{
      if (alpha <= 0.001) return;
      c.save();
      c.globalAlpha = alpha;
      c.font = "900 20px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
      c.textAlign = "center";
      c.textBaseline = "middle";

      const totalChars = phrase.length;
      const metrics = c.measureText(phrase);
      const startX = cx - (metrics.width / 2);
      let currX = startX;

      const waveStart = 7500;
      const waveDuration = 2400;
      const waveProg = (elapsed - waveStart) / waveDuration;

      for (let i = 0; i < totalChars; i++) {{
        const ch = phrase[i];
        const w = c.measureText(ch).width;
        const charCx = currX + w / 2;
        const charNorm = i / Math.max(1, totalChars - 1);
        
        let waveY = cy;
        let isSwept = false;
        let sweepIntensity = 0;

        if (waveProg >= 0 && waveProg <= 1.25) {{
          const dist = Math.abs(waveProg - charNorm);
          if (dist < 0.16) {{
            const factor = 1 - (dist / 0.16);
            waveY = cy - Math.sin(factor * Math.PI) * 9;
            sweepIntensity = Math.sin(factor * Math.PI);
            isSwept = true;
          }}
        }}

        c.save();
        if (isSwept) {{
          c.fillStyle = '#bbf7d0';
          c.shadowColor = '#22c55e';
          c.shadowBlur = 18 * sweepIntensity;
        }} else {{
          c.fillStyle = '#4ade80';
          c.shadowColor = 'rgba(74, 222, 128, 0.45)';
          c.shadowBlur = 6;
        }}
        c.fillText(ch, charCx, waveY);
        c.restore();

        currX += w;
      }}
      c.restore();
    }}

    const NUM_PARTICLES = 160;
    const particles = [];
    const colors = ['#4ade80', '#22c55e', '#38bdf8', '#7dd3fc', '#86efac', '#34d399'];

    for (let i = 0; i < NUM_PARTICLES; i++) {{
      const baseAngle = (i / NUM_PARTICLES) * Math.PI * 2;
      particles.push({{
        currentAngle: baseAngle,
        orbitRadius: 55 + Math.random() * 65,
        speed: (0.012 + Math.random() * 0.018) * (Math.random() < 0.5 ? 1 : -1),
        targetX: cx + (Math.random() - 0.5) * 220,
        targetY: cy + (Math.random() - 0.5) * 40,
        x: cx,
        y: cy,
        size: 1.2 + Math.random() * 1.8,
        color: colors[i % colors.length]
      }});
    }}

    const CYCLE = 18000;
    const startTime = performance.now();

    function animate() {{
      const now = performance.now();
      const elapsed = (now - startTime) % CYCLE;
      ctx.clearRect(0, 0, logicalW, logicalH);

      if (elapsed < 4500) {{
        renderVectorLogo(ctx, 1.0, 1.0);
      }} else if (elapsed < 7500) {{
        const pProg = (elapsed - 4500) / 3000;
        const logoAlpha = Math.max(0, 1 - pProg * 2.0);
        if (logoAlpha > 0) renderVectorLogo(ctx, logoAlpha);

        for (let i = 0; i < NUM_PARTICLES; i++) {{
          const p = particles[i];
          p.currentAngle += p.speed;
          const r = p.orbitRadius * Math.sin(pProg * Math.PI);
          p.x = cx + Math.cos(p.currentAngle) * r;
          p.y = cy + Math.sin(p.currentAngle) * (r * 0.6);
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.globalAlpha = Math.sin(pProg * Math.PI);
          ctx.fill();
        }}
        ctx.globalAlpha = 1.0;

        if (pProg > 0.5) {{
          renderWavingTextOnce(ctx, (pProg - 0.5) * 2, elapsed);
        }}
      }} else if (elapsed < 13000) {{
        renderWavingTextOnce(ctx, 1.0, elapsed);
      }} else if (elapsed < 15500) {{
        const dProg = (elapsed - 13000) / 2500;
        const textAlpha = Math.max(0, 1 - dProg * 2.0);
        if (textAlpha > 0) renderWavingTextOnce(ctx, textAlpha, elapsed);

        for (let i = 0; i < NUM_PARTICLES; i++) {{
          const p = particles[i];
          p.currentAngle += p.speed;
          const r = p.orbitRadius * Math.sin(dProg * Math.PI);
          p.x = cx + Math.cos(p.currentAngle) * r;
          p.y = cy + Math.sin(p.currentAngle) * (r * 0.6);
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.globalAlpha = Math.sin(dProg * Math.PI);
          ctx.fill();
        }}
        ctx.globalAlpha = 1.0;

        if (dProg > 0.6) {{
          renderVectorLogo(ctx, (dProg - 0.6) * 2.5);
        }}
      }} else {{
        const rProg = (elapsed - 15500) / 2500;
        renderVectorLogo(ctx, 0.4 + rProg * 0.6);
      }}

      requestAnimationFrame(animate);
    }}

    animate();
    </script>
    </body>
    </html>
    """

def hien_thi_cong_dang_nhap(lang="Tiếng Việt"):
    if "reg_success_data" not in st.session_state:
        st.session_state["reg_success_data"] = None
    if "show_intro_reg_form" not in st.session_state:
        st.session_state["show_intro_reg_form"] = False

    T = {
        "Tiếng Việt": {
            "slogan": "MỘT CÚ CHẠM - VẠN ĐIỀU XANH",
            "subtitle": "Chào mừng đến với Sàn giao dịch Tín chỉ Carbon tiên phong. Nơi công nghệ vệ tinh AI hội tụ cùng sứ mệnh bảo vệ Trái Đất.",
            "tab_login": "ĐĂNG NHẬP", "tab_reg": "TẠO TÀI KHOẢN", "tab_mission_tab": "SỨ MỆNH NỀN TẢNG",
            "welcome_msg": "XIN CHÀO QUÝ ĐỒNG HÀNH!",
            "user": "Tên đăng nhập", "pass": "Mật khẩu",
            "btn_login": "XÁC THỰC TRUY CẬP", "btn_reg": "TẠO MỚI TÀI KHOẢN",
            "btn_mission": "KHÁM PHÁ SỨ MỆNH",
            "pwd_error": "Mật khẩu phải từ 8-20 ký tự, bao gồm ít nhất 1 chữ hoa, 1 chữ thường, 1 số và 1 ký tự đặc biệt.",
            "reg_success_line1": "Bạn đã đặt bước chân đầu tiên",
            "reg_success_line2": "trên chặng đường xanh!",
            "account_label": "Tài khoản",
            "btn_auto_login": "ĐĂNG NHẬP NGAY",
            "achieve": "THÀNH TỰU NỀN TẢNG", "ach_1_val": "2.5M+", "ach_1_lbl": "Tấn Carbon Giao Dịch", "ach_2_val": "15,000", "ach_2_lbl": "Hecta Rừng Được Bảo Vệ",
            "projects": "DỰ ÁN TIÊU BIỂU", "proj_name": "Dự án Rừng ngập mặn Cà Mau", "proj_desc": "Bảo vệ sinh khối & đa dạng sinh học ven biển.", "proj_badge": "Đã xác thực AI (Verified)",
            "vision_title": "TẦM NHÌN NET-ZERO 2050",
            "vision_desc": "Phấn đấu tới năm 2050 phủ sạch tín chỉ carbon toàn cầu, kiến tạo thị trường giao dịch xanh minh bạch và bền vững.",
            "vision_badge": "Tiêu chuẩn Verra VCS",
            "flag_title": "NỀN TẢNG QUỐC GIA VIỆT NAM",
            "flag_desc": "Vận hành theo Nghị định 06/2022/NĐ-CP & Đề án thị trường Carbon",
            "news_lbl": "TIN MỚI NHẤT:", "news_txt": "Thị trường Tín chỉ Carbon Việt Nam chính thức bước vào giai đoạn vận hành thí điểm."
        },
        "English": {
            "slogan": "ONE TOUCH - ONE GREEN WORLD",
            "subtitle": "Welcome to the pioneer Carbon Credit Exchange. AI satellite technology meets Earth protection mission.",
            "tab_login": "LOGIN", "tab_reg": "REGISTER", "tab_mission_tab": "PLATFORM MISSION",
            "welcome_msg": "WELCOME PARTNER!",
            "user": "Username", "pass": "Password",
            "btn_login": "AUTHENTICATE", "btn_reg": "CREATE ACCOUNT",
            "btn_mission": "EXPLORE MISSION",
            "pwd_error": "Password must be 8-20 characters with uppercase, lowercase, number, and special character.",
            "reg_success_line1": "You have taken your first step",
            "reg_success_line2": "towards sustainability!",
            "account_label": "Account",
            "btn_auto_login": "LOGIN NOW",
            "achieve": "PLATFORM ACHIEVEMENTS", "ach_1_val": "2.5M+", "ach_1_lbl": "Tons Carbon Traded", "ach_2_val": "15,000", "ach_2_lbl": "Hectares Protected",
            "projects": "FEATURED PROJECTS", "proj_name": "Ca Mau Mangrove Project", "proj_desc": "Protecting biomass & coastal biodiversity.", "proj_badge": "AI Verified",
            "vision_title": "NET-ZERO VISION 2050",
            "vision_desc": "Committed to global net-zero carbon credit coverage by 2050, fostering a transparent, sustainable marketplace.",
            "vision_badge": "Verra VCS Standard",
            "flag_title": "VIETNAM NATIONAL PLATFORM",
            "flag_desc": "Operating under Decree 06/2022/ND-CP & National Carbon Market Project",
            "news_lbl": "LATEST NEWS:", "news_txt": "Vietnam's Carbon Credit Market officially begins pilot operation."
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

    st.markdown("""
        <style>
        @keyframes gentleStreamFlow {
            0% { background-position: 0% 40%; }
            50% { background-position: 100% 60%; }
            100% { background-position: 0% 40%; }
        }

        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #060d15 !important;
            background-image: 
                radial-gradient(circle at 15% 25%, rgba(16, 185, 129, 0.32) 0%, transparent 50%),
                radial-gradient(circle at 85% 75%, rgba(14, 165, 233, 0.30) 0%, transparent 50%),
                radial-gradient(circle at 75% 20%, rgba(5, 150, 105, 0.26) 0%, transparent 45%),
                radial-gradient(circle at 25% 80%, rgba(37, 99, 235, 0.28) 0%, transparent 50%),
                linear-gradient(130deg, #071520 0%, #082a1d 25%, #081d33 50%, #063426 75%, #0a2135 100%) !important;
            background-size: 260% 260% !important;
            animation: gentleStreamFlow 28s ease-in-out infinite !important;
        }

        html, body, [data-testid="stAppViewContainer"], .main {
            overflow: hidden !important;
            height: 100vh !important;
            max-height: 100vh !important;
        }

        /* KHUNG CHÍNH CỐ ĐỊNH KHOẢNG CÁCH CHUẨN ĐỈNH */
        .block-container {
            padding-top: 1.8rem !important;
            padding-bottom: 1.2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-height: 100vh !important;
            overflow: hidden !important;
        }

        @keyframes greenBreathePulse {
            0%, 100% {
                box-shadow: 0 0 14px rgba(72, 187, 120, 0.35), inset 0 0 12px rgba(72, 187, 120, 0.15);
                border-color: rgba(72, 187, 120, 0.55) !important;
            }
            50% {
                box-shadow: 0 0 32px rgba(72, 187, 120, 0.85), inset 0 0 20px rgba(72, 187, 120, 0.35);
                border-color: #48bb78 !important;
            }
        }

        @keyframes sweepBlueLight7s {
            0%, 75% { left: -120%; opacity: 0; }
            78% { opacity: 0.95; left: -120%; }
            92%, 100% { left: 220%; opacity: 0; }
        }

        /* KHỐI FORM BÊN TRÁI PHỦ KÍNH MỜ */
        div[data-testid="stForm"] {
            background: linear-gradient(135deg, rgba(13, 31, 60, 0.88), rgba(18, 42, 77, 0.86)) !important;
            backdrop-filter: blur(14px) !important;
            border: 2px solid rgba(72, 187, 120, 0.6) !important;
            border-radius: 16px !important;
            padding: 14px 20px !important;
            animation: greenBreathePulse 4s infinite ease-in-out !important;
            position: relative;
            overflow: hidden !important;
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.35s ease !important;
            margin-bottom: 0px !important;
        }
        div[data-testid="stForm"]::after {
            content: '';
            position: absolute;
            top: 0;
            left: -120%;
            width: 65%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.75), rgba(96, 165, 250, 0.85), transparent);
            transform: skewX(-25deg);
            animation: sweepBlueLight7s 7s infinite linear;
            z-index: 10;
            pointer-events: none;
        }
        div[data-testid="stForm"]:hover {
            transform: translateY(-3px) scale(1.015) !important;
            box-shadow: 0 16px 40px rgba(72, 187, 120, 0.9) !important;
            border-color: #48bb78 !important;
        }

        /* HIỆU ỨNG CHUYỂN MÀU TỪ TỪ XANH LÁ <-> XANH DƯƠNG CHO 'XIN CHÀO QUÝ ĐỒNG HÀNH!' */
        @keyframes greenToBlueGlow {
            0%, 100% {
                color: #4ade80 !important;
                text-shadow: 0 0 14px rgba(74, 222, 128, 0.85);
            }
            50% {
                color: #38bdf8 !important;
                text-shadow: 0 0 16px rgba(56, 189, 248, 0.85);
            }
        }
        .welcome-title-animated {
            text-align: center;
            margin-bottom: 12px;
            font-size: 1.18rem;
            font-weight: 900;
            letter-spacing: 1px;
            animation: greenToBlueGlow 5s infinite ease-in-out;
        }

        /* GIÃN CÁCH KHÔNG GIAN CÁC KHỐI BÊN PHẢI (MARGIN RỘNG RÃI HƠN) */
        .hardcore-green-card {
            background: linear-gradient(135deg, rgba(6, 44, 25, 0.88) 0%, rgba(10, 61, 35, 0.86) 100%) !important;
            backdrop-filter: blur(14px) !important;
            border: 2px solid #22c55e !important;
            border-radius: 14px !important;
            padding: 12px 18px !important;
            margin-bottom: 14px !important;
            position: relative !important;
            overflow: hidden !important;
            animation: greenBreathePulse 4s infinite ease-in-out !important;
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.35s ease, border-color 0.35s ease !important;
        }
        .hardcore-green-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: -120%;
            width: 65%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.75), rgba(96, 165, 250, 0.85), transparent);
            transform: skewX(-25deg);
            animation: sweepBlueLight7s 7s infinite linear;
            z-index: 10;
            pointer-events: none;
        }
        .hardcore-green-card:hover {
            transform: translateY(-3px) scale(1.015) !important;
            box-shadow: 0 14px 35px rgba(72, 187, 120, 0.9) !important;
            border-color: #48bb78 !important;
        }

        /* KHỐI LÁ CỜ VIỆT NAM MỞ RỘNG TO - PHÁT SÁNG ĐỎ & NGÔI SAO PHÁT SÁNG VÀNG - BỎ UỐN LƯỢN */
        .vn-flag-card-expanded {
            background: linear-gradient(135deg, rgba(20, 24, 38, 0.92) 0%, rgba(28, 36, 56, 0.9) 100%) !important;
            backdrop-filter: blur(14px) !important;
            border: 1.8px solid rgba(239, 68, 68, 0.65) !important;
            border-radius: 14px !important;
            padding: 12px 18px !important;
            margin-bottom: 0px !important;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 6px 25px rgba(220, 38, 38, 0.25);
            transition: all 0.3s ease;
        }
        .vn-flag-card-expanded:hover {
            border-color: #ef4444 !important;
            box-shadow: 0 8px 30px rgba(239, 68, 68, 0.45) !important;
            transform: translateY(-2px);
        }

        @keyframes flagRedPulseGlow {
            0%, 100% {
                box-shadow: 0 0 14px rgba(218, 37, 29, 0.8), 0 0 28px rgba(239, 68, 68, 0.5);
            }
            50% {
                box-shadow: 0 0 22px rgba(218, 37, 29, 0.95), 0 0 35px rgba(239, 68, 68, 0.75);
            }
        }
        .flag-box-glowing {
            width: 72px;
            height: 48px;
            background: #da251d;
            border-radius: 6px;
            border: 1.5px solid rgba(254, 202, 202, 0.4);
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            animation: flagRedPulseGlow 3s infinite ease-in-out;
            flex-shrink: 0;
        }

        @keyframes starYellowGlow {
            0%, 100% {
                filter: drop-shadow(0 0 4px #ffff00) drop-shadow(0 0 8px #facc15);
            }
            50% {
                filter: drop-shadow(0 0 7px #ffff00) drop-shadow(0 0 14px #eab308);
            }
        }
        .flag-star-svg {
            animation: starYellowGlow 2.5s infinite ease-in-out;
        }

        /* NÚT XÁC THỰC TRUY CẬP (MÀU XANH LÁ) */
        div[data-testid="column"]:nth-child(1) div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
            border: 1.5px solid #4ade80 !important;
            color: white !important;
            font-weight: 800 !important;
            letter-spacing: 0.8px !important;
            border-radius: 9px !important;
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.45) !important;
            transition: all 0.3s ease !important;
            margin-top: 2px !important;
            padding: 8px 14px !important;
        }
        div[data-testid="column"]:nth-child(1) div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%) !important;
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 10px 25px rgba(34, 197, 94, 0.8) !important;
        }

        /* NÚT KHÁM PHÁ SỨ MỆNH: ĐỔI SANG MÀU XANH DƯƠNG CÔNG NGHỆ (ELECTRIC BLUE) */
        div[data-testid="column"]:nth-child(2) div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 50%, #075985 100%) !important;
            border: 1.5px solid #38bdf8 !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            letter-spacing: 0.8px !important;
            border-radius: 9px !important;
            box-shadow: 0 4px 18px rgba(14, 165, 233, 0.5) !important;
            transition: all 0.3s ease !important;
            margin-top: 2px !important;
            padding: 8px 14px !important;
        }
        div[data-testid="column"]:nth-child(2) div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #38bdf8 0%, #0284c7 50%, #0369a1 100%) !important;
            border-color: #7dd3fc !important;
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 8px 25px rgba(56, 189, 248, 0.85) !important;
            color: #ffffff !important;
        }

        /* KHUNG CHỨA SLOGAN ĐƯỢC GIÃN KHOẢNG CÁCH RỘNG RÃI VỚI CÁC KHỐI BÊN DƯỚI */
        .slogan-fixed-anchor {
            text-align: center;
            padding-top: 14px;
            padding-bottom: 4px;
            overflow: visible !important;
            white-space: nowrap;
        }
        .subtitle-custom-green-blue {
            text-align: center;
            color: #38bdf8 !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            margin-top: 4px !important;
            margin-bottom: 26px !important;
            text-shadow: 0 0 12px rgba(56, 189, 248, 0.45);
            letter-spacing: 0.3px;
        }

        @keyframes waveUp {
            0%, 20%, 100% { transform: translateY(0); text-shadow: none; }
            10% { transform: translateY(-10px); text-shadow: 0 0 20px rgba(72,187,120,1); }
        }
        .wave-char {
            display: inline-block;
            position: relative;
            margin-right: 2px;
            font-size: clamp(23px, 2.7vw, 36px) !important;
            font-weight: 900 !important;
            letter-spacing: 1.5px !important;
            line-height: 1.35 !important;
            background: linear-gradient(90deg, #48bb78, #68d391, #319795);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: waveUp 10s infinite ease-in-out;
            animation-delay: var(--delay);
            vertical-align: middle;
        }

        .section-title-custom {
            color: #ffffff;
            font-size: 0.98rem;
            font-weight: 800;
            letter-spacing: 1.2px;
            margin-bottom: 4px;
            border-left: 4px solid #48bb78;
            padding-left: 8px;
            text-transform: uppercase;
        }
        .stat-value-custom {
            font-size: 1.75rem;
            font-weight: 900;
            color: #63b3ed;
            margin-bottom: 2px;
            line-height: 1.1;
        }
        .stat-label-custom { color: #cbd5e1; font-size: 0.85rem; font-weight: 500; }
        .project-title-custom { color: #48bb78; font-weight: 700; font-size: 1.05rem; margin-bottom: 3px; }
        .project-desc-custom { color: #cbd5e1; font-size: 0.82rem; margin-bottom: 6px; line-height: 1.35; }
        .verified-badge-custom {
            display: inline-block;
            background: rgba(72, 187, 120, 0.2);
            border: 1px solid #48bb78;
            color: #48bb78;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .news-ticker-container {
            position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(10, 18, 30, 0.95);
            border-top: 1px solid rgba(72, 187, 120, 0.3); color: #e2e8f0; padding: 6px 20px;
            display: flex; align-items: center; z-index: 1000;
        }
        .news-marquee { overflow: hidden; white-space: nowrap; width: 100%; }
        .news-marquee span { display: inline-block; padding-left: 100%; animation: marquee 20s linear infinite; }
        @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
        </style>
    """, unsafe_allow_html=True)

    # 1. SLOGAN LÀM MỐC CỐ ĐỊNH & DÒNG CHỮ DƯỚI TO HƠN, MÀU XANH, GIÃN CÁCH RỘNG RÃI
    wave_html = '<div class="slogan-fixed-anchor">'
    delay = 0.0
    for char in t["slogan"]:
        char_display = "&nbsp;" if char == " " else char
        wave_html += f'<span class="wave-char" style="--delay: {delay}s;">{char_display}</span>'
        delay += 0.1
    wave_html += '</div>'
    st.markdown(wave_html, unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle-custom-green-blue">{t["subtitle"]}</div>', unsafe_allow_html=True)

    _, col_form, col_space, col_info, _ = st.columns([0.1, 1.25, 0.08, 1.25, 0.1])
    
    # ================= CỘT TRÁI =================
    with col_form:
        tab_dang_nhap, tab_dang_ky = st.tabs([t["tab_login"], t["tab_reg"]])
        with tab_dang_nhap:
            with st.form("form_login"):
                # DÒNG "XIN CHÀO QUÝ ĐỒNG HÀNH!" CHUYỂN MÀU TỪ TỪ XANH LÁ <-> XANH DƯƠNG
                st.markdown(f"""
                    <div class="welcome-title-animated">
                        {t["welcome_msg"]}
                    </div>
                """, unsafe_allow_html=True)

                u_name = st.text_input(t["user"], placeholder="admin, investor, buyer")
                u_pass = st.text_input(t["pass"], type="password", placeholder="••••••")
                
                col_btn_log, col_btn_mis = st.columns([0.55, 0.45])
                with col_btn_log:
                    submitted = st.form_submit_button(t["btn_login"], type="primary", use_container_width=True)
                with col_btn_mis:
                    # NÚT SỨ MỆNH MÀU XANH DƯƠNG CÔNG NGHỆ
                    open_mission = st.form_submit_button(t["btn_mission"], use_container_width=True)
                
                if submitted:
                    users = st.session_state.get("users_db", {})
                    if u_name in users and users[u_name]["password"] == u_pass:
                        st.session_state["logged_in"] = True
                        st.session_state["current_user"] = u_name
                        st.session_state["current_role"] = users[u_name]["role"]
                        st.rerun()
                    else:
                        st.error("Thông tin không chính xác." if lang=="Tiếng Việt" else "Invalid credentials.")
                
                if open_mission:
                    hien_thi_hop_thoai_su_menh()
            
            # HOẠT HỌA LOGO -> CHỮ LƯỢN SÓNG 1 LẦN CÙNG ÁNH SÁNG XANH LƯỚT QUA -> TỤ LẠI LOGO
            components.html(get_particle_logo_html(lang), height=150, scrolling=False)
                        
        with tab_dang_ky:
            if st.session_state["reg_success_data"]:
                registered_user = st.session_state['reg_success_data']['user']
                account_txt = t["account_label"]
                st.markdown(f"""
                    <div style="background: rgba(72,187,120,0.12); border: 1.5px solid #48bb78; text-align:center; padding: 12px 10px; border-radius:12px; margin-top: 6px;">
                        <p style="color:#48bb78; font-weight:700; margin-bottom:4px; font-size:0.92rem;">{t['reg_success_line1']} {t['reg_success_line2']}</p>
                        <p style="color:#cbd5e1; margin-bottom: 0px; font-size:0.88rem;">{account_txt}: <b style="color:#63b3ed;">{registered_user}</b></p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(t["btn_auto_login"], type="primary", use_container_width=True):
                    data = st.session_state["reg_success_data"]
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = data["user"]
                    st.session_state["current_role"] = data["role"]
                    st.session_state["reg_success_data"] = None
                    st.rerun()
            else:
                with st.form("form_register", clear_on_submit=True):
                    st.markdown(f"""
                        <div class="welcome-title-animated">
                            {t["welcome_msg"]}
                        </div>
                    """, unsafe_allow_html=True)
                    new_user = st.text_input("Tên tài khoản mới" if lang=="Tiếng Việt" else "New Username")
                    new_pass = st.text_input("Mật khẩu" if lang=="Tiếng Việt" else "Password", type="password")
                    role_sel = st.selectbox(
                        "Phân loại" if lang=="Tiếng Việt" else "Role", 
                        ["Doanh nghiệp mua tín chỉ", "Chủ rừng / Kỹ sư MRV", "Nhà đầu tư từ xa (Cổ đông)"],
                        format_func=lambda x: {"Doanh nghiệp mua tín chỉ": "Credit Buyer Enterprise", "Chủ rừng / Kỹ sư MRV": "Forest Owner / MRV Engineer", "Nhà đầu tư từ xa (Cổ đông)": "Remote Investor (Shareholder)"}.get(x, x) if lang == "English" else x
                    )
                    reg_submitted = st.form_submit_button(t["btn_reg"], type="primary", use_container_width=True)
                    if reg_submitted:
                        if not new_user or not new_pass:
                            st.error("Vui lòng điền đủ thông tin." if lang=="Tiếng Việt" else "Please fill all fields.")
                        else:
                            pwd_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,20}$'
                            if not re.match(pwd_pattern, new_pass):
                                st.error(t["pwd_error"])
                            else:
                                if "users_db" not in st.session_state: st.session_state["users_db"] = {}
                                if new_user in st.session_state["users_db"]:
                                    st.error("Tài khoản đã tồn tại!" if lang=="Tiếng Việt" else "Account already exists!")
                                else:
                                    st.session_state["users_db"][new_user] = {"password": new_pass, "role": role_sel, "wallet_balance": 100000.0}
                                    st.session_state["reg_success_data"] = {"user": new_user, "role": role_sel}
                                    st.rerun()

    # ================= CỘT PHẢI: GIÃN CÁCH THOÁNG ĐÃNG + LÁ CỜ MỞ RỘNG PHÁT SÁNG =================
    with col_info:
        st.markdown(f"""
            <div class="hardcore-green-card">
                <div class="section-title-custom">{t["achieve"]}</div>
                <div style="display:flex; justify-content:space-around; align-items:center; margin-top:2px;">
                    <div style="text-align:center;">
                        <div class="stat-value-custom">{t["ach_1_val"]}</div>
                        <div class="stat-label-custom">{t["ach_1_lbl"]}</div>
                    </div>
                    <div style="text-align:center;">
                        <div class="stat-value-custom" style="color:#4ade80;">{t["ach_2_val"]}</div>
                        <div class="stat-label-custom">{t["ach_2_lbl"]}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="hardcore-green-card">
                <div class="section-title-custom">{t["projects"]}</div>
                <div class="project-title-custom">{t["proj_name"]}</div>
                <div class="project-desc-custom">{t["proj_desc"]}</div>
                <div style="text-align:right;">
                    <span class="verified-badge-custom">{t["proj_badge"]}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="hardcore-green-card">
                <div class="section-title-custom">{t["vision_title"]}</div>
                <div class="project-desc-custom">{t["vision_desc"]}</div>
                <div style="text-align:right;">
                    <span class="verified-badge-custom" style="border-color:#38bdf8; color:#38bdf8; background:rgba(56,189,248,0.15);">{t["vision_badge"]}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # LÁ CỜ VIỆT NAM ĐƯỢC MỞ RỘNG TO - PHÁT SÁNG ĐỎ & NGÔI SAO VÀNG PHÁT SÁNG
        st.markdown(f"""
            <div class="vn-flag-card-expanded">
                <div>
                    <div style="font-size:0.95rem; font-weight:800; color:#ef4444; letter-spacing:0.5px;">{t["flag_title"]}</div>
                    <div style="font-size:0.78rem; color:#cbd5e1; margin-top:3px; line-height:1.35;">{t["flag_desc"]}</div>
                </div>
                <div class="flag-box-glowing" title="Cộng hòa Xã hội Chủ nghĩa Việt Nam">
                    <svg viewBox="0 0 30 20" width="40" height="26" class="flag-star-svg">
                        <polygon points="15,3.5 17.3,10.2 24.3,10.2 18.6,14.3 20.8,21 15,16.8 9.2,21 11.4,14.3 5.7,10.2 12.7,10.2" fill="#ffff00"/>
                    </svg>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Thanh tin tức chân trang
    st.markdown(f"""
    <div class="news-ticker-container">
        <div style="font-weight:900; color:#fc8181; margin-right:15px; white-space:nowrap; text-transform:uppercase; font-size:0.8rem;">{t['news_lbl']}</div>
        <div class="news-marquee">
            <span>{t['news_txt']} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {t['news_txt']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
