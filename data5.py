import streamlit as st
from streamlit_ace import st_ace
from fpdf import FPDF
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import tempfile
import pandas as pd
import io
import sys
import os

font_path = os.path.join(os.path.dirname(__file__), "font/NanumGothic.ttf")
fm.fontManager.addfont(font_path)  
font_name = fm.FontProperties(fname=font_path).get_name()
mpl.rc('font', family=font_name)   
mpl.rc('axes', unicode_minus=False) 

def code_runner(code_input):
    output_buffer = io.StringIO()
    try:
        sys.stdout = output_buffer
        exec_globals = {}
        exec(code_input, exec_globals)
        return output_buffer.getvalue() or "출력된 내용이 없습니다.", "success"
    except Exception as e:
        return f"{e.__class__.__name__}: {e}", "error"
    finally:
        sys.stdout = sys.__stdout__

def display_output(result, status):
    if status == "success":
        st.markdown(f"```bash\n{result}\n```")
    else:
        st.markdown("##### ❌ 실행 중 오류 발생")
        st.markdown(
            f"<pre style='color: red; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>{result}</pre>",
            unsafe_allow_html=True
        )

def code_block_columns(problem_number, starter_code, prefix=""):
    key = f"{prefix}{problem_number}"
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 📥 코드 입력")
        code_input = st_ace(
            value=starter_code,
            language='python',
            theme='github',
            height=220,
            key=f"{key}_editor"
        )
    with c2:
        st.markdown("##### 📤 실행 결과")
        if st.button("▶️ 코드 실행하기", key=f"{key}_run"):
            result, status = code_runner(code_input)
            display_output(result, status)

class ThemedPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=15)
        font_path = os.path.join(os.path.dirname(__file__), "font", "NanumGothic.ttf")
        self.add_font("Nanum", "", font_path, uni=True) 
        self._font_family = "Nanum"  
        self.footer_left = ""
        self.c_primary = (25, 118, 210)
        self.c_primary_lt = (227, 242, 253)
        self.c_border = (200, 200, 200)
        self.c_text_muted = (120, 120, 120)

    def header(self):
        self.set_fill_color(*self.c_primary)
        self.rect(0, 0, self.w, 20, 'F')
        self.set_xy(10, 6)
        self.set_text_color(255, 255, 255)
        self.set_font(self._font_family, '', 16)
        self.cell(0, 10, "나만의 수열의 합 문제 만들기", ln=1, align='C')
        self.set_text_color(33, 33, 33)
        self.ln(15)

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

def create_custom_pdf(student_info, problem_text, code, result,
                      alg_decomp="", alg_steps=None, alg_validation=""):
    pdf = ThemedPDF()
    pdf.set_font("Helvetica", '', 12)
    pdf.footer_left = f"{student_info.get('school','')} • {student_info.get('name','')}"
    pdf.add_page()
    pdf.h2("👤 학생 정보")
    pdf.p(f"학교: {student_info.get('school','')}")
    pdf.p(f"학번: {student_info.get('id','')}")
    pdf.p(f"이름: {student_info.get('name','')}")
    pdf.p(f"작성일: {datetime.now().strftime('%Y-%m-%d')}")
    pdf.h2("📝 문제 설명")
    pdf.p(problem_text if problem_text else "작성된 문제 설명 없음")
    pdf.h2("알고리즘적 사고")
    pdf.p("문제 분해:")
    pdf.p(alg_decomp)
    pdf.p("절차화:")
    pdf.p("\n".join([f"{i+1}. {s}" for i, s in enumerate(alg_steps or []) if s.strip()]))
    pdf.p("검증 및 일반화:")
    pdf.p(alg_validation)
    pdf.h2("💻 작성 코드")
    pdf.p(code)
    pdf.h2("📤 실행 결과")
    pdf.p(result)
    return bytes(pdf.output(dest='S'))

# ✅ 메인 화면
def show():
    st.header("🗓️ Day 5")
    st.subheader("파이썬으로 수열의 합 다루기")
    st.write("수열의 각 항을 더한 값을 ‘수열의 합’이라 합니다. 파이썬 코드로 직접 구현해 봅시다.")
    st.divider()
    st.video("https://youtu.be/aB2iT8JIblQ")
    st.subheader("📌 학습 목표")
    st.write("""
    - 등차수열과 등비수열의 합 공식을 이해할 수 있다.
    - 파이썬으로 등차수열 및 등비수열의 합을 계산할 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    tabs = st.tabs([
        "1️⃣ [개념] 등차수열의 합",
        "2️⃣ [개념] 등비수열의 합",
        "3️⃣ [실습] 코딩",
        "4️⃣ [프로젝트] 문제 만들기",
        "5️⃣ [수준별 문제]"
    ])

    with tabs[0]:
        st.subheader("ℹ️ 수열의 합")
        st.write("""
                수열의 항을 순서대로 모두 더한 값을 수열의 합이라 합니다. 대표적으로 수열의 합은 등차수열과 등비수열에서 자주 사용됩니다
                """)
        st.divider()
        st.subheader("ℹ️ 등차수열의 합")
        st.write(""" 
                - **등차수열의 합**: 첫째 항 $a_1$, 공차 $d$, $n$항까지의 합 $S_n$는
                """)
        st.latex(r"S_n = \frac{n}{2}(a_1 + a_n) = \frac{n}{2}\bigl(2a_1 + (n-1)d\bigr)")
        st.write("- 예) $a_1=3$, $d=2$일 때")
        st.latex(r"S_{10} = \frac{10}{2}\bigl(2\times3 + (10-1)\times2\bigr) = 120")
        st.info("""
        등차수열의 합은 **직사각형의 절반**으로 이해할 수 있습니다. 밑변이 항의 개수 $n$, 높이가 $a_1 + a_n$인 직사각형을 생각하면, 그 넓이의 절반이 바로 수열의 합이 됩니다.
        """)
        st.divider()
        st.subheader("📊 수열의 합 시각화")
        c1, c2, c3 = st.columns(3)
        with c1:
            a1 = st.number_input("첫째 항 (a)", value=3)
        with c2:
            d = st.number_input("공차 (d)", value=2)
        with c3:
            n = st.number_input("항의 개수 (n)", min_value=2, max_value=50, value=6, step=1)
        terms = [a1 + i*d for i in range(n)]
        an = terms[-1]
        Sn = sum(terms)
        st.latex(rf"S_n = \frac{{n}}{{2}}(a_1 + a_n) = \frac{{{n}}}{{2}}({a1}+{an}) = {Sn}")
        c1, c2 = st.columns(2)
        with c1:
            show_sequence = st.checkbox("📊 수열 보기", value=True)
        with c2:
            show_sum = st.checkbox("🟧 수열의 합(직사각형) 보기", value=True)
        fig, ax = plt.subplots(figsize=(7,4))
        if show_sequence:
            ax.bar(np.arange(0, n), terms, width=1, align="edge", 
                color="skyblue", edgecolor="black", label="수열의 항")
        if show_sum:
            rect_x = [0, n, n, 0, 0]
            rect_y = [0, 0, a1+an, a1+an, 0]
            ax.plot(rect_x, rect_y, color="red", linestyle="--", linewidth=2)
            ax.fill_between([0, n], 0, a1+an, color="orange", alpha=0.2, label="직사각형 (합의 2배)")
            ax.plot([0, n], [0, a1+an], color="purple", linestyle="-.", linewidth=2, label="대각선 (절반)")
            ax.annotate(
                f"(밑변) = n = {n}",
                xy=(n/2, 2),
                ha="center", va="top",
                fontsize=11, color="black"
            )
            ax.annotate(
                f"(높이) = a+a_n ={a1+an}",
                xy=(0.4, (a1+an)/2),
                ha="right", va="center",
                fontsize=11, color="black", rotation=90
            )
        ax.set_xlim(0, n)
        ax.set_ylim(0, a1+an+5)
        ax.set_xlabel("항 번호 (n)")
        ax.set_ylabel("a_n (값)")
        ax.set_title("등차수열의 합 시각화")
        ax.legend(loc="upper left")
        st.pyplot(fig)
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("ℹ️ 등비수열의 합")
        st.write(""" 
        - **등비수열의 합**: 첫째 항 $a_1$, 공비 $r$, $n$항까지의 합 $S_n$는
        """)
        st.latex(r"S_n = a_1 \times \frac{r^n -1}{r-1} \quad (r \neq 1)")
        st.info("""
        등비수열의 합은 $S_n$ 과 $rS_n$ 을 비교해 **항들을 소거**하면서 유도합니다.  
        대부분의 항이 사라지고 $S_n(r-1) = a_1(r^n - 1)$ 이 남습니다.
        """)
        c1, c2, c3 = st.columns(3)
        with c1:
            a1 = st.number_input("첫째 항 (a₁)", value=2, key="geo_a1")
        with c2:
            r = st.number_input("공비 (r)", value=3, key="geo_r")
        with c3:
            n = st.number_input("항의 개수 (n)", min_value=2, max_value=8, value=5, step=1, key="geo_n")
        terms_Sn = [f"{a1}" if i==0 else f"{a1}·{r}^{i}" for i in range(n)]
        terms_rSn = [f"{a1}·{r}^{i}" for i in range(1, n+1)]
        step = st.slider("소거 단계 진행", 0, n-1, 0, key="geo_step")
        Sn_display, rSn_display = terms_Sn.copy(), terms_rSn.copy()
        for i in range(step):
            idx_sn = i + 1   
            idx_rsn = i     
            Sn_display[idx_sn] = f"\\cancel{{{Sn_display[idx_sn]}}}"
            rSn_display[idx_rsn] = f"\\cancel{{{rSn_display[idx_rsn]}}}"
        st.latex(rf"S_n = {' + '.join(Sn_display)}")
        st.latex(rf"rS_n = {' + '.join(rSn_display)}")
        if step == 0:
            st.info("👉 아직 소거 전: 전체 항목을 보여줍니다.")
        elif step < n-1:
            st.warning(f"👉 오른쪽에서 왼쪽으로 {step}쌍의 항이 소거되었습니다.")
        else:
            st.success(rf"🎉 모든 공통항 소거 완료 → $S_n(r-1) = a_1(r^n - 1)$ → $S_n = {a1}\cdot \frac{{{r}^{n}-1}}{{{r}-1}}$")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
            
    with tabs[2]:
        st.markdown("###### 💻 :blue[[예제 1]] 첫째 항이 `3`, 공차가 `2`인 등차수열의 첫 `10`항까지 합을 구하는 코드를 작성하세요.")
        st.code("a = 3\nd = 2\nS_n = a\nfor i in range(1,10):\n    next_val = a + i * d\n    S_n = S_n + next_val\nprint(S_n)\n")
        st.divider()
        st.markdown("###### 💻 :blue[[문제 1]] 첫째 항이 `2`, 공차가 `5`인 등차수열의 첫 `20`항까지 합을 구하는 코드를 작성하세요.")
        with st.expander("💡 힌트 보기"):
            st.markdown("각 항을 구해서 하나씩 더하는 방법입니다. `a + i*d`를 이용하세요")
        with st.expander("💡 정답 보기"):
            st.code("""
        a = 2
        d = 5
        S_n = a
        for i in range(1, 20):
            next_val = a + i * d
            S_n = S_n +next_val
        print(S_n)
        # 출력: 990
        """)
        code_block_columns(1,"a = 2\nd = 5\nS_n = a\n# 여기에 for문을 이용해 합을 계산하세요.\n", prefix="d5_")
        st.markdown("###### 💻 :blue[[예제 2]] 첫째 항이 `3`, 공비가 `2`인 등비수열의 첫 `10`항까지 합을 구하는 코드를 작성하세요.")
        st.code("""\
        a = 3
        r = 2
        S_n = a
        for i in range(1, 10):
            next_val = a * (r ** i)
            S_n = S_n + next_val
        print(S_n)
        """)
        st.markdown("###### 💻 :blue[[문제 2]] 첫째 항이 `2`, 공비가 `5`인 등비수열의 첫 `5`항까지 합을 구하는 코드를 작성하세요.")
        with st.expander("💡 힌트 보기"):
            st.markdown("각 항을 구해서 하나씩 더하는 방법입니다. `a * (r**i)`를 이용하세요.")
        with st.expander("💡 정답 보기"):
            st.code("""\
        a = 2
        r = 5
        S_n = a
        for i in range(1, 5):
            next_val = a * (r ** i)
            S_n = S_n + next_val
        print(S_n)
        # 출력: 1562
        """)
        code_block_columns(2, 
        "a = 2\nr = 5\nS_n = a\n# 여기에 for문을 이용해 합을 계산하세요.\n", prefix="d5_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
 
    with tabs[3]:
        st.markdown("##### 💻 :blue[[프로젝트]] 나만의 수열의 합 문제 만들기")
        student_problem = st.text_area("📝 문제 설명 입력",
                                    value=st.session_state.get("student_problem_text_d5", ""))
        st.session_state["student_problem_text_d5"] = student_problem
        st.markdown("#### 🗂️알고리즘적 사고 단계")
        st.markdown("#####  1️⃣ 문제 분해")
        st.markdown("문제에 필요한 입력(조건)과 출력(답) 및 제약(규칙)을 정리하세요.")
        alg_decomp = st.text_area("✍️문제에 필요한 입력(조건)과 출력(답)을 정리하세요.",key="alg_decomp_d5")
        st.markdown("##### 2️⃣ 절차화")
        st.markdown("문제해결 과정을 차례대로 나열하세요.")
        step_count = st.number_input("단계 수", min_value=2, max_value=8, value=3, step=1,
                                    key="alg_step_count_d5")
        alg_steps = []
        for i in range(1, step_count + 1):
            step = st.text_input(f"단계 {i}", key=f"alg_step_{i}_d5")
            alg_steps.append(step)
        st.markdown("#####  3️⃣ 검증 및 일반화")
        st.markdown("실행 결과와 정답을 비교해보며 코드를 점검해보세요.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 📄 내가 설계한 코드(미리보기)")
            pseudo = "\n".join([f"{i+1}. {line}" for i, line in enumerate(alg_steps) if line.strip()])
            st.code(pseudo, language="text")
        with c2:
            st.markdown("#### 💻 코드 작성하기")
            user_code = st_ace(
                value=st.session_state.get("custom_code_d5", "# 여기에 로직을 작성하세요\n"),
                language="python",
                theme="github",
                height=250,
                key="ace_custom_d5"
            )
            st.session_state["custom_code_d5"] = user_code 
            if st.button("▶️ 실행 결과 확인", key="run_d5"):
                result, status = code_runner(user_code)
                display_output(result, status)
                st.session_state["last_result"] = result
                st.session_state["last_status"] = status
        alg_validation = st.text_area("✍️실행 결과를 검증하고 일반화하는 방법을 서술하세요.",key="alg_validation_d5")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            school = st.text_input("학교명", value=st.session_state.get("pdf_school_d5", ""), key="pdf_school_d5")
        with col2:
            student_id = st.text_input("학번", value=st.session_state.get("pdf_id_d5", ""), key="pdf_id_d5")
        with col3:
            student_name = st.text_input("이름", value=st.session_state.get("pdf_name_d5", ""), key="pdf_name_d5")

        student_info = {"school": school, "id": student_id, "name": student_name}
        if st.button("📥 PDF 저장하기", key="save_pdf_d5"):
            result = st.session_state.get("last_result", "실행 결과 없음")
            pdf_bytes = create_custom_pdf(student_info, student_problem, user_code, result,
                                        alg_decomp, alg_steps, alg_validation)
            st.download_button(
                label="📄 PDF 다운로드",
                data=pdf_bytes,
                file_name=f"Day5_Report_{student_name}.pdf",
                mime="application/pdf"
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
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)            

    with tabs[4]:
        st.markdown("##### 🌈 :rainbow[[수준별 문제]] 수열의 합 도전")
        sum_level = st.radio(
            "난이도를 선택하세요!",
            ("하", "중", "상"),
            horizontal=True,
            key="d5_sum_level"
        )
        if sum_level == "하":
            q_title = "등차수열의 합"
            q_problem = "초항이 1, 공차가 3인 등차수열의 첫 6항까지의 합을 구하세요."
            starter_code = (
                "a = 1\n"
                "d = 3\n"
                "n = 6\n"
                "S_n = a\n"
                "# for문을 이용해 합을 구하세요\n"
            )
            answer_code = (
                "a = 1\n"
                "d = 3\n"
                "n = 6\n"
                "S_n = a\n"
                "for i in range(1, n):\n"
                "    next_val = a + i * d\n"
                "    S_n = S_n + next_val\n"
                "print(S_n)"
            )
        elif sum_level == "중":
            q_title = "등비수열의 합"
            q_problem = "초항이 2, 공비가 4인 등비수열의 첫 5항까지의 합을 구하세요."
            starter_code = (
                "a = 2\n"
                "r = 4\n"
                "n = 5\n"
                "S_n = a\n"
                "# for문을 이용해 합을 구하세요\n"
            )
            answer_code = (
                "a = 2\n"
                "r = 4\n"
                "n = 5\n"
                "S_n = a\n"
                "for i in range(1, n):\n"
                "    next_val = a * (r ** i)\n"
                "    S_n = S_n + next_val\n"
                "print(S_n)"
            )
        else:
            q_title = "등차&등비수열 합 응용"
            q_problem = (
                "초항이 5, 공차가 2인 등차수열과 초항이 1, 공비가 3인 등비수열의 "
                "각각 첫 8항의 합을 구하고, 두 합의 차를 출력하세요."
                "(절댓값: `abs(S1 - S2)`는 S1과 S2의 차이의 크기를 의미합니다)"
            )
            starter_code = (
                "a1 = 5\n"
                "d = 2\n"
                "n = 8\n"
                "S1 = a1\n"
                "a2 = 1\n"
                "r = 3\n"
                "S2 = a2\n"
                "# for문 2개를 이용해 각각 합을 구하세요\n"
            )
            answer_code = (
                "a1 = 5\n"
                "d = 2\n"
                "n = 8\n"
                "S1 = a1\n"
                "for i in range(1, n):\n"
                "    S1 += a1 + i*d\n"
                "a2 = 1\n"
                "r = 3\n"
                "S2 = a2\n"
                "for i in range(1, n):\n"
                "    S2 += a2 * (r ** i)\n"
                "print('합의 차:', abs(S1 - S2))"
            )
        st.markdown(f"**[{sum_level}] {q_title}**  \n{q_problem}")
        with st.expander("💡 정답 코드 보기"):
            st.code(answer_code, language='python')
        code_block_columns("level", starter_code, prefix=f"d5_sel_{sum_level}_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)