from data.models import User, Device


def test_relation_rollback(dbsession):
    session = dbsession

    user = User(username="owner_u1")
    session.add(user)
    session.flush()
    device = Device(sn="device_001", owner_id=user.id)

    session.add(device)
    session.flush()

    # 3. 事务内验证 (应该能查到)
    # 验证关联关系是否正确
    saved_device = session.query(Device).filter_by(sn="device_001").first()
    assert saved_device is not None
    assert saved_device.owner_id == user.id

    print("✅ 事务内校验通过！")
