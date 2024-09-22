from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from .routers.admin_user_router import admin_user_router
from .routers.client_router import client_router
from .routers.comment_router import comment_router
from .routers.order_router import order_router
from .routers.cargo_router import cargo_router
from .routers.furniture_router import furniture_router
from .routers.payment_router import payments_router
from .schemas.admin_user_schema import Settings

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(admin_user_router)
app.include_router(client_router)
app.include_router(furniture_router)
app.include_router(order_router)
app.include_router(comment_router)
app.include_router(cargo_router)
app.include_router(payments_router)
