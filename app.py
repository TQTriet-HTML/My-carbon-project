import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. CẤU HÌNH TRANG WEB (Luôn nằm trên cùng)
st.set_page_config(page_title="MRV & Carbon Exchange", layout="wide", page_icon="🌍")

# 2. KHỞI TẠO BỘ NHỚ TRẠNG THÁI (MÔ PHỎNG DATABASE)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_db" not in st.session_state:
    # Dữ liệu tạm thời để test. Sau này code sẽ kéo từ Google Sheets về đây.
    st.session_state["user_db"] = {"admin": "123456", "doanhnghiepA": "carbon2026"}

# 3. GIAO DIỆN CỔNG ĐĂNG NHẬP (Kết nối Google Sheets)
def hien_thi_cong_dang_nhap():
    st.title("🔐 CỔNG ĐĂNG NHẬP NỀN TẢNG")
    st.markdown("Vui lòng đăng nhập hoặc tạo tài khoản để truy cập Sàn giao dịch & Hệ thống MRV.")
    
    # Kết nối trực tiếp với Google Sheets bằng URL
    url_sheet = "https://docs.google.com/spreadsheets/d/1HlMhjhvE6t0RDgN2zIx4nx1rPDHQJt3bRJfdgmTFGsU/edit"
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Kéo dữ liệu từ Excel về (ttl=0 để luôn cập nhật mới nhất)
    try:
        db = conn.read(spreadsheet=url_sheet, usecols=[0, 1, 2], ttl=0)
    except:
        st.error("Chưa kết nối được với Google Sheets. Vui lòng kiểm tra lại link!")
        return

    tab_login, tab_register = st.tabs(["Đăng nhập", "Tạo tài khoản mới"])
    
    # --- LUỒNG TÌM KIẾM & ĐĂNG NHẬP ---
    with tab_login:
        user = st.text_input("Tên đăng nhập", key="login_user")
        pwd = st.text_input("Mật khẩu", type="password", key="login_pwd")
        if st.button("Đăng nhập", type="primary"):
            # Lọc trong bảng excel xem có user này không
            user_row = db[db['Username'] == user]
            
            if not user_row.empty:
                # Nếu có, kiểm tra cột Password
                mk_dung = str(user_row.iloc[0]['Password'])
                if mk_dung == pwd:
                    st.session_state["logged_in"] = True
                    st.session_state["current_role"] = user_row.iloc[0]['Role']
                    st.rerun() # Tải lại trang vào nền tảng
                else:
                    st.error("❌ Sai mật khẩu!")
            else:
                st.error("❌ Tên đăng nhập không tồn tại!")
                
    # --- LUỒNG LƯU DỮ LIỆU ĐĂNG KÝ ---
    with tab_register:
        new_user = st.text_input("Chọn tên đăng nhập mới", key="reg_user")
        new_pwd = st.text_input("Nhập mật khẩu", type="password", key="reg_pwd")
        role = st.selectbox("Vai trò của bạn", ["Doanh nghiệp mua tín chỉ", "Chủ rừng / Kỹ sư MRV"])
        
        if st.button("Đăng ký tài khoản"):
            if new_user == "" or new_pwd == "":
                st.warning("⚠️ Vui lòng nhập đầy đủ thông tin!")
            elif new_user in db['Username'].values:
                st.warning("⚠️ Tên đăng nhập này đã có người sử dụng!")
            else:
                # Tạo một dòng dữ liệu mới
                new_data = pd.DataFrame([{"Username": new_user, "Password": new_pwd, "Role": role}])
                # Ghép vào dữ liệu cũ
                updated_db = pd.concat([db, new_data], ignore_index=True)
                # Ghi đè lại lên Google Sheets
                conn.update(worksheet="Sheet1", data=updated_db, spreadsheet=url_sheet)
                
                st.success(f"✅ Tạo tài khoản {role} thành công! Hãy quay lại tab Đăng nhập.")

# 4. HỆ THỐNG LÕI (BỊ KHÓA NẾU CHƯA ĐĂNG NHẬP)
def main_app():
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.title("🌍 NỀN TẢNG MRV & SÀN GIAO DỊCH TÍN CHỈ CARBON")
    with col_logout:
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()
            
    # Phần khởi tạo Google Earth Engine
    try:
        ee_token = st.secrets["EARTHENGINE_TOKEN"]
        import os
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

    tab_mrv, tab_market = st.tabs(["🛰️ HỆ THỐNG MRV (Đo đạc)", "💹 SÀN GIAO DỊCH B2B"])

    with tab_mrv:
        c_nam1, c_nam2 = st.columns(2)
        with c_nam1: nam_co_so = st.selectbox("Năm cơ sở:", range(2016, 2027), index=4) 
        with c_nam2: nam_so_sanh = st.selectbox("Năm so sánh:", range(2016, 2027), index=8) 

        with st.spinner(f'Đang tải bản đồ...'):
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

# 5. CÔNG TẮC LUỒNG CHẠY
if not st.session_state["logged_in"]:
    hien_thi_cong_dang_nhap()
else:
    main_app()
