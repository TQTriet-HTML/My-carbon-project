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

    # Tiêu đề lớn màu xanh lá bao quát
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

def hien_thi_gioi_thieu_va_goi_von():
    st.markdown("""
        <h2 style='color:#48bb78; text-align:center; font-weight:900; margin-bottom:25px;'>
            VỀ CHÚNG TÔI & LỘ TRÌNH PHÁT TRIỂN
        </h2>
    """, unsafe_allow_html=True)
    st.write("Nền tảng kiểm kê và giao dịch tín chỉ carbon tích hợp AI & viễn thám không gian.")
