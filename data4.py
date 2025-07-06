import streamlit as st
from streamlit_ace import st_ace
import io
import sys

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

# ✅ 메인 수업 페이지 구성
def show():
    st.header("🗓️ Day 4")
    st.subheader("수열: 등비수열")
    st.write("등비수열을 파이썬 코드로 직접 구현해 봅니다.")
    st.divider()

    st.subheader("🎥 오늘의 수업 영상")

    st.subheader("📌 학습 목표")
    st.write("""
    - 등비수열의 일반항 개념을 이해할 수 있다.
    - 파이썬으로 등비수열을 구현하고 특정 조건을 만족하는 항을 찾을 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.subheader("ℹ️ 수열 (Sequence)")
    st.write("""
    - **정의**: 특정한 규칙 또는 대응에 따라 순서대로 나열된 수들의 열
    - 수열 $\{a_n\}$은 자연수 집합 $\mathbb{N}$을 정의역으로, 어떤 값의 집합 $S$를 공역으로 하는 함수
    $$
    a: \mathbb{N} \mapsto S, \quad n \mapsto a(n) = a_n
    $$
    - $a_n$: n번째 항
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    st.subheader("ℹ️ 등비수열 (Geometric Sequence)")
    st.write("""
    - **등비수열**: 인접한 두 항의 비(공비)가 일정한 수열  
    - 첫째 항을 $a_1$, 공비를 $r$이라 하면, n번째 항 $a_n$은
    $$
    a_n = a_1r^{n-1}
    $$
    - 예) $a_1=3$, $r=2$일 때 수열은 $[3, 6, 12, 24, \dots]$
    """)
    st.write("""
    - **수열과 리스트의 공통점**  
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

    st.markdown("##### 💻 :blue[[모둠 활동]] 나만의 등비수열 문제 만들기")
    st.write("✨:orange[학생 문제 설명과 작성 코드는 실행 결과 아래에서 확인할 수 있습니다.]")
    student_problem = st.text_area(
        "📝 문제 설명 입력", 
        value=st.session_state.get("student_problem_text", "초항이 4이고 공비가 3인 등비수열의 첫 7항을 출력하세요.")
    )
    st.session_state["student_problem_text"] = student_problem

    user_code = st_ace(
        value=st.session_state.get("custom_code", "# 여기에 로직을 작성하세요\n"),
        language="python",
        theme="github",
        height=250,
        key="ace_custom"
    )
    st.session_state["custom_code"] = user_code

    if st.button("▶️ 실행 결과 확인"):
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
     # === 수준별 문제 ===
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
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



if __name__ == "__main__":
    show()
