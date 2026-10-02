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

# --- CSS TỔNG HỢP (BAO GỒM HOẠT HỌA PHẦN GIỚI THIỆU) ---
def inject_custom_css():
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif !important;
        }
        
        .main-title {
            font-size: clamp(22px, 2.5vw, 32px) !important;
            font-weight: 800 !important;
            color: #E2E8F0;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
            white-space: nowrap !important;
        }

        .logout-btn-container {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            height: 100%;
            margin-top: 5px;
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"] {
            transition: all 0.3s ease-in-out !important;
            border-radius: 12px !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-6px) !important;
            box-shadow: 0 10px 25px rgba(72, 187, 120, 0.25) !important;
            border-color: #48bb78 !important;
        }
        
        div.stButton > button {
            transition: all 0.3s ease-in-out !important;
            border-radius: 8px !important;
        }
        div.stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 6px 15px rgba(72, 187, 120, 0.3) !important;
            border-color: #48bb78 !important;
        }

        /* --- CSS HOẠT HỌA CHO PHẦN GIỚI THIỆU --- */
        @keyframes floatAndGlow {
            0% { transform: translateY(0px); text-shadow: 0 0 5px rgba(56, 161, 105, 0.2); }
            50% { transform: translateY(-5px); text-shadow: 0 0 15px rgba(56, 161, 105, 0.6); }
            100% { transform: translateY(0px); text-shadow: 0 0 5px rgba(56, 161, 105, 0.2); }
        }
        .thank-you-banner {
            background: linear-gradient(90deg, rgba(26,32,44,1) 0%, rgba(45,55,72,1) 100%);
            border-left: 5px solid #3182ce;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            font-size: 1.1rem;
            line-height: 1.6;
            animation: floatAndGlow 4s ease-in-out infinite;
            border: 1px solid #4a5568;
        }
        .text-green { color: #48bb78; } 
        .text-blue-bold { color: #3182ce; font-weight: 800; font-size: 1.2rem; }

        .partner-card {
            background: linear-gradient(145deg, #1e2530, #2a3441);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #2d3748;
            height: 160px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }
        .partner-card:hover {
            transform: translateY(-10px) scale(1.02);
            border-color: #48bb78;
            box-shadow: 0 15px 30px rgba(72, 187, 120, 0.25);
        }
        .partner-card::after {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 50%; height: 100%;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.15), transparent);
            transform: skewX(-25deg);
            transition: 0.6s;
        }
        .partner-card:hover::after {
            left: 125%;
        }
        
        .pc-title { color: #a0aec0; font-size: 13px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;}
        .pc-value { color: #ffffff; font-size: 18px; font-weight: bold; margin-top: 0; line-height: 1.3;}
        .pc-status { color: #48bb78; font-size: 13px; margin-top: 15px; display: flex; align-items: center;}
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- SIDEBAR: NGÔN NGỮ & LIÊN KẾT NGOÀI ---
with st.sidebar:
    st.title("🌐 Ngôn ngữ / Language")
    ngon_ngu = st.selectbox(
        "Chọn ngôn ngữ hiển thị:", 
        ["Tiếng Việt", "English (Global)", "中文 (Chinese)", "Русский (Russian)", "Français (French)"]
    )
    if ngon_ngu != "Tiếng Việt":
        st.info(f"⏳ Đang triển khai AI dịch thuật tự động cho **{ngon_ngu}**.")
    st.divider()
    st.caption("Carbon Exchange Platform v2.5")

# Khởi tạo trạng thái phiên
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
if "social_posts" not in st.session_state:
    st.session_state["social_posts"] = [
        {
            "id": "post_seed_1",
            "author": "Chuyên gia Lâm nghiệp Lê Văn A",
            "role": "Chủ rừng / Kỹ sư MRV",
            "content": "Tôi vừa thử nghiệm công nghệ vệ tinh mới trên sàn, độ chính xác nhận diện thảm thực vật lên đến 95%. Rất đáng kỳ vọng cho đợt đo đạc tới!",
            "tag": "#KinhNghiemTrongRung",
            "time": "02/10/2026 09:30",
            "likes": 12,
            "comments": [{"user": "Đại diện Vinamilk", "text": "Tuyệt vời, chúng tôi rất mong chờ lô tín chỉ tiếp theo của anh."}]
        }
    ]

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
        }
    ]

def main_app():
    col_title, col_logout = st.columns([6, 1])
    with col_title:
        st.markdown('<div class="main-title">🌍 NỀN TẢNG MRV & SÀN GIAO DỊCH TÍN CHỈ CARBON</div>', unsafe_allow_html=True)
        st.caption(f"Chào mừng trở lại, **{st.session_state['current_user']}** ({st.session_state['current_role']})")
        
    with col_logout:
        st.markdown('<div class="logout-btn-container">', unsafe_allow_html=True)
        if st.button("🚪 Đăng xuất", type="secondary", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
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

    # Các Tab giao diện
    tab_mrv, tab_market, tab_invest, tab_social, tab_community, tab_about = st.tabs([
        "🛰️ Hệ thống MRV", 
        "💹 Sàn Giao dịch", 
        "🤝 Đầu tư Trồng rừng",
        "🌐 Mạng xã hội",
        "🏆 Bảng Vàng",
        "🌟 Về chúng tôi"
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

    with tab_market: hien_thi_san_giao_dich()
    with tab_invest: hien_thi_cong_dau_tu()
    with tab_social: hien_thi_mang_xa_hoi()
    with tab_community: hien_thi_vinh_danh_va_gop_y()
    with tab_about: hien_thi_gioi_thieu_va_goi_von()

if not st.session_state["logged_in"]:
    hien_thi_cong_dang_nhap()
else:
    main_app()
