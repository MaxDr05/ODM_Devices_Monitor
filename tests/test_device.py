import pytest
from utils.file_reader import read_yaml

test_data = read_yaml("data/test_data.yaml")


@pytest.mark.parametrize("test_case", test_data)
def test_device_lifecycle(test_case, client):

    # 测试注册新设备
    res = client.register_device(
        device_name=test_case["device_name"], device_version=test_case["device_version"]
    )
    assert res["json"]["name"] == test_case["device_name"]
    id = "1"

    # 测试查询设备
    res = client.search_device(device_id=id)
    assert res["args"]["id"] == id

    # 测试更新设备
    res = client.update_version(
        device_id=id, device_version=test_case["device_version"]
    )
    assert res["json"]["job"] == test_case["device_version"]

    # 测试注销设备
    res = client.unregister_device(device_id=id)
    assert res == 200
