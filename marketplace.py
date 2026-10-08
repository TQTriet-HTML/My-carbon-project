import streamlit as st

def hien_thi_san_giao_dich():
    st.markdown("""
        <style>
        .dash-title-green {
            color: #48bb78 !important;
            font-size: clamp(24px, 2.6vw, 32px) !important;
            font-weight: 900 !important;
            text-align: center;
            letter-spacing: 1.5px;
            margin-bottom: 25px;
            text-transform: uppercase;
            text-shadow: 0 0 16px rgba(72, 187, 120, 0.4);
        }
        .dash-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 10px;
        }
        .dash-label {
            color: #94a3b8;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 8px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            letter-spacing: 0.5px;
        }
        .dash-value {
            color: #ffffff;
            font-size: clamp(1.8rem, 2.2vw, 2.4rem);
            font-weight: 900;
            line-height: 1.1;
            margin-bottom: 10px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .dash-badge {
            display: inline-block;
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            background: rgba(72, 187, 120, 0.18);
            color: #48bb78;
            border: 1px solid rgba(72, 187, 120, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="dash-title-green">DASHBOARD QUẢN LÝ TÀI KHOẢN</div>', unsafe_allow_html=True)

    wallet_bal = st.session_state.get("wallet_balance", 150000.0)
    current_u = st.session_state.get("current_user", "")
    user_portfolios = st.session_state.get("user_portfolios", {})
    user_holdings = user_portfolios.get(current_u, [])
    total_tons = sum([item.get("volume", 0) for item in user_holdings]) if isinstance(user_holdings, list) else 0

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
                <div class="dash-card">
                    <div class="dash-label">Số Dư Ví Hệ Thống</div>
                    <div class="dash-value">${wallet_bal:,.2f}</div>
                    <div class="dash-badge">+ 50,000.00</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class="dash-card">
                    <div class="dash-label">Tổng Tín Chỉ Sở Hữu</div>
                    <div class="dash-value">{total_tons:,.0f} Tấn</div>
                    <div class="dash-badge">Đã bù trừ</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
                <div class="dash-card">
                    <div class="dash-label">Hạng Tín Nhiệm (ESG)</div>
                    <div class="dash-value">Hạng A+</div>
                    <div class="dash-badge">Đạt chuẩn</div>
                </div>
            """, unsafe_allow_html=True)
        
        with st.expander("XEM CHI TIẾT KHO TÍN CHỈ"):
            st.write("Danh mục tín chỉ carbon đã xác thực đang lưu trữ trong ví.")

    st.markdown('<div class="dash-title-green" style="margin-top: 35px;">BIỂU ĐỒ GIÁ TÍN CHỈ GIAO NGAY</div>', unsafe_allow_html=True)

def hien_thi_cong_dau_tu():
    st.markdown("""
        <h2 style='color:#48bb78; text-align:center; font-weight:900; margin-bottom:25px;'>
            CỔNG ĐẦU TƯ TRỒNG RỪNG TỪ XA
        </h2>
    """, unsafe_allow_html=True)
    st.info("Danh mục đầu tư sinh thái đang mở nhận vốn kỳ 2026.")

# ================= PHỤC HỒI NỘI DUNG TOÀN VẸN CHO TRANG VỀ CHÚNG TÔI =================
def hien_thi_gioi_thieu_va_goi_von():
    st.markdown("""
        <style>
        .about-title-green {
            color: #48bb78 !important;
            font-size: clamp(24px, 2.7vw, 34px) !important;
            font-weight: 900 !important;
            text-align: center;
            letter-spacing: 1.5px;
            margin-bottom: 25px;
            text-transform: uppercase;
            text-shadow: 0 0 16px rgba(72, 187, 120, 0.4);
        }
        .about-section-title {
            color: #48bb78;
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
            border-left: 4px solid #48bb78;
            padding-left: 10px;
        }
        .about-box {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(72, 187, 120, 0.35);
            border-radius: 12px;
            padding: 22px;
            margin-bottom: 20px;
            line-height: 1.7;
            color: #e2e8f0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="about-title-green">VỀ CHÚNG TÔI & LỘ TRÌNH PHÁT TRIỂN</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="about-section-title">SỨ MỆNH & TẦM NHÌN</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="about-box">
                Nền tảng được xây dựng với mục tiêu thương mại hóa và minh bạch hóa thị trường tín chỉ carbon tại Việt Nam. 
                Bằng cách kết hợp dữ liệu viễn thám vệ tinh đa quang phổ (Copernicus Sentinel-2) cùng mô hình trí tuệ nhân tạo (AI), 
                chúng tôi số hóa quy trình kiểm kê MRV (Measurement, Reporting, and Verification), xóa bỏ rào cản chi phí cao và 
                thời gian thẩm định kéo dài của các phương pháp thủ công truyền thống.
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="about-section-title">CÔNG NGHỆ LÕI (CORE TECHNOLOGY)</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
                <div class="about-box" style="text-align:center;">
                    <b style="color:#38bdf8; font-size:1.1rem;">Google Earth Engine</b><br>
                    Xử lý dữ liệu không gian thời gian thực trên quy mô cấp tỉnh và toàn quốc với độ trễ cực thấp.
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="about-box" style="text-align:center;">
                    <b style="color:#48bb78; font-size:1.1rem;">AI Biomass Estimation</b><br>
                    Thuật toán máy học tự động bóc tách chỉ số thực vật NDVI và tính toán độ che phủ sinh khối rừng.
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
                <div class="about-box" style="text-align:center;">
                    <b style="color:#eab308; font-size:1.1rem;">Escrow Smart Matching</b><br>
                    Cơ chế giao dịch ký quỹ tự động bảo đảm quyền lợi tài chính an toàn tuyệt đối cho người mua và chủ rừng.
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="about-section-title">LỘ TRÌNH PHÁT TRIỂN (ROADMAP 2026 - 2030)</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="about-box">
                <b>Giai đoạn 1 (2026):</b> Hoàn thiện hệ sinh thái kiểm kê tự động MRV, kết nối dữ liệu thí điểm các vùng rừng ngập mặn Cà Mau và rừng phòng hộ Bắc Trung Bộ.<br>
                <b>Giai đoạn 2 (2027 - 2028):</b> Tích hợp sàn giao dịch thứ cấp cho các doanh nghiệp FDI, niêm yết chứng chỉ tiêu chuẩn Verra/Gold Standard.<br>
                <b>Giai đoạn 3 (2029 - 2030):</b> Mở rộng quy mô ra toàn khu vực Đông Nam Á, trở thành trung tâm giao dịch hạn ngạch phát thải hàng đầu.
            </div>
        """, unsafe_allow_html=True)
