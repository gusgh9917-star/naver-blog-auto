import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from modules.researcher import gather_research
from modules.writer import generate_blog_post
from modules.image_maker import generate_images
from modules.poster import post_to_naver_blog

st.set_page_config(
    page_title="네이버 블로그 자동화",
    page_icon="📱",
    layout="wide",
)

st.title("📱 네이버 블로그 자동 포스팅")
st.caption("키워드만 입력하면 AI가 SEO 최적화 블로그 글을 작성하고 자동으로 올려드립니다.")

# ── 사이드바: 설정 ──────────────────────────────────────
with st.sidebar:
    st.header("⚙️ 설정")
    num_images = st.slider("이미지 생성 개수", 1, 3, 2)
    extra_notes = st.text_area(
        "추가 요청사항 (선택)",
        placeholder="예: 갤럭시 S25 가격 위주로, 20대 타겟, 매장 이름 '스마트폰세상' 언급",
        height=100,
    )
    auto_post = st.checkbox("생성 후 자동 포스팅", value=True)
    st.divider()
    st.caption("💡 .env 파일에 API 키를 먼저 입력해주세요")

# ── 메인: 키워드 입력 ─────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    keyword = st.text_input(
        "키워드 입력",
        placeholder="예: 갤럭시 S25 요금제 추천, 아이폰16 중고 시세, 번호이동 혜택",
        label_visibility="collapsed",
    )
with col2:
    start_btn = st.button("🚀 시작", use_container_width=True, type="primary")

st.divider()

# ── 실행 ────────────────────────────────────────────────
if start_btn and keyword:
    result_area = st.empty()
    progress = st.progress(0, text="준비 중...")
    status_box = st.empty()

    try:
        # Step 1: 정보 수집
        progress.progress(10, text="🔍 정보 수집 중...")
        status_box.info("네이버 검색으로 관련 정보를 모으고 있습니다...")
        research = gather_research(keyword)

        # Step 2: AI 글 작성
        progress.progress(30, text="✍️ AI가 글 작성 중...")
        status_box.info("Claude AI가 SEO 최적화 블로그 글을 작성 중입니다... (약 30초)")
        post_data = generate_blog_post(keyword, research, extra_notes)

        # Step 3: 이미지 생성
        progress.progress(55, text="🎨 이미지 생성 중...")
        status_box.info(f"DALL-E 3가 이미지 {num_images}장을 생성 중입니다...")
        image_paths = generate_images(post_data["image_prompts"][:num_images], keyword)

        # Step 4: 결과 미리보기
        progress.progress(75, text="📋 결과 확인 중...")
        status_box.success("글 작성 및 이미지 생성 완료!")

        with st.expander("📄 생성된 블로그 글 미리보기", expanded=True):
            st.subheader(f"제목: {post_data['title']}")
            st.caption(f"메타설명: {post_data['meta_description']}")
            st.caption(f"태그: {', '.join(post_data['tags'])}")
            st.divider()
            st.markdown(post_data["content"])

        if image_paths:
            with st.expander("🖼️ 생성된 이미지", expanded=True):
                cols = st.columns(len(image_paths))
                for i, (col, path) in enumerate(zip(cols, image_paths)):
                    with col:
                        st.image(path, caption=f"이미지 {i+1}", use_container_width=True)

        # Step 5: 자동 포스팅
        if auto_post:
            progress.progress(85, text="📤 네이버 블로그에 포스팅 중...")

            def update_status(msg):
                status_box.info(msg)

            success = post_to_naver_blog(
                title=post_data["title"],
                content=post_data["content"],
                tags=post_data["tags"],
                image_paths=image_paths,
                status_callback=update_status,
            )

            if success:
                progress.progress(100, text="✅ 완료!")
                status_box.success(
                    f"네이버 블로그 포스팅 완료! 키워드: **{keyword}**"
                )
                st.balloons()
            else:
                status_box.warning("포스팅 중 문제가 발생했습니다. 글은 저장되었으니 확인해주세요.")
        else:
            progress.progress(100, text="✅ 완료!")
            status_box.success("글과 이미지 생성 완료! (자동 포스팅 비활성화 상태)")

    except Exception as e:
        progress.empty()
        st.error(f"오류 발생: {str(e)}")
        st.info("💡 .env 파일의 API 키와 네이버 계정 정보를 확인해주세요.")

elif start_btn and not keyword:
    st.warning("키워드를 입력해주세요.")

# ── 하단 안내 ─────────────────────────────────────────────
with st.expander("📌 사용법 및 주의사항"):
    st.markdown("""
**사용법**
1. 위 키워드 입력창에 블로그 주제 키워드 입력
2. 사이드바에서 이미지 개수, 추가 요청사항 설정
3. 🚀 시작 버튼 클릭 → 자동으로 글 작성 + 이미지 생성 + 포스팅

**비용 안내 (글 1개 기준)**
- 글 작성 (Claude): 약 20~30원
- 이미지 2장 (DALL-E): 약 120원
- **총 약 150원**

**주의사항**
- 처음 실행 시 Chrome이 자동으로 열립니다 (정상)
- 네이버 로그인 보안 인증이 뜨면 수동으로 완료 후 다시 시도
- 과도한 자동 포스팅은 블로그 제재를 받을 수 있으니 하루 2~3개 권장
""")
