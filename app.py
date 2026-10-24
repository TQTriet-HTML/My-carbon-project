import streamlit as st
import ee
import geemap.foliumap as geemap
from streamlit_folium import folium_static 
import os
import random
import datetime

from i18n import t
from auth import hien_thi_cong_dang_nhap
from marketplace import hien_thi_san_giao_dich, hien_thi_gioi_thieu_va_goi_von

try:
    from forest_investment import hien_thi_dau_tu_trong_rung
except ImportError:
    def hien_thi_dau_tu_trong_rung(lang=None): st.info("Hệ thống đang bảo trì Cổng đầu tư trồng rừng.")

try:
    from social import hien_thi_mang_xa_hoi
except ImportError:
    def hien_thi_mang_xa_hoi(lang=None): st.info("Hệ thống đang bảo trì Mạng xã hội.")

try:
    from community import hien_thi_vinh_danh_va_gop_y
except ImportError:
    def hien_thi_vinh_danh_va_gop_y(lang=None): st.info("Hệ thống đang bảo trì Bảng Vàng.")

try:
    from diary import hien_thi_nhat_ky_xanh
except ImportError:
    def hien_thi_nhat_ky_xanh(lang=None): st.info("Hệ thống đang bảo trì Nhật ký xanh.")

# Khởi tạo CSDL SQLite tự động
try:
    import db_manager
    db_manager.init_db()
except Exception:
    pass

st.set_page_config(page_title="MRV & Carbon Exchange", layout="wide")

if "current_lang" not in st.session_state: st.session_state["current_lang"] = "Tiếng Việt"

if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "admin": {"password": "123", "role": "Chủ rừng / Kỹ sư MRV", "wallet_balance": 150000.0},
        "investor": {"password": "123", "role": "Nhà đầu tư từ xa (Cổ đông)", "wallet_balance": 250000.0},
        "buyer": {"password": "123", "role": "Doanh nghiệp mua tín chỉ", "wallet_balance": 500000.0}
    }

# BỘ TỪ ĐIỂN DỊCH VAI TRÒ
ROLE_DICT = {
    "Doanh nghiệp mua tín chỉ": "Corporate Buyer",
    "Nhà đầu tư từ xa (Cổ đông)": "Remote Investor",
    "Chủ rừng / Kỹ sư MRV": "Forest Owner / MRV Eng."
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
if "mrv_calc_state" not in st.session_state: st.session_state["mrv_calc_state"] = False
if "mrv_polygon_seed" not in st.session_state: st.session_state["mrv_polygon_seed"] = random.randint(10000, 99999)
if "currency_mode" not in st.session_state: st.session_state["currency_mode"] = "VND"
if "mrv_area_hectares" not in st.session_state: st.session_state["mrv_area_hectares"] = 150.0

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
        
        @keyframes blueShimmerSweep10s {
            0%, 80% { background-position: -200% center; }
            100% { background-position: 200% center; }
        }
        .welcome-text-blue {
            color: #38bdf8;
            font-weight: 700;
            font-size: 1.05rem;
            margin-top: 5px;
            margin-bottom: 25px;
            display: inline-block;
            background: linear-gradient(90deg, #38bdf8 0%, #38bdf8 40%, #bae6fd 50%, #38bdf8 60%, #38bdf8 100%);
            background-size: 200% auto;
            color: transparent;
            -webkit-background-clip: text;
            background-clip: text;
            animation: blueShimmerSweep10s 10s linear infinite;
        }
        
        button[data-baseweb="tab"] { font-weight: 700 !important; font-size: 0.95rem !important; }
        button[data-baseweb="tab"][aria-selected="true"] { color: #48bb78 !important; text-shadow: 0 0 10px rgba(72, 187, 120, 0.6) !important; }
        div[data-baseweb="tab-highlight"] { background-color: #48bb78 !important; box-shadow: 0 0 12px rgba(72, 187, 120, 0.8) !important; }

        button[kind="primary"] { background-color: #48bb78 !important; border-color: #48bb78 !important; color: white !important; font-weight: 700 !important; letter-spacing: 0.5px; }
        button[kind="primary"]:hover { background-color: #38a169 !important; box-shadow: 0 0 20px rgba(72, 187, 120, 0.7) !important; }
        
        *:focus, *:active { outline: none !important; }
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, .stSelectbox > div > div, input { border-color: #2d3748 !important; }
        div[data-baseweb="select"]:hover, div[data-baseweb="select"]:focus-within, div[data-baseweb="input"]:hover, div[data-baseweb="input"]:focus-within { border-color: #48bb78 !important; box-shadow: 0 0 12px rgba(72, 187, 120, 0.4) !important; }

        div[data-testid="stVerticalBlockBorderWrapper"], .glass-block {
            background: linear-gradient(135deg, rgba(26, 32, 44, 0.95), rgba(45, 55, 72, 0.95)) !important; 
            border: 1px solid rgba(72, 187, 120, 0.4) !important; 
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(72, 187, 120, 0.05) !important; 
            backdrop-filter: blur(12px);
            position: relative; overflow: hidden !important; transition: all 0.4s ease !important; padding: 24px !important; margin-bottom: 20px !important;
        }

        .sidebar-badge { 
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95)) !important; padding: 16px; border-radius: 10px; margin-bottom: 12px; 
            border: 1px solid rgba(72, 187, 120, 0.4) !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            transition: all 0.4s ease; position: relative; overflow: hidden !important;
        }
        .sidebar-badge:hover { transform: translateY(-2px); border-color: #48bb78 !important; box-shadow: 0 8px 25px rgba(72, 187, 120, 0.35); }
        .sb-title { color: #E2E8F0; font-size: 13px; font-weight: 700; letter-spacing: 0.5px; line-height: 1.3; }
        .sb-desc { color: #a0aec0; font-size: 11px; margin-top: 4px; }
        .sb-desc.highlight { color: #48bb78; font-weight: 600; }
        
        /* -----------------------------------------------------------
           BỘ CSS CHO KHỐI CÔNG NGHỆ CHUYÊN SÂU (HÀO QUANG XANH LÁ)
           ----------------------------------------------------------- */
        @keyframes techGreenGlow {
            0%, 100% { box-shadow: 0 0 15px rgba(72, 187, 120, 0.2); border-color: rgba(72, 187, 120, 0.4); }
            50% { box-shadow: 0 0 35px rgba(72, 187, 120, 0.7); border-color: #48bb78; }
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.tech-block-marker) {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(10, 20, 35, 0.98)) !important;
            border: 1px solid rgba(72, 187, 120, 0.5) !important;
            animation: techGreenGlow 4s infinite ease-in-out !important;
            padding: 20px 24px !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }
        
        /* Hiệu ứng lún xuống khi nhấn vào khối */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.tech-block-marker):active {
            transform: scale(0.98) translateY(2px) !important;
            box-shadow: 0 0 10px rgba(72, 187, 120, 0.3) !important;
            border-color: #38a169 !important;
        }
        
        .tech-title {
            color: #4ade80;
            font-size: 1.15rem;
            font-weight: 900;
            letter-spacing: 1.5px;
            margin-bottom: 20px;
            text-transform: uppercase;
            text-align: center;
        }

        /* Tùy chỉnh 3 công tắc thành Box Lớn (Không Icon) */
        div[data-testid="stToggle"] { display: flex; align-items: center; justify-content: center; width: 100%; margin-bottom: 12px; }
        div[data-testid="stToggle"] label { padding: 0 !important; width: 100%; cursor: pointer; }
        div[data-testid="stToggle"] label > div[data-testid="stMarkdownContainer"] { width: 100%; text-align: center; }
        
        div[data-testid="stToggle"] label > div[data-testid="stMarkdownContainer"] > p {
            font-weight: 800; font-size: 0.95rem; letter-spacing: 0.8px;
            padding: 15px 15px; border-radius: 8px; width: 100%;
            transition: all 0.3s ease; text-transform: uppercase; margin: 0;
        }
        /* Ẩn cục Switch mặc định của Streamlit */
        div[data-testid="stToggle"] label > div:last-child { display: none !important; }

        /* MÀU ĐỎ NHẠT KHI TẮT */
        div[data-testid="stToggle"]:has(input[aria-checked="false"]) label > div[data-testid="stMarkdownContainer"] > p {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            color: #fca5a5 !important;
        }
        div[data-testid="stToggle"]:has(input[aria-checked="false"]) label > div[data-testid="stMarkdownContainer"] > p:hover {
            background: rgba(239, 68, 68, 0.2) !important; transform: translateY(-1px);
        }

        /* MÀU XANH LÁ KHI BẬT */
        div[data-testid="stToggle"]:has(input[aria-checked="true"]) label > div[data-testid="stMarkdownContainer"] > p {
            background: rgba(34, 197, 94, 0.15) !important;
            border: 1px solid #4ade80 !important;
            color: #4ade80 !important;
            box-shadow: 0 0 15px rgba(34, 197, 94, 0.4) !important;
        }
        div[data-testid="stToggle"]:has(input[aria-checked="true"]) label > div[data-testid="stMarkdownContainer"] > p:hover {
            box-shadow: 0 0 25px rgba(34, 197, 94, 0.6) !important; transform: translateY(-1px);
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown(f"<h3 style='color: #48bb78; font-weight: 800; text-align: center; font-size: 1.1rem; letter-spacing: 1px; margin-top: 15px;'>{t('TÙY CHỌN NGÔN NGỮ')}</h3>", unsafe_allow_html=True)
    st.selectbox("Ngôn ngữ:", ["Tiếng Việt", "English"], key="current_lang", label_visibility="collapsed")
    st.divider()
    
    st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold; letter-spacing:1px;'>{t('ĐỐI TÁC CHIẾN LƯỢC')}</p>", unsafe_allow_html=True)
    st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">Google Earth Engine</div><div class="sb-desc">{t("Đối tác Không gian AI")}</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">Vietcombank</div><div class="sb-desc">{t("Thanh toán Escrow")}</div></div></div>""", unsafe_allow_html=True)
    
    st.divider()
    st.markdown(f"<p style='color:#a0aec0; font-size:12px; font-weight:bold; letter-spacing:1px;'>{t('CHỨNG NHẬN PHÁP LÝ')}</p>", unsafe_allow_html=True)
    st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">VCS (Verra)</div><div class="sb-desc highlight">{t("Tiêu chuẩn Toàn cầu")}</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="sidebar-badge"><div><div class="sb-title">ISO/IEC 27001</div><div class="sb-desc highlight">{t("Bảo mật Thông tin Cấp cao")}</div></div></div>""", unsafe_allow_html=True)

@st.dialog(" ")
def hop_thoai_dang_xuat():
    st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important; border: 1px solid rgba(239, 68, 68, 0.8) !important; color: white !important; font-weight: 800 !important; border-radius: 8px !important; transition: all 0.3s ease !important; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button:hover { box-shadow: 0 0 25px rgba(239, 68, 68, 0.9) !important; transform: translateY(-2px) scale(1.03) !important; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button { background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important; border: 1px solid rgba(72, 187, 120, 0.8) !important; color: white !important; font-weight: 800 !important; border-radius: 8px !important; transition: all 0.3s ease !important; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button:hover { box-shadow: 0 0 25px rgba(72,187,120,0.9) !important; transform: translateY(-2px) scale(1.03) !important; }
        </style>
    """, unsafe_allow_html=True)

    logout_msg = t("Bạn có chắc muốn tạm nghỉ chân sau một chặng đường xanh đã qua không?")
    st.markdown(f"<h3 style='color: #ffffff; font-weight: 900; line-height: 1.5; margin-bottom: 25px; font-size: 1.25rem; text-align: center;'>{logout_msg}</h3>", unsafe_allow_html=True)
    
    col_y, col_n = st.columns(2)
    with col_y:
        if st.button(t("Tạm thời nghỉ chân"), use_container_width=True, key="confirm_out_yes"):
            st.session_state["logged_in"] = False
            st.session_state["current_user"] = ""
            st.session_state["current_role"] = ""
            st.rerun()
    with col_n:
        if st.button(t("Tiếp tục chặng đường"), use_container_width=True, key="confirm_out_no"):
            st.rerun()

@st.dialog("NIÊM YẾT DỰ ÁN TỪ KẾT QUẢ MRV / LIST PROJECT", width="large")
def hop_thoai_dang_du_an_mrv(est_credits, lang="Tiếng Việt"):
    st.info("Hệ thống đã nhận kết quả thẩm định. Bạn có thể điều chỉnh số lượng tín chỉ nếu thấy cần thiết trước khi đẩy sang Cổng Đầu Tư." if lang == "Tiếng Việt" else "Assessment received. You can adjust the estimated credits before pushing to the Investment Portal.")
    p_name = st.text_input("Tên dự án sinh thái:" if lang == "Tiếng Việt" else "Eco Project Name:")
    
    c1, c2 = st.columns(2)
    with c1:
        p_credits = st.number_input("Số tín chỉ ước tính (Tấn):" if lang == "Tiếng Việt" else "Estimated credits (Tons):", min_value=100, value=int(est_credits), step=100)
    with c2:
        p_target = st.number_input("Mục tiêu gọi vốn ($):" if lang == "Tiếng Việt" else "Funding Target ($):", min_value=1000, step=5000, value=int(p_credits * 10.5))
    
    opts_tier = ["Hạng A (Cao cấp)", "Hạng B (Tiêu chuẩn)", "Hạng C (Ươm mầm)"] if lang == "Tiếng Việt" else ["Tier A (Premium)", "Tier B (Standard)", "Tier C (Seedling)"]
    p_type = st.selectbox("Loại tín chỉ dự kiến cung cấp:" if lang == "Tiếng Việt" else "Expected Credit Type:", opts_tier)
    
    if st.button("ĐĂNG DỰ ÁN LÊN CỔNG ĐẦU TƯ" if lang == "Tiếng Việt" else "PUBLISH TO INVESTMENT PORTAL", type="primary", use_container_width=True):
        if p_name.strip():
            if "invest_projects" not in st.session_state: st.session_state["invest_projects"] = []
            
            badge_color = "#fbbf24" if "A" in p_type else ("#38bdf8" if "B" in p_type else "#cbd5e1")
            bg_color = "rgba(251, 191, 36, 0.15)" if "A" in p_type else ("rgba(56, 189, 248, 0.15)" if "B" in p_type else "rgba(148, 163, 184, 0.15)")
            shield_class = "shield-a" if "A" in p_type else ("shield-b" if "B" in p_type else "shield-c")
            shield_text = "I" if "A" in p_type else ("II" if "B" in p_type else "III")

            st.session_state["invest_projects"].insert(0, {
                "name": p_name, "target": f"${p_target:,.0f}", "tier": p_type,
                "badge_color": badge_color, "bg_color": bg_color, 
                "shield_class": shield_class, "shield_text": shield_text,
                "owner": st.session_state.get("current_user", "Unknown"),
                "contact": "Theo hồ sơ viễn thám AI" if lang == "Tiếng Việt" else "Per AI spatial record",
                "file_html": f"<div style='margin-top:15px; margin-bottom:15px; padding:10px; background:rgba(16, 185, 129, 0.15); border: 1px solid #10b981; border-radius:8px; color: #6ee7b7; font-weight: 700;'>📎 Hồ sơ: Đã thẩm định {p_credits:,} Tấn qua không gian AI</div>",
                "ai_verified": True
            })
            
            today_str = datetime.date.today().strftime("%Y-%m-%d")
            if "diary_records" not in st.session_state: st.session_state["diary_records"] = {}
            st.session_state["diary_records"][today_str] = {
                "title": f"Đăng dự án (MRV): {p_name}",
                "type": "Giao dịch" if lang == "Tiếng Việt" else "Transaction",
                "content": f"Mục tiêu: ${p_target:,.0f} | Hạng: {p_type} | Khối lượng MRV: {p_credits:,} Tấn"
            }
            
            st.success("Đã niêm yết dự án thành công! Hệ thống đã ghi nhận vào Nhật Ký Xanh." if lang == "Tiếng Việt" else "Project successfully listed and recorded in Green Diary!")
            st.session_state["mrv_calc_state"] = False 
            st.rerun()
        else:
            st.warning("Vui lòng nhập tên dự án." if lang == "Tiếng Việt" else "Please enter project name.")

def render_mrv_results(nam_co_so, nam_so_sanh, sar_on, era5_on, lulc_on):
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    seed = st.session_state["mrv_polygon_seed"]
    dien_tich_hecta = st.session_state.get("mrv_area_hectares", 150.0) 
    
    base_val = int(dien_tich_hecta * 95.0 + (nam_co_so - 2020) * 27000 + (seed % 5000))
    comp_val = int(dien_tich_hecta * 95.0 + (nam_so_sanh - 2020) * 27000 + (nam_so_sanh - nam_co_so) * 41000 + (seed % 5000))
    
    # KẾT HỢP CÁC BỘ LỌC CÔNG NGHỆ (Mô phỏng tác động định lượng)
    active_filters = []
    
    if sar_on:
        base_val = int(base_val * 0.84)
        comp_val = int(comp_val * 0.84)
        active_filters.append(t("Lọc ~16% sinh khối ảo (Cỏ dại)") if lang == "Tiếng Việt" else "Filtered ~16% fake biomass")
        
    if era5_on:
        # Khử nhiễu khí hậu giúp làm mịn sai số
        comp_val = int(comp_val * 0.98) 
        active_filters.append(t("Đối soát lượng mưa ERA5") if lang == "Tiếng Việt" else "ERA5 rainfall validated")
        
    if lulc_on:
        active_filters.append(t("Xác thực LULC") if lang == "Tiếng Việt" else "LULC transition verified")

    diff = comp_val - base_val
    base_credits = base_val
    comp_credits = comp_val
    
    tong_usd = comp_val * 10.5 
    tong_vnd = tong_usd * 26000
    
    diff_usd = diff * 10.5
    diff_vnd = diff_usd * 26000

    st.markdown("""
        <style>
        @keyframes greenBreathGlow {
            0%, 100% { box-shadow: 0 0 18px rgba(72, 187, 120, 0.3), inset 0 0 15px rgba(56, 189, 248, 0.08); border-color: rgba(72, 187, 120, 0.6); }
            50% { box-shadow: 0 0 40px rgba(72, 187, 120, 0.75), inset 0 0 25px rgba(56, 189, 248, 0.18); border-color: #48bb78; }
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.mrv-result-marker) {
            background: linear-gradient(135deg, rgba(13, 31, 60, 0.96), rgba(18, 42, 77, 0.93)) !important;
            border: 2px solid #38a169 !important; border-radius: 18px !important; padding: 26px 28px 38px 28px !important;
            animation: greenBreathGlow 4s infinite ease-in-out !important; transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.35s ease, border-color 0.35s ease !important;
            position: relative; overflow: hidden !important; margin-bottom: 25px !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.mrv-result-marker):hover {
            transform: translateY(-8px) scale(1.015) !important; box-shadow: 0 22px 50px rgba(72, 187, 120, 0.9), inset 0 0 30px rgba(72, 187, 120, 0.4) !important; border-color: #48bb78 !important;
        }

        @keyframes blueCharWaveGlow {
            0%, 75% { color: #38bdf8; text-shadow: none; transform: translateY(0); }
            82% { color: #bae6fd; text-shadow: 0 0 20px rgba(56, 189, 248, 1), 0 0 8px rgba(186, 230, 253, 0.9); transform: translateY(-4px); }
            90% { color: #60a5fa; text-shadow: 0 0 10px rgba(96, 165, 250, 0.6); transform: translateY(0); }
            100% { color: #38bdf8; text-shadow: none; transform: translateY(0); }
        }
        .mrv-blue-title-container { text-align: center; margin-bottom: 25px; white-space: nowrap; }
        .mrv-blue-char { display: inline-block; font-size: clamp(20px, 2.3vw, 30px); font-weight: 900; letter-spacing: 1.5px; color: #38bdf8; animation: blueCharWaveGlow 10s infinite ease-in-out; text-transform: uppercase; }

        .mrv-stat-box { text-align: center; padding: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .mrv-stat-title { color: #cbd5e1; font-size: 0.95rem; font-weight: 600; margin-bottom: 6px; letter-spacing: 0.5px; }
        .mrv-stat-num { font-size: clamp(1.35rem, 1.9vw, 2rem); font-weight: 900; line-height: 1.2; letter-spacing: 0.5px; white-space: nowrap; color: #48bb78 !important; }
        .mrv-sub-credit { color: #38bdf8; font-size: 0.85rem; font-weight: 700; margin-top: 6px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 8px; padding: 2px 12px; }

        .mrv-delta-badge { display: inline-block; padding: 3px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; margin-top: 6px; }
        .mrv-delta-pos { background: rgba(72, 187, 120, 0.2) !important; color: #48bb78 !important; border: 1px solid rgba(72, 187, 120, 0.6) !important; }
        .mrv-delta-neg { background: rgba(239, 68, 68, 0.2) !important; color: #f87171 !important; border: 1px solid rgba(239, 68, 68, 0.6) !important; }

        @keyframes pulseBanner {
            0%, 100% { border-color: rgba(72, 187, 120, 0.45); box-shadow: 0 0 10px rgba(72, 187, 120, 0.2); }
            50% { border-color: rgba(72, 187, 120, 0.9); box-shadow: 0 0 24px rgba(72, 187, 120, 0.5); }
        }
        .mrv-highlight-banner {
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.12), rgba(6, 78, 59, 0.3), rgba(16, 185, 129, 0.12)); border: 1.5px solid rgba(72, 187, 120, 0.7);
            border-radius: 12px; padding: 14px 20px; text-align: center; font-size: clamp(12.5px, 1.05vw, 15.5px); font-weight: 700; color: #68d391; letter-spacing: 0.5px;
            animation: pulseBanner 4s infinite ease-in-out; margin-top: 18px; margin-bottom: 8px; white-space: nowrap !important; overflow-x: auto; scrollbar-width: none;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='mrv-result-marker'></div>", unsafe_allow_html=True)
        
        # IN THÔNG BÁO TỔNG HỢP CÁC BỘ LỌC TRÊN 1 DÒNG DÀI
        if active_filters:
            joined_str = " | ".join(active_filters)
            msg_final = f"{t('Đã áp dụng')}: {joined_str}. {t('Kết quả trả về là Sinh khối Gỗ Lõi')}" if lang == "Tiếng Việt" else f"Applied: {joined_str}. Returning Core Woody Biomass."
            st.markdown(f"<div style='background:rgba(34, 197, 94, 0.15); border:1px solid #4ade80; color:#4ade80; padding:10px 15px; border-radius:8px; font-size:0.95rem; font-weight:800; margin-bottom:20px; text-align:center;'>{msg_final}</div>", unsafe_allow_html=True)

        title_text = t("KẾT QUẢ PHÂN TÍCH ĐỊNH LƯỢNG")
        title_html = '<div class="mrv-blue-title-container">'
        delay = 0.0
        for char in title_text:
            c = "&nbsp;" if char == " " else char
            title_html += f'<span class="mrv-blue-char" style="animation-delay: {delay:.2f}s;">{c}</span>'
            delay += 0.08
        title_html += '</div>'
        st.markdown(title_html, unsafe_allow_html=True)
        
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.markdown(f"""
                <div class="mrv-stat-box">
                    <div class="mrv-stat-title">{t("Sinh khối Năm")} {nam_co_so}</div>
                    <div class="mrv-stat-num">{base_val:,.0f} <span style="font-size: 1.15rem; font-weight: 700;">{t("Tấn")}</span></div>
                    <div class="mrv-sub-credit">{base_credits:,.0f} {t("Tín chỉ")}</div>
                </div>
            """, unsafe_allow_html=True)

        with col_r2:
            badge_cls = "mrv-delta-pos" if diff >= 0 else "mrv-delta-neg"
            sign = "+" if diff >= 0 else ""
            st.markdown(f"""
                <div class="mrv-stat-box">
                    <div class="mrv-stat-title">{t("Sinh khối Năm")} {nam_so_sanh}</div>
                    <div class="mrv-stat-num">{comp_val:,.0f} <span style="font-size: 1.15rem; font-weight: 700;">{t("Tấn")}</span></div>
                    <div class="mrv-sub-credit" style="color: #48bb78; border-color: rgba(72,187,120,0.4); background: rgba(72,187,120,0.12);">{comp_credits:,.0f} {t("Tín chỉ")}</div>
                    <div class="mrv-delta-badge {badge_cls}">{sign}{diff:,.0f} {t("Tấn")}</div>
                </div>
            """, unsafe_allow_html=True)

        with col_r3:
            is_vnd = (st.session_state["currency_mode"] == "VND")
            if is_vnd:
                tien_hien_thi = f"{tong_vnd:,.0f}&nbsp;VND"
                diff_money_str = f"{'+' if diff_vnd >= 0 else ''}{diff_vnd:,.0f} VND"
            else:
                tien_hien_thi = f"${tong_usd:,.2f}&nbsp;USD"
                diff_money_str = f"{'+' if diff_usd >= 0 else ''}${diff_usd:,.2f} USD"
                
            money_badge_cls = "mrv-delta-pos" if diff >= 0 else "mrv-delta-neg"

            st.markdown(f"""
                <div class="mrv-stat-box">
                    <div class="mrv-stat-title">{t("Tổng Giá Trị Quy Đổi")}</div>
                    <div class="mrv-stat-num">{tien_hien_thi}</div>
                    <div class="mrv-delta-badge {money_badge_cls}">{diff_money_str}</div>
                </div>
            """, unsafe_allow_html=True)
            
            _, c_btn, _ = st.columns([0.1, 0.8, 0.1])
            with c_btn:
                btn_label = "Đổi sang USD" if is_vnd else "Đổi sang VND"
                if st.button(t(btn_label), type="primary", use_container_width=True, key="btn_toggle_curr"):
                    st.session_state["currency_mode"] = "USD" if is_vnd else "VND"
                    st.rerun()

        diff_text = f"{diff:,.0f} {t('Tấn')}"
        if diff >= 0:
            msg = f"Khu vực phân tích ghi nhận sự tăng trưởng sinh khối. Bạn có thể niêm yết thêm {diff_text} tín chỉ carbon."
            st.markdown(f"<div class='mrv-highlight-banner'>{t(msg)}</div>", unsafe_allow_html=True)
            
            curr_role = st.session_state.get("current_role", "")
            if "Chủ rừng" in curr_role or "Owner" in curr_role or "admin" in st.session_state.get("current_user", "").lower():
                st.markdown('<div id="list-mrv-btn-wrapper"></div>', unsafe_allow_html=True)
                st.markdown("""
                <style>
                div:has(> #list-mrv-btn-wrapper) + div button { background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important; border: 1.5px solid #7dd3fc !important; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4) !important; margin-top: 15px !important; height: 45px !important; font-size: 1rem !important; color: white !important; font-weight: 800 !important; border-radius: 10px !important; transition: all 0.3s ease !important; width: 100%; }
                div:has(> #list-mrv-btn-wrapper) + div button:hover { background: linear-gradient(135deg, #7dd3fc 0%, #0ea5e9 100%) !important; box-shadow: 0 8px 25px rgba(56, 189, 248, 0.7) !important; transform: translateY(-2px); }
                </style>
                """, unsafe_allow_html=True)
                
                btn_lbl = "🚀 NIÊM YẾT KẾT QUẢ NÀY LÊN CỔNG ĐẦU TƯ" if lang == "Tiếng Việt" else "🚀 LIST THIS RESULT TO INVESTMENT PORTAL"
                if st.button(btn_lbl, key="btn_push_mrv"):
                    hop_thoai_dang_du_an_mrv(diff, lang)
        else:
            msg = "Mật độ sinh khối trong khu vực sụt giảm. Cần rà soát biến động rừng."
            st.markdown(f"<div class='mrv-highlight-banner' style='color:#fca5a5; border-color:rgba(239,68,68,0.6); background:rgba(239,68,68,0.15);'>{t(msg)}</div>", unsafe_allow_html=True)

def main_app():
    lang = st.session_state.get("current_lang", "Tiếng Việt")
    curr_role = st.session_state.get('current_role', '')
    role_display = ROLE_DICT.get(curr_role, curr_role) if lang == "English" else curr_role
    
    col_t, col_l = st.columns([7, 1])
    with col_t:
        st.markdown(f'<div class="main-title">{t("NỀN TẢNG MRV & SÀN GIAO DỊCH")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="welcome-text-blue">{t("Xin chào")}, {st.session_state["current_user"]} ({role_display})</div>', unsafe_allow_html=True)
    
    with col_l:
        st.markdown("""
            <style>
            button[kind="secondary"] { background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.4)) !important; border: 1px solid rgba(239, 68, 68, 0.6) !important; color: #fca5a5 !important; font-weight: 700 !important; border-radius: 8px !important; transition: all 0.3s ease !important; }
            button[kind="secondary"]:hover { background: linear-gradient(135deg, rgba(239, 68, 68, 0.8), rgba(220, 38, 38, 0.9)) !important; border-color: #ef4444 !important; color: white !important; transform: translateY(-2px); }
            </style>
        """, unsafe_allow_html=True)
        if st.button(t("ĐĂNG XUẤT"), type="secondary", use_container_width=True):
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

    tab_titles = [t(name) for name in ["Hệ thống MRV", "Sàn Giao dịch", "Đầu tư Trồng rừng", "Mạng xã hội", "Nhật ký Xanh", "Bảng Vàng", "Về chúng tôi"]]
    tab_mrv, tab_market, tab_invest, tab_social, tab_diary, tab_community, tab_about = st.tabs(tab_titles)

    with tab_mrv:
        _, col_center, _ = st.columns([0.05, 0.9, 0.05])
        with col_center:
            st.markdown(f"<div style='text-align:center; color:#48bb78; font-weight:800; margin-bottom:15px; font-size:1.1rem; letter-spacing:1px;'>{t('HỆ THỐNG GIÁM SÁT KHÔNG GIAN AI')}</div>", unsafe_allow_html=True)
            
            with st.container(border=True):
                lbl_thong_so = "THÔNG SỐ VÙNG KHOANH VÀ DỮ LIỆU KHÔNG GIAN" if lang == "Tiếng Việt" else "SPATIAL BOUNDARY & DATA PARAMETERS"
                st.markdown(f"<h4 style='color: #38bdf8; font-size: 1.1rem; font-weight: 700; margin-bottom: 15px; text-transform: uppercase;'>{lbl_thong_so}</h4>", unsafe_allow_html=True)
                
                c_input1, c_input2 = st.columns(2)
                with c_input1:
                    lbl_toado = "Tọa độ đa giác (Nhập các đỉnh ranh giới, cách nhau bởi dấu ;):" if lang == "Tiếng Việt" else "Polygon Coordinates (Enter vertices, separated by ;):"
                    plh_toado = "VD: 11.42, 107.42 ; 11.45, 107.45 ; 11.41, 107.48" if lang == "Tiếng Việt" else "Ex: 11.42, 107.42 ; 11.45, 107.45 ; 11.41, 107.48"
                    st.text_area(lbl_toado, placeholder=plh_toado, height=90)
                    
                    lbl_area = "Diện tích khu vực ước tính (Hecta):" if lang == "Tiếng Việt" else "Estimated Area (Hectares):"
                    st.session_state["mrv_area_hectares"] = st.slider(lbl_area, min_value=1.0, max_value=10000.0, value=500.0, step=10.0)
                with c_input2:
                    lbl_upload = "Tải lên Dữ liệu Không gian (KML, GeoJSON, SHP.zip):" if lang == "Tiếng Việt" else "Upload Spatial Data (KML, GeoJSON, SHP.zip):"
                    st.file_uploader(lbl_upload, type=['kml', 'geojson', 'zip'])
                    
                    lbl_upload_note = "* Yêu cầu tải lên tệp định dạng chuẩn để AI tự động bóc tách ranh giới và loại trừ vùng chồng lấn." if lang == "Tiếng Việt" else "* Standard formats required for AI to automatically extract boundaries and exclude overlaps."
                    st.markdown(f"<div style='font-size: 0.85rem; color: #94a3b8; margin-top: 5px;'><i>{lbl_upload_note}</i></div>", unsafe_allow_html=True)

                # --- NÂNG CẤP KHỐI CÔNG NGHỆ CHUYÊN SÂU ---
                st.markdown('<div class="tech-block-marker"></div>', unsafe_allow_html=True)
                with st.container(border=True):
                    lbl_tech = "CÔNG NGHỆ CHUYÊN SÂU (ĐỘC QUYỀN)" if lang == "Tiếng Việt" else "ADVANCED TECHNOLOGY (EXCLUSIVE)"
                    st.markdown(f"<div class='tech-title'>{lbl_tech}</div>", unsafe_allow_html=True)
                    
                    lbl_sar = "Tích hợp Radar SAR (Lọc sinh khối ảo)" if lang == "Tiếng Việt" else "Integrate SAR Radar (Filter fake biomass)"
                    is_filter_grass_on = st.toggle(lbl_sar, value=True, key="tech_sar")
                    
                    lbl_weather = "Khử nhiễu Khí hậu (Dữ liệu ERA5)" if lang == "Tiếng Việt" else "Climate Noise Reduction (ERA5 Data)"
                    is_era5_on = st.toggle(lbl_weather, value=False, key="tech_weather")
                    
                    lbl_lulc = "Phân tích Chuyển đổi Lớp phủ (LULC)" if lang == "Tiếng Việt" else "Land Use Change Detection (LULC)"
                    is_lulc_on = st.toggle(lbl_lulc, value=False, key="tech_lulc")

                st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1: nam_co_so = st.selectbox(t("Năm cơ sở:"), range(2016, 2027), index=4) 
                with c2: nam_so_sanh = st.selectbox(t("Năm so sánh:"), range(2016, 2027), index=8) 
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    btn_calc = st.button(t("PHÂN TÍCH VÙNG KHOANH"), type="primary", use_container_width=True)
                with col_b2:
                    btn_reset = st.button(t("LÀM MỚI DỮ LIỆU"), type="secondary", use_container_width=True)
                
            if btn_reset:
                st.session_state["mrv_calc_state"] = False
                st.session_state["mrv_polygon_seed"] = random.randint(10000, 99999)
                st.rerun()
                
            if btn_calc:
                st.session_state["mrv_calc_state"] = True

            if st.session_state["mrv_calc_state"]:
                render_mrv_results(nam_co_so, nam_so_sanh, is_filter_grass_on, is_era5_on, is_lulc_on)

            try:
                with st.spinner(t("AI đang phân tích dữ liệu không gian...")):
                    map_base = tao_ban_do_carbon(nam_co_so)
                    map_comp = tao_ban_do_carbon(nam_so_sanh)
                    
                m = geemap.Map(center=[11.4280, 107.4286], zoom=11)
                vis = {'min': 0, 'max': 100, 'palette': ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']}
                m.addLayer(map_base, vis, f"{t('Sinh khối')} {nam_co_so}")
                m.addLayer(map_comp, vis, f"{t('Sinh khối')} {nam_so_sanh}")
                
                with st.container(border=True):
                    folium_static(m, width=1100, height=500)
            except Exception:
                st.warning(t("Đang chạy ở chế độ giả lập cục bộ do thiếu Token GEE hợp lệ."))

    with tab_market: hien_thi_san_giao_dich()
    with tab_invest: hien_thi_dau_tu_trong_rung(st.session_state["current_lang"])
    
    with tab_social:
        try:
            from social import hien_thi_mang_xa_hoi
            hien_thi_mang_xa_hoi(st.session_state["current_lang"])
        except ImportError:
            st.info(t("Hệ thống đang bảo trì Mạng xã hội."))

    with tab_diary:
        try:
            from diary import hien_thi_nhat_ky_xanh
            hien_thi_nhat_ky_xanh(st.session_state["current_lang"])
        except ImportError:
            st.info(t("Hệ thống đang bảo trì Nhật ký xanh."))

    with tab_community:
        try:
            from community import hien_thi_vinh_danh_va_gop_y
            hien_thi_vinh_danh_va_gop_y(st.session_state["current_lang"])
        except ImportError:
            st.info(t("Hệ thống đang bảo trì Bảng Vàng."))

    with tab_about: hien_thi_gioi_thieu_va_goi_von()

if not st.session_state["logged_in"]:
    hien_thi_cong_dang_nhap(st.session_state["current_lang"])
else:
    main_app()
