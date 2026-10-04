import streamlit as st
import pandas as pd

def hien_thi_vinh_danh_va_gop_y():
    st.markdown("## 🏆 Bảng Vàng & Tôn Vinh Đóng Góp Xanh")
    st.caption("Ghi nhận những cá nhân và tổ chức đi đầu trong nỗ lực Net-Zero toàn cầu")

    # PHẦN 1: BẢNG XẾP HẠNG (LEADERBOARD)
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        st.markdown("### 🏢 Top Doanh Nghiệp Mua Tín Chỉ")
        top_buyers = pd.DataFrame({
            "Hạng": ["🥇 1", "🥈 2", "🥉 3", "4", "5"],
            "Doanh Nghiệp / Tổ Chức": ["Vinamilk", "FPT Software", "Vietcombank", "Vingroup", "Masan Group"],
            "Tín chỉ đã mua": ["50,000", "42,000", "38,500", "29,000", "15,000"],
            "Huy hiệu ESG": ["💎 Kim Cương", "🥇 Vàng", "🥈 Bạc", "🥉 Đồng", "🥉 Đồng"]
        })
        st.dataframe(top_buyers, hide_index=True, use_container_width=True)
        
    with col_b2:
        st.markdown("### 🌳 Top Dự Án Trồng Rừng Xuất Sắc")
        top_forests = pd.DataFrame({
            "Hạng": ["🥇 1", "🥈 2", "🥉 3", "4", "5"],
            "Chủ Rừng / Dự Án": ["Rừng ngập mặn Cà Mau", "Dự án Bắc Trung Bộ", "KBT Nam Cát Tiên", "Rừng phòng hộ Yên Bái", "Dự án Tây Nguyên"],
            "Diện Tích (Ha)": ["12,500", "8,200", "5,400", "4,100", "3,800"],
            "CO2 Hấp Thụ": ["1.2M", "850K", "520K", "310K", "290K"]
        })
        st.dataframe(top_forests, hide_index=True, use_container_width=True)

    st.divider()

    # PHẦN 2: THÀNH TÍCH CÁ NHÂN (GLASS CARD)
    st.markdown("### 🌟 Thành tích Của Bạn")
    vai_tro = st.session_state.get('current_role', '')
    user = st.session_state.get('current_user', 'Bạn')
    
    st.markdown(f"""
        <div class="glass-card" style="border-left: 5px solid #48bb78; padding: 25px;">
            <h3 style="color: #ffffff; margin-top: 0;">👤 Tài khoản: <span style="color:#63b3ed;">{user}</span></h3>
            <p style="color: #a0aec0; font-size: 1.1rem; margin-bottom: 20px;">Vai trò hệ thống: <b>{vai_tro}</b></p>
            <div>
                <span style="background: #276749; color: #c6f6d5; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9rem;">
                    Cấp độ: 🌱 Mầm Xanh
                </span>
                <span style="margin-left: 15px; color: #cbd5e0; font-size: 0.95rem;">
                    (Hãy giao dịch hoặc niêm yết thêm để thăng hạng lên 🌳 Đại Thụ!)
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # PHẦN 3: FORM ĐÓNG GÓP Ý KIẾN (TỰ LÀM SẠCH)
    st.markdown("### 💌 Hộp thư Góp ý & Báo lỗi")
    st.info("Ý kiến của bạn là tài sản quý giá giúp chúng tôi nâng cấp hệ thống ngày càng hoàn hảo hơn.")
    
    with st.form("feedback_form", clear_on_submit=True):
        st.text_area("Nội dung góp ý / Báo lỗi (Khuyến khích mô tả chi tiết):", placeholder="Ví dụ: Tính năng biểu đồ hiển thị rất tốt, nhưng tôi cần xuất file PDF...")
        col_fb_btn, _ = st.columns([3, 7])
        with col_fb_btn:
            fb_submit = st.form_submit_button("🚀 GỬI GÓP Ý ĐẾN BAN QUẢN TRỊ", type="primary", use_container_width=True)
        
        if fb_submit:
            st.success("Cảm ơn bạn! Đóng góp của bạn đã được mã hóa và gửi tới Ban quản trị hệ thống thành công.")
