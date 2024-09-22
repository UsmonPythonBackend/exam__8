import uuid
from sqlalchemy_utils.types.choice import ChoiceType
from .database import Base
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, BigInteger, Boolean, Text, func, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class UserAdmin(Base):
    __tablename__ = 'user_admin'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(70))
    last_name = Column(String(70))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(50), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    furniture = relationship('Furniture', back_populates='user_admin')


class Client(Base):
    __tablename__ = 'client'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    comments = relationship('Comments', back_populates='client')
    orders = relationship("Order", back_populates="client")
    contact_comments = relationship('ContactComment', back_populates='client')
    socket = relationship('Socket', back_populates='client')
    payment = relationship('Payment', back_populates='client')


class Furniture(Base):
    __tablename__ = 'furniture'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_admin_id = Column(UUID(as_uuid=True), ForeignKey('user_admin.id'), nullable=False)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    review = Column(BigInteger, default=0)
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    order = relationship("Order", back_populates="furniture")
    user_admin = relationship('UserAdmin', back_populates='furniture')
    comments = relationship('Comments', back_populates='furniture', cascade="all, delete-orphan")
    socket = relationship('Socket', back_populates='furniture')


class Comments(Base):
    __tablename__ = 'comment'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('client.id'), nullable=False)
    furniture_id = Column(UUID(as_uuid=True), ForeignKey('furniture.id'), nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    client = relationship('Client', back_populates='comments')
    furniture = relationship('Furniture', back_populates='comments')


class ContactComment(Base):
    __tablename__ = 'contact_comment'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('client.id'), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(50), unique=True, nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    client = relationship('Client', back_populates='contact_comments')


class Socket(Base):
    __tablename__ = 'socket'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('client.id'), nullable=False)
    furniture_id = Column(UUID(as_uuid=True), ForeignKey("furniture.id"))
    quantity = Column(Integer, default=1)
    total_price = Column(Float)
    created_at = Column(DateTime(timezone=True), default=func.now())

    furniture = relationship('Furniture', back_populates='socket')
    client = relationship('Client', back_populates='socket')


class Order(Base):
    OrderChoice = (
        ('pn', 'Pending'),
        ('tr', 'In Transit'),
        ('cd', 'Completed')
    )

    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.id"))
    furniture_id = Column(UUID(as_uuid=True), ForeignKey("furniture.id"))
    quantity = Column(Integer, default=1)
    order_status = Column(ChoiceType(OrderChoice, impl=String()), default='pn')
    total_price = Column(Float)
    order_date = Column(DateTime(timezone=True), default=func.now())

    furniture = relationship("Furniture", back_populates="order")
    client = relationship("Client", back_populates="orders")
    cargo = relationship("Cargo", back_populates="order", uselist=False)
    payment = relationship("Payment", back_populates="order", uselist=False)


class Cargo(Base):
    DeliveryStatus = (
        ('pn', 'Pending'),
        ('tr', 'In Transit'),
        ('go', 'Delivered')
    )

    __tablename__ = "cargo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    delivery_address = Column(String)
    delivery_status = Column(ChoiceType(DeliveryStatus, impl=String()), default='pn')
    estimated_delivery_date = Column(Date)

    order = relationship("Order", back_populates="cargo")


class Payment(Base):
    PaymentChoice = (
        ('pn', 'Pending'),
        ('cd', 'Completed'),
        ('fd', 'Failed')
    )
    PaymentType = (
        ('cd', 'Card'),
        ('bn', 'Bank Transfer'),
        ('cs', 'Cash')
    )
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.id"))
    amount = Column(Float)
    payment_status = Column(ChoiceType(PaymentChoice, impl=String()), default='pn')
    payment_type = Column(ChoiceType(PaymentType, impl=String()), default='cd')

    order = relationship("Order", back_populates="payment")
    client = relationship("Client", back_populates="payment")
