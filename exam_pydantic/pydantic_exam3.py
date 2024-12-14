import json
from typing import Any, List

from typing_extensions import Annotated
import rich

from pydantic import (
    BaseModel,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
)
from pydantic.functional_validators import WrapValidator


def maybe_strip_whitespace(
    v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> int:
    if info.mode == 'json':
        assert isinstance(v, str), 'In JSON mode the input must be a string!'
        # you can call the handler multiple times
        try:
            return handler(v)
        except ValidationError:
            return handler(v.strip())
    assert info.mode == 'python'
    assert isinstance(v, int), 'In Python mode the input must be an int!'
    # do no further validation
    return v


MyNumber = Annotated[int, WrapValidator(maybe_strip_whitespace)]


class DemoModel(BaseModel):
    number: List[MyNumber]


print(DemoModel(number=[2, 8]))
#> number=[2, 8]

json_str = json.dumps({'number': [' 2 ', '8']})
print(DemoModel.model_validate_json(json_str))
#> number=[2, 8]

json_str = json.dumps({'number': [2, 8]})
json_dict = json.loads(json_str)
rich.print(DemoModel(**json_dict))


try:
    t1 = DemoModel(number=['2'])
    rich.print(t1)
except ValidationError as e:
    print(e)
    """
    1 validation error for DemoModel
    number.0
      Assertion failed, In Python mode the input must be an int!
    assert False
     +  where False = isinstance('2', int) [type=assertion_error, input_value='2', input_type=str]
    """

print()

try:
    t2 = DemoModel(number=[2, 4])
    rich.print(t2)
except ValidationError as e:
    print(e)
    """
    1 validation error for DemoModel
    number.1
      Assertion failed, 8 is not a square number
    assert ((8 ** 0.5) % 1) == 0 [type=assertion_error, input_value=4, input_type=int]
    """

print()