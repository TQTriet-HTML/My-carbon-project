import streamlit as st

def hien_thi_vinh_danh_va_gop_y():
    st.markdown("""
        <style>
        .section-header-green {
            color: #48bb78 !important;
            font-size: clamp(24px, 2.8vw, 34px) !important;
            font-weight: 900 !important;
            text-align: center;
            letter-spacing: 1.5px;
            margin-bottom: 25px;
            text-transform: uppercase;
            text-shadow: 0 0 16px rgba(72, 187, 120, 0.4);
        }
        .table-title-green {
            color: #48bb78 !important;
            font-size: 1.25rem !important;
            font-weight: 800 !important;
            text-align: center;
            letter-spacing: 1px;
            margin-bottom: 15px;
            text-transform: uppercase;
        }
        div[data-testid="stTable"] table {
            width: 100% !important;
            text-align: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Tiêu đề lớn màu xanh lá bao quát
    st.markdown('<div class="section-header-green">BẢNG VÀNG & TÔN VINH</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown('<div class="table-title-green">TOP DOANH NGHIỆP</div>', unsafe_allow_html=True)
            st.table({
                "Hạng": ["1", "2", "3"],
                "Doanh Nghiệp": ["Vinamilk", "FPT Software", "Vietcombank"],
                "Tín chỉ": ["50,000", "42,000", "38,500"]
            })

    with col2:
        with st.container(border=True):
            st.markdown('<div class="table-title-green">TOP DỰ ÁN TRỒNG RỪNG</div>', unsafe_allow_html=True)
            st.table({
                "Hạng": ["1", "2", "3"],
                "Dự Án": ["Rừng ngập mặn Cà Mau", "Dự án Bắc Trung Bộ", "KBT Nam Cát Tiên"],
                "CO2": ["1.2M", "850K", "520K"]
            })

    st.markdown("<hr style='border: 0.5px solid rgba(72, 187, 120, 0.2); margin: 35px 0;'>", unsafe_allow_html=True)
    st.markdown('<div class="section-header-green">QUÁ TRÌNH SỐNG XANH</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.write("Ghi nhận hành trình và đóng góp giảm phát thải thực tế của cộng đồng.")
