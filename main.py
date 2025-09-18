import streamlit as st

# 페이지 제목
st.title(":rainbow[7days of Coding Mathematics]")
st.markdown(
    """
    <style>
    .top-qna-link {
        display: inline-block;
        background: linear-gradient(90deg, #1976d2 5%, #42a5f5 90%);
        color: #fff !important;
        font-size: 17px;
        font-weight: 800;
        padding: 5px 10px 5px 12px;
        border-radius: 2em;
        box-shadow: 0 4px 18px rgba(25,118,210,0.13);
        margin: 0px 0 0px 0;
        letter-spacing: 1.2px;
        text-decoration: none !important;
        transition: background 0.16s, box-shadow 0.18s, transform 0.13s;
        position: relative;
    }
    .top-qna-link:hover {
        background: linear-gradient(90deg,#42a5f5 5%,#1976d2 90%);
        color: #fff !important;
        transform: translateY(-2px) scale(1.045);
        box-shadow: 0 7px 24px #1976d222;
        text-decoration: none !important;
    }
    .top-qna-link .qna-emoji {
        font-size: 17px;
        vertical-align: middle;
        margin-right: 10px;
        margin-left: -7px;
        filter: drop-shadow(0 2px 1px #1976d244);
    }
    .top-qna-row {
        width: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    </style>
    <div class="top-qna-row">
      <a href="https://docs.google.com/spreadsheets/d/161VOawYoJH6-zlY3ntZvm5JC9niaO6sVEt7IPFYFbdk/edit?usp=sharing"
         target="_blank"
         class="top-qna-link"
      ><span class="qna-emoji">💬</span>QnA 바로가기</a>
    </div>
    """,
    unsafe_allow_html=True
)

# 커스텀 CSS 삽입 (버튼 스타일링)
st.markdown(
    """
    <style>
    /* 모든 버튼 기본 그라디언트 스타일 */
    .stButton>button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        color: #08c972;
        padding: 8px 18px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 800;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
        cursor: pointer;
    }
    /* 이전 버튼 별도 컬러 */
    .stButton>button:first-of-type {
        background: #FF6B6B;
    }
    /* 다음 버튼 별도 컬러 */
    .stButton>button:last-of-type {
        background: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 드롭다운 메뉴 및 모듈 실행

days = ["1Day - 🛠️파이썬 기초 배우기(자료형,리스트)", "2Day - 🛠️파이썬 기초 배우기(조건문&반복문, 알고리즘적 사고)", "3Day - 🔢파이썬으로 등차수열 다루기", "4Day - 🔢파이썬으로 등비수열 다루기", "5Day - 🔢파이썬으로 수열의 합 다루기", "6Day - ✨인공지능의 이해", "7Day - 🔮AI 예측 스튜디오", "Day M - 🧙‍♂️코드 마스터"]
modules = {
    "1Day - 🛠️파이썬 기초 배우기(자료형,리스트)": "data1",
    "2Day - 🛠️파이썬 기초 배우기(조건문&반복문, 알고리즘적 사고)": "data2",
    "3Day - 🔢파이썬으로 등차수열 다루기": "data3",
    "4Day - 🔢파이썬으로 등비수열 다루기": "data4",
    "5Day - 🔢파이썬으로 수열의 합 다루기": "data5",
    "6Day - ✨인공지능의 이해": "data6",
    "7Day - 🔮AI 예측 스튜디오": "data7",
    "Day M - 🧙‍♂️코드 마스터": "data0",
}

if 'day' not in st.session_state:
    st.session_state.day = days[0]
if 'widget_day' not in st.session_state:
    st.session_state.widget_day = st.session_state.day

def update_from_selectbox():
    st.session_state.day = st.session_state.widget_day

def go_prev():
    idx = days.index(st.session_state.day)
    if idx > 0:
        new_day = days[idx - 1]
        st.session_state.day = new_day
        st.session_state.widget_day = new_day

def go_next():
    idx = days.index(st.session_state.day)
    if idx < len(days) - 1:
        new_day = days[idx + 1]
        st.session_state.day = new_day
        st.session_state.widget_day = new_day

st.selectbox(
    "도전을 시작합시다! 수업을 선택하세요. 👇",
    days,
    key='widget_day',
    on_change=update_from_selectbox
)

module = __import__(modules[st.session_state.day])
module.show()

# 이전 및 다음 버튼 (하단)
col1, col_blank, col3 = st.columns([1, 4, 1])
with col1:
    st.button("◀️ 이전", on_click=go_prev)
with col3:
    st.button("다음 ▶️", on_click=go_next)
