from typing import Optional
from sqlalchemy.orm import Session
from app.user.user_schema import User, UserDB
from app.models.user_model import UserModel


class UserRepository:
    """
    사용자 관련 MySQL 쿼리를 수행하는 저장소 클래스.
    SQLAlchemy ORM을 이용하여 사용자 생성, 조회, 삭제 등의 기능을 수행한다.
    """

    def __init__(self, db: Session):
        """
        :param db: SQLAlchemy 세션 객체
        """
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[UserDB]:
        """
        이메일 주소를 기준으로 사용자를 조회한다.

        :param email: 조회할 사용자의 이메일 주소
        :return: UserDB 객체 또는 None
        """
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        
        if user_model:
            return UserDB(
                email=user_model.email,
                password=user_model.password,
                salt=user_model.salt,
                username=user_model.username
            )
        return None

    def save_user(self, user: UserDB) -> UserDB:
        """
        사용자 정보를 저장한다. 기존 사용자가 있으면 업데이트, 없으면 삽입한다.

        :param user: 저장할 사용자 (UserDB 객체)
        :return: 저장된 사용자 (UserDB 객체)
        """
        existing_user = self.db.query(UserModel).filter(UserModel.email == user.email).first()

        if existing_user:
            # 기존 사용자 업데이트
            existing_user.password = user.password
            existing_user.salt = user.salt
            existing_user.username = user.username
        else:
            # 새 사용자 생성
            new_user = UserModel(
                email=user.email,
                password=user.password,
                salt=user.salt,
                username=user.username
            )
            self.db.add(new_user)

        self.db.commit()
        return user

    def delete_user(self, user: User) -> User:
        """
        이메일 주소를 기준으로 사용자를 삭제한다.

        :param user: 삭제할 사용자 (User 객체)
        :return: 삭제된 사용자 (User 객체)
        """
        user_model = self.db.query(UserModel).filter(UserModel.email == user.email).first()
        if user_model:
            self.db.delete(user_model)
            self.db.commit()
        
        return user
