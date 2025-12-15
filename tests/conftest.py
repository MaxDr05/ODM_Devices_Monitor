import pytest
from api.device_api import DeviceClient
from utils.db_manager import DBManager


# 手动创建一个数据库管理器
@pytest.fixture(scope="session")
def dbmanager():
    """
    全局数据库管理器
    scope="session" 保证整个测试过程只初始化一次连接池
    """
    dbmanager = DBManager()
    # 【新增】确保表结构存在
    # 这行代码在 Docker 环境下至关重要！因为新起的 DB 容器是空的。
    print("\n🔨 [Init] 正在检查并创建数据库表...")
    dbmanager.create_all_tables()
    yield dbmanager


@pytest.fixture(scope="function")
def dbsession(dbmanager):
    """
    时光机 Session：每个用例独享一个事务，用完回滚
    """
    # 1. 【手动接线】从连接池申请一个物理连接
    connection = dbmanager.engine.connect()
    # 2. 【记录快照】开启最外层事务 (Start Transaction)
    # 重点：要拿到这个 transaction 对象，后面才能精准回滚它
    transaction = connection.begin()
    # 3. 【偷天换日】创建一个 Session，并强行绑定到上面这根连接上
    # 解释：这里直接调用工厂()，就会生成一个 Session 实例
    # bind=connection：告诉 Session，别自己去申请连接了，就用我手里这根！
    session = dbmanager.Session_Factory(bind=connection)

    # 4. 【交付使用】把这个“被骗了”的 Session 交给测试用例
    yield session

    # --- 测试结束，开始清理 ---

    # 5. 【清理现场】关闭 Session (这会清空 Session 里的缓存，但不会关闭物理连接，因为连接是我们手动传进去的)
    session.close()

    # 6. 【时光倒流】回滚最外层的事务
    # 这一步是核心！它撤销了 connection 上发生的所有操作
    transaction.rollback()

    # 7. 【归还资源】把物理连接还回连接池
    connection.close()

    dbmanager.Session_Factory.remove()


# 创建设备客户端
@pytest.fixture
def client():

    Device_client = DeviceClient()

    yield Device_client
