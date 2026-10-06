import streamlit as st
import re
import db_manager

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
            "reg_success_msg": "Bạn đã đặt bước chân đầu tiên trên chặng đường xanh!",
            "btn_auto_login": "ĐĂNG NHẬP NGAY"
        },
        "English": {
            "slogan": "ONE TOUCH - ONE GREEN WORLD",
            "subtitle": "Welcome to the pioneer Carbon Credit Exchange. AI satellite technology meets Earth protection mission.",
            "tab_login": "LOGIN", "tab_reg": "REGISTER", "tab_intro": "ABOUT",
            "welcome_msg": "WELCOME PARTNER!",
            "user": "Username", "pass": "Password",
            "btn_login": "AUTHENTICATE", "btn_reg": "CREATE ACCOUNT",
            "pwd_error": "Password must be 8-20 characters with uppercase, lowercase, number, and special character.",
            "reg_success_msg": "You have taken your first step towards sustainability!",
            "btn_auto_login": "LOGIN NOW"
        }
    }
    t = T.get(lang, T["Tiếng Việt"])
    
    _, col_form, _ = st.columns([0.2, 0.6, 0.2])
    with col_form:
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align:center; color:#48bb78;'>{t['welcome_msg']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; color:#a0aec0;'>{t['subtitle']}</p>", unsafe_allow_html=True)
            
            tab_dang_nhap, tab_dang_ky = st.tabs([t["tab_login"], t["tab_reg"]])
            
            with tab_dang_nhap:
                with st.form("form_login"):
                    u_name = st.text_input(t["user"], placeholder="admin, investor, buyer")
                    u_pass = st.text_input(t["pass"], type="password", placeholder="••••••")
                    submitted = st.form_submit_button(t["btn_login"], type="primary", use_container_width=True)
                    
                    if submitted:
                        users = db_manager.load_users()
                        if u_name in users and users[u_name]["password"] == u_pass:
                            st.session_state["logged_in"] = True
                            st.session_state["current_user"] = u_name
                            st.session_state["current_role"] = users[u_name]["role"]
                            st.rerun()
                        else:
                            st.error("Thông tin không chính xác." if lang=="Tiếng Việt" else "Invalid credentials.")
            
            with tab_dang_ky:
                if st.session_state["reg_success_data"]:
                    st.success(t["reg_success_msg"])
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
                                    success, msg = db_manager.register_user(new_user, new_pass, role_sel)
                                    if success:
                                        st.session_state["users_db"] = db_manager.load_users()
                                        st.session_state["reg_success_data"] = {"user": new_user, "role": role_sel}
                                        st.rerun()
                                    else:
                                        st.error(msg)
