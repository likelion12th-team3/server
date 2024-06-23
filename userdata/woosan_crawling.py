from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, re

def woosan_crawling():
    locations = ["강남구", "관악구", "노원구", "도봉구", "동작구", "마포구", "송파구", "영등포구",  "용산구", "종로구"]
    base_url = "https://www.naver.com/"

    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저를 숨김 모드로 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
    chrome_options.add_argument("--disable-software-rasterizer")  # 소프트웨어 래스터라이저 비활성화

    data = {location: {"woosan": False, "temperature": 0} for location in locations}

    for location in locations: # 연도 선택
        # 웹 크롤링 시작
        with webdriver.Chrome(options=chrome_options) as driver:
            driver.implicitly_wait(5)  # 웹페이지 로딩 될때까지 5초는 기다림
            driver.maximize_window()   # 화면 최대화
            driver.get(base_url)        
            time.sleep(1)
            try:
                search_box = driver.find_element(By.CSS_SELECTOR, "#query")
                search_box.send_keys(f"{location} 날씨") # 검색어를 입력합니다.
                search_box.send_keys(Keys.RETURN) # 엔터 키를 누릅니다.
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, 150)")
                temp = driver.find_element(By.CSS_SELECTOR, "#main_pack > section.sc_new.cs_weather_new._cs_weather > div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today > div.weather_graphic").text
                temperature = re.findall(r'\d+\.\d+', temp) # 정규 표현식으로 온도만 추출
                # print(temperature[0])

                button = driver.find_element(By.CSS_SELECTOR, "#main_pack > section.sc_new.cs_weather_new._cs_weather > div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(2) > div > div > div.sub_tab > div > ul > li:nth-child(2)")
                button.click() # 버튼을 클릭해서 강수 부분 보이게 하기

                rain_list = driver.find_element(By.CSS_SELECTOR, "#main_pack > section.sc_new.cs_weather_new._cs_weather > div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(2) > div > div > div:nth-child(4) > div").text
                rain_list = rain_list.split('\n')[1:17] # 16시간 기준
                flag = False
                for prob in rain_list:
                    num = prob.replace("%", "")
                    if num == '-': continue
                    if int(num) > 50:
                        flag = True
                        break
                time.sleep(1)

                # 결과를 딕셔너리에 추가해넣기
                data[location]['temperature'] = temperature[0]
                data[location]['woosan'] = flag
                
            except Exception as e:
                print(f"An error occurred in category {location}: {e}")
            
            finally:
                driver.close()
            # break  # 테스트용으로 첫 번째 카테고리에서만 실행하도록 함
    driver.quit()
    # ["강남구", "관악구", "노원구", "도봉구", "동작구", "마포구", "송파구", "영등포구",  "용산구", "종로구"]와
    # 각각의 요소를 key로 하여 woosan(T/F), temperature를 가져올 수 있는 딕셔너리로 반환
    return locations, data 

# woosan = woosan_crawling()
# print(woosan)