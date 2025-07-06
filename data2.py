import streamlit as st
from streamlit_ace import st_ace
import io
import sys

# ✅ 코드 실행 함수
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

# ✅ 출력 표시 함수
def display_output(result, status):
    if status == "success":
        st.markdown(f"```bash\n{result}\n```")
    else:
        st.markdown("###### ❌ 실행 중 오류 발생")
        st.markdown(
            f"<pre style='color: red; background-color: #ffe6e6; padding: 10px; border-radius: 5px;'>{result}</pre>",
            unsafe_allow_html=True
        )

# ✅ 코드 블록 (좌우형)
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

# ✅ 코드 블록 (상하형)
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


# ✅ 메인 수업 내용
def show():
    st.header("🗓️ 2Day")
    st.subheader("파이썬 기초: 조건문, 반복문")
    st.write("수학적 개념을 컴퓨터에 정확히 전달하려면 `if`,` for` 같은 제어문을 이해해 원하는 논리 흐름을 코드로 구현할 수 있어야 합니다. 탄탄한 문법 이해가 실습의 핵심입니다.")
    st.divider()

    st.subheader("🎥 수업 영상 보기")

    st.subheader("📌 학습 목표")
    st.write("""
    - 조건문(if/else)을 활용하여 코드의 실행 흐름을 제어할 수 있다.
    - 반복문(for)을 사용하여 반복적 연산과 누적 계산을 수행할 수 있다.
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

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

    st.markdown("##### 🌈 :rainbow[[수준별 문제]] 조건문과 반복문 실습")

    d2_level = st.radio(
        "난이도를 선택하세요!",
        ("하", "중", "상"),
        horizontal=True,
        key="d2_level_select"
    )

    # 임의 선정: 하 = if문(홀짝 판별), 중 = for+if(배수합), 상 = for+if+리스트(짝수리스트)
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
