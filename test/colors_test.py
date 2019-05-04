import pytest
from src.colors import EnumColor

# .index
def test_index_returns_color_at_given_index():
    assert EnumColor.ENUM[3] == EnumColor.index(3)

def test_index_returns_white_by_default():
    color = EnumColor.index(999)
    assert color.name == "white"

def test_index_handles_nonsense():
    color = EnumColor.index("frog")
    assert color.name == "white"

# .rgb
def test_rgb_returns_a_3_tuple_of_rgb_values():
    assert EnumColor.ENUM[0].rgb == (255, 255, 255)

# .rgba
def test_rgba_returns_same_color_with_given_alpha_if_rgb_matches_exactly():
    color = EnumColor.ENUM[10]
    result = EnumColor.rgba((2, 190, 1, 123))
    assert color == result
    assert color.alpha != result.alpha
    assert 123 == result.alpha

def test_rgba_ignores_alpha_when_comparing_colors():
    expected_color = EnumColor.ENUM[0] # (255, 255, 255, 255)
    assert expected_color == EnumColor.rgba((255, 255, 255, 0))

def test_rgba_returns_closest_color_object_if_rgba_doesnt_match():
    expected_color = EnumColor.ENUM[9] # (148, 224, 68, 255)
    assert expected_color == EnumColor.rgba((130, 250, 65, 3))

# equality
def test_colors_are_equal_if_rbg_and_name_are_the_same():
    color_1 = EnumColor.rgba((255, 255, 255, 0))
    color_2 = EnumColor.rgba((255, 255, 255, 255))
    color_3 = EnumColor.rgba((0, 255, 255, 0))
    color_4 = EnumColor.Color(0, 'noncolor', (255, 255, 255, 0))
    assert color_1 == color_2
    assert not color_1 != color_2 # test __ne__()
    assert color_1 != color_3
    assert color_1 != color_4

def test_color_equality_works_with_bad_values():
    color = EnumColor.index(0)
    assert color != None
    assert color != 5
    assert color != "i am not a color"
