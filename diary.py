import streamlit as st
import calendar
import datetime

# Hộp thoại mở lên khi nhấn vào 1 ngày bất kỳ
@st.dialog("📝 GHI CHÉP NHẬT KÝ XANH")
def hop_thoai_ghi_chep(ngay_str):
    st.markdown(f"<h4 style='color: #48bb78; text-align: center; margin-bottom: 20px;'>Ngày: {ngay_str}</h4>", unsafe_allow_html=True)
    
    # Khởi tạo dữ liệu nếu chưa có
    if "green_diary" not in st.session_state:
        st.session_state["green_diary"] = {}
        
    data = st.session_state["green_diary"].get(ngay_str, {"title": "", "type": "Bình thường", "content": ""})
    
    with st.form(f"form_note_{ngay_str}", clear_on_submit=False):
        # Đánh dấu cờ marker để CSS nhắm trúng nút lưu trong form (tương tự phần Góp ý)
        st.markdown("<div class='form-diary-marker'></div>", unsafe_allow_html=True)
        
        title = st.text_input("Tiêu đề sự kiện:", value=data["title"], placeholder="VD: Đánh giá MRV tháng 10...")
        loai = st.selectbox("Phân loại mức độ:", ["Bình thường", "Quan trọng", "Hoàn thành"], 
                            index=["Bình thường", "Quan trọng", "Hoàn thành"].index(data["type"]) if data["type"] else 0)
        content = st.text_area("Nội dung chi tiết:", value=data["content"], height=100, placeholder="Ghi chú chi tiết cho ngày này...")
        
        if st.form_submit_button("💾 LƯU NHẬT KÝ", type="primary", use_container_width=True):
            if title.strip():
                st.session_state["green_diary"][ngay_str] = {"title": title, "type": loai, "content": content}
                st.success("Đã lưu ghi chép thành công!")
                st.rerun()
            else:
                st.error("Vui lòng nhập tiêu đề sự kiện để lưu!")

def hien_thi_nhat_ky_xanh():
    # Mock data ban đầu để hiển thị hiệu ứng
    if "green_diary" not in st.session_state:
        st.session_state["green_diary"] = {
            "2026-10-10": {"title": "Kỳ đánh giá sinh khối", "type": "Quan trọng", "content": "Rà soát lại dữ liệu trên nền tảng GEE."},
            "2026-10-15": {"title": "Mở bán chứng chỉ", "type": "Bình thường", "content": "Niêm yết tín chỉ đợt 2."}
        }

    st.markdown("""
    <style>
    .diary-title {
        font-size: 2.2rem; font-weight: 900; text-align: center; text-transform: uppercase;
        background: linear-gradient(to right, #48bb78, #63b3ed, #48bb78);
        background-size: 200% auto; color: #fff; background-clip: text;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: titleShine 4s linear infinite; margin-bottom: 20px; letter-spacing: 2px;
    }
    
    /* Đồng bộ khối ngày chuẩn (Glassmorphism) */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.day-marker) {
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.6), rgba(45, 55, 72, 0.6)) !important;
        border: 1px solid rgba(72, 187, 120, 0.2) !important;
        border-radius: 12px !important;
        padding: 10px !important;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        height: 100% !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.day-marker):hover {
        border-color: #48bb78 !important;
        box-shadow: 0 5px 15px rgba(72, 187, 120, 0.25) !important;
        transform: translateY(-3px);
    }

    /* Hiệu ứng chớp nháy đỏ cho sự kiện QUAN TRỌNG */
    @keyframes pulseImportant {
        0% { box-shadow: 0 0 0px rgba(239, 68, 68, 0.3); }
        50% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.7); border-color: #ef4444 !important; }
        100% { box-shadow: 0 0 0px rgba(239, 68, 68, 0.3); }
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.marker-Quan-trọng) {
        border: 1px solid rgba(239, 68, 68, 0.6) !important;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(26, 32, 44, 0.8)) !important;
        animation: pulseImportant 2.5s infinite;
    }
    
    /* Ngày BÌNH THƯỜNG (Xanh dương) */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.marker-Bình-thường) {
        border: 1px solid #4299e1 !important;
        background: linear-gradient(135deg, rgba(66, 153, 225, 0.15), rgba(26, 32, 44, 0.8)) !important;
    }

    /* Ngày HOÀN THÀNH (Xám) */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.marker-Hoàn-thành) {
        border: 1px solid #718096 !important; opacity: 0.6;
    }
    
    /* Đánh dấu ngày HÔM NAY */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.marker-today) {
        border: 2px solid #ecc94b !important;
        box-shadow: inset 0 0 15px rgba(236, 201, 75, 0.2) !important;
    }

    /* CSS cho chữ trong ô lịch */
    .cal-day-num { font-size: 1.6rem; font-weight: 900; color: #e2e8f0; margin-bottom: 2px; }
    .cal-event-title { font-size: 0.8rem; color: #a0aec0; height: 35px; overflow: hidden; margin-bottom: 5px; font-weight: 700; line-height: 1.2;}
    .day-header { font-weight: 900; text-align: center; color: #48bb78; padding-bottom: 10px; border-bottom: 1px solid rgba(72,187,120,0.3); margin-bottom: 15px;}
    
    /* Nút ghi chú nhỏ gọn */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.day-marker) button {
        background: transparent !important;
        border: 1px dashed rgba(255,255,255,0.2) !important;
        color: #a0aec0 !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.day-marker) button:hover {
        border-color: #48bb78 !important; color: white !important; background: rgba(72,187,120,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, c_mid, _ = st.columns([0.05, 0.9, 0.05])
    with c_mid:
        st.markdown('<div class="diary-title">📅 NHẬT KÝ XANH - LỊCH TRÌNH MRV</div>', unsafe_allow_html=True)
        
        # Bảng thông báo sự kiện quan trọng sắp tới
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")
        
        upcoming_events = [f"**{date}**: {data['title']}" for date, data in st.session_state["green_diary"].items() if data['type'] == "Quan trọng" and date >= today_str]
        if upcoming_events:
            with st.container(border=True):
                st.markdown("<h4 style='color:#fc8181; margin-bottom:10px; font-weight:800;'>🔔 Thông báo: Các sự kiện quan trọng sắp tới!</h4>", unsafe_allow_html=True)
                for ev in upcoming_events:
                    st.info(ev)
        
        st.markdown(f"<h3 style='text-align: center; color: #e2e8f0; margin-top: 25px; margin-bottom: 15px;'>Tháng {today.month} / {today.year}</h3>", unsafe_allow_html=True)

        # Header các thứ trong tuần
        days = ["THỨ 2", "THỨ 3", "THỨ 4", "THỨ 5", "THỨ 6", "THỨ 7", "CHỦ NHẬT"]
        cols = st.columns(7)
        for i, d in enumerate(days):
            cols[i].markdown(f"<div class='day-header'>{d}</div>", unsafe_allow_html=True)

        # Render lưới lịch
        cal = calendar.monthcalendar(today.year, today.month)
        
        for week in cal:
            w_cols = st.columns(7)
            for i, day in enumerate(week):
                with w_cols[i]:
                    if day != 0:
                        date_str = f"{today.year}-{today.month:02d}-{day:02d}"
                        event = st.session_state["green_diary"].get(date_str)
                        
                        # Gắn class CSS tương ứng
                        marker_class = "day-marker"
                        if date_str == today_str: marker_class += " marker-today"
                        if event: 
                            marker_type = event['type'].replace(' ', '-')
                            marker_class += f" marker-{marker_type}"
                        
                        with st.container(border=True):
                            # Thẻ div tàng hình để truyền class CSS cho container cha
                            st.markdown(f"<div class='{marker_class}' style='display:none;'></div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='cal-day-num'>{day}</div>", unsafe_allow_html=True)
                            
                            if event:
                                icon = "🔥" if event['type'] == "Quan trọng" else "📌" if event['type'] == "Bình thường" else "✅"
                                st.markdown(f"<div class='cal-event-title'>{icon} {event['title']}</div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div class='cal-event-title'></div>", unsafe_allow_html=True)
                            
                            if st.button("✏️", key=f"btn_note_{day}", use_container_width=True):
                                hop_thoai_ghi_chep(date_str)
                    else:
                        st.write("") # Khối rỗng cho những ngày không thuộc tháng
