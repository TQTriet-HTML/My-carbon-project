import streamlit as st
from datetime import datetime

def hien_thi_mang_xa_hoi():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    
    title = "## 🌐 Mạng Xã Hội Tín Chỉ Carbon" if lang == "Tiếng Việt" else "## 🌐 Carbon Credit Social Network"
    cap = "Nơi cộng đồng kết nối, chia sẻ kiến thức và lan tỏa giá trị Net-Zero" if lang == "Tiếng Việt" else "Connect, share knowledge, and spread Net-Zero values globally"
    
    st.markdown(title)
    st.caption(cap)

    if "social_posts" not in st.session_state or not st.session_state["social_posts"]:
        st.session_state["social_posts"] = [
            {
                "id": "post_1", "author": "Lê Văn A", "role": "Chủ rừng / MRV",
                "content": "Thử nghiệm công nghệ vệ tinh Sentinel-2 mới rất ấn tượng!" if lang=="Tiếng Việt" else "The new Sentinel-2 AI tech is impressive!",
                "time": "04/10/2026 09:30", "likes": 12, "comments": []
            }
        ]

    with st.container(border=True):
        st.markdown("#### ✍️ Tạo bài viết mới" if lang == "Tiếng Việt" else "#### ✍️️ Create a new post")
        with st.form("form_new_post", clear_on_submit=True):
            pl_holder = "Chia sẻ dự án của bạn..." if lang == "Tiếng Việt" else "Share your project updates..."
            noi_dung = st.text_area("Nội dung / Content:", placeholder=pl_holder)
            col_btn, _ = st.columns([2, 8])
            with col_btn:
                btn_txt = "📝 Đăng bài" if lang == "Tiếng Việt" else "📝 Post"
                submitted = st.form_submit_button(btn_txt, type="primary", use_container_width=True)
            
            if submitted and noi_dung.strip():
                st.session_state["social_posts"].insert(0, {
                    "id": f"p_{len(st.session_state['social_posts'])+1}",
                    "author": st.session_state.get('current_user', 'User'),
                    "role": st.session_state.get('current_role', 'Member'),
                    "content": noi_dung.strip(),
                    "time": datetime.now().strftime("%d/%m/%Y %H:%M"), "likes": 0, "comments": []
                })
                st.rerun()

    st.divider()
    st.markdown("### 📰 Bảng tin Cộng đồng" if lang == "Tiếng Việt" else "### 📰 Community Feed")

    for i, post in enumerate(st.session_state["social_posts"]):
        st.markdown(f"""
            <div class="glass-card" style="padding: 15px 25px; margin-bottom: 10px;">
                <h5 style="color: #63b3ed; margin-bottom: 5px; margin-top:0;">👤 {post['author']} <span style="font-size: 0.8rem; color: #a0aec0;">({post['role']})</span></h5>
                <p style="color: #a0aec0; font-size: 0.8rem; margin-bottom: 12px;">🕒 {post['time']}</p>
                <p style="color: #e2e8f0; font-size: 1.05rem;">{post['content']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_like, col_comment = st.columns([2, 10])
        with col_like:
            btn_like = f"👍 Thích ({post['likes']})" if lang=="Tiếng Việt" else f"👍 Like ({post['likes']})"
            if st.button(btn_like, key=f"like_{post['id']}_{i}", use_container_width=True):
                post['likes'] += 1
                st.rerun()
        
        txt_exp = f"💬 Bình luận ({len(post['comments'])})" if lang=="Tiếng Việt" else f"💬 Comments ({len(post['comments'])})"
        with st.expander(txt_exp):
            for cmt in post['comments']:
                st.markdown(f"**{cmt['user']}**: <span style='color:#cbd5e0;'>{cmt['text']}</span>", unsafe_allow_html=True)
            
            with st.form(f"cmt_{post['id']}_{i}", clear_on_submit=True):
                cmt_text = st.text_input("Bình luận / Comment:")
                if st.form_submit_button("Gửi / Send", type="primary") and cmt_text.strip():
                    post['comments'].append({"user": st.session_state.get('current_user', 'User'), "text": cmt_text.strip()})
                    st.rerun()
