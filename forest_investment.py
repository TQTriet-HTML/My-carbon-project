import streamlit as st
import datetime
import time
import base64

@st.dialog("CỔNG THANH TOÁN & ĐẦU TƯ / INVESTMENT GATEWAY", width="large")
def hop_thoai_thanh_toan_dau_tu(proj_idx, lang="Tiếng Việt"):
    proj = st.session_state["invest_projects"][proj_idx]
    
    T = {
        "Tiếng Việt": {
            "pledge_title": "CAM KẾT MINH BẠCH (ĐÃ XÁC MINH)",
            "pledge_desc": f"Chủ quản <b>{proj['owner']}</b> cam kết sử dụng 100% nguồn vốn vào việc phát triển sinh khối. Toàn bộ tiến trình được AI giám sát viễn thám độc lập định kỳ.",
            "discount_title": "CHÍNH SÁCH CHIẾT KHẤU & QUYỀN LỢI",
            "tier_1": "Góp vốn < 10%: Chiết khấu 5% mua tín chỉ + Lãi suất 2%/năm",
            "tier_2": "Góp vốn 10% - 30%: Chiết khấu 10% mua tín chỉ + Lãi suất 4%/năm + Báo cáo vệ tinh chi tiết",
            "tier_3": "Góp vốn > 30%: Chiết khấu 15% mua tín chỉ + Lãi suất 6%/năm + Quyền đặt giá tham chiếu",
            "invest_amt": "Nhập số tiền đầu tư ($):",
            "btn_confirm": "XÁC NHẬN THANH TOÁN",
            "success_msg": "Giao dịch thành công! Bạn đã góp phần kiến tạo mảng xanh mới.",
            "progress_msg": "Hệ thống đang xử lý giao dịch qua Vietcombank Escrow..."
        },
        "English": {
            "pledge_title": "TRANSPARENCY PLEDGE (VERIFIED)",
            "pledge_desc": f"Owner <b>{proj['owner']}</b> commits to allocating 100% of funds to biomass development. The entire progress is monitored periodically by independent AI remote sensing.",
            "discount_title": "DISCOUNT & BENEFITS POLICY",
            "tier_1": "Funding < 10%: 5% Credit Discount + 2% Annual Yield",
            "tier_2": "Funding 10% - 30%: 10% Credit Discount + 4% Annual Yield + Detailed Satellite Report",
            "tier_3": "Funding > 30%: 15% Credit Discount + 6% Annual Yield + Reference Pricing Rights",
            "invest_amt": "Enter investment amount ($):",
            "btn_confirm": "CONFIRM PAYMENT",
            "success_msg": "Transaction successful! You have contributed to a new green legacy.",
            "progress_msg": "Processing transaction via Vietcombank Escrow..."
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

    st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 15px; border-radius: 0 8px 8px 0; margin-bottom: 20px;">
            <div style="font-weight: 800; color: #10b981; font-size: 1.05rem; margin-bottom: 5px;">🛡️ {t['pledge_title']}</div>
            <div style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">{t['pledge_desc']}</div>
        </div>
        
        <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); padding: 15px; border-radius: 8px; margin-bottom: 25px;">
            <div style="font-weight: 800; color: #38bdf8; font-size: 1.05rem; margin-bottom: 10px;">💎 {t['discount_title']}</div>
            <ul style="color: #e2e8f0; font-size: 0.95rem; margin-bottom: 0;">
                <li>{t['tier_1']}</li>
                <li style="margin-top: 5px;">{t['tier_2']}</li>
                <li style="margin-top: 5px; color: #fbbf24; font-weight: 700;">{t['tier_3']}</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    amt = st.number_input(t["invest_amt"], min_value=100, step=1000)
    
    if st.button(t["btn_confirm"], type="primary", use_container_width=True):
        with st.spinner(t["progress_msg"]):
            time.sleep(2)
        
        if "my_investments" not in st.session_state:
            st.session_state["my_investments"] = []
        
        target_val = float(proj['target'].replace('$', '').replace(',', ''))
        ratio = (amt / target_val) * 100 if target_val > 0 else 0
        
        discount = "5%" if ratio < 10 else ("10%" if ratio <= 30 else "15%")
        yield_pct = "2%" if ratio < 10 else ("4%" if ratio <= 30 else "6%")
        
        st.session_state["my_investments"].append({
            "name": proj["name"],
            "amount": amt,
            "ratio": ratio,
            "discount": discount,
            "yield": yield_pct,
            "time": datetime.datetime.now().strftime("%d/%m/%Y"),
            "owner": proj["owner"]
        })
        
        if "green_points" not in st.session_state: st.session_state["green_points"] = 0
        st.session_state["green_points"] += int(amt / 10)
        
        st.success(t["success_msg"])
        time.sleep(1)
        st.rerun()

def hien_thi_dau_tu_trong_rung(lang=None):
    if lang is None:
        lang = st.session_state.get("language", st.session_state.get("lang", st.session_state.get("current_lang", "Tiếng Việt")))
    if lang not in ["Tiếng Việt", "English"]:
        lang = "Tiếng Việt"

    T = {
        "Tiếng Việt": {
            "title": "CỔNG ĐẦU TƯ TRỒNG RỪNG TỪ XA",
            "subtitle": "Nơi nguồn vốn xanh kiến tạo nên những cánh rừng nguyên sinh thế hệ mới.",
            "guide_title": "TIÊU CHUẨN PHÂN LOẠI & ĐỊNH GIÁ TÍN CHỈ CARBON",
            "tier_a": "Hạng A (Cao cấp)",
            "tier_a_desc": "Đa dạng sinh học cao, bảo tồn sinh thái lõi, xác thực chứng chỉ quốc tế (Verra/VCS).",
            "tier_a_price": "Giá tham chiếu: $25 - $35 / Tấn",
            "tier_b": "Hạng B (Tiêu chuẩn)",
            "tier_b_desc": "Rừng trồng mới công nghiệp, đạt chuẩn đo lường viễn thám MRV cơ bản.",
            "tier_b_price": "Giá tham chiếu: $10 - $18 / Tấn",
            "tier_c": "Hạng C (Ươm mầm)",
            "tier_c_desc": "Khu vực đang phục hồi, sinh khối chưa ổn định, chờ AI giám sát định kỳ.",
            "tier_c_price": "Giá tham chiếu: $5 - $8 / Tấn",
            "create_proj_title": "TẠO DỰ ÁN KÊU GỌI VỐN (Dành cho Chủ Rừng)",
            "proj_name": "Tên dự án sinh thái:",
            "proj_target": "Mục tiêu gọi vốn ($):",
            "proj_tier": "Loại tín chỉ dự kiến cung cấp:",
            "proj_contact": "Thông tin liên hệ (Email/Phone):",
            "ai_verify": "Yêu cầu AI phân tích dữ liệu vệ tinh sơ bộ để minh bạch hóa dự án",
            "btn_create": "ĐĂNG DỰ ÁN",
            "ai_processing": "AI đang đối chiếu tọa độ vệ tinh & lịch sử sinh khối...",
            "ai_success": "AI xác minh: Đạt chuẩn minh bạch ban đầu. Dự án đã được đăng!",
            "market_title": "DANH MỤC ĐẦU TƯ SINH THÁI ĐANG MỞ",
            "btn_invest": "ĐẦU TƯ NGAY",
            "contact_lbl": "Liên hệ chủ quản:",
            "my_invest_title": "CÁC DỰ ÁN TÔI ĐÃ ĐẦU TƯ",
            "no_invest": "Bạn chưa tham gia đầu tư dự án nào.",
            "badge_msg": "Huy hiệu Dấu ấn Xanh:",
            "pts": "Điểm cống hiến",
            "ratio_lbl": "Tỷ lệ góp vốn:",
            "benefit_lbl": "Quyền lợi nhận được:",
            "status_lbl": "Tiến độ dự án:"
        },
        "English": {
            "title": "REMOTE FOREST INVESTMENT PORTAL",
            "subtitle": "Where green capital creates the next generation of primeval forests.",
            "guide_title": "CARBON CREDIT CLASSIFICATION & PRICING GUIDE",
            "tier_a": "Tier A (Premium)",
            "tier_a_desc": "High biodiversity, core ecological conservation, international certification (Verra/VCS).",
            "tier_a_price": "Ref. Price: $25 - $35 / Ton",
            "tier_b": "Tier B (Standard)",
            "tier_b_desc": "Newly planted commercial forests, meeting basic MRV remote sensing standards.",
            "tier_b_price": "Ref. Price: $10 - $18 / Ton",
            "tier_c": "Tier C (Seedling/Pending)",
            "tier_c_desc": "Recovering areas, unstable biomass, pending periodic AI monitoring.",
            "tier_c_price": "Ref. Price: $5 - $8 / Ton",
            "create_proj_title": "CREATE FUNDING PROJECT (For Forest Owners)",
            "proj_name": "Eco Project Name:",
            "proj_target": "Funding Target ($):",
            "proj_tier": "Expected Credit Type:",
            "proj_contact": "Contact Info (Email/Phone):",
            "ai_verify": "Request AI preliminary satellite analysis for project transparency",
            "btn_create": "PUBLISH PROJECT",
            "ai_processing": "AI is cross-referencing satellite coordinates & biomass history...",
            "ai_success": "AI Verified: Initial transparency met. Project published!",
            "market_title": "OPEN ECO-INVESTMENT PORTFOLIO",
            "btn_invest": "INVEST NOW",
            "contact_lbl": "Contact owner:",
            "my_invest_title": "MY INVESTMENT PORTFOLIO",
            "no_invest": "You haven't invested in any projects yet.",
            "badge_msg": "Green Legacy Badge:",
            "pts": "Contribution points",
            "ratio_lbl": "Funding Ratio:",
            "benefit_lbl": "Benefits Received:",
            "status_lbl": "Project Progress:"
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

    st.markdown("""
        <style>
        .invest-title-green {
            color: #48bb78 !important;
            font-size: clamp(24px, 2.7vw, 34px) !important;
            font-weight: 900 !important;
            text-align: center;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
            text-transform: uppercase;
            text-shadow: 0 0 15px rgba(72, 187, 120, 0.4);
        }
        .invest-sub { text-align: center; color: #94a3b8; font-size: 1rem; margin-bottom: 30px; }
        
        @keyframes greenGlowPulse {
            0%, 100% { box-shadow: 0 0 15px rgba(72, 187, 120, 0.2); }
            50% { box-shadow: 0 0 25px rgba(72, 187, 120, 0.6); }
        }
        .tier-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8));
            border: 1px solid rgba(72, 187, 120, 0.3); border-radius: 12px; padding: 20px; height: 100%;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); animation: greenGlowPulse 4s infinite ease-in-out; position: relative; overflow: hidden;
        }
        .tier-card::before {
            content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.4), transparent);
            transform: skewX(-25deg); transition: all 0.5s ease; z-index: 1; pointer-events: none;
        }
        .tier-card:hover::before { animation: none; left: 200%; transition: left 0.7s ease-in-out; }
        .tier-card:hover { transform: translateY(-8px) scale(1.02); border-color: #4ade80; box-shadow: 0 15px 35px rgba(74, 222, 128, 0.5); z-index: 5; }
        .tier-title { font-size: 1.15rem; font-weight: 800; margin-bottom: 10px; position: relative; z-index: 2; }
        .tier-desc { color: #cbd5e1; font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; position: relative; z-index: 2; }
        .tier-price { font-size: 0.95rem; font-weight: 700; padding: 8px 12px; border-radius: 6px; display: inline-block; position: relative; z-index: 2; }

        .project-card {
            background: rgba(15, 23, 42, 0.65); border: 1.5px solid rgba(56, 189, 248, 0.3); border-radius: 14px;
            padding: 22px; margin-bottom: 25px; position: relative; overflow: hidden; transition: all 0.3s ease;
        }
        .project-card:hover { border-color: #38bdf8; box-shadow: 0 8px 30px rgba(56, 189, 248, 0.25); transform: translateY(-3px); }
        .badge-tier { position: absolute; top: 20px; right: 20px; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; }
        
        div[data-testid="stFormSubmitButton"] button, div[class*="st-key-btn_invest_"] button {
            background: linear-gradient(180deg, #22c55e 0%, #16a34a 100%) !important; border: 1.5px solid #4ade80 !important;
            border-radius: 10px !important; box-shadow: 0 5px 0 #15803d, 0 8px 18px rgba(34, 197, 94, 0.45) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; color: #ffffff !important; font-weight: 800 !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover, div[class*="st-key-btn_invest_"] button:hover {
            background: linear-gradient(180deg, #4ade80 0%, #22c55e 100%) !important; transform: translateY(-4px) !important;
            box-shadow: 0 9px 0 #15803d, 0 14px 26px rgba(34, 197, 94, 0.75) !important; border-color: #6ee7b7 !important;
        }
        div[data-testid="stFormSubmitButton"] button:active, div[class*="st-key-btn_invest_"] button:active {
            transform: translateY(4px) !important; box-shadow: 0 1px 0 #15803d, 0 4px 10px rgba(34, 197, 94, 0.4) !important; border-color: #4ade80 !important;
        }
        div[data-testid="stFormSubmitButton"] button:focus, div[class*="st-key-btn_invest_"] button:focus {
            outline: none !important; box-shadow: 0 5px 0 #15803d, 0 8px 18px rgba(34, 197, 94, 0.45) !important; color: #ffffff !important;
        }
        
        .contact-chip { display: inline-block; background: rgba(56,189,248,0.1); border: 1px solid rgba(56,189,248,0.4); padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; color: #7dd3fc; margin-top: 10px; }
        
        .my-invest-card {
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.4), rgba(2, 44, 34, 0.6));
            border: 1.5px solid #10b981; border-radius: 12px; padding: 18px; margin-bottom: 15px;
        }
        .prog-bar-bg { background: #1e293b; height: 8px; border-radius: 4px; overflow: hidden; margin-top: 8px; margin-bottom: 12px; }
        .prog-bar-fill { background: linear-gradient(90deg, #34d399, #10b981); height: 100%; border-radius: 4px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="invest-title-green">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="invest-sub">{t["subtitle"]}</div>', unsafe_allow_html=True)

    with st.expander(t["guide_title"], expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class="tier-card"><div class="tier-title" style="color: #fbbf24;">{t["tier_a"]}</div><div class="tier-desc">{t["tier_a_desc"]}</div><div class="tier-price" style="background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid #fbbf24;">{t["tier_a_price"]}</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="tier-card"><div class="tier-title" style="color: #38bdf8;">{t["tier_b"]}</div><div class="tier-desc">{t["tier_b_desc"]}</div><div class="tier-price" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid #38bdf8;">{t["tier_b_price"]}</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="tier-card"><div class="tier-title" style="color: #94a3b8;">{t["tier_c"]}</div><div class="tier-desc">{t["tier_c_desc"]}</div><div class="tier-price" style="background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px solid #94a3b8;">{t["tier_c_price"]}</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)

    user_role = st.session_state.get("current_role", "Nhà đầu tư từ xa (Cổ đông)")
    is_seller = "Chủ rừng" in user_role or "MRV" in user_role or "Owner" in user_role

    if is_seller:
        with st.container(border=True):
            st.markdown(f'<div style="color:#4ade80; font-weight:800; font-size:1.15rem; margin-bottom:15px; letter-spacing: 0.5px;">{t["create_proj_title"]}</div>', unsafe_allow_html=True)
            with st.form("form_create_project", clear_on_submit=True):
                p_name = st.text_input(t["proj_name"])
                c_vol, c_tier = st.columns(2)
                with c_vol: p_target = st.number_input(t["proj_target"], min_value=1000, step=5000)
                with c_tier: p_type = st.selectbox(t["proj_tier"], [t["tier_a"], t["tier_b"], t["tier_c"]])
                
                p_contact = st.text_input(t["proj_contact"])
                
                st.markdown("<div style='margin-top: 10px; margin-bottom: 5px; color:#cbd5e1; font-size:0.9rem;'>Đính kèm hồ sơ dự án/hình ảnh minh chứng (Tùy chọn):</div>", unsafe_allow_html=True)
                p_file = st.file_uploader("", label_visibility="collapsed", key="proj_file")

                ai_check = st.checkbox(t["ai_verify"], value=True)
                
                submitted_proj = st.form_submit_button(t["btn_create"], use_container_width=True)
                if submitted_proj:
                    if p_name.strip():
                        if ai_check:
                            with st.spinner(t["ai_processing"]): time.sleep(2)
                            st.success(t["ai_success"])
                        else:
                            st.success("Dự án đã được lưu vào hệ thống chờ duyệt tay.")
                        
                        if "invest_projects" not in st.session_state: st.session_state["invest_projects"] = []
                        
                        badge_color = "#fbbf24" if "Hạng A" in p_type or "Tier A" in p_type else ("#38bdf8" if "Hạng B" in p_type or "Tier B" in p_type else "#94a3b8")
                        bg_color = "rgba(251, 191, 36, 0.15)" if "Hạng A" in p_type or "Tier A" in p_type else ("rgba(56, 189, 248, 0.15)" if "Hạng B" in p_type or "Tier B" in p_type else "rgba(148, 163, 184, 0.15)")
                        
                        file_data_html = ""
                        if p_file is not None:
                            if p_file.type.startswith("image/"):
                                b64 = base64.b64encode(p_file.getvalue()).decode()
                                file_data_html = f"<img src='data:{p_file.type};base64,{b64}' style='width:100%; border-radius:12px; margin-top:15px; margin-bottom:15px; border:1.5px solid rgba(56,189,248,0.3);'/>"
                            else:
                                file_data_html = f"<div style='margin-top:15px; margin-bottom:15px; padding:10px; background:rgba(255,255,255,0.1); border-radius:8px;'>📎 Đã đính kèm tài liệu: {p_file.name}</div>"

                        st.session_state["invest_projects"].insert(0, {
                            "name": p_name, "target": f"${p_target:,.0f}", "tier": p_type,
                            "badge_color": badge_color, "bg_color": bg_color, "owner": st.session_state.get("current_user", "Unknown"),
                            "contact": p_contact, "file_html": file_data_html
                        })
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("Vui lòng nhập tên dự án.")

    if "invest_projects" not in st.session_state:
        st.session_state["invest_projects"] = [
            {
                "name": "Dự án Rừng Khộp Tây Nguyên" if lang == "Tiếng Việt" else "Central Highlands Dipterocarp Project",
                "target": "$150,000", "tier": t["tier_c"], "badge_color": "#94a3b8", "bg_color": "rgba(148, 163, 184, 0.15)",
                "owner": "Hợp tác xã Nông Lâm", "contact": "htxnonglam@eco.vn", "file_html": ""
            },
            {
                "name": "Phục hồi Sinh thái Ngập mặn Đồng bằng Sông Cửu Long" if lang == "Tiếng Việt" else "Mekong Delta Mangrove Ecological Restoration",
                "target": "$500,000", "tier": t["tier_b"], "badge_color": "#38bdf8", "bg_color": "rgba(56, 189, 248, 0.15)",
                "owner": "Tập đoàn Phát triển Rừng Ven Biển", "contact": "+84 909 123 456", "file_html": ""
            }
        ]

    st.markdown(f'<div class="invest-title-green" style="font-size:1.4rem; margin-top:35px; margin-bottom:20px;">{t["market_title"]}</div>', unsafe_allow_html=True)

    for idx, proj in enumerate(st.session_state["invest_projects"]):
        contact_html = f"<div class='contact-chip'>📞 {t['contact_lbl']} {proj.get('contact', 'N/A')}</div>" if proj.get('contact') else ""
        file_rendered = proj.get("file_html", "")

        html_card = f"""<div class="project-card">
<div class="badge-tier" style="color: {proj['badge_color']}; border: 1px solid {proj['badge_color']}; background: {proj['bg_color']};">
{proj['tier']}
</div>
<div style="font-size: 1.2rem; font-weight: 800; color: #f8fafc; margin-bottom: 8px; padding-right: 120px;">
{proj['name']}
</div>
<div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 12px;">
Chủ quản: <b style="color: #cbd5e1;">{proj['owner']}</b> &nbsp;|&nbsp; Mục tiêu: <b style="color: #4ade80;">{proj['target']}</b>
</div>
{file_rendered}
{contact_html}
</div>"""
        st.markdown(html_card, unsafe_allow_html=True)
        
        col_btn, _ = st.columns([0.3, 0.7])
        with col_btn:
            if st.button(t["btn_invest"], key=f"btn_invest_{idx}", use_container_width=True):
                hop_thoai_thanh_toan_dau_tu(idx, lang)
        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

    st.markdown(f'<div class="invest-title-green" style="font-size:1.4rem; margin-top:40px; margin-bottom:20px;">{t["my_invest_title"]}</div>', unsafe_allow_html=True)
    
    my_invs = st.session_state.get("my_investments", [])
    green_pts = st.session_state.get("green_points", 0)

    if green_pts > 0:
        lvl = "Hạt giống" if green_pts < 50 else ("Mầm non" if green_pts < 200 else ("Cây cổ thụ" if green_pts < 500 else "Đại ngàn"))
        if lang == "English": lvl = "Seed" if green_pts < 50 else ("Sprout" if green_pts < 200 else ("Ancient Tree" if green_pts < 500 else "Great Forest"))
        st.markdown(f"<div style='text-align:center; color:#38bdf8; margin-bottom:20px; font-weight:800; font-size:1.1rem;'>🎖️ {t['badge_msg']} <span style='color:#fde047;'>{lvl}</span> ({green_pts} {t['pts']})</div>", unsafe_allow_html=True)

    if not my_invs:
        st.info(t["no_invest"])
    else:
        for inv in my_invs:
            html_my_inv = f"""<div class="my-invest-card">
<div style="font-size: 1.1rem; font-weight: 800; color: #f8fafc; margin-bottom: 5px;">{inv['name']}</div>
<div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 12px;">Ngày đầu tư: {inv['time']} &nbsp;|&nbsp; Số tiền: <b style="color:#4ade80;">${inv['amount']:,.0f}</b></div>
<div style="color: #e2e8f0; font-size: 0.9rem; margin-bottom: 5px;">{t['ratio_lbl']} <b style="color:#38bdf8;">{inv['ratio']:.2f}%</b> tổng vốn</div>
<div class="prog-bar-bg"><div class="prog-bar-fill" style="width: {min(100, inv['ratio'])}%;"></div></div>
<div style="margin-top: 15px; padding: 10px; background: rgba(0,0,0,0.2); border-radius: 8px;">
<div style="color: #fbbf24; font-size: 0.85rem; font-weight: 800; margin-bottom: 4px;">{t['benefit_lbl']}</div>
<ul style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0;">
<li>Được giảm giá <b>{inv['discount']}</b> khi mua tín chỉ tương lai.</li>
<li>Lợi suất sinh thái cố định: <b>{inv['yield']}</b>.</li>
</ul>
</div>
</div>"""
            st.markdown(html_my_inv, unsafe_allow_html=True)
