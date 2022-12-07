from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchFrameException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)
review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'
review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_num_path = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
# // *[ @ id = "old_content"] / ul / li[1] / a
# // *[ @ id = "old_content"] / ul / li[2] / a

your_year = 2022
for page in range(1, 32):
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_year, page)
    titles = [] # 페이지마다 저장하겠다.
    reviews = []
    try:
        for title_num in range(1, 21):
            driver.get(url)  # 페이지 열기
            time.sleep(0.1)
            # 영화 제목 클릭
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(title_num)
            title = driver.find_element('xpath', movie_title_xpath).text
            print('title', title)
            driver.find_element('xpath', movie_title_xpath).click()
            time.sleep(0.1)
            # 리뷰 버튼 클릭
            try:
                driver.find_element('xpath', review_button_xpath).click()
                time.sleep(0.1)
                # 각 리뷰의 제목 클릭

                review_num = driver.find_element('xpath', review_num_path).text
                review_num = review_num.replace(',', '')
                review_range = (int(review_num) -1) // 10 + 1
                if review_range > 3:
                    review_range = 3
                for review_page in range(1, review_range + 1):

                    review_page_button_xpath = '//*[@id="pagerTagAnchor{}"]'.format(review_page)
                    driver.find_element('xpath', review_page_button_xpath).click()
                    time.sleep(0.1)


                    for review_title_num in range(1, 11):
                        review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(review_title_num)
                        driver.find_element('xpath', review_title_xpath).click()
                        time.sleep(0.1)
                        try:
                            # 각 리뷰의 내용 불러오기

                            review = driver.find_element('xpath', review_xpath).text
                            titles.append(title) # 타이틀이랑 리뷰는 같이 저장해야한다.
                            reviews.append(review)
                            driver.back() # 리뷰 읽은 후 뒤로 가야하기에 사용
                        except:
                            print('review', page, title_num, review_title_num)
                            driver.back()

            except:
                print('review button', page, title_num)
        df = pd.DataFrame({'titles':titles, 'reviews':reviews})
        df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, page), index=False)
    except:
        print('error', page, title_num)