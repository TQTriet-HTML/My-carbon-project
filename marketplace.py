import streamlit as st
import pandas as pd
import numpy as np

def hien_thi_san_giao_dich():
    vai_tro = st.session_state.get('current_role', '')
    
    # 1. BẢNG THỐNG KÊ TÀI KHOẢN (ACCOUNT DASHBOARD)
    st.markdown(f"## 🏢 Dashboard Quản Lý Tài Khoản")
    
    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
        st.info("💡 Bạn đang sử dụng tài khoản Cổ đông/Nhà đầu tư. Vui lòng chuyển sang Tab **'Đầu tư Trồng rừng'** để góp vốn.")
        return

    elif vai_tro == "Doanh nghiệp mua tín chỉ":
        col1, col2, col3 = st.columns(3)
        user_holdings = st.session_state["user_portfolios"].get(st.session_state['current_user'], [])
        tong_tin_chi = sum(item["Số lượng"] for item in user_holdings) if user_holdings else 0
        
        col1.metric("💳 Số Dư Ví Của Bạn", f"${st.session_state['wallet_balance']:,.2f}", "+ 50,000.00")
        col2.metric("📦 Tổng Tín Chỉ Sở Hữu", f"{tong_tin_chi:,} Tấn", "Đã bù trừ Carbon")
        col3.metric("📈 Hạng Tín Nhiệm (ESG)", "Hạng A+", "Đạt chuẩn Net-Zero")
        
        with st.expander("💼 XEM CHI TIẾT KHO TÍN CHỈ CỦA BẠN", expanded=False):
            if not user_holdings:
                st.warning("Kho của bạn đang trống. Hãy mua tín chỉ để bù đắp phát thải.")
            else:
                st.dataframe(pd.DataFrame(user_holdings), use_container_width=True, hide_index=True)
        st.divider()

    elif vai_tro == "Chủ rừng / Kỹ sư MRV":
        col1, col2, col3 = st.columns(3)
        col1.metric("🌳 Diện Tích Sở Hữu", "1,500 Ha", "Đã xác thực tọa độ")
        col2.metric("📦 Khối Lượng Có Thể Bán", "550,000 Tấn", "Sinh khối tái tạo")
        col3.metric("💳 Doanh Thu Giao Dịch", "$0.00", "Chờ khớp lệnh")
        
        st.info("💡 **Khu vực Chủ rừng:** Xác thực sinh khối và niêm yết tín chỉ lên sàn thương mại.")
        with st.expander("📝 NIÊM YẾT LÔ TÍN CHỈ MỚI", expanded=True):
            with st.form("form_niem_yet", clear_on_submit=True):
                ten_du_an = st.text_input("Tên dự án / Khu rừng niêm yết:")
                col_kl, col_gia, col_nam = st.columns(3)
                with col_kl: kl_ban = st.number_input("Khối lượng (tấn):", min_value=100, step=100, value=1000)
                with col_gia: gia_ban = st.number_input("Giá chốt (USD):", value=10.5, step=0.5)
                with col_nam: cam_ket_nam = st.number_input("Cam kết (Năm):", min_value=1, max_value=30, value=5)
                
                file_minh_chung = st.file_uploader("📎 Tải lên Sổ đỏ / Quyền sử dụng đất", type=['pdf', 'jpg', 'png'])
                submitted_ny = st.form_submit_button("🚀 CHUYỂN DỮ LIỆU LÊN SÀN", type="primary", use_container_width=True)
                
                if submitted_ny:
                    if not ten_du_an or file_minh_chung is None:
                        st.error("❌ Vui lòng nhập tên lô rừng và đính kèm giấy tờ hợp lệ.")
                    else:
                        new_proj = {
                            "id": f"user_p_{len(st.session_state['market_projects'])}", "name": ten_du_an, 
                            "owner": st.session_state['current_user'], "price": gia_ban, "volume": kl_ban, 
                            "duration": cam_ket_nam, "lat": 14.0, "lon": 108.0, "verified": True,
                            "proof_name": file_minh_chung.name, "status": "Active"
                        }
                        st.session_state["market_projects"].append(new_proj)
                        st.success("✅ Niêm yết thành công! Lô rừng của bạn đã xuất hiện trên sàn giao dịch.")
        st.divider()

    # 2. BIỂU ĐỒ BIẾN ĐỘNG GIÁ TÍN CHỈ THỰC TẾ
    st.markdown("### 📈 Biểu đồ Giá Tín chỉ Giao ngay (30 Ngày)")
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
    prices = np.random.normal(loc=10.5, scale=0.4, size=30)
    # Tạo xu hướng tăng nhẹ
    trend = np.linspace(0, 1.5, 30)
    prices = prices + trend
    price_df = pd.DataFrame({'Giá Khớp Lệnh ($/tấn)': prices}, index=dates)
    st.line_chart(price_df, color="#48bb78", height=250)

    # 3. DANH SÁCH DỰ ÁN TRÊN SÀN
    st.markdown("### 🛒 Danh mục Tín chỉ Đang Chào Bán")
    for p in st.session_state["market_projects"]:
        if p.get('volume', 0) > 0 and p.get('status') == 'Active':
            with st.container(border=True):
                col_info, col_action = st.columns([3, 2])
                with col_info:
                    st.markdown(f"#### 🌳 {p['name']}")
                    st.write(f"**Chủ rừng:** {p['owner']} | **Tình trạng:** ✅ Đã kiểm định AI")
                    st.write(f"**Trữ lượng:** {int(p['volume']):,} tấn | **Giá bán:** **${p['price']:,.2f}** / tín chỉ")
                    if st.button("📄 Xem Minh chứng Pháp lý", key=f"btn_proof_{p['id']}"):
                        st.info(f"Đã xác minh tệp: `{p.get('proof_name', 'Ho So Chuan.pdf')}`. Khớp tọa độ 100%.")

                with col_action:
                    if vai_tro == "Doanh nghiệp mua tín chỉ":
                        with st.form(f"buy_form_{p['id']}", clear_on_submit=True):
                            sl_mua = st.number_input("Khối lượng mua (tấn):", min_value=1, max_value=int(p['volume']), value=100)
                            btn_buy = st.form_submit_button(f"🛒 Đặt Lệnh Mua (${sl_mua * p['price']:,.2f})", type="primary", use_container_width=True)
                            
                            if btn_buy:
                                tong_tien = sl_mua * p['price']
                                if st.session_state["wallet_balance"] >= tong_tien:
                                    st.session_state["wallet_balance"] -= tong_tien
                                    p['volume'] -= sl_mua
                                    cur_user = st.session_state['current_user']
                                    if cur_user not in st.session_state["user_portfolios"]: st.session_state["user_portfolios"][cur_user] = []
                                    st.session_state["user_portfolios"][cur_user].append({"Dự án": p['name'], "Số lượng": sl_mua, "Hiệu lực (Năm)": p['duration']})
                                    st.success("🎉 Khớp lệnh thành công! Tín chỉ đã được chuyển vào kho.")
                                    st.rerun()
                                else:
                                    st.error("❌ Số dư ví không đủ.")
                    elif vai_tro == "Chủ rừng / Kỹ sư MRV":
                        st.button("🔒 Đăng nhập tài khoản Mua để giao dịch", key=f"lock_{p['id']}", disabled=True, use_container_width=True)

def hien_thi_cong_dau_tu():
    st.markdown("## 🤝 Quỹ Đầu tư & Góp vốn Trồng rừng")
    st.info("Khu vực đang được nâng cấp!")

def hien_thi_gioi_thieu_va_goi_von():
    st.title("🌟 VỀ CHÚNG TÔI & TẦM NHÌN TƯƠNG LAI")
    
    # LỜI CẢM ƠN ĐÃ ĐƯỢC PHỤC HỒI MÀU XANH LÁ NỔI BẬT NHỜ CSS BÊN APP.PY
    st.markdown("""
        <div class="thank-you-banner">
            <span class="text-green">Thay mặt Đội ngũ Sáng lập, chúng tôi xin gửi </span>
            <span class="text-blue-bold">LỜI CẢM ƠN CHÂN THÀNH NHẤT</span>
            <span class="text-green"> đến Quý Chủ rừng, các Doanh nghiệp và Nhà đầu tư tiên phong đã tin tưởng sử dụng nền tảng. Sự đồng hành và nguồn vốn của Quý vị không chỉ là bảo chứng cho uy tín của hệ thống, mà còn là viên gạch nền móng kiến tạo nên một kỷ nguyên Net-Zero bền vững cho nhân loại!</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 💡 Sứ mệnh & Góc nhìn của Sáng lập
    <div class="mission-container">
        <p class="mission-text">
            Thị trường tín chỉ carbon toàn cầu đang bước vào kỷ nguyên bản lề, nhưng rào cản lớn nhất hiện nay là sự <b>thiếu minh bạch trong dữ liệu sinh khối</b> và <b>độ trễ trong thẩm định pháp lý</b>.
        </p>
        <p class="mission-text">
            Nền tảng của chúng tôi ra đời như một giải pháp tiên phong tích hợp trí tuệ nhân tạo từ không gian (<b>Google Earth Engine</b>) với <b>Sổ đỏ và minh chứng gốc trực tuyến</b>, giúp loại bỏ hoàn toàn tình trạng "rừng ma" hay "khai khống trữ lượng", đưa các doanh nghiệp và chủ rừng đến gần nhau với độ tin cậy tuyệt đối.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🏛️ Chứng nhận Uy tín & Đối tác Pháp lý")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="partner-card"><div class="pc-title">Tiêu chuẩn Quốc tế</div><div class="pc-value">VCS & Gold Standard</div><div class="pc-status">✔ Đạt chuẩn toàn cầu</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="partner-card"><div class="pc-title">Công nghệ Vệ tinh</div><div class="pc-value">ESA WorldCover & GEE</div><div class="pc-status">✔️ Real-time AI Tracking</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="partner-card"><div class="pc-title">Bảo chứng Pháp lý</div><div class="pc-value">Sổ đỏ Lâm nghiệp Gốc</div><div class="pc-status">✔️ Xác thực chéo 100%</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="partner-card"><div class="pc-title">Hệ thống Kiểm toán</div><div class="pc-value">Smart Contract Escrow</div><div class="pc-status">✔️ Minh bạch tuyệt đối</div></div>""", unsafe_allow_html=True)
