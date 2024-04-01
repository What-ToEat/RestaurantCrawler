import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd

SEARCHES = ['건대 카폐', '건대 식당']
LOCATE = "건대"
# SEARCH = '건대 식당'
SCROLL_BOUND = 20
REVIEW_PAGE_BOUND = 5
 
def switch_left():
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH,'//*[@id="searchIframe"]')
    driver.switch_to.frame(iframe)

def switch_right():
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH,'//*[@id="entryIframe"]')
    driver.switch_to.frame(iframe)

def scoroll_menu_list(scroll_cnt):
    switch_left()
    scrollable_element = driver.find_element(By.CLASS_NAME, "Ryr1F")
 
    for _ in range(scroll_cnt):
        driver.execute_script("arguments[0].scrollTop += 600;", scrollable_element)
        sleep(0.5)  # 동적 콘텐츠 로드 시간에 따라 조절

def print_restaurant_name(restaurant_elements):
    for index, e in enumerate(restaurant_elements, start=1):
        final_element = e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span")
        print(str(index) + ". " + final_element.text)

def print_page_info(elemets):
    page_no = driver.find_element(By.XPATH,'//a[contains(@class, "mBN2s qxokY")]').text
    print('현재 ' + '\033[95m' + str(page_no) + '\033[0m' + ' 페이지 / '+ '총 ' + '\033[95m' + str(len(elemets)) + '\033[0m' + '개의 가게를 찾았습니다.\n')

def print_result(index, store_name, category, rating, visited_review, blog_review, store_id, address, phone_num, image_url, review_tags, user_reviews):
    print(f'{index}. ' + str(store_name) + ' · ' + str(category))
    print('평점 ' + str(rating) + ' / ' + str(visited_review) + ' · ' + str(blog_review))
    print(f'가게 고유 번호 -> {store_id}')
    print('가게 주소 ' + str(address))
    print('가게 번호 ' + phone_num)
    print('이미지 주소 ', image_url)
    print("-"*50)
    print(review_tags)
    print(user_reviews)

def click_restaurant_detail(e):
    switch_left()
    e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span").click()
    sleep(2)
    switch_right()

def parse_review_count(str):
    return int(str.split(" ")[1].replace(",", ""))

def parse_review_info(review, restaurant_info):
    rating, visited_review, blog_review = 0.0, 0, 0
    _index = 1
    if len(review) > 2:
        rating_xpath = f'.//div[2]/span[{_index}]'
        rating_element = restaurant_info.find_element(By.XPATH, rating_xpath)
        rating = rating_element.text.split("\n")[1]
        _index += 1

    try:
        visited_review = parse_review_count(restaurant_info.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text)
        _index += 1
        blog_review = parse_review_count(restaurant_info.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text)
    except:
        print('------------ 리뷰 부분 오류 ------------')
    return rating, visited_review, blog_review

def click_review(review, restaurant_info):
    _index = 1
    if len(review) > 2:
        _index += 1 
    restaurant_info.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').click()


def parse_review_tag():
    for i in range(7):
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[5]/div[3]/div[1]/div/div/div[2]/a[1]').click()
            # sleep(0.5)
        except:
            break
    review_tag_elements = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[1]/div/div/div[2]/ul/li')
    review_tags = []
    for elem in review_tag_elements:
        review_tag_name = elem.find_element(By.CLASS_NAME, 't3JSf').text
        review_tag_cnt = int(elem.find_element(By.CLASS_NAME, 'CUoLy').text.split('\n')[1])
        review_tags.append((review_tag_name, review_tag_cnt))
    return review_tags

def click_more_button(elem):
    try:
        more_button = elem.find_element(By.CLASS_NAME, 'rvCSr')
        more_button.click()
    except:
        pass

def click_other(page_bound):
    while True:
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[5]/div[3]/div[1]/div/div/div[2]/a[1]').click()
            sleep(0.5)
        except:
            break
    for _ in range(page_bound):
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[3]/div[2]/div/a').click()
            sleep(1)
        except:
            break


def parse_user_review(page_bound):
    for _ in range(page_bound):
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[3]/div[2]/div/a').click()
            sleep(1)
        except:
            break
    user_review_elements = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[3]/div[1]/ul/li')
    user_reviews = []
    for elem in user_review_elements:
        user_review = elem.find_element(By.CLASS_NAME, 'zPfVt').text
        if user_review.endswith("..."):
            click_more_button(elem)
            user_review = elem.find_element(By.CLASS_NAME, 'zPfVt').text
        user_reviews.append(user_review)
    return user_reviews

def parse_image_url():
    try:
        attribute = driver.find_element(By.CLASS_NAME, 'K0PDV').get_attribute('style')
        pattern = r'background-image: url\("([^"]+)"\)'
        match = re.search(pattern, attribute)
        image_url = match.group(1)
        return image_url
    except:
        return ''

def parse_restaurant_info(index, e):
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

    click_restaurant_detail(e)

    title = driver.find_element(By.XPATH,'//div[@class="zD5Nm undefined"]')
    image_url = parse_image_url()
    store_info = title.find_elements(By.XPATH,'//div[@class="YouOG DZucB"]/div/span')
    store_name = title.find_element(By.XPATH,'.//div[1]/div[1]/span[1]').text
    category = title.find_element(By.XPATH,'.//div[1]/div[1]/span[2]').text
    review = title.find_elements(By.XPATH,'.//div[2]/span')
    store_id = driver.find_element(By.XPATH,'//div[@class="flicking-camera"]/a').get_attribute('href').split('/')[4]
    address = driver.find_element(By.XPATH,'//span[@class="LDgIH"]').text
    phone_num = driver.find_element(By.XPATH,'//span[@class="xlx7Q"]').text

    rating, visited_review, blog_review = parse_review_info(review, title)

    click_review(review, title)

    review_tags = parse_review_tag()
    user_reviews = parse_user_review(page_bound=REVIEW_PAGE_BOUND)
    data = {"name": store_name, "category": category, "rating": rating, "visited_review": visited_review, "blog_review": blog_review, "store_id": store_id, "address": address, "phone_num": phone_num, "image_url": image_url, "locate": LOCATE, "review_tags": review_tags, "user_reviews": user_reviews}
    # print_result(index, store_name, category, rating, visited_review, blog_review, store_id, address, phone_num, image_url, review_tags, user_reviews)
    return data

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
options.add_argument('window-size=1380,900')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(time_to_wait=3)

for search in SEARCHES:
    loop = True
    driver.get(url='https://map.naver.com/p/search/' + search)
    restaurant_data = []
    while(loop):
        scoroll_menu_list(SCROLL_BOUND)
        elemets = driver.find_elements(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]//li')
        page_no = driver.find_element(By.XPATH,'//a[contains(@class, "mBN2s qxokY")]').text
        print_page_info(elemets)
        # print_restaurant_name(elemets)
        sleep(2)

        for index, e in enumerate(elemets, start=1):
            try:
                data = parse_restaurant_info(index, e)
                restaurant_data.append(data)
                pd.DataFrame(restaurant_data).to_csv("restaurants/" + search + ".csv", index=False)
                print('[' + search + '] 현재페이지 : 6/' + str(page_no) + ' //  식당 : ', index)
            except:
                print('>>>>>>>>>>Error<<<<<<<<<')

        switch_left()
        next_page = driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div[2]/div[2]/a[7]').get_attribute('aria-disabled')
        if(next_page == 'false'):
            driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div[2]/div[2]/a[7]').click()
        else:
            loop = False

    pd.DataFrame(restaurant_data).to_csv("./restaurants/" + search + ".csv", index=False)
