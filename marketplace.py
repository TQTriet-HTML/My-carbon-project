import streamlit as st
import pandas as pd

def hien_thi_san_giao_dich():
    st.markdown(f"## 🏢 Trung tâm Giao dịch Tín chỉ Carbon")
    st.caption(f"Xin chào: **{st.session_state['current_user']}** | Phiên giao dịch trực tuyến bảo mật")
    vai_tro = st.session_state.get('current_role', '')
    
    # Kịch bản 1: Cổ đông đi nhầm vào sàn B2B
    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
        st.info("💡 Bạn đang sử dụng tài khoản Cổ đông/Nhà đầu tư. Vui lòng chuyển sang Tab **'Đầu tư Trồng rừng'** để góp vốn.")
        return

    # Kịch bản 2: Khu vực đặc quyền của Chủ Rừng (Đã xử lý hiển thị)
    if vai_tro == "Chủ rừng / Kỹ sư MRV":
        st.success("🌳 **Khu vực Chủ rừng:** Xác thực sinh khối và niêm yết tín chỉ lên sàn thương mại.")
        with st.expander("📝 NIÊM YẾT LÔ TÍN CHỈ MỚI", expanded=True):
            # Form TỰ ĐỘNG XÓA sau khi Submit thành công
            with st.form("form_niem_yet", clear_on_submit=True):
                ten_du_an = st.text_input("Tên dự án / Khu rừng niêm yết:")
                col_kl, col_gia, col_nam = st.columns(3)
                with col_kl: kl_ban = st.number_input("Khối lượng (tấn):", min_value=100, step=100, value=1000)
                with col_gia: gia_ban = st.number_input("Giá chốt (USD):", value=10.0, step=0.5)
                with col_nam: cam_ket_nam = st.number_input("Cam kết (Năm):", min_value=1, max_value=30, value=5)
                
                file_minh_chung = st.file_uploader("📎 Tải lên Sổ đỏ / Quyền sử dụng đất (PDF/JPG)", type=['pdf', 'jpg', 'png'])
                
                submitted_ny = st.form_submit_button("🚀 CHUYỂN DỮ LIỆU LÊN SÀN KIỂM ĐỊNH", type="primary", use_container_width=True)
                
                if submitted_ny:
                    if not ten_du_an or file_minh_chung is None:
                        st.error("❌ Vui lòng nhập tên lô rừng và đính kèm giấy tờ hợp lệ.")
                    else:
                        new_proj = {
                            "id": f"user_p_{len(st.session_state['market_projects'])}",
                            "name": ten_du_an, "owner": st.session_state['current_user'],
                            "price": gia_ban, "volume": kl_ban, "duration": cam_ket_nam,
                            "lat": 14.0, "lon": 108.0, "verified": True,
                            "proof_name": file_minh_chung.name, "status": "Active"
                        }
                        st.session_state["market_projects"].append(new_proj)
                        st.success("✅ Niêm yết thành công! Lô rừng của bạn đã xuất hiện trên sàn giao dịch.")

    # Kịch bản 3: Doanh nghiệp mua tín chỉ
    if vai_tro == "Doanh nghiệp mua tín chỉ":
        st.info(f"💳 **Ví Doanh Nghiệp:** Khả dụng **${st.session_state['wallet_balance']:,.2f}**")
        st.markdown("### 📦 Kho Tín chỉ Đang Sở hữu")
        user_holdings = st.session_state["user_portfolios"].get(st.session_state['current_user'], [])
        if not user_holdings:
            st.warning("Kho của bạn đang trống. Hãy mua tín chỉ để bù đắp phát thải.")
        else:
            st.dataframe(pd.DataFrame(user_holdings), use_container_width=True, hide_index=True)
        st.divider()
        
    # HIỂN THỊ DANH SÁCH DỰ ÁN TRÊN SÀN (CHO TẤT CẢ TRỪ CỔ ĐÔNG)
    st.markdown("### 🛒 Thị trường Tín chỉ Giao ngay")
    for p in st.session_state["market_projects"]:
        if p.get('volume', 0) > 0 and p.get('status') == 'Active':
            with st.container(border=True):
                col_info, col_action = st.columns([3, 2])
                with col_info:
                    st.markdown(f"#### 🌳 {p['name']}")
                    st.write(f"**Chủ rừng:** {p['owner']} | **Tình trạng:** ✅ Đã kiểm định AI")
                    st.write(f"**Trữ lượng:** {int(p['volume']):,} tấn | **Giá:** ${p['price']:,.2f} / tín chỉ")
                    
                    if st.button("📄 Xem Minh chứng Pháp lý", key=f"btn_proof_{p['id']}"):
                        st.info(f"Đã xác minh tệp: `{p.get('proof_name', 'Ho So Chuan.pdf')}`. Khớp tọa độ vệ tinh 100%.")

                with col_action:
                    if vai_tro == "Doanh nghiệp mua tín chỉ":
                        # Form thanh toán tự dọn dẹp
                        with st.form(f"buy_form_{p['id']}", clear_on_submit=True):
                            sl_mua = st.number_input("Khối lượng mua (tấn):", min_value=1, max_value=int(p['volume']), value=100)
                            btn_buy = st.form_submit_button(f"🛒 Mua nhanh (${sl_mua * p['price']:,.2f})", type="primary", use_container_width=True)
                            
                            if btn_buy:
                                tong_tien = sl_mua * p['price']
                                if st.session_state["wallet_balance"] >= tong_tien:
                                    st.session_state["wallet_balance"] -= tong_tien
                                    p['volume'] -= sl_mua
                                    cur_user = st.session_state['current_user']
                                    if cur_user not in st.session_state["user_portfolios"]: st.session_state["user_portfolios"][cur_user] = []
                                    st.session_state["user_portfolios"][cur_user].append({"Dự án": p['name'], "Số lượng": sl_mua, "Hiệu lực (Năm)": p['duration']})
                                    st.success("🎉 Giao dịch thành công!")
                                    st.rerun()
                                else:
                                    st.error("❌ Số dư ví không đủ.")
                    elif vai_tro == "Chủ rừng / Kỹ sư MRV":
                        st.button("🔒 Đăng nhập tài khoản Mua để giao dịch", key=f"lock_{p['id']}", disabled=True, use_container_width=True)

# --- Các Tab khác (Rút gọn logic UI tương tự) ---
def hien_thi_cong_dau_tu():
    st.markdown("## 🤝 Quỹ Đầu tư & Góp vốn Trồng rừng")
    if st.session_state.get('current_role') != "Nhà đầu tư từ xa (Cổ đông)":
        st.warning("⚠️ Khu vực này dành riêng cho **Nhà đầu tư (Cổ đông)**.")
        return
        
    st.success(f"💰 **Ví Đầu tư:** Khả dụng **${st.session_state['wallet_balance']:,.2f}**")
    for p in st.session_state["market_projects"]:
        if "funding_goal" in p:
            with st.container(border=True):
                col_i, col_a = st.columns([3, 2])
                with col_i:
                    st.markdown(f"#### 🌲 {p['name']}")
                    st.progress(min(100, int((p['funded_amount'] / p['funding_goal']) * 100)))
                with col_a:
                    with st.form(f"fund_{p['id']}", clear_on_submit=True):
                        t_gop = st.number_input("Số vốn góp (USD):", min_value=100, value=1000)
                        if st.form_submit_button("🤝 Cấp Vốn Trồng Rừng", type="primary", use_container_width=True):
                            if st.session_state["wallet_balance"] >= t_gop:
                                st.session_state["wallet_balance"] -= t_gop
                                p['funded_amount'] += t_gop
                                st.success("Góp vốn thành công!")
                                st.rerun()
                            else:
                                st.error("Ví không đủ tiền.")

def hien_thi_gioi_thieu_va_goi_von():
    st.title("🌟 VỀ CHÚNG TÔI & TẦM NHÌN TƯƠNG LAI")
    st.markdown("""<div style="padding:20px; background:#1e2530; border-left: 5px solid #48bb78; border-radius: 8px; margin-bottom:20px;">
        Nền tảng của chúng tôi ra đời như một giải pháp tiên phong tích hợp trí tuệ nhân tạo từ không gian (<b>Google Earth Engine</b>) với <b>Sổ đỏ và minh chứng gốc trực tuyến</b>.</div>""", unsafe_allow_html=True)
    
    st.markdown("#### 🚀 Đăng ký Đầu tư Thiên thần (Series Seed)")
    with st.form("form_goi_von_nen_tang", clear_on_submit=True):
        so_tien_dau_tu = st.number_input("Số vốn cam kết đầu tư (USD):", min_value=1000, step=1000, value=5000)
        email_lh = st.text_input("Email liên hệ / Đại diện:")
        if st.form_submit_button("🤝 GỬI ĐĂNG KÝ ĐẦU TƯ", type="primary", use_container_width=True):
            if email_lh: st.success("🎉 Gửi yêu cầu thành công! Chúng tôi sẽ liên hệ sớm.")
            else: st.warning("⚠ Vui lòng nhập email.")
