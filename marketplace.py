import streamlit as st
import pandas as pd
import numpy as np

def hien_thi_san_giao_dich():
    vai_tro = st.session_state.get('current_role', '')
    
    # 1. BẢNG THỐNG KÊ TÀI KHOẢN (ACCOUNT DASHBOARD)
    st.markdown(f"## 🏢 Dashboard Quản Lý Tài Khoản")
    
    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
        st.info("💡 Bạn đang sử dụng tài khoản Cổ đông/Nhà đầu tư. Nơi giao dịch tín chỉ giao ngay dành cho doanh nghiệp. Vui lòng chuyển sang Tab **'Đầu tư Trồng rừng'** để quản lý danh mục góp vốn.")
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


# --- CẬP NHẬT MỚI: MỞ RỘNG QUYỀN ĐẦU TƯ CHO MỌI ĐỐI TƯỢNG ---
def hien_thi_cong_dau_tu():
    st.markdown("## 🤝 Quỹ Đầu tư & Góp vốn Trồng rừng")
    st.caption(f"Xin chào: **{st.session_state['current_user']}** | Số dư đầu tư: **${st.session_state['wallet_balance']:,.2f}**")
    
    vai_tro = st.session_state.get('current_role', '')
    
    # THÔNG ĐIỆP KÊU GỌI ĐẦU TƯ CÁ NHÂN HÓA THEO VAI TRÒ
    if vai_tro == "Doanh nghiệp mua tín chỉ":
        st.markdown("""
        <div style="background: linear-gradient(90deg, rgba(26,32,44,1) 0%, rgba(44,82,130,1) 100%); padding: 20px; border-radius: 8px; border-left: 5px solid #63b3ed; margin-bottom: 25px;">
            <h4 style="color:#ffffff; margin-top:0;">Đầu tư sinh lời & Hưởng đặc quyền chiết khấu</h4>
            <p style="color:#e2e8f0; font-size:1rem; margin-bottom:0;">Với tư cách là Doanh nghiệp, việc rót vốn sớm vào các dự án trồng rừng không chỉ mang lại <b>lợi nhuận từ vốn đầu tư (ROI)</b> khi dự án thương mại hóa thành công, mà còn giúp Quý công ty nhận được đặc quyền <b>mua tín chỉ carbon với mức giá chiết khấu sâu</b> trong tương lai, đảm bảo nguồn cung Net-Zero bền vững với chi phí tối ưu nhất.</p>
        </div>
        """, unsafe_allow_html=True)
    elif vai_tro == "Chủ rừng / Kỹ sư MRV":
        st.markdown("""
        <div style="background: linear-gradient(90deg, rgba(26,32,44,1) 0%, rgba(39,103,73,1) 100%); padding: 20px; border-radius: 8px; border-left: 5px solid #48bb78; margin-bottom: 25px;">
            <h4 style="color:#ffffff; margin-top:0;">Gia tăng thu nhập & Mở rộng thị trường</h4>
            <p style="color:#e2e8f0; font-size:1rem; margin-bottom:0;">Việc đầu tư chéo vào các dự án lâm nghiệp khác trên nền tảng giúp các Chủ rừng <b>đa dạng hóa nguồn thu nhập</b> ngoài diện tích rừng hiện có. Đồng thời, đây là cơ hội để thiết lập mạng lưới đối tác, chia sẻ công nghệ MRV và <b>mở rộng quy mô thị trường</b> khai thác tín chỉ carbon liên kết.</p>
        </div>
        """, unsafe_allow_html=True)
    else: # Nhà đầu tư từ xa
        st.markdown("""
        <div style="background: linear-gradient(90deg, rgba(26,32,44,1) 0%, rgba(116,42,42,1) 100%); padding: 20px; border-radius: 8px; border-left: 5px solid #f6ad55; margin-bottom: 25px;">
            <h4 style="color:#ffffff; margin-top:0;">Bắt kịp xu hướng, Tạo thu nhập thụ động xanh</h4>
            <p style="color:#e2e8f0; font-size:1rem; margin-bottom:0;">Chào mừng Nhà đầu tư tiên phong! Bằng việc rót vốn vào các dự án khôi phục sinh thái, bạn không chỉ tạo ra dòng <b>thu nhập thụ động vững chắc</b> từ việc chia sẻ doanh thu bán tín chỉ carbon, mà còn trực tiếp <b>đóng góp vào phát kiến xanh của nhân loại</b>, chung tay bảo vệ địa cầu cho thế hệ tương lai.</p>
        </div>
        """, unsafe_allow_html=True)

    # DANH MỤC ĐẦU TƯ CỦA NGƯỜI DÙNG (CHUNG CHO MỌI ROLE)
    st.markdown("### 📊 Danh mục Cổ phần Đã góp vốn")
    current_user = st.session_state['current_user']
    investor_holdings = st.session_state.get("investor_portfolios", {}).get(current_user, [])
    if not investor_holdings:
        st.info("Bạn chưa góp vốn vào dự án rừng nào. Hãy chọn một dự án tiềm năng bên dưới để bắt đầu hành trình xanh!")
    else:
        st.dataframe(pd.DataFrame(investor_holdings), use_container_width=True, hide_index=True)
    st.divider()

    # DANH SÁCH DỰ ÁN ĐANG GỌI VỐN
    st.markdown("### 🚀 Danh sách Dự án Đang Kêu gọi Vốn")
    for p in st.session_state["market_projects"]:
        if "funding_goal" in p and p.get('status', 'Active') == 'Active':
            with st.container(border=True):
                col_i, col_a = st.columns([3, 2])
                with col_i:
                    st.markdown(f"#### 🌲 {p['name']}")
                    st.write(f"**Chủ dự án:** {p['owner']}")
                    progress = min(100, int((p['funded_amount'] / p['funding_goal']) * 100))
                    st.write(f"💵 **Tiến độ góp vốn:** ${p['funded_amount']:,.0f} /${p['funding_goal']:,.0f} ({progress}%)")
                    st.progress(progress)
                with col_a:
                    with st.form(f"fund_form_{p['id']}", clear_on_submit=True):
                        max_fund = int(p['funding_goal'] - p['funded_amount'])
                        t_gop = st.number_input("Số vốn muốn góp (USD):", min_value=100, max_value=max_fund if max_fund > 0 else 1, value=min(1000, max_fund))
                        
                        btn_txt = "🤝 Góp vốn Đầu tư"
                        if vai_tro == "Doanh nghiệp mua tín chỉ": btn_txt = "🤝 Đầu tư nhận Chiết khấu"
                        elif vai_tro == "Chủ rừng / Kỹ sư MRV": btn_txt = "🤝 Đầu tư Liên kết Rừng"
                        
                        btn_fund = st.form_submit_button(btn_txt, type="primary", use_container_width=True)
                        
                        if btn_fund:
                            if max_fund <= 0:
                                st.warning("Dự án này đã gọi vốn đủ.")
                            elif st.session_state["wallet_balance"] >= t_gop:
                                st.session_state["wallet_balance"] -= t_gop
                                p['funded_amount'] += t_gop
                                
                                if current_user not in st.session_state["investor_portfolios"]:
                                    st.session_state["investor_portfolios"][current_user] = []
                                
                                q_loi = "Chia sẻ cổ tức"
                                if vai_tro == "Doanh nghiệp mua tín chỉ": q_loi = "Chiết khấu 4% khi mua Tín chỉ"
                                elif vai_tro == "Chủ rừng / Kỹ sư MRV": q_loi = "Cổ tức + Hỗ trợ MRV"
                                
                                st.session_state["investor_portfolios"][current_user].append({
                                    "Dự án": p['name'],
                                    "Vốn góp": f"${t_gop:,.2f}",
                                    "Quyền lợi ưu tiên": q_loi
                                })
                                st.success("🎉 Rót vốn thành công! Xin cảm ơn sự đồng hành của bạn.")
                                st.rerun()
                            else:
                                st.error("❌ Số dư ví của bạn không đủ để thực hiện giao dịch này.")


def hien_thi_gioi_thieu_va_goi_von():
    st.title("🌟 VỀ CHÚNG TÔI & TẦM NHÌN TƯƠNG LAI")
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

    st.markdown("### 🏛️️ Chứng nhận Uy tín & Đối tác Pháp lý")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="partner-card"><div class="pc-title">Tiêu chuẩn Quốc tế</div><div class="pc-value">VCS & Gold Standard</div><div class="pc-status">✔ Đạt chuẩn toàn cầu</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="partner-card"><div class="pc-title">Công nghệ Vệ tinh</div><div class="pc-value">ESA WorldCover & GEE</div><div class="pc-status">✔️ Real-time AI Tracking</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="partner-card"><div class="pc-title">Bảo chứng Pháp lý</div><div class="pc-value">Sổ đỏ Lâm nghiệp Gốc</div><div class="pc-status">✔️ Xác thực chéo 100%</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="partner-card"><div class="pc-title">Hệ thống Kiểm toán</div><div class="pc-value">Smart Contract Escrow</div><div class="pc-status">✔️ Minh bạch tuyệt đối</div></div>""", unsafe_allow_html=True)
