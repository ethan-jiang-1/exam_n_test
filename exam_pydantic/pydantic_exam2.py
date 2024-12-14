from typing import Any, List

from typing_extensions import Annotated

from pydantic import BaseModel, ValidationError
from pydantic.functional_validators import AfterValidator
import rich


def check_squares(v: int) -> int:
    assert v**0.5 % 1 == 0, f'{v} is not a square number'
    return v


def double(v: Any) -> Any:
    return v * 2


MyNumber = Annotated[int, AfterValidator(double), AfterValidator(check_squares)]


class DemoModel(BaseModel):
    number: List[MyNumber]

def test():
    t1 = DemoModel(number=[2, 8])
    rich.print(t1)
    rich.print(t1.model_dump())
    rich.print(t1.model_dump_json())

    try:
        t2 = DemoModel(number=[2, 4])
        rich.print(t2)
    except ValidationError as e:
        rich.print(e)
        """
        1 validation error for DemoModel
        number.1
        Assertion failed, 8 is not a square number
        assert ((8 ** 0.5) % 1) == 0 [type=assertion_error, input_value=4, input_type=int]
        """

if __name__ == "__main__":
    test()
