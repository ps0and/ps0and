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

# ---------- 한글 폰트 설정 ----------
try:
    font_path = os.path.join(os.path.dirname(__file__), "font", "NanumGothic.ttf")
    fm.fontManager.addfont(font_path)  # 🔹 폰트 등록
    font_name = fm.FontProperties(fname=font_path).get_name()
    mpl.rc('font', family=font_name)    # 🔹 그래프 기본 폰트 변경
    mpl.rc('axes', unicode_minus=False) # 🔹 마이너스 깨짐 방지
except Exception as e:
    st.warning(f"⚠️ 한글 폰트 로드 실패: {e}. 기본 폰트로 진행합니다.")
    
def code_runner(code_input):
    output_buffer = io.StringIO()
    result, status = "", "success"
    try:
        sys.stdout = output_buffer
        exec_globals = {}
        exec(code_input, exec_globals)
        result = output_buffer.getvalue() or "출력된 내용이 없습니다."
    except Exception as e:
        result = f"{e.__class__.__name__}: {e}"
        status = "error"
    finally:
        sys.stdout = sys.__stdout__
    return result, status

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
# ---------- PDF 클래스 ----------
class ThemedPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=15)

        # ✅ 한글 폰트 경로 (프로젝트 내부 font 폴더에 넣어주세요)
        font_path = os.path.join(os.path.dirname(__file__), "font", "NanumGothic.ttf")
        self.add_font("Nanum", "", font_path, uni=True)  # 유니코드 폰트 등록
        self._font_family = "Nanum"  # 기본 폰트를 나눔고딕으로 지정
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
        self.cell(0, 10, "나만의 등비수열 문제 만들기", ln=1, align='C')
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

# ---------- PDF 생성 함수 ----------
def create_custom_pdf(student_info, problem_text, code, result):
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

    pdf.h2("💻 작성 코드")
    pdf.p(code)

    pdf.h2("📤 실행 결과")
    pdf.p(result)

    return bytes(pdf.output(dest='S'))

# ✅ 메인 화면
def show():
    st.header("🗓️ Day 4")
    st.subheader("수열: 등비수열")
    st.write("등비수열을 파이썬 코드로 직접 구현해 봅니다.")
    st.divider()
    st.video("https://youtu.be/kJPv5EkTx1E")
    st.subheader("📌 학습 목표")
    st.write("""
    - 등비수열의 일반항 개념을 이해할 수 있다.
    - 파이썬으로 등비수열을 구현하고 특정 조건을 만족하는 항을 찾을 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
   
    tabs = st.tabs([
        "1️⃣ [개념] 등비수열",
        "2️⃣ [실습] 코딩",
        "3️⃣ [프로젝트] 문제 만들기",
        "4️⃣ [수준별 문제]"

    ])
    with tabs[0]:
        st.subheader("ℹ️ 등비수열 (Geometric Sequence)")
        st.write("""
        - **등비수열**: 인접한 두 항의 비(공비)가 일정한 수열  
        - 첫째 항을 $a_1$, 공비를 $r$이라 하면, n번째 항 $a_n$은
        $$
        a_n = a_1 r^{n-1}
        $$
        - 예) $a_1=3$, $r=2$일 때 수열은 $[3, 6, 12, 24, \dots]$
        """)
        st.divider()

        st.subheader("📊 등비수열 비교")
        # 두 열로 입력
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ➡️ 수열 1")
            g_a1_1 = st.number_input("첫째 항 (a₁)", value=3, step=1, key="g_seq1_a1")
            r1 = st.number_input("공비 (r)", value=2, step=1, key="g_seq1_r")
            st.latex(rf"a_n = {g_a1_1}\times({r1})^{{n-1}}")

        with col2:
            st.markdown("### ➡️ 수열 2")
            g_a1_2 = st.number_input("첫째 항 (a₁)", value=5, step=1, key="g_seq2_a1")
            r2 = st.number_input("공비 (r)", value=3, step=1, key="g_seq2_r")
            st.latex(rf"a_n = {g_a1_2}\times({r2})^{{n-1}}")

        # 공통으로 몇 항까지 비교할지 선택
        g_n_max = st.slider("몇 번째 항까지 비교할까요?", min_value=5, max_value=10, value=4, key="g_n_max")

        # 수열 생성
        g_n_values = np.arange(1, g_n_max+1)
        g_y1 = [g_a1_1 * (r1 ** (n-1)) for n in g_n_values]
        g_y2 = [g_a1_2 * (r2 ** (n-1)) for n in g_n_values]

        # --------------------
        # 📈 그래프 시각화
        # --------------------
        col1, col2 = st.columns(2)
        with col1: g_show_seq1 = st.checkbox("수열 1 보이기", value=True, key="g_show1")
        with col2: g_show_seq2 = st.checkbox("수열 2 보이기", value=True, key="g_show2")

        fig, ax = plt.subplots(figsize=(7, 5))

        if g_show_seq1:
            ax.plot(
                g_n_values, g_y1,
                marker="o", markersize=8, markeredgecolor="white", markeredgewidth=1.5,
                color="#1976d2", linewidth=2.2,
                label=fr"수열1: $a_n = {g_a1_1}\times({r1})^{{n-1}}$", zorder=3
            )

        if g_show_seq2:
            ax.plot(
                g_n_values, g_y2,
                marker="s", markersize=8, markeredgecolor="white", markeredgewidth=1.5,
                color="#d32f2f", linewidth=2.2,
                label=fr"수열2: $a_n = {g_a1_2}\times({r2})^{{n-1}}$", zorder=3
            )

        # 두 수열 차이 점선
        if g_show_seq1 and g_show_seq2:
            for n, v1, v2 in zip(g_n_values, g_y1, g_y2):
                ax.plot([n, n], [v1, v2], "--", color="gray", alpha=0.6, linewidth=1.2)

        # 그래프 꾸미기
        ax.set_title("두 등비수열 비교", fontsize=16, fontweight="bold", color="#1976d2", pad=15)
        ax.set_xlabel("n (항 번호)", fontsize=13, fontweight="bold")
        ax.set_ylabel("a_n (값)", fontsize=13, fontweight="bold")
        ax.grid(alpha=0.25, linestyle="--")

        handles, labels = ax.get_legend_handles_labels()
        if labels:
            leg = ax.legend(fontsize=9, loc="upper left",
                            frameon=True, fancybox=True, shadow=True, framealpha=0.9)
            for line in leg.get_lines():
                line.set_linewidth(3.0)

        plt.tight_layout()
        st.pyplot(fig)

        # --------------------
        # 📋 비교 표
        # --------------------
        g_df = pd.DataFrame({
            "항 번호 (n)": g_n_values,
            f"수열1 (a₁={g_a1_1}, r={r1})": g_y1,
            f"수열2 (a₁={g_a1_2}, r={r2})": g_y2,
            "차이 (수열2-수열1)": np.array(g_y2) - np.array(g_y1)
        })

        st.markdown("### 📋 비교 표")

        st.dataframe(
            g_df.style.format(precision=2).background_gradient(
                cmap="Blues", subset=["차이 (수열2-수열1)"]
            ),
            use_container_width=True,
            hide_index=True,
            height=180
        )
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)



    with tabs[1]:
        st.subheader("ℹ️ 수열과 리스트의 공통점")

        st.write("""
        - 둘 다 순서가 있는 값들의 나열이며, 인덱스로 각 항을 참조할 수 있습니다.  
        - 수열의 $a_n$은 리스트의 `list[n-1]`과 대응됩니다.  
        - 리스트의 `list[-1]`은 마지막 항을 의미합니다.
        """)

        st.markdown("###### 💻 :blue[[예제 1]] 첫째 항이 `3`, 공비가 `2`인 등비수열을 `10`항까지 출력하세요.")
        st.code("""
    a = 3
    r = 2
    seq = [a]
    for i in range(1, 10):
        next_val = seq[-1] * r
        seq.append(next_val)
    print(seq)
    # 출력: [3, 6, 12, 24, 48, 96, 192, 384, 768, 1536]
    """)
        st.divider()

        st.markdown("###### 💻 :blue[[문제 1]] 첫째 항이 `2`, 공비가 `5`인 등비수열을 `5`항까지 출력하세요.")
        with st.expander("💡 힌트 보기"):
            st.markdown("`for`문과 `append()`를 활용하세요. 새로운 항은 `seq[-1] * r`로 계산합니다.")
        with st.expander("💡 정답 보기"):
            st.code("""
    a = 2
    r = 5
    seq = [a]
    for i in range(1, 5):
        next_val = seq[-1] * r
        seq.append(next_val)
    print(seq)
    """)
        code_block_columns(1, "a=2\nr=5\nseq=[a]\n# 여기에 for문 작성\nprint(seq)", prefix="d4_")
        st.markdown("###### 💻 :blue[[문제 2]] 첫째 항이 `3`, 공비가 `2`인 등비수열에서 처음으로 600이상이 되는 항은 제몇 항인지 출력하세요.")
        with st.expander("💡 힌트 보기"):
            st.markdown("`for`문과 `if next_val > 600:`를 활용해보세요. 음수가 되는 순간 `i+1`을 출력하고 `break`하세요.")
        with st.expander("💡 정답 보기"):
            st.code("""
    a = 3
    r = 2
    seq = [a]
    for i in range(1, 100):
        next_val = seq[-1] * r
        seq.append(next_val)
        if next_val >= 600:
            print(i+1)
            break
    """)
        code_block_columns(2, "a=3\nr=2\nseq=[a]\n# 여기에 for문 작성", prefix="d4_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("##### 💻 :blue[[프로젝트]] 나만의 등비수열 문제 만들기")

        # 📝 문제 설명 입력
        student_problem = st.text_area(
            "📝 문제 설명 입력",
            value=st.session_state.get("student_problem_text", "")
        )
        st.session_state["student_problem_text"] = student_problem

        # 💻 코드 입력
        user_code = st_ace(
            value=st.session_state.get("custom_code", "# 여기에 로직을 작성하세요\n"),
            language="python",
            theme="github",
            height=250,
            key="ace_custom"
        )
        st.session_state["custom_code"] = user_code

        # ▶️ 실행 결과 확인 버튼
        if st.button("▶️ 실행 결과 확인"):
            result, status = code_runner(user_code)
            display_output(result, status)

            # 실행 결과를 세션에 저장
            st.session_state["last_result"] = result
            st.session_state["last_status"] = status

        # 학생 정보 입력 (세션 유지)
        col1, col2, col3 = st.columns([2, 1, 1])  # 비율 2:1:1
        with col1:
            school = st.text_input("학교명", value=st.session_state.get("pdf_school_d3", ""), key="pdf_school_d3")
        with col2:
            student_id = st.text_input("학번", value=st.session_state.get("pdf_id_d3", ""), key="pdf_id_d3")
        with col3:
            student_name = st.text_input("이름", value=st.session_state.get("pdf_name_d3", ""), key="pdf_name_d3")

        student_info = {"school": school, "id": student_id, "name": student_name}

        # 📥 PDF 저장 버튼
        if st.button("📥 PDF 저장하기"):
            # 세션에 저장된 결과 불러오기
            result = st.session_state.get("last_result", "실행 결과 없음")
            pdf_bytes = create_custom_pdf(student_info, student_problem, user_code, result)
            st.download_button(
                label="📄 PDF 다운로드",
                data=pdf_bytes,
                file_name=f"Day3_Report_{student_name}.pdf",
                mime="application/pdf"
            )
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("##### 🌈 :rainbow[[수준별 문제]] 등비수열 도전")

        geo_level = st.radio(
            "난이도를 선택하세요!",
            ("하", "중", "상"),
            horizontal=True,
            key="d4_geo_level"
        )

        if geo_level == "하":
            q_title = "n번째 등비수열 항 구하기"
            q_problem = "초항이 2, 공비가 3인 등비수열의 6번째 항을 출력해보세요."
            starter_code = (
                "a = 2\n"
                "r = 3\n"
                "n = 6\n"
                "# 여기에 코드 작성\n"
            )
            answer_code = (
                "a = 2\n"
                "r = 3\n"
                "n = 6\n"
                "an = a * (r ** (n-1))\n"
                "print(an)"
            )
        elif geo_level == "중":
            q_title = "리스트로 등비수열 만들기"
            q_problem = "초항이 5, 공비가 2인 등비수열의 앞 7개 항을 리스트로 만들어 출력하세요."
            starter_code = (
                "a = 5\n"
                "r = 2\n"
                "seq = [a]\n"
                "# 여기에 코드 작성\n"
            )
            answer_code = (
                "a = 5\n"
                "r = 2\n"
                "seq = [a]\n"
                "for i in range(1, 7):\n"
                "    seq.append(seq[-1]*r)\n"
                "print(seq)"
            )
        else:  # 상
            q_title = "1000을 넘는 첫 번째 항 찾기"
            q_problem = "초항이 4, 공비가 3인 등비수열에서 처음으로 1000을 넘는 항의 번호를 출력하세요."
            starter_code = (
                "a = 4\n"
                "r = 3\n"
                "seq = [a]\n"
                "# for, if, break로 작성\n"
            )
            answer_code = (
                "a = 4\n"
                "r = 3\n"
                "seq = [a]\n"
                "for i in range(1, 100):\n"
                "    next_val = seq[-1] * r\n"
                "    seq.append(next_val)\n"
                "    if next_val > 1000:\n"
                "        print(i + 1)\n"
                "        break\n"
            )

        st.markdown(f"**[{geo_level}] {q_title}**  \n{q_problem}")

        with st.expander("💡 정답 코드 보기"):
            st.code(answer_code, language='python')

        code_block_columns("level", starter_code, prefix=f"d4_sel_{geo_level}_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
