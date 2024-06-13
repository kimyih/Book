from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"Aladin/Hansik/Hansik_{current_date}.json"

# 웹드라이버 설치
options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless")  # Headless 모드 추가
options.add_argument("--no-sandbox")  # Sandbox 모드 비활성화
options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화
options.add_argument("--disable-gpu")  # GPU 비활성화
options.add_argument("--window-size=1920x1080")  # 윈도우 크기 설정
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)


# URL 열기
browser.get('https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord=%ED%95%9C%EC%8B%9D%EC%A1%B0%EB%A6%AC%EA%B8%B0%EB%8A%A5%EC%82%AC')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "Search3_Result"))
)
# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')
# 데이터 추출
book_data = []
# 첫 번째 tracks
tracks = soup.select("#Search3_Result .ss_book_box")
for track in tracks:
        title = track.select_one(".bo3").text.strip()
        price = track.select_one(".ss_p2").text.strip()
        # 이미지 요소가 로드될 때까지 대기
            # 이미지 파일 추출
        image_element = track.select_one(".flipcover_in img:nth-of-type(2)")
        if not image_element:  # nth-of-type(2)가 없을 경우 첫 번째 이미지 선택
            image_element = track.select_one(".flipcover_in img")
        image_url = image_element.get('src') if image_element else None
        if not image_element: # nth-of-type(1)가 없을 때 flipcover_in lcover_none
            image_element = track.select_one(".flipcover_in lcover_none img")
        if not image_element:  # flipcover_in img가 없을 경우 cover_area_other img 선택
            image_element = track.select_one(".cover_area_other img")
            image_url = image_element.get('src') if image_element else None

        
        image_url = image_element.get('src') if image_element else None  # src에서 이미지 URL 가져오기
        link_element = track.select_one(".cover_area a")  # 링크 요소 가져오기
        href = link_element.get('href') if link_element else None  # href 속성 가져오기
        book_data.append({
            "title": title,
            "imageURL": image_url,
            "price" : price,
            "url" : href
        })
print(book_data)
# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(book_data, f, ensure_ascii=False, indent=4)
# 브라우저 종료
browser.quit()
