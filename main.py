import streamlit as st

# 페이지 제목
st.title(":rainbow[7days of Coding Mathematics]")

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

days = ["1Day", "2Day", "3Day", "4Day", "5Day", "6Day", "7Day"]
modules = {d: f"data{d[0]}" for d in days}
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
st.markdown("---")
col1, col_blank, col3 = st.columns([1, 4, 1])
with col1:
    st.button("◀️ 이전", on_click=go_prev)
with col3:
    st.button("다음 ▶️", on_click=go_next)
