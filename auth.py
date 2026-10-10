import streamlit as st
import streamlit.components.v1 as components
import re
from mission_animation import hien_thi_hop_thoai_su_menh

def get_particle_logo_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      * { box-sizing: border-box; margin: 0; padding: 0; }
      body {
        background: transparent;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }
      canvas {
        display: block;
        background: transparent;
      }
    </style>
    </head>
    <body>
    <canvas id="logoCanvas"></canvas>
    <script>
    const canvas = document.getElementById('logoCanvas');
    const ctx = canvas.getContext('2d');

    // CẤU HÌNH HIGH-DPI RETINA ĐỂ HÌNH ẢNH MỊN MÀNG SẮC NÉT TUYỆT ĐỐI
    const logicalW = 420;
    const logicalH = 175;
    const dpr = window.devicePixelRatio || 2;
    canvas.width = logicalW * dpr;
    canvas.height = logicalH * dpr;
    canvas.style.width = logicalW + 'px';
    canvas.style.height = logicalH + 'px';
    ctx.scale(dpr, dpr);

    const cx = logicalW / 2;
    const cy = 88;
    const R = 44; // PHÓNG TO LOGO KHÔNG CẦN KHUNG VIỀN

    // HÀM VẼ LOGO VECTOR NGUYÊN BẢN (KHÔNG Ô PIXEL, KHÔNG RĂNG CƯA)
    function renderVectorLogo(c, alpha = 1.0, scale = 1.0) {
      if (alpha <= 0.001) return;
      c.save();
      c.globalAlpha = alpha;
      c.translate(cx, cy);
      c.scale(scale, scale);
      c.translate(-cx, -cy);

      // 1. QUẢ CẦU TRÁI ĐẤT
      c.save();
      c.beginPath();
      c.arc(cx, cy, R, 0, Math.PI * 2);
      c.fillStyle = '#7dd3fc';
      c.fill();
      c.lineWidth = 4.2;
      c.strokeStyle = '#0f172a';
      c.stroke();
      c.clip();

      // CÁC MẢNG LỤC ĐỊA MỊN MÀNG
      c.fillStyle = '#4ade80';
      c.strokeStyle = '#0f172a';
      c.lineWidth = 3.2;

      // Lục địa đỉnh
      c.beginPath();
      c.moveTo(cx - 10, cy - R);
      c.bezierCurveTo(cx - 7, cy - 30, cx + 10, cy - 28, cx + 14, cy - R);
      c.closePath();
      c.fill(); c.stroke();

      // Lục địa góc trên trái
      c.beginPath();
      c.moveTo(cx - R, cy - 26);
      c.bezierCurveTo(cx - 24, cy - 34, cx - 20, cy - 10, cx - 34, cy + 2);
      c.bezierCurveTo(cx - 44, cy + 8, cx - R, cy + 10, cx - R, cy - 26);
      c.closePath();
      c.fill(); c.stroke();

      // Lục địa góc dưới trái
      c.beginPath();
      c.moveTo(cx - 30, cy + 12);
      c.bezierCurveTo(cx - 10, cy + 15, cx - 14, cy + 38, cx - 26, cy + 42);
      c.bezierCurveTo(cx - 38, cy + 42, cx - 36, cy + 26, cx - 30, cy + 12);
      c.closePath();
      c.fill(); c.stroke();

      // Lục địa góc phải
      c.beginPath();
      c.moveTo(cx + 24, cy - 30);
      c.bezierCurveTo(cx + 16, cy - 10, cx + 36, cy - 4, cx + 24, cy + 10);
      c.bezierCurveTo(cx + 16, cy + 22, cx + 36, cy + 26, cx + R, cy + 12);
      c.bezierCurveTo(cx + R, cy - 24, cx + 38, cy - 34, cx + 24, cy - 30);
      c.closePath();
      c.fill(); c.stroke();

      // Vùng nước xanh đáy
      c.fillStyle = '#38bdf8';
      c.beginPath();
      c.ellipse(cx + 12, cy + 33, 16, 7.5, 0, 0, Math.PI * 2);
      c.fill();

      // KHUÔN MẶT ĐÁNG YÊU
      c.fillStyle = '#0f172a';
      c.beginPath();
      c.arc(cx - 13, cy + 2, 3.2, 0, Math.PI * 2);
      c.arc(cx + 13, cy + 2, 3.2, 0, Math.PI * 2);
      c.fill();

      c.beginPath();
      c.arc(cx, cy + 7, 4.6, 0.15 * Math.PI, 0.85 * Math.PI);
      c.lineWidth = 2.6;
      c.lineCap = 'round';
      c.stroke();

      // Má hồng
      c.fillStyle = '#f87171';
      c.beginPath();
      c.arc(cx - 22, cy + 10, 4.0, 0, Math.PI * 2);
      c.arc(cx + 22, cy + 10, 4.0, 0, Math.PI * 2);
      c.fill();

      c.restore();

      c.beginPath();
      c.arc(cx, cy, R, 0, Math.PI * 2);
      c.lineWidth = 4.2;
      c.strokeStyle = '#0f172a';
      c.stroke();

      // 2. MẦM CÂY TRÊN ĐẦU: THÂN NÂU DÀY + LÁ MẦM XANH ĐẬM (KHÔNG BÓNG CHÓI)
      c.save();
      c.translate(cx, cy - R);
      c.strokeStyle = '#0f172a';
      c.lineWidth = 7.5;
      c.lineCap = 'round';
      c.beginPath();
      c.moveTo(0, 2); c.lineTo(0, -13);
      c.stroke();

      c.strokeStyle = '#78350f';
      c.lineWidth = 4.8;
      c.beginPath();
      c.moveTo(0, 1); c.lineTo(0, -12);
      c.stroke();

      c.beginPath();
      c.ellipse(-9, -15, 9.0, 5.8, -Math.PI / 5, 0, Math.PI * 2);
      c.fillStyle = '#14532d';
      c.fill();
      c.lineWidth = 2.5;
      c.strokeStyle = '#0f172a';
      c.stroke();

      c.beginPath();
      c.ellipse(9, -15, 9.0, 5.8, Math.PI / 5, 0, Math.PI * 2);
      c.fillStyle = '#14532d';
      c.fill();
      c.lineWidth = 2.5;
      c.strokeStyle = '#0f172a';
      c.stroke();
      c.restore();

      // 3. HAI CHIẾC LÁ LỚN PHÍA TRƯỚC XÒE 45 ĐỘ (GÂN TRẮNG NỔI BẬT)
      function drawBigLeaf(angle, isFlipped) {
        c.save();
        c.translate(cx + (isFlipped ? 15 : -15), cy + 34);
        c.rotate(angle);
        if (isFlipped) c.scale(-1, 1);

        c.beginPath();
        c.moveTo(0, 0);
        c.bezierCurveTo(22, -15, 28, -48, 8, -60);
        c.bezierCurveTo(-8, -48, -13, -15, 0, 0);
        c.fillStyle = '#22c55e';
        c.fill();
        c.strokeStyle = '#0f172a';
        c.lineWidth = 3.2;
        c.stroke();

        // Gân lá chính màu trắng
        c.strokeStyle = '#ffffff';
        c.lineWidth = 1.9;
        c.beginPath();
        c.moveTo(0, 0);
        c.quadraticCurveTo(4, -28, 8, -57);
        c.stroke();

        // Gân nhánh trắng
        c.strokeStyle = 'rgba(255, 255, 255, 0.85)';
        c.lineWidth = 1.2;
        c.beginPath();
        c.moveTo(1, -14); c.lineTo(9, -21);
        c.moveTo(3, -28); c.lineTo(13, -36);
        c.moveTo(5, -42); c.lineTo(13, -48);
        c.moveTo(1, -14); c.lineTo(-6, -19);
        c.moveTo(3, -28); c.lineTo(-5, -33);
        c.stroke();

        c.restore();
      }

      drawBigLeaf(-Math.PI / 4, false);
      drawBigLeaf(Math.PI / 4, true);

      c.restore();
    }

    // 2. KHỞI TẠO CÁC TINH THỂ HẠT ÁNH SÁNG BAY VÒNG TRÒN (KHÔNG PHẢI Ô PIXEL VUÔNG)
    const NUM_PARTICLES = 160;
    const particles = [];
    const colors = ['#4ade80', '#22c55e', '#38bdf8', '#7dd3fc', '#86efac', '#60a5fa'];

    for (let i = 0; i < NUM_PARTICLES; i++) {
      const baseAngle = (i / NUM_PARTICLES) * Math.PI * 2;
      const targetRadius = 25 + Math.random() * 45; // Vị trí xuất phát từ các điểm trên logo
      particles.push({
        baseAngle: baseAngle,
        currentAngle: baseAngle,
        orbitRadius: 75 + Math.random() * 85, // Quỹ đạo bay vòng xung quanh logo
        speed: (0.012 + Math.random() * 0.016) * (Math.random() < 0.5 ? 1 : -1),
        targetX: cx + Math.cos(baseAngle) * targetRadius,
        targetY: cy + Math.sin(baseAngle) * targetRadius * 0.85,
        x: cx,
        y: cy,
        size: 1.2 + Math.random() * 1.8,
        color: colors[i % colors.length],
        alpha: 0
      });
    }

    // 3. CHU KỲ CHUYỂN ĐỘNG CHẬM RÃI 16 GIÂY (16000ms):
    // - 0s -> 6s (6 GIÂY): LOGO VECTOR NÉT CĂNG NGUYÊN BẢN (ĐỨNG YÊN HOÀN CHỈNH)
    // - 6s -> 11s (5 GIÂY): TAN RÃ CHẬM RÃI, CÁC HẠT BAY TẠO VÒNG TRÒN QUANH LOGO
    // - 11s -> 16s (5 GIÂY): CÁC HẠT TỪ TỪ HỘI TỤ VÀ TÁI HIỆN LẠI LOGO VECTOR BAN ĐẦU
    const CYCLE = 16000;
    const startTime = performance.now();

    function animate() {
      const now = performance.now();
      const elapsed = (now - startTime) % CYCLE;
      ctx.clearRect(0, 0, logicalW, logicalH);

      if (elapsed < 6000) {
        // GIAI ĐOẠN 1: LOGO HOÀN CHỈNH VECTOR MỊN MÀNG 100% (ĐỨNG YÊN 6 GIÂY)
        renderVectorLogo(ctx, 1.0, 1.0);
      } else if (elapsed < 11000) {
        // GIAI ĐOẠN 2: TAN RÃ CHẬM RÃI -> CÁC HẠT BAY TẠO VÒNG TRÒN XUNG QUANH
        const disperseProg = (elapsed - 6000) / 5000;
        const logoAlpha = Math.max(0, 1 - disperseProg * 2.2);

        // Logo mờ dần
        if (logoAlpha > 0) {
          renderVectorLogo(ctx, logoAlpha, 1.0 + disperseProg * 0.05);
        }

        // Các hạt tỏa ra và bay vòng tròn xung quanh khu vực logo
        for (let i = 0; i < NUM_PARTICLES; i++) {
          const p = particles[i];
          p.currentAngle += p.speed;

          // Bán kính nở dần ra tạo thành vòng xoay xung quanh
          const currentR = p.orbitRadius * Math.min(1, disperseProg * 1.4);
          p.x = cx + Math.cos(p.currentAngle) * currentR;
          p.y = cy + Math.sin(p.currentAngle) * (currentR * 0.72); // Quỹ đạo hình elip mềm mại

          p.alpha = Math.min(0.9, disperseProg * 1.8);

          ctx.save();
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.globalAlpha = p.alpha;
          ctx.shadowColor = p.color;
          ctx.shadowBlur = 6;
          ctx.fill();
          ctx.restore();
        }
      } else {
        // GIAI ĐOẠN 3: TỪ TỪ HỘI TỤ LẠI TỪ CÁC VÒNG TRÒN VÀ TÁI HIỆN LOGO
        const assembleProg = (elapsed - 11000) / 5000;
        const easeIn = Math.pow(assembleProg, 2);

        // Các hạt xoắn ốc thu nhỏ vòng bay và hút dần về tâm
        for (let i = 0; i < NUM_PARTICLES; i++) {
          const p = particles[i];
          p.currentAngle += p.speed * 0.7;

          // Khoảng cách thu dần từ quỹ đạo về các điểm logo
          const currentR = p.orbitRadius * (1 - easeIn);
          const orbitX = cx + Math.cos(p.currentAngle) * currentR;
          const orbitY = cy + Math.sin(p.currentAngle) * (currentR * 0.72);

          // Nội suy mượt mà về vị trí đích
          p.x = orbitX * (1 - easeIn) + p.targetX * easeIn;
          p.y = orbitY * (1 - easeIn) + p.targetY * easeIn;
          p.alpha = Math.max(0.1, 1 - assembleProg * 0.85);

          ctx.save();
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.globalAlpha = p.alpha;
          ctx.shadowColor = p.color;
          ctx.shadowBlur = 4;
          ctx.fill();
          ctx.restore();
        }

        // Logo vector nét căng xuất hiện dần trở lại khi các hạt hội tụ
        if (assembleProg > 0.35) {
          const appearAlpha = (assembleProg - 0.35) / 0.65;
          renderVectorLogo(ctx, appearAlpha, 0.95 + appearAlpha * 0.05);
        }
      }

      requestAnimationFrame(animate);
    }

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
            "news_lbl": "LATEST NEWS:", "news_txt": "Vietnam's Carbon Credit Market officially begins pilot operation."
        }
    }
    t = T.get(lang, T["Tiếng Việt"])
    text_sub = "#cbd5e1"

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

        .block-container {
            padding-top: 1.6rem !important;
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
            padding: 12px 18px !important;
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

        /* 3 KHỐI BÊN PHẢI PHỦ KÍNH MỜ */
        .hardcore-green-card {
            background: linear-gradient(135deg, rgba(6, 44, 25, 0.88) 0%, rgba(10, 61, 35, 0.86) 100%) !important;
            backdrop-filter: blur(14px) !important;
            border: 2px solid #22c55e !important;
            border-radius: 14px !important;
            padding: 10px 16px !important;
            margin-bottom: 8px !important;
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

        button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
            border: 1.5px solid #4ade80 !important;
            color: white !important;
            font-weight: 800 !important;
            letter-spacing: 0.8px !important;
            border-radius: 9px !important;
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.45) !important;
            transition: all 0.3s ease !important;
            margin-top: 2px !important;
            padding: 6px 14px !important;
        }
        button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%) !important;
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 10px 25px rgba(34, 197, 94, 0.8) !important;
        }

        .slogan-wrapper {
            text-align: center;
            padding-top: 8px;
            padding-bottom: 2px;
            overflow: visible !important;
            white-space: nowrap;
        }

        @keyframes waveUp {
            0%, 20%, 100% { transform: translateY(0); text-shadow: none; }
            10% { transform: translateY(-10px); text-shadow: 0 0 20px rgba(72,187,120,1); }
        }
        .wave-char {
            display: inline-block;
            position: relative;
            margin-right: 2px;
            font-size: clamp(23px, 2.6vw, 34px) !important;
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
            font-size: 0.95rem;
            font-weight: 800;
            letter-spacing: 1.2px;
            margin-bottom: 3px;
            border-left: 4px solid #48bb78;
            padding-left: 8px;
            text-transform: uppercase;
        }
        .stat-value-custom {
            font-size: 1.65rem;
            font-weight: 900;
            color: #63b3ed;
            margin-bottom: 2px;
            line-height: 1.1;
        }
        .stat-label-custom { color: #cbd5e1; font-size: 0.8rem; font-weight: 500; }
        .project-title-custom { color: #48bb78; font-weight: 700; font-size: 1rem; margin-bottom: 2px; }
        .project-desc-custom { color: #cbd5e1; font-size: 0.78rem; margin-bottom: 4px; line-height: 1.3; }
        .verified-badge-custom {
            display: inline-block;
            background: rgba(72, 187, 120, 0.2);
            border: 1px solid #48bb78;
            color: #48bb78;
            padding: 2px 8px;
            border-radius: 5px;
            font-size: 0.72rem;
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

    wave_html = '<div class="slogan-wrapper">'
    delay = 0.0
    for char in t["slogan"]:
        char_display = "&nbsp;" if char == " " else char
        wave_html += f'<span class="wave-char" style="--delay: {delay}s;">{char_display}</span>'
        delay += 0.1
    wave_html += '</div>'
    st.markdown(wave_html, unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; color:{text_sub}; font-size:0.86rem; margin-top:2px; margin-bottom:10px;">{t["subtitle"]}</div>', unsafe_allow_html=True)

    _, col_form, col_space, col_info, _ = st.columns([0.1, 1.25, 0.08, 1.25, 0.1])
    
    with col_form:
        st.markdown(f"""
            <div style="text-align:center; margin-bottom:4px; font-size:1.1rem; font-weight:800; color:#48bb78; letter-spacing:0.8px; text-shadow:0 0 12px rgba(72,187,120,0.5);">
                {t["welcome_msg"]}
            </div>
        """, unsafe_allow_html=True)

        tab_dang_nhap, tab_dang_ky = st.tabs([t["tab_login"], t["tab_reg"]])
        with tab_dang_nhap:
            with st.form("form_login"):
                u_name = st.text_input(t["user"], placeholder="admin, investor, buyer")
                u_pass = st.text_input(t["pass"], type="password", placeholder="••••••")
                
                col_btn_log, col_btn_mis = st.columns([0.55, 0.45])
                with col_btn_log:
                    submitted = st.form_submit_button(t["btn_login"], type="primary", use_container_width=True)
                with col_btn_mis:
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
            
            # LOGO VECTOR MỊN MÀNG 100% NÉT CĂNG + HIỆU ỨNG HẠT ÁNH SÁNG BAY TẠO VÒNG & HỘI TỤ
            components.html(get_particle_logo_html(), height=175, scrolling=False)
                        
        with tab_dang_ky:
            if st.session_state["reg_success_data"]:
                registered_user = st.session_state['reg_success_data']['user']
                account_txt = t["account_label"]
                st.markdown(f"""
                    <div style="background: rgba(72,187,120,0.12); border: 1.5px solid #48bb78; text-align:center; padding: 12px 10px; border-radius:12px; margin-top: 6px;">
                        <p style="color:#48bb78; font-weight:700; margin-bottom:4px; font-size:0.92rem;">{t['reg_success_line1']} {t['reg_success_line2']}</p>
                        <p style="color:{text_sub}; margin-bottom: 0px; font-size:0.88rem;">{account_txt}: <b style="color:#63b3ed;">{registered_user}</b></p>
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
            <div class="hardcore-green-card" style="margin-bottom:0px;">
                <div class="section-title-custom">{t["vision_title"]}</div>
                <div class="project-desc-custom">{t["vision_desc"]}</div>
                <div style="text-align:right;">
                    <span class="verified-badge-custom" style="border-color:#38bdf8; color:#38bdf8; background:rgba(56,189,248,0.15);">{t["vision_badge"]}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="news-ticker-container">
        <div style="font-weight:900; color:#fc8181; margin-right:15px; white-space:nowrap; text-transform:uppercase; font-size:0.8rem;">{t['news_lbl']}</div>
        <div class="news-marquee">
            <span>{t['news_txt']} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {t['news_txt']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
