import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
from auth import load_users

def hien_thi_san_giao_dich():
    st.markdown(f"## 🏢 Trung tâm Giao dịch & Quản lý Tín chỉ (Xin chào: **{st.session_state['current_user']}** - Vai trò: *{st.session_state['current_role']}*)")
    vai_tro = st.session_state.get('current_role', '')
    
    # 1. KHU VỰC VÍ & TÀI SẢN THEO PHÂN QUYỀN
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

    elif vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
        st.info("🤝 **Khu vực Cổ đông & Nhà đầu tư Xanh:** Góp vốn vào các dự án trồng rừng mới, hưởng lợi nhuận và nhận chiết khấu 3-4% khi mua tín chỉ.")
        st.success(f"💰 **Ví Đầu tư:** Khả dụng **${st.session_state['wallet_balance']:,.2f}** | **Đặc quyền:** Giảm giá 4% toàn bộ các lô tín chỉ trên sàn.")
        
        st.markdown("### 📊 Danh mục Cổ phần Đã góp vốn")
        current_user = st.session_state['current_user']
        investor_holdings = st.session_state.get("investor_portfolios", {}).get(current_user, [])
        if not investor_holdings:
            st.write("Bạn chưa góp vốn vào dự án nào. Hãy xem danh sách gọi vốn bên dưới để đầu tư.")
        else:
            st.dataframe(pd.DataFrame(investor_holdings), use_container_width=True, hide_index=True)
        st.divider()
        
    elif vai_tro == "Chủ rừng / Kỹ sư MRV":
        st.info("🌳 **Khu vực Chủ rừng:** Nộp hồ sơ minh chứng gốc và mở hạn mức gọi vốn từ Cổ đông.")
        with st.expander("📝 TẠO HỒ SƠ NIÊM YẾT & KÊU GỌI VỐN TRỒNG RỪNG", expanded=False):
            ten_du_an = st.text_input("Tên dự án rừng mới:")
            kl_ban = st.number_input("Khối lượng tín chỉ dự kiến khai thác (tấn):", min_value=1000, step=1000)
            gia_ban = st.number_input("Giá bán mỗi tín chỉ (USD):", value=10.0)
            muc_goi_von = st.number_input("Số vốn cần huy động từ Cổ đông (USD):", value=20000.0, step=5000)
            cam_ket_nam = st.number_input("Thời hạn cam kết bảo vệ rừng (Năm):", min_value=1, max_value=30, value=5)
            file_minh_chung = st.file_uploader("📎 Tải lên Sổ đỏ / Giấy tờ pháp lý gốc", type=['pdf', 'jpg', 'png'])
            
            if st.button("🚀 GỬI HỒ SƠ & MỞ GỌI VỐN", type="primary"):
                if not ten_du_an or file_minh_chung is None:
                    st.error("❌ Vui lòng nhập tên dự án và tải lên minh chứng pháp lý gốc.")
                else:
                    new_proj = {
                        "id": f"user_p_{len(st.session_state['market_projects'])}",
                        "name": ten_du_an,
                        "owner": st.session_state['current_user'],
                        "price": gia_ban,
                        "volume": kl_ban,
                        "duration": cam_ket_nam,
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
                    st.success("✅ Thành công! Dự án đã mở cổng gọi vốn cộng đồng.")

    st.divider()

    # 2. THỐNG KÊ HỆ SINH THÁI
    st.markdown("### 📊 Thống kê Hệ sinh thái Thời gian thực")
    user_db = load_users()
    so_doanh_nghiep = sum(1 for u in user_db.values() if u["role"] == "Doanh nghiệp mua tín chỉ")
    so_chu_rung = sum(1 for u in user_db.values() if u["role"] == "Chủ rừng / Kỹ sư MRV")
    so_nha_dau_tu = sum(1 for u in user_db.values() if u["role"] == "Nhà đầu tư từ xa (Cổ đông)")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Doanh nghiệp Đăng ký", f"{so_doanh_nghiep} Tài khoản")
    m2.metric("Chủ rừng / Chuyên gia", f"{so_chu_rung} Tài khoản")
    m3.metric("Nhà đầu tư / Cổ đông", f"{so_nha_dau_tu} Tài khoản")
    m4.metric("Dự án hoạt động", f"{len(st.session_state['market_projects'])} Dự án")

    st.divider()
    
    # 3. DANH MỤC TRÊN SÀN (MUA BÁN & GÓP VỐN)
    st.markdown("### 🛒 Danh mục Dự án & Góp vốn Trồng rừng")
    
    for p in st.session_state["market_projects"]:
        with st.container(border=True):
            col_info, col_action = st.columns([3, 2])
            
            with col_info:
                st.markdown(f"#### 🌳 {p['name']}")
                st.write(f"**Chủ sở hữu:** {p['owner']} | **Trạng thái:** ✅ Đã xác thực Pháp lý")
                st.write(f"**Trữ lượng tín chỉ:** {int(p['volume']):,} tấn | **Giá gốc:** ${p['price']:,.2f} / tín chỉ")
                st.write(f"⏳ **Thời hạn cam kết:** {p['duration']} năm")
                
                # Hiển thị thông tin gọi vốn nếu dự án có cấu hình gọi vốn
                if "funding_goal" in p:
                    progress = min(100, int((p['funded_amount'] / p['funding_goal']) * 100))
                    st.info(f"🤝 **Gọi vốn trồng rừng:** ${p['funded_amount']:,.0f} /${p['funding_goal']:,.0f} ({progress}%)")
                    st.progress(progress)
                
                if st.button("📄 Xem Minh chứng Pháp lý Gốc", key=f"btn_proof_{p['id']}"):
                    st.session_state[f"show_proof_{p['id']}"] = not st.session_state.get(f"show_proof_{p['id']}", False)
                
                if st.session_state.get(f"show_proof_{p['id']}", False):
                    st.markdown(f"**Tệp minh chứng:** `{p.get('proof_name', 'Tiêu chuẩn quốc gia')}`")
                    if p.get('proof_file') is not None and hasattr(p['proof_file'], 'type'):
                        if p['proof_file'].type in ["image/jpeg", "image/png"]:
                            st.image(p['proof_file'], caption="Sổ đỏ gốc", use_container_width=True)

            with col_action:
                # TRƯỜNG HỢP 1: DÀNH CHO NHÀ ĐẦU TƯ GÓP VỐN
                if vai_tro == "Nhà đầu tư từ xa (Cổ đông)" and "funding_goal" in p:
                    T_gop = st.number_input("Số vốn muốn góp (USD):", min_value=100, max_value=int(p['funding_goal'] - p['funded_amount']), value=1000, key=f"inv_{p['id']}")
                    if st.button("🤝 Góp vốn nhận cổ phần", key=f"fund_btn_{p['id']}", type="primary", use_container_width=True):
                        if st.session_state["wallet_balance"] >= T_gop:
                            st.session_state["wallet_balance"] -= T_gop
                            p['funded_amount'] += T_gop
                            
                            cur_inv = st.session_state['current_user']
                            if "investor_portfolios" not in st.session_state:
                                st.session_state["investor_portfolios"] = {}
                            if cur_inv not in st.session_state["investor_portfolios"]:
                                st.session_state["investor_portfolios"][cur_inv] = []
                            
                            st.session_state["investor_portfolios"][cur_inv].append({
                                "Dự án": p['name'],
                                "Vốn góp": f"${T_gop:,.2f}",
                                "Quyền lợi": "Chia lợi nhuận + Giảm giá 4% mua tín chỉ"
                            })
                            st.success(f"🎉 Góp vốn thành công ${T_gop:,.2f}! Bạn đã trở thành cổ đông dự án.")
                            st.rerun()
                        else:
                            st.error("❌ Ví không đủ tiền.")

                # TRƯỜNG HỢP 2: DÀNH CHO DOANH NGHIỆP MUA TÍN CHỈ (ĐƯỢC ÁP DỤNG CHIẾT KHẤU 4% NẾU LÀ CỔ ĐÔNG)
                elif vai_tro == "Doanh nghiệp mua tín chỉ":
                    # Kiểm tra xem doanh nghiệp này có đồng thời là nhà đầu tư góp vốn cho dự án này không để áp dụng giảm giá 4%
                    is_shareholder = False
                    cur_user = st.session_state['current_user']
                    if cur_user in st.session_state.get("investor_portfolios", {}):
                        for inv in st.session_state["investor_portfolios"][cur_user]:
                            if inv["Dự án"] == p['name']:
                                is_shareholder = True
                                break
                    
                    hieu_luc_gia = p['price'] * 0.96 if is_shareholder else p['price']
                    if is_shareholder:
                        st.success("🌟 **Đặc quyền Cổ đông:** Được giảm giá 4% trực tiếp!")
                    
                    sl_mua = st.number_input("Số lượng mua (tấn):", min_value=1, max_value=int(p['volume']), value=10, key=f"buy_sl_{p['id']}")
                    tong_tien = sl_mua * hieu_luc_gia
                    st.info(f"Thanh toán: **${tong_tien:,.2f}**")
                    
                    if st.button("🛒 Mua tín chỉ", key=f"buy_btn_{p['id']}", type="primary", use_container_width=True):
                        if st.session_state["wallet_balance"] >= tong_tien:
                            st.session_state["wallet_balance"] -= tong_tien
                            p['volume'] -= sl_mua
                            
                            if cur_user not in st.session_state["user_portfolios"]:
                                st.session_state["user_portfolios"][cur_user] = []
                            
                            st.session_state["user_portfolios"][cur_user].append({
                                "project": p['name'],
                                "amount": sl_mua,
                                "expiry": f"Tháng 12/{2026 + p['duration']} (Cam kết {p['duration']} năm)"
                            })
                            st.success("🎉 Giao dịch thành công!")
                            st.rerun()
                        else:
                            st.error("❌ Ví không đủ tiền.")
                else:
                    st.button("🔒 Đăng nhập đúng tài khoản để tương tác", disabled=True, use_container_width=True)
