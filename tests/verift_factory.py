import pytest
from tests.factories import UserFactory
from data.models import User


# 使用时光机 fixture
def test_factory_generation(dbsession):
    print("\n--- 🏭 数据工厂流水线启动 ---")

    # 【核心】把工厂绑定到当前的时光机 Session
    UserFactory._meta.sqlalchemy_session = dbsession

    # 1. 生产一个单品
    print(">>> 正在生产单个用户...")
    user_1 = UserFactory()
    # 修正：去掉了 email 打印
    print(f"✅ 产出: ID={user_1.id}, Name={user_1.username}")

    # 2. 批量生产
    print("\n>>> 正在批量生产 5 个用户...")
    users = UserFactory.create_batch(5)

    for u in users:
        print(f"📦 [Batch] ID={u.id} | Name: {u.username}")

    # 3. 验证数据库 (在当前事务内)
    count = dbsession.query(User).count()
    print(f"\n📊 数据库当前库存: {count} 人")
    assert count >= 6

    # 测试结束，时光机回滚
