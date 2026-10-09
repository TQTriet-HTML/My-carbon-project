import streamlit as st
import streamlit.components.v1 as components

def get_mission_animation_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: #0B111E;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .stage {
            position: relative;
            width: 100%;
            max-width: 680px;
            height: 480px;
            background: radial-gradient(circle at center, #112233 0%, #080D16 100%);
            border-radius: 16px;
            border: 2px solid rgba(72, 187, 120, 0.4);
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(72, 187, 120, 0.1);
            overflow: hidden;
        }

        /* KHUNG CHỮ CHÚ THÍCH CÂU CHUYỆN SỨ MỆNH */
        .story-caption {
            position: absolute;
            top: 25px;
            left: 20px;
            right: 20px;
            text-align: center;
            font-size: 15px;
            font-weight: 700;
            color: #48bb78;
            letter-spacing: 0.5px;
            min-height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(15, 23, 42, 0.7);
            border-radius: 10px;
            border: 1px solid rgba(72, 187, 120, 0.3);
            padding: 8px 16px;
            z-index: 20;
        }

        /* MẶT ĐẤT */
        .ground {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 90px;
            background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
            border-top: 3px solid #374151;
            transition: all 1s ease;
            z-index: 5;
        }

        /* 1. RỪNG XANH VÀ CÂY */
        .forest-group {
            position: absolute;
            bottom: 90px;
            width: 100%;
            height: 250px;
            display: flex;
            justify-content: space-around;
            align-items: flex-end;
            padding: 0 40px;
            z-index: 6;
        }
        .tree {
            transform-origin: bottom center;
            transition: all 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        /* 2. NHÀ MÁY VÀ KHÓI THẢI */
        .factory-group {
            position: absolute;
            bottom: 90px;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: all 1.2s ease;
            z-index: 7;
        }
        .smoke-particle {
            position: absolute;
            border-radius: 50%;
            background: rgba(148, 163, 184, 0.4);
            filter: blur(4px);
            opacity: 0;
        }

        /* 3. VÙNG KHÔNG KHÍ Ô NHIỄM */
        .pollution-sky {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(30, 41, 59, 0);
            pointer-events: none;
            transition: background 1.5s ease;
            z-index: 4;
        }

        /* 4. TIA SÁNG TÍN CHỈ CARBON */
        .carbon-matrix {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            opacity: 0;
            transition: opacity 1.2s ease;
            z-index: 10;
        }
        .energy-beam {
            position: absolute;
            height: 2px;
            background: linear-gradient(90deg, transparent, #48bb78, #38bdf8, transparent);
            box-shadow: 0 0 12px #48bb78;
        }

        /* 5. LOGO CHUNG CUỘC & SLOGAN */
        .finale-logo-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.6);
            opacity: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: all 1.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            z-index: 25;
            background: radial-gradient(circle, rgba(11, 25, 44, 0.95) 0%, rgba(8, 13, 22, 0.98) 100%);
            width: 100%;
            height: 100%;
        }
        .earth-sphere {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #38bdf8 0%, #0284c7 60%, #0369a1 100%);
            box-shadow: 0 0 35px rgba(56, 189, 248, 0.8), inset 0 0 15px rgba(255, 255, 255, 0.6);
            position: relative;
            margin-bottom: -15px;
            z-index: 2;
            animation: earthPulse 3s infinite ease-in-out;
        }
        @keyframes earthPulse {
            0%, 100% { box-shadow: 0 0 25px rgba(56, 189, 248, 0.6); }
            50% { box-shadow: 0 0 45px rgba(56, 189, 248, 0.95); }
        }
        .leaf-pair {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            gap: 10px;
            z-index: 3;
        }
        .leaf {
            width: 44px;
            height: 75px;
            background: linear-gradient(135deg, #48bb78 0%, #22c55e 60%, #15803d 100%);
            box-shadow: 0 0 20px rgba(72, 187, 120, 0.8);
        }
        .leaf-left {
            border-radius: 80% 0 80% 0;
            transform: rotate(-45deg);
        }
        .leaf-right {
            border-radius: 0 80% 0 80%;
            transform: rotate(45deg);
        }
        .slogan-banner {
            margin-top: 25px;
            font-size: 20px;
            font-weight: 900;
            letter-spacing: 2px;
            background: linear-gradient(90deg, #48bb78, #38bdf8, #48bb78);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            text-shadow: 0 0 20px rgba(72, 187, 120, 0.5);
        }
        .sub-slogan {
            font-size: 13px;
            color: #94a3b8;
            margin-top: 8px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
    </style>
    </head>
    <body>

    <div class="stage">
        <div class="story-caption" id="captionText">1. Khởi nguyên: Từ một mầm xanh vươn mình thành rừng nguyên sinh trù phú...</div>
        <div class="pollution-sky" id="skyEffect"></div>

        <!-- Rừng cây -->
        <div class="forest-group" id="forestGroup">
            <svg class="tree" id="tree1" width="80" height="150" viewBox="0 0 100 200">
                <rect x="42" y="130" width="16" height="70" fill="#854d0e" rx="4"/>
                <circle cx="50" cy="110" r="45" fill="#15803d"/>
                <circle cx="50" cy="70" r="38" fill="#16a34a"/>
                <circle cx="50" cy="35" r="28" fill="#48bb78"/>
            </svg>
            <svg class="tree" id="tree2" width="105" height="190" viewBox="0 0 100 200">
                <rect x="42" y="125" width="16" height="75" fill="#78350f" rx="4"/>
                <polygon points="50,15 15,90 85,90" fill="#22c55e"/>
                <polygon points="50,60 10,135 90,135" fill="#16a34a"/>
                <polygon points="50,105 5,175 95,175" fill="#15803d"/>
            </svg>
            <svg class="tree" id="tree3" width="75" height="140" viewBox="0 0 100 200">
                <rect x="42" y="130" width="16" height="70" fill="#854d0e" rx="4"/>
                <circle cx="50" cy="105" r="42" fill="#15803d"/>
                <circle cx="50" cy="65" r="34" fill="#22c55e"/>
                <circle cx="50" cy="35" r="24" fill="#86efac"/>
            </svg>
        </div>

        <!-- Nhà máy & Ống khói -->
        <div class="factory-group" id="factoryGroup">
            <svg width="220" height="140" viewBox="0 0 220 140">
                <rect x="20" y="55" width="110" height="85" fill="#334155" rx="3"/>
                <polygon points="20,55 50,30 50,55" fill="#475569"/>
                <polygon points="50,55 80,30 80,55" fill="#475569"/>
                <polygon points="80,55 110,30 110,55" fill="#475569"/>
                <!-- Ống khói -->
                <rect x="145" y="20" width="22" height="120" fill="#475569"/>
                <rect x="180" y="40" width="18" height="100" fill="#64748b"/>
                <!-- Cửa sổ sáng đèn -->
                <rect x="35" y="70" width="14" height="18" fill="#facc15" opacity="0.8"/>
                <rect x="60" y="70" width="14" height="18" fill="#facc15" opacity="0.8"/>
                <rect x="85" y="70" width="14" height="18" fill="#facc15" opacity="0.8"/>
            </svg>
            <div class="smoke-particle" id="smoke1" style="width:25px;height:25px;left:145px;top:5px;"></div>
            <div class="smoke-particle" id="smoke2" style="width:35px;height:35px;left:140px;top:-25px;"></div>
            <div class="smoke-particle" id="smoke3" style="width:45px;height:45px;left:135px;top:-60px;"></div>
        </div>

        <!-- Tia ma trận Tín chỉ Carbon -->
        <div class="carbon-matrix" id="carbonMatrix">
            <div class="energy-beam" style="width:80%;top:160px;left:10%;"></div>
            <div class="energy-beam" style="width:65%;top:200px;left:20%;"></div>
            <div class="energy-beam" style="width:85%;top:240px;left:5%;"></div>
        </div>

        <!-- Mặt đất -->
        <div class="ground" id="groundBar"></div>

        <!-- LOGO KẾT THÚC (2 Chiếc lá 45 độ + Trái Đất xanh + Slogan) -->
        <div class="finale-logo-container" id="finaleLogo">
            <div class="earth-sphere"></div>
            <div class="leaf-pair">
                <div class="leaf leaf-left"></div>
                <div class="leaf leaf-right"></div>
            </div>
            <div class="slogan-banner">MỘT CÚ CHẠM - VẠN ĐIỀU XANH</div>
            <div class="sub-slogan">Phát Triển Bền Vững &bull; Kết Nối Sinh Khối &bull; Net-Zero</div>
        </div>
    </div>

    <script>
        const cap = document.getElementById('captionText');
        const sky = document.getElementById('skyEffect');
        const forest = document.getElementById('forestGroup');
        const trees = [document.getElementById('tree1'), document.getElementById('tree2'), document.getElementById('tree3')];
        const factory = document.getElementById('factoryGroup');
        const smokes = [document.getElementById('smoke1'), document.getElementById('smoke2'), document.getElementById('smoke3')];
        const matrix = document.getElementById('carbonMatrix');
        const finale = document.getElementById('finaleLogo');
        const ground = document.getElementById('groundBar');

        function runStoryCycle() {
            // CẢNH 1 (0s): Rừng non vươn lên
            cap.innerText = "1. KHỞI NGUYÊN: Từ mầm xanh vươn mình thành những cánh rừng nguyên sinh trù phú...";
            cap.style.color = "#48bb78";
            sky.style.background = "rgba(30, 41, 59, 0)";
            forest.style.opacity = "1";
            factory.style.opacity = "0";
            matrix.style.opacity = "0";
            finale.style.opacity = "0";
            finale.style.transform = "translate(-50%, -50%) scale(0.6)";
            ground.style.borderTopColor = "#22c55e";

            trees.forEach((t, i) => {
                t.style.transform = "scale(0)";
                setTimeout(() => {
                    t.style.transform = "scale(1)";
                }, 200 + i * 300);
            });

            // CẢNH 2 (5s): Công nghiệp hóa & Khí thải
            setTimeout(() => {
                cap.innerText = "2. CÔNG NGHIỆP HÓA: Nhà máy mọc lên, phát thải khí thải gây ô nhiễm môi trường...";
                cap.style.color = "#f87171";
                sky.style.background = "rgba(40, 20, 20, 0.45)";
                ground.style.borderTopColor = "#64748b";

                // Thu nhỏ rừng
                trees.forEach(t => t.style.transform = "scale(0.3) translateY(40px)");
                // Hiện nhà máy
                factory.style.opacity = "1";
                smokes.forEach(s => s.style.opacity = "0.7");
            }, 5500);

            // CẢNH 3 (11s): Tín chỉ Carbon ra đời
            setTimeout(() => {
                cap.innerText = "3. TÍN CHỈ CARBON RA ĐỜI: Khuyến khích trồng lại rừng mà không kìm hãm công nghiệp!";
                cap.style.color = "#38bdf8";
                sky.style.background = "rgba(6, 78, 59, 0.25)";
                matrix.style.opacity = "1";

                // Rừng mọc lại song hành cùng nhà máy
                trees.forEach(t => t.style.transform = "scale(0.85)");
                factory.style.opacity = "0.75";
                ground.style.borderTopColor = "#38bdf8";
            }, 11500);

            // CẢNH 4 (17s - 24s): Sứ mệnh hòa hợp & Logo nền tảng
            setTimeout(() => {
                cap.innerText = "4. HÒA HỢP BỀN VỮNG: Con người & Thiên nhiên gắn kết qua nền tảng MRV Net-Zero!";
                cap.style.color = "#4ade80";
                sky.style.background = "rgba(11, 22, 34, 0.95)";
                
                // Hiện logo và slogan
                finale.style.opacity = "1";
                finale.style.transform = "translate(-50%, -50%) scale(1)";
            }, 17000);
        }

        // Chạy ngay và lặp lại mỗi 24 giây
        runStoryCycle();
        setInterval(runStoryCycle, 24000);
    </script>
    </body>
    </html>
    """

@st.dialog("HÀNH TRÌNH SỨ MỆNH & PHÁT TRIỂN BỀN VỮNG", width="large")
def hien_thi_hop_thoai_su_menh():
    html_code = get_mission_animation_html()
    components.html(html_code, height=500, scrolling=False)
