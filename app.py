import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import st_folium

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="MRV Forest Carbon", layout="wide", page_icon="🌍")
st.title("🌍 NỀN TẢNG MRV ĐÁNH GIÁ TÍN CHỈ CARBON")
st.markdown("**Bản Demo VQG Cát Tiên** - Tích hợp Vệ tinh Sentinel-2, Laser GEDI & AI")

# 2. KHỞI TẠO EARTH ENGINE (Tự động nhận diện Token bảo mật từ Secrets)
try:
    # Lấy token từ Streamlit Secrets cấu hình bảo mật
    ee_token = st.secrets["EARTHENGINE_TOKEN"]
    # Tái tạo file credentials từ chuỗi token bảo mật
    import json, os
    cred_path = os.path.expanduser('~/.config/earthengine/')
    os.makedirs(cred_path, exist_ok=True)
    with open(os.path.join(cred_path, 'credentials'), 'w') as f:
        f.write(ee_token)
    ee.Initialize()
except Exception as e:
    st.error(f"Lỗi xác thực Earth Engine: {e}. Vui lòng kiểm tra lại phần Secrets trên Streamlit Cloud!")
    st.stop()

# 3. NẠP DỮ LIỆU & HUẤN LUYỆN AI (Được lưu bộ nhớ đệm để web chạy siêu tốc)
@st.cache_resource
def load_ee_models():
    cat_tien_center = ee.Geometry.Point([107.4286, 11.4280])
    vung_du_an = cat_tien_center.buffer(20000)
    
    worldcover = ee.ImageCollection('ESA/WorldCover/v200').first()
    mask_rung = worldcover.select('Map').eq(10)
    gedi = ee.ImageCollection('LARSE/GEDI/GEDI04_A_002_MONTHLY').filterBounds(vung_du_an).filterDate('2022-01-01', '2023-12-31').select('agbd').mean().rename('Carbon_ThucTe')
    
    def tao_ban_do(nam):
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(vung_du_an).filterDate(f'{nam}-01-01', f'{nam}-12-31').median()
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        forest_mask = mask_rung.add(ndvi.gt(0.4)).gt(0)
        ndvi_forest = ndvi.updateMask(forest_mask)
        gedi_forest = gedi.updateMask(forest_mask)
        
        du_lieu = ndvi_forest.addBands(gedi_forest)
        tap_huan_luyen = du_lieu.sample(region=vung_du_an, scale=50, numPixels=2000, dropNulls=True)
        ai_model = ee.Classifier.smileRandomForest(50).setOutputMode('REGRESSION').train(features=tap_huan_luyen, classProperty='Carbon_ThucTe', inputProperties=['NDVI'])
        return ndvi_forest.classify(ai_model).clip(vung_du_an)
    
    return tao_ban_do(2020), tao_ban_do(2023), vung_du_an

with st.spinner('Đang tải dữ liệu vệ tinh từ máy chủ Google...'):
    carbon_2020, carbon_2023, vung_du_an = load_ee_models()

# 4. THIẾT KẾ GIAO DIỆN CHIA CỘT (BẢN ĐỒ & BẢNG ĐIỀU KHIỂN)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🗺️️ Khảo sát Không gian (Khoanh vùng để đo đạc)")
    m = geemap.Map(center=[11.4280, 107.4286], zoom=11)
    vis = {'min': 0, 'max': 140, 'palette': ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']}
    
    m.addLayer(carbon_2020, vis, 'Mật độ 2020')
    m.addLayer(carbon_2023, vis, 'Mật độ 2023')
    m.addLayer(ee.FeatureCollection([ee.Feature(vung_du_an)]).style(color='red', fillColor='00000000'), {}, 'Bán kính 20km')
    
    # Hiển thị bản đồ và Bắt tương tác vẽ hình từ người dùng
    map_data = st_folium(m, width=800, height=550)

with col2:
    st.markdown("### 📊 Bảng điều khiển Tài chính")
    gia_usd = st.number_input("💸 Kịch bản giá Tín chỉ (USD):", min_value=1.0, max_value=100.0, value=10.0, step=0.5)
    
    # Kiểm tra xem người dùng đã vẽ hình chưa
    if map_data and map_data.get("last_active_drawing"):
        st.success("✅ Đã nhận diện vùng khoanh!")
        coords = map_data["last_active_drawing"]["geometry"]["coordinates"]
        vung_khoanh = ee.Geometry.Polygon(coords)
        
        if st.button("🚀 TÍNH TOÁN DOANH THU", type="primary", use_container_width=True):
            with st.spinner("Đang quét AI phân tích sinh khối..."):
                md_2020 = list(carbon_2020.reduceRegion(reducer=ee.Reducer.mean(), geometry=vung_khoanh, scale=30, maxPixels=1e9).getInfo().values())[0] or 0
                md_2023 = list(carbon_2023.reduceRegion(reducer=ee.Reducer.mean(), geometry=vung_khoanh, scale=30, maxPixels=1e9).getInfo().values())[0] or 0
                dtich = (list(ee.Image.pixelArea().updateMask(carbon_2023.mask()).clip(vung_khoanh).reduceRegion(reducer=ee.Reducer.sum(), geometry=vung_khoanh, scale=30, maxPixels=1e9).getInfo().values())[0] or 0) / 10000
                
                if dtich > 0:
                    tang_truong = (md_2023 * dtich) - (md_2020 * dtich)
                    usd_val = abs(tang_truong) * 1.72 * gia_usd
                    
                    st.divider()
                    st.markdown("#### 📑 KẾT QUẢ KIỂM KÊ")
                    c1, c2 = st.columns(2)
                    c1.metric("Diện tích bảo vệ (ha)", f"{dtich:,.1f}")
                    c2.metric("Chênh lệch Sinh khối (tấn)", f"{tang_truong:,.0f}")
                    
                    c3, c4 = st.columns(2)
                    c3.metric("Mật độ 2020 (tấn/ha)", f"{md_2020:,.1f}")
                    c4.metric("Mật độ 2023 (tấn/ha)", f"{md_2023:,.1f}", delta=f"{md_2023-md_2020:,.1f} tấn/ha")
                    
                    st.divider()
                    if tang_truong > 0:
                        st.success(f"### 💰 DOANH THU TĂNG THÊM:\n# + ${usd_val:,.0f} USD")
                    else:
                        st.error(f"### ❌ THIỆT HẠI KINH TẾ (Mất trắng):\n# - ${usd_val:,.0f} USD")
                else:
                    st.warning("Vùng bạn vẽ không có dữ liệu rừng hợp lệ.")
    else:
        st.info("👈 Vui lòng sử dụng công cụ hình Đa giác/Chữ nhật bên góc trái bản đồ để khoanh một vùng cần đánh giá.")
