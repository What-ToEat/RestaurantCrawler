from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
 
from time import sleep
import random
import re
 
from selenium import webdriver
import sys

def switch_left():
############## iframe으로 왼쪽 포커스 맞추기 ##############
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH,'//*[@id="searchIframe"]')
    driver.switch_to.frame(iframe)

def switch_right():
############## iframe으로 오른쪽 포커스 맞추기 ##############
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH,'//*[@id="entryIframe"]')
    driver.switch_to.frame(iframe)


options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
options.add_argument('window-size=1380,900')
driver = webdriver.Chrome(options=options)
 
# 대기 시간
driver.implicitly_wait(time_to_wait=3)
 
# 반복 종료 조건
loop = True
 
# URL = 'https://map.naver.com/p/search/%EC%9D%B8%ED%95%98%EB%8C%80%20%EC%9D%8C%EC%8B%9D%EC%A0%90?c=15.23,0,0,0,dh'
SEARCH = '호평동 식당'
URL = 'https://map.naver.com/p/search/' + SEARCH
driver.get(url=URL)

def scoroll_menu_list(scroll_cnt):
    scrollable_element = driver.find_element(By.CLASS_NAME, "Ryr1F")
 
    for _ in range(scroll_cnt):
        driver.execute_script("arguments[0].scrollTop += 600;", scrollable_element)
        sleep(0.5)  # 동적 콘텐츠 로드 시간에 따라 조절

while(loop):
    switch_left()
 
    # 페이지 숫자를 초기에 체크 [ True / False ]
    # 이건 페이지 넘어갈때마다 계속 확인해줘야 함 (페이지 새로 로드 될때마다 버튼 상태 값이 바뀜)
    next_page = driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div[2]/div[2]/a[7]').get_attribute('aria-disabled')

    # ############## 맨 밑까지 스크롤 ##############
    # scrollable_element = driver.find_element(By.CLASS_NAME, "Ryr1F")
 
    # # last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
 
    # # while True:
    # for i in range(5): # 특정 장소에서 전체 스크롤 못하는 경우가 있어 강제로 스크롤 시키게 수정함 (끝까지 안나오는 경우 반복횟수 증가)
    #     # 요소 내에서 아래로 600px 스크롤
    #     driver.execute_script("arguments[0].scrollTop += 600;", scrollable_element)
    #     # 페이지 로드를 기다림
    #     sleep(0.5)  # 동적 콘텐츠 로드 시간에 따라 조절
    #     # 새 높이 계산
    #     # new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
    #     # last_height = new_height
    scoroll_menu_list(5)
 
    ############## 현재 page number 가져오기 - 1 페이지 ##############
    # 현재 페이지 번호
    page_no = driver.find_element(By.XPATH,'//a[contains(@class, "mBN2s qxokY")]').text
    # 식당 리스트
    elemets = driver.find_elements(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]//li')


    print('현재 ' + '\033[95m' + str(page_no) + '\033[0m' + ' 페이지 / '+ '총 ' + '\033[95m' + str(len(elemets)) + '\033[0m' + '개의 가게를 찾았습니다.\n')
    
    for index, e in enumerate(elemets, start=1):
        final_element = e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span")
        print(str(index) + ". " + final_element.text)
 
 
    switch_left()
 
    sleep(2)
 
    for index, e in enumerate(elemets, start=1):
        store_name = '' # 가게 이름
        category = '' # 카테고리
        new_open = '' # 새로 오픈
        
        rating = 0.0 # 평점
        visited_review = 0 # 방문자 리뷰
        blog_review = 0 # 블로그 리뷰
        store_id = '' # 가게 고유 번호
        
        address = '' # 가게 주소
        business_hours = [] # 영업 시간
        phone_num = '' # 전화번호
 
        switch_left()
 
 
        # 순서대로 값을 하나씩 클릭
        e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span").click()
 
        sleep(2)
 
        switch_right()
 
        ################### 여기부터 크롤링 시작 ##################
        title = driver.find_element(By.XPATH,'//div[@class="zD5Nm undefined"]')
        store_info = title.find_elements(By.XPATH,'//div[@class="YouOG DZucB"]/div/span')
 
 
        # 가게 이름
        store_name = title.find_element(By.XPATH,'.//div[1]/div[1]/span[1]').text
 
        # 카테고리
        category = title.find_element(By.XPATH,'.//div[1]/div[1]/span[2]').text
 
        if(len(store_info) > 2):
            # 새로 오픈
            new_open = title.find_element(By.XPATH,'.//div[1]/div[1]/span[3]').text
 
 
        ###############################
 
        review = title.find_elements(By.XPATH,'.//div[2]/span')

        # 인덱스 변수 값
        _index = 1
 
        # 리뷰 ROW의 갯수가 3개 이상일 경우 [별점, 방문자 리뷰, 블로그 리뷰] (별점이 없을 수도 있음)
        if len(review) > 2:
            rating_xpath = f'.//div[2]/span[{_index}]'
            rating_element = title.find_element(By.XPATH, rating_xpath)
            rating = rating_element.text.replace("\n", " ")
 
            _index += 1
 
        try:
            # 방문자 리뷰
            visited_review = title.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text
            
 
            # 인덱스를 다시 +1 증가 시킴
            _index += 1
 
            # 블로그 리뷰
            blog_review = title.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text
        except:
            print('------------ 리뷰 부분 오류 ------------')
 
        # 가게 id
        store_id = driver.find_element(By.XPATH,'//div[@class="flicking-camera"]/a').get_attribute('href').split('/')[4]
        # 가게 주소
        address = driver.find_element(By.XPATH,'//span[@class="LDgIH"]').text
        # 전화번호
        phone_num = driver.find_element(By.XPATH,'//span[@class="xlx7Q"]').text
    
        print(f'{index}. ' + str(store_name) + ' · ' + str(category) + str(new_open))
        print('평점 ' + str(rating) + ' / ' + visited_review + ' · ' + blog_review)
        print(f'가게 고유 번호 -> {store_id}')
        print('가게 주소 ' + str(address))
        print('가게 번호 ' + phone_num)
        print("-"*50)

        # 리뷰 크롤링
            # 방문자 리뷰 클릭
        _index = 1
        if len(review) > 2:
            _index += 1 
        title.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').click()
        
        # 리뷰 태그 크롤링
            # 리뷰 태그 전체 펼치기 (2번 밖에 안펼쳐짐)
        while True:
            try:
                driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[5]/div[3]/div[1]/div/div/div[2]/a[1]').click()
                # sleep(0.5)
            except:
                break
            # 리뷰 태그 파싱 (리뷰 태그 이름, 리뷰 태그 선택 횟수)
        review_tag_elements = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[1]/div/div/div[2]/ul/li')
        review_tags = []
        for elem in review_tag_elements:
            review_tag_name = elem.find_element(By.CLASS_NAME, 't3JSf').text
            review_tag_cnt = int(elem.find_element(By.CLASS_NAME, 'CUoLy').text.split('\n')[1])
            review_tags.append((review_tag_name, review_tag_cnt))
            print(review_tag_name, review_tag_cnt)

        # 줄글 리뷰 크롤링
        for _ in range(1):
            try:
                driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[3]/div[2]/div/a').click()
                sleep(0.2)
            except:
                break
        user_review_elements = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[3]/div[1]/ul/li')
        user_reviews = []
        for elem in user_review_elements:
            # 더보기 버튼 누르기 (이거 하면 많이 느려짐)
            # try:
            #     more_button = elem.find_element(By.CLASS_NAME, 'rvCSr')
            #     more_button.click()
            # except:
            #     pass
            user_review = elem.find_element(By.CLASS_NAME, 'zPfVt').text
            user_reviews.append(user_review)
            # print(user_review)

        print(review_tags)
        # sleep(6)
    
    switch_left()
        
    # 페이지 다음 버튼이 활성화 상태일 경우 계속 진행
    if(next_page == 'false'):
        driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div[2]/div[2]/a[7]').click()
    # 아닐 경우 루프 정지
    else:
        loop = False