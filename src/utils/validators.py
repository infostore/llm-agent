"""유효성 검사 유틸리티 함수들을 정의합니다."""

import re
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ValidationError


def validate_email(email: str) -> bool:
    """이메일 주소의 유효성을 검사합니다.

    Args:
        email: 검사할 이메일 주소

    Returns:
        유효성 여부
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """비밀번호의 유효성을 검사합니다.

    Args:
        password: 검사할 비밀번호

    Returns:
        유효성 여부
    """
    # 최소 8자, 최소 1개의 대문자, 소문자, 숫자, 특수문자
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))


def validate_phone_number(phone: str) -> bool:
    """전화번호의 유효성을 검사합니다.

    Args:
        phone: 검사할 전화번호

    Returns:
        유효성 여부
    """
    # 한국 전화번호 형식 (010-1234-5678)
    pattern = r"^010-\d{4}-\d{4}$"
    return bool(re.match(pattern, phone))


def validate_url(url: str) -> bool:
    """URL의 유효성을 검사합니다.

    Args:
        url: 검사할 URL

    Returns:
        유효성 여부
    """
    pattern = r"^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
    return bool(re.match(pattern, url))


def validate_dict(data: Dict[str, Any], model: BaseModel) -> Optional[Dict[str, Any]]:
    """딕셔너리 데이터의 유효성을 검사합니다.

    Args:
        data: 검사할 딕셔너리 데이터
        model: 검증에 사용할 Pydantic 모델

    Returns:
        검증된 데이터, 실패시 None
    """
    try:
        return model(**data).model_dump()
    except ValidationError:
        return None


def validate_list(data: List[Dict[str, Any]], model: BaseModel) -> List[Dict[str, Any]]:
    """딕셔너리 리스트의 유효성을 검사합니다.

    Args:
        data: 검사할 딕셔너리 리스트
        model: 검증에 사용할 Pydantic 모델

    Returns:
        검증된 데이터 리스트
    """
    validated_data = []
    for item in data:
        if validated := validate_dict(item, model):
            validated_data.append(validated)
    return validated_data


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """필수 필드의 존재 여부를 검사합니다.

    Args:
        data: 검사할 딕셔너리 데이터
        required_fields: 필수 필드 목록

    Returns:
        유효성 여부
    """
    return all(field in data for field in required_fields)


def validate_field_types(data: Dict[str, Any], field_types: Dict[str, type]) -> bool:
    """필드의 타입을 검사합니다.

    Args:
        data: 검사할 딕셔너리 데이터
        field_types: 필드별 타입 정의

    Returns:
        유효성 여부
    """
    return all(
        isinstance(data.get(field), field_type)
        for field, field_type in field_types.items()
        if field in data
    )
