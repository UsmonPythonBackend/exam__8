import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_app.app.schemas.comments_schema import CommentCreateSchema, CommentUpdateSchema
from fastapi_app.app.database import Session, ENGINE
from fastapi_app.app.models import UserAdmin, Client, Comments
from fastapi_jwt_auth.auth_jwt import AuthJWT
from werkzeug.security import check_password_hash, generate_password_hash

session = Session(bind=ENGINE)
comment_router = APIRouter(prefix="/comment", tags=["Comment"])


@comment_router.get('/')
async def get_order(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    check_user = session.query(UserAdmin).filter(UserAdmin.username == Authorization.get_jwt_subject()).first()
    if check_user:
        user = session.query(Comments).all()
        return jsonable_encoder(user)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Users not found')


@comment_router.post("/create")
async def create_comment(request: CommentCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    if check_user is not None:
        new_comment = Comments(
            client_id=check_user.id,
            furniture_id=request.furniture_id,
            content=request.content
        )
        session.add(new_comment)
        session.commit()

        data = {
            "code": 200,
            "success": True,
            "message": f"Successfully created {Authorization.get_jwt_subject()} by comment",
            "id": str(new_comment.id),
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="siz comment yozish uchun royxatdan organ bolishiz kerak")


@comment_router.put("/update/{id}")
async def update_comment(id: str, comment: CommentUpdateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    if check_user:
        check_comment = session.query(Comments).filter(Comments.id == id).first()
        if check_comment:
            for key, value in comment.dict().items():
                setattr(check_comment, key, value)
                if check_comment.client_id == check_user.id:
                    data = {
                        "code": 200,
                        "success": True,
                        "message": "Successfully updated comment",
                        "object": {
                            "client_id": check_user.id,
                            "furniture_id": check_comment.furniture_id,
                            "content": comment.content
                        }
                    }
                    session.add(check_comment)
                    session.commit()
                    return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='client not found')


@comment_router.delete("/delete/{id}")
async def delete_order(id: str, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    if check_user:
        comment_id = UUID(id)
        check_comment = session.query(Comments).filter(Comments.id == comment_id).first()
        if check_comment:
            session.delete(check_comment)
            session.commit()
            return jsonable_encoder({"code": 200, "message": "Successfully deleted comment"})

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
