import streamlit as st
import pandas as pd

def hien_thi_vinh_danh_va_gop_y():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    
    st.markdown("## 🏆 Bảng Vàng & Tôn Vinh" if lang=="Tiếng Việt" else "## 🏆 Leaderboard & Hall of Fame")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown("### 🏢 Top Doanh Nghiệp" if lang=="Tiếng Việt" else "### 🏢 Top Corporate Buyers")
        df_buy = pd.DataFrame({
            "Hạng" if lang=="Tiếng Việt" else "Rank": ["🥇 1", "🥈 2", "🥉 3"],
            "Doanh Nghiệp" if lang=="Tiếng Việt" else "Company": ["Vinamilk", "FPT Software", "Vietcombank"],
            "Tín chỉ" if lang=="Tiếng Việt" else "Credits": ["50,000", "42,000", "38,500"]
        })
        st.dataframe(df_buy, hide_index=True, use_container_width=True)
        
    with col_b2:
        st.markdown("### 🌳 Top Dự Án Trồng Rừng" if lang=="Tiếng Việt" else "### 🌳 Top Forest Projects")
        df_for = pd.DataFrame({
            "Hạng" if lang=="Tiếng Việt" else "Rank": ["🥇 1", "🥈 2", "🥉 3"],
            "Dự Án" if lang=="Tiếng Việt" else "Project": ["Rừng ngập mặn Cà Mau", "Dự án Bắc Trung Bộ", "KBT Nam Cát Tiên"],
            "CO2 (Tấn)" if lang=="Tiếng Việt" else "CO2 (Tons)": ["1.2M", "850K", "520K"]
        })
        st.dataframe(df_for, hide_index=True, use_container_width=True)

    st.divider()
    st.markdown("### 🌟 Thành tích Của Bạn" if lang=="Tiếng Việt" else "### 🌟 Your Achievements")
    
    user = st.session_state.get('current_user', 'Bạn')
    role = st.session_state.get('current_role', 'Thành viên')
    lvl = "Cấp độ: 🌱 Mầm Xanh" if lang=="Tiếng Việt" else "Level: 🌱 Sprout"
    desc = "(Giao dịch thêm để thăng hạng!)" if lang=="Tiếng Việt" else "(Trade more to level up!)"
    
    st.markdown(f"""
        <div class="glass-card" style="border-left: 5px solid #48bb78; padding: 25px;">
            <h3 style="color: #ffffff; margin-top: 0;">👤 Profile: <span style="color:#63b3ed;">{user}</span></h3>
            <p style="color: #a0aec0; font-size: 1.1rem; margin-bottom: 20px;">Role: <b>{role}</b></p>
            <div>
                <span style="background: #276749; color: #c6f6d5; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9rem;">{lvl}</span>
                <span style="margin-left: 15px; color: #cbd5e0; font-size: 0.95rem;">{desc}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
