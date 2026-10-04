import streamlit as st
import pandas as pd
import numpy as np

def hien_thi_san_giao_dich():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    vai_tro = st.session_state.get('current_role', '')
    
    T = {
        "Tiếng Việt": {
            "title": "DASHBOARD QUẢN LÝ TÀI KHOẢN", "wrong_tab_inv": "Bạn đang sử dụng tài khoản Đầu tư. Vui lòng chuyển Tab 'Đầu tư Trồng rừng'.",
            "wallet": "Số Dư Ví Hệ Thống", "total_credits": "Tổng Tín Chỉ Sở Hữu", "esg_rating": "Hạng Tín Nhiệm (ESG)",
            "expander_inv": "XEM CHI TIẾT KHO TÍN CHỈ", "empty_inv": "Kho của bạn đang trống.", "area": "Diện Tích Sở Hữu",
            "sellable": "Khối Lượng Có Thể Bán", "revenue": "Doanh Thu Giao Dịch", "forest_hint": "Xác thực sinh khối và niêm yết lên sàn thương mại.",
            "list_new": "NIÊM YẾT LÔ TÍN CHỈ MỚI", "chart_title": "BIỂU ĐỒ GIÁ TÍN CHỈ GIAO NGAY", "market_title": "DANH MỤC TÍN CHỈ ĐANG CHÀO BÁN"
        },
        "English": {
            "title": "ACCOUNT MANAGEMENT DASHBOARD", "wrong_tab_inv": "Investor account detected. Please switch to 'Forest Investment' tab.",
            "wallet": "System Wallet Balance", "total_credits": "Total Credits Owned", "esg_rating": "ESG Rating",
            "expander_inv": "VIEW CREDIT INVENTORY", "empty_inv": "Your inventory is empty.", "area": "Owned Area",
            "sellable": "Sellable Volume", "revenue": "Trading Revenue", "forest_hint": "Verify biomass and list on commercial exchange.",
            "list_new": "LIST NEW CARBON CREDITS", "chart_title": "SPOT CREDIT PRICE CHART", "market_title": "CARBON CREDITS FOR SALE"
        }
    }
    t = T[lang]

    _, c_mid, _ = st.columns([0.05, 0.9, 0.05])
    with c_mid:
        st.markdown(f"<h3 style='color: white; font-weight: 800; text-align: center; margin-bottom: 25px; letter-spacing: 1px;'>{t['title']}</h3>", unsafe_allow_html=True)
        
        if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
            st.info(t["wrong_tab_inv"])
            return

        elif vai_tro == "Doanh nghiệp mua tín chỉ":
            with st.container(border=True):
                col1, col2, col3 = st.columns(3)
                user_holdings = st.session_state["user_portfolios"].get(st.session_state['current_user'], [])
                tong_tin_chi = sum(item.get("Số lượng", item.get("Amount", 0)) for item in user_holdings) if user_holdings else 0
                
                col1.metric(t["wallet"], f"${st.session_state['wallet_balance']:,.2f}", "+ 50,000.00")
                col2.metric(t["total_credits"], f"{tong_tin_chi:,} " + ("Tấn" if lang=="Tiếng Việt" else "Tons"), "Đã bù trừ" if lang=="Tiếng Việt" else "Offset")
                col3.metric(t["esg_rating"], "Hạng A+" if lang=="Tiếng Việt" else "Grade A+", "Đạt chuẩn" if lang=="Tiếng Việt" else "Compliant")
            
            with st.expander(t["expander_inv"], expanded=False):
                if not user_holdings: st.warning(t["empty_inv"])
                else: st.dataframe(pd.DataFrame(user_holdings), use_container_width=True, hide_index=True)

        elif vai_tro == "Chủ rừng / Kỹ sư MRV":
            with st.container(border=True):
                col1, col2, col3 = st.columns(3)
                col1.metric(t["area"], "1,500 Ha", "Đã xác thực" if lang=="Tiếng Việt" else "Verified")
                col2.metric(t["sellable"], "550,000 " + ("Tấn" if lang=="Tiếng Việt" else "Tons"), "Sinh khối" if lang=="Tiếng Việt" else "Biomass")
                col3.metric(t["revenue"], "$0.00", "Chờ khớp lệnh" if lang=="Tiếng Việt" else "Pending")
            
            st.markdown(f"<p style='text-align:center; color:#a0aec0;'>{t['forest_hint']}</p>", unsafe_allow_html=True)
            with st.expander(t["list_new"], expanded=True):
                with st.form("form_niem_yet", clear_on_submit=True):
                    ten_du_an = st.text_input("Tên dự án / Khu rừng:" if lang=="Tiếng Việt" else "Project Name:")
                    col_kl, col_gia, col_nam = st.columns(3)
                    with col_kl: kl_ban = st.number_input("Khối lượng:" if lang=="Tiếng Việt" else "Volume:", min_value=100, step=100, value=1000)
                    with col_gia: gia_ban = st.number_input("Giá (USD):" if lang=="Tiếng Việt" else "Price (USD):", value=10.5, step=0.5)
                    with col_nam: cam_ket_nam = st.number_input("Cam kết (Năm):" if lang=="Tiếng Việt" else "Commitment:", min_value=1, max_value=30, value=5)
                    
                    file_minh_chung = st.file_uploader("Tải lên Minh chứng Pháp lý" if lang=="Tiếng Việt" else "Upload Legal Proof", type=['pdf', 'jpg', 'png'])
                    submitted_ny = st.form_submit_button("CHUYỂN DỮ LIỆU LÊN SÀN" if lang=="Tiếng Việt" else "SUBMIT TO EXCHANGE", type="primary", use_container_width=True)
                    
                    if submitted_ny:
                        if ten_du_an and file_minh_chung:
                            st.session_state["market_projects"].append({
                                "id": f"user_p_{len(st.session_state['market_projects'])}", "name": ten_du_an, 
                                "owner": st.session_state['current_user'], "price": gia_ban, "volume": kl_ban, 
                                "duration": cam_ket_nam, "proof_name": file_minh_chung.name, "status": "Active"
                            })
                            st.success("Niêm yết thành công!" if lang=="Tiếng Việt" else "Successfully listed!")
                        else: st.error("Vui lòng nhập đủ thông tin." if lang=="Tiếng Việt" else "Fill all fields.")

        st.divider()
        st.markdown(f"<h4 style='color: white; text-align: center;'>{t['chart_title']}</h4>", unsafe_allow_html=True)
        with st.container(border=True):
            np.random.seed(42)
            dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
            prices = np.random.normal(loc=10.5, scale=0.4, size=30) + np.linspace(0, 1.5, 30)
            col_name = 'Giá Khớp Lệnh ($/tấn)' if lang == "Tiếng Việt" else 'Clearing Price ($/ton)'
            st.line_chart(pd.DataFrame({col_name: prices}, index=dates), color="#48bb78", height=250)

        st.markdown(f"<h4 style='color: white; text-align: center; margin-top:20px;'>{t['market_title']}</h4>", unsafe_allow_html=True)
        for p in st.session_state["market_projects"]:
            if p.get('volume', 0) > 0 and p.get('status') == 'Active':
                with st.container(border=True):
                    col_info, col_action = st.columns([3, 2])
                    with col_info:
                        st.markdown(f"<h4 style='color:#48bb78; margin:0;'>{p['name']}</h4>", unsafe_allow_html=True)
                        if lang == "Tiếng Việt":
                            st.write(f"**Chủ rừng:** {p['owner']} | **Trạng thái:** Đã kiểm định AI")
                            st.write(f"**Trữ lượng:** {int(p['volume']):,} tấn | **Giá bán:** ${p['price']:,.2f} / tín chỉ")
                        else:
                            st.write(f"**Owner:** {p['owner']} | **Status:** AI Verified")
                            st.write(f"**Volume:** {int(p['volume']):,} tons | **Price:** ${p['price']:,.2f} / credit")
                    with col_action:
                        if vai_tro == "Doanh nghiệp mua tín chỉ":
                            with st.form(f"buy_form_{p['id']}", clear_on_submit=True):
                                sl_mua = st.number_input("Khối lượng mua / Volume:" , min_value=1, max_value=int(p['volume']), value=100)
                                if st.form_submit_button(f"ĐẶT LỆNH (${sl_mua * p['price']:,.2f})", type="primary", use_container_width=True):
                                    tong_tien = sl_mua * p['price']
                                    if st.session_state["wallet_balance"] >= tong_tien:
                                        st.session_state["wallet_balance"] -= tong_tien
                                        p['volume'] -= sl_mua
                                        cur_user = st.session_state['current_user']
                                        if cur_user not in st.session_state["user_portfolios"]: st.session_state["user_portfolios"][cur_user] = []
                                        st.session_state["user_portfolios"][cur_user].append({"Dự án" if lang=="Tiếng Việt" else "Project": p['name'], "Số lượng" if lang=="Tiếng Việt" else "Amount": sl_mua})
                                        st.success("Khớp lệnh thành công!" if lang=="Tiếng Việt" else "Order matched!")
                                        st.rerun()
                                    else: st.error("Số dư không đủ." if lang=="Tiếng Việt" else "Insufficient balance.")
                        else:
                            st.button("ĐĂNG NHẬP TÀI KHOẢN MUA" if lang=="Tiếng Việt" else "LOGIN BUYER ACCOUNT", key=f"lock_{p['id']}", disabled=True, use_container_width=True)

def hien_thi_cong_dau_tu():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    _, c_mid, _ = st.columns([0.1, 0.8, 0.1])
    with c_mid:
        st.markdown("<h3 style='color: white; text-align: center; font-weight:800; letter-spacing:1px;'>QUỸ ĐẦU TƯ TRỒNG RỪNG</h3>" if lang == "Tiếng Việt" else "<h3 style='color: white; text-align: center; font-weight:800; letter-spacing:1px;'>FOREST INVESTMENT FUND</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #a0aec0;'>Tài khoản: <b>{st.session_state['current_user']}</b> | Khả dụng: <b>${st.session_state['wallet_balance']:,.2f}</b></p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(f"<h4 style='color:#48bb78; text-align:center;'>{'DANH MỤC ĐẦU TƯ CỦA BẠN' if lang == 'Tiếng Việt' else 'YOUR PORTFOLIO'}</h4>", unsafe_allow_html=True)
            inv_hold = st.session_state.get("investor_portfolios", {}).get(st.session_state['current_user'], [])
            if not inv_hold: st.info("Danh mục trống." if lang == "Tiếng Việt" else "Empty portfolio.")
            else: st.dataframe(pd.DataFrame(inv_hold), use_container_width=True, hide_index=True)

        st.markdown(f"<h4 style='color: white; text-align: center; margin-top:20px;'>{'DỰ ÁN ĐANG KÊU GỌI VỐN' if lang == 'Tiếng Việt' else 'FUNDING PROJECTS'}</h4>", unsafe_allow_html=True)
        for p in st.session_state["market_projects"]:
            if "funding_goal" in p and p.get('status') == 'Active':
                with st.container(border=True):
                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.markdown(f"<h4 style='color:#63b3ed; margin:0;'>{p['name']}</h4>", unsafe_allow_html=True)
                        st.write(f"**Chủ dự án / Owner:** {p['owner']}")
                        prog = min(100, int((p['funded_amount'] / p['funding_goal']) * 100))
                        st.write(f"**Tiến độ / Progress:** ${p['funded_amount']:,.0f} / ${p['funding_goal']:,.0f} ({prog}%)")
                        st.progress(prog)
                    with c2:
                        with st.form(f"fund_f_{p['id']}", clear_on_submit=True):
                            max_f = int(p['funding_goal'] - p['funded_amount'])
                            t_gop = st.number_input("Số vốn góp / Amount:" , min_value=100, max_value=max_f if max_f > 0 else 1, value=min(1000, max_f))
                            if st.form_submit_button("XÁC NHẬN ĐẦU TƯ / INVEST", type="primary", use_container_width=True):
                                if max_f <= 0: st.warning("Đã đủ vốn / Fully funded.")
                                elif st.session_state["wallet_balance"] >= t_gop:
                                    st.session_state["wallet_balance"] -= t_gop
                                    p['funded_amount'] += t_gop
                                    u = st.session_state['current_user']
                                    if u not in st.session_state["investor_portfolios"]: st.session_state["investor_portfolios"][u] = []
                                    st.session_state["investor_portfolios"][u].append({"Dự án / Project": p['name'], "Vốn góp / Amount": f"${t_gop:,.2f}"})
                                    st.rerun()
                                else: st.error("Ví không đủ tiền / Insufficient funds.")

def hien_thi_gioi_thieu_va_goi_von():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    
    st.markdown("""
    <style>
    @keyframes titleShine {
        to { background-position: 200% center; }
    }
    .about-title {
        font-size: 2.2rem; font-weight: 900; text-align: center; text-transform: uppercase;
        background: linear-gradient(to right, #48bb78, #63b3ed, #48bb78);
        background-size: 200% auto; color: #fff; background-clip: text;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: titleShine 4s linear infinite; margin-bottom: 30px; letter-spacing: 2px;
    }
    .cert-col { text-align: center; padding: 15px; border-right: 1px solid rgba(255,255,255,0.1); }
    .cert-col:last-child { border-right: none; }
    .cert-title { color: #a0aec0; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 10px; font-weight: 600;}
    .cert-val { color: #ffffff; font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }
    .cert-status { color: #48bb78; font-size: 0.85rem; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

    _, c_mid, _ = st.columns([0.05, 0.9, 0.05])
    with c_mid:
        if lang == "Tiếng Việt":
            st.markdown('<div class="about-title">VỀ CHÚNG TÔI & TẦM NHÌN TƯƠNG LAI</div>', unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("<p style='text-align:center; font-size:1.1rem; color:#e2e8f0; line-height:1.6;'>Thay mặt Đội ngũ Sáng lập, chúng tôi xin gửi <b>LỜI CẢM ƠN CHÂN THÀNH NHẤT</b> đến Quý Chủ rừng, Doanh nghiệp và Nhà đầu tư tiên phong...<br><br><span style='color:#48bb78; font-weight:bold;'>SỨ MỆNH:</span> Tích hợp trí tuệ nhân tạo (GEE) với Sổ đỏ để loại bỏ 'rừng ma', đưa doanh nghiệp và chủ rừng đến gần nhau với độ tin cậy tuyệt đối.</p>", unsafe_allow_html=True)
            
            st.markdown("<h4 style='text-align:center; color:white; margin-top:30px; margin-bottom:20px;'>CHỨNG NHẬN UY TÍN & ĐỐI TÁC</h4>", unsafe_allow_html=True)
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown('<div class="cert-col"><div class="cert-title">Tiêu chuẩn</div><div class="cert-val">VCS & Gold Standard</div><div class="cert-status">Đạt chuẩn toàn cầu</div></div>', unsafe_allow_html=True)
                c2.markdown('<div class="cert-col"><div class="cert-title">Công nghệ</div><div class="cert-val">ESA WorldCover & GEE</div><div class="cert-status">Real-time AI</div></div>', unsafe_allow_html=True)
                c3.markdown('<div class="cert-col"><div class="cert-title">Pháp lý</div><div class="cert-val">Sổ đỏ Lâm nghiệp Gốc</div><div class="cert-status">Xác thực chéo 100%</div></div>', unsafe_allow_html=True)
                c4.markdown('<div class="cert-col"><div class="cert-title">Kiểm toán</div><div class="cert-val">Smart Contract Escrow</div><div class="cert-status">Minh bạch tuyệt đối</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="about-title">ABOUT US & FUTURE VISION</div>', unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("<p style='text-align:center; font-size:1.1rem; color:#e2e8f0; line-height:1.6;'>On behalf of the Founding Team, we send our <b>DEEPEST GRATITUDE</b> to the Forest Owners, Businesses, and pioneering Investors...<br><br><span style='color:#48bb78; font-weight:bold;'>MISSION:</span> Integrating AI (GEE) with Land Rights Certificates to eliminate 'ghost forests', bringing businesses and forest owners together with absolute trust.</p>", unsafe_allow_html=True)
            
            st.markdown("<h4 style='text-align:center; color:white; margin-top:30px; margin-bottom:20px;'>PRESTIGIOUS CERTIFICATIONS & PARTNERS</h4>", unsafe_allow_html=True)
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown('<div class="cert-col"><div class="cert-title">Standard</div><div class="cert-val">VCS & Gold Standard</div><div class="cert-status">Global Standard</div></div>', unsafe_allow_html=True)
                c2.markdown('<div class="cert-col"><div class="cert-title">Technology</div><div class="cert-val">ESA WorldCover & GEE</div><div class="cert-status">Real-time AI</div></div>', unsafe_allow_html=True)
                c3.markdown('<div class="cert-col"><div class="cert-title">Legal</div><div class="cert-val">Original Land Rights</div><div class="cert-status">100% Cross-verified</div></div>', unsafe_allow_html=True)
                c4.markdown('<div class="cert-col"><div class="cert-title">Audit</div><div class="cert-val">Smart Contract Escrow</div><div class="cert-status">Absolute Transparency</div></div>', unsafe_allow_html=True)
