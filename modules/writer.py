import os
import json
import requests


SYSTEM_PROMPT = """당신은 대한민국 최고의 휴대폰 매장 블로그 전문 작가입니다.
2026년 네이버 SEO 알고리즘(C-Rank + DIA+)에 최적화된 고품질 블로그 글을 작성합니다.

## 제목 작성 규칙 (반드시 준수)
1. 25~35자 이내로 작성
2. 키워드를 제목 앞쪽에 배치
3. 특수부호는 (), | 정도만 사용 - 느낌표(!) 이모티콘 절대 금지
4. 정보성 글처럼 작성 - "최저가!", "지금 구매하세요!", "판매중" 등 광고성 단어 절대 금지
5. 제목 클릭 후 본문 내용이 제목과 일치해야 함 (체류시간 확보)

## 본문 작성 규칙 (반드시 준수)
1. 목차 3개로 구성 (소주제 3개)
2. 각 소주제마다 500자 이상 상세하게 작성 (총 1500자 이상)
3. 각 목차는 ## 소제목으로 시작
4. 실제 매장 운영자의 경험과 전문 지식을 자연스럽게 녹여냄
5. 독자가 궁금한 핵심 정보를 먼저 제공
6. 모바일 가독성을 위해 3~5줄 단락으로 나누기
7. 자연스럽게 보라매점 방문 유도 멘트 포함

## 네이버 SEO 전략
- 핵심 키워드를 제목, 첫 문단, 소제목에 자연스럽게 배치
- 검색 의도에 맞는 구체적 답변 제공
- E-E-A-T 준수: 경험, 전문성, 권위성, 신뢰성

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이):
{
  "title": "키워드가 앞에 오는 정보성 제목 (25~35자, 광고느낌 없이)",
  "meta_description": "검색 결과에 보일 설명 (키워드 포함, 80자 이내)",
  "tags": ["태그1", "태그2", "태그3", "태그4", "태그5", "태그6", "태그7", "태그8"],
  "image_prompts": [
    "DALL-E용 이미지 프롬프트 (영어, 구체적으로)",
    "DALL-E용 이미지 프롬프트 2 (영어)",
    "DALL-E용 이미지 프롬프트 3 (영어)"
  ],
  "content": "## 목차1 제목\\n\\n500자 이상 내용...\\n\\n## 목차2 제목\\n\\n500자 이상 내용...\\n\\n## 목차3 제목\\n\\n500자 이상 내용..."
}"""


def generate_blog_post(keyword: str, research_data: str, extra_notes: str = "") -> dict:
    api_key = os.getenv("GROQ_API_KEY")

    user_message = f"""키워드: {keyword}

수집된 참고 정보:
{research_data}

{f'추가 요청사항: {extra_notes}' if extra_notes else ''}

위 키워드로 네이버 블로그 글을 작성해주세요. JSON 형식으로만 응답하세요."""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    if not response.ok:
        raise Exception(f"Groq 오류 {response.status_code}: {response.text}")

    raw = response.json()["choices"][0]["message"]["content"].strip()

    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    # JSON 문자열 내 제어문자 정리
    def fix_json(s):
        result = []
        in_string = False
        escape_next = False
        for char in s:
            if escape_next:
                result.append(char)
                escape_next = False
            elif char == '\\':
                result.append(char)
                escape_next = True
            elif char == '"':
                result.append(char)
                in_string = not in_string
            elif in_string and char == '\n':
                result.append('\\n')
            elif in_string and char == '\r':
                result.append('\\r')
            elif in_string and char == '\t':
                result.append('\\t')
            else:
                result.append(char)
        return ''.join(result)

    return json.loads(fix_json(raw))
