import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
from auth import load_users

# --- 1. GIAO DIỆN SÀN GIAO DỊCH TÍN CHỈ (B2B / B2C) ---
def hien_thi_san_giao_dich():
    st.markdown(f"## 🏢 Trung tâm Giao dịch Tín chỉ Carbon (Xin chào: **{st.session_state['current_user']}**)")
    vai_tro = st.session_state.get('current_role', '')
    
    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
        st.info("💡 Bạn đang đăng nhập bằng tài khoản Cổ đông. Vui lòng chuyển sang Tab **'Quỹ Đầu tư Trồng rừng'** ở phía trên để tham gia góp vốn và nhận đặc quyền giảm giá 4%.")
        return

    # Khung Ví & Kho của Doanh nghiệp / Chủ rừng
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
                        # Kiểm tra xem doanh nghiệp có phải là cổ đông góp vốn của dự án này không (để được giảm giá 4%)
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


# --- 2. GIAO DIỆN QUỸ ĐẦU TƯ TRỒNG RỪNG (CROWDFUNDING) ---
def hien_thi_cong_dau_tu():
    st.markdown(f"## 🤝 Quỹ Đầu tư & Góp vốn Trồng rừng (Xin chào Cổ đông: **{st.session_state['current_user']}**)")
    vai_tro = st.session_state.get('current_role', '')
    
    if vai_tro != "Nhà đầu tư từ xa (Cổ đông)" and vai_tro != "Chủ rừng / Kỹ sư MRV":
        st.warning("⚠️ Khu vực này dành riêng cho **Nhà đầu tư (Cổ đông)** và **Chủ rừng**. Vui lòng đăng ký đúng vai trò để tham gia góp vốn.")
        return

    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
        st.success(f"💰 **Ví Đầu tư Cổ đông:** Khả dụng **${st.session_state['wallet_balance']:,.2f}** | **Ưu đãi:** Giảm 4% khi mua tín chỉ các dự án bạn góp vốn.")
        
        st.markdown("### 📊 Danh mục Cổ phần Đã góp vốn của Bạn")
        current_user = st.session_state['current_user']
        investor_holdings = st.session_state.get("investor_portfolios", {}).get(current_user, [])
        if not investor_holdings:
            st.info("Bạn chưa góp vốn vào dự án rừng nào. Hãy chọn các dự án đang mở gọi vốn bên dưới.")
        else:
            st.dataframe(pd.DataFrame(investor_holdings), use_container_width=True, hide_index=True)
        st.divider()

    elif vai_tro == "Chủ rừng / Kỹ sư MRV":
        st.info("🌳 **Khu vực Chủ rừng:** Mở hạn mức gọi vốn cộng đồng để lấy nguồn lực chăm sóc rừng giai đoạn đầu.")
        with st.expander("📝 MỞ GỌI VỐN DỰ ÁN TRỒNG RỪNG MỚI", expanded=False):
            ten_du_an = st.text_input("Tên dự án trồng rừng mới:")
            muc_goi_von = st.number_input("Số vốn cần huy động từ Cổ đông (USD):", value=25000.0, step=5000)
            gia_du_kien = st.number_input("Giá dự kiến bán tín chỉ sau khai thác (USD):", value=12.0)
            file_minh_chung = st.file_uploader("📎 Tải lên Kế hoạch & Sổ đỏ dự án", type=['pdf', 'jpg'])
            
            if st.button("🚀 MỞ CỔNG GỌI VỐN CỘNG ĐỒNG", type="primary"):
                if not ten_du_an or file_minh_chung is None:
                    st.error("❌ Vui lòng nhập tên và tải minh chứng.")
                else:
                    new_proj = {
                        "id": f"user_p_{len(st.session_state['market_projects'])}",
                        "name": ten_du_an,
                        "owner": st.session_state['current_user'],
                        "price": gia_du_kien,
                        "volume": 5000, # Trữ lượng giả định khi cây trưởng thành
                        "duration": 5,
                        "funding_goal": muc_goi_von,
                        "funded_amount": 0.0,
                        "lat": 11.4280, 
                        "lon": 107.4286,
                        "verified": True,
                        "proof_file": file_minh_chung,
                        "proof_name": file_minh_chung.name,
                        "status": "Active"
                    }
                    st.session_state["market_projects"].append(new_proj)
                    st.success("✅ Thành công! Dự án đã chính thức lên sóng gọi vốn.")

    st.divider()
    st.markdown("### 🚀 Danh sách Dự án đang Gọi vốn Trồng rừng")
    
    # Chỉ hiển thị các dự án có cấu hình gọi vốn
    found_funding = False
    for p in st.session_state["market_projects"]:
        if "funding_goal" in p and p.get('status', 'Active') == 'Active':
            found_funding = True
            with st.container(border=True):
                col_i, col_a = st.columns([3, 2])
                with col_i:
                    st.markdown(f"#### 🌲 {p['name']}")
                    st.write(f"**Chủ đầu tư / Chủ rừng:** {p['owner']}")
                    progress = min(100, int((p['funded_amount'] / p['funding_goal']) * 100))
                    st.info(f"💵 **Tiến độ góp vốn:** ${p['funded_amount']:,.0f} /${p['funding_goal']:,.0f} ({progress}%)")
                    st.progress(progress)
                    st.write(f"🎁 **Quyền lợi Cổ đông:** Hưởng lợi nhuận chia sẻ & **Chiết khấu 4%** mua tín chỉ tương lai.")

                with col_a:
                    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
                        t_gop = st.number_input("Số vốn muốn góp (USD):", min_value=100, max_value=int(p['funding_goal'] - p['funded_amount']) if p['funded_amount'] < p['funding_goal'] else 1, value=1000, key=f"fund_input_{p['id']}")
                        
                        if p['funded_amount'] >= p['funding_goal']:
                            st.success("🎉 Dự án đã hoàn thành gọi vốn!")
                        else:
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
                                    st.success(f"🎉 Góp vốn thành công ${t_gop:,.2f}!")
                                    st.rerun()
                                else:
                                    st.error("❌ Ví không đủ tiền.")
                    else:
                        st.info("Đăng nhập tài khoản Cổ đông để góp vốn.")
    
    if not found_funding:
        st.info("Hiện chưa có dự án nào đang mở gọi vốn.")
