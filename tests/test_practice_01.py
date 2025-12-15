import pytest
from tests.factories import ProductFactory


def test_create_products(dbsession):
    print("\n--- 🛒 商品工厂流水线 ---")

    # 1. 绑定时光机 Session
    ProductFactory._meta.sqlalchemy_session = dbsession

    # 2. 批量生产 3 个
    products = ProductFactory.create_batch(3)

    # 3. 打印验证
    for p in products:
        print(f"📦 产出商品: ID={p.id} | SKU={p.sku} | Price=${p.price}")

    # 4. 断言
    assert len(products) == 3
    assert products[0].sku.startswith("SKU_")
