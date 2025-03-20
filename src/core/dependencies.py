"""의존성 주입을 관리하는 모듈입니다."""

from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .errors import AuthenticationError
from .settings import get_settings
from .types import TokenData

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenData:
    """현재 인증된 사용자를 가져옵니다.

    Args:
        token: JWT 토큰
        db: 데이터베이스 세션

    Returns:
        TokenData: 토큰 데이터

    Raises:
        AuthenticationError: 인증 실패 시
    """
    credentials_exception = AuthenticationError(
        "인증에 실패했습니다.",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_active_user(
    current_user: Annotated[TokenData, Depends(get_current_user)],
) -> TokenData:
    """현재 활성화된 사용자를 가져옵니다.

    Args:
        current_user: 현재 사용자

    Returns:
        TokenData: 토큰 데이터
    """
    if not current_user.username:
        raise AuthenticationError("비활성화된 사용자입니다.")
    return current_user


def get_settings_dependency() -> Generator:
    """설정 객체를 가져옵니다.

    Yields:
        Settings: 설정 객체
    """
    try:
        settings = get_settings()
        yield settings
    finally:
        pass
