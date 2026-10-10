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

      // 2 Lá bự 45 độ (Gân lá màu nâu)
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

        // Gân chính màu nâu
        c.strokeStyle = '#78350f';
        c.lineWidth = 2.0;
        c.beginPath();
        c.moveTo(0, 0);
        c.quadraticCurveTo(3, -25, 7, -50);
        c.stroke();

        // Gân nhánh màu nâu
        c.strokeStyle = 'rgba(120, 53, 15, 0.85)';
        c.lineWidth = 1.3;
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

    // DÒNG CHỮ LƯỢN SÓNG 1 LẦN DUY NHẤT KÈM ÁNH SÁNG LÓA
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
          c.fillStyle = '#ffffff';
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

    function enforceRealDOMStyles() {{
      try {{
        const doc = window.parent.document;
        
        // TIÊU ĐỀ LƯỚT MÀU TỪNG CHỮ CÁI TỪ TRÁI SANG PHẢI
        const welcomeEls = [doc.getElementById('welcomeHeading'), doc.getElementById('welcomeHeadingReg')];
        welcomeEls.forEach(el => {{
          if (el && !el.dataset.wrapped) {{
            const text = el.innerText.trim();
            el.innerHTML = '';
            for (let i = 0; i < text.length; i++) {{
              const span = doc.createElement('span');
              span.innerText = text[i] === ' ' ? '\\u00A0' : text[i];
              span.style.animation = `smoothLetterShift 4s ease-in-out infinite`;
              // Tăng delay dần đều từ trái sang phải
              span.style.animationDelay = `${{i * 0.12}}s`;
              span.style.display = 'inline-block';
              el.appendChild(span);
            }}
            el.dataset.wrapped = 'true';
          }}
        }});

        // STYLE NÚT: XÁC THỰC TRUY CẬP, TẠO MỚI TÀI KHOẢN, ĐĂNG NHẬP NGAY (MÀU XANH LÁ + KHỐI 3D + ĐỒNG BỘ NỔI BỔNG)
        const greenBtns = [
            doc.querySelector('.st-key-btn_login_submit button'), 
            doc.querySelector('.st-key-btn_reg_submit button'),
            doc.querySelector('.st-key-btn_auto_login_key button') // BỔ SUNG NÚT ĐĂNG NHẬP NGAY
        ];
        
        greenBtns.forEach(btn => {{
          if (btn && !btn.dataset.customizedGreen) {{
            btn.dataset.customizedGreen = 'true';
            btn.style.setProperty('background', 'linear-gradient(180deg, #22c55e 0%, #16a34a 100%)', 'important');
            btn.style.setProperty('border', '1.5px solid #4ade80', 'important');
            btn.style.setProperty('box-shadow', '0 5px 0 #15803d, 0 8px 18px rgba(34, 197, 94, 0.45)', 'important');
            btn.style.setProperty('border-radius', '10px', 'important');
            btn.style.setProperty('transition', 'all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)', 'important');

            const texts = btn.querySelectorAll('*');
            texts.forEach(t => t.style.setProperty('color', '#ffffff', 'important'));
            
            btn.addEventListener('mouseenter', () => {{
              btn.style.setProperty('transform', 'translateY(-3px) scale(1.02)', 'important');
              btn.style.setProperty('box-shadow', '0 8px 0 #15803d, 0 14px 26px rgba(34, 197, 94, 0.75)', 'important');
              btn.style.setProperty('background', 'linear-gradient(180deg, #4ade80 0%, #22c55e 100%)', 'important');
            }});
            btn.addEventListener('mouseleave', () => {{
              btn.style.setProperty('transform', 'translateY(0) scale(1)', 'important');
              btn.style.setProperty('box-shadow', '0 5px 0 #15803d, 0 8px 18px rgba(34, 197, 94, 0.45)', 'important');
              btn.style.setProperty('background', 'linear-gradient(180deg, #22c55e 0%, #16a34a 100%)', 'important');
            }});
            btn.addEventListener('mousedown', () => {{
              btn.style.setProperty('transform', 'translateY(3px) scale(0.98)', 'important');
              btn.style.setProperty('box-shadow', '0 2px 0 #15803d, 0 4px 10px rgba(34, 197, 94, 0.4)', 'important');
            }});
          }}
        }});

        // STYLE NÚT: KHÁM PHÁ SỨ MỆNH (MÀU XANH DƯƠNG CÔNG NGHỆ)
        const btnMission = doc.querySelector('.st-key-btn_mission_submit button');
        if (btnMission && !btnMission.dataset.customizedBlue) {{
          btnMission.dataset.customizedBlue = 'true';
          btnMission.style.setProperty('background', 'linear-gradient(180deg, #0284c7 0%, #0369a1 100%)', 'important');
          btnMission.style.setProperty('border', '1.8px solid #38bdf8', 'important');
          btnMission.style.setProperty('box-shadow', '0 5px 0 #075985, 0 0 18px rgba(56, 189, 248, 0.65)', 'important');
          btnMission.style.setProperty('border-radius', '10px', 'important');
          btnMission.style.setProperty('transition', 'all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)', 'important');

          const texts2 = btnMission.querySelectorAll('*');
          texts2.forEach(t => t.style.setProperty('color', '#ffffff', 'important'));

          btnMission.addEventListener('mouseenter', () => {{
            btnMission.style.setProperty('transform', 'translateY(-3px) scale(1.02)', 'important');
            btnMission.style.setProperty('box-shadow', '0 8px 0 #075985, 0 0 28px rgba(56, 189, 248, 0.95)', 'important');
            btnMission.style.setProperty('background', 'linear-gradient(180deg, #38bdf8 0%, #0284c7 100%)', 'important');
          }});
          btnMission.addEventListener('mouseleave', () => {{
            btnMission.style.setProperty('transform', 'translateY(0) scale(1)', 'important');
            btnMission.style.setProperty('box-shadow', '0 5px 0 #075985, 0 0 18px rgba(56, 189, 248, 0.65)', 'important');
            btnMission.style.setProperty('background', 'linear-gradient(180deg, #0284c7 0%, #0369a1 100%)', 'important');
          }});
          btnMission.addEventListener('mousedown', () => {{
            btnMission.style.setProperty('transform', 'translateY(3px) scale(0.98)', 'important');
            btnMission.style.setProperty('box-shadow', '0 2px 0 #075985, 0 4px 10px rgba(56, 189, 248, 0.4)', 'important');
          }});
        }}
      }} catch(e) {{}}
    }}

    function animate() {{
      const now = performance.now();
      const elapsed = (now - startTime) % CYCLE;
      ctx.clearRect(0, 0, logicalW, logicalH);
      
      enforceRealDOMStyles();

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
            "tab_login": "ĐĂNG NHẬP", "tab_reg": "TẠO TÀI KHOẢN",
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
            "flag_desc": "Vận hành theo Nghị định 06/2022/NĐ-CP<br/>& Đề án thị trường Carbon",
            "news_lbl": "TIN MỚI NHẤT:", "news_txt": "Thị trường Tín chỉ Carbon Việt Nam chính thức bước vào giai đoạn vận hành thí điểm."
        },
        "English": {
            "slogan": "ONE TOUCH - ONE GREEN WORLD",
            "subtitle": "Welcome to the pioneer Carbon Credit Exchange. AI satellite technology meets Earth protection mission.",
            "tab_login": "LOGIN", "tab_reg": "REGISTER",
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
            "flag_desc": "Operating under Decree 06/2022/ND-CP<br/>& National Carbon Market Project",
            "news_lbl": "LATEST NEWS:", "news_txt": "Vietnam's Carbon Credit Market officially begins pilot operation."
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

    st.markdown("""
        <style>
        /* PHÔNG NỀN ĐEN TUYỀN CÙNG CỰC QUANG XANH LÁ & XANH DƯƠNG XEN KẼ */
        @keyframes gentleStreamFlow {
            0% { background-position: 0% 40%; }
            50% { background-position: 100% 60%; }
            100% { background-position: 0% 40%; }
        }

        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #000000 !important;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.2) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(14, 165, 233, 0.2) 0%, transparent 40%),
                radial-gradient(circle at 80% 20%, rgba(5, 150, 105, 0.15) 0%, transparent 35%),
                radial-gradient(circle at 20% 80%, rgba(37, 99, 235, 0.15) 0%, transparent 40%),
                linear-gradient(130deg, #000000 0%, rgba(8, 42, 29, 0.6) 30%, #000000 50%, rgba(8, 29, 51, 0.6) 70%, #000000 100%) !important;
            background-size: 250% 250% !important;
            animation: gentleStreamFlow 32s ease-in-out infinite !important;
        }

        html, body, [data-testid="stAppViewContainer"], .main {
            overflow: hidden !important;
            height: 100vh !important;
            max-height: 100vh !important;
        }

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

        /* KHỐI FORM BÊN TRÁI HIỆU ỨNG NỔI LÊN KHI TRỎ CHUỘT VÀO */
        div[data-testid="stForm"] {
            background: linear-gradient(135deg, rgba(13, 31, 60, 0.88), rgba(18, 42, 77, 0.86)) !important;
            backdrop-filter: blur(14px) !important;
            border: 2px solid rgba(72, 187, 120, 0.6) !important;
            border-radius: 16px !important;
            padding: 14px 20px !important;
            animation: greenBreathePulse 4s infinite ease-in-out !important;
            position: relative;
            overflow: hidden !important;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease !important;
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
            transform: translateY(-4px) scale(1.015) !important;
            box-shadow: 0 16px 45px rgba(72, 187, 120, 0.95) !important;
            border-color: #48bb78 !important;
        }

        /* LƯỚT MÀU TỪNG CHỮ CÁI TỪ TRÁI SANG PHẢI */
        @keyframes smoothLetterShift {
            0%, 100% {
                color: #4ade80 !important;
                text-shadow: 0 0 15px rgba(74, 222, 128, 0.9), 0 0 5px rgba(74, 222, 128, 0.6);
            }
            50% {
                color: #38bdf8 !important;
                text-shadow: 0 0 18px rgba(56, 189, 248, 0.9), 0 0 6px rgba(56, 189, 248, 0.6);
            }
        }

        /* HIỆU ỨNG NỔI LÊN CỦA CÁC KHỐI KHI ĐƯỢC TRỎ CHUỘT VÀO */
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
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease, border-color 0.3s ease !important;
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
            transform: translateY(-4px) scale(1.015) !important;
            box-shadow: 0 16px 45px rgba(72, 187, 120, 0.95) !important;
            border-color: #48bb78 !important;
        }

        /* LÁ CỜ VIỆT NAM QUÉT SÁNG TỪ TRÁI SANG PHẢI VÀ NỞ ÊM ÁI CHẬM RÃI */
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

        /* LÓA SÁNG QUÉT TỪ TRÁI SANG PHẢI */
        @keyframes sweepGoldenGlowTextL2R {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        .nation-title-sweeping {
            font-size: 0.98rem;
            font-weight: 900;
            letter-spacing: 0.8px;
            background: linear-gradient(90deg, #ef4444 0%, #ef4444 40%, #fde047 50%, #ffffff 52%, #fde047 54%, #ef4444 60%, #ef4444 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 6px rgba(253, 224, 71, 0.6));
            animation: sweepGoldenGlowTextL2R 5.5s linear infinite;
        }

        /* NỞ RA THU LẠI TỪ TỪ CHẬM RÃI MỖI 6 GIÂY (ÊM ÁI) */
        @keyframes flagBreatheBloom {
            0%, 100% {
                transform: scale(1);
                box-shadow: 0 0 12px rgba(218, 37, 29, 0.85);
            }
            50% {
                transform: scale(1.08);
                box-shadow: 0 0 25px rgba(218, 37, 29, 1), 0 0 45px rgba(239, 68, 68, 0.8);
            }
        }
        .flag-box-glowing {
            width: 90px;
            height: 60px;
            background: #da251d;
            border-radius: 4px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            animation: flagBreatheBloom 6s ease-in-out infinite;
            flex-shrink: 0;
        }

        @keyframes starYellowGlow {
            0%, 100% { filter: drop-shadow(0 0 4px #ffff00) drop-shadow(0 0 8px #facc15); }
            50% { filter: drop-shadow(0 0 8px #ffff00) drop-shadow(0 0 16px #eab308); }
        }
        .flag-star-svg {
            animation: starYellowGlow 2.5s infinite ease-in-out;
        }

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
    
    with col_form:
        tab_dang_nhap, tab_dang_ky = st.tabs([t["tab_login"], t["tab_reg"]])
        with tab_dang_nhap:
            with st.form("form_login"):
                st.markdown(f"""
                    <div id="welcomeHeading" style="text-align:center; margin-bottom:14px; font-size:1.22rem; font-weight:900; letter-spacing:1px; transition: color 0.3s ease;">
                        {t["welcome_msg"]}
                    </div>
                """, unsafe_allow_html=True)

                u_name = st.text_input(t["user"], placeholder="admin, investor, buyer")
                u_pass = st.text_input(t["pass"], type="password", placeholder="••••••")
                
                col_btn_log, col_btn_mis = st.columns([0.55, 0.45])
                with col_btn_log:
                    submitted = st.form_submit_button(t["btn_login"], key="btn_login_submit", use_container_width=True)
                with col_btn_mis:
                    open_mission = st.form_submit_button(t["btn_mission"], key="btn_mission_submit", use_container_width=True)
                
                if submitted:
                    users = st.session_state.get("users_db", {})
                    if u_name in users and users[u_name]["password"] == u_pass:
                        st.session_state["logged_in"] = True
                        st.session_state["current_user"] = u_name
                        st.session_state["current_role"] = users[u_name]["role"]
                        st.rerun()
                    else:
                        st.error("Thôngத்துtin không chính xác." if lang=="Tiếng Việt" else "Invalid credentials.")
                
                if open_mission:
                    hien_thi_hop_thoai_su_menh()
            
            components.html(get_particle_logo_html(lang), height=150, scrolling=False)
                        
        with tab_dang_ky:
            if st.session_state["reg_success_data"]:
                registered_user = st.session_state['reg_success_data']['user']
                account_txt = t["account_label"]
                st.markdown(f"""
                    <div class="hardcore-green-card" style="text-align:center; padding: 20px 14px; margin-top: 10px; margin-bottom: 24px !important;">
                        <div style="color:#4ade80; font-weight:800; margin-bottom:8px; font-size:1.05rem; letter-spacing:0.5px;">{t['reg_success_line1']}<br/>{t['reg_success_line2']}</div>
                        <div style="color:#cbd5e1; margin-bottom: 0px; font-size:0.95rem;">{account_txt}: <b style="color:#38bdf8; font-size:1.1rem;">{registered_user}</b></div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(t["btn_auto_login"], key="btn_auto_login_key", use_container_width=True):
                    data = st.session_state["reg_success_data"]
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = data["user"]
                    st.session_state["current_role"] = data["role"]
                    st.session_state["reg_success_data"] = None
                    st.rerun()
            else:
                with st.form("form_register", clear_on_submit=True):
                    st.markdown(f"""
                        <div id="welcomeHeadingReg" style="text-align:center; margin-bottom:12px; font-size:1.15rem; font-weight:800; letter-spacing:0.8px;">
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
                    reg_submitted = st.form_submit_button(t["btn_reg"], key="btn_reg_submit", use_container_width=True)
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
            <div class="hardcore-green-card">
                <div class="section-title-custom">{t["vision_title"]}</div>
                <div class="project-desc-custom">{t["vision_desc"]}</div>
                <div style="text-align:right;">
                    <span class="verified-badge-custom" style="border-color:#38bdf8; color:#38bdf8; background:rgba(56,189,248,0.15);">{t["vision_badge"]}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="vn-flag-card-expanded">
                <div>
                    <div class="nation-title-sweeping">{t["flag_title"]}</div>
                    <div style="font-size:0.78rem; color:#cbd5e1; margin-top:5px; line-height:1.45;">{t["flag_desc"]}</div>
                </div>
                <div class="flag-box-glowing" title="Cộng hòa Xã hội Chủ nghĩa Việt Nam">
                    <svg viewBox="0 0 90 60" width="90" height="60" class="flag-star-svg">
                        <polygon points="45.00,12.00 49.04,24.44 62.12,24.44 51.54,32.12 55.58,44.56 45.00,36.88 34.42,44.56 38.46,32.12 27.88,24.44 40.96,24.44" fill="#ffff00"/>
                    </svg>
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
