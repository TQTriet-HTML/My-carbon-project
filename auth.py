import streamlit as st
import re

def hien_thi_cong_dang_nhap(lang="Tiếng Việt"):
    if "reg_success_data" not in st.session_state:
        st.session_state["reg_success_data"] = None

    # --- CSS TOÀN CỤC CHO TRANG ĐĂNG NHẬP ---
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #090d16 0%, #111827 50%, #064e3b 100%) !important;
        }
        
        /* CĂN BẰNG VÀ CĂN GIỮA 3 TAB TRUY CẬP */
        div.stTabs > div[data-baseweb="tab-list"] {
            display: flex !important;
            justify-content: space-between !important;
            width: 100% !important;
            gap: 0 !important;
        }
        div.stTabs button[data-baseweb="tab"] {
            flex: 1 1 0% !important;
            justify-content: center !important;
            text-align: center !important;
            transition: all 0.3s ease !important; /* Thêm transition cho mượt */
        }
        
        /* HIỆU ỨNG HOVER VÀ ACTIVE CHO TAB */
        /* Khi trỏ chuột vào tab */
        div.stTabs button[data-baseweb="tab"]:hover p {
            color: #48bb78 !important; /* Chuyển chữ thành xanh lá */
            transform: scale(1.05) !important; /* Phóng to một chút */
            transition: all 0.2s ease !important;
        }
        /* Tab đang được chọn (Active) */
        div.stTabs button[aria-selected="true"] p {
            color: #48bb78 !important; /* Chữ màu xanh lá */
            font-weight: bold !important;
            transform: scale(1.05) !important; /* Phóng to */
        }
        /* Màu vạch highlight dưới tab đang chọn */
        div[data-baseweb="tab-highlight"] {
            background-color: #48bb78 !important;
        }
        
        /* HOẠT HỌA CÂU SLOGAN CHÍNH */
        @keyframes letter-wave-halo {
            0%, 80% { transform: translateY(0); text-shadow: none; }
            85% { transform: translateY(-12px); text-shadow: 0 0 25px rgba(72,187,120,1), 0 0 10px rgba(104,211,145,0.8); }
            90% { transform: translateY(4px); text-shadow: 0 0 10px rgba(72,187,120,0.5); }
            100% { transform: translateY(0); text-shadow: none; }
        }
        
        .wave-text-container { text-align: center; margin-bottom: 5px; }
        .wave-char {
            display: inline-block; font-size: clamp(26px, 3.2vw, 42px) !important; font-weight: 900 !important;
            letter-spacing: 2px !important; background: linear-gradient(90deg, #48bb78, #68d391, #319795);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: letter-wave-halo 10s infinite ease-in-out;
        }
        .hero-subtitle { text-align: center; color: #a0aec0; font-size: 1.05rem; font-weight: 400; margin-bottom: 40px; }

        /* HOẠT HỌA 12S TAB GIỚI THIỆU: CHỮ XANH LÁ + HÀO QUANG XANH DƯƠNG */
        @keyframes intro-wave-blue-halo {
            0%, 85% { transform: translateY(0); text-shadow: none; }
            90% { transform: translateY(-10px); text-shadow: 0 12px 25px rgba(66,153,225,1), 0 0 15px rgba(99,179,237,0.8); }
            95% { transform: translateY(4px); text-shadow: 0 5px 10px rgba(66,153,225,0.5); }
            100% { transform: translateY(0); text-shadow: none; }
        }
        .intro-wave-char {
            display: inline-block;
            color: #48bb78; 
            font-size: 1.05rem;
            font-weight: 700;
            animation: intro-wave-blue-halo 12s infinite ease-in-out;
        }

        /* HIỆU ỨNG KHỐI KÍNH PHA LÊ CHO CÁC KHỐI BÊN PHẢI */
        div[data-testid="stVerticalBlockBorderWrapper"], .glass-block {
            background: linear-gradient(135deg, rgba(26, 32, 44, 0.95), rgba(45, 55, 72, 0.95)) !important;
            border: 1px solid rgba(72, 187, 120, 0.4) !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(72, 187, 120, 0.05) !important;
            backdrop-filter: blur(12px);
            position: relative;
            overflow: hidden !important;
            transition: all 0.4s ease !important;
            padding: 24px !important;
            margin-bottom: 20px !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover, .glass-block:hover {
            border-color: #48bb78 !important;
            box-shadow: 0 15px 35px rgba(72, 187, 120, 0.3), inset 0 0 20px rgba(72, 187, 120, 0.2) !important;
            transform: translateY(-2px);
        }
        div[data-testid="stVerticalBlockBorderWrapper"]::after, .glass-block::after {
            content: ''; position: absolute; top: 0; left: -150%; width: 60%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.25), transparent);
            transform: skewX(-25deg); transition: left 0.65s ease-in-out; pointer-events: none; z-index: 10;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover::after, .glass-block:hover::after { left: 150%; }

        /* HIỆU ỨNG LƯỚT SÁNG CHO NÚT BẤM */
        @keyframes button-shine {
            0% { left: -100%; }
            20% { left: 100%; }
            100% { left: 100%; }
        }

        /* ĐỒNG BỘ MÀU XANH LÁ + HIỆU ỨNG CHO TOÀN BỘ NÚT FORM/BUTTON */
        .stButton > button, .stFormSubmitButton > button {
            background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important; 
            border: 1px solid rgba(72, 187, 120, 0.6) !important;
            color: white !important; font-weight: 700 !important; letter-spacing: 1px;
            position: relative; overflow: hidden !important; z-index: 1;
            transition: all 0.3s ease !important;
            border-radius: 8px !important;
        }
        .stButton > button::before, .stFormSubmitButton > button::before {
            content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transform: skewX(-25deg); animation: button-shine 4s infinite ease-in-out; z-index: -1;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            box-shadow: 0 0 25px rgba(72, 187, 120, 0.9) !important; 
            transform: translateY(-2px) scale(1.02) !important; 
        }

        *:focus, *:active { outline: none !important; }
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { border-color: #2d3748 !important; }
        div[data-baseweb="select"]:hover, div[data-baseweb="input"]:hover,
        div[data-baseweb="select"]:focus-within, div[data-baseweb="input"]:focus-within {
            border-color: #48bb78 !important; box-shadow: 0 0 12px rgba(72, 187, 120, 0.4) !important;
        }
        [aria-invalid="true"] { border-color: #48bb78 !important; }

        .section-title { color: #ffffff; font-size: 1.15rem; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 25px; border-left: 5px solid #48bb78; padding-left: 12px; text-transform: uppercase; }
        .stat-value { font-size: 2.2rem; font-weight: 900; color: #63b3ed; margin-bottom: 5px; line-height: 1.1; }
        .stat-label { color: #a0aec0; font-size: 0.9rem; font-weight: 500;}
        .project-title { color: #48bb78; font-weight: 700; font-size: 1.2rem; margin-bottom: 10px; }
        .project-desc { color: #cbd5e0; font-size: 0.95rem; margin-bottom: 15px; line-height: 1.5; }
        .verified-badge { display: inline-block; background: rgba(72, 187, 120, 0.15); border: 1px solid #48bb78; color: #48bb78; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 700;}
        
        .news-ticker-container { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(15, 23, 42, 0.95); border-top: 1px solid rgba(72, 187, 120, 0.3); color: #e2e8f0; padding: 12px 25px; display: flex; align-items: center; z-index: 1000; }
        .news-label { font-weight: 900; color: #fc8181; margin-right: 20px; white-space: nowrap; text-transform: uppercase; letter-spacing: 1px; }
        .news-marquee { overflow: hidden; white-space: nowrap; width: 100%; }
        .news-marquee span { display: inline-block; padding-left: 100%; animation: marquee 20s linear infinite; }
        @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
        </style>
    """, unsafe_allow_html=True)

    T = {
        "Tiếng Việt": {
            "slogan": "MỘT CÚ CHẠM - VẠN ĐIỀU XANH",
            "subtitle": "Chào mừng đến với Sàn giao dịch Tín chỉ Carbon tiên phong. Nơi công nghệ vệ tinh AI hội tụ cùng sứ mệnh bảo vệ Trái Đất.",
            "tab_login": "ĐĂNG NHẬP", "tab_reg": "TẠO TÀI KHOẢN", "tab_intro": "GIỚI THIỆU",
            "sys_access": "HỆ THỐNG TRUY CẬP",
            "user": "Tên đăng nhập", "pass": "Mật khẩu",
            "btn_login": "XÁC THỰC TRUY CẬP", "btn_reg": "TẠO MỚI TÀI KHOẢN",
            "achieve": "THÀNH TỰU NỀN TẢNG", "ach_1_val": "2.5M+", "ach_1_lbl": "Tấn Carbon Giao Dịch", "ach_2_val": "15,000", "ach_2_lbl": "Hecta Rừng Được Bảo Vệ",
            "projects": "DỰ ÁN TIÊU BIỂU", "proj_name": "Dự án Rừng ngập mặn Cà Mau", "proj_desc": "Bảo vệ sinh khối & đa dạng sinh học ven biển.", "proj_badge": "Đã xác thực AI (Verified)",
            "news_lbl": "TIN MỚI NHẤT:", "news_txt": "Thị trường Tín chỉ Carbon Việt Nam chính thức bước vào giai đoạn vận hành thí điểm.",
            "pwd_error": "Mật khẩu phải từ 8-20 ký tự, bao gồm ít nhất 1 chữ hoa, 1 chữ thường, 1 số và 1 ký tự đặc biệt.",
            "reg_success_msg": "Bạn đã đặt bước chân đầu tiên trên chặng đường xanh!",
            "btn_auto_login": "ĐĂNG NHẬP NGAY",
            "intro_mission": "Sứ mệnh của nền tảng là kiến tạo một tương lai tươi sáng, xanh sạch và phát triển bền vững.",
            "intro_question": "Bạn đã sẵn sàng cho một tương lai xanh chưa?",
            "btn_create_acc_intro": "TẠO TÀI KHOẢN NGAY"
        },
        "English": {
            "slogan": "ONE TOUCH - ONE GREEN WORLD",
            "subtitle": "Welcome to the pioneer Carbon Credit Exchange. Where AI satellite tech meets the mission to protect the Earth.",
            "tab_login": "LOGIN", "tab_reg": "CREATE ACCOUNT", "tab_intro": "INTRODUCTION",
            "sys_access": "SYSTEM ACCESS",
            "user": "Username", "pass": "Password",
            "btn_login": "Login to Platform", "btn_reg": "Register Account",
            "achieve": "PLATFORM ACHIEVEMENTS", "ach_1_val": "2.5M+", "ach_1_lbl": "Tons Carbon Traded", "ach_2_val": "15,000", "ach_2_lbl": "Hectares Protected",
            "projects": "FEATURED PROJECTS", "proj_name": "Ca Mau Mangrove Project", "proj_desc": "Protecting biomass & coastal biodiversity.", "proj_badge": "AI Verified",
            "news_lbl": "LATEST NEWS:", "news_txt": "Vietnam's Carbon Credit Market officially begins pilot operation.",
            "pwd_error": "Password must be 8-20 characters, with at least 1 uppercase, 1 lowercase, 1 number, and 1 special character.",
            "reg_success_msg": "You have taken the first step on the green journey!",
            "btn_auto_login": "LOGIN NOW",
            "intro_mission": "The platform's mission is to forge a bright, clean, green, and sustainable future.",
            "intro_question": "Are you ready for a green future?",
            "btn_create_acc_intro": "CREATE ACCOUNT NOW"
        }
    }
    t = T[lang]

    wave_html = '<div class="wave-text-container">'
    delay = 0.0
    for char in t["slogan"]:
        wave_html += f'<span class="wave-char" style="animation-delay: {delay}s;">{"&nbsp;" if char == " " else char}</span>'
        delay += 0.08
    wave_html += '</div>'

    st.markdown(wave_html, unsafe_allow_html=True)
    st.markdown(f'<div class="hero-subtitle">{t["subtitle"]}</div>', unsafe_allow_html=True)

    _, col_form, col_space, col_info, _ = st.columns([0.5, 3, 0.2, 3, 0.5])
    
    with col_form:
        with st.container(border=True):
            st.markdown(f'<div class="section-title" style="border-left:none; padding-left:0; text-align:center;">{t["sys_access"]}</div>', unsafe_allow_html=True)
            
            tab_dang_nhap, tab_dang_ky, tab_gioi_thieu = st.tabs([t["tab_login"], t["tab_reg"], t["tab_intro"]])
            
            with tab_dang_nhap:
                with st.form("form_login"):
                    u_name = st.text_input(t["user"], placeholder="admin, investor, buyer")
                    u_pass = st.text_input(t["pass"], type="password", placeholder="••••••")
                    submitted = st.form_submit_button(t["btn_login"], type="tertiary", use_container_width=True)
                    if submitted:
                        db = st.session_state["users_db"]
                        if u_name in db and db[u_name]["password"] == u_pass:
                            st.session_state["logged_in"] = True
                            st.session_state["current_user"] = u_name
                            st.session_state["current_role"] = db[u_name]["role"]
                            st.rerun()
                        else: st.error("Thông tin không chính xác." if lang=="Tiếng Việt" else "Invalid credentials.")
            
            with tab_dang_ky:
                if st.session_state["reg_success_data"]:
                    st.markdown(f"""
                        <div class="glass-block" style="border-color: #48bb78; box-shadow: 0 0 25px rgba(72,187,120,0.5); text-align:center; padding: 25px; margin-top: 15px;">
                            <h3 style="color:#48bb78; font-weight:800; margin-bottom: 15px; font-size: 1.4rem; line-height: 1.4;">{t['reg_success_msg']}</h3>
                            <p style="color:#a0aec0; margin-bottom: 5px;">Tài khoản / Account: <b style="color:white;">{st.session_state['reg_success_data']['user']}</b></p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(t["btn_auto_login"], type="tertiary", use_container_width=True):
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
                        
                        reg_submitted = st.form_submit_button(t["btn_reg"], type="tertiary", use_container_width=True)
                        
                        if reg_submitted:
                            if not new_user or not new_pass:
                                st.error("Vui lòng điền đủ thông tin." if lang=="Tiếng Việt" else "Please fill all fields.")
                            elif new_user in st.session_state["users_db"]:
                                st.error("Tài khoản đã tồn tại." if lang=="Tiếng Việt" else "Account already exists.")
                            else:
                                pwd_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,20}$'
                                if not re.match(pwd_pattern, new_pass):
                                    st.error(t["pwd_error"])
                                else:
                                    st.session_state["users_db"][new_user] = {"password": new_pass, "role": role_sel}
                                    st.session_state["reg_success_data"] = {"user": new_user, "role": role_sel}
                                    st.rerun()

            with tab_gioi_thieu:
                intro_text = t["intro_mission"]
                intro_html = '<div style="text-align:center; margin-top: 15px; margin-bottom: 25px; line-height: 1.7;">'
                delay_intro = 0.0
                
                for word in intro_text.split(" "):
                    intro_html += '<span style="display: inline-block; white-space: nowrap;">'
                    for char in word:
                        intro_html += f'<span class="intro-wave-char" style="animation-delay: {delay_intro}s;">{char}</span>'
                        delay_intro += 0.05
                    intro_html += '</span> '
                intro_html += '</div>'
                
                st.markdown(intro_html, unsafe_allow_html=True)
                
                st.markdown(f"<h4 style='text-align:center; color:white; margin-bottom:25px; font-weight: 800;'>{t['intro_question']}</h4>", unsafe_allow_html=True)
                
                if st.button(t["btn_create_acc_intro"], type="tertiary", use_container_width=True):
                    st.info("Vui lòng nhấn vào tab 'TẠO TÀI KHOẢN' ở phía trên để bắt đầu." if lang == "Tiếng Việt" else "Please click the 'CREATE ACCOUNT' tab above to start.")

    with col_info:
        st.markdown(f"""
        <div class="glass-block">
            <div class="section-title">{t['achieve']}</div>
            <div style="display: flex; justify-content: space-around; text-align:center;">
                <div><div class="stat-value">{t['ach_1_val']}</div><div class="stat-label">{t['ach_1_lbl']}</div></div>
                <div><div class="stat-value">{t['ach_2_val']}</div><div class="stat-label">{t['ach_2_lbl']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="glass-block">
            <div class="section-title">{t['projects']}</div>
            <div class="project-title">{t['proj_name']}</div>
            <div class="project-desc">{t['proj_desc']}</div>
            <div style="text-align:center;"><span class="verified-badge">{t['proj_badge']}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="news-ticker-container">
        <div class="news-label">{t['news_lbl']}</div>
        <div class="news-marquee">
            <span>{t['news_txt']} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {t['news_txt']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
