import streamlit as st
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error, r2_score
from fpdf import FPDF
from datetime import datetime
import tempfile
import itertools
import os
import pandas as pd
import itertools

font_path = os.path.join(os.path.dirname(__file__), "font/NanumGothic.ttf")
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()
matplotlib.rcParams['font.family'] = font_name
matplotlib.rcParams['axes.unicode_minus'] = False

def poly_equation_to_latex(model, poly):
    terms = poly.get_feature_names_out(['x'])
    coefs = model.coef_
    intercept = model.intercept_
    eq_terms = []
    for t, c in zip(terms, coefs):
        if abs(c) < 1e-8:  
            continue
        if t == "x":
            term = f"{c:.2f}x"
        elif "^" in t:
            deg = t.split("^")[1]
            term = f"{c:.2f}x^{{{deg}}}"   
        else:
            term = f"{c:.2f}{t}"
        eq_terms.append(term)

    if abs(intercept) > 1e-8:
        eq_terms.append(f"{intercept:.2f}")

    equation = " + ".join(eq_terms)
    equation = equation.replace("+ -", "- ")
    return f"y = {equation}"

class ThemedPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=15)
        self._font_family = "Nanum"
        self.footer_left = ""  
        self.c_primary = (25, 118, 210) 
        self.c_primary_lt = (227, 242, 253)
        self.c_border = (200, 200, 200)
        self.c_text_muted = (120, 120, 120)

    def header(self):
        self.set_fill_color(*self.c_primary)
        self.rect(0, 0, self.w, 22, 'F')
        self.set_xy(10, 6)
        self.set_text_color(255, 255, 255)
        self.set_font(self._font_family, '', 20)
        self.cell(0, 10, "인공지능 수열 예측 보고서", ln=1, align='C')
        self.set_text_color(33, 33, 33)
        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(*self.c_border)
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.set_y(-12)
        self.set_font(self._font_family, '', 9)
        self.set_text_color(*self.c_text_muted)
        if self.footer_left:
            self.cell(0, 8, self.footer_left, 0, 0, 'L')
        self.cell(0, 8, f"{self.page_no()} / {{nb}}", 0, 0, 'R')

    def h2(self, text):
        self.set_fill_color(*self.c_primary_lt)
        self.set_text_color(21, 101, 192)
        self.set_font(self._font_family, '', 12)
        self.cell(0, 9, text, ln=1, fill=True)
        self.ln(2)
        self.set_text_color(33, 33, 33)

    def p(self, text, size=11, lh=6):
        self.set_font(self._font_family, '', size)
        self.multi_cell(0, lh, text)
        self.ln(1)

def create_pdf(student_info, analysis, latex_equation_ml, pred_ml_next, 
               x, y, y_pred, next_input, fig=None):
    pdf = ThemedPDF()
    pdf.add_font('Nanum', '', font_path, uni=True)
    pdf.set_font('Nanum', '', 12)
    pdf._font_family = "Nanum"
    pdf.footer_left = f"{student_info.get('school','')} • {student_info.get('name','')}"
    pdf.add_page()
    pdf.h2("👤 학생 정보")
    pdf.p(f"학교: {student_info.get('school','')}")
    pdf.p(f"학번: {student_info.get('id','')}")
    pdf.p(f"이름: {student_info.get('name','')}")
    pdf.p(f"작성일: {datetime.now().strftime('%Y-%m-%d')}")
    pdf.h2("🧮 모델 함수식")
    pdf.p(latex_equation_ml)
    pdf.h2("🔮 예측값")
    pdf.p(f"X={next_input:.2f} → 예측 Y = {pred_ml_next:.2f}")
    if fig is not None:
        pdf.h2("📈 시각화")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name, format="png", bbox_inches="tight", dpi=200)
            pdf.image(tmpfile.name, x=10, w=pdf.w-20)
    pdf.add_page()
    pdf.h2("📝 데이터 분석 및 예측 결과 (학생 작성)")
    pdf.p(analysis if analysis else "작성된 분석 없음")
    return bytes(pdf.output(dest='S'))

def parse_sequence(seq_text: str):
    try:
        y = np.array([float(s.strip()) for s in seq_text.split(",") if s.strip()!=""], dtype=float)
        if y.size < 3:
            return None, "데이터가 너무 적습니다. 최소 3개 이상 입력해 주세요."
        x = np.arange(1, len(y)+1, dtype=float).reshape(-1, 1)
        return (x, y), None
    except Exception:
        return None, "숫자만 쉼표로 구분해 입력해 주세요."

def fit_poly(x, y, degree):
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    Xp = poly.fit_transform(x)
    model = LinearRegression().fit(Xp, y)
    y_hat = model.predict(Xp)
    return model, poly, y_hat

def run_deep_learning(x, y, hidden1, hidden2, epochs):
    model = Sequential([
        Dense(hidden1, input_shape=(x.shape[1],), activation='tanh'),
        Dense(hidden2, activation='tanh'),
        Dense(1)
    ])
    model.compile(optimizer=Adam(0.01), loss='mse')
    model.fit(x, y, epochs=epochs, verbose=0, batch_size=len(x))
    y_pred = model.predict(x).flatten()
    latex = f"Deep Learning (1-{hidden1}-{hidden2}-1)"
    return model, y_pred, latex

def plot_with_residual_lines(x, y, y_hat, title="데이터 & 추세선 및 편차", key_prefix="plot"):
    col1, col2, col3 = st.columns(3)
    with col1:
        show_data = st.checkbox("실제값", value=True, key=f"{key_prefix}_data")
    with col2:
        show_fit = st.checkbox("추세선", value=True, key=f"{key_prefix}_fit")
    with col3:
        show_residuals = st.checkbox("편차", value=True, key=f"{key_prefix}_res")
    fig, ax = plt.subplots()
    order = np.argsort(x[:,0])
    colors = itertools.cycle(["#FF5733"])
    if show_data:
        ax.scatter(x[:,0], y, s=45, color="#1976D2", label="실제값", zorder=3)
    if show_fit:
        ax.plot(x[order,0], y_hat[order], linewidth=2, color="#FFC300", label="추세선", zorder=2)
    if show_residuals:
        for xi, yi, ypi in zip(x[:,0], y, y_hat):
            ax.plot([xi, xi], [yi, ypi], "--", color=next(colors), linewidth=1, label="편차" if xi==x[0,0] else "", zorder=1)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel("항 번호 (x)")
    ax.set_ylabel("값 (y)")
    ax.grid(alpha=0.25)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), prop=fm.FontProperties(fname=font_path, size=10))
    st.pyplot(fig)

def practice_widget(default_seq: str, tip: str = "", key_prefix: str = "d6"):
    st.divider()
    st.markdown("""
    <div style="
        background-color: #f0f7ff;
        border-left: 6px solid #1976d2;
        padding: 12px;
        margin-top: 15px;
        border-radius: 8px;
        font-size: 22px;
        font-weight: bold;
        color: #0d47a1;
        ">
        💡 생각 공작소
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        seq = st.text_input(
            "수열 입력 (쉼표로 구분)", 
            value=default_seq, 
            key=f"{key_prefix}_seq"
        )
    with col2:
        degree = st.segmented_control(
            "다항 회귀 차수 선택",
            options=[1, 2, 3, 4],
            default=1,
            key=f"{key_prefix}_deg"
        )
    parsed, err = parse_sequence(seq)
    if err:
        st.warning(err)
        return None, None, None, None   
    x, y = parsed
    model, poly, y_hat = fit_poly(x, y, degree)
    latex_eq = poly_equation_to_latex(model, poly)
    col1, col2 = st.columns([3, 5])  
    with col1:
        st.markdown("""
        <div style="
            background-color: #f5f5f5; 
            border-left: 6px solid #9e9e9e;
            padding: 10px; 
            margin-top: 10px; 
            border-radius: 6px;
            font-weight: bold;
            font-size: 16px;
            color: #424242;
            text-align: center;
            ">
            📐 회귀식
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.latex(latex_eq)
    plot_with_residual_lines(x, y, y_hat, title=f"다항 회귀 ({degree}차)와 편차 표시", key_prefix=key_prefix)
    return x, y, y_hat, degree   

# ✅ 메인 화면
def show():
    st.header("🗓️ Day 6")
    st.subheader("인공지능의 이해")
    st.write("AI는 어떻게 생각하는지 알아 봅시다.")
    st.divider()
    st.video("https://youtu.be/G8GOswA8ntA")
    st.subheader("📌 학습 목표")
    st.write("""
    - 수학적 사고와 인공지능적 사고의 차이를 설명할 수 있다.
    - 회귀와 딥러닝의 기본 원리 및 학습 과정을 이해할 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    tabs = st.tabs([
        "1️⃣ 수학적 사고 vs AI 사고",
        "2️⃣ 회귀와 함수의 원리",
        "3️⃣ 반복 학습과 오차",
        "4️⃣ 딥러닝 구조와 학습",
        "5️⃣ AI로 수열 예측",
    ])

    with tabs[0]:
        st.markdown("""
            수학자는 문제를 보고 스스로 규칙을 찾아내고, 이를 식으로 표현합니다.  
            예를 들어 `2, 4, 6, ...`이라는 수열을 보면 “`2`씩 증가하는 규칙이네”라고 판단하고 $a_n = 2n$이라는 식을 세웁니다. 이는 인간의 직관과 논리를 활용한 방식이죠.
            하지만 인공지능(AI)은 사람처럼 사고하지 않고, 많은 숫자 데이터를 관찰하여 그 안에 숨어 있는 규칙을 자동으로 찾아냅니다. 예를 들어 아래와 같은 데이터를 보고:
                """)
        st.markdown("""
            - `x` (항 번호): `1` → `y` (수열 값): `2`  
            - `x` (항 번호): `2` → `y` (수열 값): `4`  
            - `x` (항 번호): `3` → `y` (수열 값): `6`
            - `x` (항 번호): `4` → `y` (수열 값): `8`  
                """)
        st.markdown("""
            AI는 “`x`가 `1`씩 증가할 때 `y`는 `2`씩 증가하네 → $y = 2x$”라는 규칙을 스스로 찾아냅니다.
        """)
        st.success("""
        ##### 👉 [두 줄 정리]
        - **수학자**: 규칙을 직접 생각  
        - **AI**: 데이터를 보고 학습
        """)
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("""
        - AI는 숫자들 사이의 관계를 수학적으로 표현하는 법을 학습합니다.  
        가장 기본적인 방식이 **회귀**(regression)입니다. 회귀는 입력값 $x$와 출력값 $y$ 사이의 관계를 함수 형태로 표현하는 것이며, 대표적으로 **선형 회귀**(linear regression)가 있습니다.
        """)
        col1, col2 = st.columns([1, 1])  
        with col1:
            st.image("image/1dim.png",
                    caption="선형회귀",
                    width=300)  
        with col2:
            st.latex(r"y = ax + b")
            st.markdown("""예를 들어, 아래와 같은 데이터를 AI가 관찰했다면: `x: 1 → y: 3 , x: 2 → y: 5 , x: 3 → y: 7` 
            이 데이터를 통해 AI는 수식을 $y = 2x + 1$로 학습할 수 있습니다.  이처럼 선형 회귀는 **직선으로 표현 가능한 관계**를 찾아내는 방법입니다.""")
        col1, col2 = st.columns([1, 1])  
        with col1:
            st.image("image/2dim.png",
                    caption="다항회귀",
                    width=300)  
        with col2:
            st.markdown("""
            하지만 어떤 데이터는 **직선이 아니라 곡선**으로 표현됩니다. 예를 들어: ` x: 1 → y: 1, x: 2 → y: 4, x: 3 → y: 9` 이 관계는 $y = x^2$이라는 **2차 함수**로 설명할 수 있고, 이는 **다항 회귀**(polynomial regression)를 통해 학습됩니다.
            """)
            st.latex(r"y = ax^2 + bx + c")
        st.markdown("""
        - 여기서 **차수**(degree)는 함수의 최고 차항을 의미하며, 차수가 높아질수록 더 복잡한 패턴도 설명할 수 있습니다.
        """)
        st.success(""" 
        ##### 👉 [두 줄 정리]
        - **선형 회귀**는 입력과 출력 사이의 직선 규칙을 찾는 방법
        - **다항 회귀**는 데이터의 곡선 패턴까지 학습할 수 있음
        """)
        practice_widget("2,4,8,16,32,64", tip="선형 vs 다항", key_prefix="tab2")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("""
        AI는 수식을 스스로 만들기 위해 수많은 수식 조합을 시도해봅니다. 예를 들어 아래와 같은 형태의 수식을 가정합니다
        """)
        col1, col2 = st.columns([1, 1])  
        with col1:
            st.image("image/sleep.png",
                    caption="AI가 수식을 찾는 과정",
                    width=300) 
        with col2:
            st.latex(r"y = w_1x + w_0")        
            st.markdown("""
            이때 $w_1$과 $w_0$는 AI가 학습을 통해 찾아내는 **계수**(weight)입니다. 
            AI는 다양한 값을 시도해보며, **예측값과 실제값의 차이**를 줄이려고 합니다.
            이 오차를 계산하는 방법 중 하나가 **오차제곱합 **(SSE: Mean Squared Error)입니다:
            """)
        st.latex(r"\text{SSE} = \sum_{i=1}^{n}(y_i - \hat{y}_i)^2")
        st.markdown("""
        - $y_i$: 실제값 , $\hat{y}_i$: 예측값  

        AI는 이 오차를 **가장 작게** 만드는 방향으로 수식의 계수를 계속 수정합니다. 
        이 과정을 **반복 학습**(iterative learning)이라고 하며, 
        사람이 수식을 직접 세우는 것과 달리 AI는 ‘**시도와 오차 줄이기**’를 통해 최적의 수식을 찾아냅니다.
        """)
        st.success(""" 
        ##### 👉 [두 줄 정리]
        - AI는 **예측값**과 **실제값**의 차이(오차)를 계산해서 
        오차가 **작아**지도록 수식의 **계수**를 반복해서 **수정**하며 **학습**합니다.                 
        """)
        st.markdown("""
        <div style="
            background-color: #f0f7ff;
            border-left: 6px solid #1976d2;
            padding: 12px;
            margin-top: 15px;
            border-radius: 8px;
            font-size: 22px;
            font-weight: bold;
            color: #0d47a1;
            ">
            💡 생각 공작소
        </div>
        """, unsafe_allow_html=True)
        seq_text = st.text_input("수열 입력 (쉼표로 구분)", value="2,4,8,16,32,64", key="tab3_seq")
        parsed, err = parse_sequence(seq_text)
        if err:
            st.warning(err)
        else:
            x, y = parsed
            col1, col2 = st.columns([1, 1])
            with col1:
                degree = st.slider("다항 회귀 차수 선택", 1, 4, 2, key="tab3_degree")
            with col2:
                epochs = st.selectbox("학습 횟수 (Epochs)", [20, 40, 60], index=1, key="tab3_epochs")
            poly = PolynomialFeatures(degree=degree, include_bias=False)
            X_poly = poly.fit_transform(x)
            model = LinearRegression().fit(X_poly, y)
            progress = epochs / 60  
            approx_coefs = model.coef_ * progress
            approx_intercept = model.intercept_ * progress
            y_hat = X_poly.dot(approx_coefs) + approx_intercept
            full_eq = poly_equation_to_latex(model, poly)
            eq_terms = []
            terms = poly.get_feature_names_out(['x'])
            term_list = []
            for t, c in zip(terms, approx_coefs):
                if abs(c) < 1e-8:
                    continue
                if t == "x":
                    degree_val = 1
                    term = (degree_val, f"{c:.2f}x")
                elif "^" in t:
                    degree_val = int(t.split("^")[1])
                    term = (degree_val, f"{c:.2f}x^{{{degree_val}}}")
                else:
                    degree_val = 0
                    term = (degree_val, f"{c:.2f}{t}")
                term_list.append(term)
            if abs(approx_intercept) > 1e-8:
                term_list.append((0, f"{approx_intercept:.2f}"))
            term_list.sort(key=lambda x: x[0], reverse=True)
            eq_terms = [t[1] for t in term_list]
            approx_eq = " + ".join(eq_terms).replace("+ -", "- ")
            latex_eq = f"y = {approx_eq}"
            col1, col2 = st.columns([3, 5])
            with col1:
                st.markdown("""
                <div style="
                    background-color: #f5f5f5; 
                    border-left: 6px solid #9e9e9e;
                    padding: 10px; 
                    margin-top: 10px; 
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 16px;
                    color: #424242;
                    text-align: center;
                    ">
                    📐 회귀식
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.latex(latex_eq)
            fig, ax = plt.subplots()
            ax.scatter(x, y, color="#1976D2", s=45, label="실제값")
            ax.plot(x, y_hat, color="#FF9800", linewidth=2, label=f"추세선 (Epoch {epochs})")
            for xi, yi, ypi in zip(x.flatten(), y, y_hat):
                ax.plot([xi, xi], [yi, ypi], "--", color="red", linewidth=1, alpha=0.7,
                        label="편차" if xi==x[0,0] else "")
            ax.set_title(f"다항 회귀 (차수={degree}, Epoch={epochs})", fontsize=13, fontweight="bold")
            ax.set_xlabel("항 번호 (x)")
            ax.set_ylabel("값 (y)")
            ax.legend()
            st.pyplot(fig)
            sse = np.sum((y - y_hat) ** 2)
            acc = r2_score(y, y_hat) * 100
            errors_df = pd.DataFrame({
                "실제값": y,
                "예측값": y_hat,
            })
            errors_df["오차"] = (errors_df["실제값"] - errors_df["예측값"]).abs()
            st.markdown("##### 📉 실제값과 예측값 오차 비교")
            st.dataframe(
                errors_df.style.format(precision=2).background_gradient(
                    cmap='Reds', subset=["오차"]
                ),
                use_container_width=True, height=250, hide_index=True
            )
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🔢 오차제곱합 (SSE)", f"{sse:.3f}")
            with col2:
                st.metric("🎯 정확도 (R²)", f"{acc:.1f}%")

            st.info("👉 Epoch이 증가할수록 회귀식 계수가 점점 안정되어 실제 데이터에 가까워집니다!")
            st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("""AI가 더욱 복잡한 문제를 해결하기 위해 발전한 기술이 **딥러닝**(Deep Learning)입니다.
        딥러닝은 **인공신경망**(Artificial Neural Network)을 기반으로 하며,
        사람의 뇌 구조를 모방하여 정보를 처리합니다.
        """)
        col1, col2 = st.columns([1, 1]) 
        with col1:
            st.image("image/deep_learning_structure.png",
                    caption="딥러닝 구조 예시",
                    width=300)
        with col2:
            st.markdown("""
            ##### 🔗 딥러닝 구조:
            입력층 → 은닉층(hidden layer) → 출력층  
            각 층에는 수많은 **뉴런**(neuron)이 존재하고, 이들은 정보를 조금씩 처리하며 다음 층으로 전달합니다.  
            층이 많아질수록 복잡한 패턴을 인식할 수 있으며, 뉴런 수가 많을수록 더 정교한 정보 표현이 가능합니다.
            """)
        st.markdown("""
        ##### 🔁 반복 학습과 에포크(epoch)  
        이러한 딥러닝 모델은 데이터를 여러 번 학습하면서 성능을 높입니다.  
        **에포크**(epoch)란 **전체 데이터를 한 번 학습하는 과정**을 말합니다.  
        에포크가 반복될수록 AI는 오차를 줄이며 더 정확한 예측을 하게 됩니다.
        """)           
        st.success("""
        👉 **[두 줄 정리]**
        - **딥러닝**은 여러 층을 거치며 복잡한 패턴까지 찾아내는 AI 방법  
        - **데이터**를 여러 번 **학습**(에포크)해 오차를 점점 줄여간다
        """)
        st.markdown("""
        <div style="
            background-color: #f0f7ff;
            border-left: 6px solid #1976d2;
            padding: 12px;
            margin-top: 15px;
            border-radius: 8px;
            font-size: 22px;
            font-weight: bold;
            color: #0d47a1;
            ">
            💡 생각 공작소
        </div>
        """, unsafe_allow_html=True)
        seq_text = st.text_input("수열 입력 (쉼표로 구분)", value="2,4,8,16,32", key="dl_seq")
        parsed, err = parse_sequence(seq_text)
        if err:
            st.warning(err)
        else:
            x, y = parsed
            col1, col2, col3 = st.columns(3)
            with col1:
                hidden1 = st.slider("1층 뉴런 수", 4, 64, 36)
            with col2:
                hidden2 = st.slider("2층 뉴런 수", 4, 32, 18)
            with col3:
                epochs = st.slider("학습 횟수 (Epochs)", 25, 100, 50)
            scaler = MinMaxScaler()
            x_scaled = scaler.fit_transform(x)
            dl_model, y_pred_dl, latex_equation_dl = run_deep_learning(x_scaled, y, hidden1, hidden2, epochs)
            sse_dl = np.sum((y - y_pred_dl) ** 2)
            mse_dl = mean_squared_error(y, y_pred_dl)
            acc_dl = r2_score(y, y_pred_dl) * 100

            st.info("👉 딥러닝은 충분한 학습(Epoch)과 적절한 은닉층 뉴런 수를 설정해야 성능이 향상됩니다!")
            fig, ax = plt.subplots()
            ax.scatter(x, y, color="#1976D2", s=45, label="실제값", zorder=3)
            ax.plot(x, y_pred_dl, color="#FF9800", linewidth=2, label="딥러닝 예측값", zorder=2)
            for xi, yi, ypi in zip(x.flatten(), y, y_pred_dl):
                ax.plot([xi, xi], [yi, ypi], "--", color="red", linewidth=1, alpha=0.7, label="오차" if xi == x[0,0] else "")
            ax.set_title("딥러닝 예측 vs 실제값", fontsize=13, fontweight="bold")
            ax.set_xlabel("항 번호 (x)")
            ax.set_ylabel("값 (y)")
            ax.grid(alpha=0.25)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(dict(zip(labels, handles)).values(), dict(zip(labels, handles)).keys(), prop=fm.FontProperties(fname=font_path, size=10))
            st.pyplot(fig)
            c1, c2 = st.columns(2)
            with c1:
                st.metric("🔢 SSE (오차 합)", f"{sse_dl:.3f}")
            with c2:            
                st.metric("🎯 정확도 (R²)", f"{acc_dl:.1f}%")
            errors_df = pd.DataFrame({
                "실제값": y,
                "딥러닝 예측값": y_pred_dl,
            })
            errors_df["오차"] = (errors_df["실제값"] - errors_df["딥러닝 예측값"]).abs()
            st.markdown("##### 📉 실제값과 딥러닝 예측값 비교")
            st.dataframe(
                errors_df.style.format(precision=2).background_gradient(
                    cmap='Reds', subset=["오차"]
                ),
                use_container_width=True, height=250, hide_index=True
            )
            st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[4]:
        st.markdown(""" 
        머신러닝은 단순히 데이터를 외우는 것이 아니라,  입력값(X)과 출력값(Y)의 관계를 수학적 함수(모델)로 학습합니다.  
        예를 들어,
        - 입력 데이터: `X = 1, 2, 3, 4, 5`  
        - 출력 데이터: `Y = 2, 4, 6, 8, 10`   
        머신러닝은 “$y = 2x$”라는 규칙을 찾아냅니다. 이후 새로운 값 $x = 6$이 들어오면,  학습한 함수를 이용해 **$y = 12$** 라고 예측할 수 있습니다.  
        즉, 머신러닝의 예측은 **과거 데이터를 기반으로 수학적 규칙을 학습한 후, 새로운 입력값에 대해 출력값을 계산**하는 과정입니다.  
        """)
        st.success("""
        👉 **[두 줄 정리]**  
        - 머신러닝은 **데이터로부터 규칙(함수)** 을 학습  
        - 새로운 입력값에 대해 **학습한 함수를 이용해 출력값을 예측**  
        """)
        st.markdown("""
        <div style="
            background-color: #f0f7ff;
            border-left: 6px solid #1976d2;
            padding: 12px;
            margin-top: 15px;
            border-radius: 8px;
            font-size: 22px;
            font-weight: bold;
            color: #0d47a1;
            ">
            🔮 생각 공작소
        </div>
        """, unsafe_allow_html=True)
        seq_text = st.text_input("수열 입력 (쉼표로 구분)", value="1,4,9,16,25,36", key="ml_predict_seq")
        parsed, err = parse_sequence(seq_text)
        if err:
            st.warning(err)
        else:
            x, y = parsed
            degree = st.slider("다항 회귀 차수 선택", 1, 4, 2, key="ml_degree")
            poly = PolynomialFeatures(degree=degree, include_bias=False)
            X_poly = poly.fit_transform(x)
            ml_model = LinearRegression().fit(X_poly, y)
            y_pred_ml = ml_model.predict(X_poly)
            latex_equation_ml = poly_equation_to_latex(ml_model, poly)
            next_input = st.number_input(
                "예측하고 싶은 X값 입력",
                value=float(x[-1][0] + 1),
                step=1.0,
                format="%.2f"
            )
            x_next = np.array([[next_input]])
            X_next_trans = poly.transform(x_next)
            pred_ml_next = ml_model.predict(X_next_trans)[0]

            st.info(f"👉 X={next_input:.2f}일 때, 머신러닝 예측값은 **{pred_ml_next:.2f}** 입니다.")
            st.markdown("""
                <style>
                .pred-table {
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 8px;
                }
                .pred-table th, .pred-table td {
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: center;
                    font-size: 15px;
                }
                .pred-table th {
                    background-color: #f0f4f8;
                    color: #1565c0;
                    font-weight: bold;
                }
                .pred-table td {
                    font-weight: bold;
                }
                </style>
            """, unsafe_allow_html=True)
            pred_table_html = f"""
            <table class='pred-table'>
                <thead>
                    <tr>
                        <th>모델</th>
                        <th>X={next_input:.2f}일 때 예측값</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>머신러닝 ({degree}차 회귀)</td>
                        <td>{pred_ml_next:.2f}</td>
                    </tr>
                </tbody>
            </table>
            """
            st.markdown(pred_table_html, unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1: show_data = st.checkbox("입력 데이터", value=True, key="show_data_ml")
            with col2: show_fit = st.checkbox("머신러닝 곡선", value=True, key="show_fit_ml")
            with col3: show_pred = st.checkbox("예측값", value=True, key="show_pred_ml")
            fig, ax = plt.subplots(figsize=(7, 5))
            sorted_idx = np.argsort(x[:, 0])
            x_sorted = x[sorted_idx, 0]
            y_pred_ml_sorted = y_pred_ml[sorted_idx]
            if show_data:
                ax.scatter(x[:, 0], y, color='#1976d2', edgecolors='white', s=90, label='입력 데이터')
            if show_fit:
                ax.plot(x_sorted, y_pred_ml_sorted, color='#ff9800', linewidth=2.5, label=f'ML ({degree}차)')
                ax.text(
                    0.38, 0.95,
                    f"$ {latex_equation_ml} $",
                    transform=ax.transAxes,
                    fontsize=12,
                    verticalalignment='top'
                )
            if show_pred:
                ax.scatter(x_next[0][0], pred_ml_next, color='#d32f2f', edgecolors='black', s=130, marker='o', zorder=5, label='ML 예측')
                ax.annotate(
                    f"예측: {pred_ml_next:.2f}",
                    (x_next[0][0], pred_ml_next),
                    textcoords="offset points",
                    xytext=(5, 20),
                    ha='left',
                    color='#d32f2f',
                    fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#d32f2f", lw=1)
                )
            ax.set_title(f"머신러닝 예측 (차수={degree})", fontsize=15, fontweight='bold', color='#1976d2', pad=15)
            ax.set_xlabel("항 번호 (x)")
            ax.set_ylabel("값 (y)")
            ax.grid(alpha=0.25)

            ax.legend(fontsize=10, frameon=True, fancybox=True, shadow=True)
            plt.tight_layout()
            st.pyplot(fig)
            st.subheader("📝 데이터 분석 및 예측 결과 작성")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                school = st.text_input("학교명", key="pdf_school")
            with col2:
                student_id = st.text_input("학번", key="pdf_id")
            with col3:
                student_name = st.text_input("이름", key="pdf_name")
            student_info = {
                "school": school,
                "id": student_id,
                "name": student_name,
            }
            analysis_text = st.text_area("데이터 분석 및 예측 결과를 작성하세요.", key="analysis_ml")
            if st.button("📥 PDF 저장하기"):
                pdf_bytes = create_pdf(
                    student_info,
                    analysis_text,
                    latex_equation_ml,
                    pred_ml_next,
                    x, y, y_pred_ml,
                    next_input,
                    fig=fig
                )
                st.download_button(
                    label="📄 PDF 다운로드",
                    data=pdf_bytes,
                    file_name=f"AI_탐구보고서_{student_name}.pdf",
                    mime="application/pdf"
                )
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)