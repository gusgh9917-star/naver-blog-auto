import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from modules.researcher import gather_research
from modules.writer import generate_blog_post
from modules.image_maker import generate_images
from modules.poster import post_to_naver_blog

st.set_page_config(
    page_title="옆커폰 보라매점 | 블로그 자동화",
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

section[data-testid="stSidebar"] * {
    color: #fff !important;
}

.hero-box {
    text-align: center;
    padding: 50px 20px 30px;
}

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

.hero-sub {
    color: rgba(255,255,255,0.5);
    font-size: 15px;
    margin-bottom: 40px;
}

.glass-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 20px;
}

.stat-row {
    display: flex;
    gap: 16px;
    justify-content: center;
    margin-bottom: 40px;
}

.stat-item {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 16px 28px;
    text-align: center;
    color: white;
}

.stat-num {
    font-size: 28px;
    font-weight: 900;
    background: linear-gradient(90deg, #a855f7, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    margin-top: 2px;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 14px !important;
    color: #fff !important;
    font-size: 16px !important;
    padding: 16px 20px !important;
    height: auto !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255,255,255,0.3) !important;
}

.stTextInput > div > div > input:focus {
    border-color: #a855f7 !important;
    box-shadow: 0 0 0 3px rgba(168,85,247,0.2) !important;
}

div[data-testid="stTextInput"] label {
    color: rgba(255,255,255,0.7) !important;
}

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
    letter-spacing: 0.5px;
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

.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #a855f7, #6366f1) !important;
}

.stCheckbox > label {
    color: rgba(255,255,255,0.8) !important;
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

div[data-testid="stExpander"] summary {
    color: #fff !important;
}

.success-box {
    background: linear-gradient(135deg, rgba(168,85,247,0.2), rgba(99,102,241,0.2));
    border: 1px solid rgba(168,85,247,0.4);
    border-radius: 16px;
    padding: 20px;
    color: white;
    text-align: center;
    font-weight: 600;
}

.step-badge {
    display: inline-block;
    background: linear-gradient(90deg, #a855f7, #6366f1);
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 50px;
    margin-right: 8px;
}

p, div, label, span {
    color: rgba(255,255,255,0.85);
}

h1, h2, h3 { color: #fff !important; }

.stAlert { border-radius: 14px !important; }

div[data-testid="stMarkdownContainer"] {
    color: rgba(255,255,255,0.85) !important;
}
</style>
""", unsafe_allow_html=True)

# ── 헤더 ──────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="store-badge">📱 휴대폰성지 옆커폰 보라매점</div>
    <div class="hero-title">네이버 블로그<br><span>AI 자동 포스팅</span></div>
    <div class="hero-sub">키워드 하나로 SEO 최적화 블로그 글 + 이미지를 자동으로 완성</div>
    <div class="stat-row">
        <div class="stat-item">
            <div class="stat-num">3분</div>
            <div class="stat-label">포스팅 1개 완성</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">0원</div>
            <div class="stat-label">완전 무료</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">2026</div>
            <div class="stat-label">SEO 최적화</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 사이드바 ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    st.markdown("---")
    num_images = st.slider("이미지 생성 개수", 1, 3, 2)
    extra_notes = st.text_area(
        "추가 요청사항",
        placeholder="예: Galaxy S25 가격 위주로, 20대 타겟, 매장 이름 '옆커폰' 언급",
        height=120,
    )
    auto_post = st.checkbox("생성 후 자동 포스팅", value=True)
    st.markdown("---")
    st.markdown("<small style='color:rgba(255,255,255,0.3)'>⚡ Powered by Gemini AI</small>", unsafe_allow_html=True)

# ── 메인 입력 ──────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    keyword = st.text_input(
        "키워드",
        placeholder="예: 갤럭시 S25 요금제 추천, 아이폰16 중고 시세, 번호이동 혜택 2026",
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

        progress.progress(30, text="✍️ AI가 블로그 글 작성 중...")
        status_box.info("Gemini AI가 SEO 최적화 글을 작성 중입니다... (약 20초)")
        post_data = generate_blog_post(keyword, research, extra_notes)

        progress.progress(55, text="🎨 이미지 생성 중...")
        status_box.info(f"AI가 이미지 {num_images}장을 생성 중입니다... (약 1~2분)")
        image_paths = generate_images(post_data["image_prompts"][:num_images], keyword)

        progress.progress(75, text="✅ 글 & 이미지 완성!")
        status_box.success("완성! 아래에서 확인하세요.")

        with st.expander("📄 생성된 블로그 글 보기", expanded=True):
            st.markdown(f"### {post_data['title']}")
            st.caption(f"📌 {post_data['meta_description']}")
            st.caption(f"🏷️ {' · '.join(post_data['tags'])}")
            st.divider()
            st.markdown(post_data["content"])

        if image_paths:
            with st.expander("🖼️ 생성된 이미지", expanded=True):
                cols = st.columns(len(image_paths))
                for i, (col, path) in enumerate(zip(cols, image_paths)):
                    with col:
                        st.image(path, use_container_width=True)

        if auto_post:
            progress.progress(85, text="📤 네이버 블로그에 올리는 중...")

            def update_status(msg):
                status_box.info(f"📤 {msg}")

            success = post_to_naver_blog(
                title=post_data["title"],
                content=post_data["content"],
                tags=post_data["tags"],
                image_paths=image_paths,
                status_callback=update_status,
            )

            if success:
                progress.progress(100, text="🎉 포스팅 완료!")
                st.markdown(f"""
                <div class="success-box">
                    🎉 네이버 블로그 포스팅 완료!<br>
                    <small>키워드: {keyword}</small>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
        else:
            progress.progress(100, text="✅ 완료!")

    except Exception as e:
        progress.empty()
        st.error(f"오류: {str(e)}")
        st.info("💡 .env 파일의 API 키와 네이버 계정 정보를 확인해주세요.")

elif start_btn and not keyword:
    st.warning("키워드를 입력해주세요!")
