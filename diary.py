import streamlit as st
import datetime
import db_manager

@st.dialog("📝 GHI CHÉP NHẬT KÝ XANH")
def hop_thoai_ghi_chep(ngay_str):
    st.markdown(f"<h4 style='color: #48bb78; text-align: center; margin-bottom: 20px;'>Ngày: {ngay_str}</h4>", unsafe_allow_html=True)
    
    current_diary = db_manager.load_green_diary()
    data = current_diary.get(ngay_str, {"title": "", "type": "Bình thường", "content": ""})
    
    with st.form(f"form_note_{ngay_str}", clear_on_submit=False):
        title = st.text_input("Tiêu đề sự kiện:", value=data["title"], placeholder="VD: Đánh giá MRV tháng 10...")
        loai = st.selectbox("Phân loại:", ["Bình thường", "Quan trọng", "Bất thường"], index=["Bình thường", "Quan trọng", "Bất thường"].index(data["type"]))
        content = st.text_area("Nội dung chi tiết:", value=data["content"], height=100, placeholder="Ghi chú chi tiết cho ngày này...")
        
        if st.form_submit_button("💾 LƯU NHẬT KÝ", type="primary", use_container_width=True):
            if title.strip():
                db_manager.save_diary_entry(ngay_str, title, loai, content)
                st.session_state["green_diary"] = db_manager.load_green_diary()
                st.success("Đã lưu ghi chép thành công!")
                st.rerun()
            else:
                st.error("Vui lòng nhập tiêu đề sự kiện để lưu!")

def hien_thi_nhat_ky_xanh():
    if "green_diary" not in st.session_state:
        st.session_state["green_diary"] = db_manager.load_green_diary()

    if "view_date" not in st.session_state:
        st.session_state["view_date"] = datetime.date.today()

    _, c_mid, _ = st.columns([0.05, 0.9, 0.05])
    with c_mid:
        st.markdown('<h3 style="color:#48bb78; text-align:center;">📅 NHẬT KÝ XANH - LỊCH TRÌNH MRV</h3>', unsafe_allow_html=True)
        
        # Form nhập nhanh cho ngày hôm nay
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        st.info(f"Hôm nay: {today_str}")
        
        if st.button("📝 Thêm nhật ký cho ngày hôm nay", type="primary"):
            hop_thoai_ghi_chep(today_str)
            
        st.divider()
        st.markdown("#### Danh sách nhật ký đã ghi:")
        diary_data = db_manager.load_green_diary()
        if diary_data:
            for d_str, info in sorted(diary_data.items(), reverse=True):
                with st.expander(f"📌 {d_str}: {info['title']} ({info['type']})"):
                    st.write(info['content'])
                    if st.button("Sửa ghi chép này", key=f"edit_{d_str}"):
                        hop_thoai_ghi_chep(d_str)
        else:
            st.write("Chưa có ghi chép nhật ký nào.")
