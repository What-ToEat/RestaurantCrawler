from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
 
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

def print_result(index, store_name, category, rating, visited_review, blog_review, store_id, address, phone_num, review_tags, user_reviews):
    print(f'{index}. ' + str(store_name) + ' · ' + str(category))
    print('평점 ' + str(rating) + ' / ' + visited_review + ' · ' + blog_review)
    print(f'가게 고유 번호 -> {store_id}')
    print('가게 주소 ' + str(address))
    print('가게 번호 ' + phone_num)
    print("-"*50)
    print(review_tags)
    print(user_reviews)

def click_restaurant_detail(e):
    switch_left()
    e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span").click()
    sleep(2)
    switch_right()

def parse_review_info(review, restaurant_info):
    rating, visited_review, blog_review = 0.0, 0, 0
    _index = 1
    if len(review) > 2:
        rating_xpath = f'.//div[2]/span[{_index}]'
        rating_element = restaurant_info.find_element(By.XPATH, rating_xpath)
        rating = rating_element.text.replace("\n", " ")
        _index += 1

    try:
        visited_review = restaurant_info.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text
        _index += 1
        blog_review = restaurant_info.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text
    except:
        print('------------ 리뷰 부분 오류 ------------')
    return rating, visited_review, blog_review

def click_review(review, restaurant_info):
    _index = 1
    if len(review) > 2:
        _index += 1 
    restaurant_info.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').click()
    sleep(1)

def parse_review_tag():
    switch_right()
    review_tags = []

    while True:
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[5]/div[3]/div[1]/div/div/div[2]/a[1]').click()
            sleep(0.5)
        except:
            break

    review_tag_elements = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[1]/div/div/div[2]/ul/li')
    
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

def parse_user_review(page_bound):
    switch_right()
    user_reviews = []
    for _ in range(page_bound):
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[3]/div[2]/div/a').click()
            sleep(0.2)
        except:
            break
    user_review_elements = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div[3]/div[3]/div[1]/ul/li')
    
    for elem in user_review_elements:
        # click_more_button(elem) # 더보기 버튼 누르기 (이거 하면 많이 느려짐)
        user_review = elem.find_element(By.CLASS_NAME, 'zPfVt').text
        user_reviews.append(user_review)
    return user_reviews

def parse_restaurant_info(index, e):
    store_name = '' # 가게 이름
    category = '' # 카테고리

    store_id = '' # 가게 고유 번호
    address = '' # 가게 주소
    phone_num = '' # 전화번호

    click_restaurant_detail(e)

    restaurant_info = driver.find_element(By.XPATH,'//div[@class="zD5Nm undefined"]')
    store_name = restaurant_info.find_element(By.XPATH,'.//div[1]/div[1]/span[1]').text
    category = restaurant_info.find_element(By.XPATH,'.//div[1]/div[1]/span[2]').text
    store_id = driver.find_element(By.XPATH,'//div[@class="flicking-camera"]/a').get_attribute('href').split('/')[4]
    address = driver.find_element(By.XPATH,'//span[@class="LDgIH"]').text
    phone_num = driver.find_element(By.XPATH,'//span[@class="xlx7Q"]').text

    review = restaurant_info.find_elements(By.XPATH,'.//div[2]/span')
    rating, visited_review, blog_review = parse_review_info(review, restaurant_info)

    click_review(review, restaurant_info)
    review_tags = parse_review_tag()
    user_reviews = parse_user_review(page_bound=REVIEW_PAGE_BOUND)

    print_result(index, store_name, category, rating, visited_review, blog_review, store_id, address, phone_num, review_tags, user_reviews)

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
options.add_argument('window-size=1380,900')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(time_to_wait=3)
loop = True
 
SEARCH = '건대 식당'
SCROLL_BOUND = 5
REVIEW_PAGE_BOUND = 1
driver.get(url='https://map.naver.com/p/search/' + SEARCH)

while(loop):
    scoroll_menu_list(SCROLL_BOUND)
    elemets = driver.find_elements(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]//li')
    print_page_info(elemets)
    print_restaurant_name(elemets)
    sleep(2)
 
    for index, e in enumerate(elemets, start=1):
        try:
            parse_restaurant_info(index, e)
        except Exception as e:
            print(e)
            # pass
    switch_left()
    next_page = driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div[2]/div[2]/a[7]').get_attribute('aria-disabled')
    if(next_page == 'false'):
        driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div[2]/div[2]/a[7]').click()
    else:
        loop = False