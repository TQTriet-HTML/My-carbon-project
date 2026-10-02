import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import st_folium
import os
import pandas as pd

from auth import hien_thi_cong_dang_nhap
from marketplace import hien_thi_san_giao_dich, hien_thi_cong_dau_tu, hien_thi_gioi_thieu_va_goi_von

st.set_page_config(page_title="MRV & Carbon Exchange", layout="wide", page_icon="🌍")

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
if "project_reports" not in st.session_state:
    st.session_state["project_reports"] = {}

if "market_projects" not in st.session_state:
    st.session_state["market_projects"] = [
        {
            "id": "p1",
            "name": "Dự án giảm phát thải vùng Bắc Trung Bộ (ERPA)",
            "owner": "Bộ NN&PTNT",
            "price": 5.0,
            "volume": 10300000,
            "duration": 5, 
            "funding_goal": 50000.0,
            "funded_amount": 15000.0,
            "lat": 16.4637,
            "lon": 107.5908,
            "verified": True,
            "proof_file": None,
            "proof_name": "Quyết định phê duyệt FCPF.pdf",
            "status": "Active"
        },
        {
            "id": "p2",
            "name": "Dự án Rừng ngập mặn nuôi tôm Cà Mau",
            "owner": "BQL rừng phòng hộ Cà Mau",
            "price": 15.0,
            "volume": 250000,
            "duration": 3, 
            "funding_goal": 30000.0,
            "funded_amount": 30000.0,
            "lat": 8.8242,
            "lon": 104.9452,
            "verified": True,
            "proof_file": None,
            "proof_name": "Giấy chứng nhận QSDĐ.pdf",
            "status": "Active"
        }
    ]

def main_app():
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.title("🌍 NỀN TẢNG MRV & SÀN GIAO DỊCH TÍN CHỈ CARBON")
    with col_logout:
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()
            
    try:
        ee_token = st.secrets["EARTHENGINE_TOKEN"]
        cred_path = os.path.expanduser('~/.config/earthengine/')
        os.makedirs(cred_path, exist_ok=True)
        with open(os.path.join(cred_path, 'credentials'), 'w') as f:
            f.write(ee_token)
        ee.Initialize()
    except Exception as e:
        st.error("Lỗi xác thực Earth Engine Token.")
        st.stop()

    @st.cache_resource
    def get_vung_du_an(): return ee.Geometry.Point([106.6297, 10.8231]).buffer(50000) 
    vung_du_an = get_vung_du_an()

    @st.cache_resource
    def tao_ban_do_carbon(nam):
        worldcover = ee.ImageCollection('ESA/WorldCover/v200').first()
        mask_rung = worldcover.select('Map').eq(10)
        gedi = ee.ImageCollection('LARSE/GEDI/GEDI04_A_002_MONTHLY').filterBounds(vung_du_an).filterDate('2022-01-01', '2023-12-31').select('agbd').mean().rename('Carbon_ThucTe')
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(vung_du_an).filterDate(f'{nam}-01-01', f'{nam}-12-31').median()
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        forest_mask = mask_rung.add(ndvi.gt(0.4)).gt(0)
        ndvi_forest = ndvi.updateMask(forest_mask)
        gedi_forest = gedi.updateMask(forest_mask)
        du_lieu = ndvi_forest.addBands(gedi_forest)
        tap_huan_luyen = du_lieu.sample(region=vung_du_an, scale=100, numPixels=1500, dropNulls=True) 
        ai_model = ee.Classifier.smileRandomForest(50).setOutputMode('REGRESSION').train(features=tap_huan_luyen, classProperty='Carbon_ThucTe', inputProperties=['NDVI'])
        return ndvi_forest.classify(ai_model).clip(vung_du_an)

    # Thêm Tab thứ 4: Giới thiệu & Gọi vốn phát triển nền tảng
    tab_mrv, tab_market, tab_invest, tab_about = st.tabs([
        "🛰️ Hệ thống MRV (Đo đạc)", 
        "💹 Sàn Giao dịch Tín chỉ", 
        "🤝 Quỹ Đầu tư Trồng rừng",
        "🌟 Về chúng tôi & Gọi vốn"
    ])

    with tab_mrv:
        st.info("Công cụ đo đạc vệ tinh sinh khối rừng")
        c_nam1, c_nam2 = st.columns(2)
        with c_nam1: nam_co_so = st.selectbox("Năm cơ sở:", range(2016, 2027), index=4) 
        with c_nam2: nam_so_sanh = st.selectbox("Năm so sánh:", range(2016, 2027), index=8) 
        with st.spinner("Đang tải dữ liệu vệ tinh..."):
            carbon_base = tao_ban_do_carbon(nam_co_so)
            carbon_compare = tao_ban_do_carbon(nam_so_sanh)
        c1, c2 = st.columns([2, 1])
        with c1:
            m = geemap.Map(center=[10.8231, 106.6297], zoom=9)
            vis = {'min': 0, 'max': 140, 'palette': ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']}
            m.addLayer(carbon_base, vis, f'Mật độ {nam_co_so}')
            m.addLayer(carbon_compare, vis, f'Mật độ {nam_so_sanh}')
            map_data = st_folium(m, width=800, height=550)
        with c2:
            st.write("Thẩm định sinh khối")

    with tab_market:
        hien_thi_san_giao_dich()

    with tab_invest:
        hien_thi_cong_dau_tu()

    with tab_about:
        hien_thi_gioi_thieu_va_goi_von()

if not st.session_state["logged_in"]:
    hien_thi_cong_dang_nhap()
else:
    main_app()
