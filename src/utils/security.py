"""보안 관련 유틸리티 함수들을 정의합니다."""

import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.context import CryptContext


def generate_salt(length: int = 32) -> str:
    """암호화에 사용할 솔트를 생성합니다.

    Args:
        length: 솔트 길이

    Returns:
        생성된 솔트
    """
    return secrets.token_hex(length)


def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """비밀번호를 해시화합니다.

    Args:
        password: 해시화할 비밀번호
        salt: 사용할 솔트 (없으면 자동 생성)

    Returns:
        (해시화된 비밀번호, 사용된 솔트)
    """
    if salt is None:
        salt = generate_salt()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_context.hash(password + salt)
    return hashed, salt


def verify_password(password: str, hashed: str, salt: str) -> bool:
    """비밀번호를 검증합니다.

    Args:
        password: 검증할 비밀번호
        hashed: 해시화된 비밀번호
        salt: 사용된 솔트

    Returns:
        검증 성공 여부
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(password + salt, hashed)


def generate_token(
    payload: dict,
    secret_key: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """JWT 토큰을 생성합니다.

    Args:
        payload: 토큰에 포함할 데이터
        secret_key: 토큰 서명에 사용할 비밀키
        expires_delta: 만료 시간

    Returns:
        생성된 JWT 토큰
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode = payload.copy()
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, secret_key, algorithm="HS256")


def verify_token(token: str, secret_key: str) -> Optional[dict]:
    """JWT 토큰을 검증합니다.

    Args:
        token: 검증할 JWT 토큰
        secret_key: 토큰 서명에 사용된 비밀키

    Returns:
        토큰 페이로드, 검증 실패시 None
    """
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


def generate_hmac_signature(message: str, secret_key: str) -> str:
    """HMAC 서명을 생성합니다.

    Args:
        message: 서명할 메시지
        secret_key: 서명에 사용할 비밀키

    Returns:
        생성된 HMAC 서명
    """
    return hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256,
    ).hexdigest()


def verify_hmac_signature(
    message: str,
    signature: str,
    secret_key: str,
) -> bool:
    """HMAC 서명을 검증합니다.

    Args:
        message: 검증할 메시지
        signature: 검증할 서명
        secret_key: 서명에 사용된 비밀키

    Returns:
        검증 성공 여부
    """
    expected_signature = generate_hmac_signature(message, secret_key)
    return hmac.compare_digest(signature, expected_signature)


def generate_csrf_token() -> str:
    """CSRF 토큰을 생성합니다.

    Returns:
        생성된 CSRF 토큰
    """
    return secrets.token_urlsafe(32)


def sanitize_input(input_str: str) -> str:
    """입력 문자열을 정제합니다.

    Args:
        input_str: 정제할 입력 문자열

    Returns:
        정제된 문자열
    """
    # HTML 이스케이프
    input_str = input_str.replace("&", "&amp;")
    input_str = input_str.replace("<", "&lt;")
    input_str = input_str.replace(">", "&gt;")
    input_str = input_str.replace('"', "&quot;")
    input_str = input_str.replace("'", "&#x27;")

    # SQL 인젝션 방지
    input_str = input_str.replace("'", "''")
    input_str = input_str.replace(";", "")

    return input_str
