import streamlit as st
import ee
import geemap.foliumap as geemap
import folium
from streamlit_folium import st_folium
import json
import os
import pandas as pd

# ==========================================
# 1. CẤU HÌNH TRANG WEB & DATABASE ẢO
# ==========================================
st.set_page_config(page_title="MRV & Carbon Exchange", layout="wide", page_icon="🌍")

USER_FILE = "users_db.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        default_db = {"admin": {"password": "1234", "role": "Chủ rừng / Kỹ sư MRV"}}
        save_users(default_db)
        return default_db

def save_users(db):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

# Khởi tạo các trạng thái phiên (Session State) cho giả lập Giao dịch
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_role" not in st.session_state:
    st.session_state["current_role"] = ""
if "wallet_balance" not in st.session_state:
    st.session_state["wallet_balance"] = 150000.0  # Ví ảo ban đầu
if "market_projects" not in st.session_state:
    # Danh sách dự án ban đầu trên sàn
    st.session_state["market_projects"] = [
        {
            "id": "p1",
            "name": "Dự án giảm phát thải vùng Bắc Trung Bộ (ERPA)",
            "owner": "Bộ NN&PTNT",
            "price": 5.0,
            "volume": 10300000,
            "lat": 16.4637,
            "lon": 107.5908
        },
        {
            "id": "p2",
            "name": "Dự án Rừng ngập mặn nuôi tôm Cà Mau",
            "owner": "BQL rừng phòng hộ Cà Mau",
            "price": 15.0,
            "volume": 250000,
            "lat": 8.8242,
            "lon": 104.9452
        }
    ]

# ==========================================
# 2. GIAO DIỆN CỔNG ĐĂNG NHẬP
# ==========================================
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
                st.success("✅ Tạo tài khoản thành công! Hãy chuyển sang tab Đăng nhập.")

# ==========================================
# 3. HỆ THỐNG LÕI (MRV & GIAO DỊCH ẢO)
# ==========================================
def main_app():
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.title("🌍 NỀN TẢNG MRV & SÀN GIAO DỊCH TÍN CHỈ CARBON")
    with col_logout:
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()
            
    # Kết nối Earth Engine an toàn
    try:
        ee_token = st.secrets["EARTHENGINE_TOKEN"]
        cred_path = os.path.expanduser('~/.config/earthengine/')
        os.makedirs(cred_path, exist_ok=True)
        with open(os.path.join(cred_path, 'credentials'), 'w') as f:
            f.write(ee_token)
        ee.Initialize()
    except Exception as e:
        st.error("Vui lòng thiết lập cấu hình Earth Engine Token.")
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

    tab_mrv, tab_market = st.tabs(["🛰️ HỆ THỐNG MRV (Đo đạc)", "💹 SÀN GIAO DỊCH B2B"])

    # --- TAB 1: BẢN ĐỒ MRV ---
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

    # --- TAB 2: SÀN GIAO DỊCH B2B & B2C ---
    with tab_market:
        st.markdown("## 🏢 Trung tâm Giao dịch & Quản lý Tín chỉ")
        vai_tro = st.session_state.get('current_role', '')
        
        # 3.1. KHU VỰC VÍ & NIÊM YẾT
        if vai_tro == "Doanh nghiệp mua tín chỉ":
            st.success(f"💳 **Ví Khách hàng:** Khả dụng **${st.session_state['wallet_balance']:,.2f}** | Trạng thái: Đã xác thực KYC")
            if st.button("💵 Nạp thêm $50,000 vào ví"):
                st.session_state["wallet_balance"] += 50000.0
                st.rerun()
                
        elif vai_tro == "Chủ rừng / Kỹ sư MRV":
            st.info("🌳 **Khu vực Chủ rừng:** Nộp hồ sơ minh chứng để AI thẩm định và niêm yết lên sàn.")
            with st.expander("📝 TẠO HỒ SƠ NIÊM YẾT DỰ ÁN MỚI (Bắt buộc có minh chứng)", expanded=False):
                ten_du_an = st.text_input("Tên dự án rừng của bạn:")
                kl_ban = st.number_input("Khối lượng tín chỉ muốn bán (tấn):", min_value=1, step=100)
                gia_ban = st.number_input("Giá bán mỗi tín chỉ (USD):", value=10.0)
                
                # Bắt buộc tải file
                file_minh_chung = st.file_uploader("📎 Tải lên Sổ đỏ / Giấy tờ pháp lý (Bắt buộc - PDF/JPG)", type=['pdf', 'jpg', 'png'])
                
                if st.button("🚀 XÁC THỰC AI & ĐƯA LÊN SÀN", type="primary"):
                    if not ten_du_an:
                        st.error("❌ Vui lòng nhập tên dự án.")
                    elif file_minh_chung is None:
                        st.error("❌ HỒ SƠ BỊ TỪ CHỐI: Bạn chưa tải lên minh chứng pháp lý (Sổ đỏ). Trí tuệ nhân tạo không thể xác thực khu vực trống.")
                    else:
                        new_proj = {
                            "id": f"user_p_{len(st.session_state['market_projects'])}",
                            "name": ten_du_an,
                            "owner": "Chủ rừng (Đã xác thực minh chứng)",
                            "price": gia_ban,
                            "volume": kl_ban,
                            "lat": 11.4280, 
                            "lon": 107.4286,
                            "verified": True # Cờ xác nhận đã có minh chứng
                        }
                        st.session_state["market_projects"].append(new_proj)
                        st.success("✅ Hợp lệ! Dự án đã được đối chiếu Sổ đỏ với Vệ tinh và đưa lên sàn công khai.")

        st.divider()
        
        # 3.2. BẢNG HIỂN THỊ CÁC DỰ ÁN TRÊN SÀN (MUA LẺ & SỈ)
        st.markdown("### 🛒 Danh mục Tín chỉ đang giao dịch")
        
        for p in st.session_state["market_projects"]:
            # Chỉ hiển thị dự án còn hàng
            if p['volume'] > 0:
                with st.container(border=True):
                    col_info, col_action = st.columns([3, 2])
                    
                    with col_info:
                        st.markdown(f"#### 🌳 {p['name']}")
                        # Kiểm tra cờ minh chứng để cấp tích xanh
                        trang_thai = "✅ Đã xác thực Pháp lý & Vệ tinh" if p.get('verified', False) else "⚠️ Dữ liệu tham khảo (Chưa xác minh sổ đỏ)"
                        st.write(f"**Chủ sở hữu:** {p['owner']} | **Trạng thái:** {trang_thai}")
                        st.write(f"**Trữ lượng còn lại:** {int(p['volume']):,} tấn | **Giá chốt:** ${p['price']:,.2f} / tín chỉ")
                        
                        if st.button("🗺️ Xem Hồ sơ Không gian", key=f"btn_map_{p['id']}"):
                            st.session_state[f"show_map_{p['id']}"] = not st.session_state.get(f"show_map_{p['id']}", False)
                        
                        if st.session_state.get(f"show_map_{p['id']}", False):
                            if p.get('verified', False):
                                st.caption("📍 Ranh giới được số hóa từ Sổ đỏ tải lên và đối chiếu với AI vệ tinh.")
                                m_mini = folium.Map(location=[p['lat'], p['lon']], zoom_start=11)
                                folium.Polygon(
                                    locations=[[p['lat']-0.05, p['lon']-0.05], [p['lat']+0.05, p['lon']-0.05], 
                                            [p['lat']+0.05, p['lon']+0.05], [p['lat']-0.05, p['lon']+0.05]],
                                    color="green", fill=True, fill_opacity=0.4
                                ).add_to(m_mini)
                                st_folium(m_mini, width=500, height=300, key=f"fmap_{p['id']}")
                            else:
                                st.warning("Không có dữ liệu không gian do dự án chưa cung cấp minh chứng pháp lý hợp lệ.")
    
                    with col_action:
                        if vai_tro == "Doanh nghiệp mua tín chỉ":
                            # Tính năng mua lẻ: Người dùng tự nhập số lượng
                            sl_mua = st.number_input(
                                "Nhập số lượng muốn mua (tấn):", 
                                min_value=1, 
                                max_value=int(p['volume']), 
                                value=min(100, int(p['volume'])), 
                                key=f"sl_input_{p['id']}"
                            )
                            tong_tien = sl_mua * p['price']
                            st.info(f"Tổng thanh toán: **${tong_tien:,.2f}**")
                            
                            if st.button(f"🛒 Thanh toán", key=f"buy_{p['id']}", type="primary", use_container_width=True):
                                if st.session_state["wallet_balance"] >= tong_tien:
                                    st.session_state["wallet_balance"] -= tong_tien
                                    p['volume'] -= sl_mua
                                    st.success(f"🎉 Mua thành công {sl_mua} tín chỉ! Trừ ${tong_tien:,.2f} vào ví.")
                                    st.rerun() # Tải lại trang để cập nhật số dư và trữ lượng lập tức
                                else:
                                    st.error("❌ Ví không đủ tiền.")
                        elif vai_tro == "Chủ rừng / Kỹ sư MRV":
                            st.button("🔒 Đăng nhập tài khoản mua để giao dịch", key=f"lock_{p['id']}", disabled=True, use_container_width=True)
# 4. ĐIỀU HƯỚNG MÀN HÌNH
if not st.session_state["logged_in"]:
    hien_thi_cong_dang_nhap()
else:
    main_app()
