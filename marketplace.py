import streamlit as st
import pandas as pd
import numpy as np

def hien_thi_san_giao_dich():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    vai_tro = st.session_state.get('current_role', '')
    
    # --- TỪ ĐIỂN SÀN GIAO DỊCH ---
    T = {
        "Tiếng Việt": {
            "title": "## 🏢 Dashboard Quản Lý Tài Khoản",
            "wrong_tab_inv": "💡 Bạn đang sử dụng tài khoản Cổ đông/Nhà đầu tư. Nơi giao dịch tín chỉ giao ngay dành cho doanh nghiệp. Vui lòng chuyển sang Tab **'Đầu tư Trồng rừng'** để quản lý danh mục góp vốn.",
            "wallet": "💳 Số Dư Ví Của Bạn",
            "total_credits": "📦 Tổng Tín Chỉ Sở Hữu",
            "esg_rating": "📈 Hạng Tín Nhiệm (ESG)",
            "expander_inv": "💼 XEM CHI TIẾT KHO TÍN CHỈ CỦA BẠN",
            "empty_inv": "Kho của bạn đang trống. Hãy mua tín chỉ để bù đắp phát thải.",
            "area": "🌳 Diện Tích Sở Hữu",
            "sellable": "📦 Khối Lượng Có Thể Bán",
            "revenue": "💳 Doanh Thu Giao Dịch",
            "forest_hint": "💡 **Khu vực Chủ rừng:** Xác thực sinh khối và niêm yết tín chỉ lên sàn thương mại.",
            "list_new": "📝 NIÊM YẾT LÔ TÍN CHỈ MỚI",
            "chart_title": "### 📈 Biểu đồ Giá Tín chỉ Giao ngay (30 Ngày)",
            "market_title": "### 🛒 Danh mục Tín chỉ Đang Chào Bán"
        },
        "English": {
            "title": "## 🏢 Account Management Dashboard",
            "wrong_tab_inv": "💡 You are using an Investor account. This spot market is for corporate buyers. Please switch to the **'Forest Investment'** tab to manage your portfolio.",
            "wallet": "💳 Your Wallet Balance",
            "total_credits": "📦 Total Credits Owned",
            "esg_rating": "📈 ESG Rating",
            "expander_inv": "💼 VIEW YOUR CREDIT INVENTORY",
            "empty_inv": "Your inventory is empty. Buy credits to offset emissions.",
            "area": "🌳 Owned Area",
            "sellable": "📦 Sellable Volume",
            "revenue": "💳 Trading Revenue",
            "forest_hint": "💡 **Forest Owner Area:** Verify biomass and list credits on the commercial exchange.",
            "list_new": "📝 LIST NEW CARBON CREDITS",
            "chart_title": "### 📈 Spot Credit Price Chart (30 Days)",
            "market_title": "### 🛒 Carbon Credits for Sale"
        }
    }
    t = T[lang]

    st.markdown(t["title"])
    
    if vai_tro == "Nhà đầu tư từ xa (Cổ đông)":
        st.info(t["wrong_tab_inv"])
        return

    elif vai_tro == "Doanh nghiệp mua tín chỉ":
        col1, col2, col3 = st.columns(3)
        user_holdings = st.session_state["user_portfolios"].get(st.session_state['current_user'], [])
        tong_tin_chi = sum(item.get("Số lượng", item.get("Amount", 0)) for item in user_holdings) if user_holdings else 0
        
        col1.metric(t["wallet"], f"${st.session_state['wallet_balance']:,.2f}", "+ 50,000.00")
        col2.metric(t["total_credits"], f"{tong_tin_chi:,} " + ("Tấn" if lang=="Tiếng Việt" else "Tons"), "Đã bù trừ Carbon" if lang=="Tiếng Việt" else "Carbon Offset")
        col3.metric(t["esg_rating"], "Hạng A+" if lang=="Tiếng Việt" else "Grade A+", "Đạt chuẩn Net-Zero" if lang=="Tiếng Việt" else "Net-Zero Compliant")
        
        with st.expander(t["expander_inv"], expanded=False):
            if not user_holdings:
                st.warning(t["empty_inv"])
            else:
                st.dataframe(pd.DataFrame(user_holdings), use_container_width=True, hide_index=True)
        st.divider()

    elif vai_tro == "Chủ rừng / Kỹ sư MRV":
        col1, col2, col3 = st.columns(3)
        col1.metric(t["area"], "1,500 Ha", "Đã xác thực" if lang=="Tiếng Việt" else "Verified")
        col2.metric(t["sellable"], "550,000 " + ("Tấn" if lang=="Tiếng Việt" else "Tons"), "Sinh khối" if lang=="Tiếng Việt" else "Biomass")
        col3.metric(t["revenue"], "$0.00", "Chờ khớp lệnh" if lang=="Tiếng Việt" else "Pending")
        
        st.info(t["forest_hint"])
        with st.expander(t["list_new"], expanded=True):
            with st.form("form_niem_yet", clear_on_submit=True):
                ten_du_an = st.text_input("Tên dự án / Khu rừng niêm yết:" if lang=="Tiếng Việt" else "Project / Forest Name:")
                col_kl, col_gia, col_nam = st.columns(3)
                with col_kl: kl_ban = st.number_input("Khối lượng (tấn):" if lang=="Tiếng Việt" else "Volume (Tons):", min_value=100, step=100, value=1000)
                with col_gia: gia_ban = st.number_input("Giá chốt (USD):" if lang=="Tiếng Việt" else "Price (USD):", value=10.5, step=0.5)
                with col_nam: cam_ket_nam = st.number_input("Cam kết (Năm):" if lang=="Tiếng Việt" else "Commitment (Years):", min_value=1, max_value=30, value=5)
                
                file_minh_chung = st.file_uploader("📎 Tải lên Sổ đỏ / Quyền sử dụng đất" if lang=="Tiếng Việt" else "📎 Upload Land Rights Certificate", type=['pdf', 'jpg', 'png'])
                submitted_ny = st.form_submit_button("🚀 CHUYỂN DỮ LIỆU LÊN SÀN" if lang=="Tiếng Việt" else "🚀 SUBMIT TO EXCHANGE", type="primary", use_container_width=True)
                
                if submitted_ny:
                    if not ten_du_an or file_minh_chung is None:
                        st.error("❌ Vui lòng nhập đầy đủ thông tin." if lang=="Tiếng Việt" else "❌ Please fill all fields.")
                    else:
                        new_proj = {
                            "id": f"user_p_{len(st.session_state['market_projects'])}", "name": ten_du_an, 
                            "owner": st.session_state['current_user'], "price": gia_ban, "volume": kl_ban, 
                            "duration": cam_ket_nam, "lat": 14.0, "lon": 108.0, "verified": True,
                            "proof_name": file_minh_chung.name, "status": "Active"
                        }
                        st.session_state["market_projects"].append(new_proj)
                        st.success("✅ Thành công!" if lang=="Tiếng Việt" else "✅ Success! Listed on exchange.")
        st.divider()

    st.markdown(t["chart_title"])
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
    prices = np.random.normal(loc=10.5, scale=0.4, size=30) + np.linspace(0, 1.5, 30)
    col_name = 'Giá Khớp Lệnh ($/tấn)' if lang == "Tiếng Việt" else 'Clearing Price ($/ton)'
    st.line_chart(pd.DataFrame({col_name: prices}, index=dates), color="#48bb78", height=250)

    st.markdown(t["market_title"])
    for p in st.session_state["market_projects"]:
        if p.get('volume', 0) > 0 and p.get('status') == 'Active':
            with st.container(border=True):
                col_info, col_action = st.columns([3, 2])
                with col_info:
                    st.markdown(f"#### 🌳 {p['name']}")
                    if lang == "Tiếng Việt":
                        st.write(f"**Chủ rừng:** {p['owner']} | **Tình trạng:** ✅ Đã kiểm định AI")
                        st.write(f"**Trữ lượng:** {int(p['volume']):,} tấn | **Giá bán:** **${p['price']:,.2f}** / tín chỉ")
                        btn_proof = "📄 Xem Minh chứng Pháp lý"
                    else:
                        st.write(f"**Owner:** {p['owner']} | **Status:** ✅ AI Verified")
                        st.write(f"**Volume:** {int(p['volume']):,} tons | **Price:** **${p['price']:,.2f}** / credit")
                        btn_proof = "📄 View Legal Proof"

                    if st.button(btn_proof, key=f"btn_proof_{p['id']}"):
                        st.info(f"Verified file: `{p.get('proof_name', 'Verified_Doc.pdf')}`." if lang == "English" else f"Đã xác minh tệp: `{p.get('proof_name', 'Ho_so.pdf')}`.")

                with col_action:
                    if vai_tro == "Doanh nghiệp mua tín chỉ":
                        with st.form(f"buy_form_{p['id']}", clear_on_submit=True):
                            sl_mua = st.number_input("Khối lượng mua:" if lang=="Tiếng Việt" else "Volume to buy:", min_value=1, max_value=int(p['volume']), value=100)
                            btn_buy = st.form_submit_button(f"🛒 Đặt Lệnh (${sl_mua * p['price']:,.2f})" if lang=="Tiếng Việt" else f"🛒 Buy Now (${sl_mua * p['price']:,.2f})", type="primary", use_container_width=True)
                            
                            if btn_buy:
                                tong_tien = sl_mua * p['price']
                                if st.session_state["wallet_balance"] >= tong_tien:
                                    st.session_state["wallet_balance"] -= tong_tien
                                    p['volume'] -= sl_mua
                                    cur_user = st.session_state['current_user']
                                    if cur_user not in st.session_state["user_portfolios"]: st.session_state["user_portfolios"][cur_user] = []
                                    key_proj = "Dự án" if lang=="Tiếng Việt" else "Project"
                                    key_amt = "Số lượng" if lang=="Tiếng Việt" else "Amount"
                                    st.session_state["user_portfolios"][cur_user].append({key_proj: p['name'], key_amt: sl_mua})
                                    st.success("Thành công!" if lang=="Tiếng Việt" else "Success!")
                                    st.rerun()
                                else:
                                    st.error("Số dư không đủ." if lang=="Tiếng Việt" else "Insufficient balance.")
                    else:
                        st.button("🔒 Đăng nhập tài khoản Mua để giao dịch" if lang=="Tiếng Việt" else "🔒 Login with Buyer Account to trade", key=f"lock_{p['id']}", disabled=True, use_container_width=True)

def hien_thi_cong_dau_tu():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    vai_tro = st.session_state.get('current_role', '')
    
    title = "## 🤝 Quỹ Đầu tư & Góp vốn Trồng rừng" if lang == "Tiếng Việt" else "## 🤝 Forest Investment & Funding"
    welcome = f"Xin chào: **{st.session_state['current_user']}** | Số dư đầu tư: **${st.session_state['wallet_balance']:,.2f}**" if lang == "Tiếng Việt" else f"Welcome: **{st.session_state['current_user']}** | Investment Balance: **${st.session_state['wallet_balance']:,.2f}**"
    
    st.markdown(title)
    st.caption(welcome)

    if vai_tro == "Doanh nghiệp mua tín chỉ":
        if lang == "Tiếng Việt":
            st.markdown("""<div style="background: linear-gradient(90deg, #1a202c 0%, #2c5282 100%); padding: 20px; border-radius: 8px; border-left: 5px solid #63b3ed; margin-bottom: 25px;"><h4 style="color:#ffffff; margin-top:0;">Đầu tư sinh lời & Hưởng đặc quyền chiết khấu</h4><p style="color:#e2e8f0; font-size:1rem; margin-bottom:0;">Với tư cách là Doanh nghiệp, việc rót vốn sớm vào các dự án trồng rừng mang lại <b>lợi nhuận ROI</b> và <b>chiết khấu mua tín chỉ sâu</b> trong tương lai.</p></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background: linear-gradient(90deg, #1a202c 0%, #2c5282 100%); padding: 20px; border-radius: 8px; border-left: 5px solid #63b3ed; margin-bottom: 25px;"><h4 style="color:#ffffff; margin-top:0;">Profitable Investment & Discount Privileges</h4><p style="color:#e2e8f0; font-size:1rem; margin-bottom:0;">As a Business, early funding in forest projects brings <b>ROI</b> and guarantees <b>deeply discounted carbon credits</b> in the future.</p></div>""", unsafe_allow_html=True)
    elif vai_tro == "Chủ rừng / Kỹ sư MRV":
        if lang == "Tiếng Việt":
            st.markdown("""<div style="background: linear-gradient(90deg, #1a202c 0%, #276749 100%); padding: 20px; border-radius: 8px; border-left: 5px solid #48bb78; margin-bottom: 25px;"><h4 style="color:#ffffff; margin-top:0;">Gia tăng thu nhập & Mở rộng thị trường</h4><p style="color:#e2e8f0; font-size:1rem; margin-bottom:0;">Đầu tư chéo giúp <b>đa dạng hóa nguồn thu nhập</b> và <b>mở rộng quy mô thị trường</b> khai thác tín chỉ carbon liên kết.</p></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background: linear-gradient(90deg, #1a202c 0%, #276749 100%); padding: 20px; border-radius: 8px; border-left: 5px solid #48bb78; margin-bottom: 25px;"><h4 style="color:#ffffff; margin-top:0;">Increase Income & Expand Market</h4><p style="color:#e2e8f0; font-size:1rem; margin-bottom:0;">Cross-investing helps <b>diversify income sources</b> and <b>expand the market scale</b> of joint carbon credit exploitation.</p></div>""", unsafe_allow_html=True)
    else: 
        if lang == "Tiếng Việt":
            st.markdown("""<div style="background: linear-gradient(90deg, #1a202c 0%, #742a2a 100%); padding: 20px; border-radius: 8px; border-left: 5px solid #f6ad55; margin-bottom: 25px;"><h4 style="color:#ffffff; margin-top:0;">Bắt kịp xu hướng, Tạo thu nhập thụ động xanh</h4><p style="color:#e2e8f0; font-size:1rem; margin-bottom:0;">Tạo ra dòng <b>thu nhập thụ động vững chắc</b> và <b>đóng góp vào phát kiến xanh</b>, chung tay bảo vệ địa cầu.</p></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background: linear-gradient(90deg, #1a202c 0%, #742a2a 100%); padding: 20px; border-radius: 8px; border-left: 5px solid #f6ad55; margin-bottom: 25px;"><h4 style="color:#ffffff; margin-top:0;">Catch the Trend, Create Green Passive Income</h4><p style="color:#e2e8f0; font-size:1rem; margin-bottom:0;">Generate a <b>solid passive income stream</b> and <b>contribute to green innovations</b>, protecting the planet.</p></div>""", unsafe_allow_html=True)

    st.markdown("### 📊 Danh mục Cổ phần Đã góp vốn" if lang == "Tiếng Việt" else "### 📊 Your Investment Portfolio")
    cur_user = st.session_state['current_user']
    inv_hold = st.session_state.get("investor_portfolios", {}).get(cur_user, [])
    if not inv_hold:
        st.info("Bạn chưa góp vốn vào dự án nào." if lang == "Tiếng Việt" else "You haven't invested in any projects yet.")
    else:
        st.dataframe(pd.DataFrame(inv_hold), use_container_width=True, hide_index=True)
    st.divider()

    st.markdown("### 🚀 Danh sách Dự án Đang Kêu gọi Vốn" if lang == "Tiếng Việt" else "### 🚀 Projects Calling for Investment")
    for p in st.session_state["market_projects"]:
        if "funding_goal" in p and p.get('status') == 'Active':
            with st.container(border=True):
                col_i, col_a = st.columns([3, 2])
                with col_i:
                    st.markdown(f"#### 🌲 {p['name']}")
                    st.write(f"**Chủ dự án / Owner:** {p['owner']}")
                    prog = min(100, int((p['funded_amount'] / p['funding_goal']) * 100))
                    lbl_fund = "Tiến độ góp vốn" if lang=="Tiếng Việt" else "Funding Progress"
                    st.write(f"💵 **{lbl_fund}:** ${p['funded_amount']:,.0f} /${p['funding_goal']:,.0f} ({prog}%)")
                    st.progress(prog)
                with col_a:
                    with st.form(f"fund_f_{p['id']}", clear_on_submit=True):
                        max_f = int(p['funding_goal'] - p['funded_amount'])
                        t_gop = st.number_input("Số vốn góp / Amount:" , min_value=100, max_value=max_f if max_f > 0 else 1, value=min(1000, max_f))
                        
                        btn_fund = st.form_submit_button("🤝 ĐẦU TƯ / INVEST", type="primary", use_container_width=True)
                        if btn_fund:
                            if max_f <= 0: st.warning("Đã gọi đủ vốn / Fully funded.")
                            elif st.session_state["wallet_balance"] >= t_gop:
                                st.session_state["wallet_balance"] -= t_gop
                                p['funded_amount'] += t_gop
                                if cur_user not in st.session_state["investor_portfolios"]: st.session_state["investor_portfolios"][cur_user] = []
                                st.session_state["investor_portfolios"][cur_user].append({"Dự án / Project": p['name'], "Vốn góp / Amount": f"${t_gop:,.2f}"})
                                st.success("Thành công! / Success!")
                                st.rerun()
                            else: st.error("Ví không đủ tiền / Insufficient funds.")


def hien_thi_gioi_thieu_va_goi_von():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    
    if lang == "Tiếng Việt":
        st.title("🌟 VỀ CHÚNG TÔI & TẦM NHÌN TƯƠNG LAI")
        st.markdown("""<div class="thank-you-banner"><span class="text-green">Thay mặt Đội ngũ Sáng lập, chúng tôi xin gửi </span><span class="text-blue-bold">LỜI CẢM ƠN CHÂN THÀNH NHẤT</span><span class="text-green"> đến Quý Chủ rừng, Doanh nghiệp và Nhà đầu tư tiên phong...</span></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="mission-container"><p class="mission-text"><b>Sứ mệnh:</b> Tích hợp trí tuệ nhân tạo (GEE) với Sổ đỏ để loại bỏ "rừng ma", đưa doanh nghiệp và chủ rừng đến gần nhau với độ tin cậy tuyệt đối.</p></div>""", unsafe_allow_html=True)
        st.markdown("### 🏛 Chứng nhận Uy tín & Đối tác")
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown("""<div class="partner-card"><div class="pc-title">Tiêu chuẩn</div><div class="pc-value">VCS & Gold Standard</div><div class="pc-status">✔ Đạt chuẩn toàn cầu</div></div>""", unsafe_allow_html=True)
        c2.markdown("""<div class="partner-card"><div class="pc-title">Công nghệ</div><div class="pc-value">ESA WorldCover & GEE</div><div class="pc-status">✔️ Real-time AI</div></div>""", unsafe_allow_html=True)
        c3.markdown("""<div class="partner-card"><div class="pc-title">Pháp lý</div><div class="pc-value">Sổ đỏ Lâm nghiệp Gốc</div><div class="pc-status">✔️ Xác thực chéo 100%</div></div>""", unsafe_allow_html=True)
        c4.markdown("""<div class="partner-card"><div class="pc-title">Kiểm toán</div><div class="pc-value">Smart Contract Escrow</div><div class="pc-status">✔️ Minh bạch tuyệt đối</div></div>""", unsafe_allow_html=True)
    else:
        st.title("🌟 ABOUT US & FUTURE VISION")
        st.markdown("""<div class="thank-you-banner"><span class="text-green">On behalf of the Founding Team, we send our </span><span class="text-blue-bold">DEEPEST GRATITUDE</span><span class="text-green"> to the Forest Owners, Businesses, and pioneering Investors...</span></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="mission-container"><p class="mission-text"><b>Mission:</b> Integrating AI (GEE) with Land Rights Certificates to eliminate "ghost forests", bringing businesses and forest owners together with absolute trust.</p></div>""", unsafe_allow_html=True)
        st.markdown("### 🏛 Prestigious Certifications & Partners")
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown("""<div class="partner-card"><div class="pc-title">Standard</div><div class="pc-value">VCS & Gold Standard</div><div class="pc-status">✔ Global Standard</div></div>""", unsafe_allow_html=True)
        c2.markdown("""<div class="partner-card"><div class="pc-title">Technology</div><div class="pc-value">ESA WorldCover & GEE</div><div class="pc-status">✔️ Real-time AI</div></div>""", unsafe_allow_html=True)
        c3.markdown("""<div class="partner-card"><div class="pc-title">Legal</div><div class="pc-value">Original Land Rights</div><div class="pc-status">✔️ 100% Cross-verified</div></div>""", unsafe_allow_html=True)
        c4.markdown("""<div class="partner-card"><div class="pc-title">Audit</div><div class="pc-value">Smart Contract Escrow</div><div class="pc-status">✔️ Absolute Transparency</div></div>""", unsafe_allow_html=True)
