from typing import List
from pydantic import BaseModel, ValidationError
import rich
 
class Address(BaseModel):
    street: str
    building: int
 
class Person(BaseModel):
    age: int
    name: str
    is_married: bool
    address: Address
    languages: List[str]

data1 = {
    'age': 10,
    'name': 'John',
    'is_married': False,
    'address': {
        'street': 'st street',
        'building': 10
    },
    'languages': ['pt-pt', 'en-us']
}

data2 = {
    'age': 10,
    'name': 'John',
    'is_married': False,
    'address': {
        'street': 'st street',
        'building': 'test'
    },
    'languages': [{}, 'en-us']
}
 
def func1(data=None):
    if data is None:
        data = data1

    try:
        rich.print(data)
        person = Person(**data)
        rich.print(person)

        print(person.model_dump())
        print("test1 done")
        return person.model_dump()
    except ValidationError as e:
        print("Exception as str:")
        rich.print(e)
        print("Exception as json:")
        print(e.json())
        print("test1 failed")

def func2(data=None):
    if data is None:
        data = data2

    try:
        rich.print(data)
        person = Person(**data)
        rich.print(person)

        print(person.model_dump())
        print("test2 done")
        return person.model_dump()
    except ValidationError as e:
        print("Exception as str:")
        rich.print(e)
        print("Exception as json:")
        print(e.json())
        print("test2 failed")


if __name__ == "__main__":
    func1()
    print()
    func2()
