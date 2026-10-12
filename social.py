import streamlit as st
import datetime
import base64

@st.dialog("BÁO CÁO VI PHẠM / REPORT VIOLATION", width="small")
def hien_thi_hop_thoai_bao_cao(post_id, lang="Tiếng Việt"):
    T = {
        "Tiếng Việt": {
            "rep_reason_lbl": "Chọn lý do báo cáo:",
            "rep_r1": "Spam / Quảng cáo rác",
            "rep_r2": "Thông tin sai lệch / Lừa đảo",
            "rep_r3": "Ngôn từ kích động / Thù địch",
            "rep_r4": "Nội dung không liên quan đến tín chỉ Carbon",
            "rep_r5": "Vi phạm bản quyền / Quyền riêng tư",
            "rep_r6": "Xúc phạm cá nhân / Tổ chức",
            "rep_r7": "Khác...",
            "rep_other_lbl": "Vui lòng nhập lý do cụ thể:",
            "btn_submit_rep": "GỬI BÁO CÁO",
            "rep_msg": "Đã tiếp nhận báo cáo. Ban kiểm duyệt sẽ xử lý trong 24h.",
            "btn_cancel": "HỦY"
        },
        "English": {
            "rep_reason_lbl": "Select a reason for reporting:",
            "rep_r1": "Spam / Junk advertising",
            "rep_r2": "False information / Scam",
            "rep_r3": "Hate speech / Harassment",
            "rep_r4": "Content unrelated to Carbon credits",
            "rep_r5": "Copyright / Privacy violation",
            "rep_r6": "Insulting individuals / organizations",
            "rep_r7": "Other...",
            "rep_other_lbl": "Please specify the reason:",
            "btn_submit_rep": "SUBMIT REPORT",
            "rep_msg": "Report received. Moderation team will process within 24h.",
            "btn_cancel": "CANCEL"
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

    st.markdown(f"<b style='color:#ef4444;'>{t['rep_reason_lbl']}</b>", unsafe_allow_html=True)
    rep_reasons = [t["rep_r1"], t["rep_r2"], t["rep_r3"], t["rep_r4"], t["rep_r5"], t["rep_r6"], t["rep_r7"]]
    choice = st.radio("Lý do báo cáo", rep_reasons, label_visibility="collapsed", key=f"rad_rep_{post_id}")
    
    if choice == t["rep_r7"]:
        st.text_input(t["rep_other_lbl"], key=f"txt_rep_{post_id}")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button(t["btn_cancel"], use_container_width=True):
            st.rerun()
    with c2:
        if st.button(t["btn_submit_rep"], type="primary", use_container_width=True):
            st.toast(t["rep_msg"])
            st.rerun()

def hien_thi_mang_xa_hoi(lang=None):
    if lang is None:
        lang = st.session_state.get("language", st.session_state.get("lang", st.session_state.get("current_lang", "Tiếng Việt")))
    
    if lang not in ["Tiếng Việt", "English"]:
        lang = "Tiếng Việt"

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
            "upload_lbl": "Đính kèm hình ảnh/tài liệu (Tùy chọn):",
            "btn_post": "ĐĂNG BÀI",
            "msg_success": "Đã đăng bài viết thành công.",
            "msg_warning": "Vui lòng nhập nội dung bài viết.",
            "news_feed": "BẢNG TIN CỘNG ĐỒNG",
            "no_post": "Chưa có bài viết nào.",
            "world": "Thế giới",
            "attached": "Tệp đính kèm",
            "download_doc": "Tải tài liệu",
            "likes": "Lượt thích",
            "comments": "Bình luận",
            "btn_like": "Thích",
            "btn_liked": "Đã thích",
            "btn_rep": "Báo cáo vi phạm",
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
            "upload_lbl": "Attach image/document (Optional):",
            "btn_post": "POST",
            "msg_success": "Post created successfully.",
            "msg_warning": "Please enter post content.",
            "news_feed": "COMMUNITY NEWS FEED",
            "no_post": "No posts yet.",
            "world": "Worldwide",
            "attached": "Attachment",
            "download_doc": "Download Document",
            "likes": "Likes",
            "comments": "Comments",
            "btn_like": "Like",
            "btn_liked": "Liked",
            "btn_rep": "Report Violation",
            "cmt_lbl": "INTERNAL COMMENTS:",
            "cmt_input": "Write a public comment...",
            "btn_send": "Send",
            "view_cmts": "View comments ({count})"
        }
    }
    t = T.get(lang, T["Tiếng Việt"])

    MOCK_T = {
        "Tiếng Việt": {
            "mock_p1_author": "Kỹ Sư Rừng Cà Mau",
            "mock_p1_role": "Chủ rừng / Kỹ sư MRV",
            "mock_p1_content": "Đợt đo kiểm viễn thám tháng này ghi nhận mật độ sinh khối ven biển tăng rất tốt, dữ liệu viễn thám đã khớp với chỉ số thực địa.",
            "mock_p1_c1_user": "Vinamilk Net-Zero",
            "mock_p1_c1_text": "Dự án rất triển vọng, bên mình đang quan tâm nguồn cung đợt tới.",
            "mock_p1_c2_user": "Nhà Đầu Tư Xanh",
            "mock_p1_c2_text": "Dữ liệu ảnh viễn thám rõ nét và minh bạch lắm.",
            "mock_p2_author": "Quỹ Đầu Tư Xanh",
            "mock_p2_role": "Nhà đầu tư từ xa",
            "mock_p2_content": "Chúng tôi đang thẩm định thêm 3 dự án tại khu vực Bắc Trung Bộ. Nền tảng hiển thị minh bạch giúp rút ngắn rất nhiều thời gian giải ngân.",
            "mock_p2_c1_user": "Bộ NN&PTNT",
            "mock_p2_c1_text": "Rất mong được hợp tác phát triển bền vững cùng quý quỹ.",
            "mock_world": "Thế giới"
        },
        "English": {
            "mock_p1_author": "Ca Mau Forest Engineer",
            "mock_p1_role": "Forest Owner / MRV Engineer",
            "mock_p1_content": "This month's remote sensing survey recorded very good coastal biomass growth; the satellite data matches the field indices perfectly.",
            "mock_p1_c1_user": "Vinamilk Net-Zero",
            "mock_p1_c1_text": "Very promising project, we are highly interested in the next supply batch.",
            "mock_p1_c2_user": "Green Investor",
            "mock_p1_c2_text": "The remote sensing image data is very clear and highly transparent.",
            "mock_p2_author": "Green Investment Fund",
            "mock_p2_role": "Remote Investor",
            "mock_p2_content": "We are appraising 3 additional projects in the North Central region. The transparent platform drastically shortens our disbursement time.",
            "mock_p2_c1_user": "MARD Vietnam",
            "mock_p2_c1_text": "We look forward to a sustainable development partnership with your fund.",
            "mock_world": "Worldwide"
        }
    }
    mt = MOCK_T.get(lang, MOCK_T["Tiếng Việt"])

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

        div[data-testid="stRadio"] div[role="radiogroup"] label div:first-child { display: none !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] label {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
            border: 1.5px solid #334155 !important;
            padding: 10px 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 0 #020617, 0 6px 12px rgba(0,0,0,0.4) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            margin-right: 15px !important; cursor: pointer !important; margin-bottom: 10px !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label div { color: #94a3b8 !important; font-weight: 700 !important; font-size: 0.95rem !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            background: linear-gradient(180deg, #38bdf8 0%, #0284c7 100%) !important; border-color: #7dd3fc !important;
            transform: translateY(-4px) !important; box-shadow: 0 8px 0 #075985, 0 12px 25px rgba(56, 189, 248, 0.6) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover div { color: #ffffff !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(180deg, #0284c7 0%, #0369a1 100%) !important; border-color: #38bdf8 !important;
            transform: translateY(2px) !important; box-shadow: 0 2px 0 #075985, 0 4px 10px rgba(2, 132, 199, 0.5) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) div { color: #ffffff !important; font-weight: 800 !important; }

        div[class*="st-key-btn_like_"] button {
            background: linear-gradient(180deg, #0284c7 0%, #0369a1 100%) !important; border: 1.5px solid #38bdf8 !important;
            border-radius: 10px !important; box-shadow: 0 5px 0 #075985, 0 8px 18px rgba(14, 165, 233, 0.45) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; padding: 6px 18px !important;
        }
        div[class*="st-key-btn_like_"] button p { color: #ffffff !important; font-weight: 800 !important; }
        div[class*="st-key-btn_like_"] button:hover {
            background: linear-gradient(180deg, #38bdf8 0%, #0284c7 100%) !important; border-color: #7dd3fc !important;
            transform: translateY(-4px) !important; box-shadow: 0 9px 0 #075985, 0 14px 26px rgba(56, 189, 248, 0.75) !important;
        }
        div[class*="st-key-btn_like_"] button:active { transform: translateY(4px) !important; box-shadow: 0 1px 0 #075985, 0 4px 10px rgba(56, 189, 248, 0.4) !important; }

        div[class*="st-key-btn_liked_"] button {
            background: linear-gradient(180deg, #22c55e 0%, #16a34a 100%) !important; border: 1.5px solid #4ade80 !important;
            border-radius: 10px !important; box-shadow: 0 5px 0 #15803d, 0 8px 18px rgba(34, 197, 94, 0.45) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; padding: 6px 18px !important;
        }
        div[class*="st-key-btn_liked_"] button p { color: #ffffff !important; font-weight: 800 !important; }
        div[class*="st-key-btn_liked_"] button:hover {
            background: linear-gradient(180deg, #4ade80 0%, #22c55e 100%) !important; border-color: #bbf7d0 !important;
            transform: translateY(-4px) !important; box-shadow: 0 9px 0 #15803d, 0 14px 26px rgba(34, 197, 94, 0.75) !important;
        }
        div[class*="st-key-btn_liked_"] button:active { transform: translateY(4px) !important; box-shadow: 0 1px 0 #15803d, 0 4px 10px rgba(34, 197, 94, 0.4) !important; }

        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(180deg, #22c55e 0%, #16a34a 100%) !important; border: 1.5px solid #4ade80 !important;
            border-radius: 10px !important; box-shadow: 0 5px 0 #15803d, 0 8px 18px rgba(34, 197, 94, 0.45) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }
        div[data-testid="stFormSubmitButton"] button p { color: #ffffff !important; font-weight: 800 !important; }
        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(180deg, #4ade80 0%, #22c55e 100%) !important; border-color: #bbf7d0 !important;
            transform: translateY(-4px) !important; box-shadow: 0 9px 0 #15803d, 0 14px 26px rgba(34, 197, 94, 0.75) !important;
        }
        div[data-testid="stFormSubmitButton"] button:active { transform: translateY(4px) !important; box-shadow: 0 1px 0 #15803d, 0 4px 10px rgba(34, 197, 94, 0.4) !important; }
        
        div[class*="st-key-btn_rep_"] button {
            background: linear-gradient(180deg, rgba(51, 65, 85, 0.8), rgba(30, 41, 59, 0.9)) !important; border: 1px solid rgba(148, 163, 184, 0.3) !important;
            border-radius: 10px !important; box-shadow: 0 4px 0 rgba(15, 23, 42, 0.8), 0 5px 10px rgba(0,0,0,0.3) !important;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }
        div[class*="st-key-btn_rep_"] button p { color: #94a3b8 !important; font-weight: 600 !important; }
        div[class*="st-key-btn_rep_"] button:hover {
            background: linear-gradient(180deg, rgba(239, 68, 68, 0.4), rgba(185, 28, 28, 0.6)) !important; border-color: rgba(248, 113, 113, 0.6) !important;
            transform: translateY(-3px) !important; box-shadow: 0 7px 0 rgba(153, 27, 27, 0.8), 0 10px 20px rgba(239, 68, 68, 0.4) !important;
        }
        div[class*="st-key-btn_rep_"] button:hover p { color: #fca5a5 !important; }
        div[class*="st-key-btn_rep_"] button:active { transform: translateY(4px) !important; box-shadow: 0 0px 0 rgba(153, 27, 27, 0.8), 0 2px 5px rgba(239, 68, 68, 0.2) !important; }

        .social-card { background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(72, 187, 120, 0.35); border-radius: 12px; padding: 20px 24px; margin-bottom: 20px; }
        .social-author { color: #48bb78; font-weight: 800; font-size: 1.05rem; }
        .social-meta { color: #64748b; font-size: 0.85rem; }
        .social-content { color: #f1f5f9; font-size: 1rem; line-height: 1.6; margin: 12px 0 14px 0; }
        .badge-room { display: inline-block; background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); padding: 2px 10px; border-radius: 6px; font-size: 0.78rem; font-weight: 700; margin-left: 8px; }
        .comment-thread { background: rgba(15, 23, 42, 0.55); border-left: 3px solid rgba(72, 187, 120, 0.6); border-radius: 0 8px 8px 0; padding: 10px 14px; margin-top: 8px; margin-bottom: 8px; }
        .comment-user { color: #38bdf8; font-weight: 700; font-size: 0.88rem; margin-bottom: 2px; }
        .comment-body { color: #e2e8f0; font-size: 0.92rem; line-height: 1.45; }
        .upload-badge { display: inline-block; margin-top: 8px; padding: 12px 16px; background: rgba(15, 23, 42, 0.6); border: 1.5px dashed #38bdf8; border-radius: 8px; color: #bae6fd; font-size: 0.9rem; margin-bottom: 12px; width: 100%; text-align: center; }
        .btn-download-doc { display: inline-block; background: #0ea5e9; color: white !important; font-weight: bold; text-decoration: none; padding: 6px 14px; border-radius: 6px; margin-top: 10px; font-size: 0.9rem; }
        .btn-download-doc:hover { background: #38bdf8; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="social-title-green">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="social-sub">{t["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown(f"<div style='color: #cbd5e1; font-weight: 600; font-size: 0.95rem; margin-bottom: 15px;'>{t['area_lbl']}</div>", unsafe_allow_html=True)
    
    phong_chon = st.radio("Khu vực thảo luận (ẩn)", [t["room_1"], t["room_2"], t["room_3"]], horizontal=True, label_visibility="collapsed")
    st.markdown("<br/>", unsafe_allow_html=True)

    if phong_chon == t["room_2"]:
        prov_list = ["Cà Mau", "Quảng Bình", "Lâm Đồng", "Hà Tĩnh", "Sơn La", "TP. Hồ Chí Minh"] if lang == "Tiếng Việt" else ["Ca Mau", "Quang Binh", "Lam Dong", "Ha Tinh", "Son La", "Ho Chi Minh City"]
        tinh_chon = st.selectbox(t["select_prov"], prov_list)
        room_label = f"Tỉnh {tinh_chon}" if lang == "Tiếng Việt" else f"{tinh_chon} Province"
    elif phong_chon == t["room_3"]:
        group_list = ["Kỹ sư viễn thám & MRV", "Nhà đầu tư thị trường", "Chủ rừng ngập mặn"] if lang == "Tiếng Việt" else ["Remote Sensing & MRV Engineers", "Market Investors", "Mangrove Forest Owners"]
        nhom_chon = st.selectbox(t["select_group"], group_list)
        room_label = nhom_chon
    else:
        room_label = t["world"]

    with st.container(border=True):
        st.markdown(f'<div style="color:#48bb78; font-weight:800; font-size:1.15rem; margin-bottom:12px;">{t["create_post"]}</div>', unsafe_allow_html=True)
        with st.form("form_post", clear_on_submit=True):
            placeholder_text = t["post_placeholder"].replace("{room}", room_label)
            post_content = st.text_area(t["post_content"], placeholder=placeholder_text)
            
            uploaded_file = st.file_uploader(t["upload_lbl"], accept_multiple_files=False)
            
            submitted = st.form_submit_button(t["btn_post"], use_container_width=True)
            if submitted:
                if post_content.strip() or uploaded_file is not None:
                    if "social_posts_mem" not in st.session_state:
                        st.session_state["social_posts_mem"] = []
                    
                    file_name = None
                    file_data = None
                    file_type = None
                    if uploaded_file:
                        file_name = uploaded_file.name
                        file_data = base64.b64encode(uploaded_file.getvalue()).decode()
                        file_type = uploaded_file.type

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
                        "file_name": file_name,
                        "file_data": file_data,
                        "file_type": file_type,
                        "likes": 0,
                        "liked_by": [],
                        "comments": []
                    }
                    st.session_state["social_posts_mem"].insert(0, new_p)
                    st.success(t["msg_success"])
                    st.rerun()
                else:
                    st.warning(t["msg_warning"])

    st.markdown(f'<div class="social-title-green" style="font-size:1.4rem; margin-top:35px; margin-bottom:20px;">{t["news_feed"]}</div>', unsafe_allow_html=True)

    if "social_posts_mem" not in st.session_state or (st.session_state["social_posts_mem"] and st.session_state["social_posts_mem"][-1].get("author") == "Kỹ Sư Rừng Cà Mau"):
        st.session_state["social_posts_mem"] = [
            {
                "id": "p_default_1", "author": "mock_p1_author", "role": "mock_p1_role", "content": "mock_p1_content",
                "time": "08/10/2026 14:20", "room": "mock_world", "likes": 24, "liked_by": [],
                "file_name": None, "file_data": None, "file_type": None,
                "comments": [{"user": "mock_p1_c1_user", "text": "mock_p1_c1_text"}, {"user": "mock_p1_c2_user", "text": "mock_p1_c2_text"}]
            },
            {
                "id": "p_default_2", "author": "mock_p2_author", "role": "mock_p2_role", "content": "mock_p2_content",
                "time": "07/10/2026 09:15", "room": "mock_world", "likes": 18, "liked_by": [],
                "file_name": None, "file_data": None, "file_type": None,
                "comments": [{"user": "mock_p2_c1_user", "text": "mock_p2_c1_text"}]
            }
        ]

    posts = st.session_state["social_posts_mem"]
    if not posts:
        st.info(t["no_post"])
        return

    cur_user = st.session_state.get("current_user", "Anonymous" if lang == "English" else "Ẩn danh")

    for idx, p in enumerate(posts):
        display_author = mt.get(p["author"], p["author"]) if p["author"].startswith("mock_") else p["author"]
        display_role = mt.get(p["role"], p["role"]) if p["role"].startswith("mock_") else p["role"]
        display_content = mt.get(p["content"], p["content"]) if p["content"].startswith("mock_") else p["content"]
        display_room = mt.get(p.get("room", ""), p.get("room", t["world"])) if p.get("room", "").startswith("mock_") else p.get("room", t["world"])
        
        file_html = ""
        if p.get("file_name") and p.get("file_data"):
            f_type = str(p.get("file_type", ""))
            if f_type.startswith("image/"):
                file_html = f"""
                <div style="margin-top: 15px; margin-bottom: 5px; text-align: center;">
                    <img src="data:{f_type};base64,{p['file_data']}" style="max-width: 100%; border-radius: 12px; border: 1.5px solid rgba(56, 189, 248, 0.4); box-shadow: 0 4px 15px rgba(0,0,0,0.5);" />
                </div>
                """
            else:
                file_html = f"""
                <div class='upload-badge'>
                    <div style="margin-bottom: 5px;">📎 {t['attached']}: <b style="color: #ffffff;">{p['file_name']}</b></div>
                    <a href="data:{f_type};base64,{p['file_data']}" download="{p['file_name']}" class="btn-download-doc">📥 {t['download_doc']}</a>
                </div>
                """

        html_card = f"""<div class="social-card">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div>
<span class="social-author">{display_author}</span> 
<span style="color:#94a3b8; font-size:0.85rem;">({display_role})</span>
<span class="badge-room">{display_room}</span>
</div>
<span class="social-meta">{p['time']}</span>
</div>
<div class="social-content">{display_content}</div>
{file_html}
<div style="color:#94a3b8; font-size:0.88rem; margin-top:12px; margin-bottom:12px;">
{t['likes']}: <b style="color:#38bdf8;">{p['likes']}</b> &nbsp;|&nbsp; 
{t['comments']}: <b style="color:#48bb78;">{len(p.get('comments', []))}</b>
</div>
</div>"""
        st.markdown(html_card, unsafe_allow_html=True)
        
        liked_list = p.setdefault("liked_by", [])
        is_liked = cur_user in liked_list

        c_like, c_rep, _ = st.columns([0.22, 0.28, 0.5])
        with c_like:
            if is_liked:
                if st.button(f"✅ {t['btn_liked']} ({p['likes']})", key=f"btn_liked_{p['id']}_{idx}"):
                    p["likes"] -= 1
                    p["liked_by"].remove(cur_user)
                    st.rerun()
            else:
                if st.button(f"👍 {t['btn_like']} ({p['likes']})", key=f"btn_like_{p['id']}_{idx}"):
                    p["likes"] += 1
                    p["liked_by"].append(cur_user)
                    st.rerun()
        
        with c_rep:
            if st.button(t["btn_rep"], key=f"btn_rep_open_{p['id']}_{idx}"):
                hien_thi_hop_thoai_bao_cao(p['id'], lang)

        comments_list = p.get("comments", [])
        with st.expander(t["view_cmts"].replace("{count}", str(len(comments_list))), expanded=False):
            if comments_list:
                st.markdown(f"<div style='margin-bottom:5px; font-weight:700; color:#94a3b8; font-size:0.88rem;'>{t['cmt_lbl']}</div>", unsafe_allow_html=True)
                for cm in comments_list:
                    if isinstance(cm, dict):
                        raw_u = cm.get("user", "")
                        raw_t = cm.get("text", "")
                    else:
                        parts = str(cm).split(":", 1)
                        raw_u = parts[0] if len(parts) > 1 else ""
                        raw_t = parts[1] if len(parts) > 1 else str(cm)
                    
                    u_c = mt.get(raw_u, raw_u) if raw_u.startswith("mock_") else (raw_u if raw_u else ("Member" if lang == "English" else "Thành viên"))
                    t_c = mt.get(raw_t, raw_t) if raw_t.startswith("mock_") else raw_t
                        
                    html_cmt = f"""<div class="comment-thread">
<div class="comment-user">{u_c}</div>
<div class="comment-body">{t_c}</div>
</div>"""
                    st.markdown(html_cmt, unsafe_allow_html=True)
            else:
                st.caption(t["no_post"])

            with st.form(f"form_quick_cmt_{p['id']}_{idx}", clear_on_submit=True):
                col_in, col_btn = st.columns([0.82, 0.18])
                with col_in:
                    new_c_txt = st.text_input(t["cmt_input"], placeholder=t["cmt_input"], label_visibility="collapsed")
                with col_btn:
                    btn_send_c = st.form_submit_button(t["btn_send"], use_container_width=True)
                
                if btn_send_c and new_c_txt.strip():
                    p.setdefault("comments", []).append({"user": cur_user, "text": new_c_txt.strip()})
                    st.rerun()

        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
