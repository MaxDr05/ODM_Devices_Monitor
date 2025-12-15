import pytest
from tests.factories import UserFactory, ProductFactory, DeviceFactory


def test_1_n(dbsession):
    print("------流水线开始运作-------")

    UserFactory._meta.sqlalchemy_session = dbsession
    DeviceFactory._meta.sqlalchemy_session = dbsession

    user = UserFactory.create_batch(1)

    devices = DeviceFactory.create_batch(5, owner_id=user[0].id)

    assert len(devices) == 5

    for device in devices:
        assert device.owner_id == user[0].id
        print(f"-------------{device.owner_id} 验证通过！ -------------")
