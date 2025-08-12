from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

# 환경변수(.env)를 불러오기 위한 설정
import os
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

# .env에서 MySQL 접속 정보 가져오기
user = os.getenv("MYSQL_USER")           
passwd = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")           
port = os.getenv("MYSQL_PORT")          
db = os.getenv("MYSQL_DB")              

# SQLAlchemy 연결 URL 구성
DB_URL = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8'

# SQLAlchemy 엔진 생성 (DB와 실제로 연결되는 객체)
engine = create_engine(DB_URL, echo=True)

# 세션 팩토리 생성 (DB 작업 시 사용할 세션 객체 만들기용)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델 정의 시 사용할 기본 Base 클래스
Base = declarative_base()
