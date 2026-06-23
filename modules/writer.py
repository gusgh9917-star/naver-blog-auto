import os
import json
import time
import requests


SYSTEM_PROMPT_FREE = """당신은 대한민국 최고의 블로그 전문 작가이자 SEO 전문가입니다.
2026년 네이버 SEO 알고리즘(C-Rank + DIA+)에 최적화된 고품질 블로그 글을 작성합니다.
어떤 업종이든 해당 분야 전문가처럼 자연스럽고 신뢰감 있게 작성합니다.

## 제목 작성 규칙 (5개 생성)
1. 각 제목은 25~35자 이내
2. 키워드를 제목 앞쪽에 배치
3. 특수부호는 (), | 정도만 사용 - 느낌표(!) 이모티콘 절대 금지
4. 정보성 글처럼 작성 - 광고성 단어("최저가!", "지금 구매!" 등) 절대 금지
5. 각 제목은 서로 다른 각도/관점으로 작성 (비교형, 정보형, 가이드형, 경험형, 질문형)

## 본문 작성 규칙
1. 목차 3개로 구성, 각 소주제마다 500자 이상 (총 1500자 이상)
2. 각 목차는 ## 소제목으로 시작
3. 해당 업종 전문가의 경험과 지식을 자연스럽게 녹여냄
4. 모바일 가독성을 위해 3~5줄 단락으로 나누기
5. 매장/업체 방문 또는 문의 유도 멘트 자연스럽게 포함

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이):
{
  "titles": ["제목1 (25~35자)", "제목2 (25~35자)", "제목3 (25~35자)", "제목4 (25~35자)", "제목5 (25~35자)"],
  "title": "5개 중 가장 추천하는 제목",
  "meta_description": "검색 결과에 보일 설명 (키워드 포함, 80자 이내)",
  "tags": ["태그1", "태그2", "태그3", "태그4", "태그5", "태그6", "태그7", "태그8"],
  "image_prompts": [
    "대표 이미지 프롬프트 (영어, 매우 구체적으로, 고품질 사진 스타일)",
    "목차1 관련 이미지 프롬프트 (영어)",
    "목차2 관련 이미지 프롬프트 (영어)",
    "목차3 관련 이미지 프롬프트 (영어)",
    "마무리 이미지 프롬프트 (영어)"
  ],
  "content": "## 목차1 제목\\n\\n500자 이상 내용...\\n\\n## 목차2 제목\\n\\n500자 이상 내용...\\n\\n## 목차3 제목\\n\\n500자 이상 내용..."
}"""


SYSTEM_PROMPT_PREMIUM = """당신은 대한민국 최고의 블로그 전문 작가이자 SEO 전문가입니다.
2026년 네이버 SEO 알고리즘(C-Rank + DIA+)에 최적화된 최상급 블로그 글을 작성합니다.
어떤 업종이든 해당 분야 최고 전문가처럼 깊이 있고 신뢰감 있게 작성합니다.

## 제목 작성 규칙 (5개 생성)
1. 각 제목은 25~35자 이내
2. 키워드를 제목 앞쪽에 배치
3. 특수부호는 (), | 정도만 사용 - 느낌표(!) 이모티콘 절대 금지
4. 정보성 글처럼 작성 - 광고성 단어 절대 금지
5. 각 제목은 서로 다른 각도/관점으로 작성 (비교형, 정보형, 가이드형, 경험형, 질문형)
6. 클릭률을 높이는 호기심 유발 표현 사용 (낚시성 금지)

## 본문 작성 규칙 (프리미엄 고품질)
1. 목차 4개로 구성, 각 소주제마다 600자 이상 (총 2500자 이상)
2. 각 목차는 ## 소제목으로 시작, 소목차는 ### 사용
3. 해당 업종 전문가로서의 경험담과 구체적 수치/데이터 포함
4. 독자의 고민을 정확히 짚어주는 공감형 도입부 작성
5. 비교표, 체크리스트 등 스캔 가능한 구조 활용
6. 모바일 가독성을 위해 3~4줄 단락으로 나누기
7. 매장/업체 방문 유도 멘트 2회 이상 포함
8. 마지막 문단에 행동 유도(CTA) 멘트 포함
9. E-E-A-T 완벽 준수: 경험, 전문성, 권위성, 신뢰성

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이):
{
  "titles": ["제목1 (25~35자)", "제목2 (25~35자)", "제목3 (25~35자)", "제목4 (25~35자)", "제목5 (25~35자)"],
  "title": "5개 중 가장 추천하는 제목",
  "meta_description": "검색 결과에 보일 설명 (키워드 포함, 80자 이내)",
  "tags": ["태그1", "태그2", "태그3", "태그4", "태그5", "태그6", "태그7", "태그8", "태그9", "태그10"],
  "image_prompts": [
    "대표 이미지 프롬프트 (영어, 매우 구체적으로, 고품질 사진 스타일)",
    "목차1 관련 이미지 프롬프트 (영어)",
    "목차2 관련 이미지 프롬프트 (영어)",
    "목차3 관련 이미지 프롬프트 (영어)",
    "목차4 관련 이미지 프롬프트 (영어)"
  ],
  "content": "## 목차1 제목\\n\\n600자 이상 내용...\\n\\n## 목차2 제목\\n\\n600자 이상 내용...\\n\\n## 목차3 제목\\n\\n600자 이상 내용...\\n\\n## 목차4 제목\\n\\n600자 이상 내용..."
}"""


def _build_user_message(keyword, research_data, extra_notes, store_name=""):
    store_info = f"\n매장/업체명: {store_name}" if store_name else ""
    return f"""키워드: {keyword}{store_info}

수집된 참고 정보:
{research_data}

{f'추가 요청사항: {extra_notes}' if extra_notes else ''}

위 키워드로 네이버 블로그 글을 작성해주세요. JSON 형식으로만 응답하세요."""


def _parse_response(raw):
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

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

    data = json.loads(fix_json(raw))
    if "titles" not in data:
        data["titles"] = [data.get("title", "")]
    return data


def _generate_with_groq(keyword, research_data, extra_notes, store_name):
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_FREE},
            {"role": "user", "content": _build_user_message(keyword, research_data, extra_notes, store_name)},
        ],
        "temperature": 0.8,
        "max_tokens": 5000,
    }
    for attempt in range(3):
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        if response.status_code == 429:
            wait = 25
            try:
                wait = int(response.json()["error"]["message"].split("try again in ")[1].split("s.")[0].split(".")[0]) + 3
            except Exception:
                pass
            time.sleep(wait)
            continue
        if not response.ok:
            raise Exception(f"Groq 오류 {response.status_code}: {response.text}")
        raw = response.json()["choices"][0]["message"]["content"].strip()
        return _parse_response(raw)
    raise Exception("요청이 너무 많습니다. 1분 후 다시 시도해주세요.")


def _generate_with_openai(keyword, research_data, extra_notes, store_name):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("프리미엄 API 키가 설정되지 않았습니다. 관리자에게 문의하세요.")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_PREMIUM},
            {"role": "user", "content": _build_user_message(keyword, research_data, extra_notes, store_name)},
        ],
        "temperature": 0.8,
        "max_tokens": 7000,
    }
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    if not response.ok:
        raise Exception(f"OpenAI 오류 {response.status_code}: {response.text}")
    raw = response.json()["choices"][0]["message"]["content"].strip()
    return _parse_response(raw)


def generate_blog_post(keyword: str, research_data: str, extra_notes: str = "", plan: str = "free", store_name: str = "") -> dict:
    if plan == "premium":
        return _generate_with_openai(keyword, research_data, extra_notes, store_name)
    return _generate_with_groq(keyword, research_data, extra_notes, store_name)
