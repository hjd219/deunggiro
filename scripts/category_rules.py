from __future__ import annotations

import re

CATEGORY_RENUNCIATION = '상속포기·한정승인'
CATEGORY_PARTITION = '상속재산분할'
CATEGORY_CORPORATE = '법인등기'
CATEGORY_FAMILY = '가사'
CATEGORY_REAL_ESTATE = '부동산등기'
CATEGORY_INHERITANCE = '상속등기'
CATEGORY_OTHER = '기타'

CORPORATE_WORDS = (
    '법인등기','법인설립','법인주소','법인 본점','법인 상호','법인 목적','법인 대표',
    '1인 법인','1인법인','주식회사','유한회사','유한책임회사','농업회사법인','영농조합법인',
    '대표이사','주주총회','이사회','본점이전','본점주소','자본금','가수금','증자','감자',
    '회사계속','해산간주','청산종결간주','합명회사','합자회사','법인인감','법인도장','정관'
)

PARTITION_WORDS = (
    '상속재산분할심판','상속재산분할청구','상속재산분할협의서','상속재산분할협의',
    '상속분쟁','기여분','특별수익','유류분','상속회복청구'
)

REAL_ESTATE_TRANSFER_WORDS = (
    '재산분할등기','부동산 이전','부동산이전','공동명의·단독명의 이전','공동명의 단독명의 이전',
    '촉탁등기','소유권이전등기','매매예약가등기','가등기','근저당','전세권',
    '등기권리증','등기필증','신탁등기','부동산 등기부','부동산등기비용','취득세율'
)

RENUNCIATION_WORDS = (
    '상속포기','한정승인','특별한정승인','상속채무','상속빚','상속 빚','상속재산파산','단순승인'
)

INHERITANCE_STRONG_WORDS = (
    '상속등기','상속절차','상속순위','상속권','대습상속','상속취득세','상속지분',
    '누가 상속인','상속인은 누구','상속받','상속예금'
)

FAMILY_WORDS = (
    '협의이혼','재판이혼','재판상이혼','이혼소송','이혼신고','숙려기간',
    '친권','양육권','양육비','면접교섭','상간남','상간녀','위자료',
    '개명','성본변경','성·본변경','성본창설','성년후견','한정후견','미성년후견'
)

REAL_ESTATE_WORDS = (
    '부동산','임차권등기','임차인','임대인','임대차','전세보증금','보증금',
    '계약갱신거절','신탁','공매','경매','매매','증여','취득세'
)

OTHER_WORDS = (
    '가압류 해방공탁','제3채무자 공탁','채권압류','공시최고','제권판결','개인회생','파산지원센터'
)

INHERITANCE_CONTEXT_WORDS = (
    '상속인','상속재산','유언','부모님 사망','부모 사망','배우자 사망',
    '남편 사망','아내 사망','형제 사망','자녀 사망'
)

DEATH_WORDS = ('사망','망인','피상속인')
MONEY_RISK_WORDS = ('예금 인출','예금인출','통장 인출','통장예금 인출','사망보험금','해지환급금','장례비','병원비')
RISK_WORDS = ('주의','위험','단순승인','영향','괜찮을까','가능할까')


def _text(value: str) -> str:
    return re.sub(r'\s+', ' ', str(value or '')).strip()


def _has_any(text: str, words: tuple[str, ...]) -> bool:
    return any(word in text for word in words)


def classify_title_with_reason(title: str, current: str = '') -> tuple[str, str]:
    """제목 중심의 보수적 분류.

    본문 앞부분의 우연한 단어 때문에 카테고리가 바뀌지 않도록 제목만 사용한다.
    현재 카테고리가 명확히 맞는 경우에는 유지하고, 충돌이 분명할 때만 변경한다.
    """
    t = _text(title)
    current = (current or '').strip()

    if _has_any(t, CORPORATE_WORDS):
        return CATEGORY_CORPORATE, 'corporate-strong'

    if _has_any(t, PARTITION_WORDS):
        return CATEGORY_PARTITION, 'inheritance-partition-explicit'

    if _has_any(t, REAL_ESTATE_TRANSFER_WORDS):
        return CATEGORY_REAL_ESTATE, 'real-estate-transfer-explicit'

    death_context = _has_any(t, DEATH_WORDS)
    money_risk = (
        death_context
        and _has_any(t, MONEY_RISK_WORDS)
        and _has_any(t, RISK_WORDS)
    )
    if money_risk:
        return CATEGORY_RENUNCIATION, 'death-money-risk'

    inheritance_overview = (
        '상속절차' in t
        and ('상속등기' in t or '해야 할 일' in t or '사망신고' in t)
        and _has_any(t, ('예금','은행','보험','자동차','주식','안심상속'))
    )
    if inheritance_overview:
        return CATEGORY_INHERITANCE, 'inheritance-overview'

    # 기존 상속포기·한정승인 글은 해당 핵심어가 있으면 불필요하게 다른 상속 카테고리로 옮기지 않는다.
    if current == CATEGORY_RENUNCIATION and _has_any(t, RENUNCIATION_WORDS):
        return current, 'keep-renunciation-supported'

    if death_context and '특별대리인' in t:
        return CATEGORY_INHERITANCE, 'death-special-representative'

    if _has_any(t, INHERITANCE_STRONG_WORDS):
        if '상속포기는 어디까지' in t:
            return CATEGORY_RENUNCIATION, 'renunciation-scope'
        return CATEGORY_INHERITANCE, 'inheritance-strong'

    if _has_any(t, RENUNCIATION_WORDS) or (death_context and '3개월' in t):
        return CATEGORY_RENUNCIATION, 'renunciation-strong'

    if _has_any(t, FAMILY_WORDS):
        return CATEGORY_FAMILY, 'family-strong'

    if _has_any(t, REAL_ESTATE_WORDS):
        return CATEGORY_REAL_ESTATE, 'real-estate-strong'

    if _has_any(t, OTHER_WORDS):
        return CATEGORY_OTHER, 'other-explicit'

    if _has_any(t, INHERITANCE_CONTEXT_WORDS):
        return CATEGORY_INHERITANCE, 'inheritance-context'

    return current or CATEGORY_OTHER, 'keep-or-other'


def classify_title(title: str, current: str = '') -> str:
    return classify_title_with_reason(title, current)[0]
