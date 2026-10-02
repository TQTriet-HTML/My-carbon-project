import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
from auth import load_users

# --- 1. GIAO DIỆN SÀN GIAO DỊCH TÍN CHỈ (B2B / B2C) ---
def hien_thi_san_giao_dich():
    st.markdown(f"## 🏢 Trung tâm Giao dịch Tín chỉ Carbon")
    st.caption(f"Xin chào: **{st.session_state['current_user']}** | Phiên giao dịch trực tuyến bảo mật")
    vai_tro = st.session_state.get('current_role', '')
    
    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
        st.info("💡 Bạn đang đăng nhập bằng tài khoản Cổ đông dự án rừng. Vui lòng chuyển sang Tab **'Quỹ Đầu tư Trồng rừng'** ở phía trên.")
        return

    if vai_tro == "Doanh nghiệp mua tín chỉ":
        st.success(f"💳 **Ví Khách hàng:** Khả dụng **${st.session_state['wallet_balance']:,.2f}** | Trạng thái: Đã xác thực KYC")
        if st.button("💵 Nạp thêm $50,000 vào ví"):
            st.session_state["wallet_balance"] += 50000.0
            st.rerun()
            
        st.markdown("### 📦 Kho Tín chỉ Carbon Đang Sở hữu của Bạn")
        current_user = st.session_state['current_user']
        user_holdings = st.session_state["user_portfolios"].get(current_user, [])
        
        if not user_holdings:
            st.info("Kho của bạn đang trống. Hãy chọn mua các dự án bên dưới để tích lũy tín chỉ.")
        else:
            df_portfolio = pd.DataFrame(user_holdings)
            df_portfolio.columns = ["Dự án sở hữu", "Số lượng (tấn)", "Thời hạn hiệu lực"]
            st.dataframe(df_portfolio, use_container_width=True, hide_index=True)
        st.divider()
        
    elif vai_tro == "Chủ rừng / Kỹ sư MRV":
        st.info("🌳 **Khu vực Chủ rừng:** Nộp hồ sơ minh chứng gốc và niêm yết tín chỉ lên sàn.")
        with st.expander("📝 NIÊM YẾT LÔ TÍN CHỈ MỚI", expanded=False):
            ten_du_an = st.text_input("Tên dự án / Lô rừng:")
            kl_ban = st.number_input("Khối lượng tín chỉ muốn bán (tấn):", min_value=100, step=100)
            gia_ban = st.number_input("Giá bán mỗi tín chỉ (USD):", value=10.0)
            cam_ket_nam = st.number_input("Thời hạn cam kết bảo vệ rừng (Năm):", min_value=1, max_value=30, value=5)
            file_minh_chung = st.file_uploader("📎 Tải lên Sổ đỏ / Giấy tờ pháp lý gốc", type=['pdf', 'jpg', 'png'])
            
            if st.button("🚀 ĐƯA LÊN SÀN GIAO DỊCH", type="primary"):
                if not ten_du_an or file_minh_chung is None:
                    st.error("❌ Vui lòng điền tên và tải minh chứng pháp lý.")
                else:
                    new_proj = {
                        "id": f"user_p_{len(st.session_state['market_projects'])}",
                        "name": ten_du_an,
                        "owner": st.session_state['current_user'],
                        "price": gia_ban,
                        "volume": kl_ban,
                        "duration": cam_ket_nam,
                        "lat": 11.4280, 
                        "lon": 107.4286,
                        "verified": True,
                        "proof_file": file_minh_chung,
                        "proof_name": file_minh_chung.name,
                        "status": "Active"
                    }
                    st.session_state["market_projects"].append(new_proj)
                    st.success("✅ Thành công! Lô tín chỉ đã lên sàn thương mại.")

    st.divider()
    st.markdown("### 🛒 Danh mục Tín chỉ đang giao dịch trên Sàn")
    
    for p in st.session_state["market_projects"]:
        if p['volume'] > 0 and p.get('status', 'Active') == 'Active':
            with st.container(border=True):
                col_info, col_action = st.columns([3, 2])
                
                with col_info:
                    st.markdown(f"#### 🌳 {p['name']}")
                    st.write(f"**Chủ sở hữu:** {p['owner']} | **Trạng thái:** ✅ Đã kiểm định")
                    st.write(f"**Trữ lượng còn lại:** {int(p['volume']):,} tấn | **Giá chốt:** ${p['price']:,.2f} / tín chỉ")
                    st.write(f"⏳ **Thời hạn hiệu lực:** {p['duration']} năm")
                    
                    if st.button("📄 Xem Minh chứng Pháp lý", key=f"btn_proof_{p['id']}"):
                        st.session_state[f"show_proof_{p['id']}"] = not st.session_state.get(f"show_proof_{p['id']}", False)
                    
                    if st.session_state.get(f"show_proof_{p['id']}", False):
                        st.markdown(f"**Tệp:** `{p.get('proof_name', 'Tiêu chuẩn')}`")
                        if p.get('proof_file') is not None and hasattr(p['proof_file'], 'type'):
                            if p['proof_file'].type in ["image/jpeg", "image/png"]:
                                st.image(p['proof_file'], caption="Sổ đỏ gốc", use_container_width=True)

                with col_action:
                    if vai_tro == "Doanh nghiệp mua tín chỉ":
                        is_shareholder = False
                        cur_user = st.session_state['current_user']
                        for inv in st.session_state.get("investor_portfolios", {}).get(cur_user, []):
                            if inv["Dự án"] == p['name']:
                                is_shareholder = True
                                break
                        
                        thuc_te_gia = p['price'] * 0.96 if is_shareholder else p['price']
                        if is_shareholder:
                            st.success("🌟 **Đặc quyền Cổ đông:** Giảm 4%!")
                        
                        sl_mua = st.number_input("Số lượng mua (tấn):", min_value=1, max_value=int(p['volume']), value=10, key=f"buy_sl_{p['id']}")
                        tong_tien = sl_mua * thuc_te_gia
                        st.info(f"Thanh toán: **${tong_tien:,.2f}**")
                        
                        if st.button("🛒 Thanh toán mua", key=f"buy_btn_{p['id']}", type="primary", use_container_width=True):
                            if st.session_state["wallet_balance"] >= tong_tien:
                                st.session_state["wallet_balance"] -= tong_tien
                                p['volume'] -= sl_mua
                                
                                if cur_user not in st.session_state["user_portfolios"]:
                                    st.session_state["user_portfolios"][cur_user] = []
                                
                                expiry_year = 2026 + p['duration']
                                st.session_state["user_portfolios"][cur_user].append({
                                    "project": p['name'],
                                    "amount": sl_mua,
                                    "expiry": f"Tháng 12/{expiry_year} (Cam kết {p['duration']} năm)"
                                })
                                st.success("🎉 Giao dịch thành công!")
                                st.rerun()
                            else:
                                st.error("❌ Ví không đủ tiền.")
                    else:
                        st.button("🔒 Đăng nhập tài khoản Mua để giao dịch", disabled=True, use_container_width=True)


# --- 2. GIAO DIỆN QUỸ ĐẦU TƯ TRỒNG RỪNG ---
def hien_thi_cong_dau_tu():
    st.markdown(f"## 🤝 Quỹ Đầu tư & Góp vốn Trồng rừng")
    st.caption(f"Xin chào Cổ đông: **{st.session_state['current_user']}**")
    vai_tro = st.session_state.get('current_role', '')
    
    if vai_tro != "Nhà đầu tư từ xa (Cổ đông)" and vai_tro != "Chủ rừng / Kỹ sư MRV":
        st.warning("⚠️ Khu vực này dành riêng cho **Nhà đầu tư (Cổ đông)** và **Chủ rừng**.")
        return

    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
        st.success(f"💰 **Ví Đầu tư Cổ đông:** Khả dụng **${st.session_state['wallet_balance']:,.2f}**")
        st.markdown("### 📊 Danh mục Cổ phần Đã góp vốn của Bạn")
        current_user = st.session_state['current_user']
        investor_holdings = st.session_state.get("investor_portfolios", {}).get(current_user, [])
        if not investor_holdings:
            st.info("Bạn chưa góp vốn vào dự án rừng nào.")
        else:
            st.dataframe(pd.DataFrame(investor_holdings), use_container_width=True, hide_index=True)
        st.divider()

    st.markdown("### 🚀 Danh sách Dự án đang Gọi vốn Trồng rừng")
    for p in st.session_state["market_projects"]:
        if "funding_goal" in p and p.get('status', 'Active') == 'Active':
            with st.container(border=True):
                col_i, col_a = st.columns([3, 2])
                with col_i:
                    st.markdown(f"#### 🌲 {p['name']}")
                    st.write(f"**Chủ đầu tư:** {p['owner']}")
                    progress = min(100, int((p['funded_amount'] / p['funding_goal']) * 100))
                    st.info(f"💵 **Tiến độ góp vốn:** ${p['funded_amount']:,.0f} /${p['funding_goal']:,.0f} ({progress}%)")
                    st.progress(progress)
                with col_a:
                    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
                        t_gop = st.number_input("Số vốn muốn góp (USD):", min_value=100, max_value=int(p['funding_goal'] - p['funded_amount']) if p['funded_amount'] < p['funding_goal'] else 1, value=1000, key=f"fund_input_{p['id']}")
                        if st.button("🤝 Góp vốn nhận cổ phần", key=f"btn_fund_{p['id']}", type="primary", use_container_width=True):
                            if st.session_state["wallet_balance"] >= t_gop:
                                st.session_state["wallet_balance"] -= t_gop
                                p['funded_amount'] += t_gop
                                cur_inv = st.session_state['current_user']
                                if cur_inv not in st.session_state["investor_portfolios"]:
                                    st.session_state["investor_portfolios"][cur_inv] = []
                                st.session_state["investor_portfolios"][cur_inv].append({
                                    "Dự án": p['name'],
                                    "Vốn góp": f"${t_gop:,.2f}",
                                    "Quyền lợi": "Chia cổ tức + Giảm giá 4%"
                                })
                                st.success("🎉 Góp vốn thành công!")
                                st.rerun()
                            else:
                                st.error("❌ Ví không đủ tiền.")
                    else:
                        st.info("Đăng nhập tài khoản Cổ đông để góp vốn.")


# --- 3. TRANG GIỚI THIỆU & GỌI VỐN PHÁT TRIỂN NỀN TẢNG (SỬ DỤNG CARD THAY CHO METRIC ĐỂ KHÔNG BỊ CẮT CHỮ) ---
def hien_thi_gioi_thieu_va_goi_von():
    st.title("🌟 VỀ CHÚNG TÔI & TẦM NHÌN TƯƠNG LAI")
    
    st.markdown("""
    ### 💡 Sứ mệnh & Góc nhìn của Sáng lập
    Thị trường tín chỉ carbon toàn cầu đang bước vào kỷ nguyên bản lề, nhưng rào cản lớn nhất hiện nay là sự **thiếu minh bạch trong dữ liệu sinh khối** và **độ trễ trong thẩm định pháp lý**. 
    
    Nền tảng của chúng tôi ra đời như một giải pháp tiên phong tích hợp trí tuệ nhân tạo từ không gian (**Google Earth Engine**) với **Sổ đỏ và minh chứng gốc trực tuyến**, giúp loại bỏ hoàn toàn tình trạng "rừng ma" hay "khai khống trữ lượng", đưa các doanh nghiệp và chủ rừng đến gần nhau với độ tin cậy tuyệt đối.
    """)

    st.divider()

    st.markdown("### 🏛️ Chứng nhận Uy tín & Đối tác Pháp lý")
    
    # Sử dụng các khối Card Markdown được thiết kế riêng để hiển thị trọn vẹn văn bản dài, không bị lỗi cắt cụt chữ
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1e2530; padding: 15px; border-radius: 8px; border: 1px solid #2d3748; height: 140px;">
            <p style="color: #a0aec0; font-size: 13px; margin-bottom: 5px;">Tiêu chuẩn Quốc tế</p>
            <h4 style="color: #ffffff; font-size: 16px; margin-top: 0; line-height: 1.3;">VCS & Gold Standard</h4>
            <p style="color: #48bb78; font-size: 12px; margin-top: 10px;">✓ Đạt chuẩn toàn cầu</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background-color: #1e2530; padding: 15px; border-radius: 8px; border: 1px solid #2d3748; height: 140px;">
            <p style="color: #a0aec0; font-size: 13px; margin-bottom: 5px;">Công nghệ Vệ tinh</p>
            <h4 style="color: #ffffff; font-size: 16px; margin-top: 0; line-height: 1.3;">ESA WorldCover & GEE</h4>
            <p style="color: #48bb78; font-size: 12px; margin-top: 10px;">✓ Real-time AI</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background-color: #1e2530; padding: 15px; border-radius: 8px; border: 1px solid #2d3748; height: 140px;">
            <p style="color: #a0aec0; font-size: 13px; margin-bottom: 5px;">Bảo chứng Pháp lý</p>
            <h4 style="color: #ffffff; font-size: 16px; margin-top: 0; line-height: 1.3;">Sổ đỏ Lâm nghiệp Gốc</h4>
            <p style="color: #48bb78; font-size: 12px; margin-top: 10px;">✓ Xác thực 100%</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div style="background-color: #1e2530; padding: 15px; border-radius: 8px; border: 1px solid #2d3748; height: 140px;">
            <p style="color: #a0aec0; font-size: 13px; margin-bottom: 5px;">Hệ thống Kiểm toán</p>
            <h4 style="color: #ffffff; font-size: 16px; margin-top: 0; line-height: 1.3;">Smart Contract Escrow</h4>
            <p style="color: #48bb78; font-size: 12px; margin-top: 10px;">✓ Minh bạch tuyệt đối</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("🛡️ *Mọi dữ liệu tọa độ không gian trên hệ thống đều được đối chiếu chéo qua các cơ sở dữ liệu quốc gia và hình ảnh vệ tinh đa phổ, đảm bảo tính pháp lý trước khi niêm yết thương mại.*")

    st.divider()

    # --- KHU VỰC KÊU GỌI VỐN PHÁT TRIỂN NỀN TẢNG ---
    st.markdown("### 🌱 Cùng nhau xây dựng Sàn giao dịch Xanh — Bước tiến mới của Nhân loại")
    st.markdown("""
    Để mở rộng quy mô công nghệ AI vệ tinh, tích hợp thêm các tiêu chuẩn kiểm định quốc tế mới và đưa nền tảng vươn tầm khu vực Đông Nam Á, chúng tôi chính thức mở cổng **Kêu gọi vốn Chiến lược phát triển nền tảng (Series Seed)** dành cho các nhà đầu tư thiên thần, quỹ đầu tư tác động xã hội (Impact Investment) và cộng đồng.
    """)

    with st.container(border=True):
        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            st.markdown("#### 🎯 Mục tiêu gọi vốn phát triển Nền tảng Công nghệ")
            st.write("- **Huy động mục tiêu:** $500,000.00")
            st.write("- **Đã nhận cam kết:** $320,000.00 (64%)")
            st.progress(0.64)
            st.write("**Quyền lợi nhà đầu tư chiến lược:** Sở hữu cổ phần chuyển đổi (SAFE), đồng hành cùng kỳ lân công nghệ xanh đầu tiên tại Việt Nam.")
        
        with col_p2:
            st.markdown("#### 🚀 Tham gia đồng hành")
            so_tien_dau_tu = st.number_input("Số vốn cam kết đầu tư (USD):", min_value=1000, step=1000, value=5000)
            email_lh = st.text_input("Email liên hệ / Đại diện:")
            if st.button("🤝 GỬI ĐĂNG KÝ ĐẦU TƯ NỀN TẢNG", type="primary", use_container_width=True):
                if email_lh:
                    st.success(f"🎉 Cảm ơn bạn! Yêu cầu góp vốn phát triển nền tảng trị giá **${so_tien_dau_tu:,.2f}** đã được gửi đến ban sáng lập. Chúng tôi sẽ liên hệ qua `{email_lh}` trong 24h tới.")
                else:
                    st.warning("⚠ Vui lòng nhập email liên hệ.")
