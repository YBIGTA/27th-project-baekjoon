from app.user.user_repository import UserRepository
from app.user.user_schema import User, UserLogin, UserUpdate

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
        user = self.repo.get_user_by_email(user_login.email)

        if user is None:
            raise ValueError("User not Found.")

        if user.password != user_login.password:
            raise ValueError("Invalid ID/PW")

        return user
        
    def register_user(self, new_user: User) -> User:
        """
        새로운 사용자를 등록합니다.
        """
        existing_user = self.repo.get_user_by_email(new_user.email)
        if existing_user:
            raise ValueError("User already Exists.")

        self.repo.save_user(new_user)
        return new_user

    def delete_user(self, email: str) -> User:
        """
        이메일을 기반으로 사용자를 삭제합니다.
        """
        user = self.repo.get_user_by_email(email)

        if user is None:
            raise ValueError("User not Found.")

        self.repo.delete_user(user)
        return user

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        """
        사용자 비밀번호를 업데이트합니다.
        """
        user = self.repo.get_user_by_email(user_update.email)

        if user is None:
            raise ValueError("User not Found.")

        updated_user = User(
            email=user.email,
            password=user_update.new_password,
            username=user.username
        )

        self.repo.save_user(updated_user)
        return updated_user
