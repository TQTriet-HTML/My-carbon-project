import streamlit as st
import re

# Từ điển đối chiếu toàn vẹn các cụm từ trong toàn hệ thống
CORE_DICTIONARY = {
    # Điều hướng, Header & Sidebar
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
    
    # Các Tabs
    "Hệ thống MRV": "MRV System",
    "Sàn Giao dịch": "Marketplace",
    "Đầu tư Trồng rừng": "Forest Investment",
    "Mạng xã hội": "Social Network",
    "Nhật ký Xanh": "Green Diary",
    "Bảng Vàng": "Leaderboard",
    "Về chúng tôi": "About Us",

    # Tab Hệ thống MRV
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
    "AI đang phân tích dữ liệu không gian...": "AI is analyzing spatial satellite data...",
    "Sinh khối": "Biomass",
    "Đang chạy ở chế độ giả lập cục bộ do thiếu Token GEE hợp lệ.": "Running in local simulation mode due to missing GEE Token.",
    
    # Hộp thoại Đăng xuất
    "Bạn có chắc muốn tạm nghỉ chân sau một chặng đường xanh đã qua không?": "Are you sure you want to pause after your green journey?",
    "Tạm thời nghỉ chân": "Take a Break",
    "Tiếp tục chặng đường": "Continue Journey",

    # Dashboard & Thị trường
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
    "DANH SÁCH DỰ ÁN ĐANG NIÊM YẾT": "LISTED PROJECTS DIRECTORY",

    # Vai trò & Người dùng
    "Chủ rừng / Kỹ sư MRV": "Forest Owner / MRV Engineer",
    "Nhà đầu tư từ xa (Cổ đông)": "Remote Investor (Shareholder)",
    "Doanh nghiệp mua tín chỉ": "Credit Buyer Enterprise",
    
    # Bảng Vàng & Tiến trình
    "BẢNG VÀNG & TÔN VINH": "LEADERBOARD & HONORS",
    "TOP DOANH NGHIỆP": "TOP CORPORATES",
    "TOP DỰ ÁN TRỒNG RỪNG": "TOP FORESTRY PROJECTS",
    "Hạng": "Rank",
    "Doanh Nghiệp": "Enterprise",
    "Dự Án": "Project",
    "QUÁ TRÌNH SỐNG XANH": "GREEN MILESTONE PROGRESSION",
    "CẤP ĐỘ HIỆN TẠI": "CURRENT TIER",
    "TIẾN TRÌNH LÊN CẤP KẾ TIẾP": "PROGRESS TO NEXT TIER",
    "YÊU CẦU ĐỂ THĂNG CẤP TIẾP THEO": "REQUIREMENTS FOR NEXT LEVEL",
    "hoàn thành chặng đường thăng hạng.": "completed towards rank promotion."
}

def t(text: str) -> str:
    """Hàm chuyển ngữ tự động toàn diện và chuẩn xác."""
    current_lang = st.session_state.get("current_lang", "Tiếng Việt")
    if current_lang == "Tiếng Việt":
        return text

    # Lớp 1: Khớp chuẩn xác theo từ điển toàn văn
    cleaned = text.strip()
    if cleaned in CORE_DICTIONARY:
        return CORE_DICTIONARY[cleaned]

    res = text

    # Lớp 2: Xử lý các câu thông báo động chứa tham số số lượng / năm
    match_msg_pos = re.search(r"Khu vực phân tích ghi nhận sự tăng trưởng sinh khối\. Bạn có thể niêm yết thêm (.*?) tín chỉ carbon\.", res)
    if match_msg_pos:
        diff_str = match_msg_pos.group(1).replace("Tấn", "Tons")
        return f"Biomass growth detected in analyzed area. You can list {diff_str} additional carbon credits."

    if "Mật độ sinh khối trong khu vực sụt giảm" in res:
        return "Biomass density decreased in the analyzed area. Forest inspection required."

    match_sinh_khoi = re.search(r"Sinh khối Năm\s*(\d{4})", res)
    if match_sinh_khoi:
        return f"Biomass in Year {match_sinh_khoi.group(1)}"

    # Lớp 3: Thay thế các cụm từ chuẩn đã biết
    for vi, en in CORE_DICTIONARY.items():
        if vi in res:
            res = res.replace(vi, en)

    # Chuẩn hóa đơn vị đo lường
    res = re.sub(r'(\b\d[\d,\.]*)\s*Tấn\b', r'\1 Tons', res)
    res = re.sub(r'(\b\d[\d,\.]*)\s*Tín chỉ\b', r'\1 Credits', res)

    return res
