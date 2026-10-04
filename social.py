import streamlit as st
from datetime import datetime

def hien_thi_mang_xa_hoi():
    st.markdown("## 🌐 Mạng Xã Hội Tín Chỉ Carbon")
    st.caption("Nơi cộng đồng kết nối, chia sẻ kiến thức và lan tỏa giá trị Net-Zero toàn cầu")

    # Khởi tạo kho dữ liệu bài viết (nếu chưa có)
    if "social_posts" not in st.session_state or not st.session_state["social_posts"]:
        st.session_state["social_posts"] = [
            {
                "id": "post_1",
                "author": "Chuyên gia Lâm nghiệp Lê Văn A",
                "role": "Chủ rừng / Kỹ sư MRV",
                "content": "Tôi vừa thử nghiệm công nghệ vệ tinh Sentinel-2 mới cập nhật trên nền tảng. Độ chính xác nhận diện thảm thực vật cực kỳ ấn tượng, kết quả đo đạc sinh khối sát với thực tế đến 98%. Dự kiến tháng sau sẽ niêm yết lô 50,000 tấn!",
                "time": "04/10/2026 09:30",
                "likes": 12,
                "comments": [{"user": "Đại diện Vinamilk", "text": "Tuyệt vời, chúng tôi rất mong chờ lô tín chỉ tiếp theo của anh để khớp lệnh."}]
            },
            {
                "id": "post_2",
                "author": "Quỹ Đầu tư Tác động ESG",
                "role": "Nhà đầu tư từ xa (Cổ đông)",
                "content": "Chúng tôi vừa cam kết rót vốn thêm 2 triệu USD vào các dự án rừng ngập mặn Cà Mau trên nền tảng. Rất hy vọng các Chủ rừng sẽ tiếp tục giữ vững chất lượng sinh khối.",
                "time": "03/10/2026 15:45",
                "likes": 35,
                "comments": []
            }
        ]

    # FORM ĐĂNG BÀI VIẾT MỚI (Tự làm sạch)
    with st.container(border=True):
        st.markdown("#### ✍️ Tạo bài viết mới")
        with st.form("form_new_post", clear_on_submit=True):
            noi_dung = st.text_area("Chia sẻ dự án, suy nghĩ hoặc cập nhật tiến độ rừng của bạn:", placeholder="Hôm nay khu rừng của bạn thế nào?")
            col_btn, _ = st.columns([2, 8])
            with col_btn:
                submitted = st.form_submit_button("📝 Đăng bài", type="primary", use_container_width=True)
            
            if submitted:
                if noi_dung.strip():
                    new_post = {
                        "id": f"post_{len(st.session_state['social_posts']) + 1}",
                        "author": st.session_state.get('current_user', 'Ẩn danh'),
                        "role": st.session_state.get('current_role', 'Thành viên'),
                        "content": noi_dung.strip(),
                        "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "likes": 0,
                        "comments": []
                    }
                    st.session_state["social_posts"].insert(0, new_post) # Đưa bài mới lên trên cùng
                    st.success("🎉 Đăng bài thành công!")
                    st.rerun()
                else:
                    st.warning("⚠ Vui lòng nhập nội dung trước khi đăng!")
        
    st.divider()
    st.markdown("### 📰 Bảng tin Cộng đồng")

    # HIỂN THỊ CÁC BÀI VIẾT (DÙNG GLASS-CARD CHO ĐẸP)
    for i, post in enumerate(st.session_state["social_posts"]):
        st.markdown(f"""
            <div class="glass-card" style="padding: 15px 25px; margin-bottom: 10px;">
                <h5 style="color: #63b3ed; margin-bottom: 5px; margin-top:0;">👤 {post['author']} <span style="font-size: 0.8rem; color: #a0aec0; font-weight: normal;">({post['role']})</span></h5>
                <p style="color: #a0aec0; font-size: 0.8rem; margin-bottom: 12px;">🕒 {post['time']}</p>
                <p style="color: #e2e8f0; font-size: 1.05rem; line-height: 1.6;">{post['content']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Tương tác (Like & Comment)
        col_like, col_comment = st.columns([2, 10])
        with col_like:
            if st.button(f"👍 Thích ({post['likes']})", key=f"like_{post['id']}_{i}", use_container_width=True):
                post['likes'] += 1
                st.rerun()
        
        with st.expander(f"💬 Xem / Viết Bình luận ({len(post['comments'])})"):
            for cmt in post['comments']:
                st.markdown(f"**{cmt['user']}**: <span style='color:#cbd5e0;'>{cmt['text']}</span>", unsafe_allow_html=True)
            
            with st.form(f"comment_form_{post['id']}_{i}", clear_on_submit=True):
                cmt_text = st.text_input("Bình luận của bạn:", placeholder="Viết phản hồi...")
                if st.form_submit_button("Gửi Bình luận", type="primary"):
                    if cmt_text.strip():
                        post['comments'].append({
                            "user": st.session_state.get('current_user', 'Ẩn danh'),
                            "text": cmt_text.strip()
                        })
                        st.rerun()
