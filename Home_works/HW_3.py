# Задача 1: Создайте экземпляр движка для подключения к SQLite
# базе данных в памяти.
# Задача 2: Создайте сессию для взаимодействия с базой данных,
# используя созданный движок.
# Задача 3: Определите модель продукта Product со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# price: числовое значение с фиксированной точностью
# in_stock: логическое значение
# Задача 4: Определите связанную модель категории Category
# со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# description: строка (макс. 255 символов)
# Задача 5: Установите связь между таблицами Product и Category с
# помощью колонки category_id.
from itertools import product

from sqlalchemy import (create_engine,
                        Column, Integer,
                        String, Numeric,
                        Boolean, ForeignKey )
from sqlalchemy.orm import (sessionmaker,
                            DeclarativeBase,
                            relationship, Mapped,
                            mapped_column)
from unicodedata import category

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)


class Category(Base):
    __tablename__ = 'categories'

    name = Column(String(100), nullable=False)
    description = Column(String(255))

    products = relationship('Product', back_populates='category')

class Product(Base):
    __tablename__ = 'products'

    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='products')

Base.metadata.create_all(engine)

category = Category(name="Electronics", description="Electronic devices" )
product = Product(name="Smartphone", price=500.99, in_stock=True, category_id=category.id)

session.add(category)
session.add(product)
session.commit()

for p in session.query(Product).all():
    print(p.name, p.price, p.in_stock)