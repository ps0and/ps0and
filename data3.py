import streamlit as st
from streamlit_ace import st_ace
import io
import sys

# ✅ 코드 실행 함수 (간결하고 안전하게)
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

# ✅ 출력 함수 (즉시 렌더링용)
def display_output(result, status):
    if status == "success":
        st.markdown(f"```bash\n{result}\n```")
    else:
        st.markdown("#### ❌ 실행 중 오류 발생")
        st.markdown(
            f"<pre style='color: red; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>{result}</pre>",
            unsafe_allow_html=True
        )

# ✅ 리팩토링된 코드 블록 함수 (세션 상태 저장 X)
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

# ✅ 메인 수업 페이지 구성
def show():
    st.header("🗓️ Day 3")
    st.subheader("수열: 등차수열")
    st.write("등차수열을 파이썬 코드로 직접 구현해 봅니다.")
    st.divider()

    st.subheader("🎥 오늘의 수업 영상")

    st.subheader("📌 학습 목표")
    st.write("""
    - 등차수열의 일반항 개념을 이해할 수 있다.
    - 파이썬으로 등차수열을 구현하고 특정 조건을 만족하는 항을 찾을 수 있다.
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
    st.write("""
    - **수열과 리스트의 공통점**
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

    st.markdown("##### 💻 :blue[[모둠 활동]] 나만의 등차수열 문제 만들기")
    st.write("✨:orange[학생 문제 설명과 작성 코드는 실행 결과 아래에서 확인할 수 있습니다.]")
    # 💡 모둠 활동: 문제 설명과 코드 실습 최적화
    student_problem = st.text_area(
        "📝 문제 설명 입력", 
        value=st.session_state.get("student_problem_text", "초항이 4이고 공차가 3인 등차수열의 첫 7항을 출력하세요.")
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
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

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