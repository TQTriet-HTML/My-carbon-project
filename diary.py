import streamlit as st
import datetime

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
        /* Hộp sự kiện theo màu phân loại */
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

    # Tiêu đề lớn KHÔNG CÒN ICON LỊCH, màu xanh lá bao hàm
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

    c_today, c_btn = st.columns([0.65, 0.35])
    with c_today:
        st.info(f"Hôm nay: {today.strftime('%d/%m/%Y')} (Phạm vi lịch trình: {min_limit.year} - {max_limit.year})")

    # Form thêm nhật ký với ngày chọn trong phạm vi 5 năm
    with st.expander("Ghi nhận nhật ký hoặc lịch trình mới", expanded=False):
        with st.form("form_add_diary", clear_on_submit=True):
            picked_date = st.date_input(
                "Chọn ngày sự kiện (Hỗ trợ 5 năm trước đến 5 năm sau):",
                value=today,
                min_value=min_limit,
                max_value=max_limit
            )
            e_title = st.text_input("Tiêu đề sự kiện:")
            e_type = st.selectbox(
                "Phân loại sự kiện (Ô ghi chú sẽ đổi màu theo phân loại này):",
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

    st.markdown('<div class="diary-sub-green">Danh sách nhật ký đã ghi:</div>', unsafe_allow_html=True)

    records = st.session_state["diary_records"]
    # Sắp xếp theo ngày giảm dần
    sorted_keys = sorted(records.keys(), reverse=True)

    for k in sorted_keys:
        item = records[k]
        ev_type = item.get("type", "Định kỳ")
        
        # Chọn màu sắc theo phân loại
        if ev_type == "Quan trọng":
            box_cls = "event-box-important"
            type_color = "#ef4444"
        elif ev_type == "Bất thường":
            box_cls = "event-box-abnormal"
            type_color = "#f59e0b"
        else:
            box_cls = "event-box-regular"
            type_color = "#22c55e"

        # Giữ nguyên biểu tượng ghim
        with st.expander(f"📌 {k}: {item['title']} ({ev_type})"):
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
