import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi.encoders import jsonable_encoder
from fastapi_app.app.schemas.admin_user_schema import UserRegisterSchema, UserLoginSchema, PasswordResetSchema
from fastapi_app.app.database import Session, ENGINE
from fastapi_app.app.models import UserAdmin, Client
from fastapi_jwt_auth.auth_jwt import AuthJWT
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_

session = Session(bind=ENGINE)

admin_user_router = APIRouter(prefix="/admin", tags=["Admin_Users"])


@admin_user_router.get('/search/{query}')
async def get_users(query: Optional[str] = Path(..., min_length=1), authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        check_user = session.query(UserAdmin).filter(UserAdmin.username == authorization.get_jwt_subject()).first()
        if not check_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
        if query:
            users = session.query(UserAdmin).filter(
                (UserAdmin.username.ilike(f"%{query}%")) | (UserAdmin.email.ilike(f"%{query}%"))
            ).all()
        else:
            users = session.query(UserAdmin).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return jsonable_encoder(users)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@admin_user_router.get('/get')
async def get_user(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(UserAdmin).filter(UserAdmin.username == Authorization.get_jwt_subject()).first()
        if check_user:
            user = session.query(Client).all()
            return jsonable_encoder(user)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Users not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@admin_user_router.post('/login')
async def login_user_admin(request: UserLoginSchema, authorization: AuthJWT = Depends()):
    check_user = session.query(UserAdmin).filter(UserAdmin.username == request.username).first()
    if check_user and check_password_hash(check_user.password, request.password):
        access_token = authorization.create_access_token(subject=request.username,
                                                         expires_time=datetime.timedelta(minutes=50))
        refresh_token = authorization.create_refresh_token(subject=request.username,
                                                           expires_time=datetime.timedelta(days=1))
        response = {
            "status_code": 200,
            "detail": "Login successful",
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonable_encoder(response)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password or username")


@admin_user_router.post("/register")
async def user_register(request: UserRegisterSchema):
    check_user = session.query(UserAdmin).filter(
        or_(
            UserAdmin.username == request.username,
            UserAdmin.email == request.email,
            UserAdmin.phone == request.phone
        )).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = UserAdmin(
        first_name=request.first_name,
        last_name=request.last_name,
        username=request.username,
        email=request.email,
        phone=request.phone,
        password=generate_password_hash(request.password),
        is_admin=True
    )
    try:
        session.add(new_user)
        session.commit()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="shunga oxshash malumotlar oldin saqlangan")
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="User registered")


@admin_user_router.get("/token/verify")
async def token_verify(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        return {"status_code": 200, "detail": "Token verified"}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@admin_user_router.put("/reset/{username}")
async def change_password(username: str, user: PasswordResetSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(UserAdmin).filter(UserAdmin.username == username).first()
        if not check_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foydalanuvchi topilmadi")

        if user.password != user.password_2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parollar bir-biriga mos kelmaydi")

        check_user.password = generate_password_hash(user.password)
        session.add(check_user)
        session.commit()

        data = {
            "message": "Parol muvaffaqiyatli o'zgartirildi"
        }
        return jsonable_encoder(data)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Noto'g'ri token")
