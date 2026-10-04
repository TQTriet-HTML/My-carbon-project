import streamlit as st

def hien_thi_cong_dang_nhap(lang="Tiếng Việt"):
    T = {
        "Tiếng Việt": {
            "slogan": "MỘT CÚ CHẠM - VẠN ĐIỀU XANH",
            "welcome": "🌱 Chào mừng bạn đến với Nền tảng Giao dịch Tín chỉ Carbon tiên phong. Nơi công nghệ AI vệ tinh gặp gỡ sứ mệnh bảo vệ Trái Đất.",
            "login_tab": "🔐 Đăng nhập",
            "register_tab": "✨ Tạo tài khoản mới",
            "login_title": "### 🚪 Truy cập Hệ thống",
            "username": "Tên đăng nhập",
            "password": "Mật khẩu",
            "btn_login": "🚀 Đăng nhập vào Nền tảng",
            "register_title": "### 🌱 Tham gia Cộng đồng Xanh",
            "register_prompt": "💡 **Bạn đã có tài khoản chưa?** Nếu chưa hãy tạo mới để kết nối trực tiếp với các dự án bảo vệ rừng trên toàn cầu.",
            "new_username": "Tên đăng nhập mới",
            "new_password": "Mật khẩu mới",
            "role": "Vai trò của bạn:",
            "roles": ["Doanh nghiệp mua tín chỉ", "Nhà đầu tư từ xa (Cổ đông)", "Chủ rừng / Kỹ sư MRV"],
            "btn_register": "🌟 Khởi tạo Tài khoản & Bắt đầu",
            "achievements": "🏆 THÀNH TỰU NỀN TẢNG",
            "projects": "🌲 DỰ ÁN TIÊU BIỂU",
            "news": "🚀 <b>TIN TỨC MỚI NHẤT:</b>",
            "news_1": "Thị trường Tín chỉ Carbon Việt Nam chính thức vận hành thử nghiệm.",
            "news_2": "Cập nhật vệ tinh Sentinel-2 giúp theo dõi sinh khối với độ chính xác 98%.",
            "stat_1_val": "2.5M+", "stat_1_lbl": "Tấn Carbon giao dịch",
            "stat_2_val": "15,000", "stat_2_lbl": "Hecta Rừng bảo vệ",
            "proj_1_name": "Dự án Rừng ngập mặn Cà Mau", "proj_1_desc": "Bảo vệ sinh khối & Đa dạng sinh học vùng ven biển."
        },
        "English": {
            "slogan": "ONE TOUCH - ONE GREENER WORLD",
            "welcome": "🌱 Welcome to the pioneer Carbon Credit Exchange. Where AI satellite tech meets the mission to protect the Earth.",
            "login_tab": "🔐 Login",
            "register_tab": "✨ Create Account",
            "login_title": "### 🚪 System Access",
            "username": "Username",
            "password": "Password",
            "btn_login": "🚀 Login to Platform",
            "register_title": "### 🌱 Join the Green Community",
            "register_prompt": "💡 **Don't have an account yet?** Create a new account to contribute to building a greener future today.",
            "new_username": "New Username",
            "new_password": "New Password",
            "role": "Your Role:",
            "roles": ["Doanh nghiệp mua tín chỉ", "Nhà đầu tư từ xa (Cổ đông)", "Chủ rừng / Kỹ sư MRV"], 
            "btn_register": "🌟 Create Account & Start",
            "achievements": "🏆 PLATFORM ACHIEVEMENTS",
            "projects": "🌲 FEATURED PROJECTS",
            "news": "🚀 <b>LATEST NEWS:</b>",
            "news_1": "Vietnam's Carbon Credit Market officially begins pilot operation.",
            "news_2": "Sentinel-2 satellite update enables 98% accurate biomass tracking.",
            "stat_1_val": "2.5M+", "stat_1_lbl": "Tons Carbon Traded",
            "stat_2_val": "15,000", "stat_2_lbl": "Hectares Protected",
            "proj_1_name": "Ca Mau Mangrove Project", "proj_1_desc": "Protecting biomass & coastal biodiversity."
        }
    }
    
    t = T.get(lang, T["Tiếng Việt"])

    st.markdown("""
        <style>
        .stApp {
            background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), 
                              url('https://images.unsplash.com/photo-1511497584788-876760111969?q=80&w=2532&auto=format&fit=crop');
            background-size: cover; background-position: center; background-attachment: fixed;
        }
        
        /* HOẠT HỌA SÓNG - ĐÃ SỬA CHU KỲ LÊN 5s ĐỂ KHÔNG BỊ KHỰNG CHỮ CUỐI */
        @keyframes autoWave {
            0%, 20%, 100% { transform: translateY(0) scale(1); color: #48bb78; text-shadow: 0 4px 15px rgba(72, 187, 120, 0.4); }
            10% { transform: translateY(-12px) scale(1.12); color: #63b3ed; text-shadow: 0 8px 22px rgba(99, 179, 237, 0.7); }
        }
        .bouncing-slogan { text-align: center; margin-bottom: 20px; }
        .bouncing-slogan span { display: inline-block; font-size: clamp(2rem, 2.5vw, 2.8rem); font-weight: 900; cursor: default; animation: autoWave 5s infinite; }
        
        .glass-card, div[data-testid="stTabs"] {
            background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 25px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); transition: all 0.4s ease; margin-bottom: 20px;
        }
        .glass-card:hover, div[data-testid="stTabs"]:hover { transform: translateY(-5px); border-color: rgba(72, 187, 120, 0.4); box-shadow: 0 30px 60px -12px rgba(72, 187, 120, 0.3); }
        
        .stat-val { font-size: 2rem; font-weight: 800; color: #48bb78; margin-bottom: 0px; line-height: 1; }
        .stat-lbl { font-size: 0.95rem; color: #a0aec0; margin-top: 5px; }
        .news-ticker-container { position: fixed; bottom: 0; left: 0; width: 100%; background-color: rgba(15, 23, 42, 0.95); color: #a0aec0; padding: 12px 0; border-top: 1px solid #2d3748; font-size: 0.95rem; z-index: 9999; }
        .news-ticker-content a { color: #63b3ed; text-decoration: none; font-weight: 600; margin: 0 30px; }
        .news-ticker-content a:hover { color: #48bb78; text-decoration: underline; }
        .welcome-text { text-align: center; color: #e2e8f0; font-size: 1.1rem; margin-bottom: 35px; font-weight: 300; }
        </style>
    """, unsafe_allow_html=True)

    # Hiệu ứng Slogan Delay chính xác 0.05s cho mượt mà tuyệt đối
    slogan = t["slogan"]
    html_slogan = "".join([f'<span style="animation-delay: {i*0.05}s">{"&nbsp;" if c==" " else c}</span>' for i, c in enumerate(slogan)])
    st.markdown(f'<div class="bouncing-slogan">{html_slogan}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="welcome-text">{t["welcome"]}</div>', unsafe_allow_html=True)

    col_form, col_gap, col_info = st.columns([12, 1, 10])
    
    with col_form:
        tab_login, tab_register = st.tabs([t["login_tab"], t["register_tab"]])
        
        with tab_login:
            st.markdown(t["login_title"])
            with st.form("login_form", clear_on_submit=False):
                tendangnhap = st.text_input(t["username"], placeholder="admin, investor, buyer")
                matkhau = st.text_input(t["password"], type="password", placeholder="***")
                submitted_login = st.form_submit_button(t["btn_login"], type="primary", use_container_width=True)
                
                if submitted_login:
                    db = st.session_state["users_db"]
                    if tendangnhap in db and db[tendangnhap]["password"] == matkhau:
                        st.session_state["logged_in"] = True
                        st.session_state["current_user"] = tendangnhap
                        st.session_state["current_role"] = db[tendangnhap]["role"]
                        st.rerun()
                    else:
                        st.error("❌ Sai tên đăng nhập hoặc mật khẩu / Incorrect credentials.")
                    
        with tab_register:
            st.markdown(t["register_title"])
            st.info(t["register_prompt"])
            with st.form("register_form", clear_on_submit=True):
                new_user = st.text_input(t["new_username"])
                new_pass = st.text_input(t["new_password"], type="password")
                new_role = st.selectbox(t["role"], t["roles"])
                submitted_reg = st.form_submit_button(t["btn_register"], type="primary", use_container_width=True)
                
                if submitted_reg:
                    if not new_user or not new_pass:
                        st.warning("⚠️ Vui lòng điền đầy đủ thông tin!")
                    elif new_user in st.session_state["users_db"]:
                        st.error("⚠ Tên đăng nhập này đã tồn tại! Vui lòng chọn tên khác.")
                    else:
                        st.session_state["users_db"][new_user] = {"password": new_pass, "role": new_role}
                        st.success(f"🎉 Tài khoản `{new_user}` đã tạo thành công! Hãy sang Tab Đăng nhập.")

    with col_info:
        st.markdown(f"<h4 style='color: #e2e8f0;'>{t['achievements']}</h4>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between;">
                    <div><div class="stat-val">{t['stat_1_val']}</div><div class="stat-lbl">{t['stat_1_lbl']}</div></div>
                    <div><div class="stat-val" style="color: #63b3ed;">{t['stat_2_val']}</div><div class="stat-lbl">{t['stat_2_lbl']}</div></div>
                </div>
            </div>
            <h4 style='color: #e2e8f0; margin-top: 20px;'>{t['projects']}</h4>
            <div class="glass-card" style="padding: 15px 25px;">
                <h5 style="color: #fff; margin-bottom: 5px;">🌳 {t['proj_1_name']}</h5>
                <p style="color: #a0aec0; font-size: 0.9rem; margin-bottom: 10px;">{t['proj_1_desc']}</p>
                <span style="background: #276749; color: #c6f6d5; padding: 3px 8px; border-radius: 4px; font-size: 0.8rem;">Đã xác thực AI (Verified)</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="news-ticker-container">
            <marquee class="news-ticker-content" scrollamount="6" onmouseover="this.stop();" onmouseout="this.start();">
                {t['news']} <a href="#">{t['news_1']}</a> | <a href="#">{t['news_2']}</a>
            </marquee>
        </div>
    """, unsafe_allow_html=True)
