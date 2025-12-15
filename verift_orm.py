from requests import session

from utils.db_manager import DBManager
from data.models import User, Device


def test_orm_workflow():
    db = DBManager()
    session = db.Session_Factory()

    try:
        print("--- 1. 准备插入数据 ---")
        # 创建一个 Python 对象 (这在以前就是一条 INSERT SQL 语句)
        new_user = User(username="iphone 16")

        # 放到柜台上 (Staging)
        session.add(new_user)

        # 敲定 (Commit) -> 这时候才真正发生 SQL 交互
        session.commit()
        print(f"✅ 用户插入成功！ID 已自动生成: {new_user.id}")

        print("\n--- 2. 准备查询数据 ---")
        # ORM 查询：我要找 User 表里，名字叫 calvin_test 的那个人
        # .first() 表示只要第一个匹配的
        user_in_db = session.query(User).filter_by(username="iphone 16").first()

        if user_in_db:
            print(f"🎉 查到了！数据库里的数据: {user_in_db}")
            print(f"   创建时间: {user_in_db.created_at}")
        else:
            print("❌ 奇怪，没查到...")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        # 如果报错了，回滚事务，撤销刚才的操作
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    test_orm_workflow()
