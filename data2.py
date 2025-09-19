import streamlit as st
from streamlit_ace import st_ace
import io
import sys

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

def display_output(result, status):
    if status == "success":
        st.markdown(f"```bash\n{result}\n```")
    else:
        st.markdown("###### ❌ 실행 중 오류 발생")
        st.markdown(
            f"<pre style='color: red; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>{result}</pre>",
            unsafe_allow_html=True
        )

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
        run = st.button("▶️ 코드 실행하기", key=f"{key_prefix}_run")
        if run:
            result, status = code_runner(code_input)
            display_output(result, status)

def code_block_rows(problem_number, starter_code, prefix=""):
    key_prefix = f"{prefix}{problem_number}"
    st.markdown("###### 📥 코드 입력")
    code_input = st_ace(
        value=starter_code,
        language='python',
        theme='github',
        height=200,
        key=f"{key_prefix}_editor"
    )
    run = st.button("▶️ 코드 실행하기", key=f"{key_prefix}_run")
    if run:
        st.markdown("###### 📤 실행 결과")
        result, status = code_runner(code_input)
        display_output(result, status)

# ✅ 메인 화면
def show():
    st.header("🗓️ 2Day")
    st.subheader("파이썬 기초 배우기(조건문&반복문, 알고리즘적 사고)")
    st.write("수학적 개념을 컴퓨터에 정확히 전달하려면 `if`,` for` 같은 제어문을 이해해 원하는 논리 흐름을 코드로 구현할 수 있어야 합니다. 탄탄한 문법 이해가 실습의 핵심입니다.")
    st.video("https://youtu.be/ar8hbuEkdoY")
    st.subheader("📌 학습 목표")
    st.write("""
    - 조건문(if/else)을 활용하여 코드의 실행 흐름을 제어할 수 있다.
    - 반복문(for)을 사용하여 반복적 연산과 누적 계산을 수행할 수 있다.
    - 수학 문제를 해결할 때 필요한 과정을 단계별로 정의하고, 이를 알고리즘적 사고로 표현할 수 있다
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    tabs = st.tabs([
        "1️⃣ 조건문",
        "2️⃣ 반복문",
        "3️⃣ 알고리즘적 사고",
        "4️⃣ 수준별 문제",
    ])

    with tabs[0]:
        st.subheader("ℹ️ 조건문 if/else")
        st.write("조건문은 주어진 조건의 참·거짓에 따라 서로 다른 코드 블록을 실행하도록 제어하는 구문")
        st.code("""
        if 조건:
            조건이 True일 때 실행할 코드
        else:
            조건이 False일 때 실행할 코드
        """)
        st.image("image/data2_img1.png")
        st.markdown("""###### 💻 :blue[[예제 1]] 조건문을 사용해 `a > b`인 경우 메시지를 출력해보세요""")
        st.code("""
        a = 10
        b = 3
        if a > b:
            print('a는 b보다 크다')
        else:
            print('a는 b보다 작거나 같다')
        """)
        code_block_rows(1, "a = 10\nb = 3\nif a > b:\n    print('a는 b보다 크다')\nelse:\n    print('a는 b보다 작거나 같다')", prefix="d2_")
        st.markdown("""###### 💻 :blue[[문제 1]]  `num`이 짝수이면 `num은 짝수` 홀수이면 `num은 홀수`가 출력되도록 코드를 작성하세요.""")
        with st.expander("💡 힌트 보기"):
            st.markdown("짝수는 `num % 2 == 0`을 활용해보세요.")
        with st.expander("💡 정답 보기"):
            st.markdown("""```python\nnum = 1\nif num% 2 == 0:\n    print('num은 짝수')\nelse:\n    print('num은 홀수')\n```""")
        code_block_columns(2, "num = 1\nif num\n ", prefix="d2_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    
    with tabs[1]:
        st.subheader("ℹ️ 반복문 for")
        st.write("""
        - 반복문은 지정한 조건이나 횟수에 따라 동일한 코드 블록을 자동으로 여러 번 실행하도록 제어하는 구문
        - 범위에 있는 요소 하나하나가 반복자(변수)에 들어가며 차례차례 아래 코드가 반복
        - 범위 `range(start,end)`는 start부터 end-1까지의 정수로 범위를 생성
        """)
        st.code("""
        for 반복자 in 반복할 수 있는 것:
            코드
        """)
        st.write("""
        - `break`는 반복문 내부에서 사용되며, 즉시 반복을 종료하고 반복문 뒤의 코드를 실행
        """)
        st.code("""
        for i in range(1, 10):
            if i==5:
                break # i가 5일 때 즉시 반복 종료
            print(i)
        # 출력:1 2 3 4       
        """)
        st.markdown("""###### 💻 :blue[[예제 2]] 1부터 10까지 숫자를 출력하는 코드를 작성하세요""")
        st.code("""
        for i in range(1, 11):
            print(i)
        """)
        code_block_columns(3, "for i",prefix="d2_")
        st.markdown("""###### 💻 :blue[[문제 2]] 1부터 5까지의 합을 구하는 코드를 작성하세요""")
        with st.expander("💡 힌트 보기"):
            st.markdown(" 1~5까지 수는 `range(1, 6)`으로 만들 수 있습니다. `total`이라는 변수를 만들어서 `for`문 안에서 `total=total + i`로 더해줍니다.""")
        with st.expander("💡 정답 보기"):
            st.markdown("""```python\ntotal = 0\nfor i in range(1, 6):\n    total = total + i # total += i \nprint('합계:', total)\n```""")
        code_block_columns(4, "total = 0 #초기값 설정\nfor i \n\nprint('합계:', total)", prefix="d2_")
        st.markdown("###### 💻 :blue[[문제 3]] 1부터 100 사이의 짝수만 리스트에 담고 출력해보세요")
        with st.expander("💡 힌트 보기"):
            st.markdown("짝수는 `i % 2 == 0`을 활용해보세요. `even_list.append(i)`로 리스트에 추가합니다.")
        with st.expander("💡 정답 보기"):
            st.markdown("""```python\neven_list = []\nfor i in range(1, 101):\n    if i % 2 == 0:\n        even_list.append(i)\nprint(even_list)\n```""")
        code_block_columns(5, "even_list = []\nfor i in range(1, 101):\n    # 여기에 if문 작성\n\nprint(even_list)", prefix="d2_")

        st.markdown("###### 💻 :blue[[문제 4]] 1부터 10까지 수 중 3의 배수의 합을 구하세요")
        with st.expander("💡 힌트 보기"):
            st.markdown("3의 배수는 `i % 3 == 0`을 활용해보세요. `total`이라는 변수를 만들어서 `for`문 안에서 `total=totla + i`로 더해줍니다.")
        with st.expander("💡 정답 보기"):
            st.markdown("""```python\ntotal = 0\nfor i in range(1, 11):\n    if i % 3 == 0:\n        total = total + i\nprint('3의 배수의 합:', total)\n```""")
        code_block_columns(6, "total = 0\nfor i in range(1, 11):\n    # 여기에 if문 작성\n\nprint('3의 배수의 합:', total)", prefix="d2_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
   
    with tabs[2]:
        st.subheader("🗂️ 알고리즘적 사고")
        st.info("""
        알고리즘적 사고란 문제 해결을 위해 문제를 작은 단계로 나누고, 그 단계를 차례대로 연결해 해결 방법을 만드는 생각 방법이에요. 문제를 입력(문제 조건), 출력(구하려는 답), 제약(지켜야 할 규칙)으로 나눈 뒤, 그 과정을 코드로 차례대로 설계하고 결과가 맞는지 확인해요. 이러한 알고리즘적 사고를 통해 수학 문제를 해결하면 단순히 답만 아는 것이 아니라, 수학이 어떤 구조와 과정을 통해 작동하는지 깊이 이해할 수 있어요.\n
        1️⃣ 문제 분해 : 문제를 입력·출력·제약으로 나누어 핵심을 정리한다.\n
        2️⃣ 절차화 : 해결 과정을 단계별 순서로 설계하고 코드로 표현한다.\n
        3️⃣ 검증 및 일반화 : 결과를 확인하고, 다른 상황에도 적용되도록 확장한다.
        """)
        st.success("**문제**: 1부터 n까지의 합을 다음 알고리즘적 사고 단계로 구하시오")
        st.markdown("### 1️⃣ 문제 분해")
        st.write("""
        - 문제에서 필요한 입력(조건)과 출력(답) 및 제약(규칙)을 정리하세요.  
        """)
        student_thoughts = st.text_area("✍️ 문제를 분해하는 과정을 직접 작성해보세요", height=100)
        st.divider()
        st.markdown("### 2️⃣ 절차화")
        st.write("""
        - 문제 해결 과정을 차례대로 정리해 보세요.  
        - 각 단계를 코드처럼 순서대로 적어 보세요.
        """)
        st.caption("아래에 알고리즘 단계를 순서대로 적어보세요 (최소 2단계, 최대 8단계).")
        step_count = st.number_input("단계 수를 선택하세요.", min_value=2, max_value=8, value=3, step=1, key="d2_alg_step_count")
        alg_steps = []
        for i in range(1, step_count + 1):
            s = st.text_input(f"단계 {i}", key=f"d2_alg_step_{i}",
                            placeholder=f"예) total=0 으로 초기화")
            alg_steps.append(s)
        st.divider()
        st.markdown("### 3️⃣ 검증 및 일반화")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 📄 내가 설계한 코드(미리보기)")
            pseudo = "\n".join([f"{i+1}. {line}" for i, line in enumerate(alg_steps) if line.strip()])
            st.code(pseudo, language="text")
        with c2:
            st.write("아래 코드 블록의 빈칸을 채워 직접 코드를 작성해보세요.")
            starter_code = (
                "n = 5  # n 값을 바꿔보세요\n"
            )
            code_input = st_ace(
                value=starter_code,
                language="python",
                theme="github",
                height=200,
                key="alg_step2_editor"
            )
            run = st.button("▶️ 코드 실행하기", key="alg_step2_run")
        n_val = st.number_input("n 값을 입력하세요", min_value=1, value=5, step=1)

        if run:
            result, status = code_runner(code_input)
            st.markdown("#### 📤 실행 결과")
            display_output(result, status)
            correct = sum(range(1, n_val+1))
            st.success(f"✅ 정답 확인: 1부터 {n_val}까지의 합 = {correct}")
        st.write("👉 실행 결과와 정답을 비교해보며 코드를 점검해보세요.")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("##### 🌈 :rainbow[[수준별 문제]] 조건문과 반복문 실습")
        d2_level = st.radio(
            "난이도를 선택하세요!",
            ("하", "중", "상"),
            horizontal=True,
            key="d2_level_select"
        )
        if d2_level == "하":
            q_title = "홀짝 판별"
            q_problem = "정수 num이 주어졌을 때 짝수면 '짝수', 홀수면 '홀수'를 출력하는 코드를 작성하세요. (num=17)"
            starter_code = "num = 17\n# 여기에 if문 작성\n"
            answer_code = (
                "num = 17\n"
                "if num % 2 == 0:\n"
                "    print('짝수')\n"
                "else:\n"
                "    print('홀수')"
            )
        elif d2_level == "중":
            q_title = "3의 배수의 합 구하기"
            q_problem = "1부터 20까지 수 중 3의 배수의 합을 출력하세요."
            starter_code = "total = 0\nfor i in range(1, 21):\n    # 여기에 if문 작성\n\nprint('3의 배수의 합:', total)"
            answer_code = (
                "total = 0\n"
                "for i in range(1, 21):\n"
                "    if i % 3 == 0:\n"
                "        total += i\n"
                "print('3의 배수의 합:', total)"
            )
        else:  # 상
            q_title = "짝수 리스트 만들기"
            q_problem = "1부터 50까지의 짝수만 리스트에 담아 출력하세요."
            starter_code = "even_list = []\nfor i in range(1, 51):\n    # 여기에 if문 작성\n\nprint(even_list)"
            answer_code = (
                "even_list = []\n"
                "for i in range(1, 51):\n"
                "    if i % 2 == 0:\n"
                "        even_list.append(i)\n"
                "print(even_list)"
            )
        st.markdown(f"**[{d2_level}] {q_title}**  \n{q_problem}")
        with st.expander("💡 정답 코드 보기"):
            st.code(answer_code, language='python')
        code_block_columns("level", starter_code, prefix=f"d2_sel_{d2_level}_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)