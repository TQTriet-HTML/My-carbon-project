import streamlit as st

AUTH_TEXTS = {
    "Tiếng Việt": {
        "header_title": "MỘT CÚ CHẠM - VẠN ĐIỀU XANH",
        "header_sub": "Chào mừng đến với Sàn giao dịch Tín chỉ Carbon tiên phong. Nơi công nghệ vệ tinh AI hội tụ cùng sứ mệnh bảo vệ Trái Đất.",
        "welcome_box": "XIN CHÀO QUÝ ĐỒNG HÀNH!",
        "tabs": ["ĐĂNG NHẬP", "TẠO TÀI KHOẢN", "GIỚI THIỆU"],
        "user_label": "Tên đăng nhập",
        "user_placeholder": "admin, investor, buyer",
        "pass_label": "Mật khẩu",
        "login_btn": "XÁC THỰC TRUY CẬP",
        "register_user": "Tên đăng nhập mới",
        "register_pass": "Mật khẩu",
        "register_role": "Vai trò tham gia",
        "roles": ["Doanh nghiệp mua tín chỉ", "Nhà đầu tư từ xa (Cổ đông)", "Chủ rừng / Kỹ sư MRV"],
        "register_btn": "TẠO TÀI KHOẢN MỚI",
        "stats_title": "THÀNH TỰU NỀN TẢNG",
        "stat_vol_val": "2.5M+",
        "stat_vol_lbl": "Tấn Carbon Giao Dịch",
        "stat_area_val": "15,000",
        "stat_area_lbl": "Hecta Rừng Được Bảo Vệ",
        "project_title": "DỰ ÁN TIÊU BIỂU",
        "project_name": "Dự án Rừng ngập mặn Cà Mau",
        "project_desc": "Bảo vệ sinh khối & đa dạng sinh học ven biển.",
        "project_badge": "Đã xác thực AI (Verified)",
        "intro_p1": "Nền tảng tích hợp trí tuệ nhân tạo (GEE) phân tích sinh khối vệ tinh thời gian thực.",
        "intro_p2": "Giao dịch tín chỉ carbon minh bạch, loại bỏ 'rừng ma' và hỗ trợ vốn đầu tư lâm nghiệp xanh.",
        "login_err": "Tên đăng nhập hoặc mật khẩu không chính xác!",
        "reg_fill_err": "Vui lòng nhập đầy đủ thông tin!",
        "reg_exist_err": "Tên đăng nhập đã tồn tại!",
        "reg_success": "Đăng ký thành công! Hãy chuyển sang tab Đăng nhập."
    },
    "English": {
        "header_title": "ONE TOUCH - ENDLESS GREEN",
        "header_sub": "Welcome to the pioneer Carbon Credit Exchange. Where satellite AI technology converges with the mission to heal Earth.",
        "welcome_box": "WELCOME GREEN COMPANION!",
        "tabs": ["LOGIN", "REGISTER", "ABOUT"],
        "user_label": "Username",
        "user_placeholder": "admin, investor, buyer",
        "pass_label": "Password",
        "login_btn": "AUTHENTICATE ACCESS",
        "register_user": "New Username",
        "register_pass": "Password",
        "register_role": "Participation Role",
        "roles": ["Corporate Buyer", "Remote Investor", "Forest Owner / MRV Eng."],
        "register_btn": "CREATE ACCOUNT",
        "stats_title": "PLATFORM ACHIEVEMENTS",
        "stat_vol_val": "2.5M+",
        "stat_vol_lbl": "Carbon Tons Traded",
        "stat_area_val": "15,000",
        "stat_area_lbl": "Hectares Protected",
        "project_title": "FEATURED PROJECT",
        "project_name": "Ca Mau Mangrove Project",
        "project_desc": "Protecting biomass & coastal biodiversity.",
        "project_badge": "AI Verified",
        "intro_p1": "Real-time AI spatial monitoring platform integrated with satellite Earth Engine.",
        "intro_p2": "Transparent carbon marketplace, eliminating 'ghost forests' and powering green capital.",
        "login_err": "Invalid username or password!",
        "reg_fill_err": "Please complete all fields!",
        "reg_exist_err": "Username already exists!",
        "reg_success": "Registration successful! Please proceed to login."
    }
}

def hien_thi_cong_dang_nhap(lang="Tiếng Việt", is_light=False):
    txt = AUTH_TEXTS.get(lang, AUTH_TEXTS["Tiếng Việt"])
    
    # Biến màu sắc theo chế độ Sáng/Tối
    text_sub = "#475569" if is_light else "#cbd5e1"
    bg_auth_block = "rgba(255, 255, 255, 0.95)" if is_light else "linear-gradient(135deg, rgba(26, 32, 44, 0.95), rgba(45, 55, 72, 0.95))"

    st.markdown(f"""
        <style>
        /* 1. HIỆU ỨNG CHỮ LƯỚT SÓNG & VẦNG SÁNG DƯỚI CHÂN (Chu kỳ 10s) */
        @keyframes waveUp {{
            0%, 15%, 100% {{ transform: translateY(0); }}
            7.5% {{ transform: translateY(-15px); }}
        }}
        @keyframes glowUnder {{
            0%, 15%, 100% {{ opacity: 0; box-shadow: 0 0 0px transparent; }}
            7.5% {{ opacity: 1; box-shadow: 0 10px 15px #48bb78, 0 5px 10px #48bb78; }}
        }}
        .slogan-container {{
            font-size: clamp(26px, 3.5vw, 46px); font-weight: 900;
            text-align: center; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px;
        }}
        .slogan-word {{
            display: inline-block; position: relative; margin-right: 12px;
            background: linear-gradient(to right, #48bb78, #63b3ed);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: waveUp 10s infinite ease-in-out;
            animation-delay: var(--delay);
        }}
        .slogan-word::after {{
            content: ''; position: absolute; bottom: -5px; left: 0; width: 100%; height: 3px;
            background: #48bb78; border-radius: 2px;
            animation: glowUnder 10s infinite ease-in-out;
            animation-delay: var(--delay);
        }}

        /* 2. CHỮ "XIN CHÀO QUÝ ĐỒNG HÀNH" ĐỔI MÀU (Xanh lá -> Xanh dương) */
        @keyframes greenToBlue {{
            0%, 100% {{ color: #48bb78; text-shadow: 0 0 8px rgba(72,187,120,0.4); }}
            50% {{ color: #3182ce; text-shadow: 0 0 8px rgba(49,130,206,0.4); }}
        }}
        .welcome-text {{
            font-weight: 900; text-align: center; letter-spacing: 1.5px;
            margin-bottom: 20px; text-transform: uppercase;
            animation: greenToBlue 4s infinite ease-in-out;
        }}

        /* 3. KHỐI TRÁI: FORM ĐĂNG NHẬP (Giữ luồng quét sáng) */
        @keyframes leftAuthGlow {{
            0%, 100% {{ box-shadow: 0 0 15px rgba(72, 187, 120, 0.3); border-color: rgba(72, 187, 120, 0.5); }}
            50% {{ box-shadow: 0 0 35px rgba(72, 187, 120, 0.8); border-color: rgba(72, 187, 120, 1); }}
        }}
        @keyframes sweepLight {{
            0% {{ left: -100%; }} 20% {{ left: 100%; }} 100% {{ left: 100%; }}
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auth-marker) {{
            background: {bg_auth_block} !important; border: 2px solid #48bb78 !important; border-radius: 16px !important;
            padding: 25px !important; animation: leftAuthGlow 4s infinite ease-in-out !important;
            position: relative; overflow: hidden !important; transition: transform 0.4s ease !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auth-marker)::after {{
            content: ''; position: absolute; top: 0; left: -100%; width: 60%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
            transform: skewX(-25deg); animation: sweepLight 6s infinite linear; z-index: 10; pointer-events: none;
        }}

        /* 4. HAI KHỐI BÊN PHẢI: Lóa sáng xanh lá, nổi lên khi trỏ chuột */
        @keyframes rightGreenGlow {{
            0%, 100% {{ box-shadow: 0 0 10px rgba(72, 187, 120, 0.2); border-color: rgba(72, 187, 120, 0.4); }}
            50% {{ box-shadow: 0 0 25px rgba(72, 187, 120, 0.7); border-color: #48bb78; }}
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.right-glow-marker) {{
            background: {bg_auth_block} !important;
            animation: rightGreenGlow 3s infinite ease-in-out !important;
            transition: transform 0.4s ease !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.right-glow-marker):hover {{
            transform: translateY(-6px) scale(1.02) !important;
            box-shadow: 0 15px 35px rgba(72, 187, 120, 0.9) !important;
        }}

        /* Nút bấm Đăng nhập */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auth-marker) button[kind="primary"] {{
            background: linear-gradient(135deg, #2f855a 0%, #276749 100%) !important; border: 1px solid #48bb78 !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auth-marker) button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important; box-shadow: 0 0 20px rgba(72, 187, 120, 0.7) !important; transform: translateY(-2px);
        }}
        </style>
    """, unsafe_allow_html=True)

    # Tách từng chữ cho hiệu ứng lướt sóng (Mỗi chữ delay thêm 0.2s)
    title_words = txt['header_title'].split()
    title_html = "".join([f'<span class="slogan-word" style="--delay: {idx * 0.2}s;">{w}</span>' for idx, w in enumerate(title_words)])

    st.markdown(f"""
        <div style="text-align: center; margin-top: 10px; margin-bottom: 35px;">
            <div class="slogan-container">{title_html}</div>
            <p style="color: {text_sub}; font-size: 1.05rem; max-width: 820px; margin: 0 auto; line-height: 1.6;">
                {txt['header_sub']}
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    # CỘT TRÁI: KHỐI FORM ĐĂNG NHẬP / ĐĂNG KÝ
    with col_left:
        with st.container(border=True):
            st.markdown("<div class='auth-marker'></div>", unsafe_allow_html=True)
            st.markdown(f"<h3 class='welcome-text'>{txt['welcome_box']}</h3>", unsafe_allow_html=True)

            t_login, t_reg, t_intro = st.tabs(txt["tabs"])

            with t_login:
                with st.form("form_login_main", clear_on_submit=False):
                    username = st.text_input(txt["user_label"], placeholder=txt["user_placeholder"]).strip().lower()
                    password = st.text_input(txt["pass_label"], type="password")
                    btn_login = st.form_submit_button(txt["login_btn"], type="primary", use_container_width=True)

                    if btn_login:
                        db = st.session_state.get("users_db", {})
                        if username in db and db[username]["password"] == password:
                            st.session_state["logged_in"] = True
                            st.session_state["current_user"] = username
                            st.session_state["current_role"] = db[username]["role"]
                            st.rerun()
                        else:
                            st.error(txt["login_err"])

            with t_reg:
                with st.form("form_reg_main", clear_on_submit=True):
                    new_user = st.text_input(txt["register_user"]).strip().lower()
                    new_pass = st.text_input(txt["register_pass"], type="password")
                    new_role = st.selectbox(txt["register_role"], txt["roles"])
                    btn_reg = st.form_submit_button(txt["register_btn"], type="primary", use_container_width=True)

                    if btn_reg:
                        db = st.session_state.get("users_db", {})
                        if not new_user or not new_pass:
                            st.error(txt["reg_fill_err"])
                        elif new_user in db:
                            st.error(txt["reg_exist_err"])
                        else:
                            role_map = {"Corporate Buyer": "Doanh nghiệp mua tín chỉ", "Remote Investor": "Nhà đầu tư từ xa (Cổ đông)", "Forest Owner / MRV Eng.": "Chủ rừng / Kỹ sư MRV"}
                            final_role = role_map.get(new_role, new_role)
                            st.session_state["users_db"][new_user] = {"password": new_pass, "role": final_role}
                            st.success(txt["reg_success"])

            with t_intro:
                st.markdown(f"""
                    <div style="color: {text_sub}; line-height: 1.8; font-size: 0.98rem; padding: 10px 5px;">
                        <p>🌱 {txt['intro_p1']}</p>
                        <p>🛡 {txt['intro_p2']}</p>
                    </div>
                """, unsafe_allow_html=True)

    # CỘT PHẢI: KHỐI THÀNH TỰU & DỰ ÁN TIÊU BIỂU
    with col_right:
        # 1. Thành tựu
        with st.container(border=True):
            st.markdown("<div class='right-glow-marker'></div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style="border-left: 3px solid #48bb78; padding-left: 10px; margin-bottom: 20px;">
                    <span style="color: {text_sub}; font-weight: 900; font-size: 1.05rem; letter-spacing: 1px; text-transform: uppercase;">
                        {txt['stats_title']}
                    </span>
                </div>
            """, unsafe_allow_html=True)

            c_st1, c_st2 = st.columns(2)
            with c_st1:
                st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 2.2rem; font-weight: 900; color: #63b3ed; line-height: 1.1;">{txt['stat_vol_val']}</div>
                        <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 6px;">{txt['stat_vol_lbl']}</div>
                    </div>
                """, unsafe_allow_html=True)
            with c_st2:
                st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 2.2rem; font-weight: 900; color: #48bb78; line-height: 1.1;">{txt['stat_area_val']}</div>
                        <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 6px;">{txt['stat_area_lbl']}</div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # 2. Dự án tiêu biểu
        with st.container(border=True):
            st.markdown("<div class='right-glow-marker'></div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style="border-left: 3px solid #63b3ed; padding-left: 10px; margin-bottom: 15px;">
                    <span style="color: {text_sub}; font-weight: 900; font-size: 1.05rem; letter-spacing: 1px; text-transform: uppercase;">
                        {txt['project_title']}
                    </span>
                </div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #48bb78; margin-bottom: 8px;">
                    {txt['project_name']}
                </div>
                <div style="color: {text_sub}; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px;">
                    {txt['project_desc']}
                </div>
                <div style="text-align: right;">
                    <span style="background: rgba(72, 187, 120, 0.15); border: 1px solid rgba(72, 187, 120, 0.6); color: #48bb78; padding: 6px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 700;">
                        {txt['project_badge']}
                    </span>
                </div>
            """, unsafe_allow_html=True)
