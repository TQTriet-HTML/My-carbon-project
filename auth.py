import streamlit as st

# Giả lập cơ sở dữ liệu người dùng
USERS = {
    "admin": {"password": "123", "role": "Chủ rừng / Kỹ sư MRV"},
    "investor": {"password": "123", "role": "Nhà đầu tư từ xa (Cổ đông)"},
    "buyer": {"password": "123", "role": "Doanh nghiệp mua tín chỉ"}
}

def load_users():
    return USERS

def hien_thi_cong_dang_nhap(lang="Tiếng Việt"):
    # --- TỪ ĐIỂN ĐA NGÔN NGỮ CHO TRANG ĐĂNG NHẬP ---
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
            "register_prompt": "💡 **Bạn đã có tài khoản chưa?**\n\nNếu chưa thì hãy tạo một tài khoản mới để góp phần vào công cuộc xây dựng một tương lai xanh nhé! Mỗi tài khoản mới là một nhịp cầu nối liền nhà đầu tư và chủ rừng.",
            "new_username": "Tên đăng nhập mới",
            "new_password": "Mật khẩu mới",
            "role": "Vai trò của bạn:",
            "roles": ["Doanh nghiệp mua tín chỉ", "Nhà đầu tư từ xa (Cổ đông)", "Chủ rừng / Kỹ sư MRV"],
            "btn_register": "🌟 Khởi tạo Tài khoản & Bắt đầu",
            "achievements": "🏆 THÀNH TỰU NỀN TẢNG",
            "projects": "🌲 DỰ ÁN TIÊU BIỂU",
            "news": "🚀 <b>TIN TỨC MỚI NHẤT:</b>",
            "news_1": "Thị trường Tín chỉ Carbon Việt Nam chính thức vận hành thử nghiệm vào 2025.",
            "news_2": "Google Earth Engine công bố bản cập nhật thuật toán sinh khối mới, tăng độ chính xác lên 98%.",
            "stat_1_val": "2.5M+", "stat_1_lbl": "Tấn Carbon giao dịch",
            "stat_2_val": "15,000", "stat_2_lbl": "Hecta Rừng bảo vệ",
            "proj_1_name": "Dự án rừng ngập mặn Cà Mau", "proj_1_desc": "Bảo vệ sinh khối & Đa dạng sinh học vùng ven biển."
        },
        "English": {
            "slogan": "ONE TOUCH - GREEN WORLD",
            "welcome": "🌱 Welcome to the pioneer Carbon Credit Exchange. Where AI satellite tech meets the mission to protect the Earth.",
            "login_tab": "🔐 Login",
            "register_tab": "✨ Create Account",
            "login_title": "### 🚪 System Access",
            "username": "Username",
            "password": "Password",
            "btn_login": "🚀 Login to Platform",
            "register_title": "### 🌱 Join the Green Community",
            "register_prompt": "💡 **Don't have an account yet?**\n\nCreate a new account to contribute to building a green future! Each new account is a bridge connecting investors and forest owners.",
            "new_username": "New Username",
            "new_password": "New Password",
            "role": "Your Role:",
            "roles": ["Corporate Buyer", "Remote Investor (Shareholder)", "Forest Owner / MRV Engineer"],
            "btn_register": "🌟 Create Account & Start",
            "achievements": "🏆 PLATFORM ACHIEVEMENTS",
            "projects": "🌲 FEATURED PROJECTS",
            "news": "🚀 <b>LATEST NEWS:</b>",
            "news_1": "Vietnam's Carbon Credit Market officially begins pilot operation in 2025.",
            "news_2": "Google Earth Engine announces new biomass algorithm, increasing accuracy to 98%.",
            "stat_1_val": "2.5M+", "stat_1_lbl": "Tons Carbon Traded",
            "stat_2_val": "15,000", "stat_2_lbl": "Hectares Protected",
            "proj_1_name": "Ca Mau Mangrove Project", "proj_1_desc": "Protecting biomass & coastal biodiversity."
        }
    }
    
    t = T.get(lang, T["Tiếng Việt"])

    # --- CSS HOẠT HỌA & GIAO DIỆN KÍNH ---
    st.markdown("""
        <style>
        .stApp {
            background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), 
                              url('https://images.unsplash.com/photo-1511497584788-876760111969?q=80&w=2532&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        
        /* Hiệu ứng sóng Slogan tự động đồng bộ tỉ lệ thời gian */
        @keyframes autoWave {
            0%, 10%, 100% { transform: translateY(0) scale(1); color: #48bb78; text-shadow: 0 4px 15px rgba(72, 187, 120, 0.4); }
            5% { transform: translateY(-12px) scale(1.12); color: #63b3ed; text-shadow: 0 8px 22px rgba(99, 179, 237, 0.7); }
        }
        .bouncing-slogan {
            text-align: center;
            margin-bottom: 20px;
        }
        .bouncing-slogan span {
            display: inline-block;
            font-size: clamp(2rem, 2.8vw, 2.8rem);
            font-weight: 900;
            cursor: default;
            animation: autoWave 8s infinite;
        }

        .glass-card, div[data-testid="stTabs"] {
            background: rgba(30, 41, 59, 0.65);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            transition: transform 0.4s ease, box-shadow 0.4s ease, border-color 0.4s ease;
            margin-bottom: 20px;
        }
        .glass-card:hover, div[data-testid="stTabs"]:hover {
            transform: translateY(-6px);
            box-shadow: 0 30px 60px -12px rgba(72, 187, 120, 0.3);
            border-color: rgba(72, 187, 120, 0.4);
        }

        .stat-val { font-size: 2rem; font-weight: 800; color: #48bb78; margin-bottom: 0px; line-height: 1; }
        .stat-lbl { font-size: 0.95rem; color: #a0aec0; margin-top: 5px; }

        .news-ticker-container {
            position: fixed;
            bottom: 0; left: 0; width: 100%;
            background-color: rgba(15, 23, 42, 0.95);
            color: #a0aec0;
            padding: 12px 0;
            border-top: 1px solid #2d3748;
            font-size: 0.95rem;
            z-index: 9999;
            box-shadow: 0 -5px 15px rgba(0,0,0,0.4);
        }
        .news-ticker-content a { color: #63b3ed; text-decoration: none; font-weight: 600; margin: 0 30px; }
        .news-ticker-content a:hover { color: #48bb78; text-decoration: underline; }
        
        .welcome-text { text-align: center; color: #e2e8f0; font-size: 1.1rem; margin-bottom: 35px; font-weight: 300; }
        </style>
    """, unsafe_allow_html=True)

    # --- TÍNH TOÁN ĐỘ TRỄ ĐỘNG CHO TỪNG KÝ TỰ (CHỐNG LỆCH NHỊP KÝ TỰ CUỐI) ---
    slogan = t["slogan"]
    total_chars = max(len(slogan), 1)
    
    # Phân bổ độ trễ tự động trong khoảng 2 giây đầu của chu kỳ 8 giây
    html_slogan = ""
    for i, c in enumerate(slogan):
        if c == ' ':
            html_slogan += "&nbsp;"
        else:
            delay = (i / total_chars) * 1.5 
            html_slogan += f'<span style="animation-delay: {delay:.2f}s">{c}</span>'
            
    st.markdown(f'<div class="bouncing-slogan">{html_slogan}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="welcome-text">{t["welcome"]}</div>', unsafe_allow_html=True)

    # --- CHIA 2 CỘT ---
    col_form, col_gap, col_info = st.columns([12, 1, 10])
    
    with col_form:
        tab_login, tab_register = st.tabs([t["login_tab"], t["register_tab"]])
        
        with tab_login:
            st.markdown(t["login_title"])
            tendangnhap = st.text_input(t["username"], placeholder="admin, investor, buyer")
            matkhau = st.text_input(t["password"], type="password", placeholder="***")
            
            if st.button(t["btn_login"], type="primary", use_container_width=True):
                users = load_users()
                if tendangnhap in users and users[tendangnhap]["password"] == matkhau:
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = tendangnhap
                    st.session_state["current_role"] = users[tendangnhap]["role"]
                    st.rerun()
                else:
                    st.error("❌ Sai tên đăng nhập hoặc mật khẩu / Incorrect credentials.")
                    
        with tab_register:
            st.markdown(t["register_title"])
            st.info(t["register_prompt"])
            
            new_user = st.text_input(t["new_username"])
            new_pass = st.text_input(t["new_password"], type="password")
            new_role = st.selectbox(t["role"], t["roles"])
            
            if st.button(t["btn_register"], type="primary", use_container_width=True):
                st.success(f"🎉 Tài khoản `{new_user}` đã được tạo thành công! / Created successfully!")

    with col_info:
        st.markdown(f"<h4 style='color: #e2e8f0;'>{t['achievements']}</h4>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <div class="stat-val">{t['stat_1_val']}</div>
                        <div class="stat-lbl">{t['stat_1_lbl']}</div>
                    </div>
                    <div>
                        <div class="stat-val" style="color: #63b3ed;">{t['stat_2_val']}</div>
                        <div class="stat-lbl">{t['stat_2_lbl']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h4 style='color: #e2e8f0; margin-top: 20px;'>{t['projects']}</h4>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="glass-card" style="padding: 15px 25px;">
                <h5 style="color: #fff; margin-bottom: 5px;">🌳 {t['proj_1_name']}</h5>
                <p style="color: #a0aec0; font-size: 0.9rem; margin-bottom: 10px;">{t['proj_1_desc']}</p>
                <span style="background: #276749; color: #c6f6d5; padding: 3px 8px; border-radius: 4px; font-size: 0.8rem;">Đã xác thực AI (Verified)</span>
            </div>
        """, unsafe_allow_html=True)

    # --- BẢNG TIN TỨC CHẠY DƯỚI CÙNG ---
    st.markdown(f"""
        <div class="news-ticker-container">
            <marquee class="news-ticker-content" scrollamount="6" onmouseover="this.stop();" onmouseout="this.start();">
                {t['news']}
                <a href="#">{t['news_1']}</a> | 
                <a href="#">{t['news_2']}</a>
            </marquee>
        </div>
    """, unsafe_allow_html=True)
