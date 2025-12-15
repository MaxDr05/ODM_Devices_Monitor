import requests
import os


# 帮助所有用例请求发送请求
class ApiClient:

    def __init__(self, base_url=None):
        # 创建连接池
        self.session = requests.session()
        # 优先读环境变量，读不到就用默认的
        # 注意：默认值改成 httpbin.org (本地跑时用)
        # 在 Docker Compose 里，我们会通过环境变量把它覆盖成 http://mock-server
        self.base_url = os.getenv("API_BASE_URL", "https://httpbin.org")
        # --- 修改：全套伪装（不仅仅是 User-Agent）---
        self.session.headers.update(
            {
                # 模拟 Chrome 浏览器标识
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                # 告诉服务器我接受 JSON 和文本
                "Accept": "application/json, text/plain, */*",
                # 告诉服务器我是英文环境（有的防火墙会拦没有语言头的请求）
                "Accept-Language": "en-US,en;q=0.9",
                # 保持连接
                "Connection": "keep-alive",
            }
        )

    def send_request(self, path, method, **kwargs):
        # 拼接目的地址
        path = f"{self.base_url}{path}"

        timeout = kwargs.pop("timeout", 15)

        # 发送方法
        res = self.session.request(method=method, url=path, **kwargs, timeout=timeout)

        # --- 新增：简单的调试辅助 ---
        # 如果状态码不是 2xx，打印出来看看发生了什么
        if res.status_code >= 400:
            print(f"\n[⚠️ 请求异常] Code: {res.status_code}, Body: {res.text[:200]}")

        return res
