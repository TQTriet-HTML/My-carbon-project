import streamlit as st
import re

CORE_DICTIONARY = {
    # Điều hướng & Chung
    "NỀN TẢNG MRV & SÀN GIAO DỊCH": "MRV PLATFORM & CARBON EXCHANGE",
    "ĐĂNG XUẤT": "LOGOUT",
    "TÙY CHỌN NGÔN NGỮ": "LANGUAGE SETTINGS",
    "ĐỐI TÁC CHIẾN LƯỢC": "STRATEGIC PARTNERS",
    "CHỨNG NHẬN PHÁP LÝ": "LEGAL CERTIFICATIONS",
    "Đối tác Không gian AI": "AI Spatial Partner",
    "Thanh toán Escrow": "Escrow Payment",
    "Tiêu chuẩn Toàn cầu": "Global Standard",
    "Bảo mật Thông tin Cấp cao": "High-Grade Information Security",
    "Xin chào": "Welcome",
    
    # Tabs
    "Hệ thống MRV": "MRV System",
    "Sàn Giao dịch": "Marketplace",
    "Đầu tư Trồng rừng": "Forest Investment",
    "Mạng xã hội": "Social Network",
    "Nhật ký Xanh": "Green Diary",
    "Bảng Vàng": "Leaderboard",
    "Về chúng tôi": "About Us",

    # Tab MRV
    "HỆ THỐNG GIÁM SÁT KHÔNG GIAN AI": "AI SPATIAL MONITORING SYSTEM",
    "Năm cơ sở:": "Base Year:",
    "Năm so sánh:": "Comparison Year:",
    "PHÂN TÍCH VÙNG KHOANH": "ANALYZE SELECTED AREA",
    "LÀM MỚI DỮ LIỆU": "REFRESH DATA",
    "KẾT QUẢ PHÂN TÍCH ĐỊNH LƯỢNG": "QUANTITATIVE ANALYSIS RESULT",
    "Sinh khối Năm": "Biomass in Year",
    "Tổng Giá Trị Quy Đổi": "Total Converted Value",
    "Đổi sang USD": "Switch to USD",
    "Đổi sang VND": "Switch to VND",
    "Tấn": "Tons",
    "Tín chỉ": "Credits",

    # Sàn giao dịch & Dashboard
    "DASHBOARD QUẢN LÝ TÀI KHOẢN": "ACCOUNT MANAGEMENT DASHBOARD",
    "Số Dư Ví Hệ Thống": "System Wallet Balance",
    "Tổng Tín Chỉ Sở Hữu": "Total Owned Credits",
    "Hạng Tín Nhiệm (ESG)": "ESG Rating",
    "Đã bù trừ": "Offset Complete",
    "Đạt chuẩn": "Standard Qualified",
    "XEM CHI TIẾT KHO TÍN CHỈ": "VIEW CREDIT VAULT DETAILS",
    "BIỂU ĐỒ GIÁ TÍN CHỈ GIAO NGAY": "SPOT CARBON CREDIT PRICE CHART",
    "Khung thời gian phân tích:": "Analysis Timeframe:",
    "Từng ngày": "Daily",
    "Từng tháng": "Monthly",
    "Từng năm": "Yearly",
    "Giá tham chiếu hiện tại:": "Current Reference Price:",
    "trong phiên": "in session",
    "TRUNG TÂM KHỚP LỆNH THEO VAI TRÒ": "ROLE-BASED ORDER MATCHING CENTER",
    "VAI TRÒ HIỆN TẠI:": "CURRENT ROLE:",
    "XÁC NHẬN MUA TÍN CHỈ": "CONFIRM CREDIT PURCHASE",
    "NIÊM YẾT LÊN SÀN GIAO DỊCH": "LIST ON EXCHANGE",
    "XÁC NHẬN ĐẦU TƯ CỔ PHẦN RỪNG": "CONFIRM FOREST EQUITY INVESTMENT",
    "DANH SÁCH DỰ ÁN ĐANG NIÊM YẾT": "LISTED PROJECTS DIRECTORY",
    "Đơn giá giao dịch:": "Trading Unit Price:",
    "Tổng chi phí thanh toán:": "Total Payment Cost:",
    "Quy đổi VND:": "Equivalent in VND:",
    "Khả dụng:": "Available:",

    # Mạng xã hội
    "MẠNG XÃ HỘI TÍN CHỈ CARBON": "CARBON CREDIT SOCIAL NETWORK",
    "Nơi cộng đồng kết nối, chia sẻ kiến thức và lan tỏa giá trị Net-Zero": "Connecting community, sharing knowledge and spreading Net-Zero values",
    "Khu vực thảo luận:": "Discussion Channel:",
    "Phòng Thế giới (Toàn cầu)": "Global Channel",
    "Phòng Tỉnh thành (Địa phương)": "Provincial Channel",
    "Phòng Nhóm dự án riêng": "Project Team Channel",
    "TẠO BÀI VIẾT MỚI": "CREATE NEW POST",
    "Nội dung bài viết:": "Post content:",
    "ĐĂNG BÀI": "PUBLISH POST",
    "BẢNG TIN CỘNG ĐỒNG": "COMMUNITY FEED",
    "Thích": "Like",
    "Báo cáo vi phạm": "Report",
    "BÌNH LUẬN NỘI BỘ:": "INTERNAL COMMENTS:",
    "Viết bình luận công khai...": "Write a public comment...",
    "Gửi": "Send",
    "Lượt thích:": "Likes:",
    "Bình luận:": "Comments:",
    "Thế giới": "Global",

    # Nhật ký Xanh
    "NHẬT KÝ XANH - LỊCH TRÌNH MRV": "GREEN DIARY - MRV SCHEDULE",
    "Tháng:": "Month:",
    "Năm (Phạm vi 10 năm):": "Year (10-year range):",
    "Thời điểm hiện tại:": "Current Time:",
    "Đỏ: Quan trọng": "Red: Important",
    "Cam: Bất thường": "Orange: Abnormal",
    "Xanh: Định kỳ": "Green: Periodic",
    "Thứ 2": "Mon",
    "Thứ 3": "Tue",
    "Thứ 4": "Wed",
    "Thứ 5": "Thu",
    "Thứ 6": "Fri",
    "Thứ 7": "Sat",
    "Chủ Nhật": "Sun",
    "Danh sách nhật ký đã ghi:": "Logged Diary Entries:",
    "Ghi nhận sự kiện hoặc lịch trình mới": "Record New Event or Schedule",
    "Chọn ngày sự kiện (Từ 5 năm trước đến 5 năm sau):": "Select Event Date (From 5 years prior to 5 years after):",
    "Tiêu đề sự kiện:": "Event Title:",
    "Phân loại sự kiện (Ô ngày sẽ tự động đổi màu theo phân loại này):": "Event Category (Date box auto-colors based on this):",
    "Nội dung chi tiết:": "Detailed Description:",
    "LƯU VÀO NHẬT KÝ": "SAVE TO DIARY",
    "Quan trọng": "Important",
    "Bất thường": "Abnormal",
    "Định kỳ": "Periodic",

    # Về chúng tôi
    "VỀ CHÚNG TÔI & LỘ TRÌNH PHÁT TRIỂN": "ABOUT US & DEVELOPMENT ROADMAP",
    "SỨ MỆNH & TẦM NHÌN": "MISSION & VISION",
    "CÔNG NGHỆ LÕI": "CORE TECHNOLOGY",
    "LỘ TRÌNH PHÁT TRIỂN (ROADMAP 2026 - 2030)": "ROADMAP (2026 - 2030)",
    "Nền tảng được xây dựng với mục tiêu thương mại hóa và minh bạch hóa thị trường tín chỉ carbon tại Việt Nam. Bằng cách kết hợp dữ liệu viễn thám vệ tinh đa quang phổ (Copernicus Sentinel-2) cùng mô hình trí tuệ nhân tạo (AI), chúng tôi số hóa quy trình kiểm kê MRV (Measurement, Reporting, and Verification), xóa bỏ rào cản chi phí cao và thời gian thẩm định kéo dài của các phương pháp thủ công truyền thống.": 
        "The platform is engineered to commercialize and bring transparency to Vietnam's carbon credit market. By unifying multi-spectral satellite remote sensing (Copernicus Sentinel-2) with artificial intelligence (AI), we digitize the Measurement, Reporting, and Verification (MRV) process, overcoming high costs and lengthy validation periods of traditional methods.",
    "Xử lý dữ liệu không gian thời gian thực trên quy mô cấp tỉnh và toàn quốc với độ trễ cực thấp.":
        "Real-time geospatial big data processing at provincial and nationwide scales with ultra-low latency.",
    "Thuật toán máy học tự động bóc tách chỉ số thực vật NDVI và tính toán độ che phủ sinh khối rừng.":
        "Machine learning algorithms automate NDVI vegetation index extraction and forest biomass density calculations.",
    "Cơ chế giao dịch ký quỹ tự động bảo đảm quyền lợi tài chính an toàn tuyệt đối cho người mua và chủ rừng.":
        "Automated escrow clearing mechanism ensuring absolute financial security for both buyers and forest owners.",
    "Giai đoạn 1 (2026):": "Phase 1 (2026):",
    "Hoàn thiện hệ sinh thái kiểm kê tự động MRV, kết nối dữ liệu thí điểm các vùng rừng ngập mặn Cà Mau và rừng phòng hộ Bắc Trung Bộ.":
        "Complete automated MRV framework; integrate pilot spatial datasets across Ca Mau mangroves and North Central watershed forests.",
    "Giai đoạn 2 (2027 - 2028):": "Phase 2 (2027 - 2028):",
    "Tích hợp sàn giao dịch thứ cấp cho các doanh nghiệp FDI, niêm yết chứng chỉ tiêu chuẩn Verra/Gold Standard.":
        "Integrate secondary trading exchange for multinational FDI corporations; list international Verra and Gold Standard certifications.",
    "Giai đoạn 3 (2029 - 2030):": "Phase 3 (2029 - 2030):",
    "Mở rộng quy mô ra toàn khu vực Đông Nam Á, trở thành trung tâm giao dịch hạn ngạch phát thải hàng đầu.":
        "Scale coverage across Southeast Asia, establishing the premier regional emission reduction quota exchange."
}

def t(text: str) -> str:
    current_lang = st.session_state.get("current_lang", "Tiếng Việt")
    if current_lang == "Tiếng Việt":
        return text

    cleaned = text.strip()
    if cleaned in CORE_DICTIONARY:
        return CORE_DICTIONARY[cleaned]

    res = text
    # Dịch các cấu trúc chứa ngày tháng
    match_thang_nam = re.search(r"THÁNG\s*(\d+)\s*NĂM\s*(\d+)", res, re.IGNORECASE)
    if match_thang_nam:
        return f"MONTH {match_thang_nam.group(1)} YEAR {match_thang_nam.group(2)}"

    match_ngay = re.search(r"Ngày\s*(\d{4}-\d{2}-\d{2})", res)
    if match_ngay:
        res = res.replace(f"Ngày {match_ngay.group(1)}", f"Date {match_ngay.group(1)}")

    # Dịch các thông báo MRV động
    match_msg_pos = re.search(r"Khu vực phân tích ghi nhận sự tăng trưởng sinh khối\. Bạn có thể niêm yết thêm (.*?) tín chỉ carbon\.", res)
    if match_msg_pos:
        diff_str = match_msg_pos.group(1).replace("Tấn", "Tons")
        return f"Biomass growth detected in analyzed area. You can list {diff_str} additional carbon credits."

    if "Mật độ sinh khối trong khu vực sụt giảm" in res:
        return "Biomass density decreased in the analyzed area. Forest inspection required."

    match_sinh_khoi = re.search(r"Sinh khối Năm\s*(\d{4})", res)
    if match_sinh_khoi:
        return f"Biomass in Year {match_sinh_khoi.group(1)}"

    for vi, en in CORE_DICTIONARY.items():
        if vi in res:
            res = res.replace(vi, en)

    res = re.sub(r'(\b\d[\d,\.]*)\s*Tấn\b', r'\1 Tons', res)
    res = re.sub(r'(\b\d[\d,\.]*)\s*Tín chỉ\b', r'\1 Credits', res)

    return res
