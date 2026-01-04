import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="V35 - THE ARCHITECT PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CSS CUSTOM ĐỂ GIAO DIỆN ĐẸP NHƯ APP ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #262730;
        color: white;
        border: 1px solid #4x4x4x;
    }
    .stButton>button:hover { border: 1px solid #00FBFF; color: #00FBFF; }
    .status-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #333;
    }
    h1, h2, h3 { text-align: center; color: #00FBFF; }
    </style>
    """, unsafe_allow_html=True)

# --- CLASS THUẬT TOÁN CỦA ÔNG (ĐÃ TỐI ƯU CHO WEB) ---
class ArchitectV35Web:
    def __init__(self, initial_capital):
        if 'history_scores' not in st.session_state:
            st.session_state.history_scores = []
        if 'history_outcomes' not in st.session_state:
            st.session_state.history_outcomes = []
        if 'markov_matrix' not in st.session_state:
            st.session_state.markov_matrix = {}
        self.capital = initial_capital

    def update_data(self, score):
        outcome = 1 if score >= 11 else 0
        st.session_state.history_scores.append(score)
        st.session_state.history_outcomes.append(outcome)
        
        # Cập nhật Markov
        if len(st.session_state.history_outcomes) >= 4:
            prev_state = tuple(st.session_state.history_outcomes[-4:-1])
            actual_result = st.session_state.history_outcomes[-1]
            if prev_state not in st.session_state.markov_matrix:
                st.session_state.markov_matrix[prev_state] = {0: 0, 1: 0}
            st.session_state.markov_matrix[prev_state][actual_result] += 1

    def analyze_all(self):
        scores = st.session_state.history_scores
        outcomes = st.session_state.history_outcomes
        
        if len(outcomes) < 3: return None
        
        # 1. Pattern
        p_pattern, pattern_name = 0.5, "Đang quét..."
        last_3 = outcomes[-3:]
        if sum(last_3) == 3: p_pattern, pattern_name = 0.7, "BỆT TÀI 🔥"
        elif sum(last_3) == 0: p_pattern, pattern_name = 0.3, "BỆT XỈU 🔥"
        elif outcomes[-2:] == [1, 0] or outcomes[-2:] == [0, 1]: p_pattern, pattern_name = 0.5, "CẦU NHẢY 🌊"

        # 2. Markov
        p_markov = 0.5
        current_state = tuple(outcomes[-3:])
        if current_state in st.session_state.markov_matrix:
            stats = st.session_state.history_outcomes # Sửa nhẹ logic lấy stats
            s = st.session_state.markov_matrix[current_state]
            total = s[0] + s[1]
            if total > 0: p_markov = s[1] / total

        # 3. Regression
        p_regress = 0.5
        if scores[-1] >= 16: p_regress = 0.2
        elif scores[-1] <= 5: p_regress = 0.8

        # Fusion
        final_prob = (p_pattern * 0.3) + (p_markov * 0.4) + (p_regress * 0.3)
        direction = "TÀI" if final_prob > 0.5 else "XỈU"
        conf = final_prob if final_prob > 0.5 else (1 - final_prob)
        
        # Kelly
        b = 0.95
        f_star = (b * conf - (1 - conf)) / b
        bet_amt = self.capital * max(min(f_star * 0.5, 0.05), 0)
        
        return direction, conf * 100, pattern_name, int(bet_amt), f"M:{p_markov:.2f}|P:{p_pattern:.2f}|R:{p_regress:.2f}"

# --- GIAO DIỆN TRANG CHỦ ---
st.write(f"### 🏛️ THE ARCHITECT V35 PRO")
st.write(f"<p style='text-align:center; color:grey;'>{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)

# Quản lý vốn ở Sidebar
with st.sidebar:
    st.header("💰 TÀI CHÍNH")
    user_capital = st.number_input("Vốn hiện tại (VNĐ):", value=1000000, step=100000)
    if st.button("XÓA DỮ LIỆU CẦU"):
        st.session_state.history_scores = []
        st.session_state.history_outcomes = []
        st.session_state.markov_matrix = {}
        st.rerun()

bot = ArchitectV35Web(user_capital)

# --- KHU VỰC NHẬP LIỆU (NÚT BẤM TO) ---
st.write("---")
cols = st.columns(8)
for i in range(3, 11):
    if cols[i-3].button(str(i), key=f"btn_{i}"):
        bot.update_data(i)
        st.rerun()
cols2 = st.columns(8)
for i in range(11, 19):
    if cols2[i-11].button(str(i), key=f"btn_{i}"):
        bot.update_data(i)
        st.rerun()

# --- KHU VỰC HIỂN THỊ KẾT QUẢ ---
if len(st.session_state.history_scores) > 0:
    res = bot.analyze_all()
    if res:
        direction, confidence, pattern, bet_amt, reason = res
        
        # Hộp màu báo hiệu
        color = "#ff4b4b" if direction == "XỈU" else "#00f2ff"
        if confidence < 60: color = "#444" # Cầu loạn màu xám

        st.markdown(f"""
            <div class="status-box" style="background-color: {color}22; border: 2px solid {color}">
                <h1 style="color: {color}; margin:0">{direction}</h1>
                <h3 style="color: white; margin:0">{confidence:.1f}% TIN CẬY</h3>
                <p style="margin:5px 0 0 0">Hình thái: <b>{pattern}</b></p>
            </div>
        """, unsafe_allow_html=True)

        # Thông tin cược
        c1, c2 = st.columns(2)
        with c1:
            st.metric("TIỀN VÀO", f"{bet_amt:,.0f} đ")
        with c2:
            status = "🔥 CHỐT MẠNH" if confidence > 80 else "⚠️ THĂM DÒ" if confidence > 65 else "🛑 BỎ QUA"
            st.metric("CHIẾN THUẬT", status)

        # Biểu đồ nhịp cầu Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=st.session_state.history_scores, 
            mode='lines+markers+text',
            text=st.session_state.history_scores,
            textposition="top center",
            line=dict(color='#00FBFF', width=2)
        ))
        fig.update_layout(
            template="plotly_dark", height=300, 
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption(f"Log phân tích: {reason}")
    else:
        st.info("Nhập thêm ít nhất 3 phiên để bắt đầu phân tích...")
else:
    st.warning("Vui lòng nhập dữ liệu phiên gần nhất từ bàn cược.")
