import pytest
from data.models import User


# 注意：这里我们请求的是 db_session 这个 fixture
def test_create_user_with_rollback(dbsession):
    print("\n--- 测试开始 ---")

    # 1. 准备数据
    username = "ghost_user"  # "幽灵用户"

    # 2. 插入数据
    new_user = User(username=username)
    dbsession.add(new_user)

    # 【重点】不要调用 commit()！
    # flush() 的作用是：把数据发给数据库，让它生成 ID，但暂时“不敲定”
    dbsession.flush()

    # 3. 验证：在当前 session 里，我是能查到这个人的
    # (证明业务逻辑是通的)
    user_in_db = dbsession.query(User).filter_by(username=username).first()
    assert user_in_db is not None
    assert user_in_db.id is not None
    print(f"✅ 测试中：成功查到用户 {user_in_db.username}, ID={user_in_db.id}")

    # 4. 测试结束，Fixture 会自动执行 rollback
