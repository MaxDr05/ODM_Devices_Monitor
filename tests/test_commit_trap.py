import pytest
from data.models import User


# 引用我们的时光机 fixture
def test_commit_trap(dbsession):
    print("\n--- 💣 陷阱测试开始 ---")

    # 1. 准备数据
    username = "trap_user"  # 这个名字听起来就不吉利

    # 2. 插入数据
    new_user = User(username=username)
    dbsession.add(new_user)

    # 3. 【高危动作】显式调用 commit()
    # 假设新手不懂规矩，觉得“不提交怎么行？”，于是写了这一行
    print(">>> 正在执行高危操作: session.commit() ...")
    dbsession.commit()
    print(">>> Commit 执行完毕")

    # 4. 验证（肯定能查到）
    user_in_db = dbsession.query(User).filter_by(username=username).first()
    assert user_in_db is not None
    print(f"✅ 也就是在这一刻，'{username}' 被永久钉在了耻辱柱（数据库）上")

    # 5. 测试结束，Fixture 会尝试 rollback
    # 但我们来看看，还有救吗？
