import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import st_folium
import json
import os

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="MRV & Carbon Exchange", layout="wide", page_icon="🌍")

# 2. HỆ THỐNG QUẢN LÝ TÀI KHOẢN
USER_FILE = "users_db.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        default_db = {"admin": {"password": "123456", "role": "Chủ rừng / Kỹ sư MRV"}}
        save_users(default_db)
        return default_db

def save_users(db):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_role" not in st.session_state:
    st.session_state["current_role"] = ""

# 3. GIAO DIỆN CỔNG ĐĂNG NHẬP
def hien_thi_cong_dang_nhap():
    st.title("🔐 CỔNG ĐĂNG NHẬP NỀN TẢNG")
    st.markdown("Vui lòng đăng nhập hoặc tạo tài khoản để truy cập Sàn giao dịch & Hệ thống MRV.")
    
    user_db = load_users()
    tab_login, tab_register = st.tabs(["Đăng nhập", "Tạo tài khoản mới"])
    
    with tab_login:
        user = st.text_input("Tên đăng nhập", key="login_user")
        pwd = st.text_input("Mật khẩu", type="password", key="login_pwd")
        if st.button("Đăng nhập", type="primary"):
            if user in user_db and user_db[user]["password"] == pwd:
                st.session_state["logged_in"] = True
                st.session_state["current_role"] = user_db[user]["role"]
                st.rerun()
            else:
                st.error("❌ Sai tên đăng nhập hoặc mật khẩu!")
                
    with tab_register:
        new_user = st.text_input("Chọn tên đăng nhập mới", key="reg_user")
        new_pwd = st.text_input("Nhập mật khẩu", type="password", key="reg_pwd")
        role = st.selectbox("Vai trò của bạn", ["Doanh nghiệp mua tín chỉ", "Chủ rừng / Kỹ sư MRV"])
        
        if st.button("Đăng ký tài khoản"):
            if new_user == "" or new_pwd == "":
                st.warning("⚠️ Vui lòng nhập đầy đủ thông tin!")
            elif new_user in user_db:
                st.warning("⚠️ Tên đăng nhập này đã có người sử dụng!")
            else:
                user_db[new_user] = {"password": new_pwd, "role": role}
                save_users(user_db)
                st.success(f"✅ Tạo tài khoản thành công! Hãy chuyển sang tab Đăng nhập.")

# 4. HỆ THỐNG LÕI (TỐI ƯU HIỆU NĂNG LOAD NHANH)
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
        st.error(f"Lỗi xác thực Earth Engine: {e}")
        st.stop()

    @st.cache_resource
    def get_vung_du_an():
        return ee.Geometry.Point([106.6297, 10.8231]).buffer(50000) 

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

    # HIỂN THỊ TAB NGAY LẬP TỨC KHÔNG BỊ CHẶN BỞI GEE
    tab_mrv, tab_market = st.tabs(["🛰️ HỆ THỐNG MRV (Đo đạc)", "💹 SÀN GIAO DỊCH B2B"])

    with tab_mrv:
        c_nam1, c_nam2 = st.columns(2)
        with c_nam1: nam_co_so = st.selectbox("Năm cơ sở:", range(2016, 2027), index=4, key="ns1") 
        with c_nam2: nam_so_sanh = st.selectbox("Năm so sánh:", range(2016, 2027), index=8, key="ns2") 

        # Đưa lệnh gọi GEE vào trong spinner riêng của tab MRV
        with st.spinner(f'Đang kết nối vệ tinh và xử lý mô hình AI cho năm {nam_co_so} và {nam_so_sanh}...'):
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
            st.info(f"👤 Xin chào: **{st.session_state.get('current_role', 'Thành viên')}**")
            gia_usd = st.number_input("Giá Tín chỉ (USD):", value=12.5)
            if map_data and map_data.get("last_active_drawing"):
                st.success("Đã khoanh vùng. Sẵn sàng thẩm định.")
            else:
                st.info("Khoanh vùng để thẩm định dự án.")

    with tab_market:
        st.markdown("## 🏢 Trung tâm Giao dịch Tín chỉ Carbon Doanh nghiệp")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tổng khối lượng sẵn có", "245,000 tấn", "+12,000 tấn")
        m2.metric("Giá tham chiếu (VCS)", "$12.50", "+$0.50")
        m3.metric("Doanh nghiệp tìm mua", "84 Đối tác", "+3")
        m4.metric("Dự án chờ duyệt MRV", "12 Dự án")

# 5. ĐIỀU HƯỚNG MÀN HÌNH
if not st.session_state["logged_in"]:
    hien_thi_cong_dang_nhap()
else:
    main_app()
