import streamlit as st
import json
import os

USER_FILE = "users_db.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        default_db = {"admin": {"password": "1234", "role": "Chủ rừng / Kỹ sư MRV"}}
        save_users(default_db)
        return default_db

def save_users(db):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def hien_thi_cong_dang_nhap():
    st.title("🔐 CỔNG ĐĂNG NHẬP NỀN TẢNG")
    st.markdown("Vui lòng đăng nhập hoặc tạo tài khoản để truy cập Sàn giao dịch & Hệ thống MRV.")
    
    user_db = load_users()
    tab_login, tab_register = st.tabs(["Đăng nhập", "Tạo tài khoản mới"])
    
    with tab_login:
        user = st.text_input("Tên đăng nhập", key="login_user")
        pwd = st.text_input("Mật khẩu", type="password", key="login_pwd")
        if st.button("Đăng nhập", type="primary"):
            if user in user_db and user_db[user]["password"] == pwd:
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = user
                st.session_state["current_role"] = user_db[user]["role"]
                st.rerun()
            else:
                st.error("❌ Sai tên đăng nhập hoặc mật khẩu!")
                
    with tab_register:
        new_user = st.text_input("Chọn tên đăng nhập mới", key="reg_user")
        new_pwd = st.text_input("Nhập mật khẩu", type="password", key="reg_pwd")
        # Bổ sung luôn vai trò "Nhà đầu tư từ xa / Cổ đông" vào đây
        role = st.selectbox("Vai trò của bạn", ["Doanh nghiệp mua tín chỉ", "Chủ rừng / Kỹ sư MRV", "Nhà đầu tư từ xa (Cổ đông)"])
        
        if st.button("Đăng ký tài khoản"):
            if new_user == "" or new_pwd == "":
                st.warning("⚠️ Vui lòng nhập đầy đủ thông tin!")
            elif new_user in user_db:
                st.warning("⚠️ Tên đăng nhập này đã có người sử dụng!")
            else:
                user_db[new_user] = {"password": new_pwd, "role": role}
                save_users(user_db)
                st.success("✅ Tạo tài khoản thành công! Hãy chuyển sang tab Đăng nhập.")
