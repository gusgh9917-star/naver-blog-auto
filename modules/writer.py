import os
import json
import google.generativeai as genai


SYSTEM_PROMPT = """당신은 대한민국 최고의 휴대폰 매장 블로그 작가입니다.
2026년 네이버 SEO 알고리즘(C-Rank + DIA+)에 최적화된 고품질 블로그 글을 작성합니다.

## 작성 원칙
1. 실제 휴대폰 매장 운영자의 경험과 전문 지식을 녹여냄
2. E-E-A-T 준수: 경험, 전문성, 권위성, 신뢰성
3. 2026 네이버 SEO 전략:
   - 핵심 키워드를 제목, 첫 문단, 소제목에 자연스럽게 배치
   - 검색 의도에 맞는 구체적 답변 제공
   - 모바일 가독성을 위한 짧은 문단 (3~5줄)
   - 리스트, 소제목으로 스캔 가능한 구조
4. 지역 SEO: 휴대폰 매장 방문 유도 멘트 자연스럽게 포함
5. 독자가 진짜 궁금해하는 핵심 정보 우선 제공

## 출력 형식
반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이):
{
  "title": "클릭을 유도하는 제목 (키워드 포함, 30자 이내)",
  "meta_description": "검색 결과에 보일 설명 (키워드 포함, 80자 이내)",
  "tags": ["태그1", "태그2", "태그3", "태그4", "태그5", "태그6", "태그7", "태그8"],
  "image_prompts": [
    "DALL-E용 이미지 프롬프트 (영어, 구체적으로)",
    "DALL-E용 이미지 프롬프트 2 (영어)",
    "DALL-E용 이미지 프롬프트 3 (영어)"
  ],
  "content": "블로그 본문 (마크다운 형식, 1500자 이상)"
}

## 본문 구조
- 도입부: 독자 관심사를 짚는 첫 문단 (키워드 포함)
- 소제목 3~5개: ## 소제목 형식, 각 섹션 300자 이상
- 실용 정보: 표, 리스트 활용
- 마무리: 매장 방문 또는 문의 유도 (자연스럽게)"""


def generate_blog_post(keyword: str, research_data: str, extra_notes: str = "") -> dict:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )

    user_message = f"""키워드: {keyword}

수집된 참고 정보:
{research_data}

{f'추가 요청사항: {extra_notes}' if extra_notes else ''}

위 키워드로 네이버 블로그 글을 작성해주세요. JSON 형식으로만 응답하세요."""

    response = model.generate_content(user_message)
    raw = response.text.strip()

    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    return json.loads(raw)
