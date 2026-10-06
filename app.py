import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import folium_static 
import os
import random

import db_manager
from auth import hien_thi_cong_dang_nhap
from marketplace import hien_thi_san_giao_dich, hien_thi_cong_dau_tu, hien_thi_gioi_thieu_va_goi_von

try:
    from social import hien_thi_mang_xa_hoi
    from community import hien_thi_vinh_danh_va_gop_y
    from diary import hien_thi_nhat_ky_xanh
except ImportError:
    def hien_thi_mang_xa_hoi(): st.info("Hệ thống đang được bảo trì.")
    def hien_thi_vinh_danh_va_gop_y(): st.info("Hệ thống đang được bảo trì.")
    def hien_thi_nhat_ky_xanh(): st.info("Hệ thống đang được bảo trì.")

st.set_page_config(page_title="MRV & Carbon Exchange", layout="wide")

# Khởi tạo CSDL SQLite & nạp dữ liệu vào session_state
db_manager.init_db()

if "users_db" not in st.session_state:
    st.session_state["users_db"] = db_manager.load_users()

if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "current_user" not in st.session_state: st.session_state["current_user"] = ""
if "current_role" not in st.session_state: st.session_state["current_role"] = ""
if "wallet_balance" not in st.session_state: st.session_state["wallet_balance"] = 150000.0  
if "user_portfolios" not in st.session_state: st.session_state["user_portfolios"] = {}
if "investor_portfolios" not in st.session_state: st.session_state["investor_portfolios"] = {}

if "market_projects" not in st.session_state:
    st.session_state["market_projects"] = db_manager.load_market_projects()

if "social_posts" not in st.session_state:
    st.session_state["social_posts"] = db_manager.load_social_posts()

if "green_diary" not in st.session_state:
    st.session_state["green_diary"] = db_manager.load_green_diary()

if "mrv_calc_state" not in st.session_state: st.session_state["mrv_calc_state"] = False
if "mrv_polygon_seed" not in st.session_state: st.session_state["mrv_polygon_seed"] = random.randint(10000, 99999)

LANG_DICT = {
    "Tiếng Việt": {
        "title": "NỀN TẢNG MRV & SÀN GIAO DỊCH", "logout": "ĐĂNG XUẤT", "lang_select": "TÙY CHỌN NGÔN NGỮ",
        "tabs": ["Hệ thống MRV", "Sàn Giao dịch", "Đầu tư Trồng rừng", "Mạng xã hội", "Nhật ký Xanh", "Bảng Vàng", "Về chúng tôi"],
        "sidebar_partners": "ĐỐI TÁC CHIẾN LƯỢC", "sidebar_certs": "CHỨNG NHẬN PHÁP LÝ",
        "sb_p1_title": "Google Earth Engine", "sb_p1_desc": "Đối tác Không gian AI",
        "sb_p2_title": "Vietcombank", "sb_p2_desc": "Thanh toán Escrow",
        "sb_c1_title": "VCS (Verra)", "sb_c1_desc": "Tiêu chuẩn Toàn cầu",
        "sb_c2_title": "ISO/IEC 27001", "sb_c2_desc": "Bảo mật Thông tin Cấp cao",
        "welcome": "Xin chào",
        "mrv_success": "HỆ THỐNG GIÁM SÁT KHÔNG GIAN AI",
        "mrv_base_yr": "Năm cơ sở:", "mrv_comp_yr": "Năm so sánh:",
        "mrv_loading": "AI đang phân tích dữ liệu không gian...",
        "mrv_biomass": "Sinh khối",
        "mrv_calc_btn": "PHÂN TÍCH VÙNG KHOANH",
        "mrv_reset_btn": "LÀM MỚI DỮ LIỆU",
        "mrv_result_title": "KẾT QUẢ PHÂN TÍCH ĐỊNH LƯỢNG",
        "mrv_base_val": "Sinh khối Năm",
        "mrv_comp_val": "Sinh khối Năm",
        "mrv_total_val": "Tổng Giá Trị Quy Đổi",
        "mrv_unit": "Tấn",
        "mrv_success_msg": "Khu vực phân tích ghi nhận sự tăng trưởng sinh khối. Bạn có thể niêm yết thêm {diff} tín chỉ carbon.",
        "mrv_warning_msg": "Mật độ sinh khối trong khu vực sụt giảm. Cần rà soát biến động rừng."
    },
    "English": {
        "title": "MRV PLATFORM & CARBON EXCHANGE", "logout": "LOGOUT", "lang_select": "LANGUAGE SETTINGS",
        "tabs": ["MRV System", "Marketplace", "Forest Investment", "Social Network", "Green Diary", "Leaderboard", "About Us"],
        "sidebar_partners": "STRATEGIC PARTNERS", "sidebar_certs": "CERTIFICATIONS",
        "sb_p1_title": "Google Earth Engine", "sb_p1_desc": "AI Spatial Partner",
        "sb_p2_title": "Vietcombank", "sb_p2_desc": "Escrow Payment",
        "sb_c1_title": "VCS (Verra)", "sb_c1_desc": "Global Standard",
        "sb_c2_title": "ISO/IEC 27001", "sb_c2_desc": "Information Security",
        "welcome": "Welcome",
        "mrv_success": "AI SPATIAL MONITORING SYSTEM",
        "mrv_base_yr": "Base Year:", "mrv_comp_yr": "Comparison Year:",
        "mrv_loading": "AI is analyzing spatial data...",
        "mrv_biomass": "Biomass",
        "mrv_calc_btn": "ANALYZE AREA",
        "mrv_reset_btn": "RESET DATA",
        "mrv_result_title": "QUANTITATIVE ANALYSIS RESULT",
        "mrv_base_val": "Biomass Year",
        "mrv_comp_val": "Biomass Year",
        "mrv_total_val": "Total Converted Value",
        "mrv_unit": "Tons",
        "mrv_success_msg": "Biomass growth detected. You can list {diff} additional carbon credits.",
        "mrv_warning_msg": "Biomass density decreased. Forest inspection required."
    }
}

if "current_lang" not in st.session_state: st.session_state["current_lang"] = "Tiếng Việt"

def hop_thoai_dang_xuat():
    st.session_state["logged_in"] = False
    st.session_state["current_user"] = ""
    st.session_state["current_role"] = ""
    st.rerun()

def main_app():
    l = LANG_DICT[st.session_state["current_lang"]]
    
    with st.sidebar:
        st.markdown(f"<h3 style='color: white; font-weight: 800; text-align: center; font-size: 1.1rem; letter-spacing: 1px;'>{l['lang_select']}</h3>", unsafe_allow_html=True)
        st.selectbox("Ngôn ngữ:", ["Tiếng Việt", "English"], key="current_lang", label_visibility="collapsed")
        st.divider()
        
        st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold; letter-spacing:1px;'>{l['sidebar_partners']}</p>", unsafe_allow_html=True)
        st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">{l['sb_p1_title']}</div><div class="sb-desc">{l['sb_p1_desc']}</div></div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">{l['sb_p2_title']}</div><div class="sb-desc">{l['sb_p2_desc']}</div></div></div>""", unsafe_allow_html=True)
        
        st.divider()
        st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold; letter-spacing:1px;'>{l['sidebar_certs']}</p>", unsafe_allow_html=True)
        st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">{l['sb_c1_title']}</div><div class="sb-desc highlight">{l['sb_c1_desc']}</div></div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">{l['sb_c2_title']}</div><div class="sb-desc highlight">{l['sb_c2_desc']}</div></div></div>""", unsafe_allow_html=True)
        
        st.divider()
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin-bottom: 15px;">
            <p style="color:#a0aec0; font-size:11px; margin:0;">{l['welcome']}</p>
            <p style="color:#48bb78; font-weight:bold; font-size:14px; margin:0;">{st.session_state['current_user']} ({st.session_state['current_role']})</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(l["logout"], type="secondary", use_container_width=True):
            hop_thoai_dang_xuat()

    st.markdown("""<style>.stApp { background-image: none !important; background-color: #0E1117 !important;}</style>""", unsafe_allow_html=True)

    try:
        ee_token = st.secrets["EARTHENGINE_TOKEN"]
        cred_path = os.path.expanduser('~/.config/earthengine/')
        os.makedirs(cred_path, exist_ok=True)
        with open(os.path.join(cred_path, 'credentials'), 'w') as f: f.write(ee_token)
        ee.Initialize()
    except Exception:
        pass 

    @st.cache_resource(ttl=3600)
    def tao_ban_do_carbon(nam):
        vung = ee.Geometry.Point([107.4286, 11.4280]).buffer(15000) 
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(vung).filterDate(f'{nam}-01-01', f'{nam}-12-31').median()
        ndvi = s2.normalizedDifference(['B8', 'B4'])
        carbon = ndvi.updateMask(ndvi.gt(0.2)).multiply(120).rename('Carbon_Proxy')
        return carbon.clip(vung)

    tab_mrv, tab_market, tab_invest, tab_social, tab_diary, tab_community, tab_about = st.tabs(l["tabs"])

    with tab_mrv:
        _, col_center, _ = st.columns([0.05, 0.9, 0.05])
        with col_center:
            st.markdown(f"<div style='text-align:center; color:#48bb78; font-weight:800; margin-bottom:15px; font-size:1.1rem; letter-spacing:1px;'>{l['mrv_success']}</div>", unsafe_allow_html=True)
            
            with st.container(border=True):
                c1, c2 = st.columns(2)
                with c1: nam_co_so = st.selectbox(l["mrv_base_yr"], range(2016, 2027), index=4) 
                with c2: nam_so_sanh = st.selectbox(l["mrv_comp_yr"], range(2016, 2027), index=8) 

            try:
                with st.spinner(l["mrv_loading"]):
                    map_base = tao_ban_do_carbon(nam_co_so)
                    map_comp = tao_ban_do_carbon(nam_so_sanh)
                    
                m = geemap.Map(center=[11.4280, 107.4286], zoom=11)
                vis = {'min': 0, 'max': 100, 'palette': ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']}
                m.addLayer(map_base, vis, f"{l['mrv_biomass']} {nam_co_so}")
                m.addLayer(map_comp, vis, f"{l['mrv_biomass']} {nam_so_sanh}")
                
                with st.container(border=True):
                    folium_static(m, width=1100, height=500)
            except Exception:
                st.warning("Đang chạy ở chế độ giả lập cục bộ do thiếu Token GEE hợp lệ.")

    with tab_market: hien_thi_san_giao_dich()
    with tab_invest: hien_thi_cong_dau_tu()
    with tab_social: hien_thi_mang_xa_hoi()
    with tab_diary: hien_thi_nhat_ky_xanh()
    with tab_community: hien_thi_vinh_danh_va_gop_y()
    with tab_about: hien_thi_gioi_thieu_va_goi_von()

if not st.session_state["logged_in"]:
    hien_thi_cong_dang_nhap(st.session_state["current_lang"])
else:
    main_app()
