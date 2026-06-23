import time
import requests
from pathlib import Path
from urllib.parse import quote


OUTPUT_DIR = Path("generated_images")


def generate_images(prompts: list, keyword: str) -> list:
    OUTPUT_DIR.mkdir(exist_ok=True)
    saved_paths = []
    timestamp = int(time.time())

    for i, prompt in enumerate(prompts):
        enhanced_prompt = (
            f"{prompt}, professional DSLR photography, sharp focus, "
            "high resolution, cinematic lighting, ultra detailed, "
            "Korean smartphone retail store, modern clean aesthetic, 8k quality"
        )

        try:
            encoded = quote(enhanced_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=800&nologo=true&seed={timestamp+i}&model=flux"

            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                file_name = f"{keyword}_{timestamp}_{i+1}.png"
                file_path = OUTPUT_DIR / file_name
                file_path.write_bytes(response.content)
                saved_paths.append(str(file_path.resolve()))
                print(f"이미지 {i+1} 생성 완료: {file_name}")
            else:
                print(f"이미지 {i+1} 생성 실패: 상태코드 {response.status_code}")
        except Exception as e:
            print(f"이미지 {i+1} 생성 실패: {e}")

    return saved_paths
