import streamlit as st

def hien_thi_vinh_danh_va_gop_y(lang="Tiếng Việt"):
    T = {
        "Tiếng Việt": {
            "title": "BẢNG VÀNG & TÔN VINH",
            "tab_enterprise": "TOP DOANH NGHIỆP",
            "tab_project": "TOP DỰ ÁN TRỒNG RỪNG",
            "col_rank": "Hạng",
            "col_enterprise": "Doanh Nghiệp",
            "col_credits": "Tín chỉ",
            "col_project": "Dự Án",
            "col_co2": "CO2",
            "proj_1": "Rừng ngập mặn Cà Mau",
            "proj_2": "Dự án Bắc Trung Bộ",
            "proj_3": "KBT Nam Cát Tiên",
            "process_title": "QUÁ TRÌNH SỐNG XANH",
            "current_lvl": "CẤP ĐỘ HIỆN TẠI",
            "next_lvl": "TIẾN TRÌNH LÊN CẤP KẾ TIẾP",
            "progress_msg": "hoàn thành chặng đường thăng hạng.",
            "req_title": "YÊU CẦU ĐỂ THĂNG CẤP TIẾP THEO",
            "reached": "ĐÃ ĐẠT",
            "current": "HIỆN TẠI",
            "next_target": "MỤC TIÊU TIẾP THEO",
            "locked": "KHÓA",
            
            # Roles - Doanh Nghiệp
            "role_dn_1": "Doanh nghiệp Tiên Phong Xanh",
            "role_dn_2": "Đại Sứ Net-Zero",
            "dn_l1_name": "Cấp 1: Doanh nghiệp Khởi Động Xanh", "dn_l1_req": "Bù trừ tối thiểu 1,000 Tấn CO2",
            "dn_l2_name": "Cấp 2: Doanh nghiệp Tiên Phong Xanh", "dn_l2_req": "Bù trừ từ 5,000 - 20,000 Tấn CO2",
            "dn_l3_name": "Cấp 3: Đại Sứ Net-Zero", "dn_l3_req": "Bù trừ trên 50,000 Tấn CO2 & Đạt ESG Hạng A+",
            "dn_l4_name": "Cấp 4: Tập Đoàn Không Phát Thải", "dn_l4_req": "Cam kết trung hòa carbon toàn chuỗi cung ứng",
            
            # Roles - Chủ Rừng
            "role_cr_1": "Kỹ Sư Kiến Tạo Sinh Khối",
            "role_cr_2": "Đại Sứ Bảo Tồn Rừng",
            "cr_l1_name": "Cấp 1: Người Gieo Hạt Xanh", "cr_l1_req": "Kiểm kê tối thiểu 100 Hecta qua viễn thám AI",
            "cr_l2_name": "Cấp 2: Kỹ Sư Kiến Tạo Sinh Khối", "cr_l2_req": "Duy trì sinh khối rừng tăng trưởng 3 năm liên tiếp",
            "cr_l3_name": "Cấp 3: Đại Sứ Bảo Tồn Rừng", "cr_l3_req": "Bảo vệ trên 1,000 Hecta & Niêm yết thành công 100,000 Tín chỉ",
            "cr_l4_name": "Cấp 4: Thủ Lĩnh Đại Ngàn", "cr_l4_req": "Bảo tồn hệ sinh thái rừng nguyên sinh quy mô quốc gia",
            
            # Roles - Nhà Đầu Tư
            "role_nd_1": "Nhà Đầu Tư Sinh Thái Cấp 1",
            "role_nd_2": "Cổ Đông Bảo Trợ Rừng Xanh",
            "nd_l1_name": "Cấp 1: Cổ Đông Hạt Giống", "nd_l1_req": "Góp vốn vào 1 dự án sinh thái",
            "nd_l2_name": "Cấp 2: Nhà Đầu Tư Sinh Thái Cấp 1", "nd_l2_req": "Đầu tư trên $20,000 vào các dự án tín chỉ",
            "nd_l3_name": "Cấp 3: Cổ Đông Bảo Trợ Rừng Xanh", "nd_l3_req": "Đầu tư trên $100,000 & Sở hữu chứng chỉ Verra",
            "nd_l4_name": "Cấp 4: Quỹ Đầu Tư Xanh Huyền Thoại", "nd_l4_req": "Bảo lãnh tài chính cho chuỗi dự án quốc gia"
        },
        "English": {
            "title": "LEADERBOARD & HALL OF FAME",
            "tab_enterprise": "TOP ENTERPRISES",
            "tab_project": "TOP AFFORESTATION PROJECTS",
            "col_rank": "Rank",
            "col_enterprise": "Enterprise",
            "col_credits": "Credits",
            "col_project": "Project",
            "col_co2": "CO2",
            "proj_1": "Ca Mau Mangrove Forest",
            "proj_2": "North Central Region Project",
            "proj_3": "Nam Cat Tien Reserve",
            "process_title": "GREEN JOURNEY PROGRESS",
            "current_lvl": "CURRENT LEVEL",
            "next_lvl": "PROGRESS TO NEXT LEVEL",
            "progress_msg": "completed towards next rank.",
            "req_title": "REQUIREMENTS FOR NEXT LEVEL",
            "reached": "ACHIEVED",
            "current": "CURRENT",
            "next_target": "NEXT TARGET",
            "locked": "LOCKED",
            
            # Roles - Doanh Nghiệp
            "role_dn_1": "Green Pioneer Enterprise",
            "role_dn_2": "Net-Zero Ambassador",
            "dn_l1_name": "Level 1: Green Starter Enterprise", "dn_l1_req": "Offset at least 1,000 Tons of CO2",
            "dn_l2_name": "Level 2: Green Pioneer Enterprise", "dn_l2_req": "Offset 5,000 - 20,000 Tons of CO2",
            "dn_l3_name": "Level 3: Net-Zero Ambassador", "dn_l3_req": "Offset over 50,000 Tons of CO2 & Achieve ESG A+",
            "dn_l4_name": "Level 4: Zero Emission Corporation", "dn_l4_req": "Commit to carbon neutrality across supply chain",
            
            # Roles - Chủ Rừng
            "role_cr_1": "Biomass Creation Engineer",
            "role_cr_2": "Forest Conservation Ambassador",
            "cr_l1_name": "Level 1: Green Seed Sower", "cr_l1_req": "Inventory at least 100 Hectares via AI remote sensing",
            "cr_l2_name": "Level 2: Biomass Creation Engineer", "cr_l2_req": "Maintain forest biomass growth for 3 consecutive years",
            "cr_l3_name": "Level 3: Forest Conservation Ambassador", "cr_l3_req": "Protect >1,000 Hectares & List 100,000 Credits",
            "cr_l4_name": "Level 4: Master of the Woods", "cr_l4_req": "Conserve national-scale primeval forest ecosystems",
            
            # Roles - Nhà Đầu Tư
            "role_nd_1": "Eco Investor Level 1",
            "role_nd_2": "Green Forest Patron Shareholder",
            "nd_l1_name": "Level 1: Seed Shareholder", "nd_l1_req": "Capital contribution to 1 eco project",
            "nd_l2_name": "Level 2: Eco Investor Level 1", "nd_l2_req": "Invest over $20,000 in credit projects",
            "nd_l3_name": "Level 3: Green Forest Patron Shareholder", "nd_l3_req": "Invest >$100,000 & Own Verra certificates",
            "nd_l4_name": "Level 4: Legendary Green Fund", "nd_l4_req": "Financial guarantee for national project chain"
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

    st.markdown("""
        <style>
        .section-header-green {
            color: #48bb78 !important;
            font-size: clamp(24px, 2.8vw, 34px) !important;
            font-weight: 900 !important;
            text-align: center;
            letter-spacing: 1.5px;
            margin-bottom: 25px;
            text-transform: uppercase;
            text-shadow: 0 0 16px rgba(72, 187, 120, 0.4);
        }
        .table-title-blue {
            color: #38bdf8 !important;
            font-size: 1.25rem !important;
            font-weight: 800 !important;
            text-align: center;
            letter-spacing: 1px;
            margin-bottom: 15px;
            text-transform: uppercase;
        }
        @keyframes blueNeonPulse {
            0%, 100% {
                box-shadow: 0 0 16px rgba(56, 189, 248, 0.28), inset 0 0 12px rgba(56, 189, 248, 0.1);
                border-color: rgba(56, 189, 248, 0.5) !important;
            }
            50% {
                box-shadow: 0 0 38px rgba(56, 189, 248, 0.8), inset 0 0 22px rgba(56, 189, 248, 0.3);
                border-color: #38bdf8 !important;
            }
        }
        @keyframes sweepBlue10s {
            0%, 85% { left: -120%; opacity: 0; }
            86% { opacity: 1; left: -120%; }
            95%, 100% { left: 220%; opacity: 0; }
        }
        .blue-rank-card {
            background: linear-gradient(135deg, rgba(10, 25, 47, 0.95), rgba(15, 33, 64, 0.92)) !important;
            border: 2px solid rgba(56, 189, 248, 0.5) !important;
            border-radius: 16px !important;
            padding: 22px !important;
            margin-bottom: 20px !important;
            position: relative !important;
            overflow: hidden !important;
            animation: blueNeonPulse 4s infinite ease-in-out !important;
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.35s ease, border-color 0.35s ease !important;
        }
        .blue-rank-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: -120%;
            width: 55%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.65), transparent);
            transform: skewX(-25deg);
            animation: sweepBlue10s 10s infinite linear;
            z-index: 10;
            pointer-events: none;
        }
        .blue-rank-card:hover {
            transform: translateY(-8px) scale(1.02) !important;
            box-shadow: 0 22px 50px rgba(56, 189, 248, 0.9), inset 0 0 25px rgba(56, 189, 248, 0.4) !important;
            border-color: #38bdf8 !important;
            z-index: 5 !important;
        }
        .milestone-container {
            background: linear-gradient(135deg, rgba(13, 31, 60, 0.95), rgba(18, 42, 77, 0.92));
            border: 1.5px solid rgba(72, 187, 120, 0.5);
            border-radius: 14px;
            padding: 24px;
            margin-top: 15px;
        }
        .level-badge {
            display: inline-block;
            background: rgba(72, 187, 120, 0.2);
            color: #48bb78;
            border: 1px solid #48bb78;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 800;
            font-size: 0.95rem;
            margin-bottom: 12px;
        }
        .step-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(15, 23, 42, 0.6);
            border-left: 4px solid #48bb78;
            padding: 12px 18px;
            border-radius: 6px;
            margin-bottom: 10px;
            font-size: 0.92rem;
            color: #e2e8f0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-header-green">{t["title"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="blue-rank-card">
                <div class="table-title-blue">{t["tab_enterprise"]}</div>
                <table style="width:100%; text-align:center; color:#cbd5e1; border-collapse:collapse;">
                    <tr style="border-bottom:1px solid rgba(56,189,248,0.3); font-weight:700; color:#38bdf8;">
                        <th style="padding:10px;">{t["col_rank"]}</th>
                        <th style="padding:10px;">{t["col_enterprise"]}</th>
                        <th style="padding:10px;">{t["col_credits"]}</th>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:12px; font-weight:800; color:#38bdf8;">1</td><td>Vinamilk</td><td style="color:#48bb78; font-weight:700;">50,000</td></tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:12px; font-weight:800; color:#38bdf8;">2</td><td>FPT Software</td><td style="color:#48bb78; font-weight:700;">42,000</td></tr>
                    <tr><td style="padding:12px; font-weight:800; color:#38bdf8;">3</td><td>Vietcombank</td><td style="color:#48bb78; font-weight:700;">38,500</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="blue-rank-card">
                <div class="table-title-blue">{t["tab_project"]}</div>
                <table style="width:100%; text-align:center; color:#cbd5e1; border-collapse:collapse;">
                    <tr style="border-bottom:1px solid rgba(56,189,248,0.3); font-weight:700; color:#38bdf8;">
                        <th style="padding:10px;">{t["col_rank"]}</th>
                        <th style="padding:10px;">{t["col_project"]}</th>
                        <th style="padding:10px;">{t["col_co2"]}</th>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:12px; font-weight:800; color:#38bdf8;">1</td><td>{t["proj_1"]}</td><td style="color:#48bb78; font-weight:700;">1.2M</td></tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:12px; font-weight:800; color:#38bdf8;">2</td><td>{t["proj_2"]}</td><td style="color:#48bb78; font-weight:700;">850K</td></tr>
                    <tr><td style="padding:12px; font-weight:800; color:#38bdf8;">3</td><td>{t["proj_3"]}</td><td style="color:#48bb78; font-weight:700;">520K</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 0.5px solid rgba(72, 187, 120, 0.2); margin: 35px 0;'>", unsafe_allow_html=True)
    
    st.markdown(f'<div class="section-header-green">{t["process_title"]}</div>', unsafe_allow_html=True)

    user_role = st.session_state.get("current_role", "Doanh nghiệp mua tín chỉ")
    
    if "Doanh nghiệp" in user_role or "Enterprise" in user_role:
        cur_level = t["role_dn_1"]
        next_level = t["role_dn_2"]
        progress_val = 65
        levels_roadmap = [
            (t["dn_l1_name"], t["dn_l1_req"], t["reached"]),
            (t["dn_l2_name"], t["dn_l2_req"], f"{t['current']} (65%)"),
            (t["dn_l3_name"], t["dn_l3_req"], t["next_target"]),
            (t["dn_l4_name"], t["dn_l4_req"], t["locked"])
        ]
    elif "Chủ rừng" in user_role or "MRV" in user_role or "Forest" in user_role:
        cur_level = t["role_cr_1"]
        next_level = t["role_cr_2"]
        progress_val = 80
        levels_roadmap = [
            (t["cr_l1_name"], t["cr_l1_req"], t["reached"]),
            (t["cr_l2_name"], t["cr_l2_req"], f"{t['current']} (80%)"),
            (t["cr_l3_name"], t["cr_l3_req"], t["next_target"]),
            (t["cr_l4_name"], t["cr_l4_req"], t["locked"])
        ]
    else:
        cur_level = t["role_nd_1"]
        next_level = t["role_nd_2"]
        progress_val = 40
        levels_roadmap = [
            (t["nd_l1_name"], t["nd_l1_req"], t["reached"]),
            (t["nd_l2_name"], t["nd_l2_req"], f"{t['current']} (40%)"),
            (t["nd_l3_name"], t["nd_l3_req"], t["next_target"]),
            (t["nd_l4_name"], t["nd_l4_req"], t["locked"])
        ]

    with st.container(border=True):
        c_p1, c_p2 = st.columns([0.45, 0.55])
        with c_p1:
            st.markdown(f"""
                <div style="padding: 10px;">
                    <div style="color:#94a3b8; font-size:0.9rem; font-weight:600;">{t["current_lvl"]}:</div>
                    <div class="level-badge">{cur_level}</div>
                    <div style="color:#94a3b8; font-size:0.9rem; margin-top:10px;">{t["next_lvl"]} ({next_level}):</div>
                </div>
            """, unsafe_allow_html=True)
            st.progress(progress_val / 100.0)
            st.caption(f"{progress_val}% {t['progress_msg']}")

        with c_p2:
            st.markdown(f"<div style='color:#38bdf8; font-weight:700; margin-bottom:10px;'>{t['req_title']}:</div>", unsafe_allow_html=True)
            for lv_name, lv_req, lv_stt in levels_roadmap:
                status_color = "#48bb78" if t["reached"] in lv_stt else ("#38bdf8" if t["current"] in lv_stt else "#94a3b8")
                st.markdown(f"""
                    <div class="step-item">
                        <div>
                            <b style="color:#ffffff;">{lv_name}</b><br>
                            <span style="color:#94a3b8; font-size:0.85rem;">{lv_req}</span>
                        </div>
                        <div style="font-weight:800; font-size:0.82rem; color:{status_color}; white-space:nowrap; margin-left:15px;">
                            {lv_stt}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
