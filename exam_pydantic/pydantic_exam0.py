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
        person = Person(**data1)
        rich.print(person)

        print(person.model_dump())
        print("done")
    except ValidationError as e:
        print("Exception as str:")
        rich.print(e)
        print("Exception as json:")
        print(e.json())

def test2():
    try:
        person = Person(**data2)
        rich.print(person)
        
        print(person.model_dump())
        print("done")
    except ValidationError as e:
        print("Exception as str:")
        rich.print(e)
        print("Exception as json:")
        print(e.json())

if __name__ == "__main":
    test1()
    test2()
