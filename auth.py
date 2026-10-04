import streamlit as st

def hien_thi_cong_dang_nhap(lang="Tiếng Việt"):
    # --- CSS TOÀN CỤC CHO TRANG ĐĂNG NHẬP (KHÔNG ICON, HIỆU ỨNG SÁNG & HOẠT HỌA CAO CẤP) ---
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #090d16 0%, #111827 50%, #064e3b 100%) !important;
        }
        
        /* HIỆU ỨNG CHỮ LƯỢN SÓNG (WAVE EFFECT) THEO CỤM MỖI 10 GIÂY */
        @keyframes wave-animation {
            0%, 85% { transform: translateY(0); filter: drop-shadow(0 0 0 transparent); }
            90% { transform: translateY(-8px); filter: drop-shadow(0 0 12px rgba(104, 211, 145, 0.8)); }
            95% { transform: translateY(4px); }
            100% { transform: translateY(0); filter: drop-shadow(0 0 0 transparent); }
        }
        
        .wave-text {
            text-align: center;
            margin-bottom: 5px;
        }
        .wave-text span {
            display: inline-block;
            font-size: clamp(26px, 3vw, 36px) !important;
            font-weight: 900 !important;
            letter-spacing: 2px !important;
            background: linear-gradient(90deg, #48bb78, #68d391, #319795);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: wave-animation 10s infinite ease-in-out;
            padding: 0 5px;
        }

        .hero-subtitle {
            text-align: center;
            color: #a0aec0;
            font-size: 1.05rem;
            font-weight: 400;
            margin-bottom: 35px;
            letter-spacing: 0.5px;
        }

        /* --- HIỆU ỨNG LÓA SÁNG VÀ LƯỚT SÁNG XANH LÁ (SWEEP SHINE) CHO CÁC KHỐI --- */
        div[data-testid="stVerticalBlockBorderWrapper"], .side-card {
            background: rgba(17, 24, 39, 0.85) !important;
            border: 1px solid rgba(72, 187, 120, 0.3) !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(72, 187, 120, 0.05) !important;
            backdrop-filter: blur(12px);
            position: relative;
            overflow: hidden !important;
            transition: all 0.4s ease !important;
        }

        /* Khi Hover: Lóa sáng viền xanh lá mạnh hơn */
        div[data-testid="stVerticalBlockBorderWrapper"]:hover, .side-card:hover {
            border-color: #48bb78 !important;
            box-shadow: 0 15px 35px rgba(72, 187, 120, 0.3), inset 0 0 20px rgba(72, 187, 120, 0.2) !important;
            transform: translateY(-3px);
        }

        /* Lưỡi dao ánh sáng xanh lướt qua (Sweep Shine) */
        div[data-testid="stVerticalBlockBorderWrapper"]::after, .side-card::after {
            content: ''; 
            position: absolute; 
            top: 0; 
            left: -150%; 
            width: 60%; 
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.35), transparent);
            transform: skewX(-25deg); 
            transition: left 0.65s ease-in-out; 
            pointer-events: none;
            z-index: 10;
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"]:hover::after, .side-card:hover::after { 
            left: 150%; 
        }

        /* NÚT BẤM ĐỎ GỐC CỦA HỆ THỐNG */
        button[kind="primary"] {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important; 
            border: none !important;
            color: white !important;
            font-weight: 700 !important;
            letter-spacing: 1px;
            transition: all 0.3s ease !important;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.6) !important;
            transform: translateY(-2px);
        }

        *:focus, *:active { outline: none !important; }
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { border-color: #2d3748 !important; }
        div[data-baseweb="select"]:hover, div[data-baseweb="input"]:hover,
        div[data-baseweb="select"]:focus-within, div[data-baseweb="input"]:focus-within {
            border-color: #48bb78 !important;
            box-shadow: 0 0 12px rgba(72, 187, 120, 0.4) !important;
        }
        [aria-invalid="true"] { border-color: #48bb78 !important; }

        /* CSS THÀNH TỰU VÀ DỰ ÁN TIÊU BIỂU */
        .section-title {
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 800;
            letter-spacing: 1.5px;
            margin-bottom: 20px;
            border-left: 4px solid #48bb78;
            padding-left: 10px;
            text-transform: uppercase;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: 900;
            color: #63b3ed;
            margin-bottom: 0;
            line-height: 1.2;
        }
        .stat-label {
            color: #a0aec0;
            font-size: 0.85rem;
        }
        .project-title {
            color: #48bb78;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 8px;
        }
        .project-desc {
            color: #cbd5e0;
            font-size: 0.9rem;
            margin-bottom: 12px;
        }
        .verified-badge {
            display: inline-block;
            background: rgba(72, 187, 120, 0.1);
            border: 1px solid #48bb78;
            color: #48bb78;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* TIN TỨC CHẠY (NEWS TICKER) */
        .news-ticker-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: rgba(15, 23, 42, 0.95);
            border-top: 1px solid rgba(72, 187, 120, 0.3);
            color: #e2e8f0;
            padding: 10px 20px;
            display: flex;
            align-items: center;
            z-index: 1000;
        }
        .news-label {
            font-weight: 800;
            color: #fc8181;
            margin-right: 15px;
            white-space: nowrap;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .news-marquee {
            overflow: hidden;
            white-space: nowrap;
            width: 100%;
        }
        .news-marquee span {
            display: inline-block;
            padding-left: 100%;
            animation: marquee 20s linear infinite;
        }
        @keyframes marquee {
            0% { transform: translate(0, 0); }
            100% { transform: translate(-100%, 0); }
        }
        </style>
    """, unsafe_allow_html=True)

    # --- BỘ TỪ ĐIỂN TEXT CHUẨN XÁC KÈM SLOGAN MỚI ---
    T = {
        "Tiếng Việt": {
            "slogan_chunks": ["MỘT CÚ CHẠM", "-", "VẠN ĐIỀU XANH"],
            "subtitle": "Chào mừng đến với Sàn giao dịch Tín chỉ Carbon tiên phong. Nơi công nghệ vệ tinh AI hội tụ cùng sứ mệnh bảo vệ Trái Đất.",
            "tab_login": "ĐĂNG NHẬP", "tab_reg": "TẠO TÀI KHOẢN",
            "sys_access": "Hệ thống Truy cập",
            "user": "Tên đăng nhập", "pass": "Mật khẩu",
            "btn_login": "XÁC THỰC TRUY CẬP", "btn_reg": "TẠO MỚI TÀI KHOẢN",
            "achieve": "THÀNH TỰU NỀN TẢNG",
            "ach_1_val": "2.5M+", "ach_1_lbl": "Tấn Carbon Giao Dịch",
            "ach_2_val": "15,000", "ach_2_lbl": "Hecta Rừng Được Bảo Vệ",
            "projects": "DỰ ÁN TIÊU BIỂU",
            "proj_name": "Dự án Rừng ngập mặn Cà Mau",
            "proj_desc": "Bảo vệ sinh khối & đa dạng sinh học ven biển.",
            "proj_badge": "Đã xác thực AI (Verified)",
            "news_lbl": "TIN MỚI NHẤT:",
            "news_txt": "Thị trường Tín chỉ Carbon Việt Nam chính thức bước vào giai đoạn vận hành thí điểm."
        },
        "English": {
            "slogan_chunks": ["ONE TOUCH", "-", "ONE GREEN WORLD"],
            "subtitle": "Welcome to the pioneer Carbon Credit Exchange. Where AI satellite tech meets the mission to protect the Earth.",
            "tab_login": "LOGIN", "tab_reg": "CREATE ACCOUNT",
            "sys_access": "System Access",
            "user": "Username", "pass": "Password",
            "btn_login": "Login to Platform", "btn_reg": "Register Account",
            "achieve": "PLATFORM ACHIEVEMENTS",
            "ach_1_val": "2.5M+", "ach_1_lbl": "Tons Carbon Traded",
            "ach_2_val": "15,000", "ach_2_lbl": "Hectares Protected",
            "projects": "FEATURED PROJECTS",
            "proj_name": "Ca Mau Mangrove Project",
            "proj_desc": "Protecting biomass & coastal biodiversity.",
            "proj_badge": "AI Verified",
            "news_lbl": "LATEST NEWS:",
            "news_txt": "Vietnam's Carbon Credit Market officially begins pilot operation."
        }
    }
    t = T[lang]

    # --- TẠO HIỆU ỨNG CHỮ LƯỢN SÓNG (WAVE TEXT) THEO CỤM TỪ ---
    wave_html = '<div class="wave-text">'
    delay = 0.0
    for chunk in t["slogan_chunks"]:
        wave_html += f'<span style="animation-delay: {delay}s;">{chunk}</span>'
        delay += 0.15  # Các cụm sẽ lượn sóng nhịp nhàng tiếp nối nhau
    wave_html += '</div>'

    st.markdown(wave_html, unsafe_allow_html=True)
    st.markdown(f'<div class="hero-subtitle">{t["subtitle"]}</div>', unsafe_allow_html=True)

    # --- BỐ CỤC 2 CỘT NHƯ GỐC ---
    col_form, col_space, col_info = st.columns([1.1, 0.1, 1.1])
    
    with col_form:
        # Form đăng nhập (Tự động nhận hiệu ứng Glow & Sweep Shine từ CSS)
        with st.container(border=True):
            st.markdown(f'<h3 style="color: white; margin-top: 0; font-weight: 700; font-size: 1.2rem;">{t["sys_access"]}</h3>', unsafe_allow_html=True)
            tab_dang_nhap, tab_dang_ky = st.tabs([t["tab_login"], t["tab_reg"]])
            
            with tab_dang_nhap:
                with st.form("form_login"):
                    u_name = st.text_input(t["user"], placeholder="admin, investor, buyer")
                    u_pass = st.text_input(t["pass"], type="password", placeholder="••••••")
                    
                    submitted = st.form_submit_button(t["btn_login"], type="primary", use_container_width=True)
                    
                    if submitted:
                        db = st.session_state["users_db"]
                        if u_name in db and db[u_name]["password"] == u_pass:
                            st.session_state["logged_in"] = True
                            st.session_state["current_user"] = u_name
                            st.session_state["current_role"] = db[u_name]["role"]
                            st.rerun()
                        else:
                            st.error("Thông tin không chính xác." if lang=="Tiếng Việt" else "Invalid credentials.")

            with tab_dang_ky:
                with st.form("form_register"):
                    new_user = st.text_input("Tên tài khoản mới" if lang=="Tiếng Việt" else "New Username")
                    new_pass = st.text_input("Mật khẩu" if lang=="Tiếng Việt" else "Password", type="password")
                    role_sel = st.selectbox("Phân loại tài khoản" if lang=="Tiếng Việt" else "Account Role", ["Doanh nghiệp mua tín chỉ", "Chủ rừng / Kỹ sư MRV", "Nhà đầu tư từ xa (Cổ đông)"])
                    
                    reg_submitted = st.form_submit_button(t["btn_reg"], type="primary", use_container_width=True)
                    
                    if reg_submitted:
                        if new_user and new_pass:
                            if new_user in st.session_state["users_db"]:
                                st.error("Tài khoản đã tồn tại." if lang=="Tiếng Việt" else "Account already exists.")
                            else:
                                st.session_state["users_db"][new_user] = {"password": new_pass, "role": role_sel}
                                st.success("Tạo thành công!" if lang=="Tiếng Việt" else "Created successfully!")
                        else:
                            st.error("Vui lòng điền đủ thông tin." if lang=="Tiếng Việt" else "Please fill all fields.")

    with col_info:
        # Khối Thành tựu (Tự động nhận hiệu ứng Glow & Sweep Shine từ lớp .side-card)
        st.markdown(f"""
        <div class="side-card">
            <div class="section-title">{t['achieve']}</div>
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <div class="stat-value">{t['ach_1_val']}</div>
                    <div class="stat-label">{t['ach_1_lbl']}</div>
                </div>
                <div>
                    <div class="stat-value">{t['ach_2_val']}</div>
                    <div class="stat-label">{t['ach_2_lbl']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Khối Dự án Tiêu biểu (Tự động nhận hiệu ứng Glow & Sweep Shine)
        st.markdown(f"""
        <div class="side-card">
            <div class="section-title">{t['projects']}</div>
            <div class="project-title">{t['proj_name']}</div>
            <div class="project-desc">{t['proj_desc']}</div>
            <span class="verified-badge">{t['proj_badge']}</span>
        </div>
        """, unsafe_allow_html=True)

    # --- TIN TỨC CHẠY (NEWS TICKER) ---
    st.markdown(f"""
    <div class="news-ticker-container">
        <div class="news-label">{t['news_lbl']}</div>
        <div class="news-marquee">
            <span>{t['news_txt']} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {t['news_txt']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
