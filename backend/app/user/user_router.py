from fastapi import APIRouter, HTTPException, Depends, status
from app.user.user_schema import User, UserLogin, UserUpdate, UserDeleteRequest, LoginResponse, UserPublic
from app.user.user_service import UserService
from app.dependencies import get_user_service, get_current_user
from app.responses.base_response import BaseResponse
from app.auth import create_access_token, get_current_user_email

user = APIRouter(prefix="/api/user")


@user.post("/login", response_model=BaseResponse[LoginResponse], status_code=status.HTTP_200_OK)
def login_user(user_login: UserLogin, service: UserService = Depends(get_user_service)) -> BaseResponse[LoginResponse]:
    """
    :param user_login: the user object to be logged in.
    :param service: the service object in './user_service.py'
    :return: response object, if successful, otherwise raises an exception.
    An API endpoint handling user login requests.
    """
    try:
        user = service.login(user_login)
        access_token = create_access_token(subject=user.email)
        public = UserPublic(email=user.email, username=user.username)
        return BaseResponse(status="success", data=LoginResponse(user=public, access_token=access_token), message="Login Success.") 
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.post("/register", response_model=BaseResponse[User], status_code=status.HTTP_201_CREATED)
def register_user(user: User, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    :param user: the user object to be registered.
    :param service: the service object in './user_service.py'
    :return: response object, if successful, otherwise raises an exception.
    An API endpoint handling user registration requests.
    """
    try:
        user = service.register_user(user)
        return BaseResponse(status="success", data=user, message="User Registragion Success.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.delete("/delete", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def delete_user(
    user_delete_request: UserDeleteRequest,
    current_email: str = Depends(get_current_user_email),
    service: UserService = Depends(get_user_service),
) -> BaseResponse[User]:
    """
    :param user: the user object to be deleted.
    :param service: the service object in './user_service.py'
    :return: response object, if successful, otherwise raises an exception.
    An API endpoint handling user deletion requests.
    """
    try:
        if current_email != user_delete_request.email:
            raise HTTPException(status_code=403, detail="Cannot delete another user")
        deleted = service.delete_user(user_delete_request.email, user_delete_request.password)
        return BaseResponse(status="success", data=deleted, message="User Deletion Success.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.get("/me", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)) -> BaseResponse[User]:
    """토큰 기반으로 현재 사용자 조회"""
    return BaseResponse(status="success", data=current_user, message="Me")


@user.put("/update-password", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def update_user_password(
    user_update: UserUpdate,
    current_email: str = Depends(get_current_user_email),
    service: UserService = Depends(get_user_service),
) -> BaseResponse[User]:
    """
    :param user: the user object whose password is to be updated.
    :param service: the service object in './user_service.py'
    :return: response object, if successful, otherwise raises an exception.
    An API endpoint handling user password update requests.
    """
    try:
        if current_email != user_update.email:
            raise HTTPException(status_code=403, detail="Cannot update another user's password")
        user = service.update_user_pwd(user_update)
        return BaseResponse(status="success", data=user, message="User Password Update Success.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
