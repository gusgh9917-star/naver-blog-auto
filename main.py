import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from modules.researcher import gather_research
from modules.writer import generate_blog_post
from modules.image_maker import generate_images

st.set_page_config(
    page_title="휴대폰성지 옆커폰 보라매점 AI 블로그",
    page_icon="📱",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

* { font-family: 'Noto Sans KR', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

section[data-testid="stSidebar"] * { color: #fff !important; }

.hero-box { text-align: center; padding: 50px 20px 30px; }

.store-badge {
    display: inline-block;
    background: linear-gradient(90deg, #a855f7, #6366f1);
    color: white;
    font-size: 13px;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 50px;
    letter-spacing: 2px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 8px;
}

.hero-title span {
    background: linear-gradient(90deg, #a855f7, #6366f1, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub { color: rgba(255,255,255,0.5); font-size: 15px; margin-bottom: 40px; }

.copy-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 16px 20px;
    color: #fff;
    font-size: 15px;
    margin-bottom: 12px;
    word-break: break-all;
}

.label-tag {
    display: inline-block;
    background: linear-gradient(90deg, #a855f7, #6366f1);
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 50px;
    margin-bottom: 8px;
}

.step-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 10px;
    color: rgba(255,255,255,0.85);
}

.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 14px !important;
    color: #111111 !important;
    font-size: 16px !important;
    padding: 16px 20px !important;
    height: auto !important;
}

.stTextInput > div > div > input::placeholder { color: #aaaaaa !important; }
.stTextInput > div > div > input:focus {
    border-color: #a855f7 !important;
    box-shadow: 0 0 0 3px rgba(168,85,247,0.2) !important;
}

div[data-testid="stTextInput"] label { color: rgba(255,255,255,0.7) !important; }

.stButton > button {
    background: linear-gradient(135deg, #a855f7, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 14px 28px !important;
    height: auto !important;
    width: 100% !important;
    transition: all 0.3s !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(168,85,247,0.4) !important;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #a855f7, #6366f1, #06b6d4) !important;
    border-radius: 10px !important;
}

.stProgress > div > div {
    background: rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 14px !important;
    color: #fff !important;
}

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 16px !important;
}

div[data-testid="stExpander"] summary { color: #fff !important; }
p, div, label, span { color: rgba(255,255,255,0.85); }
h1, h2, h3 { color: #fff !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
header { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── 헤더 ──────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="store-badge">📱 휴대폰성지 옆커폰 보라매점</div>
    <div class="hero-title">네이버 블로그<br><span>AI 자동 작성</span></div>
    <div class="hero-sub">키워드 하나로 SEO 최적화 블로그 글 + 이미지를 자동으로 완성</div>
</div>
""", unsafe_allow_html=True)

# ── 사용 가이드 ────────────────────────────────────────────
with st.expander("📖 사용방법 가이드 (처음 사용 시 읽어주세요)", expanded=False):
    st.markdown("""
    <div style='color:rgba(255,255,255,0.85); line-height:2;'>

    **✅ 사용 순서**

    1. 키워드 입력 → 🚀 시작 클릭
    2. 약 3분 기다리기
    3. 완성된 **제목 / 태그 / 본문** 복사
    4. 네이버 블로그 글쓰기에 붙여넣기
    5. 이미지도 다운로드해서 블로그에 첨부

    ---

    **💡 키워드 예시**
    - `갤럭시 S25 요금제 추천`
    - `아이폰 16 중고 시세 2026`
    - `번호이동 혜택 보라매 휴대폰`
    - `갤럭시 S25 카메라 비교`

    ---

    **⚙️ 왼쪽 설정**
    - **이미지 개수**: 1~3장 조절 가능
    - **추가 요청사항**: "보라매점 방문 유도 포함해줘" 같은 요청 가능

    ---

    **⚠️ 주의사항**
    - 하루 2~3개 포스팅 권장
    - 생성된 글은 약간 수정 후 올리면 더 좋음

    </div>
    """, unsafe_allow_html=True)

# ── 사이드바 ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    st.markdown("---")
    num_images = st.slider("이미지 생성 개수", 1, 3, 2)
    extra_notes = st.text_area(
        "추가 요청사항",
        placeholder="예: 보라매점 방문 유도 포함, 20대 타겟으로 작성",
        height=120,
    )
    st.markdown("---")
    st.markdown("<small style='color:rgba(255,255,255,0.3)'>⚡ Powered by Gemini AI</small>", unsafe_allow_html=True)

# ── 메인 입력 ──────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    keyword = st.text_input(
        "키워드",
        placeholder="예: 갤럭시 S25 요금제 추천, 아이폰16 중고 시세, 번호이동 혜택",
        label_visibility="collapsed",
    )
with col2:
    start_btn = st.button("🚀 시작", type="primary")

st.markdown("<br>", unsafe_allow_html=True)

# ── 실행 ──────────────────────────────────────────────────
if start_btn and keyword:
    progress = st.progress(0)
    status_box = st.empty()

    try:
        progress.progress(10, text="🔍 관련 정보 수집 중...")
        status_box.info("네이버에서 관련 정보를 모으고 있습니다...")
        research = gather_research(keyword)

        progress.progress(35, text="✍️ AI가 블로그 글 작성 중...")
        status_box.info("Gemini AI가 SEO 최적화 글을 작성 중입니다... (약 20초)")
        post_data = generate_blog_post(keyword, research, extra_notes)

        progress.progress(60, text="🎨 이미지 생성 중...")
        status_box.info(f"AI가 이미지 {num_images}장을 생성 중입니다... (약 1~2분)")
        image_paths = generate_images(post_data["image_prompts"][:num_images], keyword)

        progress.progress(100, text="✅ 완성!")
        status_box.success("완성! 아래 내용을 네이버 블로그에 복사해서 붙여넣으세요.")

        st.markdown("---")

        # 제목 복사
        st.markdown('<div class="label-tag">📌 제목</div>', unsafe_allow_html=True)
        st.text_area("제목 (복사하세요)", value=post_data["title"], height=68, key="title_area", label_visibility="collapsed")

        # 태그 복사
        st.markdown('<div class="label-tag">🏷️ 태그</div>', unsafe_allow_html=True)
        tags_text = " ".join([f"#{t}" for t in post_data["tags"]])
        st.text_area("태그 (복사하세요)", value=tags_text, height=68, key="tags_area", label_visibility="collapsed")

        # 본문 복사
        st.markdown('<div class="label-tag">📝 본문</div>', unsafe_allow_html=True)
        st.text_area("본문 (복사하세요)", value=post_data["content"], height=400, key="content_area", label_visibility="collapsed")

        # 이미지 다운로드
        if image_paths:
            st.markdown("---")
            st.markdown('<div class="label-tag">🖼️ 이미지 (다운로드 후 블로그에 첨부)</div>', unsafe_allow_html=True)
            cols = st.columns(len(image_paths))
            for i, (col, path) in enumerate(zip(cols, image_paths)):
                with col:
                    st.image(path, use_container_width=True)
                    with open(path, "rb") as f:
                        st.download_button(
                            label=f"⬇️ 이미지 {i+1} 다운로드",
                            data=f,
                            file_name=f"blog_image_{i+1}.png",
                            mime="image/png",
                            key=f"dl_{i}",
                            use_container_width=True,
                        )

    except Exception as e:
        progress.empty()
        st.error(f"오류: {str(e)}")
        st.info("💡 API 키가 올바른지 확인해주세요. (관리자 문의)")

elif start_btn and not keyword:
    st.warning("키워드를 입력해주세요!")
