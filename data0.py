import streamlit as st
from streamlit_ace import st_ace
import pandas as pd
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

def code_block(problem_number, title, starter_code, prefix=""):
    key_prefix = f"{prefix}{problem_number}"
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"##### 📥 코드 입력 ")
        code_input = st_ace(
            value=starter_code,
            language='python',
            theme='github',
            height=250,
            key=f"{key_prefix}_editor"
        )

    with c2:
        st.markdown("##### 📤 실행 결과")
        if st.button("▶️ 코드 실행하기", key=f"{key_prefix}_run"):
            result, status = code_runner(code_input)
            display_output(result, status)

def diagnostic_evaluation():
    st.subheader("📝 진단 평가")
    st.write("아래 두 문제를 풀어 제출해주세요.")

    with st.form("diag_form"):
        q1 = st.text_input(
            "(1) Hello를 출력하는 코드",
            placeholder="힌트: print"
        )
        q2 = st.text_input(
            "(2) 한 줄로: 숫자 5를 a에, 3을 b에 할당하고 두 수의 합을 출력하는 코드를 작성하세요.",
            placeholder="예: a=5; print(a)"
        )
        submitted = st.form_submit_button("제출")

    if submitted:
        correct1 = q1.strip().replace('"', "'") == "print('Hello')"
        clean_q2 = q2.replace(" ", "")
        correct2 = (
            "a=5" in clean_q2 and
            "b=3" in clean_q2 and
            "print(a+b)" in clean_q2
        )

        if not correct1:
            st.info("👉 추천 학습 시작: Day 1")
            return 1
        elif not correct2:
            st.info("👉 추천 학습 시작: Day 2")
            return 2
        else:
            st.info("👉 추천 학습 시작: Day 3")
            return 3 
        
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
    st.divider()
    st.header("🗓️ Day M")
    st.subheader("🧙‍♂️코드 마스터")
    st.markdown("""
    코드 마스터는 코딩을 처음 시작하는 여정을 안내하는 **입문 단계**입니다. **Day 1 ~ Day 5의 학습 중 코딩 실습 부분을 모아 구성된 과정**으로 여기서는 파이썬의 기초 문법부터 자료형, 연산, 조건문, 반복문까지 다루며, 수학적 사고와 프로그래밍적 사고를 연결하여 **코딩의 기초 체력을 쌓는 과정**입니다.  
    👉 진단 평가를 통해 본인에게 맞는 시작 지점을 확인하고, 단계별 실습 문제를 풀면서 **코딩 마법사**로 성장해 보세요!
    """)
    st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    tabs = st.tabs([
        "0️⃣ 진단평가",
        "1️⃣ 자료형과 출력",
        "2️⃣ 변수와 입력",
        "3️⃣ 리스트와 인덱스",
        "4️⃣ 조건문",
        "5️⃣ 반복문",
        "6️⃣ 알고리즘적 사고",
        "7️⃣ 등차수열 코딩",
        "8️⃣ 등비수열 코딩",
        "9️⃣ 수열의 합 코딩",
    ])

    with tabs[0]:
        diagnostic_evaluation()
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("ℹ️ 자료형")
        st.write("""          
        - 문자열: 메일 제목, 메시지 내용 등 따옴표('')로 감싸서 입력 Ex.```'Hello World'```
        - 숫자열: 물건의 가격, 학생의 성적 Ex. ```52, 12```
        - 불: 친구의 로그인 상태 Ex. ```True, False```""")
        st.divider() 
        st.subheader("ℹ️ 출력: print() 함수")
        st.write("""          
        - ```print()``` 함수의 괄호 안에 출력하고 싶은 내용을 적습니다.
        - ```print(1,'a')``` 함수의 괄호 안에 출력하고 싶은 내용을 쉼표로 연결해서 여러 개 적어도 됩니다.""")
        st.markdown(""" ###### 💻 :blue[[문제 1]] 아래와 같이 print 함수를 이용해서 다양한 자료형을 출력해보세요""")
        code_block(1, "print 함수", "print('hello', 320)\nprint(21)", prefix="d1_")
        data = {
            "연산 종류": ["덧셈", "뺄셈", "곱셈", "나눗셈", "정수 나눗셈", "나머지", "거듭제곱"],
            "연산자": ["+", "-", "*", "/", "//", "%", "**"],
            "예시 코드": ["3 + 2", "5 - 2", "4 * 2", "10 / 4", "10 // 4", "10 % 4", "2 ** 3"],
            "결과": [5, 3, 8, 2.5, 2, 2, 8],
            "설명": [
                "두 수를 더함",
                "앞 수에서 뒤 수를 뺌",
                "두 수를 곱함",
                "실수 나눗셈 결과",
                "몫만 구함 (소수점 버림)",
                "나눗셈의 나머지 계산",
                "제곱 (2의 3제곱)"
            ]
        }
        df = pd.DataFrame(data)
        st.subheader("🧮 파이썬 사칙연산 정리표")
        st.dataframe(df, use_container_width=True)
        st.markdown(""" ###### 💻 :blue[[문제 2]] 아래와 같이 숫자의 연산을 출력해보세요""")
        code_block(2, "연산 출력", "print('5+7=', 5+7)\nprint('5**2=', 5**2)", prefix="d1_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[2]:
        st.subheader("ℹ️ 변수와 입력")
        st.write("""          
        - 변수는 값을 저장할 때 사용하는 식별자
        - ```변수 = 값``` (값을 변수에 할당합니다.)
        - ```=``` 기호는 '같다'의 의미가 아니라 우변의 값을 좌변에 '할당하겠다'의 의미""")
        st.markdown("""###### 💻 :blue[[문제 3]] 아래와 같이 x라는 변수에 숫자나 문자를 할당하고 변수를 출력해보세요""")
        code_block(3, "변수 사용", "pi = 3.14\nprint(pi)", prefix="d1_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)

    with tabs[3]:
        st.subheader("ℹ️ 리스트(list) 및 인덱스(index)")
        st.write("""          
        - 리스트란 숫자나 문자 등의 자료를 모아서 사용할 수 있게 해주는 특별한 자료
            - 리스트는 대괄호 [ ] 내부에 여러 종류의 자료를 넣어 선언합니다.
            - [요소, 요소, ..., 요소]
        """)
        st.code("""
    list = [12, '문자열', True]
    print(list)
    # 출력: [12, '문자열', True]
        """)
        st.write("""          
        - 파이썬은 인덱스를 0부터 셉니다.
        - 리스트의 특정 위치(인덱스)를 출력하려면 대괄호를 사용합니다.
        """)
        st.image("image/data1_img1.png")
        st.code("""
    list = [12, '문자열', True]
    print(list[0])  
    # 출력: 12
        """)
        st.write("""
        - append() 함수는 리스트에 요소를 추가합니다.
        """)
        st.code("""
    list = ['a', 'b', 'c']
    list.append('d')
    print(list)  
    # 출력: ['a', 'b', 'c', 'd']
        """)
        st.markdown("""###### 💻 :blue[[문제 4]] 리스트에 자료를 추가하고 특정 요소를 출력해보세요""")
        with st.expander("💡 힌트 보기"):
            st.markdown("`list.append()`를 사용하여 리스트에 요소를 추가하고 `list[]`를 사용하여 특정 요소를 출력합니다.")
        code_block(4, "리스트 사용", "list =", prefix="d1_")
        st.markdown("<hr style='border: 2px solid #2196F3;'>", unsafe_allow_html=True)
    
    with tabs[4]:
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
    
    with tabs[5]:
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
   
    with tabs[6]:
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

    with tabs[7]:
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

    with tabs[8]:
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

    with tabs[9]:
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
