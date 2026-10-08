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
    bg_auth_block = "linear-gradient(135deg, rgba(13, 31, 60, 0.95), rgba(18, 42, 77, 0.92))"
    # Nền màu xanh lá sang trọng cho 2 khối bên phải
    bg_right_block = "linear-gradient(135deg, rgba(6, 44, 25, 0.95), rgba(12, 58, 34, 0.92))"

    st.markdown(f"""
        <style>
        /* TIÊU ĐỀ LÓA SÁNG TỪNG CHỮ CÂU CHÀO */
        @keyframes char-green-blue-glow {{
            0%, 100% {{ color: #48bb78; text-shadow: 0 0 4px rgba(72,187,120,0.3); }}
            50% {{ color: #63b3ed; text-shadow: 0 0 20px rgba(99,179,237,1), 0 0 8px rgba(72,187,120,0.8); transform: translateY(-2px); }}
        }}
        .welcome-container {{ text-align: center; margin-bottom: 25px; white-space: nowrap; overflow-x: auto; scrollbar-width: none; }}
        .welcome-container::-webkit-scrollbar {{ display: none; }}
        .welcome-char {{ display: inline-block; font-size: 1.3rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; animation: char-green-blue-glow 8s infinite ease-in-out; }}

        /* SLOGAN SÓNG NHẤP NHÔ 10 GIÂY */
        @keyframes waveUp {{
            0%, 20%, 100% {{ transform: translateY(0); text-shadow: none; }}
            10% {{ transform: translateY(-15px); text-shadow: 0 0 25px rgba(72,187,120,1), 0 0 10px rgba(104,211,145,0.8); }}
        }}
        .wave-text-container {{ text-align: center; margin-bottom: 10px; padding: 20px 0; white-space: nowrap; overflow-x: auto; scrollbar-width: none; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        .wave-text-container::-webkit-scrollbar {{ display: none; }}
        .wave-char {{
            display: inline-block; position: relative; margin-right: 2px; font-size: clamp(24px, 3.5vw, 42px) !important; font-weight: 900 !important;
            letter-spacing: 2px !important; background: linear-gradient(90deg, #48bb78, #68d391, #319795); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: waveUp 10s infinite ease-in-out; animation-delay: var(--delay);
        }}
        .hero-subtitle {{ text-align: center; color: {text_sub}; font-size: 1.05rem; font-weight: 400; margin-bottom: 40px; padding: 0 20px; }}

        /* HIỆU ỨNG THỞ VÀ QUÉT SÁNG */
        @keyframes greenNeonBreath {{
            0%, 100% {{ 
                box-shadow: 0 0 16px rgba(72, 187, 120, 0.28), inset 0 0 15px rgba(72, 187, 120, 0.08); 
                border-color: rgba(72, 187, 120, 0.5) !important; 
            }}
            50% {{ 
                box-shadow: 0 0 38px rgba(72, 187, 120, 0.8), inset 0 0 25px rgba(72, 187, 120, 0.2); 
                border-color: #48bb78 !important; 
            }}
        }}

        @keyframes autoSweepRight10s {{ 
            0%, 85%   {{ left: -100%; opacity: 0; }} 
            86%       {{ opacity: 1; left: -100%; }}
            95%       {{ left: 200%; opacity: 0.9; }} 
            100%      {{ left: 200%; opacity: 0; }} 
        }}

        /* ÁP DỤNG CHO KHỐI FORM BÊN TRÁI */
        div[data-testid="stForm"] {{
            background: {bg_auth_block} !important;
            border: 2px solid rgba(72, 187, 120, 0.6) !important;
            border-radius: 18px !important;
            padding: 24px !important;
            animation: greenNeonBreath 4s infinite ease-in-out !important;
            position: relative; 
            overflow: hidden !important; 
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.35s ease, border-color 0.35s ease !important;
            margin-bottom: 20px !important;
        }}
        div[data-testid="stForm"]::after {{
            content: ''; 
            position: absolute; 
            top: 0; 
            left: -100%; 
            width: 55%; 
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.65), transparent);
            transform: skewX(-25deg); 
            animation: autoSweepRight10s 10s infinite linear; 
            z-index: 10; 
            pointer-events: none;
        }}
        div[data-testid="stForm"]:hover {{
            transform: translateY(-8px) scale(1.02) !important;
            box-shadow: 0 22px 50px rgba(72, 187, 120, 0.92), inset 0 0 25px rgba(72, 187, 120, 0.4) !important;
            border-color: #48bb78 !important;
            z-index: 5 !important;
        }}

        /* ============================================================
           HIỆU ỨNG VÀ NỀN MÀU XANH LÁ CHO 2 KHỐI KẾ BÊN PHẢI
           ============================================================ */
        .auth-info-card {{
            background: {bg_right_block} !important;
            border: 2px solid rgba(72, 187, 120, 0.6) !important;
            border-radius: 18px !important;
            padding: 24px !important;
            margin-bottom: 22px !important;
            animation: greenNeonBreath 4s infinite ease-in-out !important;
            position: relative;
            overflow: hidden !important;
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.35s ease, border-color 0.35s ease !important;
        }}
        .auth-info-card::after {{
            content: ''; 
            position: absolute; 
            top: 0; 
            left: -100%; 
            width: 55%; 
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.65), transparent);
            transform: skewX(-25deg); 
            animation: autoSweepRight10s 10s infinite linear; 
            z-index: 10; 
            pointer-events: none;
        }}
        .auth-info-card:hover {{
            transform: translateY(-8px) scale(1.02) !important;
            box-shadow: 0 22px 50px rgba(72, 187, 120, 0.92), inset 0 0 25px rgba(72, 187, 120, 0.4) !important;
            border-color: #48bb78 !important;
            z-index: 5 !important;
        }}

        /* TAB VÀ NÚT BẤM */
        button[data-baseweb="tab"] {{
            color: #94a3b8 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: #48bb78 !important;
            border-bottom-color: #48bb78 !important;
            text-shadow: 0 0 12px rgba(72, 187, 120, 0.8) !important;
        }}
        div[data-baseweb="tab-highlight"] {{
            background-color: #48bb78 !important;
            box-shadow: 0 0 15px rgba(72, 187, 120, 0.9) !important;
        }}

        button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button {{
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
            border: 1.5px solid #4ade80 !important;
            color: white !important; 
            font-weight: 900 !important; 
            letter-spacing: 1px !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 18px rgba(34, 197, 94, 0.45) !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            margin-top: 15px !important;
        }}
        button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] button:hover {{
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%) !important;
            transform: translateY(-4px) scale(1.03) !important; 
            box-shadow: 0 12px 30px rgba(34, 197, 94, 0.85), inset 0 0 12px rgba(255, 255, 255, 0.4) !important; 
            border-color: #86efac !important;
        }}

        .section-title {{ 
            color: #ffffff; 
            font-size: 1.15rem; 
            font-weight: 800; 
            letter-spacing: 1.5px; 
            margin-bottom: 22px; 
            border-left: 5px solid #48bb78; 
            padding-left: 12px; 
            text-transform: uppercase; 
        }}
        .stat-value {{ 
            font-size: 2.3rem; 
            font-weight: 900; 
            color: #63b3ed; 
            margin-bottom: 5px; 
            line-height: 1.1; 
            letter-spacing: 0.5px;
        }}
        .stat-label {{ color: {text_sub}; font-size: 0.92rem; font-weight: 500; }}
        .project-title {{ color: #48bb78; font-weight: 700; font-size: 1.25rem; margin-bottom: 10px; }}
        .project-desc {{ color: {text_sub}; font-size: 0.95rem; margin-bottom: 16px; line-height: 1.5; }}
        .verified-badge {{ 
            display: inline-block; 
            background: rgba(72, 187, 120, 0.15); 
            border: 1px solid #48bb78; 
            color: #48bb78; 
            padding: 6px 14px; 
            border-radius: 8px; 
            font-size: 0.82rem; 
            font-weight: 700; 
        }}
        
        .news-ticker-container {{ 
            position: fixed; 
            bottom: 0; 
            left: 0; 
            width: 100%; 
            background: rgba(15, 23, 42, 0.95); 
            border-top: 1px solid rgba(72, 187, 120, 0.3); 
            color: #e2e8f0; 
            padding: 12px 25px; 
            display: flex; 
            align-items: center; 
            z-index: 1000; 
        }}
        .news-label {{ font-weight: 900; color: #fc8181; margin-right: 20px; white-space: nowrap; text-transform: uppercase; letter-spacing: 1px; }}
        .news-marquee {{ overflow: hidden; white-space: nowrap; width: 100%; }}
        .news-marquee span {{ display: inline-block; padding-left: 100%; animation: marquee 20s linear infinite; }}
        @keyframes marquee {{ 0% {{ transform: translate(0, 0); }} 100% {{ transform: translate(-100%, 0); }} }}
        </style>
    """, unsafe_allow_html=True)

    wave_html = '<div class="wave-text-container">'
    delay = 0.0
    for char in t["slogan"]:
        char_display = "&nbsp;" if char == " " else char
        wave_html += f'<span class="wave-char" style="--delay: {delay}s;">{char_display}</span>'
        delay += 0.1
    wave_html += '</div>'

    st.markdown(wave_html, unsafe_allow_html=True)
    st.markdown(f'<div class="hero-subtitle">{t["subtitle"]}</div>', unsafe_allow_html=True)

    _, col_form, col_space, col_info, _ = st.columns([0.15, 1.25, 0.1, 1.25, 0.15])
    
    # ================= CỘT TRÁI =================
    with col_form:
        welcome_text = t["welcome_msg"]
        welcome_html = '<div class="welcome-container">'
        delay_wc = 0.0
        for char in welcome_text:
            char_display = "&nbsp;" if char == " " else char
            welcome_html += f'<span class="welcome-char" style="animation-delay: {delay_wc}s;">{char_display}</span>'
            delay_wc += 0.06
        welcome_html += '</div>'
        st.markdown(welcome_html, unsafe_allow_html=True)

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
                        <h4 style="color:#48bb78; font-weight:800; margin-bottom: 10px;">{t['reg_success_line1']} {t['reg_success_line2']}</h4>
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
                                if "users_db" not in st.session_state:
                                    st.session_state["users_db"] = {}
                                if new_user in st.session_state["users_db"]:
                                    st.error("Tài khoản đã tồn tại!" if lang=="Tiếng Việt" else "Account already exists!")
                                else:
                                    st.session_state["users_db"][new_user] = {
                                        "password": new_pass, "role": role_sel, "wallet_balance": 100000.0
                                    }
                                    st.session_state["reg_success_data"] = {"user": new_user, "role": role_sel}
                                    st.rerun()

    # ================= CỘT PHẢI: 2 KHỐI CÓ HIỆU ỨNG VÀ NỀN MÀU XANH LÁ =================
    with col_info:
        # Khối 1: Thành tựu nền tảng
        st.markdown(f"""
            <div class="auth-info-card">
                <div class="section-title">{t["achieve"]}</div>
                <div style="display:flex; justify-content:space-around; align-items:center; margin-top:15px;">
                    <div style="text-align:center;">
                        <div class="stat-value">{t["ach_1_val"]}</div>
                        <div class="stat-label">{t["ach_1_lbl"]}</div>
                    </div>
                    <div style="text-align:center;">
                        <div class="stat-value" style="color:#48bb78;">{t["ach_2_val"]}</div>
                        <div class="stat-label">{t["ach_2_lbl"]}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Khối 2: Dự án tiêu biểu
        st.markdown(f"""
            <div class="auth-info-card">
                <div class="section-title">{t["projects"]}</div>
                <div class="project-title">{t["proj_name"]}</div>
                <div class="project-desc">{t["proj_desc"]}</div>
                <div style="text-align:right;">
                    <span class="verified-badge">{t["proj_badge"]}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Thanh tin tức chạy marquee
    st.markdown(f"""
    <div class="news-ticker-container">
        <div class="news-label">{t['news_lbl']}</div>
        <div class="news-marquee">
            <span>{t['news_txt']} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {t['news_txt']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
