"""Разработать систему регистрации пользователя, используя Pydantic
для валидации входных данных, обработки вложенных структур и сериализации.
Система должна обрабатывать данные в формате JSON.
Задачи:
Создать классы моделей данных с помощью Pydantic для пользователя
и его адреса.
Реализовать функцию, которая принимает JSON строку, десериализует
её в объекты Pydantic, валидирует данные, и в случае успеха сериализует
объект обратно в JSON и возвращает его.
Добавить кастомный валидатор для проверки соответствия возраста
и статуса занятости пользователя.
Написать несколько примеров JSON строк для проверки различных сценариев
валидации: успешные регистрации и случаи, когда валидация не проходит
(например возраст не соответствует статусу занятости).
Модели:
Address: Должен содержать следующие поля:
city: строка, минимум 2 символа.
street: строка, минимум 3 символа.
house_number: число, должно быть положительным.
User: Должен содержать следующие поля:
name: строка, должна быть только из букв, минимум 2 символа.
age: число, должно быть между 0 и 120.
email: строка, должна соответствовать формату email.
is_employed: булево значение, статус занятости пользователя.
address: вложенная модель адреса.
Валидация:
Проверка, что если пользователь указывает, что он занят
(is_employed = true), его возраст должен быть от 18 до 65 лет.
# Пример JSON данных для регистрации пользователя"""

json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

from pydantic import BaseModel, EmailStr,  Field, model_validator
import json


class Address(BaseModel):
    city: str = Field(..., min_length=2,
                      description="Название города должно содержать минимум 2 символа")
    street: str = Field(..., min_length=3,
                        description="Название улицы должно содержать минимум 3 символа")
    house_number: int = Field(..., gt=0,
                              description="Номер дома должен быть положительным числом")



class User(BaseModel):
    name: str = Field(..., min_length=2,
                      pattern=r"^[A-Za-zА-Яа-яЁё\s]+$",
                      description="Имя должно состоять только из букв и пробелов"
                      )
    age: int = Field(..., gt=0, le=120,
                     description="Возраст от 0 до 120 лет")
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode="after")
    def check_employment_age(self):
        if self.is_employed and not  ( 18 <= self.age <= 65 ):
            raise ValueError("""Если пользователь трудоустроен, возраст
                              должен быть от 18 до 65 лет""")
        return self

data = json.loads(json_input)
print(User(**data))



