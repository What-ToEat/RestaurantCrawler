# RestaurantCrawler

## 사용법

1. `pip install selenium pandas`
2. root 경로에 `restaurants` 폴더 생성
3. 상수 설정
   - `SEARCH` : 네이버 지도에 검색할 키워드
   - `SCROLL_BOUND` : 한 페이지에서 얼마나 스크롤 할지. 모두 긁으려면 20 정도가 적당하다.
   - `REVIEW_PAGE_BOUND` = 방문자리뷰를 얼마나 가져올지, 1번에 더보기 한번을 누른다. (기본으로 10개, REVIEW_PAGE_BOUND 1개 당 10 추가)
4. 실행

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
  - review_tags : 리뷰 태그
  - user_reviews : 방문자 리뷰
