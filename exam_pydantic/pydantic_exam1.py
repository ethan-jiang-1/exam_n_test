from typing import Dict, List, Literal, Tuple

from annotated_types import Gt

from pydantic import BaseModel
import rich


class Fruit(BaseModel):
    name: str  
    color: Literal['red', 'green']  
    weight: float
    bazam: Dict[str, List[Tuple[int, bool, float]]]  

def test():
    ft = Fruit(
            name='Apple',
            color='red',
            weight=4.2,
            bazam={'foobar': [(1, True, 0.1)]},
        )
    rich.print(ft)
    print(type(ft))

if __name__ == "__main__":
    test()
