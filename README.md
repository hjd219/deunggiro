# 등기로 홈페이지 CMS 설치

이 폴더의 파일을 GitHub 저장소 `hjd219/deunggiro`의 main 브랜치 루트에 업로드하면 됩니다.

## 업로드 파일
- index.html : 메인 홈페이지
- posts.html : 법률정보 전체 목록
- admin.html : 관리자 글쓰기
- data/posts.json : 글 목록 데이터
- posts/ : 개별 글 HTML 생성 폴더

## 관리자 사용
1. https://www.deunggiro.kr/admin.html 접속
2. GitHub Fine-grained Personal Access Token 입력
3. 제목·카테고리·요약·본문 작성
4. `GitHub에 게시하기` 클릭
5. `data/posts.json`과 `posts/<slug>.html`이 자동 커밋됨
6. GitHub Pages 배포 후 홈페이지에 자동 노출

## GitHub 토큰 권한
- Repository access: Only select repositories → `deunggiro`
- Repository permissions → Contents: Read and write
- 토큰을 HTML 소스에 직접 적지 마세요.

## SEO
각 글은 `/posts/영문주소.html` 형태의 실제 정적 HTML 파일로 생성됩니다.
title, description, keywords, canonical, Open Graph 메타태그가 개별 글에 자동 추가됩니다.

## 주의
`admin.html` 주소 자체는 공개될 수 있습니다. 실제 게시 권한은 GitHub 토큰이 있어야 합니다.
공용 PC에서는 토큰을 입력하지 마세요.


## 관리자 글 관리 기능
- 새 글 작성
- 기존 글 목록 조회
- 기존 글 수정
- 기존 글 삭제
- 삭제 시 posts HTML과 posts.json 목록에서 함께 제거
