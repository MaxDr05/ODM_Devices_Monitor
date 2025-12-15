import os
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from data.models import Base


# 确保整个过程中只有一个数据库管家
class DBManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # 这里的逻辑是：
        # 1. 看看 _instance 是不是空的？
        # 2. 如果是空的，加上锁（防止两个线程同时进来）
        # 3. 再看一眼是不是空的（双重检查），确认空，就造一个
        # 4. 下次再有人来调用，直接把造好的这个给他，不许造新的
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 防呆开关：如果有engine属性，说明有这个引擎了
        if hasattr(self, "engine"):
            return
        # 与数据库的连接地址
        db_host = os.getenv("DB_HOST", "127.0.0.1")

        self.db_url = (
            f"mysql+pymysql://root:root@{db_host}:3306/odm_test?charset=utf8mb4"
        )

        # 创建引擎（连接池）
        self.engine = create_engine(
            self.db_url,
            echo=True,  # 打印sql
            pool_recycle=3600,  # 自动回收时间
            pool_size=10,  # 连接池大小
            max_overflow=20,  # 超过池子大小时，最多再临时创建20个
        )

        # 创建会话工厂（线程安全版）
        self.Session_Factory = scoped_session(sessionmaker(bind=self.engine))

    def create_all_tables(self):
        # 这里的逻辑是：
        # Base.metadata: 拿着所有登记在册的图纸
        # create_all: 去数据库建表
        # bind=self.engine: 告诉它用哪个数据库连接去建
        Base.metadata.create_all(bind=self.engine)
        print("✅ 施工完毕：表结构已创建")


if __name__ == "__main__":
    db = DBManager()
    db.create_all_tables()
