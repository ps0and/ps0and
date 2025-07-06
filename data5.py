import streamlit as st
from streamlit_ace import st_ace
import io
import sys

# ✅ 코드 실행 함수
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

# ✅ 좌우 2열 코드 작성 및 실행 블록
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

# ✅ 메인 수업 페이지 구성
def show():
    st.header("🗓️ Day 5")
    st.subheader("수열의 합")
    st.write("수열의 각 항을 더한 값을 ‘수열의 합’이라 합니다. 파이썬 코드로 직접 구현해 봅시다.")
    st.divider()

    st.subheader("🎥 오늘의 수업 영상")

    st.subheader("📌 학습 목표")
    st.write("""
    - 등차수열과 등비수열의 합 공식을 이해할 수 있다.
    - 파이썬으로 등차수열 및 등비수열의 합을 계산할 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.subheader("ℹ️ 수열의 합")
    st.write("""
            수열의 항을 순서대로 모두 더한 값을 수열의 합이라 합니다. 대표적으로 수열의 합은 등차수열과 등비수열에서 자주 사용됩니다
            - 등차수열의 합(차이가 일정함)
            - 등비수열의 합(곱하는 값이 일정함)
             """)
    
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.subheader("ℹ️ 등차수열의 합")
    st.write(""" 
             - **등차수열의 합**: 첫째 항 $a_1$, 공차 $d$, $n$항까지의 합 $S_n$는
             """)
    st.latex(r"S_n = \frac{n}{2}(a_1 + a_n) = \frac{n}{2}\bigl(2a_1 + (n-1)d\bigr)")
    st.write("- 예) $a_1=3$, $d=2$일 때")
    st.latex(r"S_{10} = \frac{10}{2}\bigl(2\times3 + (10-1)\times2\bigr) = 120")
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
        
    code_block_columns(1,"a = 2\nd = 5\nn = 20\nS_n = 0\n# 여기에 for문을 이용해 합을 계산하세요.\n", prefix="d5_")
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.subheader("ℹ️ 등비수열의 합")
    st.write(""" 
            - **등비수열의 합**: 첫째 항 $a_1$, 공비 $r$, $n$항까지의 합 $S_n$는
            """)
    st.latex(r"S_n = a_1 \times \frac{1 - r^n}{1 - r} \quad (r \neq 1)")
    st.write("- 예) $a_1=2$, $r=3$일 때")
    st.latex(r"S_{4} = 2 \times \frac{1-3^4}{1-3} = 2 \times \frac{1-81}{-2} = 2 \times 40 = 80")

    st.markdown("###### 💻 :blue[[예제 1]] 첫째 항이 `3`, 공비가 `2`인 등비수열의 첫 `10`항까지 합을 구하는 코드를 작성하세요.")
    st.code("""\
    a = 3
    r = 2
    S_n = a
    for i in range(1, 10):
        next_val = a * (r ** i)
        S_n = S_n + next_val
    print(S_n)
    """)

    st.markdown("###### 💻 :blue[[문제 1]] 첫째 항이 `2`, 공비가 `5`인 등비수열의 첫 `5`항까지 합을 구하는 코드를 작성하세요.")

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
    "a = 2\nr = 5\nn = 5\nS_n = 0\n# 여기에 for문을 이용해 합을 계산하세요.\n", prefix="d5_")
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    st.markdown("##### 💻 :blue[[모둠 문제]] 수열의 합 문제 만들기")
    st.write("학생 문제 설명과 작성 코드는 실행 결과 아래에서 확인할 수 있습니다.")

    student_problem = st.text_area(
    "📝 문제 설명 입력",
    value="초항이 4이고 공비가 3인 등비수열의 8항까지의 합을 구하는 코드를 작성하세요."
    )

    user_code = st_ace(
        value="# 여기에 로직을 작성하세요\n",
        language="python",
        theme="github",
        height=250,
        key="custom_editor"
    )

    if st.button("▶️ 실행 결과 확인", key="custom_run"):
        result, status = code_runner(user_code)
        display_output(result, status)
        st.code(f"# 🔍 학생 문제 설명\n{student_problem}\n\n# 💻 학생 작성 코드\n{user_code}")
        st.markdown(
        "<div style='text-align: left; color:orange;'>✨문제 설명과 시각화 작성 코드를 복사한 뒤, 스프레드시트 링크에 그대로 붙여넣어 과제를 제출해주세요!",
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
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

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
    else:  # 상
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

if __name__ == "__main__":
    show()