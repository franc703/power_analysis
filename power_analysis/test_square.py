# In test_square.py
from power_analysis.square import square


def test_square():
    assert square(2) == 4
    assert square(-2) == 4
    assert square(0) == 0
