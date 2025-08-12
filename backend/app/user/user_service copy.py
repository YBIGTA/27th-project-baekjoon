from fastapi import HTTPException
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
    def __init__(self, userRepository: UserRepository) -> None:
        self.repo = userRepository

    def login(self, user_login: UserLogin) -> User:
        """
        사용자 로그인을 처리합니다.

        사용자의 이메일로 정보를 조회한 뒤, 입력한 비밀번호와 비교합니다.
        일치하지 않으면 HTTP 400 예외를 발생시킵니다.

        Args:
            user_login (UserLogin): 로그인 시 필요한 사용자 이메일과 비밀번호

        Returns:
            User: 로그인에 성공한 사용자 객체

        Raises:
            HTTPException: 이메일이 존재하지 않거나 비밀번호가 틀린 경우
        """
        # 1️⃣ 이메일로 해당 유저 정보를 Repository에서 가져옴
        user = self.repo.get_user_by_email(user_login.email)

        # 2️⃣ 만약 해당 이메일이 없다면, 로그인 실패로 처리 (HTTP 400 에러 발생)
        if user is None:
            raise HTTPException(
                status_code=400,
                detail="User not Found."  # 에러 메시지: 사용자를 찾을 수 없음
            )

        # 3️⃣ 이메일은 있지만, 비밀번호가 일치하지 않으면 로그인 실패 처리
        if user.password != user_login.password:
            raise HTTPException(
                status_code=400,
                detail="Invalid PW"  # 에러 메시지: 비밀번호가 틀렸음
            )

        # 4️⃣ 모든 조건 통과 시 로그인 성공 → 해당 유저 정보 반환
        return user

    def register_user(self, new_user: User) -> User:
        """
        새로운 사용자를 등록합니다.

        중복된 이메일이 존재할 경우 HTTP 400 예외를 발생시키며,
        성공적으로 등록되면 사용자 정보를 반환합니다.

        Args:
            new_user (User): 등록할 사용자 정보

        Returns:
            User: 등록된 사용자 객체

        Raises:
            HTTPException: 이미 존재하는 이메일일 경우
        """
        # 1️⃣ 이메일 중복 확인
        existing_user = self.repo.get_user_by_email(new_user.email)
        if existing_user:
            # 이미 존재한다면 400 에러 발생
            raise HTTPException(
                status_code=400,
                detail="User already Exists."
            )

        # 2️⃣ Repository를 통해 유저 추가 (DB 또는 JSON에 저장됨)
        self.repo.save_user(new_user)

        # 3️⃣ 성공적으로 등록된 사용자 정보 반환
        return new_user

    def delete_user(self, email: str) -> User:
        """
        이메일을 기반으로 사용자를 삭제합니다.

        존재하지 않는 이메일일 경우 HTTP 404 예외를 발생시키며,
        삭제된 사용자 정보를 반환합니다.

        Args:
            email (str): 삭제할 사용자의 이메일

        Returns:
            User: 삭제된 사용자 정보

        Raises:
            HTTPException: 사용자가 존재하지 않을 경우
        """
        # 1️⃣ 이메일로 해당 유저를 조회
        user = self.repo.get_user_by_email(email)

        # 2️⃣ 사용자가 존재하지 않으면 에러 반환
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not Found."
            )

        # 3️⃣ 존재하면 해당 유저를 삭제
        self.repo.delete_user(user)

        # 4️⃣ 삭제된 유저 정보를 반환 (삭제되기 전 정보)
        return user

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        """
        사용자의 비밀번호를 업데이트합니다.

        이메일로 사용자를 조회한 뒤, 존재할 경우 비밀번호를 새 값으로 갱신합니다.

        Args:
            user_update (UserUpdate): 이메일과 새로운 비밀번호 정보

        Returns:
            User: 비밀번호가 업데이트된 사용자 정보

        Raises:
            HTTPException: 사용자가 존재하지 않을 경우
        """
        # 1️⃣ 이메일로 유저 찾기
        user = self.repo.get_user_by_email(user_update.email)

        # 2️⃣ 없으면 404 에러 발생
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not Found"
            )

        # 3️⃣ 기존 유저 정보를 바탕으로 비밀번호만 바꿔서 새 User 객체 생성
        updated_user = User(
            email=user.email,
            password=user_update.new_password,
            username=user.username
        )

        # 4️⃣ Repository에 업데이트 요청 (데이터 저장)
        self.repo.save_user(updated_user)

        # 5️⃣ 바뀐 유저 정보 반환
        return updated_user
