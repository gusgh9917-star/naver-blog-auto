import os
import time
import random
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def _delay(min_sec=0.8, max_sec=1.8):
    time.sleep(random.uniform(min_sec, max_sec))


def _make_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--window-size=1400,900")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def _login(driver: webdriver.Chrome, naver_id: str, naver_pw: str):
    driver.get("https://nid.naver.com/nidlogin.login?mode=form")
    wait = WebDriverWait(driver, 15)

    id_field = wait.until(EC.presence_of_element_located((By.ID, "id")))
    _delay()
    id_field.click()
    # 자동입력 방지를 위해 JS로 값 설정
    driver.execute_script(f"document.getElementById('id').value = '{naver_id}'")
    _delay(0.3, 0.6)

    pw_field = driver.find_element(By.ID, "pw")
    pw_field.click()
    driver.execute_script(f"document.getElementById('pw').value = '{naver_pw}'")
    _delay(0.5, 1.0)

    login_btn = driver.find_element(By.ID, "log.login")
    login_btn.click()
    _delay(2, 3)

    # 보안 캡차나 추가 인증 화면 체크
    if "nidlogin" in driver.current_url or "captcha" in driver.current_url:
        raise Exception(
            "로그인 실패: 보안 인증이 필요합니다. 브라우저에서 직접 네이버에 로그인 후 다시 시도해주세요."
        )


def _convert_markdown_to_blog(content: str) -> str:
    """마크다운을 네이버 블로그 붙여넣기용 텍스트로 변환"""
    lines = content.split("\n")
    result = []
    for line in lines:
        if line.startswith("## "):
            result.append(f"\n【 {line[3:]} 】\n")
        elif line.startswith("### "):
            result.append(f"\n▶ {line[4:]}\n")
        elif line.startswith("# "):
            result.append(f"\n★ {line[2:]} ★\n")
        elif line.startswith("- ") or line.startswith("* "):
            result.append(f"  • {line[2:]}")
        elif line.startswith("**") and line.endswith("**"):
            result.append(f"[ {line[2:-2]} ]")
        else:
            result.append(line)
    return "\n".join(result)


def _type_in_editor(driver: webdriver.Chrome, wait: WebDriverWait, text: str):
    """SmartEditor ONE에 텍스트 입력"""
    # SmartEditor ONE iframe 전환
    try:
        # 외부 mainFrame으로 전환
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mainFrame")))
    except Exception:
        pass

    _delay(2, 3)

    # 에디터 내 contenteditable 영역 찾기
    editor_selectors = [
        "div.se-content",
        "div[contenteditable='true']",
        ".se-main-container",
        "#content_area",
    ]

    editor = None
    for selector in editor_selectors:
        try:
            editor = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            if editor:
                break
        except Exception:
            continue

    if not editor:
        raise Exception("에디터 영역을 찾을 수 없습니다.")

    editor.click()
    _delay(0.5, 1)

    # 클립보드를 통해 텍스트 붙여넣기
    pyperclip.copy(text)
    _delay(0.3, 0.5)
    editor.send_keys(Keys.CONTROL, "a")
    _delay(0.2, 0.4)
    editor.send_keys(Keys.CONTROL, "v")
    _delay(1, 2)


def _upload_image(driver: webdriver.Chrome, wait: WebDriverWait, image_path: str):
    """이미지 업로드"""
    try:
        # 이미지 추가 버튼 클릭
        img_btn_selectors = [
            "button[data-type='image']",
            ".se-toolbar-item-image button",
            "button[title*='사진']",
            "button[aria-label*='이미지']",
        ]
        img_btn = None
        for sel in img_btn_selectors:
            try:
                img_btn = driver.find_element(By.CSS_SELECTOR, sel)
                if img_btn:
                    break
            except Exception:
                continue

        if img_btn:
            img_btn.click()
            _delay(1, 2)

        # 파일 input 찾아서 경로 전달
        file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        for fi in file_inputs:
            try:
                fi.send_keys(image_path)
                _delay(2, 3)
                break
            except Exception:
                continue
    except Exception as e:
        print(f"이미지 업로드 실패: {e}")


def post_to_naver_blog(
    title: str,
    content: str,
    tags: list,
    image_paths: list,
    status_callback=None,
) -> bool:
    naver_id = os.getenv("NAVER_ID")
    naver_pw = os.getenv("NAVER_PW")
    blog_id = os.getenv("NAVER_BLOG_ID")

    if not all([naver_id, naver_pw, blog_id]):
        raise Exception(".env 파일에 NAVER_ID, NAVER_PW, NAVER_BLOG_ID를 입력해주세요.")

    driver = _make_driver()
    wait = WebDriverWait(driver, 20)

    try:
        if status_callback:
            status_callback("네이버 로그인 중...")
        _login(driver, naver_id, naver_pw)

        if status_callback:
            status_callback("블로그 글쓰기 페이지 이동 중...")

        write_url = f"https://blog.naver.com/{blog_id}/postwrite"
        driver.get(write_url)
        _delay(3, 5)

        # mainFrame 전환
        try:
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mainFrame")))
            _delay(2, 3)
        except Exception:
            pass

        # 제목 입력
        if status_callback:
            status_callback("제목 입력 중...")
        title_selectors = [
            "input.se-title-input",
            "input[placeholder*='제목']",
            ".blog2_subtitle input",
            "#subject",
        ]
        title_field = None
        for sel in title_selectors:
            try:
                title_field = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                )
                if title_field:
                    break
            except Exception:
                continue

        if title_field:
            title_field.click()
            _delay(0.3, 0.6)
            title_field.clear()
            title_field.send_keys(title)
            _delay(0.5, 1)

        # 본문 입력
        if status_callback:
            status_callback("본문 내용 입력 중...")

        blog_text = _convert_markdown_to_blog(content)

        editor_selectors = [
            "div.se-content",
            "div[contenteditable='true']",
            ".se-main-container",
        ]
        editor = None
        for sel in editor_selectors:
            try:
                editor = driver.find_element(By.CSS_SELECTOR, sel)
                if editor:
                    break
            except Exception:
                continue

        if editor:
            editor.click()
            _delay(0.5, 1)
            pyperclip.copy(blog_text)
            _delay(0.3, 0.5)
            editor.send_keys(Keys.CONTROL, "v")
            _delay(2, 3)

        # 이미지 업로드
        if image_paths:
            if status_callback:
                status_callback(f"이미지 {len(image_paths)}장 업로드 중...")
            for img_path in image_paths[:3]:
                _upload_image(driver, wait, img_path)

        # 태그 입력
        if status_callback:
            status_callback("태그 입력 중...")
        tag_selectors = [
            "input.tag_input",
            "input[placeholder*='태그']",
            ".tag_area input",
        ]
        tag_field = None
        for sel in tag_selectors:
            try:
                tag_field = driver.find_element(By.CSS_SELECTOR, sel)
                if tag_field:
                    break
            except Exception:
                continue

        if tag_field:
            for tag in tags[:8]:
                tag_field.click()
                tag_field.send_keys(tag)
                _delay(0.2, 0.4)
                tag_field.send_keys(Keys.RETURN)
                _delay(0.3, 0.6)

        # 발행
        if status_callback:
            status_callback("포스팅 발행 중...")
        _delay(1, 2)

        publish_selectors = [
            "button.publish_btn",
            "button[data-action='publish']",
            "button[class*='publish']",
            "button:contains('발행')",
        ]
        published = False
        for sel in publish_selectors:
            try:
                btn = driver.find_element(By.CSS_SELECTOR, sel)
                if btn:
                    btn.click()
                    published = True
                    _delay(2, 3)
                    break
            except Exception:
                continue

        if not published:
            # XPath로 '발행' 텍스트 버튼 찾기
            try:
                btn = driver.find_element(
                    By.XPATH, "//button[contains(text(),'발행')]"
                )
                btn.click()
                _delay(2, 3)
                published = True
            except Exception:
                pass

        _delay(2, 3)

        # 발행 확인 팝업 처리
        try:
            confirm_btn = driver.find_element(
                By.XPATH, "//button[contains(text(),'확인')]"
            )
            confirm_btn.click()
            _delay(2, 3)
        except Exception:
            pass

        return True

    except Exception as e:
        raise e
    finally:
        _delay(2, 3)
        driver.quit()
