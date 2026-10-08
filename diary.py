import streamlit as st
import datetime
import calendar

def hien_thi_nhat_ky_xanh():
    st.markdown("""
        <style>
        .diary-title-green {
            color: #48bb78 !important;
            font-size: clamp(24px, 2.7vw, 34px) !important;
            font-weight: 900 !important;
            text-align: center;
            letter-spacing: 1.5px;
            margin-bottom: 22px;
            text-transform: uppercase;
            text-shadow: 0 0 15px rgba(72, 187, 120, 0.4);
        }
        .diary-sub-green {
            color: #48bb78 !important;
            font-weight: 800 !important;
            font-size: 1.25rem !important;
            margin: 25px 0 15px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* LƯỚI CUỐN LỊCH THÁNG */
        .cal-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
            margin-top: 15px;
        }
        .cal-header {
            text-align: center;
            font-weight: 800;
            color: #94a3b8;
            font-size: 0.85rem;
            padding: 8px 0;
            text-transform: uppercase;
        }
        .cal-day-cell {
            min-height: 58px;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.05rem;
            transition: all 0.25s ease;
            position: relative;
        }
        .cal-empty {
            background: transparent;
        }
        .cal-normal {
            background: rgba(30, 41, 59, 0.5);
            color: #cbd5e1;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .cal-today {
            outline: 2px solid #38bdf8;
            outline-offset: 1px;
        }
        /* MÀU SẮC Ô THEO PHÂN LOẠI SỰ KIỆN */
        .cal-event-important {
            background: rgba(239, 68, 68, 0.25) !important;
            color: #fca5a5 !important;
            border: 1.5px solid #ef4444 !important;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.4);
        }
        .cal-event-abnormal {
            background: rgba(245, 158, 11, 0.25) !important;
            color: #fde68a !important;
            border: 1.5px solid #f59e0b !important;
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.4);
        }
        .cal-event-regular {
            background: rgba(34, 197, 94, 0.25) !important;
            color: #86efac !important;
            border: 1.5px solid #22c55e !important;
            box-shadow: 0 0 12px rgba(34, 197, 94, 0.4);
        }

        /* CHI TIẾT SỰ KIỆN */
        .event-box-important {
            background: rgba(239, 68, 68, 0.12);
            border-left: 5px solid #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 12px;
        }
        .event-box-abnormal {
            background: rgba(245, 158, 11, 0.12);
            border-left: 5px solid #f59e0b;
            border: 1px solid rgba(245, 158, 11, 0.4);
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 12px;
        }
        .event-box-regular {
            background: rgba(34, 197, 94, 0.12);
            border-left: 5px solid #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.4);
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Tiêu đề lớn màu xanh lá (Không có icon)
    st.markdown('<div class="diary-title-green">NHẬT KÝ XANH - LỊCH TRÌNH MRV</div>', unsafe_allow_html=True)

    today = datetime.date.today()
    min_limit = today.replace(year=today.year - 5)
    max_limit = today.replace(year=today.year + 5)

    if "diary_records" not in st.session_state:
        st.session_state["diary_records"] = {
            "2026-10-15": {
                "title": "Phát hiện cháy rừng diện rộng",
                "type": "Bất thường",
                "content": "Rừng ở khu vực tiểu khu 4 ghi nhận biến động sinh khối giảm sút đột ngột do hỏa hoạn."
            },
            "2026-10-10": {
                "title": "Kỳ đánh giá sinh khối dự án",
                "type": "Quan trọng",
                "content": "Tiến hành rà soát dữ liệu ảnh vệ tinh Sentinel-2 đồng bộ với kiểm kê thực địa."
            },
            "2026-10-01": {
                "title": "Báo cáo định kỳ tuần 1",
                "type": "Định kỳ",
                "content": "Cập nhật số liệu tuần hoàn tín chỉ carbon cho các nhà đầu tư."
            }
        }

    # BỘ ĐIỀU HƯỚNG CUỐN LỊCH
    col_nav1, col_nav2, col_info = st.columns([0.25, 0.25, 0.5])
    with col_nav1:
        sel_month = st.selectbox("Tháng:", range(1, 13), index=today.month - 1)
    with col_nav2:
        year_range = list(range(today.year - 5, today.year + 6))
        sel_year = st.selectbox("Năm (Phạm vi 10 năm):", year_range, index=year_range.index(today.year))
    with col_info:
        st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(72,187,120,0.3); border-radius: 8px; padding: 10px 15px; margin-top: 25px; font-size: 0.9rem; color: #94a3b8;">
                Thời điểm hiện tại: <b style="color: #48bb78;">{today.strftime('%d/%m/%Y')}</b> &nbsp;|&nbsp;
                <span style="color:#ef4444; font-weight:700;">Đỏ: Quan trọng</span> &bull; 
                <span style="color:#f59e0b; font-weight:700;">Cam: Bất thường</span> &bull; 
                <span style="color:#22c55e; font-weight:700;">Xanh: Định kỳ</span>
            </div>
        """, unsafe_allow_html=True)

    # KHỐI HIỂN THỊ CUỐN LỊCH THÁNG
    with st.container(border=True):
        st.markdown(f"<div style='text-align:center; color:#ffffff; font-weight:800; font-size:1.15rem; letter-spacing:1px;'>THÁNG {sel_month} NĂM {sel_year}</div>", unsafe_allow_html=True)
        
        cal_html = '<div class="cal-grid">'
        weekdays = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
        for w in weekdays:
            cal_html += f'<div class="cal-header">{w}</div>'

        # Tính toán ma trận ngày trong tháng
        cal = calendar.monthcalendar(sel_year, sel_month)
        records = st.session_state["diary_records"]

        for week in cal:
            for day in week:
                if day == 0:
                    cal_html += '<div class="cal-day-cell cal-empty"></div>'
                else:
                    date_str = f"{sel_year}-{sel_month:02d}-{day:02d}"
                    cell_class = "cal-day-cell cal-normal"
                    
                    if date_str in records:
                        ev_type = records[date_str].get("type", "Định kỳ")
                        if ev_type == "Quan trọng":
                            cell_class += " cal-event-important"
                        elif ev_type == "Bất thường":
                            cell_class += " cal-event-abnormal"
                        else:
                            cell_class += " cal-event-regular"

                    if sel_year == today.year and sel_month == today.month and day == today.day:
                        cell_class += " cal-today"

                    cal_html += f'<div class="{cell_class}"><span>{day}</span></div>'

        cal_html += '</div>'
        st.markdown(cal_html, unsafe_allow_html=True)

    # BIỂU MẪU GHI NHẬT KÝ MỚI
    with st.expander("Ghi nhận sự kiện hoặc lịch trình mới", expanded=False):
        with st.form("form_add_diary", clear_on_submit=True):
            picked_date = st.date_input(
                "Chọn ngày sự kiện (Từ 5 năm trước đến 5 năm sau):",
                value=today,
                min_value=min_limit,
                max_value=max_limit
            )
            e_title = st.text_input("Tiêu đề sự kiện:")
            e_type = st.selectbox(
                "Phân loại sự kiện (Ô ngày sẽ tự động đổi màu theo phân loại này):",
                ["Quan trọng", "Bất thường", "Định kỳ"]
            )
            e_content = st.text_area("Nội dung chi tiết:")
            
            sub = st.form_submit_button("LƯU VÀO NHẬT KÝ", type="primary")
            if sub:
                if e_title.strip():
                    date_key = picked_date.strftime("%Y-%m-%d")
                    st.session_state["diary_records"][date_key] = {
                        "title": e_title,
                        "type": e_type,
                        "content": e_content
                    }
                    st.success(f"Đã lưu sự kiện ngày {picked_date.strftime('%d/%m/%Y')} thành công.")
                    st.rerun()
                else:
                    st.warning("Vui lòng điền tiêu đề sự kiện.")

    # DANH SÁCH CHI TIẾT CÁC NHẬT KÝ (Không dùng bất kỳ icon nào)
    st.markdown('<div class="diary-sub-green">Danh sách nhật ký đã ghi:</div>', unsafe_allow_html=True)

    sorted_keys = sorted(records.keys(), reverse=True)
    for k in sorted_keys:
        item = records[k]
        ev_type = item.get("type", "Định kỳ")
        
        if ev_type == "Quan trọng":
            box_cls = "event-box-important"
            type_color = "#ef4444"
        elif ev_type == "Bất thường":
            box_cls = "event-box-abnormal"
            type_color = "#f59e0b"
        else:
            box_cls = "event-box-regular"
            type_color = "#22c55e"

        # Hiển thị tiêu đề rõ ràng, không có icon
        with st.expander(f"Ngày {k}: {item['title']} ({ev_type})"):
            st.markdown(f"""
                <div class="{box_cls}">
                    <div style="font-weight:800; font-size:1.05rem; color:{type_color}; margin-bottom:6px;">
                        Ngày: {k} | Phân loại: {ev_type}
                    </div>
                    <div style="color:#ffffff; font-weight:700; font-size:1.1rem; margin-bottom:8px;">
                        {item['title']}
                    </div>
                    <div style="color:#cbd5e1; font-size:0.95rem; line-height:1.6;">
                        {item.get('content', 'Không có chi tiết')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
