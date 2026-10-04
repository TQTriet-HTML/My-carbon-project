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
            "sellable": "Khối Lượng Có Thể Bán", "revenue": "Doanh Thu Giao Dịch", "forest_hint": "Xác thực sinh khối và niêm yết tín chỉ lên sàn thương mại.",
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
                    
                    file_minh_chung = st.file_uploader("Tải lên Sổ đỏ / Quyền sử dụng đất" if lang=="Tiếng Việt" else "Upload Legal Proof", type=['pdf', 'jpg', 'png'])
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
                            st.write(f"**Chủ dự án / Owner:** {p['owner']}")
                            st.write(f"**Khối lượng:** {int(p['volume']):,} tấn | **Giá chốt:** ${p['price']:,.2f} / tín chỉ")
                        else:
                            st.write(f"**Owner:** {p['owner']}")
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
            st.markdown(f"<h4 style='color:#48bb78; text-align:center;'>{'DANH MỤC CỔ PHẦN ĐÃ GÓP VỐN' if lang == 'Tiếng Việt' else 'YOUR PORTFOLIO'}</h4>", unsafe_allow_html=True)
            inv_hold = st.session_state.get("investor_portfolios", {}).get(st.session_state['current_user'], [])
            if not inv_hold: st.info("Bạn chưa góp vốn vào dự án nào." if lang == "Tiếng Việt" else "Empty portfolio.")
            else: st.dataframe(pd.DataFrame(inv_hold), use_container_width=True, hide_index=True)

        st.markdown(f"<h4 style='color: white; text-align: center; margin-top:20px;'>{'DANH SÁCH DỰ ÁN ĐANG KÊU GỌI VỐN' if lang == 'Tiếng Việt' else 'FUNDING PROJECTS'}</h4>", unsafe_allow_html=True)
        for p in st.session_state["market_projects"]:
            if "funding_goal" in p and p.get('status') == 'Active':
                with st.container(border=True):
                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.markdown(f"<h4 style='color:#63b3ed; margin:0;'>{p['name']}</h4>", unsafe_allow_html=True)
                        st.write(f"**Chủ dự án / Owner:** {p['owner']}")
                        prog = min(100, int((p['funded_amount'] / p['funding_goal']) * 100))
                        st.write(f"**Tiến độ góp vốn:** ${p['funded_amount']:,.0f} / ${p['funding_goal']:,.0f} ({prog}%)")
                        st.progress(prog)
                    with c2:
                        with st.form(f"fund_f_{p['id']}", clear_on_submit=True):
                            max_f = int(p['funding_goal'] - p['funded_amount'])
                            t_gop = st.number_input("Số vốn góp / Amount:" , min_value=100, max_value=max_f if max_f > 0 else 1, value=min(1000, max_f))
                            if st.form_submit_button("ĐẦU TƯ / INVEST", type="primary", use_container_width=True):
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
    .cert-col { text-align: center; padding: 10px; }
    .cert-title { color: #a0aec0; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 15px; font-weight: 700;}
    .cert-val { color: #ffffff; font-size: 1.15rem; font-weight: 800; margin-bottom: 10px; }
    .cert-status { color: #48bb78; font-size: 0.9rem; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

    T = {
        "Tiếng Việt": {
            "title": "VỀ CHÚNG TÔI & TẦM NHÌN TƯƠNG LAI",
            "thank_you": "Cảm ơn quý vị vì đã tin tưởng, đồng hành và cùng phát triển với nền tảng. Thay mặt đội ngũ phát triển xin gửi lời cảm ơn chân thành từ tận đáy lòng đến tất cả người đồng hành xanh trên nền tảng của chúng tôi!",
            "mission": "Tích hợp trí tuệ nhân tạo (GEE) với Sổ đỏ để loại bỏ 'rừng ma', đưa doanh nghiệp và chủ rừng đến gần nhau với độ tin cậy tuyệt đối.",
            "slogan_block": "Vì một ngày mai tươi sáng và thế giới xanh bền vững",
            "cert_title": "CHỨNG NHẬN UY TÍN & ĐỐI TÁC",
            "c1_t": "Tiêu chuẩn", "c1_v": "VCS & Gold Standard", "c1_s": "Đạt chuẩn toàn cầu",
            "c2_t": "Công nghệ", "c2_v": "ESA WorldCover & GEE", "c2_s": "Real-time AI",
            "c3_t": "Pháp lý", "c3_v": "Sổ đỏ Lâm nghiệp Gốc", "c3_s": "Xác thực chéo 100%",
            "c4_t": "Kiểm toán", "c4_v": "Smart Contract Escrow", "c4_s": "Minh bạch tuyệt đối"
        },
        "English": {
            "title": "ABOUT US & FUTURE VISION",
            "thank_you": "Thank you for trusting, accompanying, and growing with our platform. On behalf of the development team, we send our deepest and most sincere gratitude to all our green companions!",
            "mission": "Integrating AI (GEE) with Land Rights Certificates to eliminate 'ghost forests', bringing businesses and forest owners together with absolute trust.",
            "slogan_block": "For a brighter tomorrow and a sustainable green world",
            "cert_title": "PRESTIGIOUS CERTIFICATIONS & PARTNERS",
            "c1_t": "Standard", "c1_v": "VCS & Gold Standard", "c1_s": "Global Standard",
            "c2_t": "Technology", "c2_v": "ESA WorldCover & GEE", "c2_s": "Real-time AI",
            "c3_t": "Legal", "c3_v": "Original Land Rights", "c3_s": "100% Cross-verified",
            "c4_t": "Audit", "c4_v": "Smart Contract Escrow", "c4_s": "Absolute Transparency"
        }
    }
    t = T[lang]

    _, c_mid, _ = st.columns([0.05, 0.9, 0.05])
    with c_mid:
        st.markdown(f'<div class="about-title">{t["title"]}</div>', unsafe_allow_html=True)
        
        # Tất cả các khối dưới đây đều sử dụng st.container(border=True) để tự động nhận hoạt họa lóa sáng và lướt sáng xanh lá chuẩn MRV
        with st.container(border=True):
            st.markdown(f"<p style='text-align:center; font-size:1.1rem; color:#e2e8f0; line-height:1.7;'>{t['thank_you']}<br><br><span style='color:#48bb78; font-weight:800; font-size: 1.15rem;'>{'SỨ MỆNH' if lang=='Tiếng Việt' else 'MISSION'}:</span> {t['mission']}</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(f"<h4 style='text-align:center; color:#48bb78; font-weight:900; letter-spacing:1px; margin: 10px 0;'>{t['slogan_block']}</h4>", unsafe_allow_html=True)
        
        st.markdown(f"<h4 style='text-align:center; color:white; margin-top:40px; margin-bottom:25px;'>{t['cert_title']}</h4>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            with st.container(border=True):
                st.markdown(f'<div class="cert-col"><div class="cert-title">{t["c1_t"]}</div><div class="cert-val">{t["c1_v"]}</div><div class="cert-status">{t["c1_s"]}</div></div>', unsafe_allow_html=True)
        with c2:
            with st.container(border=True):
                st.markdown(f'<div class="cert-col"><div class="cert-title">{t["c2_t"]}</div><div class="cert-val">{t["c2_v"]}</div><div class="cert-status">{t["c2_s"]}</div></div>', unsafe_allow_html=True)
        with c3:
            with st.container(border=True):
                st.markdown(f'<div class="cert-col"><div class="cert-title">{t["c3_t"]}</div><div class="cert-val">{t["c3_v"]}</div><div class="cert-status">{t["c3_s"]}</div></div>', unsafe_allow_html=True)
        with c4:
            with st.container(border=True):
                st.markdown(f'<div class="cert-col"><div class="cert-title">{t["c4_t"]}</div><div class="cert-val">{t["c4_v"]}</div><div class="cert-status">{t["c4_s"]}</div></div>', unsafe_allow_html=True)
