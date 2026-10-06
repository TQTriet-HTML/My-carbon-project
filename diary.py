import streamlit as st
import calendar
import datetime

# Hộp thoại mở lên khi nhấn vào 1 ngày bất kỳ
@st.dialog("📝 GHI CHÉP NHẬT KÝ XANH")
def hop_thoai_ghi_chep(ngay_str):
    st.markdown(f"<h4 style='color: #48bb78; text-align: center; margin-bottom: 20px;'>Ngày: {ngay_str}</h4>", unsafe_allow_html=True)
    
    if "green_diary" not in st.session_state:
        st.session_state["green_diary"] = {}
        
    data = st.session_state["green_diary"].get(ngay_str, {"title": "", "type": "Bình thường", "content": ""})
    
    with st.form(f"form_note_{ngay_str}", clear_on_submit=False):
        st.markdown("<div class='form-diary-marker'></div>", unsafe_allow_html=True)
        
        title = st.text_input("Tiêu đề sự kiện:", value=data["title"], placeholder="VD: Đánh giá MRV tháng 10...")
        
        # Thêm mục Bất thường vào phân loại
        danh_sach_loai = ["Bình thường", "Quan trọng", "Bất thường", "Hoàn thành"]
        chi_muc = danh_sach_loai.index(data["type"]) if data.get("type") in danh_sach_loai else 0
        loai = st.selectbox("Phân loại mức độ:", danh_sach_loai, index=chi_muc)
        
        content = st.text_area("Nội dung chi tiết:", value=data["content"], height=100, placeholder="Ghi chú chi tiết cho ngày này...")
        
        if st.form_submit_button("💾 LƯU NHẬT KÝ", type="primary", use_container_width=True):
            if title.strip():
                st.session_state["green_diary"][ngay_str] = {"title": title, "type": loai, "content": content}
                st.success("Đã lưu ghi chép thành công!")
                st.rerun()
            else:
                st.error("Vui lòng nhập tiêu đề sự kiện để lưu!")

def hien_thi_nhat_ky_xanh():
    # Khởi tạo dữ liệu mẫu nếu chưa có
    if "green_diary" not in st.session_state:
        st.session_state["green_diary"] = {
            "2026-10-10": {"title": "Kỳ đánh giá sinh khối dự án", "type": "Quan trọng", "content": "Rà soát lại dữ liệu trên nền tảng GEE."},
            "2026-10-15": {"title": "Phát hiện cháy rừng diện rộng", "type": "Bất thường", "content": "Rừng ở khu vực B bị suy giảm sinh khối."},
            "2026-10-22": {"title": "Mở bán chứng chỉ đợt 2", "type": "Bình thường", "content": "Niêm yết tín chỉ đợt 2."}
        }

    # Khởi tạo trạng thái điều hướng tháng (Giới hạn 10/2026 đến 10/2031)
    if "nav_year" not in st.session_state: st.session_state["nav_year"] = 2026
    if "nav_month" not in st.session_state: st.session_state["nav_month"] = 10

    st.markdown("""
    <style>
    .diary-title {
        font-size: 2.2rem; font-weight: 900; text-align: center; text-transform: uppercase;
        background: linear-gradient(to right, #48bb78, #63b3ed, #48bb78);
        background-size: 200% auto; color: #fff; background-clip: text;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: titleShine 4s linear infinite; margin-bottom: 30px; letter-spacing: 2px;
    }
    
    /* =========================================
       KHỐI THÔNG BÁO XANH DƯƠNG TƯƠNG TÁC
       ========================================= */
    .noti-block {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.4), rgba(49, 130, 206, 0.2));
        border: 2px solid #3182ce;
        border-left: 8px solid #63b3ed;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        transition: all 0.4s ease;
        box-shadow: 0 5px 15px rgba(49, 130, 206, 0.2);
    }
    .noti-block:hover {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.6), rgba(49, 130, 206, 0.4));
        box-shadow: 0 10px 30px rgba(49, 130, 206, 0.6), inset 0 0 15px rgba(99, 179, 237, 0.3);
        transform: translateY(-4px) scale(1.01);
        border-color: #63b3ed;
    }
    .noti-title { color: #90cdf4; font-size: 1.2rem; font-weight: 900; margin-bottom: 15px; letter-spacing: 1px; text-transform: uppercase; }
    .noti-item { color: #e2e8f0; font-size: 0.95rem; margin-bottom: 8px; padding-left: 10px; border-left: 2px solid rgba(255,255,255,0.2); }
    .noti-item b { color: #63b3ed; }

    /* =========================================
       KHỐI THÁNG XANH DƯƠNG LÓA SÁNG
       ========================================= */
    @keyframes blueGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(49, 130, 206, 0.4), inset 0 0 10px rgba(49, 130, 206, 0.1); border-color: rgba(49, 130, 206, 0.6); }
        50% { box-shadow: 0 0 35px rgba(49, 130, 206, 0.9), inset 0 0 20px rgba(49, 130, 206, 0.4); border-color: rgba(99, 179, 237, 1); }
    }
    .month-header-block {
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.9), rgba(45, 55, 72, 0.9));
        border: 2px solid #3182ce;
        border-radius: 16px;
        padding: 12px;
        text-align: center;
        transition: all 0.4s ease;
        margin-bottom: 25px;
    }
    .month-header-block:hover {
        animation: blueGlow 3s infinite ease-in-out;
        transform: translateY(-5px);
    }
    .month-header-text { color: #90cdf4; font-size: 1.6rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 2px; }

    /* =========================================
       CSS CHO LƯỚI LỊCH
       ========================================= */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.day-marker) {
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.6), rgba(45, 55, 72, 0.6)) !important;
        border: 1px solid rgba(72, 187, 120, 0.2) !important;
        border-radius: 12px !important;
        padding: 10px !important;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        height: 140px !important; /* Cố định chiều cao để không bị lệch */
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.day-marker):hover {
        border-color: #48bb78 !important; box-shadow: 0 5px 15px rgba(72, 187, 120, 0.25) !important; transform: translateY(-3px);
    }

    /* Đánh dấu Quan trọng (Đỏ) */
    @keyframes pulseImportant {
        0% { box-shadow: 0 0 0px rgba(239, 68, 68, 0.3); }
        50% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.7); border-color: #ef4444 !important; }
        100% { box-shadow: 0 0 0px rgba(239, 68, 68, 0.3); }
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.marker-Quan-trọng) {
        border: 1px solid rgba(239, 68, 68, 0.6) !important; background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(26, 32, 44, 0.8)) !important;
        animation: pulseImportant 2.5s infinite;
    }
    
    /* Đánh dấu Bất thường (Vàng/Cam chớp nhanh) */
    @keyframes pulseAbnormal {
        0% { box-shadow: 0 0 0px rgba(221, 107, 32, 0.4); }
        50% { box-shadow: 0 0 25px rgba(221, 107, 32, 0.9); border-color: #dd6b20 !important; }
        100% { box-shadow: 0 0 0px rgba(221, 107, 32, 0.4); }
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.marker-Bất-thường) {
        border: 1px solid rgba(221, 107, 32, 0.8) !important; background: linear-gradient(135deg, rgba(221, 107, 32, 0.2), rgba(26, 32, 44, 0.8)) !important;
        animation: pulseAbnormal 1s infinite;
    }

    /* Bình thường (Xanh lam) */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.marker-Bình-thường) { border: 1px solid #4299e1 !important; background: linear-gradient(135deg, rgba(66, 153, 225, 0.15), rgba(26, 32, 44, 0.8)) !important; }
    
    /* Hoàn thành (Xám) */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.marker-Hoàn-thành) { border: 1px solid #718096 !important; opacity: 0.6; }
    
    /* Hôm nay */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.marker-today) { border: 2px solid #ecc94b !important; box-shadow: inset 0 0 15px rgba(236, 201, 75, 0.2) !important; }

    .cal-day-num { font-size: 1.6rem; font-weight: 900; color: #e2e8f0; margin-bottom: 2px; }
    .cal-event-title { font-size: 0.75rem; color: #a0aec0; height: 35px; overflow: hidden; margin-bottom: 5px; font-weight: 700; line-height: 1.3;}
    .day-header { font-weight: 900; text-align: center; color: #48bb78; padding-bottom: 10px; border-bottom: 1px solid rgba(72,187,120,0.3); margin-bottom: 15px;}
    
    /* =========================================
       NÚT GHI CHÚ MÀU XANH LÁ
       ========================================= */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.day-marker) button {
        background: linear-gradient(135deg, #2f855a 0%, #276749 100%) !important;
        border: 1px solid #48bb78 !important;
        color: white !important;
        border-radius: 6px !important;
        transition: all 0.3s ease !important;
        padding: 5px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.day-marker) button:hover {
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important;
        box-shadow: 0 0 15px rgba(72,187,120,0.6) !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

    _, c_mid, _ = st.columns([0.05, 0.9, 0.05])
    with c_mid:
        st.markdown('<div class="diary-title">📅 NHẬT KÝ XANH - LỊCH TRÌNH MRV</div>', unsafe_allow_html=True)
        
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        
        # BẢNG THÔNG BÁO TƯƠNG TÁC (Chỉ hiện sự kiện Quan trọng / Bất thường sắp tới)
        events_html = ""
        for date, data in st.session_state["green_diary"].items():
            if data['type'] in ["Quan trọng", "Bất thường"] and date >= today_str:
                icon_noti = "🚨" if data['type'] == "Bất thường" else "🔥"
                color_noti = "#dd6b20" if data['type'] == "Bất thường" else "#fc8181"
                events_html += f"<div class='noti-item' style='color: {color_noti};'>{icon_noti} <b>{date}</b>: {data['title']}</div>"
        
        if events_html:
            st.markdown(f"""
            <div class='noti-block'>
                <div class='noti-title'>🔔 THÔNG BÁO: CÁC SỰ KIỆN NỔI BẬT SẮP TỚI!</div>
                {events_html}
            </div>
            """, unsafe_allow_html=True)

        # NÚT ĐIỀU HƯỚNG THÁNG & KHỐI THÁNG XANH DƯƠNG
        col_btn_l, col_month, col_btn_r = st.columns([1, 2, 1])
        
        with col_btn_l:
            st.write("") # Dóng hàng
            disable_prev = (st.session_state["nav_year"] <= 2026 and st.session_state["nav_month"] <= 10)
            if st.button("◀ THÁNG TRƯỚC", use_container_width=True, disabled=disable_prev):
                st.session_state["nav_month"] -= 1
                if st.session_state["nav_month"] < 1:
                    st.session_state["nav_month"] = 12
                    st.session_state["nav_year"] -= 1
                st.rerun()
                
        with col_btn_r:
            st.write("") # Dóng hàng
            disable_next = (st.session_state["nav_year"] >= 2031 and st.session_state["nav_month"] >= 10)
            if st.button("THÁNG SAU ▶", use_container_width=True, disabled=disable_next):
                st.session_state["nav_month"] += 1
                if st.session_state["nav_month"] > 12:
                    st.session_state["nav_month"] = 1
                    st.session_state["nav_year"] += 1
                st.rerun()
                
        with col_month:
            st.markdown(f"""
            <div class='month-header-block'>
                <h3 class='month-header-text'>Tháng {st.session_state['nav_month']} / {st.session_state['nav_year']}</h3>
            </div>
            """, unsafe_allow_html=True)

        # HEADER CÁC THỨ TRONG TUẦN
        days = ["THỨ 2", "THỨ 3", "THỨ 4", "THỨ 5", "THỨ 6", "THỨ 7", "CHỦ NHẬT"]
        cols = st.columns(7)
        for i, d in enumerate(days):
            cols[i].markdown(f"<div class='day-header'>{d}</div>", unsafe_allow_html=True)

        # LƯỚI LỊCH
        cal = calendar.monthcalendar(st.session_state["nav_year"], st.session_state["nav_month"])
        
        for week in cal:
            w_cols = st.columns(7)
            for i, day in enumerate(week):
                with w_cols[i]:
                    if day != 0:
                        date_str = f"{st.session_state['nav_year']}-{st.session_state['nav_month']:02d}-{day:02d}"
                        event = st.session_state["green_diary"].get(date_str)
                        
                        marker_class = "day-marker"
                        if date_str == today_str: marker_class += " marker-today"
                        if event: 
                            marker_type = event['type'].replace(' ', '-')
                            marker_class += f" marker-{marker_type}"
                        
                        with st.container(border=True):
                            st.markdown(f"<div class='{marker_class}' style='display:none;'></div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='cal-day-num'>{day}</div>", unsafe_allow_html=True)
                            
                            # GIỚI HẠN KÝ TỰ (30 chars) VÀ KÝ HIỆU ICON
                            if event:
                                icon = "🚨" if event['type'] == "Bất thường" else "🔥" if event['type'] == "Quan trọng" else "📌" if event['type'] == "Bình thường" else "✅"
                                
                                raw_title = event['title']
                                short_title = raw_title if len(raw_title) <= 30 else raw_title[:27] + "..."
                                
                                st.markdown(f"<div class='cal-event-title'>{icon} {short_title}</div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div class='cal-event-title'></div>", unsafe_allow_html=True)
                            
                            if st.button("✏️️", key=f"btn_note_{date_str}", use_container_width=True):
                                hop_thoai_ghi_chep(date_str)
                    else:
                        st.write("") # Khối rỗng cho ngày ngoài tháng
