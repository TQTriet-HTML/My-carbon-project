import streamlit as st
from datetime import datetime

def hien_thi_mang_xa_hoi():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    _, c_mid, _ = st.columns([0.15, 0.7, 0.15])
    
    with c_mid:
        st.markdown("<h3 style='color: white; text-align: center; font-weight:800;'>MẠNG XÃ HỘI TÍN CHỈ CARBON</h3>" if lang == "Tiếng Việt" else "<h3 style='color: white; text-align: center; font-weight:800;'>CARBON CREDIT SOCIAL NETWORK</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #a0aec0;'>Nơi cộng đồng kết nối, chia sẻ kiến thức và lan tỏa giá trị Net-Zero</p>" if lang == "Tiếng Việt" else "<p style='text-align: center; color: #a0aec0;'>Connect, share knowledge, and spread Net-Zero values globally</p>", unsafe_allow_html=True)

        if "social_posts" not in st.session_state or not st.session_state["social_posts"]:
            st.session_state["social_posts"] = [
                {"id": "post_1", "author": "Hệ Thống", "role": "Admin", "content": "Thử nghiệm công nghệ vệ tinh mới rất ấn tượng!" if lang=="Tiếng Việt" else "New satellite tech is impressive!", "time": "04/10/2026 09:30", "likes": 12, "comments": []}
            ]

        with st.container(border=True):
            st.markdown(f"<h4 style='color:#48bb78;'>{'TẠO BÀI VIẾT MỚI' if lang == 'Tiếng Việt' else 'CREATE NEW POST'}</h4>", unsafe_allow_html=True)
            with st.form("form_new_post", clear_on_submit=True):
                noi_dung = st.text_area("Nội dung / Content:", placeholder="Chia sẻ góc nhìn của bạn..." if lang == "Tiếng Việt" else "Share your thoughts...")
                col_btn, _ = st.columns([3, 7])
                with col_btn:
                    if st.form_submit_button("ĐĂNG BÀI" if lang == "Tiếng Việt" else "PUBLISH", type="primary", use_container_width=True) and noi_dung.strip():
                        st.session_state["social_posts"].insert(0, {
                            "id": f"p_{len(st.session_state['social_posts'])+1}",
                            "author": st.session_state.get('current_user', 'User'), "role": st.session_state.get('current_role', 'Member'),
                            "content": noi_dung.strip(), "time": datetime.now().strftime("%d/%m/%Y %H:%M"), "likes": 0, "comments": []
                        })
                        st.rerun()

        st.markdown(f"<h4 style='color: white; text-align: center; margin-top:30px;'>{'BẢNG TIN CỘNG ĐỒNG' if lang == 'Tiếng Việt' else 'COMMUNITY FEED'}</h4>", unsafe_allow_html=True)
        for i, post in enumerate(st.session_state["social_posts"]):
            with st.container(border=True):
                st.markdown(f"""
                    <h5 style="color: #63b3ed; margin-bottom: 5px; margin-top:0;">{post['author']} <span style="font-size: 0.8rem; color: #a0aec0;">({post['role']})</span></h5>
                    <p style="color: #a0aec0; font-size: 0.8rem; margin-bottom: 12px;">{post['time']}</p>
                    <p style="color: #e2e8f0; font-size: 1.05rem;">{post['content']}</p>
                """, unsafe_allow_html=True)
                
                c_like, c_cmt = st.columns([2, 8])
                with c_like:
                    if st.button(f"Thích ({post['likes']})" if lang=="Tiếng Việt" else f"Like ({post['likes']})", key=f"like_{post['id']}_{i}", use_container_width=True):
                        post['likes'] += 1
                        st.rerun()
                
                with st.expander(f"Bình luận ({len(post['comments'])})" if lang=="Tiếng Việt" else f"Comments ({len(post['comments'])})"):
                    for cmt in post['comments']: st.markdown(f"**{cmt['user']}**: <span style='color:#cbd5e0;'>{cmt['text']}</span>", unsafe_allow_html=True)
                    with st.form(f"cmt_{post['id']}_{i}", clear_on_submit=True):
                        cmt_text = st.text_input("Bình luận / Comment:")
                        if st.form_submit_button("Gửi / Send", type="primary") and cmt_text.strip():
                            post['comments'].append({"user": st.session_state.get('current_user', 'User'), "text": cmt_text.strip()})
                            st.rerun()
