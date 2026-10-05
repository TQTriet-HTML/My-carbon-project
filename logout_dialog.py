import streamlit as st

def hien_thi_popup_dang_xuat():
    # Khởi tạo trạng thái hiển thị popup nếu chưa có
    if "show_logout_dialog" not in st.session_state:
        st.session_state["show_logout_dialog"] = False

    # CSS tùy chỉnh cho hộp thoại nổi và 2 nút lựa chọn (Đỏ & Xanh lá)
    st.markdown("""
    <style>
    .logout-dialog-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(9, 13, 22, 0.85); backdrop-filter: blur(8px);
        z-index: 99999; display: flex; justify-content: center; align-items: center;
    }
    .logout-box {
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.98), rgba(45, 55, 72, 0.98));
        border: 2px solid #48bb78; border-radius: 16px; padding: 40px; text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 30px rgba(72,187,120,0.5);
        max-width: 480px; width: 90%; animation: zoomInPopup 0.3s ease;
    }
    @keyframes zoomInPopup {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }

    /* Nút Tạm thời nghỉ chân (Màu Đỏ, sáng lên khi trỏ chuột) */
    div.stButton > button.logout-btn-red {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626) !important;
        border: 1px solid rgba(239, 68, 68, 0.8) !important;
        color: white !important; font-weight: 800 !important; border-radius: 8px !important;
        transition: all 0.3s ease !important; letter-spacing: 0.5px;
    }
    div.stButton > button.logout-btn-red:hover {
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.9) !important;
        transform: translateY(-2px) scale(1.03) !important;
    }

    /* Nút Tiếp tục chặng đường (Màu Xanh lá, sáng lên khi trỏ chuột) */
    div.stButton > button.logout-btn-green {
        background: linear-gradient(135deg, #38a169 0%, #2f855a) !important;
        border: 1px solid rgba(72, 187, 120, 0.8) !important;
        color: white !important; font-weight: 800 !important; border-radius: 8px !important;
        transition: all 0.3s ease !important; letter-spacing: 0.5px;
    }
    div.stButton > button.logout-btn-green:hover {
        box-shadow: 0 0 25px rgba(72,187,120,0.9) !important;
        transform: translateY(-2px) scale(1.03) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Nút bấm Đăng xuất ở giao diện chính (Sidebar hoặc Menu)
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    btn_label = "Đăng xuất" if lang == "Tiếng Việt" else "Logout"
    
    if st.button(btn_label, use_container_width=True, key="trigger_logout_btn"):
        st.session_state["show_logout_dialog"] = True
        st.rerun()

    # Nếu trạng thái gọi hộp thoại là True thì hiển thị modal phủ giữa màn hình
    if st.session_state["show_logout_dialog"]:
        st.markdown("""
            <div class="logout-dialog-overlay">
                <div class="logout-box">
                    <h3 style="color: #ffffff; font-weight: 900; line-height: 1.5; margin-bottom: 25px; font-size: 1.3rem;">
                        Bạn có chắc muốn tạm nghỉ chân sau một chặng đường xanh đã qua không?
                    </h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Đặt 2 nút lựa chọn (Dùng cột để xếp ngang)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            # Gán class CSS tùy chỉnh qua markdown hoặc dùng button thông thường
            if st.button("Tạm thời nghỉ chân", use_container_width=True, key="btn_confirm_logout"):
                st.session_state["logged_in"] = False
                st.session_state["current_user"] = ""
                st.session_state["current_role"] = ""
                st.session_state["show_logout_dialog"] = False
                st.rerun()
        with col_c2:
            if st.button("Tiếp tục chặng đường", use_container_width=True, key="btn_cancel_logout"):
                st.session_state["show_logout_dialog"] = False
                st.rerun()
