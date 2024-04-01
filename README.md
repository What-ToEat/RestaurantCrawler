# RestaurantCrawler

네이버 지도에서 식당 정보와 리뷰를 긁어오는 크롤러

- 네이버 지도가 동적 페이지라 selenium을 사용
- csv 형식으로 저장

## 사용법

1. `pip install selenium pandas`
2. root 경로에 `restaurants` 폴더 생성
3. 상수 설정
   - `SEARCHES` : 네이버 지도에 검색할 키워드들을 배열에 저장. 반복문으로 돌면서 담긴 검색어들을 크롤링 함.
   - `SCROLL_BOUND` : 한 페이지에서 얼마나 스크롤 할지. 모두 긁으려면 20 정도가 적당하다.
   - `REVIEW_PAGE_BOUND` : 방문자리뷰를 얼마나 가져올지, 1번에 더보기 한번을 누른다. (기본으로 10개, REVIEW_PAGE_BOUND 1개 당 10 추가)
   - `LOCATE` : 본인이 크롤링하려는 지역 ex) 건대, 홍대, 강남, 신촌 등..
4. 실행

## 주의사항

- 가끔식 크롬창을 봐줘야댐. -> 오류 생겨서 크롬에서 다음으로 안넘어갈수도 있음
- 되도록이면 크롬창을 항상 보이게 합시다.
- 한 크롬창에서 계속 크롤링 할 경우 처음 검색어는 괜찮은데 다음 검색어부터 오류가 많이 나서 검색어 마다 크롬창을 새로 키도록 수정했음.

## 결과

- `{SEARCH}.csv` 형식으로 파일 생성
- 컬럼 종류
  - name : 식당이름
  - category : 식당 종류
  - rating : 별점
  - visited_review : 방문자 리뷰 수
  - blog_review : 블로그 리뷰 수
  - store_id : 가게 고유 번호
  - address : 주소
  - phone_num : 전화번호
  - image_url : 대표 이미지 url
  - locate : 지역이름 ex) 건대, 홍대, 강남
  - review_tags : 리뷰 태그
  - user_reviews : 방문자 리뷰
