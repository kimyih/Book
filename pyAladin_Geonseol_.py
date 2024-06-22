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
import os

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"Aladin/Geonseol/Geonseol_{current_date}.json"


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
browser.get('https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord=%EA%B1%B4%EC%84%A4%EC%95%88%EC%A0%84%EA%B8%B0%EC%82%AC')

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
    title = track.select_one(".bo3").text.strip() if track.select_one(".bo3") else 'No title'
    price = track.select_one(".ss_p2").text.strip() if track.select_one(".ss_p2") else 'No price'
    
    # 이미지 파일 추출
    image_element = track.select_one(".flipcover_in img:nth-of-type(2)")
    if not image_element:  # nth-of-type(2)가 없을 경우 첫 번째 이미지 선택
        image_element = track.select_one(".flipcover_in img")
    if not image_element:  # nth-of-type(1)가 없을 때 flipcover_in lcover_none
        image_element = track.select_one(".flipcover_in lcover_none img")
    if not image_element:  # flipcover_in img가 없을 경우 cover_area_other img 선택
        image_element = track.select_one(".cover_area_other img")
        
    image_url = image_element.get('src') if image_element else None  # src에서 이미지 URL 가져오기
    link_element = track.select_one(".cover_area a")  # 링크 요소 가져오기
    href = link_element.get('href') if link_element else None  # href 속성 가져오기

    # 저자 이름 추출 (ss_book_list 안의 3번째 li 요소의 첫 번째 a 링크)
    author_element = track.select_one(".ss_book_list li:nth-of-type(3) a")
    author = author_element.text.strip() if author_element else 'No author'

    book_data.append({
        "title": title,
        "imageURL": image_url,
        "price": price,
        "url": href,
        "author": author
    })

print(book_data)

# 데이터를 JSON 파일로 저장
if book_data:  # 데이터가 비어있지 않은 경우에만 저장
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, ensure_ascii=False, indent=4)
else:
    print("No data to save.")

# 브라우저 종료
browser.quit()
