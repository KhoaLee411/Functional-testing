import pytest

# Demo assert function to test the add function
def add(a, b): 
    return a + b

def test_super_normal_add():
    assert add(3, 5) == 8

# Demo using parametrized to test multiple test cases
# at the same time
@pytest.mark.parametrize("a, b, expect", [
    [1, 2, 3],  [4, 5, 9]
])
def test_add_arrays(a, b, expect):
    output = a + b
    assert output == expect

# Demo using markers to skip some tests, or tell it 
# to run some tests, please see the documentation here
# to see more examples: https://blog.jetbrains.com/pycharm/2024/02/pytest-features/
@pytest.mark.skip(reason="This test should be skipped!")
def test_normal_add():
    assert add(5, 6) == 12