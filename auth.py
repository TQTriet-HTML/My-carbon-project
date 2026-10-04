import streamlit as st

# Giả lập cơ sở dữ liệu người dùng
USERS = {
    "admin": {"password": "123", "role": "Chủ rừng / Kỹ sư MRV"},
    "investor": {"password": "123", "role": "Nhà đầu tư từ xa (Cổ đông)"},
    "buyer": {"password": "123", "role": "Doanh nghiệp mua tín chỉ"}
}

def load_users():
    return USERS

def hien_thi_cong_dang_nhap():
    # --- CSS SIÊU HOẠT HỌA CHO TRANG ĐĂNG NHẬP ---
    st.markdown("""
        <style>
        /* Đặt hình nền mờ ảo cho toàn bộ ứng dụng khi ở trang đăng nhập */
        .stApp {
            background-image: linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.9)), 
                              url('https://images.unsplash.com/photo-1511497584788-876760111969?q=80&w=2532&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        
        /* Hiệu ứng Slogan nảy từng chữ */
        .bouncing-slogan {
            text-align: center;
            margin-bottom: 30px;
        }
        .bouncing-slogan span {
            display: inline-block;
            font-size: 2.2rem;
            font-weight: 900;
            color: #48bb78;
            text-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
            transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275), color 0.2s;
            cursor: default;
        }
        .bouncing-slogan span:hover {
            transform: translateY(-12px) scale(1.1);
            color: #63b3ed;
            text-shadow: 0 8px 20px rgba(99, 179, 237, 0.6);
        }

        /* Khối Đăng nhập & Tạo tài khoản (Glassmorphism + Shine Effect) */
        div[data-testid="stTabs"] {
            background: rgba(30, 41, 59, 0.65);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
            transition: transform 0.4s ease, box-shadow 0.4s ease;
        }
        
        div[data-testid="stTabs"]:hover {
            transform: translateY(-8px);
            box-shadow: 0 30px 60px -12px rgba(72, 187, 120, 0.3);
            border-color: rgba(72, 187, 120, 0.4);
        }

        /* Tia sáng lướt qua khi Hover */
        div[data-testid="stTabs"]::before {
            content: '';
            position: absolute;
            top: 0; left: -150%;
            width: 50%; height: 100%;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent);
            transform: skewX(-25deg);
            transition: 0.7s;
            z-index: 1;
            pointer-events: none;
        }
        div[data-testid="stTabs"]:hover::before {
            left: 150%;
        }

        /* Thanh Bảng tin (News Ticker) cố định ở đáy màn hình */
        .news-ticker-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: rgba(15, 23, 42, 0.95);
            color: #a0aec0;
            padding: 10px 0;
            border-top: 1px solid #2d3748;
            font-size: 0.95rem;
            z-index: 9999;
            box-shadow: 0 -5px 15px rgba(0,0,0,0.3);
        }
        .news-ticker-content a {
            color: #63b3ed;
            text-decoration: none;
            font-weight: 600;
            margin: 0 30px;
        }
        .news-ticker-content a:hover {
            color: #48bb78;
            text-decoration: underline;
        }
        
        /* Chào mừng nhẹ nhàng */
        .welcome-text {
            text-align: center;
            color: #e2e8f0;
            font-size: 1.1rem;
            margin-bottom: 20px;
            font-weight: 300;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- RENDER SLOGAN "MỘT CÚ CHẠM - VẠN ĐIỀU XANH" ---
    slogan = "MỘT CÚ CHẠM - VẠN ĐIỀU XANH"
    html_slogan = "".join([f"<span>{c}</span>" if c != ' ' else "&nbsp;" for c in slogan])
    st.markdown(f'<div class="bouncing-slogan">{html_slogan}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="welcome-text">🌱 Chào mừng bạn đến với Nền tảng Giao dịch Tín chỉ Carbon tiên phong. Nơi công nghệ AI vệ tinh gặp gỡ sứ mệnh bảo vệ Trái Đất.</div>', unsafe_allow_html=True)

    # Căn giữa Form đăng nhập
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab_login, tab_register = st.tabs(["🔐 Đăng nhập", "✨ Tạo tài khoản mới"])
        
        with tab_login:
            st.markdown("### 🚪 Truy cập Hệ thống")
            tendangnhap = st.text_input("Tên đăng nhập", placeholder="Nhập admin, investor, hoặc buyer")
            matkhau = st.text_input("Mật khẩu", type="password", placeholder="Nhập 123")
            
            if st.button("🚀 Đăng nhập vào Nền tảng", type="primary", use_container_width=True):
                users = load_users()
                if tendangnhap in users and users[tendangnhap]["password"] == matkhau:
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = tendangnhap
                    st.session_state["current_role"] = users[tendangnhap]["role"]
                    st.rerun()
                else:
                    st.error("❌ Sai tên đăng nhập hoặc mật khẩu.")
                    
        with tab_register:
            st.markdown("### 🌱 Tham gia Cộng đồng Xanh")
            st.info("💡 **Bạn đã có tài khoản chưa?**\n\nNếu chưa thì hãy tạo một tài khoản mới để góp phần vào công cuộc xây dựng một tương lai xanh nhé! Mỗi tài khoản mới là một nhịp cầu nối liền nhà đầu tư và chủ rừng.")
            
            new_user = st.text_input("Tên đăng nhập mới")
            new_pass = st.text_input("Mật khẩu mới", type="password")
            new_role = st.selectbox("Vai trò của bạn:", ["Doanh nghiệp mua tín chỉ", "Nhà đầu tư từ xa (Cổ đông)", "Chủ rừng / Kỹ sư MRV"])
            
            if st.button("🌟 Khởi tạo Tài khoản & Bắt đầu", type="primary", use_container_width=True):
                st.success(f"🎉 Chúc mừng! Tài khoản `{new_user}` đã được tạo thành công. Vui lòng quay lại tab Đăng nhập.")

    # --- BẢNG TIN TỨC CHẠY DƯỚI CÙNG (MARQUEE) ---
    st.markdown("""
        <div class="news-ticker-container">
            <marquee class="news-ticker-content" scrollamount="6" onmouseover="this.stop();" onmouseout="this.start();">
                🚀 <b>TIN TỨC MỚI NHẤT:</b> 
                <a href="#">Thị trường Tín chỉ Carbon Việt Nam chính thức vận hành thử nghiệm vào 2025.</a> | 
                <a href="#">Google Earth Engine công bố bản cập nhật thuật toán sinh khối mới, tăng độ chính xác lên 98%.</a> | 
                <a href="#">Báo cáo Net-Zero 2026: Nhu cầu tín chỉ carbon toàn cầu dự kiến tăng 150%.</a> |
                <a href="#">Quỹ Đầu tư Tác động (Impact Fund) cam kết rót 10 triệu USD vào các dự án trồng rừng ngập mặn.</a>
            </marquee>
        </div>
    """, unsafe_allow_html=True)
