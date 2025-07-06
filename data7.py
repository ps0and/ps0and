import streamlit as st
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import pandas as pd
import re
import os

# 폰트 파일 절대 경로 설정 (중요!)
font_path = os.path.join(os.path.dirname(__file__), "font/NanumGothic.ttf")

# 시스템에 폰트 추가
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()

# 전역 폰트 설정 적용
matplotlib.rcParams['font.family'] = font_name
matplotlib.rcParams['axes.unicode_minus'] = False

# -------------------- [레이아웃용 마크다운 함수] --------------------
def pretty_title(text, color1, color2):
    return f"""
    <div style='
        background: linear-gradient(90deg, {color1} 0%, {color2} 100%);
        border-radius: 18px;
        box-shadow: 0 2px 8px 0 rgba(33,150,243,0.06);
        padding: 4px 18px 0px 18px;
        margin-bottom: 10px;'>
        <h4 style='margin-top:0;'><b>{text}</b></h4>
    </div>
    """

# -------------------- [수식(LaTeX) 생성 함수] --------------------
def get_polynomial_equation_latex(model, poly):
    terms = poly.get_feature_names_out(['x'])
    coefs = model.coef_
    intercept = model.intercept_
    parsed_terms = []
    for term, coef in zip(terms, coefs):
        if abs(coef) > 1e-6:
            if "^" in term:
                degree = int(term.split("^")[1])
            else:
                degree = 1
            parsed_terms.append((degree, coef))
    parsed_terms.sort(reverse=True, key=lambda t: t[0])
    latex_terms = []
    for degree, coef in parsed_terms:
        if abs(coef) == 1.0:
            sign = "-" if coef < 0 else ""
            term = f"{sign}x^{{{degree}}}"
        else:
            term = f"{coef:.2f}x^{{{degree}}}"
        latex_terms.append(term)
    if abs(intercept) > 1e-6:
        sign = "-" if intercept < 0 else "+"
        latex_terms.append(f"{sign}{abs(intercept):.2f}")
    expr = " + ".join(latex_terms)
    expr = re.sub(r"\+\s*\+", "+", expr)
    expr = re.sub(r"\+\s*-\s*", "- ", expr)
    expr = re.sub(r"-\s*-\s*", "+ ", expr)
    expr = expr.strip()
    if expr.startswith("+"):
        expr = expr[1:]
    return f"y = {expr}"

def get_manual_equation_latex(coeffs, b):
    terms = []
    for deg, coef in coeffs:
        if abs(coef) > 1e-6:
            sign = "-" if coef < 0 else ""
            if abs(coef) == 1.0:
                term = f"{sign}x^{{{deg}}}"
            else:
                term = f"{coef:.2f}x^{{{deg}}}"
            terms.append(term)
    if abs(b) > 1e-6:
        sign_b = "-" if b < 0 else "+"
        terms.append(f"{sign_b}{abs(b):.2f}")
    expr = " + ".join(terms)
    expr = re.sub(r"\+\s*\+", "+", expr)
    expr = re.sub(r"\+\s*-\s*", "- ", expr)
    expr = re.sub(r"-\s*-\s*", "+ ", expr)
    expr = expr.strip()
    if expr.startswith("+"): expr = expr[1:]
    return f"y = {expr}" if terms else f"y = {b:.2f}"

# -------------------- [AI 모델 함수] --------------------
@st.cache_data
def run_poly_regression(x, y, degree):
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train = poly.fit_transform(x)
    model = LinearRegression().fit(X_train, y)
    y_pred = model.predict(X_train)
    latex = get_polynomial_equation_latex(model, poly)
    return model, poly, y_pred, latex

@st.cache_data
def run_deep_learning(x, y, hidden1, hidden2, epochs):
    model = Sequential([
        Dense(hidden1, input_shape=(x.shape[1],), activation='relu'),
        Dense(hidden2, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer=Adam(0.01), loss='mse')
    model.fit(x, y, epochs=epochs, verbose=0)
    y_pred = model.predict(x).flatten()
    latex = f"Deep Learning (1-{hidden1}-{hidden2}-1)"
    return model, y_pred, latex

def show():
    st.header("🗓️ Day 7")
    st.subheader("인공지능 수열 예측 시뮬레이터")
    st.write("AI를 이용해서 수열 또는 실생활 데이터를 예측해봅시다.")
    st.divider()
    st.subheader("🎥 오늘의 수업 영상")
    st.subheader("📌 학습 목표")
    st.markdown("""
    - 수학 모델과 AI 모델의 예측 성능을 비교할 수 있다.\n 
        수동 회귀 모델과 AI 모델(머신러닝 또는 딥러닝)의 예측값($\hat{y}$)과 오차($SSE = \sum (y_i - \hat{y}_i)^2$)를 비교 분석한다.
    - AI 모델로 새로운 데이터를 예측할 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    # ---- 입력 방식 ----
    st.subheader("1️⃣ 입력 방식 선택 및 데이터 입력")
    input_mode = st.radio("입력 방식 선택을 선택하세요.", ["수열 입력", "실생활 데이터 입력"])

    if input_mode == "실생활 데이터 입력":
        # 데이터 수집 사이트 표 추가
        st.markdown("""
        **🔎 데이터 수집 사이트 추천**

        | 사이트명             | 링크                                      | 특징                                                      |
        |:--------------------|:-----------------------------------------|:----------------------------------------------------------|
        | 🌍 **Kaggle (캐글)**     | [kaggle.com](https://www.kaggle.com)      | - 전 세계 데이터 과학자들이 모여 다양한 **공개 데이터셋**을 공유|
        | 🇰🇷 **공공데이터 포털**   | [data.go.kr](https://www.data.go.kr)      | - **대한민국 정부 및 공공기관에서 제공**하는 신뢰성 높은 데이터로서 행정, 교통, 환경, 경제 등 다양한 주제|
        """)

    if input_mode == "수열 입력":
        x_name, y_name = "X", "Y"
    else:
        # 실생활 데이터 입력 모드에서만 변수 이름 입력을 바로 아래에 위치
        st.markdown(f"#### 🎓 실생활 데이터 입력")
        with st.expander("🔤 변수 설명(이름) 입력"):
            x_name_input = st.text_input("X 변수의 이름/설명 (예: 공부 시간, 키 등)", value="")
            y_name_input = st.text_input("Y 변수의 이름/설명 (예: 점수, 몸무게 등)", value="")
        x_name = x_name_input.strip() if x_name_input.strip() else "X"
        y_name = y_name_input.strip() if y_name_input.strip() else "Y"

    if input_mode == "수열 입력":
        default_seq = "2, 5, 8, 11, 14, 17"
        st.markdown(f"#### 🎓 수열 데이터 입력")
        seq_input = st.text_input("수열을 입력하세요 (쉼표로 구분):", default_seq, key="seq_input")
        y = np.array(list(map(float, seq_input.split(","))))
        x = np.arange(1, len(y) + 1).reshape(-1, 1)
    else:
        # 실생활 데이터 입력 모드에서 x/y 값 입력
        x_input = st.text_input(f"{x_name} 값 (쉼표로 구분):", "6.5,8,5,7,9,4.5,10,6,7.5,5.5", key="x_input")
        y_input = st.text_input(f"{y_name} 값 (쉼표로 구분):", "7,8,5,6,9,4,8,5,7,6", key="y_input")
        try:
            x_vals = list(map(float, x_input.strip().split(",")))
            y = list(map(float, y_input.strip().split(",")))
        except ValueError:
            st.error("❌ 숫자만 쉼표로 구분해 입력해 주세요!")
            st.stop()
        if len(x_vals) != len(y):
            st.error(f"❌ {x_name}와 {y_name}의 길이가 같아야 합니다.")
            st.stop()
        x = np.array(x_vals).reshape(-1, 1)
        y = np.array(y)

    st.divider()

    st.markdown(f"##### 📝 입력 데이터 미리보기 ({x_name}, {y_name})")
    data_df = pd.DataFrame({
        x_name: x.flatten(),
        y_name: y.flatten()
    })
    st.dataframe(data_df.T, use_container_width=True)
    if input_mode == "수열 입력":
        st.info("**참고:** 수열의 X값(즉, 항의 번호)은 항상 1, 2, 3, ...과 같은 자연수입니다.")

    st.markdown(f"##### 📑 데이터 요약 정보 ({x_name}, {y_name})")
    desc = data_df.describe().T
    desc['missing'] = data_df.isnull().sum()
    st.write(desc)
    correlation = data_df[x_name].corr(data_df[y_name])
    st.markdown(
        f"""
        - 📦 **데이터 개수:** {len(data_df)}
        - 📈 **{x_name} 평균:** {data_df[x_name].mean():.2f},  **표준편차**: {data_df[x_name].std():.2f}
        - 📈 **{y_name} 평균:** {data_df[y_name].mean():.2f},  **표준편차**: {data_df[y_name].std():.2f}
        - 🔗 **상관계수({x_name} ↔ {y_name}):** {correlation:.2f}
        """
    )
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    # ---- 수동 회귀 vs AI 모델 ----
    st.subheader("2️⃣ 수동 회귀 vs AI 모델")
    manual_col, ai_col = st.columns(2)

    with manual_col:
        st.markdown(pretty_title("✍️ 수동 회귀", "#e3f2fd", "#bbdefb"), unsafe_allow_html=True)
        st.info("👉 사용자가 직접 차수와 계수를 조절하여, 데이터에 가장 잘 맞는 수학 함수를 만들어 보는 방법입니다.")
        degree_manual = st.selectbox("차수 선택 (최대 3차)", options=[1, 2, 3], index=0)
        coeffs = []
        y_pred_manual = np.zeros_like(y, dtype=float)
        for deg in range(degree_manual, 0, -1):
            coef = st.slider(
                f"$ x^{{{deg}}}$ 계수",
                -10.0, 10.0,
                1.0 if deg == 1 else 0.0,
                0.1,
                key=f"manual_coef_deg{deg}"
            )
            coeffs.append((deg, coef))
            y_pred_manual += coef * x[:, 0] ** deg
        b = st.slider(f"상수항 $b$ (절편)", -20.0, 20.0, 0.0, 0.1)
        y_pred_manual += b
        latex_equation_manual = get_manual_equation_latex(coeffs, b)
        manual_sse = np.sum((y - y_pred_manual) ** 2)
        st.markdown("#### **📐수동 회귀 함수식**")
        st.latex(latex_equation_manual)

    with ai_col:
        st.markdown(pretty_title("🤖 AI 모델", "#e3f2fd", "#bbdefb"), unsafe_allow_html=True)
        st.info("""
            👉 컴퓨터가 데이터를 보고 자동으로 예측 공식을 학습합니다.
            - **AI 회귀:** 여러 차수의 수학식(다항식)을 자동으로 찾아줍니다.
            - **AI 딥러닝:** 인공신경망으로 복잡한 패턴도 학습 가능합니다.
        """)
        model_type = st.radio("모델 선택", ["AI 회귀", "AI 딥러닝"])
        if model_type == "AI 회귀":
            degree = st.selectbox("차수 선택", options=[1, 2, 3], index=0)
            model, poly, y_pred, latex_equation_ai = run_poly_regression(x, y, degree)
        else:
            hidden1 = st.slider("1층 뉴런 수", 4, 64, 36)
            hidden2 = st.slider("2층 뉴런 수", 4, 32, 18)
            epochs = st.slider("학습 횟수", 25, 50, 30)
            model, y_pred, latex_equation_ai = run_deep_learning(x, y, hidden1, hidden2, epochs)
            poly = None  # 딥러닝에서는 다항 특성 변환이 없음
        sse = np.sum((y - y_pred) ** 2)
        st.markdown("#### **📐 AI 모델 함수식**")
        st.latex(latex_equation_ai)
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(pretty_title("📋 모델 비교", "#e3f2fd", "#bbdefb"), unsafe_allow_html=True)
        comparison_df = pd.DataFrame({
            "모델": ["수동 회귀", model_type],
            "함수식": [latex_equation_manual, latex_equation_ai],
            "SSE": [f"{manual_sse:.2f}", f"{sse:.2f}"]
        })
        st.dataframe(comparison_df.reset_index(drop=True), use_container_width=True, height=125)
        st.markdown(
            f"""
            <span style='color:#1976d2; font-size:15px;'>
            🧮 <b>SSE</b>가 낮을수록 <b>모델의 예측 오차</b>가 적습니다.
            </span>
            """, unsafe_allow_html=True
        )
        best_model = comparison_df.loc[comparison_df['SSE'].astype(float).idxmin(), '모델']
        st.info(f"👉 두 모델의 SSE(오차 합계)를 비교해보세요. SSE가 더 작은 모델✨({best_model})이 주어진 데이터에 더 잘 맞는 예측을 했음을 의미합니다.")

    with col2:
        st.markdown(pretty_title("🔍 예측값 비교", "#fce4ec", "#f8bbd0"), unsafe_allow_html=True)
        if input_mode == "수열 입력":
            next_label = f"예측하고 싶은 {y_name}의 {x_name}값"
            next_input_default = float(len(y) + 1)
        else:
            next_label = f"예측하고 싶은 {x_name} 입력값"
            next_input_default = float(len(y) + 1)
        next_input = st.number_input(next_label, value=next_input_default)
        x_next = np.array([[next_input]])
        pred_manual_next = sum([
            coef * (x_next[0][0] ** deg) for (deg, coef) in coeffs
        ]) + b
        if model_type == "AI 회귀":
            X_next_trans = poly.transform(x_next)
            pred_ai_next = model.predict(X_next_trans)[0]
        else:
            pred_ai_next = model.predict(x_next)[0][0]
        prediction_df = pd.DataFrame({
            "모델": ["수동 회귀", model_type],
            f"{x_name}={next_input:.2f}일 때 {y_name} 예측값": [f"{pred_manual_next:.2f}", f"{pred_ai_next:.2f}"]
        })
        st.dataframe(prediction_df.reset_index(drop=True), use_container_width=True, height=125)
        st.markdown(
            f"""
            <span style='color:#d81b60; font-size:15px;'>
            ⭐️ <b>다음 입력</b>에 대해 <b>두 모델의 예측값</b>을 직접 비교해보세요!
            </span>
            """, unsafe_allow_html=True
        )
        st.info(f"👉 {x_name}={next_input:.2f}에서 두 모델의 예측값이 얼마나 다른지 확인해보고, 실제 관측값과 비교해 어떤 모델이 더 현실적으로 예측했는지 해석해보세요.")

    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    # ---- 시각화 ----
    st.subheader(f"📊 시각화 ({x_name} vs {y_name} 비교)")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(
        x[:, 0], y,
        color='#1976d2', edgecolors='white', linewidths=1.8,
        s=90, marker='o', label='입력 데이터'
    )
    sorted_idx = np.argsort(x[:, 0])
    x_sorted = x[sorted_idx, 0]
    y_pred_manual_sorted = y_pred_manual[sorted_idx]
    ax.plot(
        x_sorted, y_pred_manual_sorted,
        color='#ff9800', linestyle='--', linewidth=2.5, label='수동 회귀'
    )
    y_pred_sorted = y_pred[sorted_idx]
    ax.plot(
        x_sorted, y_pred_sorted,
        color='#43a047', linestyle='-', linewidth=2.5, label='AI 모델'
    )
    ax.scatter(
        x_next[0][0], pred_manual_next,
        color='#d32f2f', edgecolors='black', s=130, marker='o', zorder=5, label='수동 예측'
    )
    ax.scatter(
        x_next[0][0], pred_ai_next,
        color='#f06292', edgecolors='black', s=130, marker='X', zorder=5, label='AI 예측'
    )
    ax.annotate(
        f"수동 예측: {pred_manual_next:.2f}",
        (x_next[0][0], pred_manual_next),
        textcoords="offset points",
        xytext=(5, -30),
        ha='left',
        color='#d32f2f',
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#d32f2f", lw=1)
    )
    ax.annotate(
        f"AI 예측: {pred_ai_next:.2f}",
        (x_next[0][0], pred_ai_next),
        textcoords="offset points",
        xytext=(5, 20),
        ha='left',
        color='#f06292',
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#f06292", lw=1)
    )
    ax.text(
        0.38, 0.95,
        f"수동: $ {latex_equation_manual} $",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment='top'
    )
    ax.text(
        0.38, 0.88,
        f"AI: $ {latex_equation_ai} $",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment='top'
    )
    ax.set_title(f"{x_name}와(과) {y_name}의 관계 및 예측", fontsize=17, fontweight='bold', color='#1976d2', pad=15)
    ax.set_xlabel(x_name, fontsize=13, fontweight='bold')
    ax.set_ylabel(y_name, fontsize=13, fontweight='bold')
    ax.grid(alpha=0.25)
    leg = ax.legend(
        fontsize=8, loc='upper left', frameon=True, fancybox=True, framealpha=0.88, shadow=True,
        borderpad=1, labelspacing=0.8
    )
    for line in leg.get_lines():
        line.set_linewidth(3.0)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    # ---- 결과 분석 ----
    st.subheader("📌 결과 분석")
    st.markdown(f"""
    - 입력 방식: **{input_mode}**  
    - **수동 회귀**와 **{model_type}** 모델로 예측을 수행했습니다.  
    - 수동 회귀: $ {latex_equation_manual} $
    - AI 모델: $ {latex_equation_ai} $
    - 다음 입력({x_name}={next_input:.2f})에 대한 예측값:  
    - 수동 회귀: **{pred_manual_next:.2f}**  
    - {model_type}: **{pred_ai_next:.2f}**
    -  SSE가 더 작은 모델: **{best_model}**
    """)
    st.success(
        f"""🔎 **학습 Tip**  
    두 모델의 예측 결과를 비교하고, 실제 현상(혹은 관측 데이터)에 더 가까운 쪽이 무엇인지,
    그리고 왜 그런 결과가 나왔는지 생각해보세요.  
    데이터의 개수, 분포, 함수의 복잡성 등이 모델의 성능에 영향을 미칩니다."""
    )
    st.markdown(
    "<div style='text-align: left; color:orange;'>✨결과 분석과 시각화 그래프를 복사한 뒤, 스프레드시트 링크에 그대로 붙여넣어 과제를 제출해주세요!",
    unsafe_allow_html=True
    )
    st.markdown(
    """
    <style>
    .hw-submit-btn {
        display: inline-block;
        background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
        color: #fff !important;
        font-size: 17px;
        font-weight: bold;
        padding: 5px 10px 5px 10px;
        border-radius: 2em;
        box-shadow: 0 3px 16px #1976d238;
        margin: 0px 0 0 0;
        letter-spacing: 1px;
        text-decoration: none !important;
        transition: background 0.18s, box-shadow 0.18s, transform 0.13s;
    }
    .hw-submit-btn:hover {
        background: linear-gradient(90deg, #42a5f5 0%, #1976d2 100%);
        color: #fff !important;
        transform: translateY(-2px) scale(1.045);
        box-shadow: 0 8px 30px #1976d22f;
        text-decoration: none !important;
    }
    </style>
    <div style='text-align: right; margin: 0px 0 0px 0;'>
        <a href="https://docs.google.com/spreadsheets/d/1n82pBQVdLg0iXVtm0aXJAGq0C_5N1RB-C-7sCZX7AEw/edit?usp=sharing"
           target="_blank"
           class="hw-submit-btn">
            📤 과제 제출하러 가기
        </a>
    </div>
    """,
    unsafe_allow_html=True
)