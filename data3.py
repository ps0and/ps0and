import streamlit as st
from streamlit_ace import st_ace
from fpdf import FPDF
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import pandas as pd
import io
import sys
import os

# 코드 실행 함수
def code_runner(code_input):
    output_buffer = io.StringIO()
    result = ""
    status = "success"
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

# 출력 함수
def display_output(result, status):
    if status == "success":
        st.markdown(f"```bash\n{result}\n```")
    else:
        st.markdown("#### ❌ 실행 중 오류 발생")
        st.markdown(
            f"<pre style='color: red; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>{result}</pre>",
            unsafe_allow_html=True
        )

# 리팩토링된 코드 블록 함수 (세션 상태 저장 X)
def code_block_columns(problem_number, starter_code, prefix=""):
    key_prefix = f"{prefix}{problem_number}"
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 📥 코드 입력")
        code_input = st_ace(
            value=starter_code,
            language='python',
            theme='github',
            height=220,
            key=f"{key_prefix}_editor"
        )
    with c2:
        st.markdown("##### 📤 실행 결과")
        if st.button("▶️ 코드 실행하기", key=f"{key_prefix}_run"):
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
        self.cell(0, 10, "나만의 등차수열 문제 만들기", ln=1, align='C')
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
    st.header("🗓️ Day 3")
    st.subheader("수열: 등차수열")
    st.write("등차수열을 파이썬 코드로 직접 구현해 봅니다.")
    st.divider()
    st.video("https://youtu.be/D17z97cYUxw")
    st.subheader("📌 학습 목표")
    st.write("""
    - 등차수열의 일반항 개념을 이해할 수 있다.
    - 파이썬으로 등차수열을 구현하고 특정 조건을 만족하는 항을 찾을 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    tabs = st.tabs([
        "1️⃣ [개념] 수열",
        "2️⃣ [개념] 등차수열",
        "3️⃣ [실습] 코딩",
        "4️⃣ [프로젝트] 문제 만들기",
        "5️⃣ [수준별 문제]"

    ])

    with tabs[0]:
        st.subheader("ℹ️ 수열 (Sequence)")
        st.write("""
        - **정의**: 특정한 규칙 또는 대응에 따라 순서대로 나열된 수들의 열
        - 수열 $\{a_n\}$은 자연수 집합 $\mathbb{N}$을 정의역으로, 어떤 값의 집합 $S$를 공역으로 하는 함수
        $$
        a: \mathbb{N} \mapsto S, \quad n \mapsto a(n) = a_n
        $$
        - $a_n$: n번째 항
        """)
        st.divider()

        st.subheader("📊 수열 시각화")
        # 📝 일반항 입력
        formula = st.text_input("n에 관한 수열 일반항을 입력하세요 (예: 2 * n+1, n ** 2)", value="2*n+1")

        # 🔢 최대 항 번호
        n_max = st.slider("몇 번째 항까지 볼까요?", min_value=5, max_value=30, value=10)

        # 👉 수열 계산
        try:
            n_values = np.arange(1, n_max+1)
            # eval을 안전하게 실행하기 위해 n만 허용
            y_values = [eval(formula, {"n": int(n)}) for n in n_values]

            # 결과 표시
            st.write(f"👉 생성된 수열: {y_values}")
            fig, ax = plt.subplots(figsize=(7, 5))

            # 점 + 선
            ax.scatter(
                n_values, y_values,
                color='#1976d2', edgecolors='white', linewidths=1.5,
                s=100, marker='o', label="수열 값 (aₙ)", zorder=3
            )
            ax.plot(
                n_values, y_values,
                color='#ff9800', linestyle='--', linewidth=2.2,
                label="수열 추세선", zorder=2
            )

            # 그래프 제목 & 라벨
            ax.set_title(
                f"수열 시각화: $a_n = {formula}$",
                fontsize=15, fontweight='bold', color='#1976d2', pad=15
            )
            ax.set_xlabel("항 번호 (n)", fontsize=13, fontweight='bold')
            ax.set_ylabel("수열 값 (a_n)", fontsize=13, fontweight='bold')

            # 격자 + 범례
            ax.grid(alpha=0.25, linestyle="--")
            leg = ax.legend(
                fontsize=9, loc='upper left', frameon=True, fancybox=True, framealpha=0.88, shadow=True,
                borderpad=1, labelspacing=0.8
            )
            for line in leg.get_lines():
                line.set_linewidth(3.0)

            plt.tight_layout()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ 식을 계산할 수 없습니다: {e}")

        col1, col2 = st.columns(2)
        with col1:
            query_n = st.number_input("항 번호 (n)", min_value=1, value=1, step=1)

        with col2:
            try:
                query_val = eval(formula, {"n": int(query_n)})
                st.metric(label=f"제 {int(query_n)}항", value=query_val)
            except Exception:
                st.error("❌ 올바른 수식을 입력해주세요.")

        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
        
    with tabs[1]:
        st.subheader("ℹ️ 등차수열 (Arithmetic Sequence)")
        st.write("""
        - **등차수열**: 이웃한 두 항의 차이가 일정한 수열
        -  첫째 항을 $a_1$, 공차를 d라 하면, n번째 항 $a_n$:
        $$
        a_n = a_1 + (n - 1) d
        $$
        - ex) $a_1$ = 3, d = 2일 때 수열은 [3, 5, 7, 9, ...]
        와 같이 생성됨.
        """)
        st.divider()

        st.subheader("📊 등차수열 비교")

        # 두 열로 입력
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ➡️ 수열 1")
            a1_1 = st.number_input("첫째 항 (a₁)", value=3, step=1, key="seq1_a1")
            d1 = st.number_input("공차 (d)", value=2, step=1, key="seq1_d")
            st.latex(rf"a_n = {a1_1} + (n-1)\times{d1}")

        with col2:
            st.markdown("### ➡️ 수열 2")
            a1_2 = st.number_input("첫째 항 (a₁)", value=5, step=1, key="seq2_a1")
            d2 = st.number_input("공차 (d)", value=3, step=1, key="seq2_d")
            st.latex(rf"a_n = {a1_2} + (n-1)\times{d2}")

        # 공통으로 몇 항까지 비교할지 선택
        n_max = st.slider("몇 번째 항까지 비교할까요?", min_value=5, max_value=30, value=10)

        # 수열 생성
        n_values = np.arange(1, n_max+1)
        y1 = [a1_1 + (n-1)*d1 for n in n_values]
        y2 = [a1_2 + (n-1)*d2 for n in n_values]

        # --------------------
        # 📈 그래프 시각화
        # --------------------
        col1, col2 = st.columns(2)
        with col1: show_seq1 = st.checkbox("수열 1 보이기", value=True)
        with col2: show_seq2 = st.checkbox("수열 2 보이기", value=True)

        fig, ax = plt.subplots(figsize=(7, 5))

        if show_seq1:
            ax.plot(
                n_values, y1,
                marker="o", markersize=8, markeredgecolor="white", markeredgewidth=1.5,
                color="#1976d2", linewidth=2.2,
                label=fr"수열1: $a_n = {a1_1} + (n-1)\times{d1}$", zorder=3
            )

        if show_seq2:
            ax.plot(
                n_values, y2,
                marker="s", markersize=8, markeredgecolor="white", markeredgewidth=1.5,
                color="#d32f2f", linewidth=2.2,
                label=fr"수열2: $a_n = {a1_2} + (n-1)\times{d2}$", zorder=3
            )

        # 두 수열의 차이를 --- 점선으로 표시
        if show_seq1 and show_seq2:
            for n, v1, v2 in zip(n_values, y1, y2):
                ax.plot([n, n], [v1, v2], "--", color="gray", alpha=0.6, linewidth=1.2)

        # 그래프 꾸미기
        ax.set_title(
            "두 등차수열 비교",
            fontsize=16, fontweight="bold", color="#1976d2", pad=15
        )
        ax.set_xlabel("n (항 번호)", fontsize=13, fontweight="bold")
        ax.set_ylabel("aₙ (값)", fontsize=13, fontweight="bold")
        ax.grid(alpha=0.25, linestyle="--")

        # 범례 스타일
        handles, labels = ax.get_legend_handles_labels()
        if labels:
            leg = ax.legend(
                fontsize=9, loc="upper left",
                frameon=True, fancybox=True, shadow=True, framealpha=0.9
            )
            for line in leg.get_lines():
                line.set_linewidth(3.0)

        plt.tight_layout()
        st.pyplot(fig)



        # --------------------
        # 📋 비교 표
        # --------------------
        df = pd.DataFrame({
            "항 번호 (n)": n_values,
            f"수열1 (a₁={a1_1}, d={d1})": y1,
            f"수열2 (a₁={a1_2}, d={d2})": y2,
            "차이 (수열2-수열1)": np.array(y2) - np.array(y1)
        })

        st.markdown("### 📋 비교 표")

        # 최근 4항만 잘라서 표시 & 차이에 색상 강조
        st.dataframe(
            df.style.format(precision=2).background_gradient(
                cmap="Reds", subset=["차이 (수열2-수열1)"]
            ),
            use_container_width=True,
            hide_index=True,   # index 숨김
            height=180         # 표 높이 제한
        )


    with tabs[2]:
        st.subheader("ℹ️ 수열과 리스트의 공통점")
        st.write("""
        - 두 개념 모두 항이 차례대로 정해진 순서를 가지며, 첫 번째·두 번째·… 방식으로 위치가 구분
        - $a_n$​과 `list[n-1]` 모두 수열 또는 리스트의 n번째 항을 의미함
        - `list[-1]`은 리스트의 마지막 항을 의미
        """)
        st.markdown("###### 💻 :blue[[예제 1]] 첫째 항이 `3`, 공차가 `2`인 등차수열을 `9`항까지 출력하세요.")
        st.code("""
        a = 3
        d = 2
        seq = [a]
        for i in range(1, 9):
            next_val = seq[-1] + d
            seq.append(next_val)
        print(seq)
        # 출력: [3, 5, 7, 9, 11, 13, 15, 17, 19]
        """)
        st.divider()

        st.markdown("###### 💻 :blue[[문제 1]] 첫째 항이 `2`, 공차가 `5`인 등차수열을 `5`항까지 출력하세요.")
        with st.expander("💡 힌트 보기"):
            st.markdown("`for`문과 `append()`를 활용해보세요. 새로운 항은 `seq[-1] + d`로 계산합니다.")
        with st.expander("💡 정답 보기"):
            st.code("""
        a = 2
        d = 5
        seq = [a]
        for i in range(1, 5):
            next_val = seq[-1] + d
            seq.append(next_val)
        print(seq)
        """)

        code_block_columns(1, "a=2\nd=5\nseq=[a]\n# 여기에 for문 작성\nprint(seq)", prefix="d3_")

        st.markdown("###### :blue[💻 [문제 2]] 첫째 항이 `30`, 공차가 `-3`인 등차수열에서 처음으로 음수가 되는 항은 제몇 항인지 출력하세요.")
        with st.expander("💡 힌트 보기"):
            st.markdown("`for`문으로 각 항을 생성하면서 `if next_val < 0:` 조건을 확인하고, 음수가 되는 순간 `break`로 종료한 뒤 그 인덱스(항 번호)를 출력해 보세요.")
        with st.expander("💡 정답 보기"):
            st.code("""
        a = 30
        d = -3
        seq = [a]
        for i in range(1, 100):  # 충분히 큰 반복 횟수 설정
            next_val = seq[-1] + d
            seq.append(next_val)
            if next_val < 0:
                print(i + 1)  # i=n 일때 next_val는 (n+1)항 
                break
        """)
        code_block_columns(2, "a=30\nd=-3\nseq=[a]\n# 여기에 for문 작성", prefix="d3_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("##### 💻 :blue[[프로젝트]] 나만의 등차수열 문제 만들기")

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

    with tabs[4]:
        st.markdown("##### 🌈 :rainbow[[수준별 문제]] 등차수열 도전")

        seq_level = st.radio(
            "난이도를 선택하세요!",
            ("하", "중", "상"),
            horizontal=True,
            key="d3_seq_level"
        )

        if seq_level == "하":
            q_title = "등차수열의 n번째 항 구하기"
            q_problem = "초항이 5, 공차가 2인 등차수열의 8번째 항을 출력해보세요."
            starter_code = "a = 5\nd = 2\nn = 8\n# 여기에 코드 작성\n"
            answer_code = (
                "a = 5\n"
                "d = 2\n"
                "n = 8\n"
                "an = a + (n-1)*d\n"
                "print(an)"
            )
        elif seq_level == "중":
            q_title = "리스트로 등차수열 만들기"
            q_problem = "초항이 7, 공차가 4인 등차수열의 앞 6개 항을 리스트로 만들어 출력하세요."
            starter_code = "a = 7\nd = 4\nseq = [a]\n# 여기에 코드 작성\n"
            answer_code = (
                "a = 7\n"
                "d = 4\n"
                "seq = [a]\n"
                "for i in range(1,6):\n"
                "    seq.append(seq[-1]+d)\n"
                "print(seq)"
            )
        else:  # 상
            q_title = "음수가 되는 첫 항 찾기"
            q_problem = "초항이 50, 공차가 -6인 등차수열에서 처음으로 음수가 되는 항의 번호를 출력하세요."
            starter_code = (
                "a = 50\n"
                "d = -6\n"
                "seq = [a]\n"
                "# 여기에 for, if, break로 작성\n"
            )
            answer_code = (
                "a = 50\n"
                "d = -6\n"
                "seq = [a]\n"
                "for i in range(1, 100):\n"
                "    next_val = seq[-1] + d\n"
                "    seq.append(next_val)\n"
                "    if next_val < 0:\n"
                "        print(i + 1)\n"
                "        break\n"
            )


        st.markdown(f"**[{seq_level}] {q_title}**  \n{q_problem}")

        with st.expander("💡 정답 코드 보기"):
            st.code(answer_code, language='python')

        code_block_columns("level", starter_code, prefix=f"d3_sel_{seq_level}_")


if __name__ == "__main__":
    show()