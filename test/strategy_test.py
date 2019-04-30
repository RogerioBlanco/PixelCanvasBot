import os
import pytest
import src.strategy as strategies
from src.colors import EnumColor
from src.image import Image
from src.matrix import Matrix


STRATEGIES = [(strategies.Randomize, {}),
              (strategies.Linear, {}),
              (strategies.LinearVertical, {}),
              (strategies.QuickFill, {}),
              (strategies.Radiate, {"px": 10, "py": -5}),
              (strategies.Spiral, {"px": 2, "py": 3}),
              (strategies.Spiral, {"px": -1000, "py": 3}),
              (strategies.Spiral, {"px": 2, "py": 3000}),
              (strategies.Spiral, {"px": 1000, "py": -3000})]


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


@pytest.mark.parametrize("strategy, opts", STRATEGIES)
def test_strategies_choose_all_valid_pixels(strategy, opts, canvas_and_image):
    canvas, image = canvas_and_image(1, -1)
    strat = strategy(canvas, image, 1, -1, **opts)
    i = 0
    chosen_coords = set()
    for pixel in strat.pixels():
        chosen_coords.add(pixel[0:2])
        assert image.pix[pixel[0] - 1, pixel[1] + 1][0:3] == pixel[2].rgb
        canvas.update(*pixel)
        i += 1
    assert i == 20  # don't paint when alpha == 0
    assert len(chosen_coords) == 20  # ensure all pixels chosen uniquely


@pytest.mark.parametrize("strategy, opts", STRATEGIES)
def test_strategies_detect_updates(strategy, opts, canvas_and_image):
    canvas, image = canvas_and_image(-1, 1, complete=True)
    strat = strategy(canvas, image, -1, 1, **opts)
    assert len(list(strat.pixels())) == 0

    canvas.update(2, 1, EnumColor.ENUM[0])
    i = 0
    for pixel in strat.pixels():
        assert (2, 1) == pixel[0:2]
        assert EnumColor.ENUM[11].rgb == pixel[2].rgb
        canvas.update(*pixel)
        i += 1
    assert i == 1


def test_status_outputs_percentage_complete(canvas_and_image):
    canvas, image = canvas_and_image(10, 10)
    status = strategies.Status(canvas, image, 10, 10)
    progress = status.run()
    assert progress == 0.0

    canvas.update(10, 10, EnumColor.ENUM[1])
    progress = status.run()
    assert progress == 5.0
