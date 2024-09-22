import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_app.app.schemas.cargo_schema import CargoCreateSchema, CargoUpdateSchema
from fastapi_app.app.database import Session, ENGINE
from fastapi_app.app.models import Payment, Client, Order, Cargo
from fastapi_jwt_auth.auth_jwt import AuthJWT

session = Session(bind=ENGINE)
cargo_router = APIRouter(prefix="/cargo", tags=["Cargo"])


@cargo_router.post("/create-cargo")
async def create_payment(request: CargoCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    order = session.query(Order).all()
    if check_user is not None:
        if order:
            new_cargo = Cargo(
                order_id=order[0].id,
                delivery_address=request.delivery_address,
                delivery_status=request.delivery_status
            )
            session.add(new_cargo)
            session.commit()

            data = {
                "code": 200,
                "success": True,
                "message": f"Successfully created {Authorization.get_jwt_subject()}",
                "cargo_id": new_cargo.id
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo not found")

@cargo_router.delete("/delete/{id}")
async def delete_order(id: str, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()
    if check_user:
        check_order = session.query(Cargo).filter(Cargo.id == id).first()
        if check_order:
            session.delete(check_order)
            session.commit()
            return jsonable_encoder({"code": 200, "message": "Successfully deleted cargo"})

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cargo not found")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
