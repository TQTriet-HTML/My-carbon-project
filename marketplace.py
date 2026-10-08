import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go

def hien_thi_san_giao_dich():
    # CSS hiệu ứng viền phát quang xanh lá + nổi bổng 3D cho toàn bộ container
    st.markdown("""
        <style>
        .dash-title-green {
            color: #48bb78 !important;
            font-size: clamp(24px, 2.6vw, 32px) !important;
            font-weight: 900 !important;
            text-align: center;
            letter-spacing: 1.5px;
            margin-bottom: 25px;
            text-transform: uppercase;
            text-shadow: 0 0 16px rgba(72, 187, 120, 0.4);
        }
        .dash-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 10px;
        }
        .dash-label {
            color: #94a3b8;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }
        .dash-value {
            color: #ffffff;
            font-size: clamp(1.8rem, 2.2vw, 2.4rem);
            font-weight: 900;
            line-height: 1.1;
            margin-bottom: 10px;
        }
        .dash-badge {
            display: inline-block;
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            background: rgba(72, 187, 120, 0.18);
            color: #48bb78;
            border: 1px solid rgba(72, 187, 120, 0.5);
        }

        /* HIỆU ỨNG THỞ VÀ NỔI KHỐI CHO TẤT CẢ CONTAINER CÓ VIỀN */
        @keyframes greenNeonGlowBreathe {
            0%, 100% {
                box-shadow: 0 0 16px rgba(72, 187, 120, 0.3), inset 0 0 12px rgba(72, 187, 120, 0.1);
                border-color: rgba(72, 187, 120, 0.5) !important;
            }
            50% {
                box-shadow: 0 0 38px rgba(72, 187, 120, 0.85), inset 0 0 20px rgba(72, 187, 120, 0.3);
                border-color: #48bb78 !important;
            }
        }

        @keyframes sweep10sMarket {
            0%, 85% { left: -120%; opacity: 0; }
            86% { opacity: 1; left: -120%; }
            95%, 100% { left: 220%; opacity: 0; }
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(135deg, rgba(13, 31, 60, 0.95), rgba(18, 42, 77, 0.92)) !important;
            border: 2px solid rgba(72, 187, 120, 0.55) !important;
            border-radius: 16px !important;
            padding: 22px !important;
            animation: greenNeonGlowBreathe 4s infinite ease-in-out !important;
            position: relative !important;
            overflow: hidden !important;
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.35s ease, border-color 0.35s ease !important;
            margin-bottom: 25px !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]::after {
            content: '';
            position: absolute;
            top: 0;
            left: -120%;
            width: 55%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.65), transparent);
            transform: skewX(-25deg);
            animation: sweep10sMarket 10s infinite linear;
            z-index: 10;
            pointer-events: none;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-8px) scale(1.018) !important;
            box-shadow: 0 22px 50px rgba(72, 187, 120, 0.92), inset 0 0 25px rgba(72, 187, 120, 0.4) !important;
            border-color: #48bb78 !important;
            z-index: 5 !important;
        }

        /* Nút xác nhận đặt lệnh màu xanh lá */
        button[kind="primary"] {
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
            border: 1.5px solid #4ade80 !important;
            color: white !important;
            font-weight: 800 !important;
            letter-spacing: 0.5px;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%) !important;
            box-shadow: 0 0 20px rgba(72, 187, 120, 0.8) !important;
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)

    # ================= 1. DASHBOARD QUẢN LÝ TÀI KHOẢN =================
    st.markdown('<div class="dash-title-green">DASHBOARD QUẢN LÝ TÀI KHOẢN</div>', unsafe_allow_html=True)

    wallet_bal = st.session_state.get("wallet_balance", 150000.0)
    current_u = st.session_state.get("current_user", "")
    current_role = st.session_state.get("current_role", "Doanh nghiệp mua tín chỉ")
    user_portfolios = st.session_state.get("user_portfolios", {})
    user_holdings = user_portfolios.get(current_u, [])
    total_tons = sum([item.get("volume", 0) for item in user_holdings]) if isinstance(user_holdings, list) else 0

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
                <div class="dash-card">
                    <div class="dash-label">Số Dư Ví Hệ Thống</div>
                    <div class="dash-value">${wallet_bal:,.2f}</div>
                    <div class="dash-badge">+ 50,000.00</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class="dash-card">
                    <div class="dash-label">Tổng Tín Chỉ Sở Hữu</div>
                    <div class="dash-value">{total_tons:,.0f} Tấn</div>
                    <div class="dash-badge">Đã bù trừ</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
                <div class="dash-card">
                    <div class="dash-label">Hạng Tín Nhiệm (ESG)</div>
                    <div class="dash-value">Hạng A+</div>
                    <div class="dash-badge">Đạt chuẩn</div>
                </div>
            """, unsafe_allow_html=True)
        
        with st.expander("XEM CHI TIẾT KHO TÍN CHỈ"):
            if user_holdings:
                for h in user_holdings:
                    st.write(f"- Dự án: **{h.get('project_name', 'Tín chỉ rừng')}** | Khối lượng: **{h.get('volume', 0):,.0f} Tấn** | Đơn giá: **${h.get('price', 10.5)}/Tấn**")
            else:
                st.write("Hiện tại tài khoản chưa nắm giữ tín chỉ nào. Bạn có thể đặt lệnh mua ở sàn bên dưới.")

    # ================= 2. BIỂU ĐỒ GIÁ TÍN CHỈ GIAO NGAY (TRỤC NGÀY NẰM NGANG) =================
    st.markdown('<div class="dash-title-green" style="margin-top: 35px;">BIỂU ĐỒ GIÁ TÍN CHỈ GIAO NGAY</div>', unsafe_allow_html=True)

    with st.container(border=True):
        col_view, col_stat = st.columns([0.45, 0.55])
        with col_view:
            time_frame = st.radio("Khung thời gian phân tích:", ["Từng ngày", "Từng tháng", "Từng năm"], horizontal=True)
        with col_stat:
            st.markdown("""
                <div style="text-align: right; padding-top: 5px;">
                    <span style="color: #94a3b8; font-size: 0.9rem;">Giá tham chiếu hiện tại: </span>
                    <b style="color: #48bb78; font-size: 1.4rem;">$10.50 / Tấn</b> 
                    <span style="color: #48bb78; font-weight:700; font-size: 0.9rem;">(+4.2% trong phiên)</span>
                </div>
            """, unsafe_allow_html=True)

        today = datetime.date.today()
        if time_frame == "Từng ngày":
            dates = [today - datetime.timedelta(days=i) for i in range(29, -1, -1)]
            date_labels = [d.strftime("%d/%m") for d in dates]
            base_p = 10.2
            noise = np.cumsum(np.random.normal(0.015, 0.12, len(dates)))
            prices = [round(max(8.0, base_p + n), 2) for n in noise]
        elif time_frame == "Từng tháng":
            date_labels = ["T11/25", "T12/25", "T01/26", "T02/26", "T03/26", "T04/26", "T05/26", "T06/26", "T07/26", "T08/26", "T09/26", "T10/26"]
            prices = [8.50, 8.80, 9.10, 8.95, 9.40, 9.65, 9.80, 10.10, 9.90, 10.25, 10.40, 10.50]
        else:
            date_labels = ["2021", "2022", "2023", "2024", "2025", "2026"]
            prices = [4.50, 5.80, 7.20, 8.90, 9.80, 10.50]

        # Biểu đồ Plotly chuyên nghiệp với trục hoành nằm ngang hoàn toàn (tickangle = 0)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=date_labels,
            y=prices,
            mode='lines',
            line=dict(color='#22c55e', width=2.5),
            fill='tozeroy',
            fillcolor='rgba(34, 197, 94, 0.08)',
            hovertemplate='Thời gian: %{x}<br>Giá: $%{y:.2f} USD<extra></extra>'
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=20, b=20),
            height=360,
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.05)',
                tickfont=dict(color='#94a3b8', size=12),
                tickangle=0,  # Ép chữ luôn nằm ngang hoàn toàn
                nticks=10,    # Chia khoảng đều đặn để chữ không bị đè lên nhau
                showline=True,
                linecolor='rgba(72, 187, 120, 0.3)'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.08)',
                tickfont=dict(color='#94a3b8', size=12),
                tickprefix='$',
                range=[max(0, min(prices) - 1.5), max(prices) + 1.5],
                showline=False
            ),
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # ================= 3. TRUNG TÂM KHỚP LỆNH THEO VAI TRÒ =================
    st.markdown('<div class="dash-title-green" style="margin-top: 35px;">TRUNG TÂM KHỚP LỆNH THEO VAI TRÒ</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f"<div style='color:#38bdf8; font-weight:800; font-size:1.15rem; margin-bottom:15px;'>VAI TRÒ HIỆN TẠI: {current_role.upper()}</div>", unsafe_allow_html=True)
        
        if "Doanh nghiệp" in current_role or "buyer" in current_u.lower():
            col_b1, col_b2 = st.columns([0.6, 0.4])
            with col_b1:
                st.markdown("<p style='color:#cbd5e1;'>Đặt lệnh mua tín chỉ bù trừ phát thải trực tiếp cho doanh nghiệp của bạn:</p>", unsafe_allow_html=True)
                proj_pick = st.selectbox("Chọn dự án muốn mua:", [
                    "Dự án Rừng ngập mặn Cà Mau ($10.50/tấn - Có sẵn 250,000 tấn)",
                    "Dự án Giảm phát thải Bắc Trung Bộ ($9.80/tấn - Có sẵn 180,000 tấn)",
                    "Dự án Bảo tồn Nam Cát Tiên ($11.20/tấn - Có sẵn 95,000 tấn)"
                ])
                buy_vol = st.number_input("Số lượng tín chỉ cần mua (Tấn CO2):", min_value=100, max_value=500000, value=1000, step=500)
                unit_price = 10.50 if "Cà Mau" in proj_pick else (9.80 if "Bắc Trung Bộ" in proj_pick else 11.20)
                total_cost = buy_vol * unit_price
            with col_b2:
                st.markdown(f"""
                    <div style='background:rgba(15,23,42,0.6); border:1px solid rgba(72,187,120,0.4); border-radius:10px; padding:18px; margin-top:20px;'>
                        <div style='color:#94a3b8; font-size:0.9rem;'>Đơn giá giao dịch: <b style='color:#ffffff;'>${unit_price:.2f} / Tấn</b></div>
                        <div style='color:#94a3b8; font-size:0.9rem; margin-top:8px;'>Tổng chi phí thanh toán:</div>
                        <div style='color:#48bb78; font-size:1.8rem; font-weight:900;'>${total_cost:,.2f}</div>
                        <div style='color:#cbd5e1; font-size:0.85rem; margin-top:6px;'>Quy đổi VND: {total_cost*26000:,.0f} VND</div>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                if st.button("XÁC NHẬN MUA TÍN CHỈ", type="primary", use_container_width=True):
                    if wallet_bal >= total_cost:
                        st.session_state["wallet_balance"] = wallet_bal - total_cost
                        if "user_portfolios" not in st.session_state: st.session_state["user_portfolios"] = {}
                        st.session_state["user_portfolios"].setdefault(current_u, []).append({
                            "project_name": proj_pick.split(" (")[0],
                            "volume": buy_vol,
                            "price": unit_price
                        })
                        st.success(f"Khớp lệnh thành công! Đã chuyển {buy_vol:,.0f} tấn tín chỉ vào kho lưu trữ của bạn.")
                        st.rerun()
                    else:
                        st.error("Số dư ví hệ thống không đủ để thực hiện giao dịch này.")

        elif "Chủ rừng" in current_role or "MRV" in current_role or "admin" in current_u.lower():
            st.markdown("<p style='color:#cbd5e1;'>Niêm yết tín chỉ mới từ diện tích rừng đã được đo đạc và xác thực bởi viễn thám AI:</p>", unsafe_allow_html=True)
            c_s1, c_s2 = st.columns(2)
            with c_s1:
                forest_name = st.text_input("Tên khu rừng / Dự án niêm yết:", value="Khu bảo tồn sinh thái Rừng Tràm")
                list_vol = st.number_input("Số lượng tín chỉ muốn mở bán (Tấn):", min_value=1000, value=25000, step=1000)
            with c_s2:
                ask_price = st.number_input("Giá niêm yết đề xuất ($/Tấn):", min_value=5.0, value=10.5, step=0.1)
                expected_rev = list_vol * ask_price
                st.markdown(f"""
                    <div style='background:rgba(15,23,42,0.6); border:1px solid rgba(72,187,120,0.4); border-radius:10px; padding:12px; margin-top:20px;'>
                        <span style='color:#94a3b8;'>Dự thu khi bán hết:</span>
                        <div style='color:#48bb78; font-size:1.5rem; font-weight:800;'>${expected_rev:,.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
            if st.button("NIÊM YẾT LÊN SÀN GIAO DỊCH", type="primary", use_container_width=True):
                st.success(f"Đã gửi hồ sơ niêm yết dự án '{forest_name}' với {list_vol:,.0f} tấn lên sàn giao dịch!")

        else:
            st.markdown("<p style='color:#cbd5e1;'>Thị trường thứ cấp: Giao dịch lướt sóng hoặc đầu tư ủy thác vào các dự án tín chỉ có tiềm năng tăng trưởng:</p>", unsafe_allow_html=True)
            ci1, ci2 = st.columns(2)
            with ci1:
                inv_proj = st.selectbox("Chọn dự án đầu tư:", ["Quỹ Tín chỉ Carbon Rừng Cà Mau", "Trái phiếu Xanh Bắc Trung Bộ"])
                inv_shares = st.number_input("Số vốn đầu tư ($):", min_value=1000.0, value=5000.0, step=500.0)
            with ci2:
                st.markdown("""
                    <div style='background:rgba(15,23,42,0.6); border:1px solid rgba(72,187,120,0.4); border-radius:10px; padding:15px; margin-top:25px;'>
                        <div style='color:#94a3b8;'>Lợi suất kỳ vọng hàng năm: <b style='color:#48bb78;'>14.5% / năm</b></div>
                        <div style='color:#94a3b8; margin-top:4px;'>Cơ chế bảo lãnh: Escrow Vietcombank</div>
                    </div>
                """, unsafe_allow_html=True)
            if st.button("XÁC NHẬN ĐẦU TƯ CỔ PHẦN RỪNG", type="primary", use_container_width=True):
                if wallet_bal >= inv_shares:
                    st.session_state["wallet_balance"] = wallet_bal - inv_shares
                    st.success(f"Đã đầu tư thành công ${inv_shares:,.2f} vào {inv_proj}!")
                    st.rerun()
                else:
                    st.error("Số dư ví không đủ.")

    # ================= 4. DANH SÁCH DỰ ÁN ĐANG NIÊM YẾT =================
    st.markdown('<div class="dash-title-green" style="margin-top: 35px;">DANH SÁCH DỰ ÁN ĐANG NIÊM YẾT</div>', unsafe_allow_html=True)

    projects_data = [
        {
            "name": "Dự án Rừng ngập mặn Cà Mau",
            "owner": "Sở NN&PTNT Tỉnh Cà Mau",
            "code": "CMR-2026-VCS",
            "volume": 250000,
            "price": 10.50,
            "desc": "Dự án phục hồi sinh khối đước vẹt phòng hộ ven biển, lưu trữ carbon xanh tầng đất ngập triều."
        },
        {
            "name": "Dự án Giảm phát thải Rừng Bắc Trung Bộ",
            "owner": "Ban Quản lý Rừng Phòng hộ Hà Tĩnh",
            "code": "BTB-2026-REDD",
            "volume": 180000,
            "price": 9.80,
            "desc": "Bảo tồn nghiêm ngặt rừng tự nhiên, kiểm kê viễn thám Sentinel-2 chu kỳ 10 ngày."
        },
        {
            "name": "Khu bảo tồn Đa dạng sinh học Nam Cát Tiên",
            "owner": "Vườn Quốc gia Nam Cát Tiên",
            "code": "NCT-2026-GS",
            "volume": 95000,
            "price": 11.20,
            "desc": "Tín chỉ chất lượng cao kết hợp chứng chỉ bảo tồn động vật hoang dã nguy cấp."
        }
    ]

    for p in projects_data:
        with st.container(border=True):
            col_info_p, col_action_p = st.columns([0.75, 0.25])
            with col_info_p:
                st.markdown(f"""
                    <div style='color:#48bb78; font-size:1.25rem; font-weight:800;'>{p['name']}</div>
                    <div style='color:#94a3b8; font-size:0.85rem; margin-top:2px;'>Đơn vị quản lý: {p['owner']} | Mã chuẩn hóa: {p['code']}</div>
                    <div style='color:#cbd5e1; font-size:0.95rem; margin-top:10px; line-height:1.5;'>{p['desc']}</div>
                """, unsafe_allow_html=True)
            with col_action_p:
                st.markdown(f"""
                    <div style='text-align:right;'>
                        <div style='color:#ffffff; font-size:1.5rem; font-weight:900;'>${p['price']:.2f} <span style='font-size:0.9rem; color:#94a3b8;'>/ Tấn</span></div>
                        <div style='color:#38bdf8; font-weight:700; font-size:0.9rem; margin-top:4px;'>Khả dụng: {p['volume']:,.0f} Tấn</div>
                    </div>
                """, unsafe_allow_html=True)

def hien_thi_cong_dau_tu():
    st.markdown("""
        <h2 style='color:#48bb78; text-align:center; font-weight:900; margin-bottom:25px;'>
            CỔNG ĐẦU TƯ TRỒNG RỪNG TỪ XA
        </h2>
    """, unsafe_allow_html=True)
    st.info("Danh mục đầu tư sinh thái đang mở nhận vốn kỳ 2026.")

def hien_thi_gioi_thieu_va_goi_von():
    st.markdown("""
        <style>
        .about-title-green {
            color: #48bb78 !important;
            font-size: clamp(24px, 2.7vw, 34px) !important;
            font-weight: 900 !important;
            text-align: center;
            letter-spacing: 1.5px;
            margin-bottom: 25px;
            text-transform: uppercase;
            text-shadow: 0 0 16px rgba(72, 187, 120, 0.4);
        }
        .about-section-title {
            color: #48bb78;
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
            border-left: 5px solid #48bb78;
            padding-left: 12px;
            text-transform: uppercase;
        }
        @keyframes greenCardBreath {
            0%, 100% {
                box-shadow: 0 0 15px rgba(72, 187, 120, 0.28), inset 0 0 12px rgba(72, 187, 120, 0.1);
                border-color: rgba(72, 187, 120, 0.5) !important;
            }
            50% {
                box-shadow: 0 0 38px rgba(72, 187, 120, 0.8), inset 0 0 22px rgba(72, 187, 120, 0.28);
                border-color: #48bb78 !important;
            }
        }
        @keyframes sweep10sAbout {
            0%, 85% { left: -120%; opacity: 0; }
            86% { opacity: 1; left: -120%; }
            95%, 100% { left: 220%; opacity: 0; }
        }
        .about-card-glow {
            background: linear-gradient(135deg, rgba(13, 31, 60, 0.95), rgba(18, 42, 77, 0.92)) !important;
            border: 2px solid rgba(72, 187, 120, 0.5) !important;
            border-radius: 16px !important;
            padding: 22px 24px !important;
            margin-bottom: 22px !important;
            line-height: 1.7 !important;
            color: #cbd5e1 !important;
            font-size: 0.98rem !important;
            position: relative !important;
            overflow: hidden !important;
            animation: greenCardBreath 4s infinite ease-in-out !important;
            transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.35s ease, border-color 0.35s ease !important;
        }
        .about-card-glow::after {
            content: '';
            position: absolute;
            top: 0;
            left: -120%;
            width: 55%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.65), transparent);
            transform: skewX(-25deg);
            animation: sweep10sAbout 10s infinite linear;
            z-index: 10;
            pointer-events: none;
        }
        .about-card-glow:hover {
            transform: translateY(-8px) scale(1.022) !important;
            box-shadow: 0 22px 50px rgba(72, 187, 120, 0.92), inset 0 0 25px rgba(72, 187, 120, 0.4) !important;
            border-color: #48bb78 !important;
            z-index: 5 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="about-title-green">VỀ CHÚNG TÔI & LỘ TRÌNH PHÁT TRIỂN</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-section-title">SỨ MỆNH & TẦM NHÌN</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="about-card-glow">
            Nền tảng được xây dựng với mục tiêu thương mại hóa và minh bạch hóa thị trường tín chỉ carbon tại Việt Nam. 
            Bằng cách kết hợp dữ liệu viễn thám vệ tinh đa quang phổ (Copernicus Sentinel-2) cùng mô hình trí tuệ nhân tạo (AI), 
            chúng tôi số hóa quy trình kiểm kê MRV (Measurement, Reporting, and Verification), xóa bỏ rào cản chi phí cao và 
            thời gian thẩm định kéo dài của các phương pháp thủ công truyền thống.
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="about-section-title">CÔNG NGHỆ LÕI </div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="about-card-glow" style="text-align:center; min-height:190px;">
                <div style="color:#38bdf8; font-size:1.15rem; font-weight:800; margin-bottom:8px;">Google Earth Engine</div>
                Xử lý dữ liệu không gian thời gian thực trên quy mô cấp tỉnh và toàn quốc với độ trễ cực thấp.
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="about-card-glow" style="text-align:center; min-height:190px;">
                <div style="color:#48bb78; font-size:1.15rem; font-weight:800; margin-bottom:8px;">AI Biomass Estimation</div>
                Thuật toán máy học tự động bóc tách chỉ số thực vật NDVI và tính toán độ che phủ sinh khối rừng.
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="about-card-glow" style="text-align:center; min-height:190px;">
                <div style="color:#f6e05e; font-size:1.15rem; font-weight:800; margin-bottom:8px;">Escrow Smart Matching</div>
                Cơ chế giao dịch ký quỹ tự động bảo đảm quyền lợi tài chính an toàn tuyệt đối cho người mua và chủ rừng.
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="about-section-title">LỘ TRÌNH PHÁT TRIỂN (ROADMAP 2026 - 2030)</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="about-card-glow">
            <div style="margin-bottom:6px;"><b style="color:#48bb78;">Giai đoạn 1 (2026):</b> Hoàn thiện hệ sinh thái kiểm kê tự động MRV, kết nối dữ liệu thí điểm các vùng rừng ngập mặn Cà Mau và rừng phòng hộ Bắc Trung Bộ.</div>
            <div style="margin-bottom:6px;"><b style="color:#48bb78;">Giai đoạn 2 (2027 - 2028):</b> Tích hợp sàn giao dịch thứ cấp cho các doanh nghiệp FDI, niêm yết chứng chỉ tiêu chuẩn Verra/Gold Standard.</div>
            <div><b style="color:#48bb78;">Giai đoạn 3 (2029 - 2030):</b> Mở rộng quy mô ra toàn khu vực Đông Nam Á, trở thành trung tâm giao dịch hạn ngạch phát thải hàng đầu.</div>
        </div>
    """, unsafe_allow_html=True)
