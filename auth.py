import streamlit as st

def hien_thi_cong_dang_nhap(lang="Tiếng Việt"):
    st.markdown("""
        <style>
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
        
        .section-title { color: #ffffff; font-size: 1.15rem; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 25px; border-left: 5px solid #48bb78; padding-left: 12px; text-transform: uppercase; }
        .stat-value { font-size: 2.2rem; font-weight: 900; color: #63b3ed; margin-bottom: 5px; line-height: 1.1; }
        .stat-label { color: #a0aec0; font-size: 0.9rem; font-weight: 500;}
        .project-title { color: #48bb78; font-weight: 700; font-size: 1.2rem; margin-bottom: 10px; }
        .project-desc { color: #cbd5e0; font-size: 0.95rem; margin-bottom: 15px; line-height: 1.5; }
        .verified-badge { display: inline-block; background: rgba(72, 187, 120, 0.15); border: 1px solid #48bb78; color: #48bb78; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 700;}
        </style>
    """, unsafe_allow_html=True)

    T = {
        "Tiếng Việt": {
            "slogan": "MỘT CÚ CHẠM - VẠN ĐIỀU XANH",
            "subtitle": "Chào mừng đến với Sàn giao dịch Tín chỉ Carbon tiên phong. Nơi công nghệ vệ tinh AI hội tụ cùng sứ mệnh bảo vệ Trái Đất.",
            "tab_login": "ĐĂNG NHẬP", "tab_reg": "TẠO TÀI KHOẢN", "sys_access": "HỆ THỐNG TRUY CẬP",
            "user": "Tên đăng nhập", "pass": "Mật khẩu",
            "btn_login": "XÁC THỰC TRUY CẬP", "btn_reg": "TẠO MỚI TÀI KHOẢN",
            "achieve": "THÀNH TỰU NỀN TẢNG", "ach_1_val": "2.5M+", "ach_1_lbl": "Tấn Carbon Giao Dịch", "ach_2_val": "15,000", "ach_2_lbl": "Hecta Rừng Được Bảo Vệ",
            "projects": "DỰ ÁN TIÊU BIỂU", "proj_name": "Dự án Rừng ngập mặn Cà Mau", "proj_desc": "Bảo vệ sinh khối & đa dạng sinh học ven biển.", "proj_badge": "Đã xác thực AI (Verified)"
        },
        "English": {
            "slogan": "ONE TOUCH - ONE GREEN WORLD",
            "subtitle": "Welcome to the pioneer Carbon Credit Exchange. Where AI satellite tech meets the mission to protect the Earth.",
            "tab_login": "LOGIN", "tab_reg": "CREATE ACCOUNT", "sys_access": "SYSTEM ACCESS",
            "user": "Username", "pass": "Password",
            "btn_login": "Login to Platform", "btn_reg": "Register Account",
            "achieve": "PLATFORM ACHIEVEMENTS", "ach_1_val": "2.5M+", "ach_1_lbl": "Tons Carbon Traded", "ach_2_val": "15,000", "ach_2_lbl": "Hectares Protected",
            "projects": "FEATURED PROJECTS", "proj_name": "Ca Mau Mangrove Project", "proj_desc": "Protecting biomass & coastal biodiversity.", "proj_badge": "AI Verified"
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

    # Bóp không gian hai bên
    _, col_form, col_space, col_info, _ = st.columns([0.5, 3, 0.2, 3, 0.5])
    
    with col_form:
        with st.container(border=True):
            st.markdown(f'<div class="section-title" style="border-left:none; padding-left:0; text-align:center;">{t["sys_access"]}</div>', unsafe_allow_html=True)
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
                        else: st.error("Thông tin không chính xác." if lang=="Tiếng Việt" else "Invalid credentials.")
            with tab_dang_ky:
                with st.form("form_register"):
                    new_user = st.text_input("Tên tài khoản mới" if lang=="Tiếng Việt" else "New Username")
                    new_pass = st.text_input("Mật khẩu" if lang=="Tiếng Việt" else "Password", type="password")
                    role_sel = st.selectbox("Phân loại" if lang=="Tiếng Việt" else "Role", ["Doanh nghiệp mua tín chỉ", "Chủ rừng / Kỹ sư MRV", "Nhà đầu tư từ xa (Cổ đông)"])
                    reg_submitted = st.form_submit_button(t["btn_reg"], type="primary", use_container_width=True)
                    if reg_submitted:
                        if new_user and new_pass:
                            if new_user in st.session_state["users_db"]: st.error("Tài khoản đã tồn tại.")
                            else:
                                st.session_state["users_db"][new_user] = {"password": new_pass, "role": role_sel}
                                st.success("Thành công!" if lang=="Tiếng Việt" else "Created!")

    with col_info:
        with st.container(border=True):
            st.markdown(f"""
            <div class="section-title">{t['achieve']}</div>
            <div style="display: flex; justify-content: space-around; text-align:center;">
                <div><div class="stat-value">{t['ach_1_val']}</div><div class="stat-label">{t['ach_1_lbl']}</div></div>
                <div><div class="stat-value">{t['ach_2_val']}</div><div class="stat-label">{t['ach_2_lbl']}</div></div>
            </div>
            """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"""
            <div class="section-title">{t['projects']}</div>
            <div class="project-title">{t['proj_name']}</div>
            <div class="project-desc">{t['proj_desc']}</div>
            <div style="text-align:center;"><span class="verified-badge">{t['proj_badge']}</span></div>
            """, unsafe_allow_html=True)
