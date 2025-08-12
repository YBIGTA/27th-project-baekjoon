from pymongo import MongoClient
from dotenv import load_dotenv
import os
from typing import List, Dict

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# 환경변수에서 MongoDB 접속 정보 가져오기
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB")

# MongoDB 클라이언트 및 DB 객체 생성
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DB_NAME]


def get_collection(site_name: str):
    """site_name을 컬렉션 이름으로 간주하여 해당 컬렉션 객체 반환"""
    return mongo_db[site_name]


def get_reviews(site_name: str) -> List[Dict]:
    """site_name 컬렉션에서 모든 리뷰를 가져옴 (_id 제외)"""
    collection = get_collection(site_name)
    return list(collection.find({}, {"_id": 0}))


def replace_reviews(site_name: str, reviews: List[Dict]):
    """site_name 컬렉션을 비우고 새 리뷰들을 저장"""
    collection = get_collection(site_name)
    collection.delete_many({})
    collection.insert_many(reviews)


def save_preprocessed_reviews(site_name: str, reviews: List[Dict]):
    """전처리된 리뷰들을 별도 컬렉션에 저장 (원본 덮어쓰지 않음)"""
    preprocessed_collection_name = f"{site_name}_preprocessed"
    collection = mongo_db[preprocessed_collection_name]
    collection.delete_many({})  # 기존 전처리 데이터 삭제
    collection.insert_many(reviews)
    return preprocessed_collection_name


def get_preprocessed_reviews(site_name: str) -> List[Dict]:
    """전처리된 리뷰들을 가져옴"""
    preprocessed_collection_name = f"{site_name}_preprocessed"
    collection = mongo_db[preprocessed_collection_name]
    return list(collection.find({}, {"_id": 0}))
