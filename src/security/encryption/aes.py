"""AES 암호화 구현을 구현합니다."""

import base64
import json
from typing import Any, Dict

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .base import Encryptor

from core.settings import get_settings

settings = get_settings()


class AESEncryptor(Encryptor):
    """AES 암호화 구현입니다."""

    def __init__(self, key: str = None):
        """AES 암호화를 초기화합니다.

        Args:
            key: 암호화 키
        """
        self.key = key or settings.SECRET_KEY
        self._init_fernet()

    def _init_fernet(self) -> None:
        """Fernet 인스턴스를 초기화합니다."""
        # 키 생성
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"llm-agent",
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.key.encode()))
        self.fernet = Fernet(key)

    async def encrypt(self, data: Any) -> str:
        """데이터를 암호화합니다.

        Args:
            data: 암호화할 데이터

        Returns:
            암호화된 데이터
        """
        # 데이터를 JSON 문자열로 변환
        json_data = json.dumps(data)
        # 암호화
        encrypted_data = self.fernet.encrypt(json_data.encode())
        return encrypted_data.decode()

    async def decrypt(self, encrypted_data: str) -> Any:
        """암호화된 데이터를 복호화합니다.

        Args:
            encrypted_data: 암호화된 데이터

        Returns:
            복호화된 데이터
        """
        # 복호화
        decrypted_data = self.fernet.decrypt(encrypted_data.encode())
        # JSON 문자열을 파이썬 객체로 변환
        return json.loads(decrypted_data.decode())

    async def encrypt_dict(self, data: Dict[str, Any]) -> Dict[str, str]:
        """딕셔너리를 암호화합니다.

        Args:
            data: 암호화할 딕셔너리

        Returns:
            암호화된 딕셔너리
        """
        return {key: await self.encrypt(value) for key, value in data.items()}

    async def decrypt_dict(self, encrypted_data: Dict[str, str]) -> Dict[str, Any]:
        """암호화된 딕셔너리를 복호화합니다.

        Args:
            encrypted_data: 암호화된 딕셔너리

        Returns:
            복호화된 딕셔너리
        """
        return {key: await self.decrypt(value) for key, value in encrypted_data.items()}
