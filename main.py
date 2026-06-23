import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from modules.researcher import gather_research
from modules.writer import generate_blog_post
from modules.image_maker import generate_images

st.set_page_config(
    page_title="옆커폰 AI 블로그",
    page_icon="📱",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
* { font-family: 'Noto Sans KR', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #060611 0%, #0d0820 50%, #060e1a 100%);
    min-height: 100vh;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.8) !important; }

/* 히어로 */
.hero { text-align: center; padding: 60px 20px 40px; }
.hero-badge {
    display: inline-block;
    background: rgba(168,85,247,0.15);
    border: 1px solid rgba(168,85,247,0.4);
    color: #c084fc;
    font-size: 12px;
    font-weight: 700;
    padding: 5px 16px;
    border-radius: 50px;
    letter-spacing: 2px;
    margin-bottom: 24px;
    backdrop-filter: blur(10px);
}
.hero-title {
    font-size: 52px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 12px;
}
.hero-title .grad {
    background: linear-gradient(90deg, #a855f7, #6366f1, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub { color: rgba(255,255,255,0.4); font-size: 15px; margin-bottom: 50px; }

/* 플랜 카드 */
.plan-grid { display: flex; gap: 16px; margin-bottom: 32px; }
.plan-card {
    flex: 1;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 24px;
    transition: all 0.3s;
}
.plan-card.premium {
    background: rgba(168,85,247,0.08);
    border: 1px solid rgba(168,85,247,0.3);
}
.plan-name { font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 6px; }
.plan-price { font-size: 26px; font-weight: 900; color: #a855f7; margin-bottom: 14px; }
.plan-feature { font-size: 13px; color: rgba(255,255,255,0.6); line-height: 1.9; }
.plan-feature span { color: #22d3ee; }

/* 입력 */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 16px !important;
    color: #ffffff !important;
    font-size: 16px !important;
    padding: 16px 20px !important;
    backdrop-filter: blur(10px);
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.3) !important; }
.stTextInput > div > div > input:focus {
    border-color: #a855f7 !important;
    box-shadow: 0 0 0 3px rgba(168,85,247,0.15) !important;
}
div[data-testid="stTextInput"] label { color: rgba(255,255,255,0.6) !important; }

/* 버튼 */
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
    box-shadow: 0 4px 20px rgba(168,85,247,0.3) !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(168,85,247,0.5) !important;
}

/* 프로그레스 */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #a855f7, #6366f1, #22d3ee) !important;
    border-radius: 10px !important;
}
.stProgress > div > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}

/* 텍스트 영역 */
.stTextArea textarea {
    background: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #111111 !important;
    font-size: 14px !important;
}

/* 라벨 */
.label-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(168,85,247,0.15);
    border: 1px solid rgba(168,85,247,0.3);
    color: #c084fc;
    font-size: 12px;
    font-weight: 700;
    padding: 5px 14px;
    border-radius: 50px;
    margin-bottom: 10px;
    backdrop-filter: blur(10px);
}

/* 유리 카드 */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 16px;
}

/* 구분선 */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* 익스팬더 */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(10px);
}
div[data-testid="stExpander"] summary { color: rgba(255,255,255,0.7) !important; }

/* 텍스트 색상 */
p, div, label, span { color: rgba(255,255,255,0.8); }
h1, h2, h3 { color: #fff !important; }
.stMarkdown p { color: rgba(255,255,255,0.8); }

/* 숨기기 */
footer, #MainMenu, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stHeader"] { visibility: hidden !important; height: 0 !important; }
div[class*="viewerBadge"], div[class*="badge"], a[href*="streamlit.io"] { display: none !important; }

/* 슬라이더 */
.stSlider [data-baseweb="slider"] [role="slider"] { background: #a855f7 !important; }

/* 알림 */
.stAlert { border-radius: 14px !important; backdrop-filter: blur(10px); }
</style>
""", unsafe_allow_html=True)

PREMIUM_PASSWORD = os.getenv("PREMIUM_PASSWORD", "")

# ── 헤더 ──────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">📱 휴대폰성지 옆커폰 보라매점</div>
    <div class="hero-title">네이버 블로그<br><span class="grad">AI 자동 작성</span></div>
    <div class="hero-sub">키워드 하나로 SEO 최적화 블로그 글 + 이미지를 자동으로 완성</div>
</div>
""", unsafe_allow_html=True)

# ── 플랜 비교 ──────────────────────────────────────────────
st.markdown("""
<div class="plan-grid">
    <div class="plan-card">
        <div class="plan-name">🆓 무료 버전</div>
        <div class="plan-price">무료</div>
        <div class="plan-feature">
            <span>✓</span> AI: Groq Llama 3.3<br>
            <span>✓</span> 이미지: 최대 5장<br>
            <span>✓</span> 글 길이: 1,500자<br>
            <span>✓</span> 목차 3개 구성<br>
            <span>✓</span> 하루 무제한 생성<br>
            ⭐⭐⭐
        </div>
    </div>
    <div class="plan-card premium">
        <div class="plan-name">💎 프리미엄 버전</div>
        <div class="plan-price">월 39,900원</div>
        <div class="plan-feature">
            <span>✓</span> AI: GPT-4o (최고급)<br>
            <span>✓</span> 이미지: 최대 5장<br>
            <span>✓</span> 글 길이: 2,500자+<br>
            <span>✓</span> 목차 4개 + 소목차<br>
            <span>✓</span> 하루 무제한 생성<br>
            ⭐⭐⭐⭐⭐
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 플랜 선택 ──────────────────────────────────────────────
col_free, col_premium = st.columns(2)
with col_free:
    free_btn = st.button("🆓 무료 버전 사용", key="free_plan")
with col_premium:
    premium_btn = st.button("💎 프리미엄 버전 사용", key="premium_plan")

if free_btn:
    st.session_state["plan"] = "free"
    st.session_state["premium_verified"] = False
if premium_btn:
    st.session_state["plan"] = "premium"

if "plan" not in st.session_state:
    st.session_state["plan"] = "free"

current_plan = st.session_state.get("plan", "free")

if current_plan == "premium" and not st.session_state.get("premium_verified", False):
    st.markdown("---")
    pw = st.text_input("🔒 프리미엄 비밀번호를 입력하세요", type="password", key="pw_input")
    if st.button("확인", key="pw_confirm"):
        if pw == PREMIUM_PASSWORD and PREMIUM_PASSWORD:
            st.session_state["premium_verified"] = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")

plan_verified = current_plan == "free" or st.session_state.get("premium_verified", False)

if plan_verified:
    if current_plan == "premium":
        st.success("💎 프리미엄 버전 사용 중 | GPT-4o 고품질 AI")
    else:
        st.info("🆓 무료 버전 사용 중 | Groq Llama 3.3 AI")

st.markdown("---")

# ── 사이드바 ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    st.markdown("---")

    st.markdown("<div style='color:rgba(255,255,255,0.7); font-size:14px; margin-bottom:6px;'>📎 내 이미지 첨부 (선택)</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:rgba(255,255,255,0.4); font-size:12px; margin-bottom:8px;'>첨부하면 AI 이미지 대신 내 사진 사용</div>", unsafe_allow_html=True)
    uploaded_images = st.file_uploader(
        "이미지 업로드",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    st.markdown("---")
    if not uploaded_images:
        num_images = st.slider("AI 이미지 생성 개수", 1, 5, 5)
    else:
        num_images = 0
        st.markdown(f"<div style='color:#a855f7; font-size:13px;'>✅ 내 이미지 {len(uploaded_images)}장 사용</div>", unsafe_allow_html=True)

    st.markdown("---")
    store_name = st.text_input(
        "매장/업체명 (선택)",
        placeholder="예: 옆커폰 보라매점, 강남 카페 OO, 홍대 미용실 OO",
        key="store_name_input",
    )
    extra_notes = st.text_area(
        "추가 요청사항",
        placeholder="예: 방문 유도 포함, 20대 타겟으로 작성",
        height=100,
    )
    st.markdown("---")
    plan_label = "💎 Powered by GPT-4o" if current_plan == "premium" else "⚡ Powered by Groq AI"
    st.markdown(f"<small style='color:rgba(255,255,255,0.3)'>{plan_label}</small>", unsafe_allow_html=True)

# ── 사용 가이드 ────────────────────────────────────────────
with st.expander("📖 사용방법 가이드 (처음 사용 시 읽어주세요)", expanded=False):
    st.markdown("""
    <div style='color:rgba(255,255,255,0.8); line-height:2;'>

    **✅ 사용 순서**
    1. 플랜 선택 (무료 / 프리미엄)
    2. 키워드 입력 → 🚀 시작 클릭
    3. 약 2~3분 기다리기
    4. 완성된 **제목 / 태그 / 본문** 복사
    5. 네이버 블로그 글쓰기에 붙여넣기
    6. 이미지도 다운로드해서 블로그에 첨부

    ---
    **💡 키워드 예시**
    - `갤럭시 S25 요금제 추천`
    - `아이폰 16 중고 시세 2026`
    - `번호이동 혜택 보라매 휴대폰`

    ---
    **⚠️ 주의사항**
    - 하루 2~3개 포스팅 권장
    - 생성된 글은 약간 수정 후 올리면 더 좋음

    </div>
    """, unsafe_allow_html=True)

# ── 메인 입력 ──────────────────────────────────────────────
if plan_verified:
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

            ai_name = "GPT-4o" if current_plan == "premium" else "Groq AI"
            progress.progress(35, text=f"✍️ {ai_name}가 블로그 글 작성 중...")
            status_box.info(f"{ai_name}가 SEO 최적화 글을 작성 중입니다... (약 20~30초)")
            store_name = st.session_state.get("store_name_input", "")
            post_data = generate_blog_post(keyword, research, extra_notes, plan=current_plan, store_name=store_name)

            if uploaded_images:
                progress.progress(70, text="📎 업로드한 이미지 불러오는 중...")
                status_box.info(f"업로드한 이미지 {len(uploaded_images)}장을 사용합니다.")
                image_paths = None
            else:
                progress.progress(60, text="🎨 이미지 생성 중...")
                status_box.info(f"AI가 이미지 {num_images}장을 생성 중입니다... (약 1~2분)")
                image_paths = generate_images(post_data["image_prompts"][:num_images], keyword)

            progress.progress(100, text="✅ 완성!")
            status_box.success("완성! 아래 내용을 네이버 블로그에 복사해서 붙여넣으세요.")

            st.markdown("---")

            # 제목 5개
            st.markdown('<div class="label-chip">📌 추천 제목 5개 (골라서 사용하세요)</div>', unsafe_allow_html=True)
            titles = post_data.get("titles", [post_data.get("title", "")])
            for i, t in enumerate(titles):
                st.text_area(f"제목 {i+1}", value=t, height=60, key=f"title_{i}", label_visibility="collapsed")

            # 태그
            st.markdown('<div class="label-chip">🏷️ 태그</div>', unsafe_allow_html=True)
            tags_text = " ".join([f"#{t}" for t in post_data["tags"]])
            st.text_area("태그", value=tags_text, height=68, key="tags_area", label_visibility="collapsed")

            # 본문
            st.markdown('<div class="label-chip">📝 본문</div>', unsafe_allow_html=True)
            st.text_area("본문", value=post_data["content"], height=500, key="content_area", label_visibility="collapsed")

            # 이미지
            st.markdown("---")
            st.markdown('<div class="label-chip">🖼️ 이미지 (블로그에 첨부)</div>', unsafe_allow_html=True)

            if uploaded_images:
                cols = st.columns(min(len(uploaded_images), 3))
                for i, img_file in enumerate(uploaded_images):
                    with cols[i % 3]:
                        st.image(img_file, use_container_width=True)
                        st.download_button(
                            label=f"⬇️ 이미지 {i+1}",
                            data=img_file.getvalue(),
                            file_name=img_file.name,
                            mime=img_file.type,
                            key=f"ul_{i}",
                            use_container_width=True,
                        )
            elif image_paths:
                cols = st.columns(min(len(image_paths), 3))
                for i, path in enumerate(image_paths):
                    with cols[i % 3]:
                        st.image(path, use_container_width=True)
                        with open(path, "rb") as f:
                            st.download_button(
                                label=f"⬇️ 이미지 {i+1}",
                                data=f,
                                file_name=f"blog_image_{i+1}.png",
                                mime="image/png",
                                key=f"dl_{i}",
                                use_container_width=True,
                            )

        except Exception as e:
            progress.empty()
            st.error(f"오류: {str(e)}")
            st.info("💡 잠시 후 다시 시도하거나 관리자에게 문의하세요.")

    elif start_btn and not keyword:
        st.warning("키워드를 입력해주세요!")
