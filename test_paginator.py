import pytest
from paginator import Paginator

def test_wrong_parameters_types():
    """ Test if TypeError is raised when any input type is wrong"""
    with pytest.raises(TypeError) as error1:
        Paginator('1', 1, 0, 0)
    with pytest.raises(TypeError) as error2:
        Paginator(1, '1', 0, 0)
    with pytest.raises(TypeError) as error3:
        Paginator(1, 1, '0', 0)
    with pytest.raises(TypeError) as error4:
        Paginator(1, 1, 0, '0')
    assert (str(error1.value) == str(error2.value) == str(error3.value) 
            == str(error4.value) == 'At least one parameter type is not supported. All parameters should be int.')
    
def test_positive_out_of_range_boundary():
    """ Test if ValueError is raised if boundary size is out of range"""
    with pytest.raises(ValueError) as error:
        Paginator(1, 1, 5, 0)
    assert str(error.value) == 'Boundary size is out of the maximum total pages range.'

def test_using_positive_out_of_range_around():
    """ Test if ValueError is raised if around size is out of range"""
    with pytest.raises(ValueError) as error:
        Paginator(1, 1, 0, 10)
    assert str(error.value) == 'Around size is out of the maximum total pages range.'

def test_using_positive_out_of_range_current_page():
    """ Test if ValueError is raised if current page value is out of range"""
    with pytest.raises(ValueError) as error:
        Paginator(5, 1, 0, 0)
    assert str(error.value) == 'Current page position is out of the maximum total pages range.'

def test_using_positive_out_of_range_total_pages():
    """ Test if ValueError is raised if total pages value is out of positive 64bits range"""
    with pytest.raises(ValueError) as error:
        Paginator(1, 2**63 + 1, 0, 5)
    assert str(error.value) == 'Total page is out of the positive range of 64bits.'

def test_using_negative_out_of_range_boundary():
    """ Test if ValueError is raised if boundary size is lower than 0"""
    with pytest.raises(ValueError) as error:
        Paginator(1, 1, -5, 0)
    assert str(error.value) == 'Boundary size is out of the maximum total pages range.'

def test_using_negative_out_of_range_around():
    """ Test if ValueError is raised if around size is lower than 0"""
    with pytest.raises(ValueError) as error:
        Paginator(1, 1, 0, -10)
    assert str(error.value) == 'Around size is out of the maximum total pages range.'

def test_when_current_page_equals_0():
    """ Test if ValueError is raised if current page value is lower than 1"""
    with pytest.raises(ValueError) as error:
        Paginator(0, 1, 0, 0)
    assert str(error.value) == 'Current page position is out of the maximum total pages range.'

def test_when_total_pages_equals_0():
    """ Test if ValueError is raised if total pages value is lower than 1"""
    with pytest.raises(ValueError) as error:
        Paginator(0, 0, 0, 5)
    assert str(error.value) == 'Total page is out of the positive range of 64bits.'

def test_when_current_page_value_is_negative():
    """ Test if ValueError is raised if current page value is lower than 1"""
    with pytest.raises(ValueError) as error:
        Paginator(-1, 1, 0, 0)
    assert str(error.value) == 'Current page position is out of the maximum total pages range.'

def test_when_total_pages_value_is_negative():
    """ Test if ValueError is raised if total pages value is lower than 1"""
    with pytest.raises(ValueError) as error:
        Paginator(-1, 0, 0, 5)
    assert str(error.value) == 'Total page is out of the positive range of 64bits.'

def test_boundary_bigger_than_total_pages():
    """ Should early return in this case"""
    paginator = Paginator(5, 10, 0, 5)
    assert hasattr(paginator, 'early_return')

def test_around_bigger_than_total_pages():
    """ Should early return in this case"""
    paginator = Paginator(5, 10, 5, 0)
    assert hasattr(paginator, 'early_return')

def test_around_plus_bondary_bigger_than_total_pages():
    """ Should early return in this case"""
    paginator = Paginator(5, 10, 5, 5)
    assert hasattr(paginator, 'early_return')

def test_around_equals_to_zero_return():
    """ Should early return in this case"""
    paginator = Paginator(1, 5, 1, 0)
    assert hasattr(paginator, 'early_return')
    assert paginator.around == []

def test_around_respect_interval_range():
    """ Should early return in this case"""
    paginator = Paginator(1, 20, 1, 5)
    assert paginator.around[0] >= 1
    paginator1 = Paginator(20, 20, 1, 5)
    assert paginator1.around[-1] <= 20

def test_first_result_piece_should_be_gap():
    """ When there is no boundary and the current page is in the middle"""
    paginator = Paginator(10, 20, 0, 5)
    assert paginator.pagination_list[0] == '...'

def test_complete_case_when_boundary_equals_zero():
    """ 
    Testing define_boundaries method early return 
    when boundary == 0
    """
    paginator = Paginator(5, 10, 0, 1)
    r1, r2 = paginator.define_boundaries()
    assert hasattr(paginator, 'early_return')
    assert r1 == []
    assert r2 == []

def test_complete_case_when_boundary_is_valid():
    """
    Testing define_boundaries method early return 
    when boundary is valid
    """
    paginator = Paginator(5, 8, 2, 1)
    r1, r2 = paginator.define_boundaries()
    assert not hasattr(paginator, 'early_return')
    assert r1 == [1, 2]
    assert r2 == [7, 8]

def test_case_when_there_is_boundary_and_gap_until_around():
    """
    Testing case when there is boundary and a gap between the
    left boundary and the around range.
    """
    paginator = Paginator(10, 16, 2, 3)
    assert paginator.pagination_list[0] == 1
    assert paginator.pagination_list[1] == 2

def test_case_when_there_is_gap_until_current_page():
    """
    Testing case where there is a gap until current page
    """
    paginator = Paginator(16, 16, 0, 0)
    assert paginator.pagination_list[0] == '...'
    assert paginator.pagination_list[1] == 16

def test_case_where_is_like_gap__current_page__gap():
    """
    Testing a common case where there isn't boundary neither around,
    and the current page is in the middle situation.
    """
    paginator = Paginator(10, 16, 0, 0)
    assert paginator.pagination_list[0] == '...'
    assert paginator.pagination_list[1] == 10
    assert paginator.pagination_list[2] == '...'

def test_case_where_is_like_gap__around__current_page__around__gap():
    """
    Testing a common case where there is no boundary, has around and the
    current page is in the middle situation.
    """
    paginator = Paginator(10, 16, 0, 2)
    assert paginator.pagination_list[0] == '...'
    assert paginator.pagination_list[1] == 8
    assert paginator.pagination_list[3] == 10
    assert paginator.pagination_list[5] == 12
    assert paginator.pagination_list[6] == '...'

def test_case_where_is_like_boundary__around__current_page__around__boundary():
    """
    Testing a common case where there is a boundary, around and the current page
    is in the middle situation.
    """
    paginator = Paginator(8, 16, 5, 2)
    assert paginator.pagination_list[0] == 1
    assert paginator.pagination_list[1] == 2
    assert paginator.pagination_list[6] == 7
    assert paginator.pagination_list[7] == 8
    assert paginator.pagination_list[8] == 9
    assert paginator.pagination_list[15] == 16

def test_simplest_paginator_message_value():
    """ Test the simplest paginator when is only 1"""
    assert Paginator(1, 1, 0, 0).message == '1'

def test_current_page_in_the_beginning():
    """ Test the valid case starting with the current page"""
    assert Paginator(1, 10, 2, 2).message == '1 2 3 ... 9 10'
    assert Paginator(1, 15, 5, 1).message == '1 2 3 4 5 ... 11 12 13 14 15'
    assert Paginator(1, 8, 0, 5).message == '1 2 3 4 5 6 ...'

def test_current_page_in_the_middle():
    """ Test the valid case with the current page in the middle"""
    assert Paginator(10, 20, 2, 2).message == '1 2 ... 8 9 10 11 12 ... 19 20'

def test_current_page_in_the_end():
    """ Test the valid case ending with the current page"""
    assert Paginator(20, 20, 2, 2).message == '1 2 ... 18 19 20'

def test_exercise_example_1():
    """ Test the test proposal example 01"""
    assert Paginator(4, 5, 1, 0).message == '1 ... 4 5'

def test_exercise_example_2():
    """ Test the test proposal example 02"""
    assert Paginator(4, 10, 2, 2).message == '1 2 3 4 5 6 ... 9 10'