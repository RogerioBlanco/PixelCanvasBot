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
