"""암호화의 기본 클래스를 정의합니다."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Encryptor(ABC):
    """암호화 기본 클래스입니다."""

    @abstractmethod
    async def encrypt(self, data: Any) -> str:
        """데이터를 암호화합니다.

        Args:
            data: 암호화할 데이터

        Returns:
            암호화된 데이터
        """
        pass

    @abstractmethod
    async def decrypt(self, encrypted_data: str) -> Any:
        """암호화된 데이터를 복호화합니다.

        Args:
            encrypted_data: 암호화된 데이터

        Returns:
            복호화된 데이터
        """
        pass

    @abstractmethod
    async def encrypt_dict(self, data: Dict[str, Any]) -> Dict[str, str]:
        """딕셔너리를 암호화합니다.

        Args:
            data: 암호화할 딕셔너리

        Returns:
            암호화된 딕셔너리
        """
        pass

    @abstractmethod
    async def decrypt_dict(self, encrypted_data: Dict[str, str]) -> Dict[str, Any]:
        """암호화된 딕셔너리를 복호화합니다.

        Args:
            encrypted_data: 암호화된 딕셔너리

        Returns:
            복호화된 딕셔너리
        """
        pass
