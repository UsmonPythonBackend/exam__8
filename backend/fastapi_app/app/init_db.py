from .database import Base, ENGINE
from .models import UserAdmin, Client, Comments, ContactComment, Socket, Furniture, Cargo, Payment, Order


def migrate():
    Base.metadata.create_all(bind=ENGINE)
