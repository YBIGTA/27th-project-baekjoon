from database.mysql_connection import engine, Base
from app.models.user_model import UserModel


def init_database():
    """
    애플리케이션 시작 시 데이터베이스 테이블을 생성합니다.
    """
    try:
        # 모든 모델의 테이블을 생성
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise e


if __name__ == "__main__":
    init_database()
