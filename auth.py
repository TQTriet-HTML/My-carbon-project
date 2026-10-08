import streamlit as st
import re

def hien_thi_cong_dang_nhap(lang="Tiếng Việt"):
    if "reg_success_data" not in st.session_state:
        st.session_state["reg_success_data"] = None
    if "show_intro_reg_form" not in st.session_state:
        st.session_state["show_intro_reg_form"] = False

    T = {
        "Tiếng Việt": {
            "slogan": "MỘT CÚ CHẠM - VẠN ĐIỀU XANH",
            "subtitle": "Chào mừng đến với Sàn giao dịch Tín chỉ Carbon tiên phong. Nơi công nghệ vệ tinh AI hội tụ cùng sứ mệnh bảo vệ Trái Đất.",
            "tab_login": "ĐĂNG NHẬP", "tab_reg": "TẠO TÀI KHOẢN", "tab_intro": "GIỚI THIỆU",
            "welcome_msg": "XIN CHÀO QUÝ ĐỒNG HÀNH!",
            "user": "Tên đăng nhập", "pass": "Mật khẩu",
            "btn_login": "XÁC THỰC TRUY CẬP", "btn_reg": "TẠO MỚI TÀI KHOẢN",
            "pwd_error": "Mật khẩu phải từ 8-20 ký tự, bao gồm ít nhất 1 chữ hoa, 1 chữ thường, 1 số và 1 ký tự đặc biệt.",
            "reg_success_line1": "Bạn đã đặt bước chân đầu tiên",
            "reg_success_line2": "trên chặng đường xanh!",
            "btn_auto_login": "ĐĂNG NHẬP NGAY",
            "achieve": "THÀNH TỰU NỀN TẢNG", "ach_1_val": "2.5M+", "ach_1_lbl": "Tấn Carbon Giao Dịch", "ach_2_val": "15,000", "ach_2_lbl": "Hecta Rừng Được Bảo Vệ",
            "projects": "DỰ ÁN TIÊU BIỂU", "proj_name": "Dự án Rừng ngập mặn Cà Mau", "proj_desc": "Bảo vệ sinh khối & đa dạng sinh học ven biển.", "proj_badge": "Đã xác thực AI (Verified)",
            "news_lbl": "TIN MỚI NHẤT:", "news_txt": "Thị trường Tín chỉ Carbon Việt Nam chính thức bước vào giai đoạn vận hành thí điểm."
        },
        "English": {
            "slogan": "ONE TOUCH - ONE GREEN WORLD",
            "subtitle": "Welcome to the pioneer Carbon Credit Exchange. AI satellite technology meets Earth protection mission.",
            "tab_login": "LOGIN", "tab_reg": "REGISTER", "tab_intro": "ABOUT",
            "welcome_msg": "WELCOME PARTNER!",
            "user": "Username", "pass": "Password",
            "btn_login": "AUTHENTICATE", "btn_reg": "CREATE ACCOUNT",
            "pwd_error": "Password must be 8-20 characters with uppercase, lowercase, number, and special character.",
            "reg_success_line1": "You have taken your first step",
            "reg_success_line2": "towards sustainability!",
            "btn_auto_login": "LOGIN NOW",
            "achieve": "PLATFORM ACHIEVEMENTS", "ach_1_val": "2.5M+", "ach_1_lbl": "Tons Carbon Traded", "ach_2_val": "15,000", "ach_2_lbl": "Hectares Protected",
            "projects": "FEATURED PROJECTS", "proj_name": "Ca Mau Mangrove Project", "proj_desc": "Protecting biomass & coastal biodiversity.", "proj_badge": "AI Verified",
            "news_lbl": "LATEST NEWS:", "news_txt": "Vietnam's Carbon Credit Market officially begins pilot operation."
        }
    }
    t = T.get(lang, T["Tiếng Việt"])
    text_sub = "#cbd5e1"

    # CAN THIỆP MẠNH TAY BẰNG CSS TOÀN CỤC CƯỠNG CHẾ
    st.markdown("""
        <style>
        /* Hiệu ứng thở phát sáng xanh neon */
        @keyframes greenBreathePulse {
            0%, 100% {
                box-shadow: 0 0 16px rgba(72, 187, 120, 0.35), inset 0 0 15px rgba(72, 187, 120, 0.15);
                border-color: rgba(72, 187, 120, 0.55) !important;
            }
            50% {
                box-shadow: 0 0 40px rgba(72, 187, 120, 0.9), inset 0 0 25px rgba(72, 187, 120, 0.35);
                border-color: #48bb78 !important;
            }
        }

        /* Tia sáng quét qua mỗi 10 giây */
        @keyframes sweepLight10s {
            0%, 85% { left: -120%; opacity: 0; }
            86% { opacity: 1; left: -120%; }
            95%, 100% { left: 220%; opacity: 0; }
        }

        /* KHỐI BÊN TRÁI (FORM) */
        div[data-testid="stForm"] {
            background: linear-gradient(135deg, rgba(13, 31, 60, 0.96), rgba(18, 42, 77, 0.94)) !important;
            border: 2px solid rgba(72, 187, 120, 0.6) !important;
            border-radius: 18px !important;
            padding: 24px !important;
            animation: greenBreathePulse 4s infinite ease-in-out !important;
            position: relative;
            overflow: hidden !important;
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.35s ease !important;
            margin-bottom: 20px !important;
        }
        div[data-testid="stForm"]::after {
            content: '';
            position: absolute;
            top: 0;
            left: -120%;
            width: 60%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.7), transparent);
            transform: skewX(-25deg);
            animation: sweepLight10s 10s infinite linear;
            z-index: 10;
            pointer-events: none;
        }
        div[data-testid="stForm"]:hover {
            transform: translateY(-8px) scale(1.02) !important;
            box-shadow: 0 22px 50px rgba(72, 187, 120, 0.95), inset 0 0 25px rgba(72, 187, 120, 0.45) !important;
            border-color: #48bb78 !important;
        }

        /* KHỐI BÊN PHẢI (2 KHỐI NỀN XANH LÁ CÓ HIỆU ỨNG THỞ VÀ NỔI LÊN) */
        .hardcore-green-card {
            background: linear-gradient(135deg, rgba(6, 44, 25, 0.96) 0%, rgba(10, 61, 35, 0.94) 100%) !important;
            border: 2px solid #22c55e !important;
            border-radius: 18px !important;
            padding: 24px !important;
            margin-bottom: 22px !important;
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
            width: 60%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.7), transparent);
            transform: skewX(-25deg);
            animation: sweepLight10s 10s infinite linear;
            z-index: 10;
            pointer-events: none;
        }
        .hardcore-green-card:hover {
            transform: translateY(-8px) scale(1.025) !important;
            box-shadow: 0 22px 50px rgba(72, 187, 120, 0.95), inset 0 0 30px rgba(72, 187, 120, 0.5) !important;
            border-color: #48bb78 !important;
            z-index: 5 !important;
        }

        /* Nút xác thực màu xanh lá neon */
        button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
            border: 1.5px solid #4ade80 !important;
            color: white !important;
            font-weight: 900 !important;
            letter-spacing: 1px !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 18px rgba(34, 197, 94, 0.45) !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            margin-top: 15px !important;
        }
        button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%) !important;
            transform: translateY(-4px) scale(1.03) !important;
            box-shadow: 0 12px 30px rgba(34, 197, 94, 0.85) !important;
            border-color: #86efac !important;
        }

        /* Slogan và tiêu đề sóng */
        @keyframes waveUp {
            0%, 20%, 100% { transform: translateY(0); text-shadow: none; }
            10% { transform: translateY(-15px); text-shadow: 0 0 25px rgba(72,187,120,1); }
        }
        .wave-char {
            display: inline-block; position: relative; margin-right: 2px; font-size: clamp(24px, 3.5vw, 42px) !important; font-weight: 900 !important;
            letter-spacing: 2px !important; background: linear-gradient(90deg, #48bb78, #68d391, #319795); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: waveUp 10s infinite ease-in-out; animation-delay: var(--delay);
        }

        .section-title-custom {
            color: #ffffff;
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: 1.5px;
            margin-bottom: 20px;
            border-left: 5px solid #48bb78;
            padding-left: 12px;
            text-transform: uppercase;
        }
        .stat-value-custom {
            font-size: 2.3rem;
            font-weight: 900;
            color: #63b3ed;
            margin-bottom: 5px;
            line-height: 1.1;
            letter-spacing: 0.5px;
        }
        .stat-label-custom { color: #cbd5e1; font-size: 0.92rem; font-weight: 500; }
        .project-title-custom { color: #48bb78; font-weight: 700; font-size: 1.25rem; margin-bottom: 10px; }
        .project-desc-custom { color: #cbd5e1; font-size: 0.95rem; margin-bottom: 16px; line-height: 1.5; }
        .verified-badge-custom {
            display: inline-block;
            background: rgba(72, 187, 120, 0.2);
            border: 1px solid #48bb78;
            color: #48bb78;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 700;
        }

        .news-ticker-container {
            position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(15, 23, 42, 0.95);
            border-top: 1px solid rgba(72, 187, 120, 0.3); color: #e2e8f0; padding: 12px 25px;
            display: flex; align-items: center; z-index: 1000;
        }
        .news-marquee { overflow: hidden; white-space: nowrap; width: 100%; }
        .news-marquee span { display: inline-block; padding-left: 100%; animation: marquee 20s linear infinite; }
        @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
        </style>
    """, unsafe_allow_html=True)

    # Hiển thị slogan sóng
    wave_html = '<div style="text-align: center; padding: 20px 0; white-space: nowrap;">'
    delay = 0.0
    for char in t["slogan"]:
        char_display = "&nbsp;" if char == " " else char
        wave_html += f'<span class="wave-char" style="--delay: {delay}s;">{char_display}</span>'
        delay += 0.1
    wave_html += '</div>'
    st.markdown(wave_html, unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; color:{text_sub}; font-size:1.05rem; margin-bottom:40px;">{t["subtitle"]}</div>', unsafe_allow_html=True)

    _, col_form, col_space, col_info, _ = st.columns([0.15, 1.25, 0.1, 1.25, 0.15])
    
    # CỘT TRÁI: FORM ĐĂNG NHẬP / ĐĂNG KÝ
    with col_form:
        st.markdown(f"""
            <div style="text-align:center; margin-bottom:20px; font-size:1.3rem; font-weight:900; color:#48bb78; letter-spacing:1px; text-shadow:0 0 15px rgba(72,187,120,0.5);">
                {t["welcome_msg"]}
            </div>
        """, unsafe_allow_html=True)

        tab_dang_nhap, tab_dang_ky = st.tabs([t["tab_login"], t["tab_reg"]])
        with tab_dang_nhap:
            with st.form("form_login"):
                u_name = st.text_input(t["user"], placeholder="admin, investor, buyer")
                u_pass = st.text_input(t["pass"], type="password", placeholder="••••••")
                submitted = st.form_submit_button(t["btn_login"], type="primary", use_container_width=True)
                if submitted:
                    users = st.session_state.get("users_db", {})
                    if u_name in users and users[u_name]["password"] == u_pass:
                        st.session_state["logged_in"] = True
                        st.session_state["current_user"] = u_name
                        st.session_state["current_role"] = users[u_name]["role"]
                        st.rerun()
                    else:
                        st.error("Thông tin không chính xác." if lang=="Tiếng Việt" else "Invalid credentials.")
                        
        with tab_dang_ky:
            if st.session_state["reg_success_data"]:
                st.markdown(f"""
                    <div style="background: rgba(72,187,120,0.1); border: 1px solid #48bb78; text-align:center; padding: 25px; border-radius:12px; margin-top: 15px;">
                        <h4 style="color:#48bb78; font-weight:800; margin-bottom: 10px;">{t['reg_success_line1']}<br>{t['reg_success_line2']}</h4>
                        <p style="color:{text_sub}; margin-bottom: 5px;">Tài khoản: <b style="color:#63b3ed;">{st.session_state['reg_success_data']['user']}</b></p>
                    </div>
                """, unsafe_allow_html=True)
                st.write("")
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
                    role_sel = st.selectbox("Phân loại" if lang=="Tiếng Việt" else "Role", ["Doanh nghiệp mua tín chỉ", "Chủ rừng / Kỹ sư MRV", "Nhà đầu tư từ xa (Cổ đông)"])
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

    # CỘT PHẢI: 2 KHỐI NỀN XANH LÁ + HIỆU ỨNG THỞ & NỔI LÊN TRỰC TIẾP
    with col_info:
        # Khối 1: THÀNH TỰU NỀN TẢNG (Nền xanh lá, viền neon, quét sáng 10s, hover nổi lên)
        st.markdown(f"""
            <div class="hardcore-green-card">
                <div class="section-title-custom">{t["achieve"]}</div>
                <div style="display:flex; justify-content:space-around; align-items:center; margin-top:10px;">
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

        # Khối 2: DỰ ÁN TIÊU BIỂU (Nền xanh lá, viền neon, quét sáng 10s, hover nổi lên)
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

    # Thanh tin tức chạy chân trang
    st.markdown(f"""
    <div class="news-ticker-container">
        <div style="font-weight:900; color:#fc8181; margin-right:20px; white-space:nowrap; text-transform:uppercase;">{t['news_lbl']}</div>
        <div class="news-marquee">
            <span>{t['news_txt']} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {t['news_txt']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
