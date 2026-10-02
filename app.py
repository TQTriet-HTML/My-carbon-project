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

# --- ĐẠI TU GIAO DIỆN (UI OVERHAUL) BẰNG CSS ---
def inject_custom_css():
    st.markdown("""
        <style>
        /* Ép font chữ sang các họ sans-serif hiện đại, chuyên nghiệp */
        html, body, [class*="css"]  {
            font-family: 'Inter', 'Roboto', 'Segoe UI', sans-serif !important;
        }
        
        /* Tinh chỉnh tiêu đề chính để không bị rớt dòng (giảm size một chút) */
        .main-title {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
            color: #E2E8F0;
        }

        /* Định dạng lại nút Đăng xuất cho gọn gàng và đẹp mắt */
        .logout-btn-container {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            height: 100%;
            margin-top: 15px;
        }
        
        /* Hiệu ứng nổi lên cho các khối container (Card) */
        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            border-radius: 10px;
            background-color: #1A202C; /* Màu nền tối sang trọng */
        }
        div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.3);
            border-color: #38A169 !important; /* Viền xanh lá khi hover */
        }
        
        /* Chỉnh nút bấm primary (màu chính) */
        button[data-testid="baseButton-primary"] {
            border-radius: 6px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease;
        }
        button[data-testid="baseButton-primary"]:hover {
            transform: translateY(-1px);
            filter: brightness(1.1);
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
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
    
    st.markdown("### Kết nối với chúng tôi")
    st.markdown("[📘 Facebook Fanpage](https://facebook.com)")
    st.markdown("[💬 Nhóm Zalo Cộng đồng](https://zalo.me)")
    st.markdown("[💼 LinkedIn B2B](https://linkedin.com)")
    
    st.divider()
    st.caption("Carbon Exchange Platform v2.0")

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
    # Sử dụng cột để cấu trúc lại phần Tiêu đề và Nút Đăng xuất cho thẳng hàng, gọn gàng
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        # Sử dụng thẻ div với class main-title đã định dạng bằng CSS thay vì thẻ markdown mặc định
        st.markdown('<div class="main-title">🌍 NỀN TẢNG MRV & SÀN GIAO DỊCH TÍN CHỈ CARBON</div>', unsafe_allow_html=True)
        st.caption(f"Chào mừng trở lại, **{st.session_state['current_user']}** ({st.session_state['current_role']})")
        
    with col_logout:
        # Đặt nút đăng xuất vào một container để căn chỉnh tốt hơn
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
