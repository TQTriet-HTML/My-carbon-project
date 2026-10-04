import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import st_folium
import os

from auth import hien_thi_cong_dang_nhap
from marketplace import hien_thi_san_giao_dich, hien_thi_cong_dau_tu, hien_thi_gioi_thieu_va_goi_von
from community import hien_thi_vinh_danh_va_gop_y
from social import hien_thi_mang_xa_hoi

st.set_page_config(page_title="MRV & Carbon Exchange", layout="wide", page_icon="🌍")

LANG_DICT = {
    "Tiếng Việt": {
        "title": "🌍 NỀN TẢNG MRV & SÀN GIAO DỊCH TÍN CHỈ CARBON",
        "logout": "🚪 Đăng xuất",
        "lang_select": "🌐 Ngôn ngữ / Language",
        "tabs": ["🛰️ Hệ thống MRV", "💹 Sàn Giao dịch", "🤝 Đầu tư Trồng rừng", "🌐 Mạng xã hội", "🏆 Bảng Vàng", "🌟 Về chúng tôi"],
        "sidebar_partners": "🤝 ĐỐI TÁC CHIẾN LƯỢC",
        "sidebar_certs": "📜 CHỨNG NHẬN PHÁP LÝ"
    },
    "English": {
        "title": "🌍 MRV PLATFORM & CARBON CREDIT EXCHANGE",
        "logout": "🚪 Logout",
        "lang_select": "🌐 Language",
        "tabs": ["🛰️ MRV System", "💹 Marketplace", "🤝 Forest Investment", "🌐 Social Network", "🏆 Leaderboard", "🌟 About Us"],
        "sidebar_partners": "🤝 STRATEGIC PARTNERS",
        "sidebar_certs": "📜 CERTIFICATIONS"
    }
}

if "current_lang" not in st.session_state:
    st.session_state["current_lang"] = "Tiếng Việt"

def change_lang():
    pass

def inject_custom_css():
    st.markdown("""
        <style>
        html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif !important; }
        .main-title { font-size: clamp(22px, 2.5vw, 32px) !important; font-weight: 800 !important; color: #E2E8F0; margin-bottom: 0px !important; padding-bottom: 0px !important; white-space: nowrap !important; }
        .logout-btn-container { display: flex; justify-content: flex-end; align-items: center; height: 100%; margin-top: 5px; }
        div[data-testid="stVerticalBlockBorderWrapper"] { transition: all 0.3s ease-in-out !important; border-radius: 12px !important; }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover { transform: translateY(-6px) !important; box-shadow: 0 10px 25px rgba(72, 187, 120, 0.25) !important; border-color: #48bb78 !important; }
        div.stButton > button { transition: all 0.3s ease-in-out !important; border-radius: 8px !important; }
        div.stButton > button:hover { transform: translateY(-3px) !important; box-shadow: 0 6px 15px rgba(72, 187, 120, 0.3) !important; border-color: #48bb78 !important; }
        button[kind="primary"] { background-color: #48bb78 !important; border-color: #48bb78 !important; color: white !important; }
        button[kind="primary"]:hover { background-color: #38a169 !important; border-color: #38a169 !important; }
        *:focus { outline: none !important; }
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div { transition: all 0.3s ease !important; }
        div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within,
        div[data-baseweb="input"] > div:focus-visible, div[data-baseweb="select"] > div:focus-visible { border-color: #48bb78 !important; box-shadow: 0 0 0 1px #48bb78 !important; }
        .sidebar-badge { background-color: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid rgba(255, 255, 255, 0.05); display: flex; align-items: center; transition: transform 0.2s ease, background-color 0.2s ease; }
        .sidebar-badge:hover { transform: scale(1.02); background-color: rgba(30, 41, 59, 0.8); border-color: rgba(72, 187, 120, 0.5); }
        .sb-icon { font-size: 22px; margin-right: 12px; }
        .sb-title { color: #e2e8f0; font-size: 13px; font-weight: 600; line-height: 1.2; }
        .sb-desc { color: #a0aec0; font-size: 11px; margin-top: 3px; }
        .sb-desc.highlight { color: #48bb78; }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

with st.sidebar:
    lang_dict = LANG_DICT[st.session_state["current_lang"]]
    st.title(lang_dict["lang_select"])
    st.caption("🚀 Carbon Exchange Platform v5.5")
    
    st.selectbox(
        "Chọn ngôn ngữ / Select language:", 
        ["Tiếng Việt", "English"],
        key="current_lang",
        on_change=change_lang,
        label_visibility="collapsed"
    )
    st.divider()
    
    st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold; margin-bottom:10px;'>{lang_dict['sidebar_partners']}</p>", unsafe_allow_html=True)
    st.markdown("""
        <div class="sidebar-badge"><div class="sb-icon">🇻🇳</div><div><div class="sb-title">Bộ Tài nguyên & Môi trường</div><div class="sb-desc">Cơ quan Quản lý & Giám sát</div></div></div>
        <div class="sidebar-badge"><div class="sb-icon">📡</div><div><div class="sb-title">Google Earth Engine</div><div class="sb-desc">Đối tác Dữ liệu Không gian AI</div></div></div>
        <div class="sidebar-badge"><div class="sb-icon">🏦</div><div><div class="sb-title">Vietcombank</div><div class="sb-desc">Ngân hàng Thanh toán Escrow</div></div></div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold; margin-bottom:10px;'>{lang_dict['sidebar_certs']}</p>", unsafe_allow_html=True)
    st.markdown("""
        <div class="sidebar-badge"><div class="sb-icon">🥇</div><div><div class="sb-title">VCS (Verra) & Gold Standard</div><div class="sb-desc highlight">✔ Tiêu chuẩn Carbon Toàn cầu</div></div></div>
        <div class="sidebar-badge"><div class="sb-icon">🛡️</div><div><div class="sb-title">ISO/IEC 27001:2022</div><div class="sb-desc highlight">✔ Bảo mật Thông tin Cấp cao</div></div></div>
    """, unsafe_allow_html=True)

# === KHỞI TẠO TẤT CẢ BIẾN TRẠNG THÁI (BAO GỒM USERS_DB) TẠI ĐÂY ===
if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "admin": {"password": "123", "role": "Chủ rừng / Kỹ sư MRV"},
        "investor": {"password": "123", "role": "Nhà đầu tư từ xa (Cổ đông)"},
        "buyer": {"password": "123", "role": "Doanh nghiệp mua tín chỉ"}
    }
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = ""
if "current_role" not in st.session_state:
    st.session_state["current_role"] = ""
if "wallet_balance" not in st.session_state:
    st.session_state["wallet_balance"] = 150000.0  
if "user_portfolios" not in st.session_state:
    st.session_state["user_portfolios"] = {}
if "investor_portfolios" not in st.session_state:
    st.session_state["investor_portfolios"] = {}
if "market_projects" not in st.session_state:
    st.session_state["market_projects"] = [
        {"id": "p1", "name": "Dự án giảm phát thải Bắc Trung Bộ", "owner": "Bộ NN&PTNT", "price": 5.0, "volume": 10300000, "duration": 5, "funding_goal": 50000.0, "funded_amount": 15000.0, "status": "Active"}
    ]

def main_app():
    lang = LANG_DICT[st.session_state["current_lang"]]
    col_title, col_logout = st.columns([6, 1])
    with col_title:
        st.markdown(f'<div class="main-title">{lang["title"]}</div>', unsafe_allow_html=True)
        st.caption(f"Welcome back, **{st.session_state['current_user']}** ({st.session_state['current_role']})")
    with col_logout:
        st.markdown('<div class="logout-btn-container">', unsafe_allow_html=True)
        if st.button(lang["logout"], type="secondary", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown("""<style>.stApp { background-image: none !important; background-color: #0E1117 !important;}</style>""", unsafe_allow_html=True)

    tab_mrv, tab_market, tab_invest, tab_social, tab_community, tab_about = st.tabs(lang["tabs"])

    with tab_mrv: st.info("Hệ thống MRV đang khởi chạy...")
    with tab_market: hien_thi_san_giao_dich()
    with tab_invest: hien_thi_cong_dau_tu()
    with tab_social: hien_thi_mang_xa_hoi()
    with tab_community: hien_thi_vinh_danh_va_gop_y()
    with tab_about: hien_thi_gioi_thieu_va_goi_von()

if not st.session_state["logged_in"]:
    hien_thi_cong_dang_nhap(st.session_state["current_lang"])
else:
    main_app()
