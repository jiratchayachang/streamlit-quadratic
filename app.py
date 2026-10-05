import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configure Matplotlib default styles
plt.rcParams['axes.unicode_minus'] = False  # Display negative signs correctly

st.set_page_config(
    page_title="Quadratic Explorer - ระบบสำรวจฟังก์ชันกำลังสอง",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished layout and card aesthetics
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 12px 16px;
        border-left: 5px solid #2563EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .info-box {
        background-color: #EFF6FF;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #BFDBFE;
        color: #1E40AF;
    }
    </style>
""", unsafe_allow_html=True)


def calculate_quadratic_properties(a: float, b: float, c: float):
    """
    คำนวณคุณสมบัติหลักของฟังก์ชันกำลังสอง y = ax^2 + bx + c
    """
    # Vertex (h, k)
    h = -b / (2 * a)
    k = c - (b ** 2) / (4 * a)
    
    # Discriminant (Delta = b^2 - 4ac)
    delta = (b ** 2) - (4 * a * c)
    
    # Concavity / Direction
    concavity = "พาราโบลาหงาย (Concave Up)" if a > 0 else "พาราโบลาคว่ำ (Concave Down)"
    extremum_type = "จุดต่ำสุด (Minimum)" if a > 0 else "จุดสูงสุด (Maximum)"
    
    # Roots calculation
    if delta > 0:
        x1 = (-b + np.sqrt(delta)) / (2 * a)
        x2 = (-b - np.sqrt(delta)) / (2 * a)
        roots_type = "คำตอบเป็นจำนวนจริง 2 ค่าที่ต่างกัน"
        roots = (x1, x2)
    elif delta == 0:
        x1 = -b / (2 * a)
        roots_type = "คำตอบเป็นจำนวนจริง 1 ค่า (รากซ้ำ)"
        roots = (x1,)
    else:
        real_part = -b / (2 * a)
        imag_part = np.sqrt(-delta) / (2 * a)
        roots_type = "คำตอบเป็นจำนวนเชิงซ้อน (ไม่มีจุดตัดแกน X)"
        roots = (complex(real_part, imag_part), complex(real_part, -imag_part))
        
    return {
        "h": h,
        "k": k,
        "delta": delta,
        "concavity": concavity,
        "extremum_type": extremum_type,
        "roots_type": roots_type,
        "roots": roots,
        "y_intercept": (0, c)
    }


st.sidebar.header("⚙️ กำหนดค่าพารามิเตอร์ (Input)")

# Preset selector for quick learning scenarios
st.sidebar.subheader("🎯 เลือกตัวอย่างสมการ (Presets)")
preset = st.sidebar.selectbox(
    "เลือกรูปแบบมาตรฐาน:",
    [
        "กำหนดเอง (Custom)",
        "2 คำตอบจำนวนจริง (a=1, b=-4, c=3)",
        "1 คำตอบรากซ้ำ (a=1, b=-4, c=4)",
        "คำตอบจำนวนเชิงซ้อน (a=1, b=2, c=5)",
        "พาราโบลาคว่ำ / จุดสูงสุด (a=-2, b=4, c=1)"
    ]
)

# Initial coefficient default values
default_a, default_b, default_c = 1.0, -2.0, -3.0

if preset == "2 คำตอบจำนวนจริง (a=1, b=-4, c=3)":
    default_a, default_b, default_c = 1.0, -4.0, 3.0
elif preset == "1 คำตอบรากซ้ำ (a=1, b=-4, c=4)":
    default_a, default_b, default_c = 1.0, -4.0, 4.0
elif preset == "คำตอบจำนวนเชิงซ้อน (a=1, b=2, c=5)":
    default_a, default_b, default_c = 1.0, 2.0, 5.0
elif preset == "พาราโบลาคว่ำ / จุดสูงสุด (a=-2, b=4, c=1)":
    default_a, default_b, default_c = -2.0, 4.0, 1.0

st.sidebar.markdown("---")
st.sidebar.subheader("1️⃣ สัมประสิทธิ์ $y = ax^2 + bx + c$")

a = st.sidebar.slider("สัมประสิทธิ์ a (ความชันและทิศทาง)", -10.0, 10.0, default_a, 0.5)
b = st.sidebar.slider("สัมประสิทธิ์ b (ตำแหน่งแกน)", -10.0, 10.0, default_b, 0.5)
c = st.sidebar.slider("สัมประสิทธิ์ c (จุดตัดแกน Y)", -10.0, 10.0, default_c, 0.5)

st.sidebar.markdown("---")
st.sidebar.subheader("2️⃣ ขอบเขตแกน X และการแสดงผล")
x_min = st.sidebar.number_input("ค่า X ต่ำสุด (x_min)", value=-10.0, step=1.0)
x_max = st.sidebar.number_input("ค่า X สูงสุด (x_max)", value=10.0, step=1.0)
num_points = st.sidebar.slider("จำนวนจุดคำนวณ (Resolution)", 50, 500, 200)

show_vertex = st.sidebar.checkbox("แสดงจุดยอด (Vertex)", value=True)
show_roots = st.sidebar.checkbox("แสดงจุดตัดแกน X (X-Intercept)", value=True)
show_y_intercept = st.sidebar.checkbox("แสดงจุดตัดแกน Y (Y-Intercept)", value=True)
show_axis_sym = st.sidebar.checkbox("แสดงเส้นแกนสมมติ (Axis of Symmetry)", value=True)
show_tangent = st.sidebar.checkbox("แสดงเส้นสัมผัสกราฟ (Tangent Line)", value=False)

if show_tangent:
    x0_tangent = st.sidebar.slider("จุด x₀ สำหรับเส้นสัมผัส", float(x_min), float(x_max), 0.0, 0.5)

# Validation Step 1: Check a != 0
if a == 0:
    st.warning("⚠️ **ข้อแนะนำ:** เมื่อสัมประสิทธิ์ $a = 0$ สมการจะไม่ใช่ **ฟังก์ชันกำลังสอง (Quadratic Function)** แต่จะกลายเป็น **ฟังก์ชันเชิงเส้น (Linear Function)** $y = bx + c$")
    st.info("กรุณาปรับค่า $a \\neq 0$ ใน Sidebar เพื่อสำรวจรูปทรงกราฟพาราโบลา")
    
    # Display linear graph fallback
    x_linear = np.linspace(x_min, x_max, num_points)
    y_linear = b * x_linear + c
    
    fig_lin, ax_lin = plt.subplots(figsize=(8, 4))
    ax_lin.plot(x_linear, y_linear, color="#DC2626", linewidth=2, label=f"y = {b}x + {c}")
    ax_lin.axhline(0, color="black", linestyle="--", alpha=0.5)
    ax_lin.axvline(0, color="black", linestyle="--", alpha=0.5)
    ax_lin.set_xlabel("X")
    ax_lin.set_ylabel("Y")
    ax_lin.set_title("Linear Function (a = 0)")
    ax_lin.grid(True, alpha=0.3)
    ax_lin.legend()
    st.pyplot(fig_lin)
    plt.close(fig_lin)
    st.stop()

# Validation Step 2: Check x_min < x_max
if x_min >= x_max:
    st.error("❌ **ข้อผิดพลาด:** ค่า $x_{\\min}$ ต้องน้อยกว่า $x_{\\max}$ กรุณาปรับช่วงข้อมูลใน Sidebar")
    st.stop()


props = calculate_quadratic_properties(a, b, c)
h, k = props["h"], props["k"]
delta = props["delta"]

# Calculate grid array
x = np.linspace(x_min, x_max, num_points)
y = a * (x ** 2) + b * x + c


st.markdown('<div class="main-header">📐 Quadratic Explorer (ระบบสำรวจฟังก์ชันกำลังสอง)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">ทดลองปรับค่าสัมประสิทธิ์ a, b, c เพื่อเรียนรู้พฤติกรรม จุดยอด จุดตัดแกน และวิเคราะห์รากของสมการ</div>', unsafe_allow_html=True)

# Metrics Dashboard Display
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.metric(
        label="จุดยอด (Vertex / Extremum)",
        value=f"({h:.2f}, {k:.2f})",
        delta=props["extremum_type"]
    )

with col_m2:
    st.metric(
        label="ดิสครีมิแนนต์ (Discriminant Δ)",
        value=f"{delta:.2f}",
        delta="Δ > 0 (2 ราก)" if delta > 0 else ("Δ = 0 (1 ราก)" if delta == 0 else "Δ < 0 (เชิงซ้อน)"),
        delta_color="normal" if delta >= 0 else "inverse"
    )

with col_m3:
    st.metric(
        label="จุดตัดแกน Y",
        value=f"(0.00, {c:.2f})"
    )

with col_m4:
    st.metric(
        label="ลักษณะรูปทรงกราฟ",
        value="หงาย (a > 0)" if a > 0 else "คว่ำ (a < 0)"
    )


fig, ax = plt.subplots(figsize=(10, 5.5), dpi=120)

# Main Parabola Curve
ax.plot(x, y, color="#2563EB", linewidth=2.5, label=f"$y = {a:.1f}x^2 + ({b:.1f})x + ({c:.1f})$")

# Draw Cartesian Axes
ax.axhline(0, color="#374151", linestyle="-", linewidth=1.2, alpha=0.7)
ax.axvline(0, color="#374151", linestyle="-", linewidth=1.2, alpha=0.7)

# 1. Axis of Symmetry
if show_axis_sym:
    ax.axvline(h, color="#9333EA", linestyle="--", linewidth=1.5, label=f"Axis of Symmetry ($x = {h:.2f}$)")

# 2. Vertex Marker
if show_vertex:
    ax.scatter([h], [k], color="#DC2626", s=90, zorder=5, label=f"Vertex ({h:.2f}, {k:.2f})")
    ax.annotate(
        f"  Vertex ({h:.2f}, {k:.2f})",
        (h, k),
        textcoords="offset points",
        xytext=(0, 10 if a > 0 else -15),
        ha='center',
        fontweight='bold',
        color="#DC2626"
    )

# 3. Y-Intercept Marker
if show_y_intercept:
    ax.scatter([0], [c], color="#D97706", s=70, zorder=5, label=f"Y-Intercept (0, {c:.2f})")

# 4. Roots Markers (x-intercepts)
if show_roots and delta >= 0:
    for idx, r in enumerate(props["roots"]):
        if isinstance(r, (float, int, np.floating)):
            ax.scatter([r], [0], color="#059669", s=80, zorder=5, label=f"X-Intercept ({r:.2f}, 0)" if idx == 0 else "")
            ax.annotate(
                f"x = {r:.2f}",
                (r, 0),
                textcoords="offset points",
                xytext=(0, -15 if a > 0 else 10),
                ha='center',
                fontsize=9,
                color="#059669",
                fontweight='bold'
            )

# 5. Tangent Line Option
if show_tangent:
    y0 = a * (x0_tangent ** 2) + b * x0_tangent + c
    slope = 2 * a * x0_tangent + b
    y_tangent = slope * (x - x0_tangent) + y0
    ax.plot(x, y_tangent, color="#E11D48", linestyle="-.", linewidth=1.8, label=f"Tangent at x0={x0_tangent:.1f} (m={slope:.2f})")
    ax.scatter([x0_tangent], [y0], color="#E11D48", s=60, zorder=6)

# Formatting plot styling
ax.set_xlim([x_min, x_max])
# Adjust y limits dynamically with margins
y_margin = (max(y) - min(y)) * 0.15 if max(y) != min(y) else 5
ax.set_ylim([min(y) - y_margin, max(y) + y_margin])

ax.set_xlabel("X (Domain)", fontsize=10, fontweight='bold')
ax.set_ylabel("Y (Range)", fontsize=10, fontweight='bold')
ax.set_title(f"Parabola: $y = {a:.2f}x^2 + ({b:.2f})x + ({c:.2f})$", fontsize=12, fontweight='bold', pad=12)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", framealpha=0.9, fontsize=9)


st.pyplot(fig)
plt.close(fig)


tab_math, tab_calc, tab_data, tab_guide = st.tabs([
    "🧮 วิเคราะห์รูปแบบสมการ (Mathematical Forms)",
    "📐 แคลคูลัส & เส้นสัมผัส (Calculus & Tangent)",
    "📊 ตารางพิกัด & ดาวน์โหลด (Data & CSV)",
    "📖 คู่มือและการประยุกต์ใช้งาน (User Guide)"
])


with tab_math:
    st.subheader("📝 รูปแบบการแสดงสมการพาราโบลา")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown("##### 1. รูปแบบทั่วไป (Standard Form)")
        st.latex(rf"y = {a:.2f}x^2 + ({b:.2f})x + ({c:.2f})")
        
        st.markdown("##### 2. รูปแบบจุดยอด (Vertex Form)")
        h_str = f"- {abs(h):.2f}" if h >= 0 else f"+ {abs(h):.2f}"
        k_str = f"+ {k:.2f}" if k >= 0 else f"- {abs(k):.2f}"
        st.latex(rf"y = {a:.2f}(x {h_str})^2 {k_str}")
        
    with col_f2:
        st.markdown("##### 3. รูปแบบการแยกตัวประกอบ (Factored Form)")
        if delta > 0:
            r1, r2 = props["roots"]
            r1_str = f"- {r1:.2f}" if r1 >= 0 else f"+ {abs(r1):.2f}"
            r2_str = f"- {r2:.2f}" if r2 >= 0 else f"+ {abs(r2):.2f}"
            st.latex(rf"y = {a:.2f}(x {r1_str})(x {r2_str})")
        elif delta == 0:
            r1 = props["roots"][0]
            r1_str = f"- {r1:.2f}" if r1 >= 0 else f"+ {abs(r1):.2f}"
            st.latex(rf"y = {a:.2f}(x {r1_str})^2")
        else:
            st.info("ไม่สามารถแยกตัวประกอบในระบบจำนวนจริงได้ เนื่องจาก $\\Delta < 0$")

    st.markdown("---")
    st.subheader("🔍 การคำนวณหารากสมการ ($x$-intercepts)")
    st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
    st.latex(rf"x = \frac{{-({b:.2f}) \pm \sqrt{{({b:.2f})^2 - 4({a:.2f})({c:.2f})}}}}{{2({a:.2f})}}")
    st.latex(rf"x = \frac{{{ -b:.2f} \pm \sqrt{{{delta:.2f}}}}}{{{2*a:.2f}}}")

    if delta > 0:
        r1, r2 = props["roots"]
        st.success(f"✅ มีคำตอบเป็นจำนวนจริง 2 ค่า: **x₁ = {r1:.4f}** และ **x₂ = {r2:.4f}**")
    elif delta == 0:
        r1 = props["roots"][0]
        st.success(f"✅ มีคำตอบเป็นจำนวนจริง 1 ค่า (รากซ้ำ): **x = {r1:.4f}**")
    else:
        c1, c2 = props["roots"]
        st.warning(f"⚠️ คำตอบเป็นจำนวนเชิงซ้อน: **x = {c1.real:.4f} + {abs(c1.imag):.4f}i** และ **x = {c2.real:.4f} - {abs(c2.imag):.4f}i**")


with tab_calc:
    st.subheader("📈 การอนุพันธ์และอัตราการเปลี่ยนแปลง (Derivative Insight)")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("##### ฟังก์ชันอนุพันธ์อันดับ 1 (First Derivative)")
        st.latex(r"\frac{dy}{dx} = f'(x) = 2ax + b")
        st.latex(rf"f'(x) = {2*a:.2f}x + ({b:.2f})")
        
        st.markdown("##### หาจุดวิกฤต (Critical Point) เมื่อ $f'(x) = 0$")
        st.latex(rf"{2*a:.2f}x + ({b:.2f}) = 0 \implies x = \frac{{-({b:.2f})}}{{{2*a:.2f}}} = {h:.4f}")
        
    with col_c2:
        st.markdown("##### ฟังก์ชันอนุพันธ์อันดับ 2 (Second Derivative Test)")
        st.latex(r"\frac{d^2y}{dx^2} = f''(x) = 2a")
        st.latex(rf"f''(x) = {2*a:.2f}")
        
        if a > 0:
            st.success(f"เนื่องจาก $f''(x) = {2*a:.2f} > 0$ ดังนั้น จุดวิกฤตที่ $x = {h:.2f}$ ให้ **ค่าต่ำสุดสัมบูรณ์ (Global Minimum)** มีค่าเท่ากับ **y = {k:.4f}**")
        else:
            st.info(f"เนื่องจาก $f''(x) = {2*a:.2f} < 0$ ดังนั้น จุดวิกฤตที่ $x = {h:.2f}$ ให้ **ค่าสูงสุดสัมบูรณ์ (Global Maximum)** มีค่าเท่ากับ **y = {k:.4f}**")

    if show_tangent:
        st.markdown("---")
        st.markdown(f"##### 📍 สมการเส้นสัมผัส ณ จุด $x_0 = {x0_tangent:.2f}$")
        y0_val = a * (x0_tangent ** 2) + b * x0_tangent + c
        slope_val = 2 * a * x0_tangent + b
        intercept_val = y0_val - slope_val * x0_tangent
        
        st.latex(rf"y - y_0 = m(x - x_0)")
        st.latex(rf"y - ({y0_val:.2f}) = {slope_val:.2f}(x - {x0_tangent:.2f})")
        st.latex(rf"y = {slope_val:.2f}x + ({intercept_val:.2f})")


with tab_data:
    st.subheader("📊 ตารางแสดงค่าพิกัด $(x, y)$")
    
    df_points = pd.DataFrame({
        "x": x,
        "y": y,
        "f'(x) Slope": 2 * a * x + b
    })
    
    col_d1, col_d2 = st.columns([3, 1])
    
    with col_d1:
        st.dataframe(df_points.round(4), height=320, use_container_width=True)
        
    with col_d2:
        st.markdown("##### 📥 ดาวน์โหลดข้อมูล")
        st.write("นิสิตสามารถนำผลลัพธ์คำนวณพิกัด $(x,y)$ ไปใช้วิเคราะห์เพิ่มเติมใน Excel หรือ Colab ได้")
        
        csv_data = df_points.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 ดาวน์โหลด CSV",
            data=csv_data,
            file_name=f"quadratic_data_a{a}_b{b}_c{c}.csv",
            mime="text/csv",
            key="download-csv"
        )
        
        st.markdown("---")
        st.markdown("##### 📌 ข้อมูลสรุปเชิงสถิติ")
        st.write(f"- ค่า $y$ ต่ำสุดในช่วง: `{y.min():.2f}`")
        st.write(f"- ค่า $y$ สูงสุดในช่วง: `{y.max():.2f}`")


with tab_guide:
    st.subheader("📚 ความรู้พื้นฐานเกี่ยวกับฟังก์ชันกำลังสอง (Quadratic Functions)")
    
    st.markdown("""
    ฟังก์ชันกำลังสอง คือ ฟังก์ชันที่อยู่ในรูป $f(x) = ax^2 + bx + c$ โดยที่ $a, b, c$ เป็นจำนวนจริง และ $a \\neq 0$
    
    #### 1. ความหมายของสัมประสิทธิ์แต่ละตัว
    - **$a$ (Leading Coefficient):** ควบคุม **ความกว้างและความหงาย/คว่ำ** ของพาราโบลา
      - ถ้า $a > 0$: พาราโบลา **หงาย** (มีจุดต่ำสุด)
      - ถ้า $a < 0$: พาราโบลา **คว่ำ** (มีจุดสูงสุด)
      - ยิ่ง $|a|$ มีค่ามาก กราฟจะยิ่ง **แคบ/ชัน**
    - **$b$ (Linear Coefficient):** ควบคุมการเลื่อนขนานของแกนสมมติในแนวแกน $X$
      - แกนสมมติอยู่ที่เส้นตรง $x = -\\frac{b}{2a}$
    - **$c$ (Constant Term):** เป็นค่าพิกัด **จุดตัดแกน Y** ที่ตำแหน่ง $(0, c)$
    
    #### 2. ดิสครีมิแนนต์ ($\Delta = b^2 - 4ac$)
    - **$\Delta > 0$:** กราฟตัดแกน $X$ จำนวน **2 จุด**
    - **$\Delta = 0$:** กราฟสัมผัสแกน $X$ จำนวน **1 จุด** (จุดยอดแตะแกน X)
    - **$\Delta < 0$:** กราฟ **ไม่ตัดแกน X** ในระบบจำนวนจริง
    
    #### 3. ตัวอย่างการนำไปประยุกต์ใช้งานจริง (Real-world Applications)
    - **ฟิสิกส์ (Projectile Motion):** การเคลื่อนที่แบบโปรเจกไทล์ เช่น การโยนลูกบอล
    """)
    st.latex(r"h(t) = -\frac{1}{2}gt^2 + v_0 t + h_0")
    st.markdown("""
    - **วิศวรรกม (Structural Design):** การออกแบบสะพานแขวน จานดาวเทียม และไฟหน้ารถยนต์
    - **เศรษฐศาสตร์ (Business Optimization):** การหาจุดกำไรสูงสุด (Maximum Profit) หรือต้นทุนต่ำสุด (Minimum Cost)
    """)
