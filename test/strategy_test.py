import os
import pytest
import src.strategy as strategies
from src.colors import EnumColor
from src.image import Image
from src.matrix import Matrix


STRATEGIES = [(strategies.Randomize),
              (strategies.Linear),
              (strategies.LinearVertical),
              (strategies.QuickFill)]


@pytest.fixture(scope="module")
def image():
    file = os.path.join(os.path.dirname(__file__), 'img', 'test_5x5.png')
    return Image(file, 3, 15)


@pytest.fixture
def canvas_and_image(image):

    def _canvas_and_image(start_x, start_y, complete=False):
        canvas = Matrix(1, 0, 0)
        if complete:
            for x in range(image.image.width):
                for y in range(image.image.height):
                    color = EnumColor.rgba(image.pix[x, y], True)
                    canvas.update(x + start_x, y + start_y, color)
        return (canvas, image)

    return _canvas_and_image


@pytest.mark.parametrize("strategy", STRATEGIES)
def test_strategies_choose_all_valid_pixels(strategy, canvas_and_image):
    canvas, image = canvas_and_image(100, -123)
    strat = strategy(canvas, image, 100, -123)
    i = 0
    for pixel in strat.pixels():
        assert image.pix[pixel[0] - 100, pixel[1] + 123][0:3] == pixel[2].rgb
        canvas.update(*pixel)
        i += 1
    assert i == 20  # don't paint when alpha == 0


@pytest.mark.parametrize("strategy", STRATEGIES)
def test_strategies_detect_updates(strategy, canvas_and_image):
    canvas, image = canvas_and_image(-4, 300, complete=True)
    strat = strategy(canvas, image, -4, 300)
    assert len(list(strat.pixels())) == 0

    canvas.update(-3, 304, EnumColor.ENUM[0])
    i = 0
    for pixel in strat.pixels():
        assert (-3, 304) == pixel[0:2]
        assert EnumColor.ENUM[6].rgba == pixel[2].rgba
        canvas.update(*pixel)
        i += 1
    assert i == 1
