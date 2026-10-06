import streamlit as st
from datetime import datetime
import db_manager

def hien_thi_mang_xa_hoi():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    _, c_mid, _ = st.columns([0.15, 0.7, 0.15])

    with c_mid:
        st.markdown("<h3 style='color: white; text-align: center; font-weight:800;'>MẠNG XÃ HỘI TÍN CHỈ CARBON</h3>" if lang == "Tiếng Việt" else "<h3 style='color: white; text-align: center; font-weight:800;'>CARBON CREDIT SOCIAL NETWORK</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #a0aec0;'>Nơi cộng đồng kết nối, chia sẻ kiến thức và lan tỏa giá trị Net-Zero</p>" if lang == "Tiếng Việt" else "<p style='text-align: center; color: #a0aec0;'>Connect, share knowledge, and spread Net-Zero values globally</p>", unsafe_allow_html=True)

        if "social_posts" not in st.session_state:
            st.session_state["social_posts"] = db_manager.load_social_posts()

        with st.container(border=True):
            st.markdown(f"<h4 style='color:#48bb78;'>{'TẠO BÀI VIẾT MỚI' if lang == 'Tiếng Việt' else 'CREATE NEW POST'}</h4>", unsafe_allow_html=True)
            with st.form("form_create_post", clear_on_submit=True):
                noi_dung = st.text_area("Nội dung bài viết:" if lang == "Tiếng Việt" else "Post Content:", placeholder="Chia sẻ góc nhìn, câu chuyện xanh..." if lang=="Tiếng Việt" else "Share green insights...", height=100)
                if st.form_submit_button("ĐĂNG BÀI" if lang == "Tiếng Việt" else "PUBLISH", type="primary", use_container_width=True) and noi_dung.strip():
                    author = st.session_state.get('current_user', 'User')
                    role = st.session_state.get('current_role', 'Member')
                    post_time = datetime.now().strftime("%d/%m/%Y %H:%M")
                    
                    db_manager.add_social_post(author, role, noi_dung.strip(), post_time)
                    st.session_state["social_posts"] = db_manager.load_social_posts()
                    st.rerun()

        st.markdown(f"<h4 style='color: white; text-align: center; margin-top:30px;'>{'BẢNG TIN CỘNG ĐỒNG' if lang == 'Tiếng Việt' else 'COMMUNITY FEED'}</h4>", unsafe_allow_html=True)
        
        posts = db_manager.load_social_posts()
        for i, post in enumerate(posts):
            with st.container(border=True):
                st.markdown(f"""
                <h5 style="color: #63b3ed; margin-bottom: 5px; margin-top:0;">{post['author']} <span style="font-size: 0.8rem; color: #a0aec0;">({post['role']})</span></h5>
                <p style="color: #a0aec0; font-size: 0.8rem; margin-bottom: 12px;">{post['time']}</p>
                <p style="color: #e2e8f0; font-size: 1.05rem;">{post['content']}</p>
                """, unsafe_allow_html=True)
