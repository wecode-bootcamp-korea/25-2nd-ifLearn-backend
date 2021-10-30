
# INFLEARN Clone Project (MECOOK)
  동영상 강의 플랫폼 사이트인 inflearn 웹사이트 클론.

## 개발 기간 / 개발 인원
  개발 기간: 2021-10-18 ~ 2021-10-29
  <br>
  개발 인원: 김민찬(**백엔드**), 김주형(**백엔드**)
  김경현(**프론트엔트**), 김동휘(**프론트엔트**), 손호영(**프론트엔트**), 이상철(**프론트엔트**)
  
## DB modeling

<img src="https://postfiles.pstatic.net/MjAyMTEwMzBfMjc2/MDAxNjM1NTc1MTkzNTcx.MhGhVuEczWb8Q1jw1yjCDhchxGWykIcc5vzxcjUpMcQg.MfxufIrupy7msmjW8aOgZbU3BKQXyKU4JfDsKwNYHiYg.PNG.km0192/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7_2021-10-30_%EC%98%A4%ED%9B%84_3.26.30.png?type=w966">
<img src="https://postfiles.pstatic.net/MjAyMTEwMzBfMjI3/MDAxNjM1NTc1MTY3NjQ1.kFDsH5jkFVmLGvWiSki1bMlv3RihqbWtHW6PXd6jlG4g.c0SknOUPm50BuP5wchYQkO4-rOJctJtwNUufdSt0010g.PNG.km0192/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7_2021-10-30_%EC%98%A4%ED%9B%84_3.26.02.png?type=w966">


## Technologies (BackEnd)
* Python
* Django
* MySQL
* jwt, bcrypt
* AWS RDS, S3
* Git, Github
* Slack, Trello

## Features
**김민찬**
* 동영상 스트리밍 API (``GET``)
* 동영상 학습 페이지 API (``GET``)
* 상품 이미지 API (AWS S3) (``GET``)
* 학습완료 영상 표시 (``GET``)
* 쿼리파라미터 없이 URL 파라미터만으로 처리


**김주형**
* 


## Endpoint
* ``GET`` /courses/categories (navbar 카테고리 데이터)
* ``GET`` /courses/video/<int:course_id> (영상 학습페이지 데이터)
* ``GET`` /courses/video/detail/<int:lecture_id> (렉쳐 1개의 데이터)
* ``GET`` /all (?)
* ``GET`` /courses/<int:category_id>
* ``GET`` /coruses/<int:category_id>/<int:sub_category_id> (?)
* ``GET`` /course/<int:course_id> (?)
* ``GET`` /courses/<path> (동영상 스트리밍용 데이터)
