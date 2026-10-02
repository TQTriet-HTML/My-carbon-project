import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import st_folium

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="MRV Forest Carbon", layout="wide", page_icon="🌍")
st.title("🌍 NỀN TẢNG MRV ĐÁNH GIÁ TÍN CHỈ CARBON")
st.markdown("**Bản Demo Khu vực Miền Nam** - Tích hợp Vệ tinh Sentinel-2, Laser GEDI & AI")

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

# 3. MỞ RỘNG VÙNG DỰ ÁN & HUẤN LUYỆN AI ĐỘNG
@st.cache_resource
def get_vung_du_an():
    # Chuyển tâm bản đồ về TP.HCM và mở rộng bán kính lên 150km (bao quát toàn Miền Nam)
    mien_nam_center = ee.Geometry.Point([106.6297, 10.8231])
    return mien_nam_center.buffer(150000)

vung_du_an = get_vung_du_an()

@st.cache_resource
def tao_ban_do_carbon(nam):
    # Khai báo dữ liệu nền tảng
    worldcover = ee.ImageCollection('ESA/WorldCover/v200').first()
    mask_rung = worldcover.select('Map').eq(10)
    gedi = ee.ImageCollection('LARSE/GEDI/GEDI04_A_002_MONTHLY').filterBounds(vung_du_an).filterDate('2022-01-01', '2023-12-31').select('agbd').mean().rename('Carbon_ThucTe')
    
    # Kéo dữ liệu vệ tinh theo năm được chọn
    s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(vung_du_an).filterDate(f'{nam}-01-01', f'{nam}-12-31').median()
    ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
    
    # Xử lý và huấn luyện AI
    forest_mask = mask_rung.add(ndvi.gt(0.4)).gt(0)
    ndvi_forest = ndvi.updateMask(forest_mask)
    gedi_forest = gedi.updateMask(forest_mask)
    
    du_lieu = ndvi_forest.addBands(gedi_forest)
    tap_huan_luyen = du_lieu.sample(region=vung_du_an, scale=100, numPixels=3000, dropNulls=True) # Tăng Scale để xử lý mượt diện rộng
    ai_model = ee.Classifier.smileRandomForest(50).setOutputMode('REGRESSION').train(features=tap_huan_luyen, classProperty='Carbon_ThucTe', inputProperties=['NDVI'])
    
    return ndvi_forest.classify(ai_model).clip(vung_du_an)

# 4. GIAO DIỆN ĐIỀU KHIỂN & CHỌN NĂM
st.markdown("### ⏳ Bộ lọc Thời gian")
c_nam1, c_nam2 = st.columns(2)
with c_nam1:
    nam_co_so = st.selectbox("📅 Chọn Năm cơ sở (Quá khứ):", range(2016, 2027), index=4) # Mặc định 2020
with c_nam2:
    nam_so_sanh = st.selectbox("📅 Chọn Năm so sánh (Hiện tại/Tương lai):", range(2016, 2027), index=7) # Mặc định 2023

with st.spinner(f'Đang tải và phân tích dữ liệu AI cho năm {nam_co_so} và {nam_so_sanh}...'):
    carbon_base = tao_ban_do_carbon(nam_co_so)
    carbon_compare = tao_ban_do_carbon(nam_so_sanh)

# 5. THIẾT KẾ BẢN ĐỒ & TÍNH TOÁN
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🗺 Khảo sát Không gian")
    # Thu nhỏ mức zoom để nhìn được toàn cảnh Miền Nam
    m = geemap.Map(center=[10.8231, 106.6297], zoom=8)
    vis = {'min': 0, 'max': 140, 'palette': ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']}
    
    m.addLayer(carbon_base, vis, f'Mật độ {nam_co_so}')
    m.addLayer(carbon_compare, vis, f'Mật độ {nam_so_sanh}')
    m.addLayer(ee.FeatureCollection([ee.Feature(vung_du_an)]).style(color='blue', fillColor='00000000'), {}, 'Phạm vi khảo sát Miền Nam')
    
    map_data = st_folium(m, width=800, height=550)

with col2:
    st.markdown("### 📊 Bảng điều khiển Tài chính")
    gia_usd = st.number_input("💸 Kịch bản giá Tín chỉ (USD):", min_value=1.0, max_value=100.0, value=10.0, step=0.5)
    
    if map_data and map_data.get("last_active_drawing"):
        st.success("✅ Đã nhận diện vùng khoanh!")
        coords = map_data["last_active_drawing"]["geometry"]["coordinates"]
        vung_khoanh = ee.Geometry.Polygon(coords)
        
        if st.button("🚀 TÍNH TOÁN DOANH THU", type="primary", use_container_width=True):
            with st.spinner("Đang quét AI phân tích sinh khối..."):
                md_base = list(carbon_base.reduceRegion(reducer=ee.Reducer.mean(), geometry=vung_khoanh, scale=30, maxPixels=1e9).getInfo().values())[0] or 0
                md_comp = list(carbon_compare.reduceRegion(reducer=ee.Reducer.mean(), geometry=vung_khoanh, scale=30, maxPixels=1e9).getInfo().values())[0] or 0
                dtich = (list(ee.Image.pixelArea().updateMask(carbon_compare.mask()).clip(vung_khoanh).reduceRegion(reducer=ee.Reducer.sum(), geometry=vung_khoanh, scale=30, maxPixels=1e9).getInfo().values())[0] or 0) / 10000
                
                if dtich > 0:
                    tang_truong = (md_comp * dtich) - (md_base * dtich)
                    usd_val = abs(tang_truong) * 1.72 * gia_usd
                    
                    st.divider()
                    st.markdown(f"#### 📑 KẾT QUẢ KIỂM KÊ ({nam_co_so} - {nam_so_sanh})")
                    c1, c2 = st.columns(2)
                    c1.metric("Diện tích bảo vệ (ha)", f"{dtich:,.1f}")
                    c2.metric("Chênh lệch Sinh khối (tấn)", f"{tang_truong:,.0f}")
                    
                    c3, c4 = st.columns(2)
                    c3.metric(f"Mật độ {nam_co_so}", f"{md_base:,.1f}")
                    c4.metric(f"Mật độ {nam_so_sanh}", f"{md_comp:,.1f}", delta=f"{md_comp-md_base:,.1f} tấn/ha")
                    
                    st.divider()
                    if tang_truong > 0:
                        st.success(f"### 💰 DOANH THU TĂNG THÊM:\n# + ${usd_val:,.0f} USD")
                    else:
                        st.error(f"### ❌ THIỆT HẠI KINH TẾ (Mất trắng):\n# - ${usd_val:,.0f} USD")
                else:
                    st.warning("Vùng bạn vẽ không có dữ liệu rừng hợp lệ.")
    else:
        st.info("👈 Vui lòng sử dụng công cụ hình Đa giác/Chữ nhật bên góc trái bản đồ để khoanh một vùng cần đánh giá.")
