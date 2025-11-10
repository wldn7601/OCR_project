# OCR_project

---

## 환경
* 파이썬 3.12 버전으로 가상환경 생성
* OCR_Space api 이용
* flask
* template으로 페이지 생성

---

## 폴더 및 파일 설명

### models
SQLAlchemy를 이용해서 user 테이블 정의

users 테이블 요소
* 유저 id
* email
* 해시된 비밀번호
* 생성 일시


### routes
flask의 라우팅을 종류별로 정리

* admin_route
admin 사용자로 로그인 라우팅

* auth_route
사용자별로 회원가입, 로그인, 로그아웃 라우팅

* user_route
사용자로 로그인했을 때의 라우팅
이미지 디테일 라우팅
이미지 삭제 라우팅


### services
다른 파일에서 쓰는 서비스 정의

* file_service
업로드한 이미지가 허용된 확장자인지 판단
업로드한 이미지를 폴더에 저장

* ocrpace_service
ocr_sapce api 이용
추출한 텍스트를 json으로 변환
api 키는 .env에 저장

* parse_receipt_service
OCR에서 추출한 텍스트 정규화
OCR에서 추출한 텍스트에서 지출 금액 파싱

* preprocess_service
업로드한 이미지 전처리

### static
template에서 적용할 css, js 정의

### templates
flask에서 렌더링할 html 저으이

### main.py
실제 실행 함수

---

## 사용 방법

### 1. 페이지 접속
퍼블릭ip:5000으로 접속

### 2. 로그인 및 회원가입
관리자 로그인
* admin, admin으로 잡속
* 회원가입한 유저 확인
* 유저별로 어떤 이미지 업로드하고 영수증 금액이 얼마인지 확인

사용자 회원가입
* id, password, email 입력
* id는 중복 안됨

사용자 로그인
* 알맞은 id, password 입력
* 로그인된 유저가 아닌 사람이 url로 접속 불가

### 3. 사용자로 로그인했을 시
이미지 업로드
* png, jpg, jpeg 확장자만 업로드 가능
* 업로드 후 OCR 적용

업로드한 이미지 삭제
* 삭제 버튼을 누르면 해당 이미지 삭제
* 그럼 헤당 이미지, 전처리 이미지, 결과가 폴더에서 삭제됨

업로드 이미지 디테일
* OCR 적용한 이미지면 페이지에 표시됨
* 미리보기 사진을 누르면 해당 이미지의 디테일 정보 확인


---

### 4. 관리자로 로그인했을 시
사용자 목록 보기
* 사용자 삭제를 누르면 해당 사용자 삭제
* 업로드한 이미지, 전처리 이미지, 결과에서 유저 폴더 삭제

사용자의 정보 보기
* 해당 사용자가 어떤 이미지를 올렸는지 확인
* 해당 사용자가 영수증에서 얼마나 지불했는지 확인


