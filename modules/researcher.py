import os
import re
import requests


def _clean_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def search_naver(keyword: str, display: int = 5) -> str:
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")

    if not client_id or not client_secret:
        return ""

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }

    results = []
    endpoints = {
        "blog": "블로그",
        "news": "뉴스",
        "webkr": "웹문서",
    }

    for endpoint, label in endpoints.items():
        url = f"https://openapi.naver.com/v1/search/{endpoint}"
        params = {"query": keyword, "display": display, "sort": "sim"}
        try:
            r = requests.get(url, headers=headers, params=params, timeout=5)
            if r.status_code == 200:
                for item in r.json().get("items", []):
                    title = _clean_html(item.get("title", ""))
                    desc = _clean_html(item.get("description", ""))
                    if title or desc:
                        results.append(f"[{label}] {title}: {desc}")
        except Exception:
            pass

    return "\n".join(results[:18])


def gather_research(keyword: str) -> str:
    naver_results = search_naver(keyword, display=6)

    research = f"""=== '{keyword}' 키워드 관련 수집 정보 ===

{naver_results if naver_results else "검색 결과 없음 (API 키 확인 필요)"}
"""
    return research
