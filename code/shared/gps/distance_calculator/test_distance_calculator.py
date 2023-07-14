import pytest
from distance_calculator import calc_distance_km


def test_calc_distance_km_should_return_correct_distance():
    holon_mall = (32.01278924606207, 34.77908810682126)
    hit = (32.01487634797979, 34.77458326803195)

    distance = calc_distance_km(holon_mall, hit)

    assert distance == pytest.approx(0.48, 0.01)


def test_calc_distance_km_should_return_zero_when_same_coordinates():
    c1 = (32.01278924606207, 34.77908810682126)
    c2 = (32.01278924606207, 34.77908810682126)

    distance = calc_distance_km(c1, c2)

    assert distance == pytest.approx(0.0, 0.01)


@pytest.mark.parametrize(
    "c1, c2",
    [
        (32.01278924606207, (32.01278924606207, 34.77908810682126)),
        ((32.01278924606207, 34.77908810682126), 32.01278924606207),
    ],
)
def test_calc_distance_km_should_fail_when_input_is_not_tuple(c1, c2):
    with pytest.raises(TypeError):
        distance = calc_distance_km(c1, c2)


def test_calc_distance_km_should_fail_when_input_is_not_tuple_of_floats():
    c1 = (32.01278924606207, 34.77908810682126)
    c2 = (32.01278924606207, "34.77908810682126")

    with pytest.raises(TypeError):
        distance = calc_distance_km(c1, c2)  # type: ignore


def test_calc_distance_km_should_fail_when_input_is_not_tuple_of_length_2():
    c1 = (32.01278924606207, 34.77908810682126)
    c2 = (32.01278924606207, 34.77908810682126, 34.77908810682126)

    with pytest.raises(TypeError):
        distance = calc_distance_km(c1, c2)  # type: ignore
