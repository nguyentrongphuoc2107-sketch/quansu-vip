import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- 1. CẤU HÌNH HỆ THỐNG (SYSTEM CONFIG) ---
st.set_page_config(page_title="V35 GOD MODE", layout="wide", initial_sidebar_state="collapsed")

# --- 2. GIAO DIỆN HACKER TỐI THƯỢNG (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ff00; }
    
    /* Style cho nút bấm nhập liệu */
    div.stButton > button {
        width: 100%; height: 60px; border-radius: 12px; font-weight: bold; font-size: 20px;
        transition: all 0.2s; border: 1px solid #333;
    }
    
    /* Phe XỈU (3-10): Màu Đỏ năng lượng */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        background: linear-gradient(180deg, #4a0000 0%, #200000 100%); color: #ff4d4d;
    }
    div[data-testid="column"]:nth-of-type(1) div.stButton > button:hover {
        border-color: #ff0000; box-shadow: 0 0 15px #ff0000;
    }

    /* Phe TÀI (11-18): Màu Xanh Neon */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        background: linear-gradient(180deg, #002d4a 0%, #001020 100%); color: #00e5ff;
    }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        border-color: #00e5ff; box-shadow: 0 0 15px #00e5ff;
    }

    /* Hộp thông báo kết quả */
    .result-box {
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
    }
    .metric-value { font-size: 28px; font-weight: bold; color: white; }
    .metric-label { font-size: 14px; color: #888; }
    
    /* Cảnh báo phiên */
    .alert-box {
        padding: 15px; background-color: #330000; border: 1px solid red; 
        color: red; text-align: center; border-radius: 10px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BỘ NÃO XỬ LÝ (CORE INTELLIGENCE) ---
class GodModeV35:
    def __init__(self, capital):
        # Khởi tạo kho dữ liệu nếu chưa có
        if 'history_scores' not in st.session_state: st.session_state.history_scores = []
        if 'history_outcomes' not in st.session_state: st.session_state.history_outcomes = []
        if 'markov_matrix' not in st.session_state: st.session_state.markov_matrix = {}
        self.capital = capital

    def update(self, score):
        outcome = 1 if score >= 11 else 0 # 1=Tài, 0=Xỉu
        st.session_state.history_scores.append(score)
        st.session_state.history_outcomes.append(outcome)
        
        # Học sâu (Deep Learning) từ quá khứ
        # Logic: Xem xét chuỗi 3 ván trước đó dẫn đến kết quả gì
        if len(st.session_state.history_outcomes) >= 5:
            prev_pattern = tuple(st.session_state.history_outcomes[-5:-2]) # Trạng thái cũ
            result_triggered = st.session_state.history_outcomes[-2]      # Kết quả đã ra
            
            if prev_pattern not in st.session_state.markov_matrix:
                st.session_state.markov_matrix[prev_pattern] = {0: 0, 1: 0}
            st.session_state.markov_matrix[prev_pattern][result_triggered] += 1

    def analyze(self):
        outcomes = st.session_state.history_outcomes
        scores = st.session_state.history_scores
        
        if len(outcomes) < 5: return None # Cần tối thiểu 5 ván để bot chạy ổn định

        # --- A. PHÂN TÍCH PATTERN (HÌNH THÁI) ---
        p_patt, patt_name = 0.5, "Không rõ"
        last_3 = outcomes[-3:]
        
        if sum(last_3) == 3: p_patt, patt_name = 0.8, "BỆT TÀI (Rồng bay)"
        elif sum(last_3) == 0: p_patt, patt_name = 0.2, "BỆT XỈU (Hổ xuống)"
        elif outcomes[-4:] == [1,0,1,0]: p_patt, patt_name = 0.6, "CẦU 1-1 (Về Tài)"
        elif outcomes[-4:] == [0,1,0,1]: p_patt, patt_name = 0.4, "CẦU 1-1 (Về Xỉu)"

        # --- B. PHÂN TÍCH MARKOV (LỊCH SỬ) ---
        p_mark = 0.5
        curr_state = tuple(outcomes[-3:])
        markov_txt = "Chưa đủ dữ liệu khớp lệnh"
        
        if curr_state in st.session_state.markov_matrix:
            data = st.session_state.markov_matrix[curr_state]
            total = data[0] + data[1]
            if total > 0:
                p_mark = data[1] / total
                markov_txt = f"Lịch sử thế bài này: {data[1]} Tài - {data[0]} Xỉu"

        # --- C. PHÂN TÍCH HỒI QUY (LỰC NẾN) ---
        p_reg = 0.5
        last_s = scores[-1]
        reg_txt = "Điểm số vùng an toàn"
        
        if last_s >= 16: # Vùng quá mua (Overbought)
            p_reg = 0.2 # Kéo mạnh về Xỉu
            reg_txt = f"Điểm {last_s} chạm đỉnh trần -> Dễ sập Xỉu"
        elif last_s <= 5: # Vùng quá bán (Oversold)
            p_reg = 0.8 # Kéo mạnh về Tài
            reg_txt = f"Điểm {last_s} chạm đáy sàn -> Dễ hồi Tài"

        # --- D. TỔNG HỢP (FUSION CORE) ---
        # Công thức V35: Markov(40%) + Pattern(30%) + Regression(30%)
        final_score = (p_mark * 0.4) + (p_patt * 0.3) + (p_reg * 0.3)
        
        direction = "TÀI" if final_score > 0.5 else "XỈU"
        confidence = final_score if final_score > 0.5 else (1 - final_score)
        
        # --- E. QUẢN LÝ VỐN KELLY ---
        odds = 0.95
        kelly = (confidence * odds - (1 - confidence)) / odds
        bet_pct = max(0, min(kelly * 0.5, 0.08)) # Max 8% vốn, đánh 1/2 Kelly
        money = self.capital * bet_pct
        
        # Tạo lý do hiển thị
        full_log = f"""
        - 🧠 **AI Markov:** {markov_txt} ({p_mark:.2f})
        - 🌊 **Hình thái:** {patt_name}
        - 📊 **Lực nến:** {reg_txt}
        """
        
        return direction, confidence*100, patt_name, int(money), full_log

# --- 4. GIAO DIỆN NGƯỜI DÙNG (UI) ---
st.title("👾 V35 GOD MODE - FINAL EDITION")

# Sidebar
with st.sidebar:
    st.header("⚙️ CONTROL")
    von = st.number_input("VỐN (VNĐ)", value=1000000, step=500000)
    
    c1, c2 = st.columns(2)
    if c1.button("↩️ HOÀN TÁC"):
        if 'history_scores' in st.session_state and len(st.session_state.history_scores) > 0:
            st.session_state.history_scores.pop()
            st.session_state.history_outcomes.pop()
            st.rerun()
            
    if c2.button("🔥 RESET"):
        st.session_state.clear()
        st.rerun()
    st.info("Nhập 5-10 ván mồi để kích hoạt AI.")

bot = GodModeV35(von)

# BÀN PHÍM NHẬP LIỆU (Chia 2 phe rõ ràng)
col_xiu, col_tai = st.columns(2)

with col_xiu:
    st.markdown("<h3 style='text-align:center; color:#ff4d4d; margin-bottom:10px;'>🔴 PHE XỈU (3-10)</h3>", unsafe_allow_html=True)
    c_x1, c_x2 = st.columns(2)
    for i in range(3, 7): 
        if c_x1.button(f"⚡ {i}"): bot.update(i); st.rerun()
    for i in range(7, 11): 
        if c_x2.button(f"⚡ {i}"): bot.update(i); st.rerun()

with col_tai:
    st.markdown("<h3 style='text-align:center; color:#00e5ff; margin-bottom:10px;'>🔵 PHE TÀI (11-18)</h3>", unsafe_allow_html=True)
    c_t1, c_t2 = st.columns(2)
    for i in range(11, 15): 
        if c_t1.button(f"💎 {i}"): bot.update(i); st.rerun()
    for i in range(15, 19): 
        if c_t2.button(f"💎 {i}"): bot.update(i); st.rerun()

# --- HIỂN THỊ KẾT QUẢ & CẢNH BÁO AN TOÀN ---
st.markdown("---")

# Lấy số lượng phiên hiện tại
session_count = len(st.session_state.history_scores)

if session_count >= 5:
    # --- TÍNH NĂNG MỚI: CẦU CHÌ AN TOÀN ---
    # Nếu quá 50 phiên, dừng toàn bộ hệ thống để ép Reset
    if session_count >= 50:
        st.markdown(f"""
        <div class="alert-box">
            <h1>⚠️ CẢNH BÁO: ĐÃ ĐẠT {session_count} PHIÊN!</h1>
            <h3>HỆ THỐNG TẠM KHÓA ĐỂ BẢO VỆ TÀI SẢN.</h3>
            <p>Nhà cái có thể đã thay đổi thuật toán (Reset Seed).</p>
            <p>Vui lòng bấm nút <b>'🔥 RESET'</b> bên trái để làm mới dữ liệu và tiếp tục chiến đấu!</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop() # Lệnh này chặn không cho code chạy tiếp phần dưới
    
    # Nếu chưa đến 50 phiên thì chạy bình thường
    res = bot.analyze()
    if res:
        direction, conf, patt, money, log = res
        
        # Màu chủ đạo
        main_color = "#00e5ff" if direction == "TÀI" else "#ff4d4d"
        shadow_color = "rgba(0, 229, 255, 0.3)" if direction == "TÀI" else "rgba(255, 77, 77, 0.3)"
        
        if conf < 60: 
            direction = "BỎ QUA"
            main_color = "#666"
            money = 0
            
        # 1. BIG BOX
        st.markdown(f"""
        <div class="result-box" style="border: 2px solid {main_color}; box-shadow: 0 0 30px {shadow_color};">
            <h4 style="color:#aaa; margin:0">KẾT LUẬN CỦA V35</h4>
            <h1 style="font-size: 70px; margin: 5px 0; color: {main_color}; text-shadow: 0 0 10px {main_color}; text-transform: uppercase;">{direction}</h1>
            <div style="display:flex; justify-content:center; gap:30px;">
                <span>🎯 Độ tin cậy: <b>{conf:.1f}%</b></span>
                <span>🌊 Hình thái: <b>{patt}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. METRICS
        m1, m2, m3 = st.columns(3)
        with m1: st.markdown(f"<div class='metric-value'>{money:,.0f} đ</div><div class='metric-label'>TIỀN VÀO</div>", unsafe_allow_html=True)
        with m2: 
            action = "CHỐT MẠNH" if conf > 80 else "THĂM DÒ" if conf > 60 else "QUAN SÁT"
            st.markdown(f"<div class='metric-value' style='color:{main_color}'>{action}</div><div class='metric-label'>CHIẾN THUẬT</div>", unsafe_allow_html=True)
        with m3: 
            # Hiển thị số phiên kèm màu cảnh báo nếu sắp đến giới hạn
            ss_color = "white" if session_count < 40 else "orange"
            st.markdown(f"<div class='metric-value' style='color:{ss_color}'>{session_count}/50</div><div class='metric-label'>GIỚI HẠN PHIÊN</div>", unsafe_allow_html=True)

        # 3. LÝ DO
        st.info(f"**🕵️ GIẢI MÃ THUẬT TOÁN:** {log}")

        # 4. CHART (BIỂU ĐỒ)
        fig = go.Figure()
        
        # Vẽ đường nối
        fig.add_trace(go.Scatter(y=st.session_state.history_scores, mode='lines', line=dict(color='#555', width=1)))
        
        # Vẽ điểm (Tài xanh, Xỉu đỏ)
        colors = ['#ff4d4d' if x <= 10 else '#00e5ff' for x in st.session_state.history_scores]
        fig.add_trace(go.Scatter(
            y=st.session_state.history_scores, 
            mode='markers+text',
            text=st.session_state.history_scores,
            textposition="top center",
            marker=dict(size=12, color=colors, line=dict(width=2, color='white'))
        ))
        
        # Vùng Danger Zone
        fig.add_hrect(y0=16, y1=18, fillcolor="red", opacity=0.1, line_width=0, annotation_text="VÙNG ĐỈNH (Đảo Xỉu)")
        fig.add_hrect(y0=3, y1=5, fillcolor="#00e5ff", opacity=0.1, line_width=0, annotation_text="VÙNG ĐÁY (Đảo Tài)")
        fig.add_hline(y=10.5, line_dash="dot", line_color="#333")

        fig.update_layout(
            template="plotly_dark", height=350, margin=dict(t=30, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[2, 19], showgrid=False), xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning(f"⚠️ Đang khởi động... Vui lòng nhập thêm {5 - len(st.session_state.history_scores)} phiên nữa để Bot bắt đầu phân tích.")
