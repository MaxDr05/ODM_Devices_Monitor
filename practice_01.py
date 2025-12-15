from utils.db_manager import DBManager
from data.models import User


def verify_truth():
    print("--- 🏁 实验开始 ---")

    # 1. 基础设施
    db = DBManager()

    # 2. 开启“时光机” (外部事务)
    connection = db.engine.connect()
    transaction = connection.begin()
    print(f"1. 外部事务已开启 (Transaction Active: {transaction.is_active})")

    # 3. 绑定 Session
    session = db.Session_Factory(bind=connection)

    # 4. 插入数据
    user = User(username="truth_user")
    session.add(user)

    # 5. 【关键动作】执行 session.commit()
    # 请盯着控制台日志：有没有出现 "COMMIT" 这个词？
    print("\n>>> 准备执行 session.commit() <<<")
    session.commit()
    print(">>> session.commit() 执行完毕 <<<\n")

    # 6. 验证数据是否还在
    check_conn = db.engine.connect()

    # 【修复点】导入 text，并包裹 SQL 字符串
    from sqlalchemy import text

    # 使用 text(...) 包裹 SQL
    result = check_conn.execute(
        text("SELECT * FROM users WHERE username='truth_user'")
    ).fetchone()

    if result:
        print("😱 震惊！路人甲查到了数据！(说明真的 Commit 了)")
    else:
        print("✅ 路人甲没查到数据！(说明没 Commit，时光机还是安全的)")

    check_conn.close()

    # 7. 最后回滚
    transaction.rollback()
    connection.close()
    session.close()


if __name__ == "__main__":
    verify_truth()
