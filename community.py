import streamlit as st
import pandas as pd

def hien_thi_vinh_danh_va_gop_y():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    
    # --- DANH SÁCH 10 CẤP ĐỘ THEO VAI TRÒ ---
    LEVELS = {
        "Doanh nghiệp mua tín chỉ": ["Thành viên Mới", "Khởi đầu Xanh", "Nhận thức Carbon", "Hành động Giảm phát", "Đối tác Môi trường", "Tích cực Bù trừ", "Doanh nghiệp Xanh", "Dẫn đầu Bền vững", "Tiên phong Net-Zero", "Đại sứ Net-Zero"],
        "Chủ rừng / Kỹ sư MRV": ["Thành viên Mới", "Hạt giống Sinh thái", "Ươm mầm Xanh", "Bảo vệ Nguyên sinh", "Quản lý Sinh khối", "Chuyên gia MRV", "Đối tác Tín chỉ", "Vệ sĩ Rừng thẳm", "Biểu tượng Bảo tồn", "Vệ thần Trái Đất"],
        "Nhà đầu tư từ xa (Cổ đông)": ["Thành viên Mới", "Góp vốn Xanh", "Hỗ trợ Sinh thái", "Nhà đầu tư Bền vững", "Đối tác Chiến lược", "Quỹ Môi trường", "Tầm nhìn Net-Zero", "Thiên thần Xanh", "Dẫn dắt Thị trường", "Tỷ phú Sinh thái"]
    }

    _, c_mid, _ = st.columns([0.05, 0.9, 0.05])
    with c_mid:
        st.markdown("<h3 style='color: white; text-align: center; font-weight:800;'>BẢNG VÀNG & TÔN VINH</h3>" if lang=="Tiếng Việt" else "<h3 style='color: white; text-align: center; font-weight:800;'>LEADERBOARD & HALL OF FAME</h3>", unsafe_allow_html=True)
        
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            with st.container(border=True):
                st.markdown("<h4 style='color:#48bb78; text-align:center;'>TOP DOANH NGHIỆP</h4>" if lang=="Tiếng Việt" else "<h4 style='color:#48bb78; text-align:center;'>TOP BUYERS</h4>", unsafe_allow_html=True)
                df_buy = pd.DataFrame({
                    "Hạng" if lang=="Tiếng Việt" else "Rank": ["1", "2", "3"],
                    "Doanh Nghiệp" if lang=="Tiếng Việt" else "Company": ["Vinamilk", "FPT Software", "Vietcombank"],
                    "Tín chỉ" if lang=="Tiếng Việt" else "Credits": ["50,000", "42,000", "38,500"]
                })
                st.dataframe(df_buy, hide_index=True, use_container_width=True)
            
        with c_b2:
            with st.container(border=True):
                st.markdown("<h4 style='color:#48bb78; text-align:center;'>TOP DỰ ÁN TRỒNG RỪNG</h4>" if lang=="Tiếng Việt" else "<h4 style='color:#48bb78; text-align:center;'>TOP PROJECTS</h4>", unsafe_allow_html=True)
                df_for = pd.DataFrame({
                    "Hạng" if lang=="Tiếng Việt" else "Rank": ["1", "2", "3"],
                    "Dự Án" if lang=="Tiếng Việt" else "Project": ["Rừng ngập mặn Cà Mau", "Dự án Bắc Trung Bộ", "KBT Nam Cát Tiên"],
                    "CO2" : ["1.2M", "850K", "520K"]
                })
                st.dataframe(df_for, hide_index=True, use_container_width=True)

        st.divider()
        st.markdown("<h3 style='color: white; text-align: center; font-weight:800;'>QUÁ TRÌNH SỐNG XANH</h3>" if lang=="Tiếng Việt" else "<h3 style='color: white; text-align: center; font-weight:800;'>GREEN LIVING PROGRESS</h3>", unsafe_allow_html=True)
        
        user = st.session_state.get('current_user', 'Guest')
        role = st.session_state.get('current_role', 'Doanh nghiệp mua tín chỉ')
        
        # Mô phỏng level hiện tại (Level 4)
        current_level = 4
        level_name = LEVELS.get(role, LEVELS["Doanh nghiệp mua tín chỉ"])[current_level - 1]
        
        with st.container(border=True):
            st.markdown(f"""
                <div style="text-align:center; padding: 10px;">
                    <h2 style="color: #63b3ed; margin:0;">{user}</h2>
                    <p style="color: #a0aec0; font-size: 1rem; margin-top:5px; margin-bottom: 20px;">{role}</p>
                    <div style="margin-bottom: 15px;">
                        <span style="background: rgba(72,187,120,0.2); border: 1px solid #48bb78; color: #48bb78; padding: 8px 20px; border-radius: 20px; font-weight: 800; font-size: 1.1rem; text-transform:uppercase;">Cấp {current_level}: {level_name}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.progress(current_level * 10)
            st.markdown(f"<p style='text-align:right; color:#a0aec0; font-size:0.85rem; margin-top:5px;'>{'Hoàn thành 40% chặng đường' if lang=='Tiếng Việt' else '40% Journey Completed'}</p>", unsafe_allow_html=True)

            with st.expander("XEM LỘ TRÌNH 10 CẤP ĐỘ DANH HIỆU" if lang=="Tiếng Việt" else "VIEW 10-LEVEL TITLE ROADMAP"):
                all_levels = LEVELS.get(role, LEVELS["Doanh nghiệp mua tín chỉ"])
                html_list = "<ul style='color:#cbd5e0; line-height:2; list-style-type:square;'>"
                for idx, lvl in enumerate(all_levels):
                    if idx + 1 == current_level:
                        html_list += f"<li style='color:#48bb78; font-weight:bold; font-size:1.1rem;'>Cấp {idx+1}: {lvl} (Hiện tại)</li>"
                    else:
                        html_list += f"<li>Cấp {idx+1}: {lvl}</li>"
                html_list += "</ul>"
                st.markdown(html_list, unsafe_allow_html=True)
