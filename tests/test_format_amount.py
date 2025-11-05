from src.allowances import format_amount

def test_format_amount_basic():
    assert format_amount(0, 18) == "0"
    assert format_amount(10**18, 18) == "1"
    assert format_amount(1234500000000000000, 18) == "1.2345"

def test_format_amount_zero_decimals():
    assert format_amount(42, 0) == "42"
