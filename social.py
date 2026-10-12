import streamlit as st
import datetime

def hien_thi_mang_xa_hoi(lang="Tiếng Việt"):
    T = {
        "Tiếng Việt": {
            "title": "MẠNG XÃ HỘI TÍN CHỈ CARBON",
            "subtitle": "Nơi cộng đồng kết nối, chia sẻ kiến thức và lan tỏa giá trị Net-Zero",
            "area_lbl": "Khu vực thảo luận:",
            "room_1": "Phòng Thế giới (Toàn cầu)",
            "room_2": "Phòng Tỉnh thành (Địa phương)",
            "room_3": "Phòng Nhóm dự án riêng",
            "select_prov": "Chọn tỉnh / thành phố:",
            "select_group": "Chọn nhóm chuyên trách:",
            "create_post": "TẠO BÀI VIẾT MỚI",
            "post_content": "Nội dung bài viết:",
            "post_placeholder": "Chia sẻ góc nhìn xanh tại {room}...",
            "btn_post": "ĐĂNG BÀI",
            "msg_success": "Đã đăng bài viết thành công.",
            "msg_warning": "Vui lòng nhập nội dung bài viết.",
            "news_feed": "BẢNG TIN CỘNG ĐỒNG",
            "no_post": "Chưa có bài viết nào.",
            "world": "Thế giới",
            "likes": "Lượt thích",
            "comments": "Bình luận",
            "btn_like": "Thích",
            "btn_rep": "Báo cáo vi phạm",
            "rep_msg": "Đã tiếp nhận báo cáo vi phạm. Ban kiểm duyệt sẽ xử lý trong 24h.",
            "cmt_lbl": "BÌNH LUẬN NỘI BỘ:",
            "cmt_input": "Viết bình luận công khai...",
            "btn_send": "Gửi",
            "view_cmts": "Xem bình luận ({count})"
        },
        "English": {
            "title": "CARBON CREDIT SOCIAL NETWORK",
            "subtitle": "Where the community connects, shares knowledge, and spreads Net-Zero values",
            "area_lbl": "Discussion Area:",
            "room_1": "Global Room (Worldwide)",
            "room_2": "Provincial Room (Local)",
            "room_3": "Private Project Room",
            "select_prov": "Select province / city:",
            "select_group": "Select specialized group:",
            "create_post": "CREATE NEW POST",
            "post_content": "Post content:",
            "post_placeholder": "Share your green perspective in {room}...",
            "btn_post": "POST",
            "msg_success": "Post created successfully.",
            "msg_warning": "Please enter post content.",
            "news_feed": "COMMUNITY NEWS FEED",
            "no_post": "No posts yet.",
            "world": "Worldwide",
            "likes": "Likes",
            "comments": "Comments",
            "btn_like": "Like",
            "btn_rep": "Report Violation",
            "rep_msg": "Violation report received. The moderation team will process within 24h.",
            "cmt_lbl": "INTERNAL COMMENTS:",
            "cmt_input": "Write a public comment...",
            "btn_send": "Send",
            "view_cmts": "View comments ({count})"
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

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

        /* 1. BIẾN 3 CHẤM RADIO THÀNH 3 KHỐI NÚT XANH DƯƠNG NỔI BỔNG */
        div[data-testid="stRadio"] div[role="radiogroup"] label div:first-child {
            display: none !important; /* Ẩn triệt để dấu chấm tròn */
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
            border: 1.5px solid #334155 !important;
            padding: 10px 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 0 #020617, 0 6px 12px rgba(0,0,0,0.4) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            margin-right: 15px !important;
            cursor: pointer !important;
            margin-bottom: 10px !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label div {
            color: #94a3b8 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }
        
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            background: linear-gradient(180deg, #38bdf8 0%, #0284c7 100%) !important;
            border-color: #7dd3fc !important;
            transform: translateY(-4px) !important;
            box-shadow: 0 8px 0 #075985, 0 12px 25px rgba(56, 189, 248, 0.6) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover div {
            color: #ffffff !important;
        }
        
        div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(180deg, #0284c7 0%, #0369a1 100%) !important;
            border-color: #38bdf8 !important;
            transform: translateY(2px) !important;
            box-shadow: 0 2px 0 #075985, 0 4px 10px rgba(2, 132, 199, 0.5) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) div {
            color: #ffffff !important;
            font-weight: 800 !important;
        }

        /* 2. NÚT THÍCH MÀU XANH DƯƠNG NỔI BỔNG CƠ HỌC */
        div[class*="st-key-btn_like_"] button {
            background: linear-gradient(180deg, #0284c7 0%, #0369a1 100%) !important;
            border: 1.5px solid #38bdf8 !important;
            border-radius: 10px !important;
            box-shadow: 0 5px 0 #075985, 0 8px 18px rgba(14, 165, 233, 0.45) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            padding: 6px 18px !important;
        }
        div[class*="st-key-btn_like_"] button p {
            color: #ffffff !important;
            font-weight: 800 !important;
        }
        div[class*="st-key-btn_like_"] button:hover {
            background: linear-gradient(180deg, #38bdf8 0%, #0284c7 100%) !important;
            transform: translateY(-4px) !important;
            box-shadow: 0 9px 0 #075985, 0 14px 26px rgba(56, 189, 248, 0.75) !important;
            border-color: #7dd3fc !important;
        }
        div[class*="st-key-btn_like_"] button:active {
            transform: translateY(4px) !important;
            box-shadow: 0 1px 0 #075985, 0 4px 10px rgba(56, 189, 248, 0.4) !important;
        }

        /* 3. ĐỒNG BỘ NÚT ĐĂNG BÀI LÊN XANH LÁ NỔI 3D CHUẨN */
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(180deg, #22c55e 0%, #16a34a 100%) !important;
            border: 1.5px solid #4ade80 !important;
            border-radius: 10px !important;
            box-shadow: 0 5px 0 #15803d, 0 8px 18px rgba(34, 197, 94, 0.45) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }
        div[data-testid="stFormSubmitButton"] button p {
            color: #ffffff !important;
            font-weight: 800 !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(180deg, #4ade80 0%, #22c55e 100%) !important;
            transform: translateY(-4px) !important;
            box-shadow: 0 9px 0 #15803d, 0 14px 26px rgba(34, 197, 94, 0.75) !important;
        }
        div[data-testid="stFormSubmitButton"] button:active {
            transform: translateY(4px) !important;
            box-shadow: 0 1px 0 #15803d, 0 4px 10px rgba(34, 197, 94, 0.4) !important;
        }
        
        /* 4. ĐỒNG BỘ NÚT BÁO CÁO VI PHẠM (CHÌM XUỐNG - HOVER NỔI ĐỎ) */
        div[class*="st-key-btn_rep_"] button {
            background: linear-gradient(180deg, rgba(51, 65, 85, 0.8), rgba(30, 41, 59, 0.9)) !important;
            border: 1px solid rgba(148, 163, 184, 0.3) !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 0 rgba(15, 23, 42, 0.8), 0 5px 10px rgba(0,0,0,0.3) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }
        div[class*="st-key-btn_rep_"] button p {
            color: #94a3b8 !important;
            font-weight: 600 !important;
        }
        div[class*="st-key-btn_rep_"] button:hover {
            background: linear-gradient(180deg, rgba(239, 68, 68, 0.4), rgba(185, 28, 28, 0.6)) !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 7px 0 rgba(153, 27, 27, 0.8), 0 10px 20px rgba(239, 68, 68, 0.4) !important;
            border-color: rgba(248, 113, 113, 0.6) !important;
        }
        div[class*="st-key-btn_rep_"] button:hover p {
            color: #fca5a5 !important;
        }
        div[class*="st-key-btn_rep_"] button:active {
            transform: translateY(4px) !important;
            box-shadow: 0 0px 0 rgba(153, 27, 27, 0.8), 0 2px 5px rgba(239, 68, 68, 0.2) !important;
        }

        .social-card {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(72, 187, 120, 0.35);
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 20px;
        }
        .social-author {
            color: #48bb78;
            font-weight: 800;
            font-size: 1.05rem;
        }
        .social-meta {
            color: #64748b;
            font-size: 0.85rem;
        }
        .social-content {
            color: #f1f5f9;
            font-size: 1rem;
            line-height: 1.6;
            margin: 12px 0 14px 0;
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
        .comment-thread {
            background: rgba(15, 23, 42, 0.55);
            border-left: 3px solid rgba(72, 187, 120, 0.6);
            border-radius: 0 8px 8px 0;
            padding: 10px 14px;
            margin-top: 8px;
            margin-bottom: 8px;
        }
        .comment-user {
            color: #38bdf8;
            font-weight: 700;
            font-size: 0.88rem;
            margin-bottom: 2px;
        }
        .comment-body {
            color: #e2e8f0;
            font-size: 0.92rem;
            line-height: 1.45;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="social-title-green">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="social-sub">{t["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown(f"<div style='color: #cbd5e1; font-weight: 600; font-size: 0.95rem; margin-bottom: 15px;'>{t['area_lbl']}</div>", unsafe_allow_html=True)
    
    phong_chon = st.radio(
        "Khu vực thảo luận (ẩn)",
        [t["room_1"], t["room_2"], t["room_3"]],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("<br/>", unsafe_allow_html=True)

    if phong_chon == t["room_2"]:
        tinh_chon = st.selectbox(t["select_prov"], ["Cà Mau", "Quảng Bình", "Lâm Đồng", "Hà Tĩnh", "Sơn La", "TP. Hồ Chí Minh"])
        room_label = f"Tỉnh {tinh_chon}" if lang == "Tiếng Việt" else f"{tinh_chon} Province"
    elif phong_chon == t["room_3"]:
        nhom_chon = st.selectbox(t["select_group"], ["Kỹ sư viễn thám & MRV", "Nhà đầu tư thị trường", "Chủ rừng ngập mặn"])
        room_label = nhom_chon
    else:
        room_label = t["world"]

    with st.container(border=True):
        st.markdown(f'<div style="color:#48bb78; font-weight:800; font-size:1.15rem; margin-bottom:12px;">{t["create_post"]}</div>', unsafe_allow_html=True)
        with st.form("form_post", clear_on_submit=True):
            placeholder_text = t["post_placeholder"].replace("{room}", room_label)
            post_content = st.text_area(t["post_content"], placeholder=placeholder_text)
            submitted = st.form_submit_button(t["btn_post"], use_container_width=True)
            if submitted:
                if post_content.strip():
                    if "social_posts_mem" not in st.session_state:
                        st.session_state["social_posts_mem"] = []
                    now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    author = st.session_state.get("current_user", "Member" if lang == "English" else "Thành viên")
                    role = st.session_state.get("current_role", "Green Companion" if lang == "English" else "Đồng hành xanh")
                    
                    new_p = {
                        "id": f"p_{len(st.session_state['social_posts_mem']) + 1}",
                        "author": author,
                        "role": role,
                        "content": post_content,
                        "time": now_str,
                        "room": room_label,
                        "likes": 0,
                        "comments": []
                    }
                    st.session_state["social_posts_mem"].insert(0, new_p)
                    st.success(t["msg_success"])
                    st.rerun()
                else:
                    st.warning(t["msg_warning"])

    st.markdown(f'<div class="social-title-green" style="font-size:1.4rem; margin-top:35px; margin-bottom:20px;">{t["news_feed"]}</div>', unsafe_allow_html=True)

    if "social_posts_mem" not in st.session_state:
        st.session_state["social_posts_mem"] = [
            {
                "id": "p_default_1",
                "author": "Kỹ Sư Rừng Cà Mau",
                "role": "Forest Owner / MRV Engineer" if lang == "English" else "Chủ rừng / Kỹ sư MRV",
                "content": "The remote sensing survey this month shows very good coastal biomass growth, matching field data perfectly." if lang == "English" else "Đợt đo kiểm viễn thám tháng này ghi nhận mật độ sinh khối ven biển tăng rất tốt, dữ liệu viễn thám đã khớp với chỉ số thực địa.",
                "time": "08/10/2026 14:20",
                "room": t["world"],
                "likes": 24,
                "comments": [
                    {"user": "Vinamilk Net-Zero", "text": "Very promising project, we are interested in the next supply batch." if lang == "English" else "Dự án rất triển vọng, bên mình đang quan tâm nguồn cung đợt tới."},
                    {"user": "Nhà Đầu Tư Xanh", "text": "Satellite data is very clear and transparent." if lang == "English" else "Dữ liệu ảnh viễn thám rõ nét và minh bạch lắm."}
                ]
            },
            {
                "id": "p_default_2",
                "author": "Quỹ Đầu Tư Xanh",
                "role": "Remote Investor" if lang == "English" else "Nhà đầu tư từ xa",
                "content": "We are appraising 3 more projects in the North Central region. The transparent platform significantly shortens disbursement time." if lang == "English" else "Chúng tôi đang thẩm định thêm 3 dự án tại khu vực Bắc Trung Bộ. Nền tảng hiển thị minh bạch giúp rút ngắn rất nhiều thời gian giải ngân.",
                "time": "07/10/2026 09:15",
                "room": t["world"],
                "likes": 18,
                "comments": [
                    {"user": "Bộ NN&PTNT", "text": "Looking forward to sustainable cooperation with your fund." if lang == "English" else "Rất mong được hợp tác phát triển bền vững cùng quý quỹ."}
                ]
            }
        ]

    posts = st.session_state["social_posts_mem"]
    if not posts:
        st.info(t["no_post"])
        return

    for idx, p in enumerate(posts):
        st.markdown(f"""
            <div class="social-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span class="social-author">{p['author']}</span> 
                        <span style="color:#94a3b8; font-size:0.85rem;">({p['role']})</span>
                        <span class="badge-room">{p.get('room', t['world'])}</span>
                    </div>
                    <span class="social-meta">{p['time']}</span>
                </div>
                <div class="social-content">{p['content']}</div>
                <div style="color:#94a3b8; font-size:0.88rem; margin-bottom:12px;">
                    {t['likes']}: <b style="color:#38bdf8;">{p['likes']}</b> &nbsp;|&nbsp; 
                    {t['comments']}: <b style="color:#48bb78;">{len(p.get('comments', []))}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        c_like, c_rep, _ = st.columns([0.22, 0.28, 0.5])
        with c_like:
            if st.button(f"{t['btn_like']} ({p['likes']})", key=f"btn_like_{p['id']}_{idx}"):
                p["likes"] += 1
                st.rerun()
        with c_rep:
            if st.button(t["btn_rep"], key=f"btn_rep_{p['id']}_{idx}"):
                st.toast(t["rep_msg"])

        comments_list = p.get("comments", [])
        
        # HIỆN EXPANDER XEM BÌNH LUẬN GIỐNG FACEBOOK
        with st.expander(t["view_cmts"].replace("{count}", str(len(comments_list))), expanded=False):
            if comments_list:
                st.markdown(f"<div style='margin-bottom:5px; font-weight:700; color:#94a3b8; font-size:0.88rem;'>{t['cmt_lbl']}</div>", unsafe_allow_html=True)
                for cm in comments_list:
                    if isinstance(cm, dict):
                        u_c = cm.get("user", "Member" if lang == "English" else "Thành viên")
                        t_c = cm.get("text", "")
                    else:
                        parts = str(cm).split(":", 1)
                        u_c = parts[0] if len(parts) > 1 else ("Member" if lang == "English" else "Thành viên")
                        t_c = parts[1] if len(parts) > 1 else str(cm)
                        
                    st.markdown(f"""
                        <div class="comment-thread">
                            <div class="comment-user">{u_c}</div>
                            <div class="comment-body">{t_c}</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption(t["no_post"])

            with st.form(f"form_quick_cmt_{p['id']}_{idx}", clear_on_submit=True):
                col_in, col_btn = st.columns([0.82, 0.18])
                with col_in:
                    new_c_txt = st.text_input(t["cmt_input"], placeholder=t["cmt_input"], label_visibility="collapsed")
                with col_btn:
                    btn_send_c = st.form_submit_button(t["btn_send"], use_container_width=True)
                
                if btn_send_c and new_c_txt.strip():
                    cur_user = st.session_state.get("current_user", "Anonymous" if lang == "English" else "Ẩn danh")
                    p.setdefault("comments", []).append({"user": cur_user, "text": new_c_txt.strip()})
                    st.rerun()

        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
