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
    'languages':['pt-pt', 'en-us']
}

data2 = {
    'age': 10,
    'name': 'John',
    'is_married': False,
    'address': {
        'street': 'st street',
        'building': 'test'
    },
    'languages':[{}, 'en-us']
}
 
def test1():

    try:
        rich.print(data1)
        person = Person(**data1)
        rich.print(person)

        print(person.model_dump())
        print("test1 done")
    except ValidationError as e:
        print("Exception as str:")
        rich.print(e)
        print("Exception as json:")
        print(e.json())
        print("test1 failed")

def test2():
    try:
        rich.print(data2)
        person = Person(**data2)
        rich.print(person)

        print(person.model_dump())
        print("test2 done")
    except ValidationError as e:
        print("Exception as str:")
        rich.print(e)
        print("Exception as json:")
        print(e.json())
        print("test2 failed")


if __name__ == "__main__":
    test1()
    print()
    test2()
