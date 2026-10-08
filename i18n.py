import streamlit as st
import re

# Từ điển ánh xạ từ vựng và cụm từ động cốt lõi
TRANSLATION_MAP = {
    # Điều hướng & Chung
    "NỀN TẢNG MRV & SÀN GIAO DỊCH": "MRV PLATFORM & CARBON EXCHANGE",
    "ĐĂNG XUẤT": "LOGOUT",
    "TÙY CHỌN NGÔN NGỮ": "LANGUAGE SETTINGS",
    "Hệ thống MRV": "MRV System",
    "Sàn Giao dịch": "Marketplace",
    "Đầu tư Trồng rừng": "Forest Investment",
    "Mạng xã hội": "Social Network",
    "Nhật ký Xanh": "Green Diary",
    "Bảng Vàng": "Leaderboard",
    "Về chúng tôi": "About Us",
    "Xin chào": "Welcome",
    "Hôm nay": "Today",
    "ĐỐI TÁC CHIẾN LƯỢC": "STRATEGIC PARTNERS",
    "CHỨNG NHẬN PHÁP LÝ": "LEGAL CERTIFICATIONS",

    # Hộp thoại Đăng xuất
    "Bạn có chắc muốn tạm nghỉ chân sau một chặng đường xanh đã qua không?": "Are you sure you want to take a break after your green journey?",
    "Tạm thời nghỉ chân": "Take a Break",
    "Tiếp tục chặng đường": "Continue Journey",

    # Bảng Vàng & Tôn Vinh
    "BẢNG VÀNG & TÔN VINH": "LEADERBOARD & HONORS",
    "TOP DOANH NGHIỆP": "TOP CORPORATES",
    "TOP DỰ ÁN TRỒNG RỪNG": "TOP FORESTRY PROJECTS",
    "Hạng": "Rank",
    "Doanh Nghiệp": "Enterprise",
    "Tín chỉ": "Credits",
    "Dự Án": "Project",
    "QUÁ TRÌNH SỐNG XANH": "GREEN MILESTONE PROGRESSION",
    "CẤP ĐỘ HIỆN TẠI": "CURRENT TIER",
    "TIẾN TRÌNH LÊN CẤP KẾ TIẾP": "PROGRESS TO NEXT TIER",
    "YÊU CẦU ĐỂ THĂNG CẤP TIẾP THEO": "REQUIREMENTS FOR NEXT LEVEL",

    # Phân loại tài khoản & Cấp bậc
    "Doanh nghiệp mua tín chỉ": "Credit Buyer Enterprise",
    "Chủ rừng / Kỹ sư MRV": "Forest Owner / MRV Engineer",
    "Nhà đầu tư từ xa (Cổ đông)": "Remote Investor (Shareholder)",
    "Doanh nghiệp Tiên Phong Xanh": "Green Pioneer Enterprise",
    "Đại Sứ Net-Zero": "Net-Zero Ambassador",
    "Kỹ Sư Kiến Tạo Sinh Khối": "Biomass Architect Engineer",
    "Đại Sứ Bảo Tồn Rừng": "Forest Conservation Ambassador",
    "Nhà Đầu Tư Sinh Thái Cấp 1": "Tier 1 Eco-Investor",
    "Cổ Đông Bảo Trợ Rừng Xanh": "Green Forest Patron Shareholder",
    "Rừng ngập mặn Cà Mau": "Ca Mau Mangrove Forest",
    "Dự án Bắc Trung Bộ": "North Central Project",
    "KBT Nam Cát Tiên": "Nam Cat Tien Sanctuary",

    # Dashboard & Sàn
    "DASHBOARD QUẢN LÝ TÀI KHOẢN": "ACCOUNT MANAGEMENT DASHBOARD",
    "Số Dư Ví Hệ Thống": "System Wallet Balance",
    "Tổng Tín Chỉ Sở Hữu": "Total Owned Credits",
    "Hạng Tín Nhiệm (ESG)": "ESG Credit Rating",
    "Đã bù trừ": "Offset Complete",
    "Đạt chuẩn": "Standard Qualified",
    "XEM CHI TIẾT KHO TÍN CHỈ": "VIEW CREDIT VAULT DETAILS",
    "BIỂU ĐỒ GIÁ TÍN CHỈ GIAO NGAY": "SPOT CARBON CREDIT PRICE CHART",
    "TRUNG TÂM KHỚP LỆNH THEO VAI TRÒ": "ROLE-BASED ORDER MATCHING CENTER",
    "DANH SÁCH DỰ ÁN ĐANG NIÊM YẾT": "CURRENTLY LISTED PROJECTS"
}

def t(text: str) -> str:
    """Hàm dịch tự động thông minh: Dịch chính xác hoặc tự động chuyển ngữ theo ngữ cảnh."""
    current_lang = st.session_state.get("current_lang", "Tiếng Việt")
    if current_lang == "Tiếng Việt":
        return text

    # Nếu có sẵn trong từ điển khớp tuyệt đối
    if text in TRANSLATION_MAP:
        return TRANSLATION_MAP[text]

    # Quy tắc dịch thay thế từ khóa linh hoạt cho các đoạn văn bản dài
    translated = text
    for vn_word, en_word in TRANSLATION_MAP.items():
        if vn_word in translated:
            translated = translated.replace(vn_word, en_word)
            
    # Chuyển đổi định dạng số và đơn vị tự động
    translated = re.sub(r'(\d+)\s*Tấn', r'\1 Tons', translated)
    translated = re.sub(r'(\d+)\s*Tín chỉ', r'\1 Credits', translated)
    translated = translated.replace("Hôm nay:", "Today:").replace("Ngày:", "Date:").replace("Tháng", "Month").replace("Năm", "Year")
    return translated
