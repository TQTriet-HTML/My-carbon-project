import streamlit as st
import datetime
import calendar

# --- HỘP THOẠI ĐIỀN SỰ KIỆN CHO NGÀY ĐƯỢC CHỌN ---
@st.dialog("GHI NHẬN SỰ KIỆN / ADD EVENT", width="medium")
def hop_thoai_ghi_su_kien(ngay_chon, thang_chon, nam_chon, lang="Tiếng Việt"):
    st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(74, 222, 128, 0.45); border-left: 5px solid #4ade80; padding: 14px 18px; border-radius: 8px; margin-bottom: 16px;">
            <div style="color: #f8fafc; font-weight: 800; font-size: 1.05rem;">
                Ngày được chọn: <span style="color: #4ade80;">{ngay_chon:02d}/{thang_chon:02d}/{nam_chon}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    T = {
        "Tiếng Việt": {
            "event_title": "Tiêu đề sự kiện:",
            "event_type": "Phân loại sự kiện (Ô ngày sẽ đổi màu theo phân loại này):",
            "event_type_list": ["Quan trọng", "Bất thường", "Định kỳ"],
            "event_content": "Nội dung chi tiết:",
            "btn_save": "LƯU VÀO NHẬT KÝ",
            "msg_success": "Đã lưu sự kiện thành công.",
            "msg_warning": "Vui lòng điền tiêu đề sự kiện."
        },
        "English": {
            "event_title": "Event title:",
            "event_type": "Event type (Color-coded on calendar):",
            "event_type_list": ["Critical", "Abnormal", "Routine"],
            "event_content": "Detailed content:",
            "btn_save": "SAVE TO DIARY",
            "msg_success": "Event saved successfully.",
            "msg_warning": "Please enter an event title."
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

    e_title = st.text_input(t["event_title"])
    e_type = st.selectbox(t["event_type"], t["event_type_list"], index=2)
    e_content = st.text_area(t["event_content"], height=100)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button(t["btn_save"], type="primary", use_container_width=True):
        if e_title.strip():
            date_key = f"{nam_chon}-{thang_chon:02d}-{ngay_chon:02d}"
            
            if "diary_records" not in st.session_state:
                st.session_state["diary_records"] = {}
                
            st.session_state["diary_records"][date_key] = {
                "title": e_title,
                "type": e_type,
                "content": e_content
            }
            
            st.success(t["msg_success"])
            st.rerun()
        else:
            st.warning(t["msg_warning"])

def hien_thi_nhat_ky_xanh(lang="Tiếng Việt"):
    T = {
        "Tiếng Việt": {
            "title": "NHẬT KÝ XANH - LỊCH TRÌNH MRV",
            "month": "Tháng:",
            "year": "Năm (Phạm vi 10 năm):",
            "current_time": "Thời điểm hiện tại:",
            "legend_red": "Đỏ: Quan trọng",
            "legend_orange": "Cam: Bất thường",
            "legend_green": "Xanh: Định kỳ",
            "month_prefix": "THÁNG",
            "year_prefix": "NĂM",
            "days": ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"],
            "event_type_list": ["Quan trọng", "Bất thường", "Định kỳ"],
            "diary_list": "Danh sách nhật ký đã ghi:",
            "lbl_date": "Ngày",
            "lbl_class": "Phân loại",
            "no_detail": "Không có chi tiết"
        },
        "English": {
            "title": "GREEN DIARY - MRV SCHEDULE",
            "month": "Month:",
            "year": "Year (10-year range):",
            "current_time": "Current time:",
            "legend_red": "Red: Critical",
            "legend_orange": "Orange: Abnormal",
            "legend_green": "Green: Routine",
            "month_prefix": "MONTH",
            "year_prefix": "YEAR",
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "event_type_list": ["Critical", "Abnormal", "Routine"],
            "diary_list": "Recorded Diary List:",
            "lbl_date": "Date",
            "lbl_class": "Type",
            "no_detail": "No details provided"
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

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
        
        .info-box-diary {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(72,187,120,0.3);
            border-radius: 8px;
            padding: 10px 15px;
            margin-top: 25px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .cal-header {
            text-align: center;
            font-weight: 800;
            color: #94a3b8;
            font-size: 0.85rem;
            padding: 8px 0;
            text-transform: uppercase;
            margin-top: 15px;
            margin-bottom: 10px;
        }

        /* Tùy chỉnh nút ngày trong Lịch */
        div.stButton > button {
            width: 100% !important;
            height: 60px !important;
            background: rgba(30, 41, 59, 0.5) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            color: #f8fafc !important;
            font-weight: 800 !important;
            font-size: 1.1rem !important;
            border-radius: 10px !important;
            transition: all 0.25s ease !important;
        }
        div.stButton > button:hover {
            background: rgba(56, 189, 248, 0.15) !important;
            border-color: #38bdf8 !important;
            transform: translateY(-2px);
        }

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

    st.markdown(f'<div class="diary-title-green">{t["title"]}</div>', unsafe_allow_html=True)

    today = datetime.date.today()

    if "diary_records" not in st.session_state:
        st.session_state["diary_records"] = {
            "2026-10-15": {
                "title": "Phát hiện cháy rừng diện rộng" if lang=="Tiếng Việt" else "Widespread forest fire detected",
                "type": t["event_type_list"][1],
                "content": "Rừng ở khu vực tiểu khu 4 ghi nhận biến động sinh khối giảm sút đột ngột do hỏa hoạn." if lang=="Tiếng Việt" else "Forest in sub-zone 4 shows sudden biomass drop due to fire."
            },
            "2026-10-10": {
                "title": "Kỳ đánh giá sinh khối dự án" if lang=="Tiếng Việt" else "Project biomass assessment cycle",
                "type": t["event_type_list"][0],
                "content": "Tiến hành rà soát dữ liệu ảnh vệ tinh Sentinel-2 đồng bộ với kiểm kê thực địa." if lang=="Tiếng Việt" else "Reviewing Sentinel-2 satellite data in sync with field inventory."
            },
            "2026-10-01": {
                "title": "Báo cáo định kỳ tuần 1" if lang=="Tiếng Việt" else "Weekly routine report",
                "type": t["event_type_list"][2],
                "content": "Cập nhật số liệu tuần hoàn tín chỉ carbon cho các nhà đầu tư." if lang=="Tiếng Việt" else "Updating carbon credit circulation data for investors."
            }
        }

    col_nav1, col_nav2, col_info = st.columns([0.25, 0.25, 0.5])
    with col_nav1:
        sel_month = st.selectbox(t["month"], range(1, 13), index=today.month - 1)
    with col_nav2:
        year_range = list(range(today.year - 5, today.year + 6))
        sel_year = st.selectbox(t["year"], year_range, index=year_range.index(today.year))
    with col_info:
        st.markdown(f"""
            <div class="info-box-diary">
                <div style="font-size: 0.95rem; color: #94a3b8; margin-bottom: 6px;">
                    {t["current_time"]} <b style="color: #48bb78;">{today.strftime('%d/%m/%Y')}</b>
                </div>
                <div style="font-size: 0.9rem;">
                    <span style="color:#ef4444; font-weight:700;">{t["legend_red"]}</span> &bull; 
                    <span style="color:#f59e0b; font-weight:700;">{t["legend_orange"]}</span> &bull; 
                    <span style="color:#22c55e; font-weight:700;">{t["legend_green"]}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f"<div style='text-align:center; color:#ffffff; font-weight:800; font-size:1.25rem; margin-bottom: 20px; letter-spacing:1px;'>{t['month_prefix']} {sel_month} {t['year_prefix']} {sel_year}</div>", unsafe_allow_html=True)
        
        cols_header = st.columns(7)
        for i, w in enumerate(t["days"]):
            with cols_header[i]:
                st.markdown(f'<div class="cal-header">{w}</div>', unsafe_allow_html=True)

        cal = calendar.monthcalendar(sel_year, sel_month)
        records = st.session_state["diary_records"]

        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day != 0:
                        date_str = f"{sel_year}-{sel_month:02d}-{day:02d}"
                        
                        # Hack CSS để thay đổi viền, màu nền button dựa vào trạng thái
                        border_color = "rgba(255,255,255,0.05)"
                        bg_color = "rgba(30, 41, 59, 0.5)"
                        text_color = "#cbd5e1"
                        box_shadow = "none"
                        
                        if sel_year == today.year and sel_month == today.month and day == today.day:
                            border_color = "#38bdf8"
                            box_shadow = "0 0 10px rgba(56, 189, 248, 0.5)"
                            text_color = "#bae6fd"
                            
                        if date_str in records:
                            ev_type = records[date_str].get("type", t["event_type_list"][2])
                            if ev_type == t["event_type_list"][0]: # Đỏ: Quan trọng
                                border_color = "#ef4444"
                                bg_color = "rgba(239, 68, 68, 0.25)"
                                text_color = "#fca5a5"
                                box_shadow = "0 0 12px rgba(239, 68, 68, 0.4)"
                            elif ev_type == t["event_type_list"][1]: # Cam: Bất thường
                                border_color = "#f59e0b"
                                bg_color = "rgba(245, 158, 11, 0.25)"
                                text_color = "#fde68a"
                                box_shadow = "0 0 12px rgba(245, 158, 11, 0.4)"
                            else: # Xanh: Định kỳ
                                border_color = "#22c55e"
                                bg_color = "rgba(34, 197, 94, 0.25)"
                                text_color = "#86efac"
                                box_shadow = "0 0 12px rgba(34, 197, 94, 0.4)"
                        
                        st.markdown(f"""
                        <style>
                        div[data-testid="stVerticalBlock"] > div:has(button[key="btn_day_{day}"]) button {{
                            border: 2px solid {border_color} !important;
                            background: {bg_color} !important;
                            color: {text_color} !important;
                            box-shadow: {box_shadow} !important;
                        }}
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Khi nhấn vào ngày, hiện hộp thoại điền sự kiện
                        if st.button(str(day), key=f"btn_day_{day}", use_container_width=True):
                            hop_thoai_ghi_su_kien(day, sel_month, sel_year, lang)
                    else:
                        st.write("") 

    st.markdown(f'<div class="diary-sub-green">{t["diary_list"]}</div>', unsafe_allow_html=True)

    sorted_keys = sorted(records.keys(), reverse=True)
    for k in sorted_keys:
        item = records[k]
        ev_type = item.get("type", t["event_type_list"][2])
        
        if ev_type == t["event_type_list"][0]:
            box_cls = "event-box-important"
            type_color = "#ef4444"
        elif ev_type == t["event_type_list"][1]:
            box_cls = "event-box-abnormal"
            type_color = "#f59e0b"
        else:
            box_cls = "event-box-regular"
            type_color = "#22c55e"

        with st.expander(f"{t['lbl_date']} {k}: {item['title']} ({ev_type})"):
            st.markdown(f"""
                <div class="{box_cls}">
                    <div style="font-weight:800; font-size:1.05rem; color:{type_color}; margin-bottom:6px;">
                        {t['lbl_date']}: {k} | {t['lbl_class']}: {ev_type}
                    </div>
                    <div style="color:#ffffff; font-weight:700; font-size:1.1rem; margin-bottom:8px;">
                        {item['title']}
                    </div>
                    <div style="color:#cbd5e1; font-size:0.95rem; line-height:1.6;">
                        {item.get('content', t['no_detail'])}
                    </div>
                </div>
            """, unsafe_allow_html=True)
