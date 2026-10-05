import streamlit as st

def hien_thi_popup_dang_xuat():
    if "show_logout_dialog" not in st.session_state:
        st.session_state["show_logout_dialog"] = False

    # 1. Nút Đăng xuất trên menu/sidebar
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    if st.button("Đăng xuất" if lang == "Tiếng Việt" else "Logout", use_container_width=True, key="btn_trigger_logout"):
        st.session_state["show_logout_dialog"] = True
        st.rerun()

    # 2. Xây dựng Hộp thoại Popup nổi giữa màn hình
    if st.session_state["show_logout_dialog"]:
        # Container chứa toàn bộ popup
        with st.container():
            st.markdown("""
            <div class="logout-anchor"></div>
            <style>
            /* Lớp mờ đen toàn màn hình */
            .logout-overlay {
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background-color: rgba(9, 13, 22, 0.85);
                backdrop-filter: blur(8px);
                z-index: 999998;
            }
            
            /* Ép thẻ Container của Streamlit thành khung Popup giữa màn hình */
            div[data-testid="stVerticalBlock"] > div:has(.logout-anchor) {
                position: fixed !important;
                top: 50% !important; left: 50% !important;
                transform: translate(-50%, -50%) !important;
                background: linear-gradient(135deg, rgba(26, 32, 44, 0.98), rgba(45, 55, 72, 0.98)) !important;
                border: 2px solid #48bb78 !important;
                border-radius: 16px !important;
                padding: 35px !important;
                z-index: 999999 !important;
                width: 90% !important;
                max-width: 480px !important;
                box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 30px rgba(72,187,120,0.5) !important;
                animation: popIn 0.3s ease-out forwards !important;
            }
            
            @keyframes popIn {
                from { opacity: 0; transform: translate(-50%, -45%) scale(0.9); }
                to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            }

            /* HIỆU ỨNG NÚT ĐỎ (Tạm thời nghỉ chân) - Cột số 1 */
            div[data-testid="stVerticalBlock"] > div:has(.logout-anchor) div[data-testid="column"]:nth-child(1) button {
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
                border: 1px solid rgba(239, 68, 68, 0.8) !important;
                color: white !important; font-weight: 800 !important; border-radius: 8px !important;
                transition: all 0.3s ease !important;
            }
            div[data-testid="stVerticalBlock"] > div:has(.logout-anchor) div[data-testid="column"]:nth-child(1) button:hover {
                box-shadow: 0 0 25px rgba(239, 68, 68, 0.9) !important;
                transform: translateY(-2px) scale(1.03) !important;
            }

            /* HIỆU ỨNG NÚT XANH LÁ (Tiếp tục chặng đường) - Cột số 2 */
            div[data-testid="stVerticalBlock"] > div:has(.logout-anchor) div[data-testid="column"]:nth-child(2) button {
                background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important;
                border: 1px solid rgba(72, 187, 120, 0.8) !important;
                color: white !important; font-weight: 800 !important; border-radius: 8px !important;
                transition: all 0.3s ease !important;
            }
            div[data-testid="stVerticalBlock"] > div:has(.logout-anchor) div[data-testid="column"]:nth-child(2) button:hover {
                box-shadow: 0 0 25px rgba(72,187,120,0.9) !important;
                transform: translateY(-2px) scale(1.03) !important;
            }
            </style>
            <div class="logout-overlay"></div>
            """, unsafe_allow_html=True)

            # Nội dung câu hỏi đầy chất thơ
            st.markdown("<h3 style='color: #ffffff; font-weight: 900; line-height: 1.5; margin-bottom: 25px; font-size: 1.25rem; text-align: center;'>Bạn có chắc muốn tạm nghỉ chân sau một chặng đường xanh đã qua không?</h3>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                # Nút Đỏ (Đăng xuất thật)
                if st.button("Tạm thời nghỉ chân", use_container_width=True, key="btn_confirm_out"):
                    st.session_state["logged_in"] = False
                    st.session_state["current_user"] = ""
                    st.session_state["current_role"] = ""
                    st.session_state["show_logout_dialog"] = False
                    st.rerun()
            with c2:
                # Nút Xanh lá (Hủy, tiếp tục)
                if st.button("Tiếp tục chặng đường", use_container_width=True, key="btn_cancel_out"):
                    st.session_state["show_logout_dialog"] = False
                    st.rerun()
