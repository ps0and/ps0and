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
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from fpdf import FPDF
from datetime import datetime
import tempfile
import io
import pandas as pd
import re
import os

font_path = os.path.join(os.path.dirname(__file__), "font/NanumGothic.ttf")
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()
matplotlib.rcParams['font.family'] = font_name
matplotlib.rcParams['axes.unicode_minus'] = False

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

@st.cache_data
def run_poly_regression(x, y, degree):
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train = poly.fit_transform(x)
    model = LinearRegression().fit(X_train, y)
    y_pred = model.predict(X_train)
    latex = get_polynomial_equation_latex(model, poly)
    return model, poly, y_pred, latex

@st.cache_resource
def run_deep_learning(x, y, hidden1, hidden2, epochs):
    model = Sequential([
        Dense(hidden1, input_shape=(x.shape[1],), activation='relu'), 
        Dense(hidden2, activation='relu'),
        Dense(1, activation='linear')  
    ])
    model.compile(optimizer=Adam(0.01), loss='mse')
    model.fit(x, y, epochs=epochs, verbose=0, batch_size=32)  
    y_pred = model.predict(x)
    return model, y_pred, f"Deep Learning (1-{hidden1}-{hidden2}-1)"

class ThemedPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=15)
        self._font_family = "Nanum"
        self.footer_left = ""
        self.c_primary = (25, 118, 210)  
        self.c_primary_lt = (227, 242, 253)  
        self.c_accent = (67, 160, 71)     
        self.c_warn = (211, 47, 47)       
        self.c_border = (200, 200, 200)
        self.c_text_muted = (120, 120, 120)

    def header(self):
        self.set_fill_color(*self.c_primary)
        self.rect(0, 0, self.w, 22, 'F')
        self.set_xy(10, 6)
        self.set_text_color(255, 255, 255)
        self.set_font(self._font_family, '', 25)
        self.cell(0, 10, "데이터 기반 탐구 보고서", ln=1, align='C')
        self.set_text_color(33, 33, 33)
        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(*self.c_border)
        self.set_line_width(0.2)
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

    def kv_card(self, title, kv_pairs):
        """ key-value 형태의 카드 (2열) """
        self.h2(title)
        self.set_draw_color(*self.c_border)
        self.set_line_width(0.3)
        self.set_font(self._font_family, '', 11)
        self.set_fill_color(255, 255, 255)
        col_w = (self.w - 20) / 2  
        cell_h = 8
        x0 = 10
        y0 = self.get_y()
        for i, (k, v) in enumerate(kv_pairs):
            x = x0 + (i % 2) * col_w
            if i % 2 == 0 and i > 0:
                self.ln(cell_h)
            self.set_x(x)
            # 키
            self.set_text_color(120, 120, 120)
            self.cell(col_w * 0.35, cell_h, str(k), border=1)
            # 값
            self.set_text_color(33, 33, 33)
            self.cell(col_w * 0.65, cell_h, str(v), border=1)
        if len(kv_pairs) % 2 == 1:
            self.set_x(x0 + col_w)
            self.set_text_color(120, 120, 120)
            self.cell(col_w * 0.35, cell_h, "", border=1)
            self.set_text_color(33, 33, 33)
            self.cell(col_w * 0.65, cell_h, "", border=1)
            self.ln(cell_h)
        else:
            self.ln(cell_h)
        self.ln(2)

    def info_card(self, title, lines):
        self.h2(title)
        self.set_draw_color(*self.c_border)
        self.set_line_width(0.3)
        self.set_font(self._font_family, '', 11)
        self.set_fill_color(255, 255, 255)
        x, y = 10, self.get_y()
        w = self.w - 20
        start_y = self.get_y()
        for line in lines:
            self.set_x(12)
            self.multi_cell(w - 4, 7, line)
        end_y = self.get_y()
        self.rect(x, y, w, end_y - y)
        self.ln(2)

    def table(self, headers, rows, col_widths=None, zebra=True, highlight_row_idx=None):
        """
        headers: list[str]
        rows: list[list]
        col_widths: list[float] or None -> 자동 분배
        """
        self.set_font(self._font_family, '', 11)
        border = 1
        cell_h = 8
        table_w = self.w - 20  
        if col_widths is None:
            col_widths = [table_w / len(headers)] * len(headers)
        self.set_fill_color(240, 244, 248)
        self.set_text_color(21, 101, 192)
        for h, w in zip(headers, col_widths):
            self.cell(w, cell_h, str(h), border=border, align='C', fill=True)
        self.ln(cell_h)
        self.set_text_color(33, 33, 33)
        for i, row in enumerate(rows):
            if zebra and i % 2 == 1:
                self.set_fill_color(250, 250, 250)
                fill = True
            else:
                self.set_fill_color(255, 255, 255)
                fill = True
            if highlight_row_idx is not None and i == highlight_row_idx:
                self.set_fill_color(255, 249, 196) 
                fill = True
            for val, w in zip(row, col_widths):
                self.cell(w, cell_h, str(val), border=border, align='C', fill=fill)
            self.ln(cell_h)
        self.ln(2)

def create_pdf(student_info, analysis, interpretation, comparison_df, errors_df, 
               latex_equation_ml, latex_equation_dl, pred_ml_next, pred_dl_next, 
               x_name, y_name, next_input, fig=None):
    pdf = ThemedPDF()
    pdf.add_font('Nanum', '', font_path, uni=True)
    pdf.set_font('Nanum', '', 12)
    pdf._font_family = "Nanum"   
    pdf.footer_left = f"{student_info.get('school','')} • {student_info.get('name','')}"
    pdf.add_page()
    pdf.add_font('Nanum', '', font_path, uni=True)
    pdf.set_font('Nanum', '', 12)
    pdf.footer_left = f"{student_info.get('school','')} • {student_info.get('name','')}"
    pdf.set_title("데이터 기반 탐구 보고서")
    pdf.set_author(student_info.get('name', ''))
    pdf.set_subject(student_info.get('topic', ''))
    pdf.set_creator("AI Sequence Predictor")
    pdf.set_keywords("AI, Machine Learning, Deep Learning, Regression")
    kvs = [
        ("학교", student_info.get('school', '')),
        ("학번", student_info.get('id', '')),
        ("이름", student_info.get('name', '')),
        ("탐구 주제", student_info.get('topic', '')),
        ("작성일", datetime.now().strftime("%Y-%m-%d")),
    ]
    pdf.ln(5)  
    pdf.kv_card("👤 학생 정보", kvs)
    pdf.info_card("🧮 모델 함수식",
        [f"머신러닝: {latex_equation_ml}",
         f"딥러닝: {latex_equation_dl}"]
    )
    pdf.info_card("🔮 예측 요약",
        [f"{x_name} = {next_input:.2f} 일 때",
         f"• 머신러닝 예측 {y_name}: {pred_ml_next:.2f}",
         f"• 딥러닝 예측 {y_name}: {pred_dl_next:.2f}"]
    )
    headers = ["모델", "SSE", "정확도"]
    rows = comparison_df[["모델", "SSE", "정확도"]].values.tolist()
    min_sse_idx = comparison_df["SSE"].astype(float).idxmin()
    highlight_idx = list(comparison_df.index).index(min_sse_idx)
    pdf.h2("📊 모델 비교")
    pdf.table(headers, rows, highlight_row_idx=highlight_idx)
    if fig is not None:
        pdf.add_page()  
        pdf.h2("📈 시각화")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name, format="png", bbox_inches="tight", dpi=200)
            pdf.image(tmpfile.name, x=10, y=None, w=pdf.w-20)
        pdf.ln(3)
    pdf.h2("📝 데이터 분석 및 예측 결과 (학생 작성)")
    pdf.p(analysis if analysis else "내용 없음")
    pdf.h2("📖 탐구 결과 및 해석 (학생 작성)")
    pdf.p(interpretation if interpretation else "내용 없음")
    return bytes(pdf.output(dest='S'))

# ✅ 메인 화면
def show():
    st.header("🗓️ Day 7")
    st.subheader("AI 예측 스튜디오")
    st.write("AI를 이용해서 수열 또는 실생활 데이터를 예측해봅시다.")
    st.divider()
    st.video("https://youtu.be/GU4YUJVb_kA")
    st.subheader("📌 학습 목표")
    st.markdown("""
    - 머신러닝과 딥러닝의 예측값과 정확도를 비교 분석할 수 있다.
    - AI 모델로 새로운 데이터를 예측할 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    tabs = st.tabs([
        "1️⃣ 데이터 수집",
        "2️⃣ 데이터 입력",
        "3️⃣ AI 모델 만들기",
        "4️⃣ 예측 및 시각화",
        "5️⃣ 결과 분석"
    ])
    st.markdown("""
        <style>
        div[data-baseweb="tab-list"] {
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    with tabs[0]:   
        st.subheader("👤 학생 정보 입력")
        col1, col2, col3 = st.columns([2, 1, 1]) 

        with col1:
            school = st.text_input("학교명", key="school")
        with col2:
            student_id = st.text_input("학번", key="id")
        with col3:
            student_name = st.text_input("이름", key="name")
        topic = st.text_input("탐구 주제", key="topic")
        st.session_state["student_info"] = {
            "school": school,
            "id": student_id,
            "name": student_name,
            "topic": topic
        }
        st.markdown("""
            <style>
            .summary-table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 10px;
            }
            .summary-table th, .summary-table td {
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 15px;
                text-align: center;
            }
            .summary-table th {
                background-color: #f0f4f8;
                color: #1565c0;
                font-weight: bold;
            }
            .info-box {
                background-color: #e3f2fd;
                border-left: 6px solid #1976d2;
                padding: 12px;
                margin: 15px 0;
                border-radius: 6px;
                font-size: 15px;
            }
            </style>
        """, unsafe_allow_html=True)
        data_source_table = """
        <table class='summary-table'>
        <thead>
            <tr>
            <th>사이트명</th>
            <th>링크</th>
            <th>특징</th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <td>🌍 <b>Kaggle (캐글)</b></td>
            <td><a href="https://www.kaggle.com" target="_blank">kaggle.com</a></td>
            <td>전 세계 데이터 과학자들이 모여 다양한 <b>공개 데이터셋</b>을 공유</td>
            </tr>
            <tr>
            <td>🇰🇷 <b>공공데이터 포털</b></td>
            <td><a href="https://www.data.go.kr" target="_blank">data.go.kr</a></td>
            <td><b>대한민국 정부 및 공공기관</b>에서 제공하는 신뢰성 높은 데이터</td>
            </tr>
            <tr>
            <td>📊 <b>통계청 (KOSIS)</b></td>
            <td><a href="https://kosis.kr" target="_blank">kosis.kr</a></td>
            <td>국가통계포털로 인구, 고용, 물가, 산업 등 <b>공식 통계 데이터</b> 제공</td>
            </tr>
        </tbody>
        </table>
        """
        st.subheader("1️⃣ 데이터 수집")
        st.markdown("**🔎 데이터 수집 사이트 추천**")
        st.markdown(data_source_table, unsafe_allow_html=True)
        st.markdown("""
            <div class="info-box">
            ⚠️ <b>데이터 수집 시 유의사항</b><br><br>
            - 이 앱은 <b>일변수 함수</b> (하나의 입력 변수 X와 하나의 출력 변수 Y) 관계만 분석합니다.<br>
            - X와 Y의 데이터 개수가 반드시 동일해야 합니다.<br>
            - 입력값은 반드시 <b>숫자형 데이터</b>여야 합니다. (문자, 범주형 불가)<br>
            - 결측치(빈칸)나 극단값(이상치)이 있으면 결과가 왜곡될 수 있습니다.<br>
            - 가능한 한 <b>연속적이고 의미 있는 데이터</b>를 선택하세요.<br><br>
            <b>예시:</b> 공부 시간(X) ↔ 시험 점수(Y), 나이(X) ↔ 키(Y), 광고비(X) ↔ 매출액(Y) <br>
                           
            - 예시 데이터(평균기온) 자료 출처: 본 저작물은 기상청에서 작성하여 공공누리 제1유형으로 개방한 평균기온(기상청)을 이용하였으며, 해당 저작물은 기상청 (https://data.kma.go.kr/stcs/grnd/grndTaList.do?pgmNo=70) 에서 무료로 다운받으실 수 있습니다.
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("2️⃣ 입력 방식 선택 및 데이터 입력")
        input_mode = st.radio("입력 방식 선택을 선택하세요.", ["수열 입력", "실생활 데이터 입력"])
        if input_mode == "수열 입력":
            x_name, y_name = "X", "Y"
        else:
            st.markdown(f"#### 🎓 실생활 데이터 입력")
            if st.button("🔄 초기화", type="primary"):
                st.session_state["x_input"] = ""
                st.session_state["y_input"] = ""
            with st.expander("🔤 변수 설명(이름) 입력"):
                x_name_input = st.text_input("X 변수의 이름/설명 (예: 공부 시간, 키 등)", value="연도")
                y_name_input = st.text_input("Y 변수의 이름/설명 (예: 점수, 몸무게 등)", value="평균기온(℃)")
            x_name = x_name_input.strip() if x_name_input.strip() else "X"
            y_name = y_name_input.strip() if y_name_input.strip() else "Y"
        if input_mode == "수열 입력":
            default_seq = "2, 5, 8, 11, 14, 17"
            st.markdown(f"#### 🎓 수열 데이터 입력")
            seq_input = st.text_input("수열을 입력하세요 (쉼표로 구분):", default_seq, key="seq_input")
            if not seq_input.strip():
                st.warning("⚠️ 수열 데이터를 입력해주세요.")
                st.stop()
            y = np.array(list(map(float, seq_input.split(","))))
            x = np.arange(1, len(y) + 1).reshape(-1, 1)
        else:
            x_input = st.text_input(f"{x_name} 값 (쉼표로 구분):",
                                    "2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024",
                                    key="x_input")
            y_input = st.text_input(f"{y_name} 값 (쉼표로 구분):",
                                    "12.2,12.4,12.4,12.2,12.9,12.1,12.6,13.0,12.7,12.7,12.4,12.1,12.1,12.6,12.8,13.1,13.4,12.8,12.8,13.3,13.0,13.3,12.9,13.7,14.5",
                                    key="y_input")
            if not x_input.strip() or not y_input.strip():
                st.warning("⚠️ 데이터를 입력해주세요. (X, Y 값이 모두 필요합니다)")
                st.stop()
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
            st.markdown("### ⚙️ 이상치 전처리 옵션")
            outlier_methods = st.multiselect(
                "이상치 처리 방법을 선택하세요 (여러 개 가능):",
                ["없음", "IQR 방식", "Z-Score 방식"],
                default=["없음"]
            )
            if "IQR 방식" in outlier_methods:
                st.info("📊 **IQR(Interquartile Range) 방식**\n\n"
                        "- Q1(25%), Q3(75%)를 기준으로 IQR = Q3 - Q1 계산\n"
                        "- [Q1 - 1.5×IQR, Q3 + 1.5×IQR] 범위 밖은 이상치")
                Q1_x, Q3_x = np.percentile(x.flatten(), [25, 75])
                Q1_y, Q3_y = np.percentile(y.flatten(), [25, 75])
                IQR_x, IQR_y = Q3_x - Q1_x, Q3_y - Q1_y
                mask = (
                    (x.flatten() >= Q1_x - 1.5 * IQR_x) & (x.flatten() <= Q3_x + 1.5 * IQR_x) &
                    (y.flatten() >= Q1_y - 1.5 * IQR_y) & (y.flatten() <= Q3_y + 1.5 * IQR_y)
                )
                x, y = x[mask], y[mask]
                st.success(f"✅ IQR 방식 적용: {len(x)}개 데이터 남음")
            if "Z-Score 방식" in outlier_methods:
                st.info("📈 **Z-Score 방식**\n\n"
                        "- 평균에서 몇 표준편차 떨어져 있는지 계산\n"
                        "- |Z| > 3 인 데이터는 이상치로 제거")
                from scipy import stats
                z_scores = np.abs(stats.zscore(np.column_stack((x.flatten(), y.flatten()))))
                mask = (z_scores < 3).all(axis=1)
                x, y = x[mask], y[mask]
                st.success(f"✅ Z-Score 방식 적용: {len(x)}개 데이터 남음")

            if outlier_methods == ["없음"]:
                st.info("🔍 이상치 전처리를 적용하지 않았습니다.")
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
        x_mean, y_mean = data_df[x_name].mean(), data_df[y_name].mean()
        x_std, y_std = data_df[x_name].std(), data_df[y_name].std()
        x_min, y_min = data_df[x_name].min(), data_df[y_name].min()
        x_max, y_max = data_df[x_name].max(), data_df[y_name].max()
        correlation = data_df[x_name].corr(data_df[y_name])
        summary_df = pd.DataFrame({
            "평균": [round(x_mean, 2), round(y_mean, 2)],
            "표준편차": [round(x_std, 2), round(y_std, 2)],
            "최솟값": [round(x_min, 2), round(y_min, 2)],
            "최댓값": [round(x_max, 2), round(y_max, 2)],
            "상관계수": [None, round(correlation, 2)]
        }, index=[x_name, y_name])
        summary_df.index.name = "항목"
        styled_df = summary_df.style.set_properties(**{
            "text-align": "center", 
            "font-weight": "bold", 
            "border": "1px solid black"
        }).set_table_styles([
            {"selector": "th", "props": [("text-align", "center"), ("font-weight", "bold"), ("border", "1px solid black")]}
        ])
        st.table(styled_df)
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[2]:
        st.subheader("3️⃣ 머신러닝 vs 딥러닝")
        ml_col, dl_col = st.columns(2)
        with ml_col:
            st.markdown(pretty_title("🤖 머신러닝 (다항 회귀)", "#e3f2fd", "#bbdefb"), unsafe_allow_html=True)
            st.info("👉 머신러닝 모델은 데이터를 보고 자동으로 다항 회귀식을 학습합니다.")
            degree = st.selectbox("차수 선택", options=[1, 2, 3], index=0)
            ml_model, ml_poly, y_pred_ml, latex_equation_ml = run_poly_regression(x, y, degree)
            sse_ml = np.sum((y - y_pred_ml) ** 2)
            st.markdown("#### **📐 머신러닝 함수식**")
            st.latex(latex_equation_ml)
        with dl_col:
            st.markdown(pretty_title("🧠 딥러닝 (신경망)", "#e3f2fd", "#bbdefb"), unsafe_allow_html=True)
            st.info("👉 딥러닝 모델은 인공 신경망으로 복잡한 패턴까지 학습할 수 있습니다.")
            hidden1 = st.slider("1층 뉴런 수", 4, 64, 36)
            hidden2 = st.slider("2층 뉴런 수", 4, 32, 18)
            epochs = st.slider("학습 횟수", 25, 70, 50)
            scaler_x = MinMaxScaler()
            scaler_y = MinMaxScaler()
            x_scaled = scaler_x.fit_transform(x)
            y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))
            dl_model, y_pred_dl_scaled, latex_equation_dl = run_deep_learning(
                x_scaled, y_scaled, hidden1, hidden2, epochs
            )
            y_pred_dl = scaler_y.inverse_transform(y_pred_dl_scaled).flatten()
            sse_dl = np.sum((y - y_pred_dl) ** 2)
            st.markdown("#### **📐 딥러닝 함수식**")
            st.latex(latex_equation_dl)
        st.divider()
        st.markdown(pretty_title("📋 모델 비교", "#e3f2fd", "#bbdefb"), unsafe_allow_html=True)
        acc_ml = r2_score(y, y_pred_ml) * 100
        acc_dl = r2_score(y, y_pred_dl) * 100
        comparison_df = pd.DataFrame({
                "모델": ["머신러닝", "딥러닝"],
                "함수식": [latex_equation_ml, latex_equation_dl],
                "SSE": [f"{sse_ml:.2f}", f"{sse_dl:.2f}"],
                "정확도": [f"{acc_ml:.1f}%", f"{acc_dl:.1f}%"]
            })
        st.dataframe(comparison_df.reset_index(drop=True), use_container_width=True, height=107, hide_index=True)
        errors_df = pd.DataFrame({
                "X값": x.flatten(),
                "실제값": y,
                "머신러닝 예측값": y_pred_ml,
                "딥러닝 예측값": y_pred_dl,
            })
        errors_df["머신러닝 오차"] = (errors_df["실제값"] - errors_df["머신러닝 예측값"]).abs()
        errors_df["딥러닝 오차"] = (errors_df["실제값"] - errors_df["딥러닝 예측값"]).abs()
        st.markdown("##### 📉 실제값과 예측값 오차 비교")
        st.dataframe(
            errors_df.style.format(precision=2).background_gradient(
                cmap='Reds', subset=["머신러닝 오차", "딥러닝 오차"]
            ),
            use_container_width=True, height=250, hide_index=True
        )
        best_model = comparison_df.loc[comparison_df['SSE'].astype(float).idxmin(), '모델']
        st.info(f"👉 두 모델의 SSE(오차 합계)를 비교해보세요. SSE가 더 작은 모델✨({best_model})이 데이터를 더 잘 설명합니다.")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[3]:
        st.subheader("4️⃣예측 및 시각화")
        st.markdown(pretty_title("🔍 예측값 비교", "#fce4ec", "#f8bbd0"), unsafe_allow_html=True)
        col_left, col_right = st.columns(2)
        with col_left:
            if input_mode == "수열 입력":
                next_label = f"예측하고 싶은 {y_name}의 {x_name}값"
                next_input_default = float(x[-1][0] + 1)
            else:
                next_label = f"예측하고 싶은 {x_name} 입력값"
                next_input_default = float(x[-1][0] + 1)
            next_input = st.number_input(
                next_label,
                value=float(next_input_default),
                step=1.0,
                format="%.2f"
            )
            x_next = np.array([[next_input]])
            X_next_trans = ml_poly.transform(x_next)
            pred_ml_next = ml_model.predict(X_next_trans)[0]
            x_next_scaled = scaler_x.transform(x_next)
            pred_dl_next_scaled = dl_model.predict(x_next_scaled)
            pred_dl_next = scaler_y.inverse_transform(pred_dl_next_scaled)[0][0]
            st.info(
                f"👉 {x_name}={next_input:.2f}에서 두 모델의 예측값을 비교해보세요."
            )
        with col_right:
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
                        <th>{x_name}={next_input:.2f}일 때  {y_name} 예측값</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>머신러닝</td>
                        <td>{pred_ml_next:.2f}</td>
                    </tr>
                    <tr>
                        <td>딥러닝</td>
                        <td>{pred_dl_next:.2f}</td>
                    </tr>
                </tbody>
            </table>
            """
            st.markdown(pred_table_html, unsafe_allow_html=True)
        st.subheader(f"📊 시각화 ({x_name} vs {y_name} 비교)")
        col1, col2, col3, col4 = st.columns(4)
        with col1: show_data = st.checkbox("입력 데이터", value=True, key="show_data")
        with col2: show_ml = st.checkbox("머신러닝", value=True, key="show_ml")
        with col3: show_dl = st.checkbox("딥러닝", value=True, key="show_dl")
        with col4: show_pred = st.checkbox("예측", value=True, key="show_pred")
        fig, ax = plt.subplots(figsize=(7, 5))
        if show_data:
            ax.scatter(
                x[:, 0], y,
                color='#1976d2', edgecolors='white', linewidths=1.8,
                s=90, marker='o', label='입력 데이터'
            )
        sorted_idx = np.argsort(x[:, 0])
        x_sorted = x[sorted_idx, 0]
        if show_ml:
            y_pred_ml_sorted = y_pred_ml[sorted_idx]
            ax.plot(
                x_sorted, y_pred_ml_sorted,
                color='#ff9800', linestyle='--', linewidth=2.5, label='머신러닝'
            )
            ax.text(
                0.38, 0.95,
                f"ML: $ {latex_equation_ml} $",
                transform=ax.transAxes,
                fontsize=12,
                verticalalignment='top'
            )
        if show_dl:
            y_pred_dl_sorted = y_pred_dl[sorted_idx]
            ax.plot(
                x_sorted, y_pred_dl_sorted,
                color='#43a047', linestyle='-', linewidth=2.5, label='딥러닝'
            )
            ax.text(
                0.38, 0.88,
                f"DL: $ {latex_equation_dl} $",
                transform=ax.transAxes,
                fontsize=12,
                verticalalignment='top'
            )
        if show_pred:
            ax.scatter(
                x_next[0][0], pred_ml_next,
                color='#d32f2f', edgecolors='black', s=130, marker='o', zorder=5, label='ML 예측'
            )
            ax.annotate(
                f"ML 예측: {pred_ml_next:.2f}",
                (x_next[0][0], pred_ml_next),
                textcoords="offset points",
                xytext=(5, -30),
                ha='left',
                color='#d32f2f',
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#d32f2f", lw=1)
            )
            ax.scatter(
                x_next[0][0], pred_dl_next,
                color='#f06292', edgecolors='black', s=130, marker='X', zorder=5, label='DL 예측'
            )
            ax.annotate(
                f"DL 예측: {pred_dl_next:.2f}",
                (x_next[0][0], pred_dl_next),
                textcoords="offset points",
                xytext=(5, 20),
                ha='left',
                color='#f06292',
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#f06292", lw=1)
            )
        ax.set_title(
            f"{x_name}와(과) {y_name}의 관계 및 예측\n",
            fontsize=15, fontweight='bold', color='#1976d2', pad=15
        )
        ax.set_xlabel(x_name, fontsize=13, fontweight='bold')
        ax.set_ylabel(y_name, fontsize=13, fontweight='bold')
        ax.grid(alpha=0.25)
        handles, labels = ax.get_legend_handles_labels()
        if labels:
            leg = ax.legend(
                fontsize=8, loc='upper left', frameon=True, fancybox=True, framealpha=0.88, shadow=True,
                borderpad=1, labelspacing=0.8
            )
            for line in leg.get_lines():
                line.set_linewidth(3.0)
        plt.tight_layout()
        st.pyplot(fig)
        st.subheader("📝 데이터 분석 및 예측 결과 작성")
        analysis_text = st.text_area("데이터 분석 및 예측 결과를 작성하세요.", key="analysis")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[4]:
        st.subheader("5️⃣ 결과 분석")
        st.markdown("""
            <style>
            .summary-table td, .summary-table th {
                padding: 8px 12px;
                border: 1px solid #ccc;
                font-size: 15px;
            }
            .summary-table th {
                background-color: #f0f4f8;
                color: #1565c0;
                font-weight: bold;
            }
            .summary-table {
                border-collapse: collapse;
                margin-top: 15px;
                width: 100%;
            }
            .highlight {
                background-color: #fff9c4;
                font-weight: bold;
                color: #d32f2f;
            }
            .equation {
                font-family: monospace;
                color: #424242;
            }
            </style>
        """, unsafe_allow_html=True)
        styled_table_html = f"""
        <table class='summary-table'>
            <thead>
                <tr><th>분석 항목</th><th>결과</th></tr>
            </thead>
            <tbody>
                <tr><td>입력 방식</td><td>{input_mode}</td></tr>
                <tr><td>머신러닝 함수식</td><td class='equation'> {latex_equation_ml} </td></tr>
                <tr><td>딥러닝 함수식</td><td class='equation'> {latex_equation_dl} </td></tr>
                <tr><td>예측값 ({x_name}={next_input:.2f}) - 머신러닝</td><td>{pred_ml_next:.2f}</td></tr>
                <tr><td>예측값 ({x_name}={next_input:.2f}) - 딥러닝</td><td>{pred_dl_next:.2f}</td></tr>
                <tr><td>SSE (머신러닝)</td><td>{sse_ml:.2f}</td></tr>
                <tr><td>SSE (딥러닝)</td><td>{sse_dl:.2f}</td></tr>
                <tr><td>정확도 (머신러닝)</td><td>{acc_ml:.1f}%</td></tr>
                <tr><td>정확도 (딥러닝)</td><td>{acc_dl:.1f}%</td></tr>
                <tr><td>더 적합한 모델 (SSE 기준)</td><td class='highlight'>{best_model}</td></tr>
            </tbody>
        </table>
        """
        st.markdown(styled_table_html, unsafe_allow_html=True)
        st.success(
            f"""🔎 **학습 Tip**  
        머신러닝과 딥러닝의 예측 결과를 비교해 보세요.  
        SSE(오차 합계)가 작은 모델이 데이터를 더 잘 설명합니다.  
        또한 정확도(설명력, R² %)도 참고하여 어떤 모델이 실제 데이터에 더 적합한지 판단해 보세요.  
        데이터의 개수, 분포, 함수의 복잡성 등이 모델의 성능에 영향을 줍니다."""
        )
        st.subheader("📖 탐구 결과 및 해석")
        interpretation_text = st.text_area("탐구 결과 및 해석을 작성하세요.", key="interpretation")
        if st.button("📥 PDF 다운로드"):
            pdf_bytes = create_pdf(
                st.session_state["student_info"],
                st.session_state.get("analysis", ""),
                st.session_state.get("interpretation", ""),
                comparison_df,  
                errors_df,
                latex_equation_ml,
                latex_equation_dl,
                pred_ml_next,
                pred_dl_next,
                x_name,
                y_name,
                next_input,
                fig=fig
            )
            st.download_button(
                label="📄 PDF 저장하기",
                data=pdf_bytes,
                file_name="AI_탐구보고서.pdf",
                mime="application/pdf"
            )
        st.markdown(
            "<div style='text-align: left; color:orange;'>✨실생활 데이터를 활용한 주제탐구 보고서를 작성하여 정해진 양식에 맞춰 제출하세요!</div>",
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
                <a href="https://docs.google.com/document/d/1qEsfs1vruu6x-Pfa_yJOyK2_thBLjv6knccVNNm2u5o/edit?usp=sharing"
                target="_blank"
                class="hw-submit-btn">
                    📤 데이터 기반 탐구 보고서 작성하기
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)