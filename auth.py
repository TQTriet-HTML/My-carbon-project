import streamlit as st

def hien_thi_cong_dang_nhap(lang="Tiếng Việt"):
    # --- CSS KHÔNG ICON, HIỆU ỨNG SÁNG & HOẠT HỌA CAO CẤP ---
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #090d16 0%, #111827 50%, #064e3b 100%) !important;
        }
        
        @keyframes glowText {
            0% { text-shadow: 0 0 10px rgba(72,187,120,0.3); }
            50% { text-shadow: 0 0 25px rgba(72,187,120,0.8), 0 0 10px rgba(56,161,105,0.5); }
            100% { text-shadow: 0 0 10px rgba(72,187,120,0.3); }
        }
        
        .hero-title {
            font-size: clamp(26px, 3.2vw, 42px) !important;
            font-weight: 900 !important;
            letter-spacing: 2px !important;
            text-align: center;
            background: linear-gradient(90deg, #48bb78, #68d391, #319795);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glowText 4s infinite ease-in-out;
            margin-bottom: 5px;
        }

        .hero-subtitle {
            text-align: center;
            color: #a0aec0;
            font-size: 1.05rem;
            font-weight: 400;
            margin-bottom: 35px;
            letter-spacing: 0.5px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(17, 24, 39, 0.85) !important;
            border: 1px solid rgba(72, 187, 120, 0.3) !important;
            border-radius: 16px !important;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(72, 187, 120, 0.05) !important;
            backdrop-filter: blur(12px);
        }

        button[kind="primary"] {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
            border: none !important;
            color: white !important;
            font-weight: 700 !important;
            letter-spacing: 1px;
            transition: all 0.3s ease !important;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 0 25px rgba(72, 187, 120, 0.8) !important;
            transform: translateY(-2px);
        }

        *:focus, *:active { outline: none !important; }
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
            border-color: #2d3748 !important;
        }
        div[data-baseweb="select"]:hover, div[data-baseweb="input"]:hover,
        div[data-baseweb="select"]:focus-within, div[data-baseweb="input"]:focus-within {
            border-color: #48bb78 !important;
            box-shadow: 0 0 12px rgba(72, 187, 120, 0.4) !important;
        }
        [aria-invalid="true"] { border-color: #48bb78 !important; }
        </style>
    """, unsafe_allow_html=True)

    if lang == "Tiếng Việt":
        st.markdown('<div class="hero-title">HỆ THỐNG GIAO DỊCH TÍN CHỈ CARBON</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Nền tảng tiên phong kết nối công nghệ vệ tinh AI và tài chính lâm nghiệp bền vững</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hero-title">CARBON CREDIT TRADING PLATFORM</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Pioneering platform connecting AI satellite technology and sustainable forestry finance</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    
    with col2:
        with st.container(border=True):
            tab_dang_nhap, tab_dang_ky = st.tabs(["ĐĂNG NHẬP" if lang=="Tiếng Việt" else "LOGIN", "TẠO TÀI KHOẢN" if lang=="Tiếng Việt" else "REGISTER"])
            
            with tab_dang_nhap:
                with st.form("form_login"):
                    u_name = st.text_input("Tên đăng nhập" if lang=="Tiếng Việt" else "Username", placeholder="admin, buyer, investor")
                    u_pass = st.text_input("Mật khẩu" if lang=="Tiếng Việt" else "Password", type="password", placeholder="••••••")
                    
                    submitted = st.form_submit_button("XÁC THỰC TRUY CẬP" if lang=="Tiếng Việt" else "AUTHENTICATE ACCESS", type="primary", use_container_width=True)
                    
                    if submitted:
                        db = st.session_state["users_db"]
                        if u_name in db and db[u_name]["password"] == u_pass:
                            st.session_state["logged_in"] = True
                            st.session_state["current_user"] = u_name
                            st.session_state["current_role"] = db[u_name]["role"]
                            st.success("Đăng nhập thành công!" if lang=="Tiếng Việt" else "Login successful!")
                            st.rerun()
                        else:
                            st.error("Thông tin đăng nhập không chính xác." if lang=="Tiếng Việt" else "Invalid credentials.")

            with tab_dang_ky:
                with st.form("form_register"):
                    new_user = st.text_input("Tên tài khoản mới" if lang=="Tiếng Việt" else "New Username")
                    new_pass = st.text_input("Mật khẩu" if lang=="Tiếng Việt" else "Password", type="password")
                    role_sel = st.selectbox("Phân loại tài khoản" if lang=="Tiếng Việt" else "Account Role", ["Doanh nghiệp mua tín chỉ", "Chủ rừng / Kỹ sư MRV", "Nhà đầu tư từ xa (Cổ đông)"])
                    
                    reg_submitted = st.form_submit_button("ĐĂNG KÝ HỆ THỐNG" if lang=="Tiếng Việt" else "REGISTER SYSTEM", type="primary", use_container_width=True)
                    
                    if reg_submitted:
                        if new_user and new_pass:
                            if new_user in st.session_state["users_db"]:
                                st.error("Tài khoản đã tồn tại." if lang=="Tiếng Việt" else "Account already exists.")
                            else:
                                st.session_state["users_db"][new_user] = {"password": new_pass, "role": role_sel}
                                st.success("Tạo tài khoản thành công! Vui lòng chuyển sang tab Đăng nhập." if lang=="Tiếng Việt" else "Account created successfully! Please login.")
                        else:
                            st.error("Vui lòng điền đầy đủ thông tin." if lang=="Tiếng Việt" else "Please fill all fields.")
