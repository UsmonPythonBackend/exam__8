import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_app.app.schemas.client_schema import ClientRegisterSchema, ClientLoginSchema, PasswordResetSchema
from fastapi_app.app.database import Session, ENGINE
from fastapi_app.app.models import Client, UserAdmin
from fastapi_jwt_auth.auth_jwt import AuthJWT
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_

session = Session(bind=ENGINE)

client_router = APIRouter(prefix="/client", tags=["Clients"])


@client_router.get('/')
async def get_client(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_admin = session.query(UserAdmin).filter(UserAdmin.username == Authorization.get_jwt_subject()).first()
        if check_admin:
            clients = session.query(Client).all()
            data = [{
                "id": client.id,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "name": client.username,
                "email": client.email,
                "password": generate_password_hash(client.password)[-8]
            } for client in clients
            ]
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Clients not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@client_router.post('/login')
async def login_client(request: ClientLoginSchema, Authorizotion: AuthJWT = Depends()):
    check_client = session.query(Client).filter(Client.username == request.username).first()
    if check_client and check_password_hash(check_client.password, request.password):
        access_token = Authorizotion.create_access_token(subject=request.username,
                                                         expires_time=datetime.timedelta(minutes=50))
        refresh_token = Authorizotion.create_refresh_token(subject=request.username,
                                                           expires_time=datetime.timedelta(days=1))
        response = {
            "status_code": 200,
            "detail": "Login successful",
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonable_encoder(response)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password or username")


@client_router.post("/register")
async def client_register(request: ClientRegisterSchema):
    check_username = session.query(Client).filter(Client.username == request.username).first()
    if check_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username")
    check_email = session.query(Client).filter(Client.email == request.email).first()
    if check_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email")

    new_client = Client(
        first_name=request.first_name,
        last_name=request.last_name,
        username=request.username,
        email=request.email,
        password=generate_password_hash(request.password)
    )
    try:
        session.add(new_client)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bunday emaildan foydalanuvchi royxatdan otgan")
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Client registered")


@client_router.get("/token/verify")
async def token_verify(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        return {"status_code": 200, "detail": "Token verified"}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@client_router.put("/reset/{username}")
async def change_password(username: str, user: PasswordResetSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_client = session.query(Client).filter(Client.username == username).first()
        if check_client:
            if user.password == user.password_2:
                check_client.password = generate_password_hash(user.password)
                session.add(check_client)
                session.commit()
                data = {
                    "message": "Password changed successfully"
                }
                return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
