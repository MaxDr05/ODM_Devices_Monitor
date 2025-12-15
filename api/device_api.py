from core.client import ApiClient


# 设备客户端
class DeviceClient(ApiClient):

    def __init__(self):
        super().__init__()

    # 注册设备
    def register_device(self, device_name, device_version):
        res = self.send_request(
            path="/post",
            method="POST",
            timeout=20,
            json={"name": device_name, "job": device_version},
        )

        return res.json()

    # 查询单个设备
    def search_device(self, device_id):
        res = self.send_request(path="/get", method="GET", params={"id": device_id})

        return res.json()

    # 更新固件
    def update_version(self, device_id, device_version):
        res = self.send_request(
            path="/put",
            method="PUT",
            timeout=20,
            json={"job": device_version},
        )

        return res.json()

    # 注销设备
    def unregister_device(self, device_id):
        res = self.send_request(
            path="/delete", method="DELETE", params={"id": device_id}
        )

        return res.status_code
