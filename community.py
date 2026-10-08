import streamlit as st
from i18n import t

def hien_thi_vinh_danh_va_gop_y():
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

        /* HIỆU ỨNG THỞ PHÁT QUANG XANH DƯƠNG CHO 2 BẢNG XẾP HẠNG */
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

        /* KHỐI TIẾN TRÌNH SỐNG XANH */
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

    # Tiêu đề lớn màu xanh lá bao quát (Dịch tự động)
    st.markdown(f'<div class="section-header-green">{t("BẢNG VÀNG & TÔN VINH")}</div>', unsafe_allow_html=True)

    # 2 KHỐI XẾP HẠNG PHÁT QUANG XANH DƯƠNG VÀ NỔI LÊN KHI HOVER
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="blue-rank-card">
                <div class="table-title-blue">{t("TOP DOANH NGHIỆP")}</div>
                <table style="width:100%; text-align:center; color:#cbd5e1; border-collapse:collapse;">
                    <tr style="border-bottom:1px solid rgba(56,189,248,0.3); font-weight:700; color:#38bdf8;">
                        <th style="padding:10px;">{t("Hạng")}</th>
                        <th style="padding:10px;">{t("Doanh Nghiệp")}</th>
                        <th style="padding:10px;">{t("Tín chỉ")}</th>
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
                <div class="table-title-blue">{t("TOP DỰ ÁN TRỒNG RỪNG")}</div>
                <table style="width:100%; text-align:center; color:#cbd5e1; border-collapse:collapse;">
                    <tr style="border-bottom:1px solid rgba(56,189,248,0.3); font-weight:700; color:#38bdf8;">
                        <th style="padding:10px;">{t("Hạng")}</th>
                        <th style="padding:10px;">{t("Dự Án")}</th>
                        <th style="padding:10px;">CO2</th>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:12px; font-weight:800; color:#38bdf8;">1</td><td>{t("Rừng ngập mặn Cà Mau")}</td><td style="color:#48bb78; font-weight:700;">1.2M</td></tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:12px; font-weight:800; color:#38bdf8;">2</td><td>{t("Dự án Bắc Trung Bộ")}</td><td style="color:#48bb78; font-weight:700;">850K</td></tr>
                    <tr><td style="padding:12px; font-weight:800; color:#38bdf8;">3</td><td>{t("KBT Nam Cát Tiên")}</td><td style="color:#48bb78; font-weight:700;">520K</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 0.5px solid rgba(72, 187, 120, 0.2); margin: 35px 0;'>", unsafe_allow_html=True)
    
    # TIẾN TRÌNH SỐNG XANH - CẤP ĐỘ THEO TỪNG VAI TRÒ TÀI KHOẢN
    st.markdown(f'<div class="section-header-green">{t("QUÁ TRÌNH SỐNG XANH")}</div>', unsafe_allow_html=True)

    user_role = st.session_state.get("current_role", "Doanh nghiệp mua tín chỉ")
    
    # Thiết lập cấp độ và tiến trình dựa theo vai trò tài khoản
    if "Doanh nghiệp" in user_role:
        cur_level = t("Doanh nghiệp Tiên Phong Xanh")
        next_level = t("Đại Sứ Net-Zero")
        progress_val = 65
        levels_roadmap = [
            ("Cấp 1: Doanh nghiệp Khởi Động Xanh", "Bù trừ tối thiểu 1,000 Tấn CO2", "ĐÃ ĐẠT"),
            ("Cấp 2: Doanh nghiệp Tiên Phong Xanh", "Bù trừ từ 5,000 - 20,000 Tấn CO2", "HIỆN TẠI (65%)"),
            ("Cấp 3: Đại Sứ Net-Zero", "Bù trừ trên 50,000 Tấn CO2 & Đạt ESG Hạng A+", "MỤC TIÊU TIẾP THEO"),
            ("Cấp 4: Tập Đoàn Không Phát Thải", "Cam kết trung hòa carbon toàn chuỗi cung ứng", "KHÓA")
        ]
    elif "Chủ rừng" in user_role or "MRV" in user_role:
        cur_level = t("Kỹ Sư Kiến Tạo Sinh Khối")
        next_level = t("Đại Sứ Bảo Tồn Rừng")
        progress_val = 80
        levels_roadmap = [
            ("Cấp 1: Người Gieo Hạt Xanh", "Kiểm kê tối thiểu 100 Hecta qua viễn thám AI", "ĐÃ ĐẠT"),
            ("Cấp 2: Kỹ Sư Kiến Tạo Sinh Khối", "Duy trì sinh khối rừng tăng trưởng 3 năm liên tiếp", "HIỆN TẠI (80%)"),
            ("Cấp 3: Đại Sứ Bảo Tồn Rừng", "Bảo vệ trên 1,000 Hecta & Niêm yết thành công 100,000 Tín chỉ", "MỤC TIÊU TIẾP THEO"),
            ("Cấp 4: Thủ Lĩnh Đại Ngàn", "Bảo tồn hệ sinh thái rừng nguyên sinh quy mô quốc gia", "KHÓA")
        ]
    else:
        cur_level = t("Nhà Đầu Tư Sinh Thái Cấp 1")
        next_level = t("Cổ Đông Bảo Trợ Rừng Xanh")
        progress_val = 40
        levels_roadmap = [
            ("Cấp 1: Cổ Đông Hạt Giống", "Góp vốn vào 1 dự án sinh thái", "ĐÃ ĐẠT"),
            ("Cấp 2: Nhà Đầu Tư Sinh Thái Cấp 1", "Đầu tư trên $20,000 vào các dự án tín chỉ", "HIỆN TẠI (40%)"),
            ("Cấp 3: Cổ Đông Bảo Trợ Rừng Xanh", "Đầu tư trên $100,000 & Sở hữu chứng chỉ Verra", "MỤC TIÊU TIẾP THEO"),
            ("Cấp 4: Quỹ Đầu Tư Xanh Huyền Thoại", "Bảo lãnh tài chính cho chuỗi dự án quốc gia", "KHÓA")
        ]

    with st.container(border=True):
        c_p1, c_p2 = st.columns([0.45, 0.55])
        with c_p1:
            st.markdown(f"""
                <div style="padding: 10px;">
                    <div style="color:#94a3b8; font-size:0.9rem; font-weight:600;">{t("CẤP ĐỘ HIỆN TẠI")}:</div>
                    <div class="level-badge">{cur_level}</div>
                    <div style="color:#94a3b8; font-size:0.9rem; margin-top:10px;">{t("TIẾN TRÌNH LÊN CẤP KẾ TIẾP")} ({next_level}):</div>
                </div>
            """, unsafe_allow_html=True)
            st.progress(progress_val / 100.0)
            st.caption(f"{progress_val}% {t('hoàn thành chặng đường thăng hạng.')}")

        with c_p2:
            st.markdown(f"<div style='color:#38bdf8; font-weight:700; margin-bottom:10px;'>{t('YÊU CẦU ĐỂ THĂNG CẤP TIẾP THEO')}:</div>", unsafe_allow_html=True)
            for lv_name, lv_req, lv_stt in levels_roadmap:
                status_color = "#48bb78" if "ĐÃ ĐẠT" in lv_stt else ("#38bdf8" if "HIỆN TẠI" in lv_stt else "#94a3b8")
                st.markdown(f"""
                    <div class="step-item">
                        <div>
                            <b style="color:#ffffff;">{t(lv_name)}</b><br>
                            <span style="color:#94a3b8; font-size:0.85rem;">{t(lv_req)}</span>
                        </div>
                        <div style="font-weight:800; font-size:0.82rem; color:{status_color}; white-space:nowrap; margin-left:15px;">
                            {t(lv_stt)}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
