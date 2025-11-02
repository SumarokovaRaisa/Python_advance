"""Добавьте в базу данных следующие категории и продукты
Добавление категорий: Добавьте в таблицу categories следующие категории:
Название: "Электроника", Описание: "Гаджеты и устройства."
Название: "Книги", Описание: "Печатные книги и электронные книги."
Название: "Одежда", Описание: "Одежда для мужчин и женщин."
Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись,
что каждый продукт связан с соответствующей категорией:
Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда"""



from sqlalchemy import (create_engine,
                        Column, Integer,
                        String, Text,
                        Float, Boolean,
                        ForeignKey, func)
from sqlalchemy.orm import (declarative_base,
                            relationship,
                            sessionmaker)


Base = declarative_base()
engine = create_engine('sqlite:///categories.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    products = relationship('Product', back_populates='category')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products')


Base.metadata.create_all(engine)

if not session.query(Category).first():
    categories_data = [
            {"name": "Электроника", "description": "Гаджеты и устройства."},
            {"name": "Книги", "description": "Печатные книги и электронные книги."},
            {"name": "Одежда", "description": "Одежда для мужчин и женщин."}
        ]
    categories = []
    for cat in categories_data:
        category = Category(name=cat['name'], description=cat['description'])
        session.add(category)
        categories.append(category)
    session.commit()

    cat_electronics = session.query(Category).filter_by(name="Электроника").first()
    cat_books = session.query(Category).filter_by(name="Книги").first()
    cat_clothes = session.query(Category).filter_by(name="Одежда").first()

    products_data = [
        {"name": "Смартфон", "price": 299.99, "in_stock": True, "category": cat_electronics},
        {"name": "Ноутбук", "price": 499.99, "in_stock": True, "category": cat_electronics},
        {"name": "Научно-фантастический роман", "price": 15.99, "in_stock": True, "category": cat_books},
        {"name": "Джинсы", "price": 40.50, "in_stock": True, "category": cat_clothes},
        {"name": "Футболка", "price": 20.00, "in_stock": True, "category": cat_clothes}
    ]

    for prod in products_data:
        product = Product(**prod)
        session.add(product)
    session.commit()
print("База данных успешно создана и заполнена.")


"""Задача 2: Чтение данных
Извлеките все записи из таблицы categories. Для каждой категории извлеките
и выведите все связанные с ней продукты, включая их названия и цены."""

print("Список категорий и продуктов")
for category in session.query(Category).all():
    print(f"Категория: {category.name} - {category.description}")
    for product in category.products:
        print(f"{product.name} - {product.price} pyб.")



"""Задача 3: Обновление данных
Найдите в таблице products первый продукт с названием "Смартфон".
Замените цену этого продукта на 349.99."""


print("Обновление цены смартфона")
smartphone = session.query(Product).filter_by(name="Смартфон").first()
if smartphone:
    smartphone.price = 349.99
    session.commit()
    print(f"Цена обновлена: {smartphone.name} теперь стоит {smartphone.price} pуб.")
else:
    print("Смартфон не найден.")


"""Задача 4: Агрегация и группировка
Используя агрегирующие функции и группировку, подсчитайте общее
количество продуктов в каждой категории."""

print("Количество продуктов в каждой категории")
results = (session.query(Category.name, func.count(Product.id))
           .join(Product)
           .group_by(Category.id)
           .all())
for name, count in results:
    print(f"{name} - {count}")



"""Задача 5: Группировка с фильтрацией
Отфильтруйте и выведите только те категории, в которых более одного продукта."""

print("Категории с более чем одним продуктом")
filtered = (session.query(Category.name, func.count(Product.id).label("count"))
            .join(Product)
            .group_by(Category.id)
            .having(func.count(Product.id) > 1)
            .all())

for name, count in filtered:
    print(f"{name}: {count}")

print("Все задачи выполнены успешно")




