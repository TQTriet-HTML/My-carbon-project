import streamlit as st
import pandas as pd

def hien_thi_vinh_danh_va_gop_y():
    st.title("🏆 CỘNG ĐỒNG & BẢNG VÀNG VINH DANH")
    st.markdown("Nơi tri ân những cá nhân, tổ chức tiên phong vì một tương lai Net-Zero toàn cầu.")
    
    st.divider()
    
    # 1. BẢNG VÀNG VINH DANH (Leaderboard)
    st.markdown("### 🌟 Bảng Vàng Nền Tảng (Top Đóng Góp)")
    col_top1, col_top2 = st.columns(2)
    
    with col_top1:
        st.success("👑 **Top Doanh nghiệp & Nhà Đầu tư (Bù đắp & Góp vốn)**")
        df_dn = pd.DataFrame({
            "Hạng": ["🥇 1", "🥈 2", "🥉 3"],
            "Tổ chức / Cá nhân": ["Vinamilk", "Vietcombank", "FPT Software"],
            "Đóng góp": ["150,000 tấn", "85,000 tấn", "42,000 tấn"]
        })
        st.dataframe(df_dn, hide_index=True, use_container_width=True)
        
    with col_top2:
        st.info("🌳 **Top Chủ Rừng & Kỹ sư MRV (Bảo vệ sinh khối)**")
        df_cr = pd.DataFrame({
            "Hạng": ["🥇 1", "🥈 2", "🥉 3"],
            "Chủ rừng": ["BQL Rừng Cà Mau", "Dự án Bắc Trung Bộ", "Vườn QG Cát Tiên"],
            "Cung cấp": ["250,000 tín chỉ", "120,000 tín chỉ", "80,000 tín chỉ"]
        })
        st.dataframe(df_cr, hide_index=True, use_container_width=True)
        
    st.divider()
    
    # 2. CUỘC THI KIẾN TẠO XANH
    st.markdown("### 🎯 Cuộc thi: Đại sứ Kiến tạo Xanh Toàn cầu")
    st.markdown("""
    **Thử thách:** Cá nhân/Tổ chức có lượng giao dịch tín chỉ lẻ hoặc tích cực báo cáo vi phạm nhất trên nền tảng.
    - 🎁 **Giải thưởng:** Chuyến đi thực tế thăm thảm thực vật rừng ngập mặn Cà Mau + Kỷ niệm chương Gỗ sinh thái.
    - ⏳ **Thời gian chốt sổ:** 31/12/2026
    """)
    if st.button("🚀 Tham gia Thi đua", type="primary"):
        st.balloons()
        st.success("🎉 Đăng ký thành công! Hãy tích cực giao dịch và tương tác để tích lũy điểm trên Bảng Vàng.")
        
    st.divider()
    
    # 3. LIÊN HỆ & GÓP Ý CẢI THIỆN
    st.markdown("### 📬 Liên hệ & Đóng góp ý kiến")
    st.markdown("Mọi ý kiến đóng góp của bạn là viên gạch quý giá giúp nền tảng ngày càng hoàn thiện và vươn tầm quốc tế.")
    with st.container(border=True):
        loai_gop_y = st.selectbox("Chủ đề:", ["Đề xuất tính năng mới", "Báo cáo lỗi kỹ thuật (Bug)", "Hợp tác đối tác / Mở rộng thị trường", "Khác"])
        noi_dung = st.text_area("Nội dung chi tiết (Chúng tôi luôn lắng nghe bạn):")
        email_lh = st.text_input("Email liên hệ của bạn (Để chúng tôi phản hồi):")
        
        if st.button("✉️ Gửi Đóng Góp"):
            if noi_dung:
                st.success("💖 Cảm ơn bạn rất nhiều! Ý kiến của bạn đã được gửi trực tiếp đến Đội ngũ Kỹ thuật và Ban Sáng lập.")
            else:
                st.warning("⚠ Vui lòng nhập nội dung góp ý trước khi gửi.")
