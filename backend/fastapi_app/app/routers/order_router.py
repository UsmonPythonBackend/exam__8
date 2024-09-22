import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_app.app.schemas.order_schema import OrderCreateSchema, OrderUpdateSchema
from fastapi_app.app.database import Session, ENGINE
from fastapi_app.app.models import UserAdmin, Order, Client
from fastapi_jwt_auth.auth_jwt import AuthJWT
from werkzeug.security import check_password_hash, generate_password_hash

session = Session(bind=ENGINE)
order_router = APIRouter(prefix="/order", tags=["Order"])


@order_router.get('/')
async def get_order(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    check_user = session.query(UserAdmin).filter(UserAdmin.username == Authorization.get_jwt_subject()).first()
    if check_user:
        user = session.query(Order).all()
        return jsonable_encoder(user)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Users not found')


@order_router.post("/create-order")
async def create_order(request: OrderCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    if check_user is not None:
        new_order = Order(
            order_status=request.order_status,
            client_id=check_user.id,
            furniture_id=request.furniture_id,
            quantity=request.quantity,
            total_price=request.total_price
        )
        session.add(new_order)
        session.commit()

        data = {
            "code": 200,
            "success": True,
            "message": f"Successfully created {Authorization.get_jwt_subject()}",
            "order_id": new_order.id
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@order_router.put("/update/{id}")
async def update_order(id: str, order: OrderUpdateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    if check_user:
        order_id = UUID(id)
        check_order = session.query(Order).filter(Order.id == order_id).first()
        if check_order:
            for key, value in order.dict().items():
                setattr(check_order, key, value)

                data = {
                    "code": 200,
                    "success": True,
                    "message": "Successfully updated order",
                    "object": {
                        "order_status": check_order.order_status,
                        "furniture_id": order.furniture_id,
                        "quantity": order.quantity,
                        "total_price": check_order.total_price
                    }
                }
                session.add(check_order)
                session.commit()
                return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='client not found')


@order_router.delete("/delete/{id}")
async def delete_order(id: str, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    if check_user:
        order_id = UUID(id)
        check_order = session.query(Order).filter(Order.id == order_id).first()
        if check_order:
            session.delete(check_order)
            session.commit()
            return jsonable_encoder({"code": 200, "message": "Successfully deleted order"})

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
