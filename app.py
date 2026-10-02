import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import st_folium

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="MRV & Carbon Exchange", layout="wide", page_icon="🌍")
st.title("🌍 NỀN TẢNG MRV & SÀN GIAO DỊCH TÍN CHỈ CARBON")
st.markdown("**Hệ sinh thái Toàn diện:** Đo đạc Vệ tinh (MRV) ↔ Kết nối Doanh nghiệp & Chủ rừng (Marketplace)")

# 2. KHỞI TẠO EARTH ENGINE
try:
    ee_token = st.secrets["EARTHENGINE_TOKEN"]
    import json, os
    cred_path = os.path.expanduser('~/.config/earthengine/')
    os.makedirs(cred_path, exist_ok=True)
    with open(os.path.join(cred_path, 'credentials'), 'w') as f:
        f.write(ee_token)
    ee.Initialize()
except Exception as e:
    st.error(f"Lỗi xác thực Earth Engine: {e}")
    st.stop()

# 3. LÕI HUẤN LUYỆN AI (Giữ nguyên cấu trúc ổn định bán kính 50km)
@st.cache_resource
def get_vung_du_an():
    trung_tam = ee.Geometry.Point([106.6297, 10.8231])
    return trung_tam.buffer(50000) 

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

# --- CHIA GIAO DIỆN THÀNH 2 TAB ĐỘC LẬP ---
tab_mrv, tab_market = st.tabs(["🛰️ HỆ THỐNG MRV (Đo đạc Vệ tinh)", "💹 SÀN GIAO DỊCH B2B (Marketplace)"])

# ==========================================
# TAB 1: KHÔNG GIAN ĐO ĐẠC MRV (Dành cho Chủ rừng/Kỹ sư)
# ==========================================
with tab_mrv:
    st.markdown("### ⏳ Bộ lọc Thời gian")
    c_nam1, c_nam2 = st.columns(2)
    with c_nam1:
        nam_co_so = st.selectbox("📅 Chọn Năm cơ sở (Quá khứ):", range(2016, 2027), index=4) 
    with c_nam2:
        nam_so_sanh = st.selectbox("📅 Chọn Năm so sánh (Hiện tại/Tương lai):", range(2016, 2027), index=8) 

    with st.spinner(f'Đang tải bản đồ AI cho năm {nam_co_so} và {nam_so_sanh}...'):
        carbon_base = tao_ban_do_carbon(nam_co_so)
        carbon_compare = tao_ban_do_carbon(nam_so_sanh)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🗺 Khảo sát Không gian")
        m = geemap.Map(center=[10.8231, 106.6297], zoom=9)
        vis = {'min': 0, 'max': 140, 'palette': ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']}
        m.addLayer(carbon_base, vis, f'Mật độ {nam_co_so}')
        m.addLayer(carbon_compare, vis, f'Mật độ {nam_so_sanh}')
        map_data = st_folium(m, width=800, height=550)

    with col2:
        st.markdown("### 📊 Thẩm định Dự án")
        gia_usd = st.number_input("💸 Kịch bản giá Tín chỉ dự kiến (USD):", min_value=1.0, max_value=100.0, value=12.5, step=0.5)
        
        if map_data and map_data.get("last_active_drawing"):
            st.success("✅ Đã nhận diện vùng khoanh!")
            coords = map_data["last_active_drawing"]["geometry"]["coordinates"]
            vung_khoanh = ee.Geometry.Polygon(coords)
            
            if st.button("🚀 XUẤT BÁO CÁO THẨM ĐỊNH", type="primary", use_container_width=True):
                with st.spinner("Đang quét AI phân tích..."):
                    md_base = list(carbon_base.reduceRegion(reducer=ee.Reducer.mean(), geometry=vung_khoanh, scale=30, maxPixels=1e9).getInfo().values())[0] or 0
                    md_comp = list(carbon_compare.reduceRegion(reducer=ee.Reducer.mean(), geometry=vung_khoanh, scale=30, maxPixels=1e9).getInfo().values())[0] or 0
                    dtich = (list(ee.Image.pixelArea().updateMask(carbon_compare.mask()).clip(vung_khoanh).reduceRegion(reducer=ee.Reducer.sum(), geometry=vung_khoanh, scale=30, maxPixels=1e9).getInfo().values())[0] or 0) / 10000
                    
                    if dtich > 0:
                        tang_truong = (md_comp * dtich) - (md_base * dtich)
                        usd_val = abs(tang_truong) * 1.72 * gia_usd
                        
                        st.markdown("#### 📑 KẾT QUẢ KIỂM KÊ")
                        c1, c2 = st.columns(2)
                        c1.metric("Diện tích (ha)", f"{dtich:,.1f}")
                        c2.metric("Chênh lệch (tấn)", f"{tang_truong:,.0f}")
                        if tang_truong > 0:
                            st.success(f"Dự án đủ điều kiện niêm yết lên Sàn giao dịch với giá trị ước tính **${usd_val:,.0f}**")
                            st.button("Tạo hồ sơ niêm yết lên Sàn", use_container_width=True)
                    else:
                        st.warning("Vùng bạn vẽ không có dữ liệu rừng hợp lệ.")
        else:
            st.info("👈 Khoanh vùng để thẩm định dự án trước khi đưa lên sàn.")
