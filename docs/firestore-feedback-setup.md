# 등기로 도움 평가: Firestore 설정 및 집계

## 적용 코드 (2026-10-25)
- /assets/feedback-v1.js : 동일 스크립트로 글별, 계산기별, 자동작성기별 평가창 표시 및 투표 처리
- /assets/feedback-v1.css : 모바일 포함 공통 디자인, PDF 출력시 숨김
- 개별 글: /assets/site-shell.js 가 모든 /posts/*.html 에서 자동 로드
- 계산기: acquisition-calculator.html, corporate-calculator.html, renunciation-calculator.html
- 자동작성: inheritance.html (4단계), family.html (출력 및 저장 안내)
- Firestore (기존 프로젝트): project-b08e5f3c-fa49-4ae6-933
- 문서: /feedback/{id}; 예: feedback/calc-acquisition, feedback/writer-divorce,
  feedback/post-inheritance-incheon-29s7ds
- 필드: helpful (좋아요 수), unhelpful (아쉬워요 수). 값은 Firestore atomic increment로 누적됩니다.
- 개인정보, 문서 내용, 입력값, IP 주소는 별도로 전송하거나 저장하지 않습니다.
  Firebase / 네트워크 제공자의 기술적 로그까지 수집하지 않는다는 의미는 아닙니다.
- 방문자에게 집계 숫자를 공개하지 않습니다. Firebase 콘솔에서만 현재 합계를 확인합니다.
- 브라우저 localStorage로 같은 대상에 한 번만 투표하도록 안내합니다.
  **이것은 강력한 부정투표 방지가 아닙니다** (브라우저 초기화/개발자 도구/봇 우회 가능).
- Firestore 기존 카운터(counters/calculator, counters/pdf)는 전혀 수정하지 않습니다.

## 반드시 확인할 Firestore Security Rules

이 저장소의 GitHub 작업만으로 Firebase 콘솔에 Security Rules를 배포할 수는 없습니다.
기존에 /feedback/{id} 비인증 쓰기를 허용하지 않았다면 버튼은 표시되지만 저장은 실패합니다.
Firebase Console > Firestore Database > Rules 에서 **기존 서비스 규칙을 보존**하며
다음 match 블록만 기존 \`match /databases/{database}/documents { ... }\` 블록 안에 추가하고
Rules Playground에서 create/update를 테스트한 후 Publish하십시오.
외부에 무제한 공개 쓰기를 허용하는 설계의 남용 가능성을 반드시 고려하십시오.

\`\`\`firestore-rules
match /feedback/{id} {
  function validId() {
    return id.matches('^(calc|writer|post)-[a-z0-9_-]{1,130}$');
  }
  function validData() {
    return request.resource.data.keys().hasOnly(['helpful', 'unhelpful']) &&
      request.resource.data.keys().hasAny(['helpful', 'unhelpful']) &&
      request.resource.data.get('helpful', 0) is int &&
      request.resource.data.get('unhelpful', 0) is int &&
      request.resource.data.get('helpful', 0) >= 0 &&
      request.resource.data.get('unhelpful', 0) >= 0;
  }
  allow get, list, delete: if false;
  allow create: if validId() && validData() && (
    (request.resource.data.get('helpful', 0) == 1 &&
     request.resource.data.get('unhelpful', 0) == 0) ||
    (request.resource.data.get('helpful', 0) == 0 &&
     request.resource.data.get('unhelpful', 0) == 1)
  );
  allow update: if validId() && validData() &&
    request.resource.data.diff(resource.data).affectedKeys().hasOnly(['helpful', 'unhelpful']) &&
    (
      (request.resource.data.get('helpful', 0) == resource.data.get('helpful', 0) + 1 &&
       request.resource.data.get('unhelpful', 0) == resource.data.get('unhelpful', 0)) ||
      (request.resource.data.get('unhelpful', 0) == resource.data.get('unhelpful', 0) + 1 &&
       request.resource.data.get('helpful', 0) == resource.data.get('helpful', 0))
    );
}
\`\`\`

**주의:** 위 코드는 익명 투표 작동에 필요한 최소 쓰기 제한 예시이며,
자동화된 반복 투표를 강하게 막지는 못합니다. 전체 Firestore 규칙 파일을 덮어쓰지 마십시오.
신뢰할 수 있는 외부 공개 지표를 만들려면 서버 측 속도 제한, CAPTCHA/App Check,
Firebase Authentication 또는 Cloudflare Worker 도입을 별도로 검토해야 합니다.

## 기능 확인 (실제 투표는 관리자 테스트로 1건만)

1. 모바일 /acquisition-calculator.html 에서 결과 아래에 작은 평가창이 나오는지 확인
2. 실제 👍 또는 👎 클릭 후 '평가해 주셔서 감사합니다.' 표시 확인
3. Firebase Console > Firestore > Data > feedback > calc-acquisition 문서에서
   해당 숫자가 1 증가했는지 확인
4. 새로고침 후 같은 대상의 버튼이 비활성화되는지 확인
5. 자동작성기의 완료 단계에만 평가창이 나타나는지 확인
6. /posts/ 아래 개별글에서 추천 글 위에 표시되는지 확인
7. HTTP 403/PERMISSION_DENIED이면 Firestore Rules 게시 여부 확인

지금은 실시간 투표·저장 성공을 브라우저에서 직접 검증하지 못했으므로
권한 설정 전에는 완료로 간주하지 마십시오.
