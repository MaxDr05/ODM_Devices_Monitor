from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


# 继承这个基类的类都是数据库表
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"  # 数据库里显示的表名

    # 定义列：主键、自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 定义列：用户名、字符串长度50，不能为空
    username = Column(String(50), nullable=False)
    # 定义列:创建时间，默认使用数据库服务器的当前时间
    created_at = Column(DateTime, server_default=func.now())


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sn = Column(String(50), unique=True, nullable=False)  # 序列号唯一
    # 外键：关联到users表的id字段
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), unique=True, nullable=False, comment="商品编码")
    price = Column(Integer, nullable=False, comment="价格")
