import streamlit as st
import google.generativeai as genai

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="2025 영어 세특 메이트", page_icon="📘", layout="centered")

# --- 2. [디자인] CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }
    .stTextArea textarea { border-radius: 12px; background-color: #FAFCFA; }
    .stButton button { background-color: #557C64 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API 키 설정 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = None

st.title("📘 2025 영어 세특 메이트 (구버전 호환)")
st.caption("※ 구형 모델(gemini-pro) 모드로 작동 중입니다.")

if not api_key:
    with st.expander("🔐 관리자 설정"):
        api_key = st.text_input("Google API Key", type="password")

# 입력 영역
st.markdown("### 1. 학생 관찰 내용")
student_input = st.text_area("입력창", height=200, placeholder="내용을 입력하세요.")

# 옵션
st.markdown("### 2. 옵션 설정")
mode = st.radio("모드", ["풍성하게", "엄격하게"], horizontal=True)
target_length = st.slider("글자 수", 300, 1000, 500, 50)

# 실행
if st.button("✨ 작성하기"):
    if not api_key or not student_input:
        st.error("키와 내용을 입력해주세요.")
    else:
        with st.spinner('작성 중...'):
            try:
                genai.configure(api_key=api_key)
                
                # [중요] 여기서 무조건 구형 모델을 씁니다.
                target_model = "gemini-pro" 
                
                model = genai.GenerativeModel(target_model)
                
                prompt = f"""
                역할: 고등학교 영어 교사.
                내용: {student_input}
                목표: 영어 세부능력 및 특기사항 작성. {target_length}자 내외.
                모드: {mode} (엄격하게면 팩트위주, 풍성하게면 살을 붙여서)
                """
                
                response = model.generate_content(prompt)
                st.success("완료!")
                st.text_area("결과", value=response.text, height=400)
                
            except Exception as e:
                st.error(f"오류 발생: {e}")
                if "404" in str(e):
                    st.error("🚨 이 키로는 구형 모델(gemini-pro)도 쓸 수 없습니다. Google AI Studio에서 새 키를 받으셔야 합니다.")

