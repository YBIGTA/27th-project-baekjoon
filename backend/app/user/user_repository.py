from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.user.user_schema import User


class UserRepository:
    """
    사용자 관련 MySQL 쿼리를 수행하는 저장소 클래스.
    SQLAlchemy 세션을 이용하여 사용자 생성, 조회, 삭제 등의 기능을 수행한다.
    """

    def __init__(self, db: Session):
        """
        :param db: SQLAlchemy 세션 객체
        """
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        이메일 주소를 기준으로 사용자를 조회한다.

        :param email: 조회할 사용자의 이메일 주소
        :return: User 객체 또는 None
        """
        sql = text("SELECT email, password, username FROM users WHERE email = :email")
        result = self.db.execute(sql, {"email": email}).fetchone()

        if result:
            return User(
                email=result.email,
                password=result.password,
                username=result.username
            )
        return None

    def save_user(self, user: User) -> User:
        """
        사용자 정보를 저장한다. 기존 사용자가 있으면 업데이트, 없으면 삽입한다.

        :param user: 저장할 사용자 (Pydantic User 객체)
        :return: 저장된 사용자 (User 객체)
        """
        existing_user = self.get_user_by_email(user.email)

        if existing_user:
            sql = text("""
                UPDATE users 
                SET password = :password, username = :username 
                WHERE email = :email
            """)
        else:
            sql = text("""
                INSERT INTO users (email, password, username) 
                VALUES (:email, :password, :username)
            """)

        self.db.execute(sql, {
            "email": user.email,
            "password": user.password,
            "username": user.username
        })
        self.db.commit()

        return user

    def delete_user(self, user: User) -> User:
        """
        이메일 주소를 기준으로 사용자를 삭제한다.

        :param user: 삭제할 사용자 (User 객체)
        :return: 삭제된 사용자 (User 객체)
        """
        sql = text("DELETE FROM users WHERE email = :email")
        self.db.execute(sql, {"email": user.email})
        self.db.commit()

        return user
