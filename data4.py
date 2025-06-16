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
            theme='dracula',
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
    1. 등비수열의 일반항을 이해한다.  
    2. 파이썬 코드로 수열을 생성한다.
    """)
    st.divider()

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
    st.divider()

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
        theme="monokai",
        height=250,
        key="ace_custom"
    )
    st.session_state["custom_code"] = user_code

    if st.button("▶️ 실행 결과 확인"):
        result, status = code_runner(user_code)
        display_output(result, status)

        st.code(f"# 🔍 학생 문제 설명\n{student_problem}\n\n# 💻 학생 작성 코드\n{user_code}")
        st.markdown(
        "<div style='text-align: right; color:orange;'>✨아래 문제 설명과 코드를 복사한 뒤, 스프레드시트 링크에 그대로 붙여넣어 과제를 제출해주세요! <a href='https://docs.google.com/spreadsheets/d/1n82pBQVdLg0iXVtm0aXJAGq0C_5N1RB-C-7sCZX7AEw/edit?usp=sharing' target='_blank'>(과제 제출 링크)</a></div>",
        unsafe_allow_html=True
        )


if __name__ == "__main__":
    show()
