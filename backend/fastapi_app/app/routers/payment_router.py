import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_app.app.schemas.payment_schema import PaymentCreateSchema
from fastapi_app.app.database import Session, ENGINE
from fastapi_app.app.models import Payment, Client, Order
from fastapi_jwt_auth.auth_jwt import AuthJWT

session = Session(bind=ENGINE)
payments_router = APIRouter(prefix="/payment", tags=["Payment"])


@payments_router.get('/')
async def get_order(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    if check_user:
        user = session.query(Payment).filter(Payment.client_id == check_user.id).all()
        return jsonable_encoder(user)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Client not found')


@payments_router.post("/create-pay")
async def create_payment(request: PaymentCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    order = session.query(Order).filter(Order.client_id == check_user.id).all()
    if check_user is not None:
        new_payment = Payment(
            order_id=order.order_id,
            amount=request.amount,
            payment_type=request.payment_type
        )
        session.add(new_payment)
        session.commit()

        data = {
            "code": 200,
            "success": True,
            "message": f"Successfully created {Authorization.get_jwt_subject()}",
            "order_id": new_payment.id
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paymenty not found")


