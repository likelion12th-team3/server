from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os
from openai import OpenAI
from dotenv import load_dotenv

# OpenAI API 키 설정
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_text(text):
    prompt = f"다음의 뉴스 기사를 3문장으로 요약해줘.\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    summary = response.choices[0].message.content.strip()
    return summary

def news_crawling():
    categories = ["정치", "경제", "사회", "생활/문화", "세계", "IT/과학"]
    categroy_link = ['100/', '101/', '102/', '103/', '104/', '105/']

    base_url = "https://news.naver.com/section/"

    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저를 숨김 모드로 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
    chrome_options.add_argument("--disable-software-rasterizer")  # 소프트웨어 래스터라이저 비활성화

    data = {category: {"title": "", "content": "", "link": ""} for category in categories}

    for idx, category in enumerate(categories): # 연도 선택
        url = base_url + categroy_link[idx]
        category_name = category

        # 웹 크롤링 시작
        with webdriver.Chrome(options=chrome_options) as driver:
            driver.implicitly_wait(5)  # 웹페이지 로딩 될때까지 5초는 기다림
            driver.maximize_window()    # 화면 최대화
            driver.get(url)        
            time.sleep(1)
            try:
                element = driver.find_element(By.CSS_SELECTOR, "a.sa_thumb_link[data-clk='clart']")
                link = element.get_attribute('href')
                element.click()  # 해당 카테고리의 최상단 기사 링크 클릭
                # print(f"Category: {category_name}")
                time.sleep(1)  # 추가 작업을 위한 대기 시간
                title = driver.find_element(By.CSS_SELECTOR, "#title_area > span").text
                # print("Title :", title)
                content = driver.find_element(By.CSS_SELECTOR, "#dic_area").text
                summary = summarize_text(content)
                # print("Summary :", summary)

                data[category_name]["title"] = title
                data[category_name]["content"] = summary
                data[category_name]["link"] = link
                time.sleep(1)
                
            except Exception as e:
                print(f"An error occurred in category {category_name}: {e}")
            
            finally:
                driver.close()
            # break  # 테스트용으로 첫 번째 카테고리에서만 실행하도록 함
    
    driver.quit()
    # ["정치", "경제", "사회", "생활/문화", "세계", "IT/과학"]와
    # 각각의 요소를 key로 하여 title, content, link를 가져올 수 있는 딕셔너리로 반환
    return categories, data 

# news_data = news_crawling()
# print(news_data)