import streamlit as st
import google.generativeai as genai

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="2025 과목세특 메이트",
    page_icon="📚",
    layout="centered"
)

# --- 2. [디자인] 숲속 테마 CSS (기존 디자인 유지) ---
st.markdown("""
    <style>
    /* 폰트 설정 */
    html, body, [class*="css"] { 
        font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif; 
    }
    
    /* 입력창: 부드러운 테두리 */
    .stTextArea textarea { 
        border-radius: 12px; 
        border: 1px solid rgba(85, 124, 100, 0.2); 
        background-color: #FAFCFA; 
    }
    
    /* 제목 스타일 */
    h1 { font-weight: 700; letter-spacing: -1px; color: #2F4F3A; } 
    .subtitle { font-size: 16px; color: #666; margin-top: -15px; margin-bottom: 30px; }
    
    /* 버튼 스타일: 세이지 그린 */
    .stButton button { 
        background-color: #557C64 !important; 
        color: white !important;
        border-radius: 10px; 
        font-weight: bold; 
        border: none; 
        transition: all 0.2s ease; 
        padding: 0.8rem 1rem; 
        font-size: 16px !important;
        width: 100%; 
    }
    .stButton button:hover { 
        background-color: #3E5F4A !important; 
        transform: scale(1.01); 
        color: white !important;
    }
    
    /* 슬라이더 스타일 */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div {
        background-color: #E0E0E0 !important; border-radius: 10px; height: 6px !important; 
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
        background-color: #D4AC0D !important; height: 6px !important; 
    }
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: transparent !important; box-shadow: none !important; border: none !important; height: 24px; width: 24px; 
    }
    div[data-testid="stSlider"] div[role="slider"]::after {
        content: "★"; font-size: 32px; color: #D4AC0D !important; position: absolute; top: -18px; left: -5px; text-shadow: 0px 1px 2px rgba(0,0,0,0.2);
    }
    div[data-testid="stSlider"] div[data-testid="stMarkdownContainer"] p { color: #557C64 !important; }

    /* 라디오 버튼 스타일 */
    div[data-testid="stRadio"] { background-color: transparent; }
    div[data-testid="stRadio"] > div[role="radiogroup"] { display: flex; justify-content: space-between; width: 100%; gap: 10px; }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        flex-grow: 1; background-color: #FFFFFF; border: 1px solid #E0E5E2; border-radius: 8px; padding: 12px; justify-content: center;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover { border-color: #557C64; background-color: #F7F9F8; }
    
    .guide-box { background-color: #F7F9F8; padding: 20px; border-radius: 12px; border: 1px solid #E0E5E2; margin-bottom: 25px; font-size: 14px; color: #444; line-height: 1.6; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
    .guide-title { font-weight: bold; margin-bottom: 8px; display: block; font-size: 15px; color: #557C64;}
    .warning-text { color: #8D6E63; font-size: 14px; margin-top: 5px; font-weight: 500; }
    .count-box { background-color: #E3EBE6; color: #2F4F3A; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 14px; margin-bottom: 10px; text-align: right; border: 1px solid #C4D7CD; }
    .analysis-box { background-color: #FCFDFD; border-left: 4px solid #557C64; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 14px; color: #333; }
    .footer { margin-top: 50px; text-align: center; font-size: 14px; color: #888; border-top: 1px solid #eee; padding-top: 20px; }
    .card-title { font-size: 15px; font-weight: 700; color: #557C64; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API 키 설정 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    api_key = None

# --- 4. 헤더 영역 ---
st.title("📚 2025 과목세특 메이트")
st.markdown("<p class='subtitle'>Subject Specific Records Generator</p>", unsafe_allow_html=True)
st.divider()

if not api_key:
    with st.expander("🔐 관리자 설정 (API Key 입력)"):
        api_key = st.text_input("Google API Key", type="password")

# [수정됨] 과목세특용 작성 팁
st.markdown("""
<div class="guide-box">
    <span class="guide-title">💡 완벽한 세특을 위한 3-Step 작성법</span>
    단순한 활동 나열은 NO! 아래 3가지 흐름이 들어가게 적어주세요.<br><br>
    1. <b>(동기/수업내용)</b> 교과서 단원, 배운 개념, 혹은 호기심을 갖게 된 계기<br>
    2. <b>(심화탐구)</b> 수행평가, 보고서 작성, 독서 등 구체적인 탐구 과정<br>
    3. <b>(성장/결과)</b> 이를 통해 확장된 지식, 변화된 생각, 진로와의 연결점
</div>
""", unsafe_allow_html=True)

# --- 5. 입력 영역 ---
st.markdown("### 1. 수업 활동 및 관찰 내용")
student_input = st.text_area(
    "입력창",
    height=200


