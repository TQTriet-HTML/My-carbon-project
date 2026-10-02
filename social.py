import streamlit as st
from datetime import datetime

def hien_thi_mang_xa_hoi():
    st.markdown("## 🌐 Carbon Connect - Mạng xã hội Tín chỉ Xanh")
    st.caption("Cộng đồng kết nối, chia sẻ kiến thức và thảo luận về thị trường Net-Zero toàn cầu.")
    
    # 1. KHU VỰC ĐĂNG BÀI
    with st.container(border=True):
        st.markdown("#### ✍️ Chia sẻ góc nhìn của bạn")
        noi_dung = st.text_area("Bạn đang nghĩ gì về thị trường Carbon hôm nay? (Hỗ trợ định dạng Markdown)", height=100)
        
        col_tag, col_btn = st.columns([3, 1])
        with col_tag:
            tag = st.selectbox("Gắn thẻ chủ đề:", ["#TinTucThitruong", "#KinhNghiemTrongRung", "#GoiVonDauTu", "#HoiDapMRV", "#NetZero"])
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Đăng bài", type="primary", use_container_width=True):
                if noi_dung:
                    nguoi_dang = st.session_state.get('current_user', 'Khách ẩn danh')
                    vai_tro = st.session_state.get('current_role', 'Người dùng')
                    
                    # Thêm bài viết mới lên đầu danh sách
                    st.session_state["social_posts"].insert(0, {
                        "id": f"post_{len(st.session_state['social_posts'])}",
                        "author": nguoi_dang,
                        "role": vai_tro,
                        "content": noi_dung,
                        "tag": tag,
                        "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "likes": 0,
                        "comments": []
                    })
                    st.success("Tạo bài viết thành công!")
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập nội dung trước khi đăng.")

    st.divider()
    
    # 2. BẢNG TIN CỘNG ĐỒNG (NEWS FEED)
    st.markdown("### 📰 Bảng tin Mới nhất")
    
    if not st.session_state.get("social_posts"):
        st.info("Chưa có bài viết nào. Hãy là người đầu tiên khai trương mạng xã hội này!")
    else:
        for post in st.session_state["social_posts"]:
            with st.container(border=True):
                # Avatar và Tên người đăng
                col_ava, col_name = st.columns([1, 15])
                with col_ava:
                    # Gán avatar giả lập theo vai trò
                    if post["role"] == "Chủ rừng / Kỹ sư MRV": st.markdown("## 👨‍🌾")
                    elif post["role"] == "Doanh nghiệp mua tín chỉ": st.markdown("## 🏢")
                    else: st.markdown("## 🤵")
                with col_name:
                    st.markdown(f"**{post['author']}** 🔹 *{post['role']}*")
                    st.caption(f"🕒 {post['time']} | 🏷️ {post['tag']}")
                
                # Nội dung bài viết
                st.markdown(f"> {post['content']}")
                
                # Nút tương tác
                col_like, col_cmt, col_blank = st.columns([2, 2, 8])
                with col_like:
                    if st.button(f"❤️️ Thích ({post['likes']})", key=f"like_{post['id']}", help="Thích bài viết này"):
                        post['likes'] += 1
                        st.rerun()
                with col_cmt:
                    if st.button(f"💬 Bình luận ({len(post['comments'])})", key=f"cmt_btn_{post['id']}"):
                        st.session_state[f"show_cmt_{post['id']}"] = not st.session_state.get(f"show_cmt_{post['id']}", False)
                
                # Khu vực Bình luận
                if st.session_state.get(f"show_cmt_{post['id']}", False):
                    st.markdown("---")
                    for cmt in post['comments']:
                        st.markdown(f"**{cmt['user']}**: {cmt['text']}")
                    
                    new_cmt = st.text_input("Viết bình luận...", key=f"new_cmt_{post['id']}")
                    if st.button("Gửi bình luận", key=f"send_cmt_{post['id']}"):
                        if new_cmt:
                            post['comments'].append({
                                "user": st.session_state.get('current_user', 'Khách'),
                                "text": new_cmt
                            })
                            st.rerun()
