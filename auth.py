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
    <canvas id="particleCanvas" width="380" height="135"></canvas>
    <script>
    const canvas = document.getElementById('particleCanvas');
    const ctx = canvas.getContext('2d');

    // 1. Vẽ logo mẫu lên canvas ảo để trích xuất các mảnh hạt
    const off = document.createElement('canvas');
    off.width = 380;
    off.height = 135;
    const octx = off.getContext('2d');

    const cx = 190;
    const cy = 70;
    const R = 30;

    // Viền xám mỏng bo góc quanh logo
    octx.strokeStyle = "rgba(148, 163, 184, 0.45)";
    octx.lineWidth = 1.3;
    octx.beginPath();
    const bx = cx - 52, by = cy - R - 18, bw = 104, bh = R * 2 + 36, rad = 14;
    octx.moveTo(bx + rad, by);
    octx.lineTo(bx + bw - rad, by);
    octx.quadraticCurveTo(bx + bw, by, bx + bw, by + rad);
    octx.lineTo(bx + bw, by + bh - rad);
    octx.quadraticCurveTo(bx + bw, by + bh, bx + bw - rad, by + bh);
    octx.lineTo(bx + rad, by + bh);
    octx.quadraticCurveTo(bx, by + bh, bx, by + bh - rad);
    octx.lineTo(bx, by + rad);
    octx.quadraticCurveTo(bx, by, bx + rad, by);
    octx.stroke();

    // Quả cầu Trái Đất
    octx.beginPath();
    octx.arc(cx, cy, R, 0, Math.PI * 2);
    octx.fillStyle = '#7dd3fc';
    octx.fill();
    octx.lineWidth = 3;
    octx.strokeStyle = '#0f172a';
    octx.stroke();

    // Mảng lục địa
    octx.save();
    octx.beginPath();
    octx.arc(cx, cy, R, 0, Math.PI * 2);
    octx.clip();
    octx.fillStyle = '#4ade80';
    octx.beginPath();
    octx.arc(cx - 14, cy - 10, 14, 0, Math.PI * 2);
    octx.arc(cx + 14, cy - 8, 12, 0, Math.PI * 2);
    octx.arc(cx - 6, cy + 17, 10, 0, Math.PI * 2);
    octx.arc(cx + 11, cy + 15, 11, 0, Math.PI * 2);
    octx.fill();

    // Mắt & Miệng hoạt hình
    octx.fillStyle = '#0f172a';
    octx.beginPath();
    octx.arc(cx - 9, cy + 2, 2.2, 0, Math.PI * 2);
    octx.arc(cx + 9, cy + 2, 2.2, 0, Math.PI * 2);
    octx.fill();
    octx.beginPath();
    octx.arc(cx, cy + 5, 3.2, 0.15 * Math.PI, 0.85 * Math.PI);
    octx.lineWidth = 1.8;
    octx.stroke();

    // Má hồng
    octx.fillStyle = '#f87171';
    octx.beginPath();
    octx.arc(cx - 15, cy + 7, 2.8, 0, Math.PI * 2);
    octx.arc(cx + 15, cy + 7, 2.8, 0, Math.PI * 2);
    octx.fill();
    octx.restore();

    // Mầm cây: Thân nâu dày dặn + lá mầm xanh đậm, không bóng chói
    octx.strokeStyle = '#0f172a';
    octx.lineWidth = 5.5;
    octx.lineCap = 'round';
    octx.beginPath();
    octx.moveTo(cx, cy - R + 2);
    octx.lineTo(cx, cy - R - 9);
    octx.stroke();
    octx.strokeStyle = '#78350f';
    octx.lineWidth = 3.5;
    octx.beginPath();
    octx.moveTo(cx, cy - R + 1);
    octx.lineTo(cx, cy - R - 8);
    octx.stroke();

    // 2 Lá mầm: Xanh lục rừng già (#14532d)
    octx.fillStyle = '#14532d';
    octx.strokeStyle = '#0f172a';
    octx.lineWidth = 1.8;
    octx.beginPath();
    octx.ellipse(cx - 7, cy - R - 11, 6.2, 4, -Math.PI / 5, 0, Math.PI * 2);
    octx.fill(); octx.stroke();
    octx.beginPath();
    octx.ellipse(cx + 7, cy - R - 11, 6.2, 4, Math.PI / 5, 0, Math.PI * 2);
    octx.fill(); octx.stroke();

    // 2 Chiếc lá bự nâng đỡ 45 độ bên dưới (có gân lá)
    function drawLeaf(ang, flip) {
      octx.save();
      octx.translate(cx + (flip ? 10 : -10), cy + 22);
      octx.rotate(ang);
      if (flip) octx.scale(-1, 1);
      octx.beginPath();
      octx.moveTo(0, 0);
      octx.bezierCurveTo(15, -10, 19, -34, 6, -42);
      octx.bezierCurveTo(-6, -34, -9, -10, 0, 0);
      octx.fillStyle = '#22c55e';
      octx.fill();
      octx.strokeStyle = '#0f172a';
      octx.lineWidth = 2;
      octx.stroke();
      octx.strokeStyle = '#ffffff';
      octx.lineWidth = 1.2;
      octx.beginPath();
      octx.moveTo(0, 0);
      octx.quadraticCurveTo(3, -20, 6, -40);
      octx.stroke();
      octx.restore();
    }
    drawLeaf(-Math.PI / 4, false);
    drawLeaf(Math.PI / 4, true);

    // 2. Trích xuất mảng các mảnh nhỏ
    const imgData = octx.getImageData(0, 0, off.width, off.height).data;
    const particles = [];
    const step = 3;
    for (let y = 0; y < off.height; y += step) {
      for (let x = 0; x < off.width; x += step) {
        const idx = (y * off.width + x) * 4;
        const a = imgData[idx + 3];
        if (a > 60) {
          const r = imgData[idx];
          const g = imgData[idx + 1];
          const b = imgData[idx + 2];
          particles.push({
            tx: x,
            ty: y,
            color: `rgba(${r},${g},${b},${a/255})`,
            x: Math.random() * off.width,
            y: Math.random() * off.height,
            size: 2.1,
            randOffset: Math.random() * 200,
            driftSpeed: 1.3 + Math.random() * 2.4,
            waveFreq: 0.02 + Math.random() * 0.03
          });
        }
      }
    }

    // 3. Chu kỳ chuyển động đúng 15 giây
    const CYCLE = 15000;
    const startTime = performance.now();

    function renderLoop() {
      const now = performance.now();
      const elapsed = (now - startTime) % CYCLE;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        if (elapsed < 3500) {
          // Giai đoạn 1 (0s -> 3.5s): Các mảnh nhỏ bay vào ráp nối thành logo
          const prog = elapsed / 3500;
          const easeOut = 1 - Math.pow(1 - Math.min(1, prog), 3);
          p.x += (p.tx - p.x) * 0.085;
          p.y += (p.ty - p.y) * 0.085;
          ctx.globalAlpha = Math.min(1, 0.35 + easeOut * 0.65);
        } else if (elapsed < 8500) {
          // Giai đoạn 2 (3.5s -> 8.5s - ĐÚNG 5 GIÂY): Logo hoàn chỉnh giữ nguyên sắc nét
          p.x = p.tx;
          p.y = p.ty;
          ctx.globalAlpha = 1.0;
        } else if (elapsed < 12500) {
          // Giai đoạn 3 (8.5s -> 12.5s): Tan rã, gió thổi cuốn các mảnh NGANG TỪ TRÁI SANG PHẢI
          const disperseProg = (elapsed - 8500) / 4000;
          p.x += (p.driftSpeed * 3.6) + (p.tx / canvas.width) * 1.6;
          p.y += Math.sin((elapsed + p.randOffset) * p.waveFreq) * 0.75;
          ctx.globalAlpha = Math.max(0.12, 1 - disperseProg * 0.88);
        } else {
          // Giai đoạn 4 (12.5s -> 15s): Các mảnh trôi dạt bay vòng về bên trái chuẩn bị tụ lại
          const prepProg = (elapsed - 12500) / 2500;
          if (p.x > canvas.width + 40) {
            p.x = -30 - Math.random() * 90;
            p.y = p.ty + (Math.random() - 0.5) * 50;
          }
          p.x += (p.tx - p.x) * 0.05;
          p.y += (p.ty - p.y) * 0.05;
          ctx.globalAlpha = 0.3 + prepProg * 0.7;
        }

        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, p.size, p.size);
      }

      ctx.globalAlpha = 1.0;
      requestAnimationFrame(renderLoop);
    }

    renderLoop();
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
        /* HIỆU ỨNG LUỒNG MÀU XANH LÁ & XANH DƯƠNG CHUYỂN DỊCH ÊM ÁI (28 GIÂY) */
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
            padding-top: 1.8rem !important;
            padding-bottom: 1.5rem !important;
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
            padding-top: 10px;
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

        /* Thanh tin tức chân trang */
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

    # KHUNG SLOGAN CHUẨN CỐ ĐỊNH PHÍA TRÊN
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
    
    # CỘT TRÁI: FORM ĐĂNG NHẬP + LOGO HẠT HOẠT HỌA PHÍA DƯỚI
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
            
            # LOGO HẠT HOẠT HỌA ĐẶT NGAY BÊN DƯỚI FORM ĐĂNG NHẬP
            components.html(get_particle_logo_html(), height=135, scrolling=False)
                        
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

    # CỘT PHẢI: 3 KHỐI THÔNG TIN
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

    # Thanh tin tức chân trang
    st.markdown(f"""
    <div class="news-ticker-container">
        <div style="font-weight:900; color:#fc8181; margin-right:15px; white-space:nowrap; text-transform:uppercase; font-size:0.8rem;">{t['news_lbl']}</div>
        <div class="news-marquee">
            <span>{t['news_txt']} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {t['news_txt']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
