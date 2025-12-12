import streamlit as st
import google.generativeai as genai
import importlib.metadata

st.title("🕵️‍♂️ 긴급 진단 모드")

# 1. 라이브러리 버전 확인
try:
    ver = importlib.metadata.version("google-generativeai")
    st.write(f"### 1. 서버 라이브러리 버전: `{ver}`")
    if ver >= "0.8.3":
        st.success("✅ 버전은 최신입니다! (합격)")
    else:
        st.error("❌ 버전이 낮습니다. (불합격) -> requirements.txt 확인 필요")
except:
    st.error("❌ 라이브러리가 아예 설치되지 않았습니다.")

# 2. 모델 목록 확인
st.write("### 2. 내 키로 사용 가능한 모델 목록")
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    models = genai.list_models()
    available_models = []
    
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            
    st.code(available_models) # 화면에 목록 출력

    if "models/gemini-1.5-flash" in available_models:
        st.success("🎉 목록에 'gemini-1.5-flash'가 있습니다! 이제 본 코드를 쓰셔도 됩니다.")
    else:
        st.error("😱 목록에 'gemini-1.5-flash'가 없습니다!")
        st.warning("👉 원인: API 키가 '옛날 프로젝트'에 연결되어 있습니다.")
        st.info("👉 해결책: 구글 AI Studio에서 반드시 'Create key in NEW PROJECT'를 눌러서 키를 새로 받아야 합니다.")

except Exception as e:
    st.error(f"키 인증 실패: {e}")
