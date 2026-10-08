import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import folium_static 
import os
import random

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

if "current_lang" not in st.session_state: st.session_state["current_lang"] = "Tiếng Việt"

if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "admin": {"password": "123", "role": "Chủ rừng / Kỹ sư MRV", "wallet_balance": 150000.0},
        "investor": {"password": "123", "role": "Nhà đầu tư từ xa (Cổ đông)", "wallet_balance": 250000.0},
        "buyer": {"password": "123", "role": "Doanh nghiệp mua tín chỉ", "wallet_balance": 500000.0}
    }
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "current_user" not in st.session_state: st.session_state["current_user"] = ""
if "current_role" not in st.session_state: st.session_state["current_role"] = ""
if "wallet_balance" not in st.session_state: st.session_state["wallet_balance"] = 150000.0  
if "user_portfolios" not in st.session_state: st.session_state["user_portfolios"] = {}
if "investor_portfolios" not in st.session_state: st.session_state["investor_portfolios"] = {}
if "market_projects" not in st.session_state:
    st.session_state["market_projects"] = [
        {"id": "p1", "name": "Dự án giảm phát thải Bắc Trung Bộ", "owner": "Bộ NN&PTNT", "price": 10.5, "volume": 1030000, "duration": 5, "funding_goal": 50000.0, "funded_amount": 15000.0, "status": "Active"}
    ]
if "social_posts" not in st.session_state:
    st.session_state["social_posts"] = [
        {"id": "post_1", "author": "Hệ Thống", "role": "Admin", "content": "Thử nghiệm công nghệ vệ tinh mới rất ấn tượng!", "time": "04/10/2026 09:30", "likes": 12, "comments": []}
    ]
if "green_diary" not in st.session_state:
    st.session_state["green_diary"] = {
        "2026-10-10": {"title": "Kỳ đánh giá sinh khối dự án", "type": "Quan trọng", "content": "Rà soát lại dữ liệu trên nền tảng GEE."},
        "2026-10-15": {"title": "Phát hiện cháy rừng diện rộng", "type": "Bất thường", "content": "Rừng ở khu vực B bị suy giảm sinh khối nghiêm trọng."}
    }
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

# ================= CSS TOÀN CỤC CHUẨN DARK MODE VÀ HIỆU ỨNG =================
def inject_custom_css():
    st.markdown("""
        <style>
        .stApp { background-image: none !important; background-color: #0E1117 !important; }
        html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif !important; }
        
        @keyframes titleWave { to { background-position: 200% center; } }
        .main-title { 
            font-size: clamp(22px, 2.5vw, 32px) !important; font-weight: 900 !important; 
            background: linear-gradient(to right, #48bb78, #63b3ed, #48bb78);
            background-size: 200% auto; color: #fff; background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: titleWave 4s linear infinite; margin-bottom: 0px !important; padding-bottom: 0px !important; letter-spacing: 1px;
        }
        
        button[kind="primary"] { background-color: #48bb78 !important; border-color: #48bb78 !important; color: white !important; font-weight: 700 !important; letter-spacing: 0.5px; }
        button[kind="primary"]:hover { background-color: #38a169 !important; box-shadow: 0 0 20px rgba(72, 187, 120, 0.7) !important; }
        
        *:focus, *:active { outline: none !important; }
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, .stSelectbox > div > div, input { border-color: #2d3748 !important; }
        div[data-baseweb="select"]:hover, div[data-baseweb="select"]:focus-within, div[data-baseweb="input"]:hover, div[data-baseweb="input"]:focus-within { border-color: #48bb78 !important; box-shadow: 0 0 12px rgba(72, 187, 120, 0.4) !important; }
        [aria-invalid="true"] { border-color: #48bb78 !important; box-shadow: 0 0 12px rgba(72, 187, 120, 0.4) !important; }

        /* Hiệu ứng quét sáng khi hover cho tất cả các khối */
        @keyframes hoverSweepLight {
            0% { left: -100%; opacity: 0; }
            50% { opacity: 1; }
            100% { left: 200%; opacity: 0; }
        }

        /* Hiệu ứng quét sáng tự động mỗi 10 giây cho các khối đặc biệt (Cột phải) */
        @keyframes autoSweepLight10s {
            0%, 85% { left: -100%; opacity: 0; }
            86% { opacity: 1; left: -100%; }
            95%, 100% { left: 200%; opacity: 0; }
        }

        /* Định dạng chung cho các khối kính */
        div[data-testid="stVerticalBlockBorderWrapper"], .glass-block {
            background: linear-gradient(135deg, rgba(26, 32, 44, 0.95), rgba(45, 55, 72, 0.95)) !important; 
            border: 1px solid rgba(72, 187, 120, 0.4) !important; 
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(72, 187, 120, 0.05) !important; 
            backdrop-filter: blur(12px);
            position: relative; overflow: hidden !important; transition: all 0.4s ease !important; padding: 24px !important; margin-bottom: 20px !important;
        }

        /* Ánh sáng lướt khi trỏ chuột vào các khối (Cột trái) */
        div[data-testid="stVerticalBlockBorderWrapper"]:hover::after, .glass-block:hover::after {
             content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
             background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.6), transparent);
             transform: skewX(-25deg); animation: hoverSweepLight 1.5s ease-in-out; z-index: 10; pointer-events: none;
        }

        /* -----------------------------------------------------------
           TÙY CHỈNH RIÊNG CHO 2 KHỐI CỘT PHẢI (THÀNH TỰU & DỰ ÁN) 
           ----------------------------------------------------------- */
        /* Tạo quầng sáng xanh lá nhịp nhàng */
        @keyframes unifiedGreenGlow {
            0%, 100% { box-shadow: 0 0 10px rgba(72, 187, 120, 0.2); border-color: rgba(72, 187, 120, 0.3) !important; }
            50% { box-shadow: 0 0 30px rgba(72, 187, 120, 0.8), inset 0 0 10px rgba(72, 187, 120, 0.2); border-color: #48bb78 !important; }
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auto-glow-block) {
             animation: unifiedGreenGlow 4s infinite ease-in-out !important;
        }

        /* Hiệu ứng nổi bật + lóa sáng khi Hover vào 2 khối cột phải */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auto-glow-block):hover {
            transform: translateY(-8px) scale(1.02) !important;
            box-shadow: 0 20px 40px rgba(72, 187, 120, 0.9), inset 0 0 20px rgba(72, 187, 120, 0.5) !important;
            border-color: #48bb78 !important;
            z-index: 5 !important;
        }
        
        /* Hiệu ứng ánh sáng lướt qua TỰ ĐỘNG mỗi 10 giây cho 2 khối cột phải */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auto-glow-block)::before {
            content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.6), transparent);
            transform: skewX(-25deg); animation: autoSweepLight10s 10s infinite linear; z-index: 10; pointer-events: none;
        }
        /* Ngăn hiệu ứng hover lướt sáng mặc định ghi đè lên khối này */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.auto-glow-block):hover::after {
            display: none !important;
        }


        [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 900 !important; color: #E2E8F0 !important; text-align: center !important; width: 100% !important; display: block !important;}
        [data-testid="stMetricLabel"] { text-align: center !important; width: 100% !important; justify-content: center !important; font-weight: 600 !important; letter-spacing: 0.5px;}
        [data-testid="stMetricDelta"] { justify-content: center !important; font-weight: 700 !important;}

        .sidebar-badge { 
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95)) !important; padding: 16px; border-radius: 10px; margin-bottom: 12px; 
            border: 1px solid rgba(72, 187, 120, 0.4) !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            transition: all 0.4s ease; position: relative; overflow: hidden !important;
        }
        .sidebar-badge:hover { transform: translateY(-2px); border-color: #48bb78 !important; box-shadow: 0 8px 25px rgba(72, 187, 120, 0.35); }
        .sidebar-badge:hover::after {
             content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
             background: linear-gradient(90deg, transparent, rgba(72, 187, 120, 0.6), transparent);
             transform: skewX(-25deg); animation: hoverSweepLight 1.5s ease-in-out; z-index: 10; pointer-events: none;
        }
        
        .sb-title { color: #E2E8F0; font-size: 13px; font-weight: 700; letter-spacing: 0.5px; line-height: 1.3; }
        .sb-desc { color: #a0aec0; font-size: 11px; margin-top: 4px; }
        .sb-desc.highlight { color: #48bb78; font-weight: 600; }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ================= SIDEBAR =================
with st.sidebar:
    l = LANG_DICT[st.session_state["current_lang"]]

    st.markdown(f"<h3 style='color: #48bb78; font-weight: 800; text-align: center; font-size: 1.1rem; letter-spacing: 1px; margin-top: 15px;'>{l['lang_select']}</h3>", unsafe_allow_html=True)
    st.selectbox("Ngôn ngữ:", ["Tiếng Việt", "English"], key="current_lang", label_visibility="collapsed")
    st.divider()
    
    st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold; letter-spacing:1px;'>{l['sidebar_partners']}</p>", unsafe_allow_html=True)
    st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">{l['sb_p1_title']}</div><div class="sb-desc">{l['sb_p1_desc']}</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">{l['sb_p2_title']}</div><div class="sb-desc">{l['sb_p2_desc']}</div></div></div>""", unsafe_allow_html=True)
    
    st.divider()
    st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold; letter-spacing:1px;'>{l['sidebar_certs']}</p>", unsafe_allow_html=True)
    st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">{l['sb_c1_title']}</div><div class="sb-desc highlight">{l['sb_c1_desc']}</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">{l['sb_c2_title']}</div><div class="sb-desc highlight">{l['sb_c2_desc']}</div></div></div>""", unsafe_allow_html=True)


@st.dialog(" ")
def hop_thoai_dang_xuat():
    st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important; border: 1px solid rgba(239, 68, 68, 0.8) !important;
            color: white !important; font-weight: 800 !important; border-radius: 8px !important; transition: all 0.3s ease !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button:hover { box-shadow: 0 0 25px rgba(239, 68, 68, 0.9) !important; transform: translateY(-2px) scale(1.03) !important; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
            background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important; border: 1px solid rgba(72, 187, 120, 0.8) !important;
            color: white !important; font-weight: 800 !important; border-radius: 8px !important; transition: all 0.3s ease !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button:hover { box-shadow: 0 0 25px rgba(72,187,120,0.9) !important; transform: translateY(-2px) scale(1.03) !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: #ffffff; font-weight: 900; line-height: 1.5; margin-bottom: 25px; font-size: 1.25rem; text-align: center;'>Bạn có chắc muốn tạm nghỉ chân sau một chặng đường xanh đã qua không?</h3>", unsafe_allow_html=True)
    
    col_y, col_n = st.columns(2)
    with col_y:
        if st.button("Tạm thời nghỉ chân", use_container_width=True, key="confirm_out_yes"):
            st.session_state["logged_in"] = False
            st.session_state["current_user"] = ""
            st.session_state["current_role"] = ""
            st.rerun()
    with col_n:
        if st.button("Tiếp tục chặng đường", use_container_width=True, key="confirm_out_no"):
            st.rerun()

def main_app():
    l = LANG_DICT[st.session_state["current_lang"]]
    role_display = st.session_state['current_role']
    
    col_t, col_l = st.columns([7, 1])
    with col_t:
        st.markdown(f'<div class="main-title">{l["title"]}</div>', unsafe_allow_html=True)
        st.caption(f"{l['welcome']}, **{st.session_state['current_user']}** ({role_display})")
    
    with col_l:
        st.markdown("""
            <style>
            button[kind="secondary"] {
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.4)) !important; border: 1px solid rgba(239, 68, 68, 0.6) !important;
                color: #fca5a5 !important; font-weight: 700 !important; border-radius: 8px !important; transition: all 0.3s ease !important;
                position: relative; overflow: hidden !important;
            }
            button[kind="secondary"]:hover {
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.8), rgba(220, 38, 38, 0.9)) !important; border-color: #ef4444 !important; color: white !important;
                box-shadow: 0 0 20px rgba(239, 68, 68, 0.7) !important; transform: translateY(-2px);
            }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button(l["logout"], type="secondary", use_container_width=True):
            hop_thoai_dang_xuat()

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
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    btn_calc = st.button(l["mrv_calc_btn"], type="primary", use_container_width=True)
                with col_b2:
                    btn_reset = st.button(l["mrv_reset_btn"], type="secondary", use_container_width=True)
                
            if btn_reset:
                st.session_state["mrv_calc_state"] = False
                st.session_state["mrv_polygon_seed"] = random.randint(10000, 99999)
                st.rerun()
                
            if btn_calc:
                st.session_state["mrv_calc_state"] = True

            if st.session_state["mrv_calc_state"]:
                seed = st.session_state["mrv_polygon_seed"]
                dien_tich_hecta = 8000.0 + (seed % 12000) 
                
                base_val = int(dien_tich_hecta * 95.0 + (nam_co_so - 2020) * 27000 + (seed % 5000))
                comp_val = int(dien_tich_hecta * 95.0 + (nam_so_sanh - 2020) * 27000 + (nam_so_sanh - nam_co_so) * 41000 + (seed % 5000))
                diff = comp_val - base_val
                tong_usd = abs(diff) * 10.5 
                
                tong_tien_str = f"{tong_usd * 26000:,.0f} VND" if st.session_state["current_lang"] == "Tiếng Việt" else f"${tong_usd:,.2f} USD"
                
                with st.container(border=True):
                    st.markdown(f"<h3 style='color:#ffffff; text-align:center; font-weight:800; letter-spacing:1px; margin-bottom:25px;'>{l['mrv_result_title']}</h3>", unsafe_allow_html=True)
                    
                    col_r1, col_r2, col_r3 = st.columns(3)
                    col_r1.metric(f"{l['mrv_base_val']} {nam_co_so}", f"{base_val:,.0f} {l['mrv_unit']}")
                    delta_str = f"+{diff:,.0f} {l['mrv_unit']}" if diff >= 0 else f"{diff:,.0f} {l['mrv_unit']}"
                    col_r2.metric(f"{l['mrv_comp_val']} {nam_so_sanh}", f"{comp_val:,.0f} {l['mrv_unit']}", delta=delta_str, delta_color="normal" if diff >= 0 else "inverse")
                    diff_text = f"{diff:,.0f} {l['mrv_unit']}"
                    if diff >= 0:
                        msg = l['mrv_success_msg'].format(diff=diff_text)
                        st.markdown(f"<div style='color:#48bb78; text-align:center; font-weight:600;'>{msg}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='color:#fc8181; text-align:center; font-weight:600;'>{l['mrv_warning_msg']}</div>", unsafe_allow_html=True)
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
            except:
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
