import streamlit as st
import datetime

try:
    import db_manager
except ImportError:
    db_manager = None

def hien_thi_mang_xa_hoi():
    st.markdown("""
        <style>
        .social-title-green {
            color: #48bb78 !important;
            font-size: clamp(24px, 2.7vw, 34px) !important;
            font-weight: 900 !important;
            text-align: center;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
            text-transform: uppercase;
            text-shadow: 0 0 15px rgba(72, 187, 120, 0.4);
        }
        .social-sub {
            text-align: center;
            color: #94a3b8;
            font-size: 1rem;
            margin-bottom: 25px;
        }
        .social-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(72, 187, 120, 0.35);
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 16px;
        }
        .social-author {
            color: #48bb78;
            font-weight: 800;
            font-size: 1.05rem;
        }
        .social-meta {
            color: #64748b;
            font-size: 0.85rem;
            margin-bottom: 10px;
        }
        .social-content {
            color: #f1f5f9;
            font-size: 0.98rem;
            line-height: 1.6;
            margin-bottom: 14px;
        }
        .badge-room {
            display: inline-block;
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.4);
            padding: 2px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 700;
            margin-left: 8px;
        }
        /* Nút đăng bài màu xanh lá */
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
            border: 1.5px solid #4ade80 !important;
            color: white !important;
            font-weight: 800 !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%) !important;
            box-shadow: 0 0 20px rgba(72, 187, 120, 0.8) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="social-title-green">MẠNG XÃ HỘI TÍN CHỈ CARBON</div>', unsafe_allow_html=True)
    st.markdown('<div class="social-sub">Nơi cộng đồng kết nối, chia sẻ kiến thức và lan tỏa giá trị Net-Zero</div>', unsafe_allow_html=True)

    # Phân chia phòng trò chuyện
    phong_chon = st.radio(
        "Khu vực thảo luận:",
        ["Phòng Thế giới (Toàn cầu)", "Phòng Tỉnh thành (Địa phương)", "Phòng Nhóm dự án riêng"],
        horizontal=True
    )

    if phong_chon == "Phòng Tỉnh thành (Địa phương)":
        tinh_chon = st.selectbox("Chọn tỉnh / thành phố:", ["Cà Mau", "Quảng Bình", "Lâm Đồng", "Hà Tĩnh", "Sơn La", "TP. Hồ Chí Minh"])
        room_label = f"Tỉnh {tinh_chon}"
    elif phong_chon == "Phòng Nhóm dự án riêng":
        nhom_chon = st.selectbox("Chọn nhóm chuyên trách:", ["Kỹ sư viễn thám & MRV", "Nhà đầu tư thị trường", "Chủ rừng ngập mặn"])
        room_label = nhom_chon
    else:
        room_label = "Thế giới"

    # Tạo bài viết mới
    with st.container(border=True):
        st.markdown('<div style="color:#48bb78; font-weight:800; font-size:1.15rem; margin-bottom:12px;">TẠO BÀI VIẾT MỚI</div>', unsafe_allow_html=True)
        with st.form("form_post", clear_on_submit=True):
            post_content = st.text_area("Nội dung bài viết:", placeholder=f"Chia sẻ góc nhìn xanh tại {room_label}...")
            submitted = st.form_submit_button("ĐĂNG BÀI", use_container_width=True)
            if submitted:
                if post_content.strip():
                    if "social_posts_mem" not in st.session_state:
                        st.session_state["social_posts_mem"] = []
                    now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    author = st.session_state.get("current_user", "Ẩn danh")
                    role = st.session_state.get("current_role", "Thành viên")
                    
                    new_p = {
                        "id": f"p_{len(st.session_state['social_posts_mem']) + 1}",
                        "author": author,
                        "role": role,
                        "content": post_content,
                        "time": now_str,
                        "room": room_label,
                        "likes": 0,
                        "liked_by": set(),
                        "comments": []
                    }
                    st.session_state["social_posts_mem"].insert(0, new_p)
                    st.success("Đã đăng bài viết thành công.")
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập nội dung bài viết.")

    st.markdown('<div class="social-title-green" style="font-size:1.4rem; margin-top:30px;">BẢNG TIN CỘNG ĐỒNG</div>', unsafe_allow_html=True)

    if "social_posts_mem" not in st.session_state:
        st.session_state["social_posts_mem"] = [
            {
                "id": "p_default_1",
                "author": "Kỹ Sư Rừng Cà Mau",
                "role": "Chủ rừng / Kỹ sư MRV",
                "content": "Đợt đo kiểm viễn thám tháng này ghi nhận mật độ sinh khối ven biển tăng rất tốt, dữ liệu viễn thám đã khớp với chỉ số thực địa.",
                "time": "08/10/2026 14:20",
                "room": "Thế giới",
                "likes": 24,
                "liked_by": set(),
                "comments": ["Dự án tuyệt vời!", "Bao giờ mở bán tín chỉ đợt mới ạ?"]
            },
            {
                "id": "p_default_2",
                "author": "Quỹ Đầu Tư Xanh",
                "role": "Nhà đầu tư từ xa",
                "content": "Chúng tôi đang thẩm định thêm 3 dự án tại khu vực Bắc Trung Bộ. Nền tảng hiển thị minh bạch giúp rút ngắn rất nhiều thời gian giải ngân.",
                "time": "07/10/2026 09:15",
                "room": "Thế giới",
                "likes": 18,
                "liked_by": set(),
                "comments": ["Rất mong được hợp tác cùng quý quỹ."]
            }
        ]

    posts = st.session_state["social_posts_mem"]
    if not posts:
        st.info("Chưa có bài viết nào trong phòng này.")
        return

    for idx, p in enumerate(posts):
        st.markdown(f"""
            <div class="social-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span class="social-author">{p['author']}</span> 
                        <span style="color:#94a3b8; font-size:0.85rem;">({p['role']})</span>
                        <span class="badge-room">{p.get('room', 'Thế giới')}</span>
                    </div>
                    <span class="social-meta">{p['time']}</span>
                </div>
                <div class="social-content" style="margin-top:10px;">{p['content']}</div>
                <div style="color:#94a3b8; font-size:0.88rem; margin-bottom:8px;">
                    Lượt thích: <b style="color:#48bb78;">{p['likes']}</b> &nbsp;|&nbsp; 
                    Bình luận: <b style="color:#38bdf8;">{len(p.get('comments', []))}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        c_l, c_c, c_rep, _ = st.columns([0.18, 0.22, 0.25, 0.35])
        with c_l:
            user_now = st.session_state.get("current_user", "")
            if st.button(f"Thích ({p['likes']})", key=f"btn_like_{p['id']}_{idx}"):
                p["likes"] += 1
                st.rerun()
        with c_c:
            show_cmt = st.checkbox("Bình luận", key=f"chk_cmt_{p['id']}_{idx}")
        with c_rep:
            if st.button("Báo cáo vi phạm", key=f"btn_rep_{p['id']}_{idx}"):
                st.toast("Đã tiếp nhận báo cáo. Ban quản trị sẽ rà soát nội dung trong 24 giờ.")

        if show_cmt:
            with st.container():
                for cm in p.get("comments", []):
                    st.markdown(f"<div style='background:rgba(30,41,59,0.5); padding:6px 12px; border-radius:6px; margin:4px 0 4px 15px; font-size:0.9rem; color:#e2e8f0;'>{cm}</div>", unsafe_allow_html=True)
                with st.form(f"f_cmt_{p['id']}_{idx}", clear_on_submit=True):
                    c_txt = st.text_input("Viết bình luận...", label_visibility="collapsed")
                    if st.form_submit_button("Gửi"):
                        if c_txt.strip():
                            u_name = st.session_state.get("current_user", "Ẩn danh")
                            p.setdefault("comments", []).append(f"{u_name}: {c_txt}")
                            st.rerun()
