import streamlit as st
import plotly.graph_objects as go

# 1. CẤU HÌNH HỆ THỐNG VIP
st.set_page_config(page_title="V31 - ULTIMATE FUSION VIP", layout="wide")

if 'data' not in st.session_state:
    st.session_state.data = []

# --- BỘ NÃO TỔNG HỢP THUẬT TOÁN (FUSION ENGINE) ---
def fusion_analytics(data):
    if len(data) < 6:
        return "THĂM DÒ", 0, ["Hệ thống cần tối thiểu 6 phiên để nạp Ma Trận Đa Tầng."], "N/A"
    
    tongs = [d['t'] for d in data]
    x1, x2, x3 = [d['x1'] for d in data], [d['x2'] for d in data], [d['x3'] for d in data]
    chuoi = ["T" if x > 10 else "X" for x in tongs]
    
    score_T, score_X = 0, 0
    ly_do = []
    loai_cau = "Cầu Linh Hoạt"

    # THUẬT TOÁN 1: MA TRẬN MARKOV (SOI MẪU CHUỖI)
    pattern = "".join(chuoi[-3:])
    vung_dem = "".join(chuoi[:-1])
    t_count = vung_dem.count(pattern + "T")
    x_count = vung_dem.count(pattern + "X")
    if t_count > x_count: score_T += 35; ly_do.append(f"🧬 Markov: Mẫu {pattern} nghiêng Tài ({t_count} lần)")
    elif x_count > t_count: score_X += 35; ly_do.append(f"🧬 Markov: Mẫu {pattern} nghiêng Xỉu ({x_count} lần)")

    # THUẬT TOÁN 2: NHẬN DIỆN CẤU TRÚC (BỆT / 1-1 / 2-2)
    gan_nhat = chuoi[-4:]
    if all(x == "T" for x in chuoi[-3:]): 
        score_T += 45; loai_cau = "🔥 BỆT TÀI"; ly_do.append("Nhịp bệt đang chạy, ưu tiên thuận thiên.")
    elif all(x == "X" for x in chuoi[-3:]): 
        score_X += 45; loai_cau = "🔥 BỆT XỈU"; ly_do.append("Nhịp bệt đang chạy, ưu tiên thuận thiên.")
    elif gan_nhat in [['T','X','T','X'], ['X','T','X','T']]:
        loai_cau = "🌊 CẦU ĐẢO 1-1"; ly_do.append("Cầu 1-1 cực nét, đánh đối xứng phiên trước.")
        if chuoi[-1] == "T": score_X += 50
        else: score_T += 50

    # THUẬT TOÁN 3: ĐIỂM RƠI HỒI QUY (VẬT LÝ XÍ NGẦU)
    cuoi = tongs[-1]
    if cuoi >= 15: score_X += 55; ly_do.append("💎 Điểm rơi: Chạm đỉnh ma trận, xác suất hồi Xỉu 95%")
    elif cuoi <= 6: score_T += 55; ly_do.append("💎 Điểm rơi: Chạm đáy ma trận, xác suất bật Tài 95%")

    # TỔNG HỢP KẾT QUẢ
    du_doan = "TÀI" if score_T > score_X else "XỈU"
    tin_cay = min(max(score_T, score_X) + 5, 99)
    
    # CẢNH BÁO SOI (NẾU XUNG ĐỘT THÌ BỎ QUA)
    if abs(score_T - score_X) < 15:
        return "BỎ QUA", 40, ["Dữ liệu xung đột - Nhà cái có thể đang đổi thuật toán."], "Cầu Nhiễu"

    return du_doan, tin_cay, ly_do, loai_cau

# --- GIAO DIỆN HIỂN THỊ ---
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🛡️ ULTIMATE FUSION V31</h1>", unsafe_allow_html=True)

col_in, col_viz = st.columns([1, 2])

with col_in:
    st.subheader("📥 NHẬP XÍ NGẦU")
    v1 = st.radio("XN 1", [1,2,3,4,5,6], horizontal=True, key="xn1")
    v2 = st.radio("XN 2", [1,2,3,4,5,6], horizontal=True, key="xn2")
    v3 = st.radio("XN 3", [1,2,3,4,5,6], horizontal=True, key="xn3")
    
    if st.button("🚀 CHỐT PHIÊN", use_container_width=True):
        st.session_state.data.append({'t': v1+v2+v3, 'x1': v1, 'x2': v2, 'x3': v3})
        st.rerun()
    
    if st.button("🔄 LÀM MỚI"):
        st.session_state.data = []
        st.rerun()

with col_viz:
    if st.session_state.data:
        t_list = [d['t'] for d in st.session_state.data]
        fig = go.Figure(go.Scatter(y=t_list, mode='lines+markers+text', text=t_list, 
                                   line=dict(color='gold', width=4),
                                   marker=dict(size=12, color='white', line=dict(width=2, color='black'))))
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

st.divider()

if st.session_state.data:
    keo, cf, ld, nhip = fusion_analytics(st.session_state.data)
    c1, c2, c3 = st.columns(3)
    c1.metric("KÈO CHỐT", keo)
    c2.metric("ĐỘ TIN CẬY", f"{cf}%")
    c3.metric("NHẬN DIỆN CẦU", nhip)
    with st.expander("📝 LẬP LUẬN TỔNG HỢP", expanded=True):
        for line in ld: st.write(f"🔹 {line}")