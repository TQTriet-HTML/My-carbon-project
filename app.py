import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import st_folium
import os

from auth import hien_thi_cong_dang_nhap
from marketplace import hien_thi_san_giao_dich, hien_thi_cong_dau_tu, hien_thi_gioi_thieu_va_goi_von

try:
    from social import hien_thi_mang_xa_hoi
    from community import hien_thi_vinh_danh_va_gop_y
except ImportError:
    def hien_thi_mang_xa_hoi(): st.info("Mạng xã hội đang được bảo trì.")
    def hien_thi_vinh_danh_va_gop_y(): st.info("Cộng đồng đang được bảo trì.")

st.set_page_config(page_title="MRV & Carbon Exchange", layout="wide", page_icon="🌍")

LANG_DICT = {
    "Tiếng Việt": {
        "title": "🌍 NỀN TẢNG MRV & SÀN GIAO DỊCH", "logout": "🚪 Đăng xuất", "lang_select": "🌐 Ngôn ngữ",
        "tabs": ["🛰️ Hệ thống MRV", "💹 Sàn Giao dịch", "🤝 Đầu tư Trồng rừng", "🌐 Mạng xã hội", "🏆 Bảng Vàng", "🌟 Về chúng tôi"],
        "sidebar_partners": "🤝 ĐỐI TÁC CHIẾN LƯỢC", "sidebar_certs": "📜 CHỨNG NHẬN PHÁP LÝ"
    },
    "English": {
        "title": "🌍 MRV PLATFORM & CARBON EXCHANGE", "logout": "🚪 Logout", "lang_select": "🌐 Language",
        "tabs": ["🛰️ MRV System", "💹 Marketplace", "🤝 Forest Investment", "🌐 Social Network", "🏆 Leaderboard", "🌟 About Us"],
        "sidebar_partners": "🤝 STRATEGIC PARTNERS", "sidebar_certs": "📜 CERTIFICATIONS"
    }
}

if "current_lang" not in st.session_state: st.session_state["current_lang"] = "Tiếng Việt"
def change_lang(): pass

def inject_custom_css():
    st.markdown("""
        <style>
        html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif !important; }
        .main-title { font-size: clamp(22px, 2.5vw, 32px) !important; font-weight: 800 !important; color: #E2E8F0; margin-bottom: 0px !important; padding-bottom: 0px !important;}
        
        button[kind="primary"] { background-color: #48bb78 !important; border-color: #48bb78 !important; color: white !important; }
        button[kind="primary"]:hover { background-color: #38a169 !important; border-color: #38a169 !important; box-shadow: 0 0 15px rgba(72, 187, 120, 0.6) !important; }
        
        *:focus { outline: none !important; }
        .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus,
        [data-baseweb="select"] > div:focus-within, [data-baseweb="input"] > div:focus-within,
        [data-testid="stSelectbox"] div:focus-within, [data-testid="stTextInput"] div:focus-within {
            border-color: #48bb78 !important; box-shadow: 0 0 10px rgba(72, 187, 120, 0.6) !important;
        }

        /* TẠO LÓA SÁNG XUNG QUANH (GLOW) */
        div[data-testid="stVerticalBlockBorderWrapper"] { transition: all 0.3s ease-in-out !important; }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover { 
            transform: translateY(-5px) !important; 
            border-color: #48bb78 !important;
            box-shadow: 0 10px 25px rgba(72, 187, 120, 0.3), 0 0 20px rgba(72, 187, 120, 0.5) !important; 
        }

        .sidebar-badge { background-color: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid rgba(255, 255, 255, 0.05); display: flex; align-items: center; transition: all 0.3s ease;}
        .sidebar-badge:hover { 
            transform: scale(1.02); background-color: rgba(30, 41, 59, 0.8); border-color: rgba(72, 187, 120, 0.6);
            box-shadow: 0 0 15px rgba(72, 187, 120, 0.6);
        }
        
        .partner-card { background: linear-gradient(145deg, #1e2530, #2a3441); padding: 20px; border-radius: 12px; border: 1px solid #2d3748; height: 160px; transition: all 0.4s ease;}
        .partner-card:hover { 
            transform: translateY(-10px); border-color: #48bb78; 
            box-shadow: 0 15px 30px rgba(72, 187, 120, 0.3), 0 0 25px rgba(72, 187, 120, 0.6);
        }

        /* ========================================================================= */
        /* HIỆU ỨNG MỚI: LUỒNG SÁNG LƯỚT QUA (SWEEP/SHINE EFFECT) NHƯ BẠN YÊU CẦU */
        /* ========================================================================= */
        
        /* 1. Đặt thuộc tính relative và ẩn các phần tử tràn viền để giấu luồng sáng */
        .glass-card, .partner-card, .sidebar-badge, button[kind="primary"], div[data-testid="stVerticalBlockBorderWrapper"] {
            position: relative;
            overflow: hidden !important;
        }
        
        /* 2. Tạo một dải sáng ảo nằm nghiêng, ẩn ở ngoài cùng bên trái khối */
        .glass-card::after, .partner-card::after, .sidebar-badge::after, button[kind="primary"]::after, div[data-testid="stVerticalBlockBorderWrapper"]::after {
            content: '';
            position: absolute;
            top: 0;
            left: -150%;
            width: 60%;
            height: 100%;
            /* Màu xanh lá nhạt với hiệu ứng mờ viền (Gradient) */
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.4), transparent);
            transform: skewX(-25deg);
            transition: left 0.65s ease-in-out;
            pointer-events: none; /* Tránh cản trở khi bấm nút */
            z-index: 10;
        }
        
        /* 3. Khi rê chuột, dải sáng chạy vụt từ trái sang phải */
        .glass-card:hover::after, .partner-card:hover::after, .sidebar-badge:hover::after, button[kind="primary"]:hover::after, div[data-testid="stVerticalBlockBorderWrapper"]:hover::after {
            left: 150%;
        }

        /* CSS phụ trợ */
        .sb-icon { font-size: 22px; margin-right: 12px; }
        .sb-title { color: #e2e8f0; font-size: 13px; font-weight: 600; line-height: 1.2; }
        .sb-desc { color: #a0aec0; font-size: 11px; margin-top: 3px; }
        .sb-desc.highlight { color: #48bb78; }
        .thank-you-banner { background: linear-gradient(90deg, rgba(26,32,44,1) 0%, rgba(45,55,72,1) 100%); border-left: 5px solid #3182ce; padding: 20px; border-radius: 8px; margin-bottom: 30px; border: 1px solid #4a5568; }
        .text-green { color: #48bb78; }
        .text-blue-bold { color: #3182ce; font-weight: 800; font-size: 1.2rem;}
        .mission-container { padding: 10px 15px; border-left: 4px solid #f6ad55; background-color: rgba(26, 32, 44, 0.4); border-radius: 6px; margin-bottom: 25px; }
        .mission-text { color: #e2e8f0; font-size: 1.05rem; line-height: 1.7; transition: all 0.3s ease; display: inline-block; margin-bottom: 15px;}
        .mission-text:hover { transform: translateY(-4px) scale(1.01); color: #ffffff; text-shadow: 0 0 10px rgba(246, 173, 85, 0.6); }
        .pc-title { color: #a0aec0; font-size: 13px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;}
        .pc-value { color: #ffffff; font-size: 18px; font-weight: bold; margin-top: 0; line-height: 1.3;}
        .pc-status { color: #48bb78; font-size: 13px; margin-top: 15px; display: flex; align-items: center;}
        </style>
    """, unsafe_allow_html=True)
