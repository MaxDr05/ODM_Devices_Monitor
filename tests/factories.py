import factory
from factory import Faker
from data.models import User, Device, Product
from utils.db_manager import DBManager


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User

        sqlalchemy_session = None

        sqlalchemy_session_persistence = "flush"

    id = factory.Sequence(lambda n: 10000 + n)

    username = Faker("name")


class DeviceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Device
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    sn = factory.Sequence(lambda n: f"SKU_2025_{n:03d}")


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product

        sqlalchemy_session = None

        sqlalchemy_session_persistence = "flush"

    sku = factory.Sequence(lambda n: f"SKU_{1001+n}")
    price = factory.Faker("random_int", min=10, max=1000)
