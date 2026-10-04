import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import st_folium
import os

from auth import hien_thi_cong_dang_nhap
from marketplace import hien_thi_san_giao_dich, hien_thi_cong_dau_tu, hien_thi_gioi_thieu_va_goi_von

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
        button[kind="primary"]:hover { background-color: #38a169 !important; border-color: #38a169 !important; }
        
        /* CSS HỦY DIỆT MÀU ĐỎ CỦA STREAMLIT (FOCUS RING BUG) */
        *:focus { outline: none !important; }
        .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus,
        [data-baseweb="select"] > div:focus-within, [data-baseweb="input"] > div:focus-within,
        [data-testid="stSelectbox"] div:focus-within, [data-testid="stTextInput"] div:focus-within {
            border-color: #48bb78 !important; box-shadow: 0 0 0 1px #48bb78 !important;
        }

        .sidebar-badge { background-color: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid rgba(255, 255, 255, 0.05); display: flex; align-items: center; transition: transform 0.2s ease;}
        .sidebar-badge:hover { transform: scale(1.02); background-color: rgba(30, 41, 59, 0.8); border-color: rgba(72, 187, 120, 0.5); }
        .sb-icon { font-size: 22px; margin-right: 12px; }
        .sb-title { color: #e2e8f0; font-size: 13px; font-weight: 600; line-height: 1.2; }
        .sb-desc { color: #a0aec0; font-size: 11px; margin-top: 3px; }
        .sb-desc.highlight { color: #48bb78; }

        /* KHÔI PHỤC CSS CHO LỜI CẢM ƠN VÀ SỨ MỆNH NỔI BẬT */
        .thank-you-banner { background: linear-gradient(90deg, rgba(26,32,44,1) 0%, rgba(45,55,72,1) 100%); border-left: 5px solid #3182ce; padding: 20px; border-radius: 8px; margin-bottom: 30px; border: 1px solid #4a5568; }
        .text-green { color: #48bb78; }
        .text-blue-bold { color: #3182ce; font-weight: 800; font-size: 1.2rem;}
        .mission-container { padding: 10px 15px; border-left: 4px solid #f6ad55; background-color: rgba(26, 32, 44, 0.4); border-radius: 6px; margin-bottom: 25px; }
        .mission-text { color: #e2e8f0; font-size: 1.05rem; line-height: 1.7; transition: all 0.3s ease; display: inline-block; margin-bottom: 15px;}
        .mission-text:hover { transform: translateY(-4px) scale(1.01); color: #ffffff; text-shadow: 0 4px 10px rgba(246, 173, 85, 0.2); }
        
        /* CSS Đối tác Trang Giới thiệu */
        .partner-card { background: linear-gradient(145deg, #1e2530, #2a3441); padding: 20px; border-radius: 12px; border: 1px solid #2d3748; height: 160px; transition: all 0.4s; position: relative; overflow: hidden; cursor: pointer;}
        .partner-card:hover { transform: translateY(-10px); border-color: #48bb78; box-shadow: 0 15px 30px rgba(72, 187, 120, 0.25); }
        .pc-title { color: #a0aec0; font-size: 13px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;}
        .pc-value { color: #ffffff; font-size: 18px; font-weight: bold; margin-top: 0; line-height: 1.3;}
        .pc-status { color: #48bb78; font-size: 13px; margin-top: 15px; display: flex; align-items: center;}
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "admin": {"password": "123", "role": "Chủ rừng / Kỹ sư MRV"},
        "investor": {"password": "123", "role": "Nhà đầu tư từ xa (Cổ đông)"},
        "buyer": {"password": "123", "role": "Doanh nghiệp mua tín chỉ"}
    }
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "current_user" not in st.session_state: st.session_state["current_user"] = ""
if "current_role" not in st.session_state: st.session_state["current_role"] = ""
if "wallet_balance" not in st.session_state: st.session_state["wallet_balance"] = 150000.0  
if "user_portfolios" not in st.session_state: st.session_state["user_portfolios"] = {}
if "investor_portfolios" not in st.session_state: st.session_state["investor_portfolios"] = {}
if "market_projects" not in st.session_state:
    st.session_state["market_projects"] = [
        {"id": "p1", "name": "Dự án giảm phát thải Bắc Trung Bộ", "owner": "Bộ NN&PTNT", "price": 10.5, "volume": 1030000, "duration": 5, "funding_goal": 50000.0, "funded_amount": 15000.0, "status": "Active"}
    ]

# SIDEBAR BẢO CHỨNG ĐÃ ĐƯỢC PHỤC HỒI ĐẦY ĐỦ
with st.sidebar:
    l = LANG_DICT[st.session_state["current_lang"]]
    st.title(l["lang_select"])
    st.caption("🚀 Carbon Exchange Platform v7.0 Final")
    st.selectbox("Ngôn ngữ:", ["Tiếng Việt", "English"], key="current_lang", on_change=change_lang, label_visibility="collapsed")
    st.divider()
    st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold;'>{l['sidebar_partners']}</p>", unsafe_allow_html=True)
    st.markdown("""<div class="sidebar-badge"><div class="sb-icon">📡</div><div><div class="sb-title">Google Earth Engine</div><div class="sb-desc">Đối tác Không gian AI</div></div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="sidebar-badge"><div class="sb-icon">🏦</div><div><div class="sb-title">Vietcombank</div><div class="sb-desc">Escrow Payment</div></div></div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold;'>{l['sidebar_certs']}</p>", unsafe_allow_html=True)
    st.markdown("""<div class="sidebar-badge"><div class="sb-icon">🥇</div><div><div class="sb-title">VCS (Verra)</div><div class="sb-desc highlight">✔ Tiêu chuẩn Toàn cầu</div></div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="sidebar-badge"><div class="sb-icon">🛡️</div><div><div class="sb-title">ISO/IEC 27001</div><div class="sb-desc highlight">✔ Bảo mật Thông tin Cấp cao</div></div></div>""", unsafe_allow_html=True)

def main_app():
    lang = LANG_DICT[st.session_state["current_lang"]]
    col_t, col_l = st.columns([7, 1])
    with col_t:
        st.markdown(f'<div class="main-title">{lang["title"]}</div>', unsafe_allow_html=True)
        st.caption(f"Welcome, **{st.session_state['current_user']}** ({st.session_state['current_role']})")
    with col_l:
        if st.button(lang["logout"], type="secondary", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()
            
    st.markdown("""<style>.stApp { background-image: none !important; background-color: #0E1117 !important;}</style>""", unsafe_allow_html=True)

    try:
        ee_token = st.secrets["EARTHENGINE_TOKEN"]
        cred_path = os.path.expanduser('~/.config/earthengine/')
        os.makedirs(cred_path, exist_ok=True)
        with open(os.path.join(cred_path, 'credentials'), 'w') as f: f.write(ee_token)
        ee.Initialize()
    except Exception:
        pass # Bypass for demo

    @st.cache_resource(ttl=3600)
    def tao_ban_do_carbon(nam):
        vung = ee.Geometry.Point([106.6297, 10.8231]).buffer(15000) 
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(vung).filterDate(f'{nam}-01-01', f'{nam}-12-31').median()
        ndvi = s2.normalizedDifference(['B8', 'B4'])
        carbon = ndvi.updateMask(ndvi.gt(0.4)).multiply(120).rename('Carbon_Proxy')
        return carbon.clip(vung)

    tab_mrv, tab_market, tab_invest, tab_social, tab_community, tab_about = st.tabs(lang["tabs"])

    with tab_mrv:
        st.success("🛰️ Hệ thống Giám sát Không gian AI (Tải siêu tốc)")
        c1, c2 = st.columns(2)
        with c1: nam_co_so = st.selectbox("Năm cơ sở:", range(2016, 2027), index=4) 
        with c2: nam_so_sanh = st.selectbox("Năm so sánh:", range(2016, 2027), index=8) 
        
        try:
            with st.spinner("Đang truy xuất dữ liệu từ Vệ tinh Copernicus..."):
                map_base = tao_ban_do_carbon(nam_co_so)
                map_comp = tao_ban_do_carbon(nam_so_sanh)
                
            m = geemap.Map(center=[10.8231, 106.6297], zoom=11)
            vis = {'min': 0, 'max': 100, 'palette': ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']}
            m.addLayer(map_base, vis, f'Sinh khối {nam_co_so}')
            m.addLayer(map_comp, vis, f'Sinh khối {nam_so_sanh}')
            st_folium(m, width=1200, height=550)
        except:
            st.warning("Đang chạy ở chế độ giả lập cục bộ do thiếu Token GEE hợp lệ.")

    with tab_market: hien_thi_san_giao_dich()
    with tab_invest: hien_thi_cong_dau_tu()
    with tab_about: hien_thi_gioi_thieu_va_goi_von()

if not st.session_state["logged_in"]:
    hien_thi_cong_dang_nhap(st.session_state["current_lang"])
else:
    main_app()
