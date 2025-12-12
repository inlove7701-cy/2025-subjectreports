import streamlit as st
import google.generativeai as genai

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="2025 영어 세특 메이트",
    page_icon="📘",
    layout="centered"
)

# --- 2. [디자인] 숲속 테마 CSS ---
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
st.title("📘 2025 영어 세특 메이트")
st.markdown("<p class='subtitle'>Gift for English Teachers (Text Only)</p>", unsafe_allow_html=True)
st.divider()

if not api_key:
    with st.expander("🔐 관리자 설정 (API Key 입력)"):
        api_key = st.text_input("Google API Key", type="password")

# 영어 세특용 작성 팁
st.markdown("""
<div class="guide-box">
    <span class="guide-title">💡 고퀄리티 영어 세특을 위한 3-Step 가이드</span>
    입력창에 아래 3가지 요소를 포함해서 적어주시면 AI가 완벽하게 정리해줍니다.<br><br>
    1. <b>(What)</b> 수업 시간에 배운 단원, 지문 주제, 수행평가 내용<br>
    2. <b>(How)</b> 학생이 읽은 심화 자료(TED, 영자신문, 원서)나 탐구 과정<br>
    3. <b>(Why/Result)</b> 이를 통해 향상된 영어 실력(어휘/독해/작문)이나 진로 연계점
</div>
""", unsafe_allow_html=True)

# --- 5. 입력 영역 ---
st.markdown("### 1. 학생 관찰 내용")
student_input = st.text_area(
    "입력창",
    height=200,
    placeholder="예시: '환경' 단원을 배우고 기후변화 관련 영문 기사를 찾아 읽음. 전문 용어(carbon footprint 등)를 정리하고, 자신의 진로인 환경공학자와 연결하여 영어 에세이를 작성함.", 
    label_visibility="collapsed"
)

if student_input and len(student_input) < 30:
    st.markdown("<p class='warning-text'>⚠️ 내용이 조금 짧습니다. 구체적인 활동 내용을 넣어주세요.</p>", unsafe_allow_html=True)

# --- 6. 3단계 작성 옵션 ---
st.markdown("### 2. 작성 옵션 설정")

# [카드 1] 모드 선택
with st.container(border=True):
    st.markdown('<p class="card-title">① 작성 모드 선택</p>', unsafe_allow_html=True)
    mode = st.radio(
        "모드",
        ["✨ 풍성하게 (내용 보강)", "🛡️ 엄격하게 (팩트 중심)"],
        captions=["살을 붙여 자연스럽게 만듭니다.", "입력된 사실 외에는 절대 짓지 않습니다."],
        horizontal=True, 
        label_visibility="collapsed"
    )

# [카드 2] 희망 분량
with st.container(border=True):
    st.markdown('<p class="card-title">② 희망 분량 (공백 포함)</p>', unsafe_allow_html=True)
    target_length = st.slider(
        "글자 수",
        min_value=100, max_value=1000, value=500, step=10,
        label_visibility="collapsed"
    )

# [카드 3] 영어과 역량 키워드 선택
with st.container(border=True):
    st.markdown('<p class="card-title">③ 강조할 핵심 역량 (다중 선택)</p>', unsafe_allow_html=True)
    filter_options = [
        "👑 AI 자동 판단", 
        "📖 심화 독해력(Reading)", 
        "✍️ 논리적 영작문(Writing)", 
        "🗣️ 유창한 발표(Speaking)", 
        "📚 어휘 및 문법 활용력", 
        "🔎 비판적 사고/주제 탐구", 
        "🌏 문화적 소양/글로벌 감각", 
        "🚀 진로 연계 탐구"
    ]
    try:
        selected_tags = st.pills("키워드 버튼", options=filter_options, selection_mode="multi", label_visibility="collapsed")
    except:
        selected_tags = st.multiselect("키워드 선택", filter_options, label_visibility="collapsed")

# [고급 설정] 모델 선택
st.markdown("")
with st.expander("⚙️ AI 모델 직접 선택하기 (고급 설정)"):
    manual_model = st.selectbox(
        "사용할 모델을 선택하세요 (오류 시 구버전을 선택하세요)",
        ["🤖 자동 (Auto)", "⚡ gemini-1.5-flash (빠름/무료)", "🤖 gemini-1.5-pro (고성능)"],
        index=0
    )

# --- 7. 실행 및 결과 영역 ---
st.markdown("")
if st.button("✨ 영어 세특 생성하기", use_container_width=True):
    if not api_key:
        st.error("⚠️ API Key가 설정되지 않았습니다.")
    elif not student_input:
        st.warning("⚠️ 학생 관찰 내용을 입력해주세요!")
    else:
        with st.spinner(f'AI가 영어 선생님 모드로 분석 중입니다...'):
            try:
                genai.configure(api_key=api_key)

                # --- 모델 선택 로직 (여기서 2.5 같은 오타 방지) ---
                target_model = "gemini-1.5-flash" # 기본값
                
                if "pro" in manual_model:
                    target_model = "gemini-1.5-pro"
                elif "flash" in manual_model:
                    target_model = "gemini-1.5-flash"
                elif "자동" in manual_model:
                    # 자동일 때도 안전하게 flash 우선
                    target_model = "gemini-1.5-flash"

                # 모드별 프롬프트 설정
                if "엄격하게" in mode:
                    temp = 0.2
                    prompt_instruction = """
                    # ★★★ 엄격 작성 원칙 (Strict Mode) ★★★
                    1. **절대 날조 금지 (Zero Hallucination)**: 학생이 하지 않은 활동(책, 발표 등)은 절대 창작하지 마십시오.
                    2. **담백한 서술**: 미사여구보다는 '어떤 활동을 통해 무엇을 배웠는지' 인과관계 위주로 작성하십시오.
                    3. 입력된 사실(Fact)에 기반한 영어 실력 평가 위주로 작성하십시오.
                    """
                else:
                    temp = 0.75
                    prompt_instruction = """
                    # ★★★ 풍성 작성 원칙 (Rich Mode) ★★★
                    1. **내용 보강 (Elaboration)**: 단순한 활동 나열을 넘어, 해당 활동이 학생의 영어 실력 향상에 어떤 도움이 되었는지 교육적으로 서술하십시오.
                    2. **자연스러운 연결**: 문장과 문장 사이를 매끄럽게 연결하여 유려한 글이 되도록 하십시오.
                    3. 학생의 영어 학습 열정과 잠재력을 긍정적인 어조로 구체화하여 서술하십시오.
                    """

                generation_config = genai.types.GenerationConfig(temperature=temp)
                model = genai.GenerativeModel(target_model, generation_config=generation_config)

                # 키워드 처리
                if not selected_tags:
                    tags_str = "별도 지정 없음. [수업태도/참여] -> [주제탐구활동] -> [영어역량성장] -> [진로연계] 순서로 작성."
                else:
                    tags_str = f"핵심 키워드: {', '.join(selected_tags)}"

                # 영어 세특 전용 프롬프트
                system_prompt = f"""
                당신은 입학사정관의 평가 기준을 완벽히 이해하고 있는 고등학교 영어 담당 베테랑 교사입니다.
                교사가 입력한 [수업 활동 관찰 내용]을 바탕으로, 학생의 영어 학업 역량이 돋보이는 '영어 과목 세부능력 및 특기사항(세특)'을 작성해야 합니다.

                # Input Data
                1. 학생 활동 및 관찰 내용: {student_input}
                2. 강조할 핵심 역량: [{tags_str}]

                # Writing Guidelines (작성 지침)
                1. **영어 고유 역량 강조**: 단순히 활동 내용만 나열하지 말고, 그 활동을 통해 드러난 **[어휘력, 구문 독해력, 영작문 실력, 비판적 사고력, 의사소통 능력]**을 구체적으로 서술하십시오.
                2. **단원 및 주제 연계**: 수업 시간에 배운 지문이나 주제(Topic)가 학생의 심화 탐구 활동으로 어떻게 확장되었는지 '동기 -> 과정 -> 결과'의 흐름으로 작성하십시오.
                3. **진로 연계 심화**: 만약 입력 내용에 학생의 진로(희망 전공)가 포함되어 있다면, 영어 원서 읽기나 영문 기사 분석 등을 통해 전공 적합성을 드러내십시오. (단, 억지스러운 연결은 지양할 것)
                4. **목표 분량 준수**: 공백 포함 약 {target_length}자 (오차범위 ±10%)

                다음 두 가지 파트로 나누어 출력하세요. 구분선: "---SPLIT---"

                [Part 1] 역량별 분석 (개조식)
                - [수업참여 / 심화탐구 / 영어능력] 등으로 분류하여 요약
                
                ---SPLIT---

                [Part 2] 영어 과목 세특 (서술형 종합본)
                - 실제 생기부 입력용 줄글
                - 문체: '~함', '~임', '~보임', '~분석함' 등의 개조식과 서술형 혼용 (생기부 표준 문체).
                
                {prompt_instruction}
                """

                response = model.generate_content(system_prompt)
                full_text = response.text
                
                if "---SPLIT---" in full_text:
                    parts = full_text.split("---SPLIT---")
                    analysis_text = parts[0].strip()
                    final_text = parts[1].strip()
                else:
                    analysis_text = "영역별 분석을 생성하지 못했습니다."
                    final_text = full_text

                char_count = len(final_text)
                char_count_no_space = len(final_text.replace(" ", "").replace("\n", ""))
                
                # 바이트 계산
                byte_count = 0
                for char in final_text:
                    if ord(char) > 127: byte_count += 3
                    else: byte_count += 1
                
                st.success("작성 완료!")
                
                with st.expander("🔍 역량별 분석 내용 확인하기 (클릭)", expanded=True):
                    st.markdown(analysis_text)
                
                st.markdown("---")
                st.markdown("### 📋 최종 제출용 종합본")

                st.markdown(f"""
                <div class="count-box">
                    📊 목표: {target_length}자 | <b>실제: {char_count}자</b> (공백제외 {char_count_no_space}자)<br>
                    💾 <b>예상 바이트: {byte_count} Bytes</b> (NEIS 기준)
                </div>
                """, unsafe_allow_html=True)
                
                st.caption(f"※ {mode.split()[1]} 모드 동작 중 ({target_model})")
                st.text_area("결과 (복사해서 나이스에 붙여넣으세요)", value=final_text, height=350)

            except Exception as e:
                # 에러 메시지 처리 (429 등)
                if "429" in str(e):
                    st.error("🚨 오늘 사용 가능한 무료 AI 횟수를 모두 쓰셨습니다! (Quota exceeded)")
                elif "404" in str(e):
                    st.error("🚨 모델을 찾을 수 없습니다. (requirements.txt 버전을 확인하거나 Reboot 해주세요.)")
                else:
                    st.error(f"오류가 발생했습니다: {e}")

# --- 8. 푸터 ---
st.markdown("""
<div class="footer">
    © 2025 <b>Chaeyun with AI</b>. All rights reserved.<br>
    문의: <a href="mailto:inlove11@naver.com" style="color: #888; text-decoration: none;">inlove11@naver.com</a>
</div>
""", unsafe_allow_html=True)
