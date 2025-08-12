from app.user.user_repository import UserRepository
from app.user.user_schema import User, UserLogin, UserUpdate, UserDB
import os
import hashlib
import hmac
from typing import Tuple

"""
description:
- UserService: 사용자 관련 비즈니스 로직을 처리하는 서비스 클래스
- login: 사용자 로그인 처리
- register_user: 사용자 등록 처리
- delete_user: 사용자 삭제 처리
- update_user_pwd: 사용자 비밀번호 업데이트 처리
"""

class UserService:
    def __init__(self, userRepoitory: UserRepository) -> None:
        self.repo = userRepoitory

    def login(self, user_login: UserLogin) -> User:
        """
        사용자 로그인을 처리합니다.
        """
        user_db = self.repo.get_user_by_email(user_login.email)

        if user_db is None:
            raise ValueError("Invalid Email/PW")
        
        if not self._verify_password(user_login.password, user_db.salt, user_db.password):
            raise ValueError("Invalid Email/PW")

        # 외부로는 해시된 패스워드와 솔트를 숨긴 모델 반환
        return User(email=user_db.email, password="", username=user_db.username)
        
    def register_user(self, new_user: User) -> User:
        """
        새로운 사용자를 등록합니다.
        """
        existing_user = self.repo.get_user_by_email(new_user.email)
        if existing_user:
            raise ValueError("User already Exists.")

        salt = self._gen_salt()
        hashed = self._hash_password(new_user.password, salt)
        user_db = UserDB(
            email=new_user.email,
            password=hashed,
            salt=salt.hex(),
            username=new_user.username,
        )
        self.repo.save_user(user_db)
        return User(email=user_db.email, password="", username=user_db.username)

    def delete_user(self, email: str, current_password: str) -> User:
        """
        이메일을 기반으로 사용자를 삭제합니다.
        """
        user_db = self.repo.get_user_by_email(email)

        if user_db is None:
            raise ValueError("Invalid Email/PW")

        if not self._verify_password(current_password, user_db.salt, user_db.password):
            raise ValueError("Invalid Email/PW")

        self.repo.delete_user(User(email=user_db.email, password="", username=user_db.username))
        return User(email=user_db.email, password="", username=user_db.username)

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        """
        사용자 비밀번호를 업데이트합니다.
        """
        user_db = self.repo.get_user_by_email(user_update.email)

        if user_db is None:
            raise ValueError("User not Found.")
        if not self._verify_password(user_update.current_password, user_db.salt, user_db.password):
            raise ValueError("Invalid Email/PW")
        
        # 새 salt 발급 및 해시 저장
        new_salt = self._gen_salt()
        new_hash = self._hash_password(user_update.new_password, new_salt)
        updated_user_db = UserDB(
            email=user_db.email,
            password=new_hash,
            salt=new_salt.hex(),
            username=user_db.username,
        )

        self.repo.save_user(updated_user_db)
        return User(email=updated_user_db.email, password="", username=updated_user_db.username)

    # 보안 설정
    _PBKDF2_ITERATIONS = 200_000
    _HASH_NAME = "sha256"
    _SALT_BYTES = 16

    @staticmethod
    def _hash_password(password: str, salt: bytes) -> str:
        """PBKDF2-HMAC 으로 비밀번호 해시를 생성 (hex 문자열 반환)."""
        dk = hashlib.pbkdf2_hmac(
            UserService._HASH_NAME,
            password.encode("utf-8"),
            salt,
            UserService._PBKDF2_ITERATIONS,
            dklen=32,
        )
        return dk.hex()

    @staticmethod
    def _gen_salt() -> bytes:
        return os.urandom(UserService._SALT_BYTES)

    @staticmethod
    def _verify_password(password: str, salt_hex: str, expected_hash_hex: str) -> bool:
        salt = bytes.fromhex(salt_hex)
        computed = UserService._hash_password(password, salt)
        return hmac.compare_digest(computed, expected_hash_hex)