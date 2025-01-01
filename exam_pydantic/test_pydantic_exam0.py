from pydantic_exam0 import func1, func2

def test_valid_person_data():
    result = func1()
    assert isinstance(result, dict)
    assert result["age"] == 10
    assert result["name"] == "John"
    assert result["is_married"] is False
    assert result["address"]["street"] == "st street"
    assert result["address"]["building"] == 10
    assert result["languages"] == ["pt-pt", "en-us"]

def test_invalid_person_data():
    result = func2()
    assert result is None  # 因为验证失败会返回None

def test_custom_valid_data():
    custom_data = {
        'age': 25,
        'name': 'Alice',
        'is_married': True,
        'address': {
            'street': 'main street',
            'building': 42
        },
        'languages': ['zh-cn', 'en-us']
    }
    result = func1(custom_data)
    assert result["age"] == 25
    assert result["name"] == "Alice"
    assert result["languages"] == ['zh-cn', 'en-us']

def test_invalid_address_type():
    invalid_data = {
        'age': 30,
        'name': 'Bob',
        'is_married': False,
        'address': 'invalid address',  # 应该是一个字典
        'languages': ['en-us']
    }
    result = func1(invalid_data)
    assert result is None

def test_invalid_language_type():
    invalid_data = {
        'age': 30,
        'name': 'Bob',
        'is_married': False,
        'address': {
            'street': 'test street',
            'building': 1
        },
        'languages': 'english'  # 应该是一个列表
    }
    result = func1(invalid_data)
    assert result is None 

def test_missing_required_field():
    invalid_data = {
        'age': 30,
        'name': 'Bob',
        'is_married': False,
        'languages': ['en-us']
        # missing address field
    }
    result = func1(invalid_data)
    assert result is None

def test_empty_values():
    invalid_data = {
        'age': 30,
        'name': '',  # empty string
        'is_married': False,
        'address': {
            'street': '',  # empty street
            'building': 1
        },
        'languages': []  # empty list
    }
    result = func1(invalid_data)
    assert result is not None  # 空值应该是允许的
    assert result['name'] == ''
    assert result['address']['street'] == ''
    assert result['languages'] == []

def test_invalid_age():
    invalid_data = {
        'age': -1,  # negative age
        'name': 'Bob',
        'is_married': False,
        'address': {
            'street': 'test street',
            'building': 1
        },
        'languages': ['en-us']
    }
    result = func1(invalid_data)
    assert result is not None  # age没有验证规则，应该通过

def test_invalid_building_number():
    invalid_data = {
        'age': 30,
        'name': 'Bob',
        'is_married': False,
        'address': {
            'street': 'test street',
            'building': -1  # negative building number
        },
        'languages': ['en-us']
    }
    result = func1(invalid_data)
    assert result is not None  # building没有验证规则，应该通过

def test_extra_fields():
    data_with_extra = {
        'age': 30,
        'name': 'Bob',
        'is_married': False,
        'address': {
            'street': 'test street',
            'building': 1,
            'extra_field': 'should be ignored'  # extra field in address
        },
        'languages': ['en-us'],
        'extra_field': 'should be ignored'  # extra field in person
    }
    result = func1(data_with_extra)
    assert result is not None
    assert 'extra_field' not in result
    assert 'extra_field' not in result['address'] 