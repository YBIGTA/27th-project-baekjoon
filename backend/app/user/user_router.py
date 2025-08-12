from fastapi import APIRouter, HTTPException, Depends, status
from app.user.user_schema import User, UserLogin, UserUpdate, UserDeleteRequest
from app.user.user_service import UserService
from app.dependencies import get_user_service
from app.responses.base_response import BaseResponse

user = APIRouter(prefix="/api/user")


@user.post("/login", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def login_user(user_login: UserLogin, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    :param user_login: the user object to be logged in.
    :param service: the service object in './user_service.py'
    :return: response object, if successful, otherwise raises an exception.
    An API endpoint handling user login requests.
    """
    try:
        user = service.login(user_login)
        return BaseResponse(status="success", data=user, message="Login Success.") 
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
def delete_user(user_delete_request: UserDeleteRequest, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    :param user: the user object to be deleted.
    :param service: the service object in './user_service.py'
    :return: response object, if successful, otherwise raises an exception.
    An API endpoint handling user deletion requests.
    """
    try:
        deleted = service.delete_user(user_delete_request.email)
        return BaseResponse(status="success", data=deleted, message="User Deletion Success.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail="User not Found.")


@user.put("/update-password", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def update_user_password(user_update: UserUpdate, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    :param user: the user object whose password is to be updated.
    :param service: the service object in './user_service.py'
    :return: response object, if successful, otherwise raises an exception.
    An API endpoint handling user password update requests.
    """
    try:
        user = service.update_user_pwd(user_update)
        return BaseResponse(status="success", data=user, message="User Password Update Success.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail="User not Found.")
