import functions_framework

import os

import json

import html

import re

import urllib.request

import urllib.error
import hmac
import hashlib
import base64
import time

from datetime import date, datetime, timezone, timedelta

from calendar import monthrange

from flask import jsonify, make_response

from google.cloud import documentai

from google.cloud import firestore
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_auth_requests

# =========================================================

# 기본 설정

# =========================================================

PROJECT_ID = "project-b08e5f3c-fa49-4ae6-933"

LOCATION = "us"

PROCESSOR_ID = "a0437f7fd3ec77f5"

OFFICER_COLLECTION = "officerManagement"

ALLOWED_ORIGINS = {

    "https://www.deunggiro.kr",

    "https://deunggiro.kr",

}

MAX_FILE_SIZE = 15 * 1024 * 1024

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "").strip()

RESEND_API_URL = "https://api.resend.com/emails"

EMAIL_FROM = "등기로 임원관리 <notice@deunggiro.kr>"

ALERT_TYPE = "expiry_1_month"

ADMIN_EMAIL = "hjd21@naver.com"
ADMIN_PASSWORD = os.environ.get("OFFICER_ADMIN_PASSWORD", "")
ADMIN_TOKEN_SECRET = os.environ.get("OFFICER_ADMIN_TOKEN_SECRET", ADMIN_PASSWORD)
ADMIN_TOKEN_TTL_SECONDS = 8 * 60 * 60

# Abuse protection
ADMIN_LOGIN_MAX_FAILURES = 5
ADMIN_LOGIN_LOCK_SECONDS = 15 * 60
ADMIN_LOGIN_ATTEMPT_COLLECTION = "adminLoginAttempts"
OCR_RATE_LIMIT_MAX_REQUESTS = 20
OCR_RATE_LIMIT_WINDOW_SECONDS = 60 * 60
OCR_RATE_LIMIT_COLLECTION = "ocrRateLimits"

# Cloud Scheduler -> /alerts/run 전용 OIDC 인증
SCHEDULER_SERVICE_ACCOUNT = "209298170572-compute@developer.gserviceaccount.com"
SCHEDULER_AUDIENCE = "https://deunggiro-ocr-209298170572.asia-northeast3.run.app"

# =========================================================
# 관리자 인증
# =========================================================

def _b64url_encode(data):
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")

def _b64url_decode(value):
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)

def _make_admin_token(email):
    payload = {
        "email": email,
        "exp": int(time.time()) + ADMIN_TOKEN_TTL_SECONDS,
    }
    body = _b64url_encode(
        json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )
    signature = hmac.new(
        ADMIN_TOKEN_SECRET.encode("utf-8"),
        body.encode("ascii"),
        hashlib.sha256,
    ).digest()
    return body + "." + _b64url_encode(signature)

def _verify_admin_token(token):
    if not token or "." not in token or not ADMIN_TOKEN_SECRET:
        return False
    try:
        body, signature = token.split(".", 1)
        expected = hmac.new(
            ADMIN_TOKEN_SECRET.encode("utf-8"),
            body.encode("ascii"),
            hashlib.sha256,
        ).digest()
        supplied = _b64url_decode(signature)
        if not hmac.compare_digest(expected, supplied):
            return False
        payload = json.loads(_b64url_decode(body).decode("utf-8"))
        return (
            payload.get("email") == ADMIN_EMAIL
            and int(payload.get("exp", 0)) >= int(time.time())
        )
    except Exception:
        return False

CUSTOMER_SAVE_TOKEN_TTL_SECONDS = 15 * 60

def _customer_company_key(value):
    value = str(value or "").strip()
    return re.sub(r"\s*\([^()]*[A-Za-z][^()]*\)\s*$", "", value).strip()

def _make_customer_save_token(company, registration_number):
    if not ADMIN_TOKEN_SECRET:
        return ""
    payload = {
        "company": _customer_company_key(company),
        "registrationNumber": str(registration_number or "").strip(),
        "exp": int(time.time()) + CUSTOMER_SAVE_TOKEN_TTL_SECONDS,
        "purpose": "customer_officer_save",
    }
    body = _b64url_encode(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    signature = hmac.new(ADMIN_TOKEN_SECRET.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
    return body + "." + _b64url_encode(signature)

def _verify_customer_save_token(token):
    if not token or "." not in token or not ADMIN_TOKEN_SECRET:
        return None
    try:
        body, signature = token.split(".", 1)
        expected = hmac.new(ADMIN_TOKEN_SECRET.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
        supplied = _b64url_decode(signature)
        if not hmac.compare_digest(expected, supplied):
            return None
        payload = json.loads(_b64url_decode(body).decode("utf-8"))
        if payload.get("purpose") != "customer_officer_save" or int(payload.get("exp", 0)) < int(time.time()):
            return None
        return payload
    except Exception:
        return None

def _admin_authorized(request):
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return False
    return _verify_admin_token(header[7:].strip())

def require_admin(request):
    if _admin_authorized(request):
        return None
    return response_json(request, {"error": "관리자 인증이 필요합니다."}, 401)

def _scheduler_authorized(request):
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return False
    token = header[7:].strip()
    if not token:
        return False
    try:
        claims = google_id_token.verify_oauth2_token(
            token,
            google_auth_requests.Request(),
            SCHEDULER_AUDIENCE,
        )
        issuer = claims.get("iss")
        email = str(claims.get("email") or "").lower()
        email_verified = claims.get("email_verified") is True
        return (
            issuer in {"https://accounts.google.com", "accounts.google.com"}
            and email_verified
            and hmac.compare_digest(email, SCHEDULER_SERVICE_ACCOUNT.lower())
        )
    except Exception:
        return False

def require_scheduler(request):
    if _scheduler_authorized(request):
        return None
    return response_json(request, {"error": "Scheduler 인증이 필요합니다."}, 401)

def _client_ip(request):
    forwarded = str(request.headers.get("X-Forwarded-For") or "").split(",", 1)[0].strip()
    return forwarded or str(request.remote_addr or "unknown").strip() or "unknown"


def _rate_key(scope, request, identity=""):
    raw = f"{scope}|{_client_ip(request)}|{str(identity or '').strip().lower()}"
    secret = ADMIN_TOKEN_SECRET or PROJECT_ID
    return hmac.new(secret.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()


def _login_rate_state(request, email):
    key = _rate_key("admin-login", request, email)
    ref = firestore_db.collection(ADMIN_LOGIN_ATTEMPT_COLLECTION).document(key)
    snap = ref.get()
    data = snap.to_dict() or {} if snap.exists else {}
    now = int(time.time())
    locked_until = int(data.get("lockedUntil") or 0)
    if locked_until > now:
        return ref, True
    if locked_until and locked_until <= now:
        ref.delete()
    return ref, False


def _record_login_failure(ref):
    transaction = firestore_db.transaction()

    @firestore.transactional
    def update_in_transaction(transaction):
        snap = ref.get(transaction=transaction)
        data = snap.to_dict() or {} if snap.exists else {}
        now = int(time.time())
        locked_until = int(data.get("lockedUntil") or 0)
        if locked_until and locked_until <= now:
            failures = 0
        else:
            failures = int(data.get("failures") or 0)
        failures += 1
        payload = {"failures": failures, "updatedAt": firestore.SERVER_TIMESTAMP}
        if failures >= ADMIN_LOGIN_MAX_FAILURES:
            payload["lockedUntil"] = now + ADMIN_LOGIN_LOCK_SECONDS
        transaction.set(ref, payload, merge=True)
        return failures

    return update_in_transaction(transaction)


def _ocr_rate_limited(request):
    key = _rate_key("ocr", request)
    ref = firestore_db.collection(OCR_RATE_LIMIT_COLLECTION).document(key)
    transaction = firestore_db.transaction()

    @firestore.transactional
    def update_in_transaction(transaction):
        snap = ref.get(transaction=transaction)
        data = snap.to_dict() or {} if snap.exists else {}
        now = int(time.time())
        window_start = int(data.get("windowStart") or 0)
        count = int(data.get("count") or 0)
        if not window_start or now - window_start >= OCR_RATE_LIMIT_WINDOW_SECONDS:
            window_start, count = now, 0
        if count >= OCR_RATE_LIMIT_MAX_REQUESTS:
            return True
        transaction.set(ref, {
            "windowStart": window_start,
            "count": count + 1,
            "updatedAt": firestore.SERVER_TIMESTAMP,
        }, merge=True)
        return False

    return update_in_transaction(transaction)


def admin_login(request):
    if not ADMIN_PASSWORD or not ADMIN_TOKEN_SECRET:
        return response_json(
            request,
            {"error": "관리자 인증 환경변수가 설정되지 않았습니다."},
            503,
        )
    data = request.get_json(silent=True) or {}
    email = str(data.get("email") or "").strip().lower()
    password = str(data.get("password") or "")
    rate_ref, locked = _login_rate_state(request, email)
    if locked:
        return response_json(request, {"error": "로그인 시도가 너무 많습니다. 15분 후 다시 시도해주세요."}, 429)
    email_ok = hmac.compare_digest(email, ADMIN_EMAIL.lower())
    password_ok = hmac.compare_digest(password, ADMIN_PASSWORD)
    if not (email_ok and password_ok):
        failures = _record_login_failure(rate_ref)
        if failures >= ADMIN_LOGIN_MAX_FAILURES:
            return response_json(request, {"error": "로그인 시도가 너무 많습니다. 15분 후 다시 시도해주세요."}, 429)
        return response_json(request, {"error": "아이디 또는 비밀번호가 올바르지 않습니다."}, 401)
    rate_ref.delete()
    return response_json(
        request,
        {"ok": True, "token": _make_admin_token(ADMIN_EMAIL), "expiresIn": ADMIN_TOKEN_TTL_SECONDS},
        200,
    )

# =========================================================

# Firestore

# 실제 데이터베이스 ID = default

# =========================================================

firestore_db = firestore.Client(

    project=PROJECT_ID,

    database="default"

)

# =========================================================

# CORS

# =========================================================

def cors_headers(request):

    origin = request.headers.get("Origin", "")

    if origin in ALLOWED_ORIGINS:

        allow_origin = origin

    else:

        allow_origin = "https://www.deunggiro.kr"

    return {

        "Access-Control-Allow-Origin": allow_origin,

        "Access-Control-Allow-Methods":

            "GET, POST, PATCH, DELETE, OPTIONS",

        "Access-Control-Allow-Headers":

            "Content-Type, Authorization",

        "Vary": "Origin",

    }

# =========================================================

# 공통 JSON 응답

# =========================================================

def response_json(request, data, status=200):

    response = make_response(

        jsonify(data),

        status

    )

    for key, value in cors_headers(request).items():

        response.headers[key] = value

    return response

# =========================================================

# 관리대장 저장

#

# POST /officers/save

# =========================================================

def save_officers(request):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):

        return response_json(

            request,

            {

                "ok": False,

                "error": "JSON 요청이 필요합니다."

            },

            400

        )

    items = data.get("items")

    customer_claims=None
    if not _admin_authorized(request):
        customer_claims=_verify_customer_save_token(data.get("saveToken"))
        if not customer_claims:
            return response_json(request,{"ok":False,"error":"유효한 분석 인증이 필요합니다. 등기사항증명서를 다시 분석해 주세요."},401)

    if not isinstance(items, list) or not items:

        return response_json(

            request,

            {

                "ok": False,

                "error": "저장할 임원 정보가 없습니다."

            },

            400

        )

    try:

        saved_ids = []

        skipped = []

        # 회사 식별/중복 판정: 회사명 + 법인등록번호만 사용
        # 같은 회사가 이미 있으면 기존 임원행을 이번 분석 결과로 갱신한다.
        prepared = []
        company_keys = set()

        for item in items:
            if not isinstance(item, dict):
                continue

            company = str(item.get("company") or "").strip()
            registration_number = str(item.get("registrationNumber") or "").strip()
            officer_name = str(item.get("officer") or item.get("name") or "").strip()
            position = str(item.get("position") or "").strip()
            term_start = str(
                item.get("termStart")
                or item.get("event_date")
                or item.get("registration_date")
                or ""
            ).strip()
            expiry = str(item.get("expiry") or "").strip()
            phone = str(item.get("phone") or "").strip()
            email = str(item.get("email") or "").strip()
            source = str(item.get("source") or "기존고객").strip()

            if not company or not registration_number or not officer_name or not position:
                continue

            company_keys.add((company, registration_number))
            prepared.append({
                "company": company,
                "registrationNumber": registration_number,
                "officer": officer_name,
                "position": position,
                "termStart": term_start,
                "expiry": expiry,
                "phone": phone,
                "email": email,
                "source": source,
            })

        if customer_claims:
            tc=_customer_company_key(customer_claims.get("company")); tr=str(customer_claims.get("registrationNumber") or "").strip()
            if not prepared or any(_customer_company_key(x["company"])!=tc or x["registrationNumber"]!=tr for x in prepared):
                return response_json(request,{"ok":False,"error":"분석 결과와 저장 요청의 회사 정보가 일치하지 않습니다."},403)

        # 기존 등록 여부는 회사명 + 법인등록번호로만 확인
        # 동일 회사면 기존 행을 삭제하고 현재 등기부 분석 결과 전체로 교체
        for company, registration_number in company_keys:
            existing_docs = list(
                firestore_db.collection(OFFICER_COLLECTION)
                .where("company", "==", company)
                .where("registrationNumber", "==", registration_number)
                .stream()
            )
            for doc in existing_docs:
                doc.reference.delete()

        # 한 회사의 여러 임원은 모두 저장
        for item in prepared:
            doc_ref = firestore_db.collection(OFFICER_COLLECTION).document()
            doc_ref.set({
                **item,
                "createdAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP,
            })
            saved_ids.append(doc_ref.id)

        # =====================================================

        # 실제 저장된 데이터 없음

        # =====================================================

        if not saved_ids:

            return response_json(

                request,

                {

                    "ok": False,

                    "error":

                        "저장 가능한 임원 정보가 없습니다."

                },

                400

            )

        # =====================================================

        # 저장 성공

        # =====================================================

        return response_json(

            request,

            {

                "ok": True,

                "savedCount":

                    len(saved_ids),

                "skippedCount":

                    len(skipped),

                "savedIds":

                    saved_ids

            },

            200

        )

    except Exception as e:

        print(

            "Firestore officer save error:",

            repr(e)

        )

        return response_json(

            request,

            {

                "ok": False,

                "error":

                    "임원 관리대장 저장 실패"

            },

            500

        )

# =========================================================

# 관리대장 전체 조회

#

# GET /officers

# =========================================================

def get_officers(request):

    try:

        docs = (

            firestore_db

            .collection(OFFICER_COLLECTION)

            .stream()

        )

        items = []

        for doc in docs:

            data = doc.to_dict() or {}

            created_at = data.get("createdAt")
            if created_at:
                try:
                    created_at = created_at.isoformat()
                except Exception:
                    created_at = str(created_at)
            else:
                created_at = ""

            items.append({

                "id":

                    doc.id,

                "company":

                    data.get(

                        "company",

                        ""

                    ),

                "registrationNumber":

                    data.get(

                        "registrationNumber",

                        ""

                    ),

                "officer":

                    data.get(

                        "officer",

                        ""

                    ),

                "position":

                    data.get(

                        "position",

                        ""

                    ),

                "termStart":

                    data.get(

                        "termStart",

                        ""

                    ),

                "expiry":

                    data.get(

                        "expiry",

                        ""

                    ),

                "phone":

                    data.get(

                        "phone",

                        ""

                    ),

                "email":

                    data.get(

                        "email",

                        ""

                    ),

                "source":

                    data.get(

                        "source",

                        "기존고객"

                    ),

                "createdAt":

                    created_at

            })

        # 예상 만료일 빠른 순

        items.sort(

            key=lambda x: (

                x.get("expiry")

                or "9999-99-99",

                x.get("company")

                or "",

                x.get("officer")

                or ""

            )

        )

        return response_json(

            request,

            {

                "ok": True,

                "count":

                    len(items),

                "items":

                    items

            },

            200

        )

    except Exception as e:

        print(

            "Firestore officer read error:",

            repr(e)

        )

        return response_json(

            request,

            {

                "ok": False,

                "error":

                    "임원 관리대장 조회 실패"

            },

            500

        )

# =========================================================

# 관리대장 개별 수정

#

# PATCH /officers/{document_id}

# =========================================================

def update_officer(request, document_id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):

        return response_json(

            request,

            {

                "ok": False,

                "error": "JSON 요청이 필요합니다."

            },

            400

        )

    try:

        doc_ref = (

            firestore_db

            .collection(OFFICER_COLLECTION)

            .document(document_id)

        )

        snapshot = doc_ref.get()

        if not snapshot.exists:

            return response_json(

                request,

                {

                    "ok": False,

                    "error":

                        "수정할 임원 정보를 찾을 수 없습니다."

                },

                404

            )

        allowed_fields = {

            "company",

            "registrationNumber",

            "officer",

            "position",

            "termStart",

            "expiry",

            "phone",

            "email",

            "source"

        }

        update_data = {}

        for key in allowed_fields:

            if key in data:

                update_data[key] = str(

                    data.get(key) or ""

                ).strip()

        if not update_data:

            return response_json(

                request,

                {

                    "ok": False,

                    "error": "수정할 내용이 없습니다."

                },

                400

            )

        update_data["updatedAt"] = (

            firestore.SERVER_TIMESTAMP

        )

        doc_ref.update(

            update_data

        )

        return response_json(

            request,

            {

                "ok": True,

                "id": document_id

            },

            200

        )

    except Exception as e:

        print(

            "Firestore officer update error:",

            repr(e)

        )

        return response_json(

            request,

            {

                "ok": False,

                "error": "임원 정보 수정 실패"

            },

            500

        )

# =========================================================

# 관리대장 개별 삭제

#

# DELETE /officers/{document_id}

# =========================================================

def delete_officer(request, document_id):

    try:

        doc_ref = (

            firestore_db

            .collection(OFFICER_COLLECTION)

            .document(document_id)

        )
