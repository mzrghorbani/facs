"""Tests for the utils module."""

from unittest import mock

import pytest

from facs.base import utils


def test_probability_general():
    """Test the probability function."""

    assert utils.probability(0) is False
    assert utils.probability(1) is True
    assert utils.probability(0.5) in [True, False]


@mock.patch("numpy.random.random")
def test_probability_with_mock(mock_random):
    """Test the probability function with a mock."""

    mock_random.return_value = 0.5
    assert utils.probability(0.6) is True
    assert utils.probability(0.4) is False


def test_probability_raises_error():
    """Test the probability function raises an error."""

    with pytest.raises(ValueError):
        utils.probability(-0.1)
    with pytest.raises(ValueError):
        utils.probability(1.1)


@mock.patch("numpy.random.randint")
def test_get_random_int_valid(mock_randint):
    """Test the get_random_int function."""

    mock_randint.return_value = 3
    high = 10
    result = utils.get_random_int(high)
    mock_randint.assert_called_once_with(0, high)
    assert result == 3


def test_get_random_int_negative_high():
    """Test the get_random_int function raises an error."""

    with pytest.raises(ValueError):
        utils.get_random_int(-1)


@mock.patch("os.path.exists", return_value=False)
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_open_new_file(mock_open, mock_exists):
    """Test the open function when the file does not exist."""

    out_files = utils.OutputFiles()
    file_name = "test_file.txt"

    file_handle = out_files.open(file_name)

    mock_exists.assert_called_once_with(file_name)
    mock_open.assert_called_once_with(file_name, "a", encoding="utf-8")
    assert file_handle == mock_open.return_value
    assert file_name in out_files.files


@mock.patch("os.remove")
@mock.patch("os.path.exists", return_value=True)
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_open_existing_file(mock_open, mock_exists, mock_remove):
    """Test the open function when the file exists."""

    out_files = utils.OutputFiles()
    file_name = "test_file.txt"

    file_handle = out_files.open(file_name)

    mock_exists.assert_called_once_with(file_name)
    mock_remove.assert_called_once_with(file_name)
    mock_open.assert_called_once_with(file_name, "a", encoding="utf-8")
    assert file_handle == mock_open.return_value
    assert file_name in out_files.files


@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_close_files_on_delete(mock_open):
    """Test the __del__ function."""

    out_files = utils.OutputFiles()
    file_name = "test_file.txt"
    out_files.open(file_name)

    del out_files

    mock_open.return_value.close.assert_called_once()


@mock.patch("facs.base.utils.out_files.open", new_callable=mock.mock_open)
@mock.patch("builtins.print")
def test_log_to_file(mock_print, mocked_file):
    """Test the log_to_file function."""

    category = "test_category"
    rank = 1
    data = [1, 2.5, "test"]
    expected_output = "1,2.5,test"

    utils.log_to_file(category, rank, data)

    mocked_file.assert_called_once_with(f"./covid_out_{category}_{rank}.csv")
    mock_print.assert_called_once_with(expected_output, file=mocked_file(), flush=True)


@mock.patch("builtins.open", new_callable=mock.mock_open)
@mock.patch("builtins.print")
def test_log_infection(mock_print, mock_open):
    """Test the log_infection function."""

    utils.log_infection(1, 2, 3, 4, 5, 6)

    mock_open.assert_called_once_with(
        "./covid_out_infections_5.csv", "a", encoding="utf-8"
    )
    mock_print.assert_called_once_with(
        "1,2,3,4,5,6", file=mock_open.return_value, flush=True
    )


@mock.patch("builtins.open", new_callable=mock.mock_open)
@mock.patch("builtins.print")
def test_log_hospitalisation(mock_print, mock_open):
    """Test the log_hospitalisation function."""

    utils.log_hospitalisation(1, 2, 3, 4, 5)

    mock_open.assert_called_once_with(
        "./covid_out_hospitalisations_5.csv", "a", encoding="utf-8"
    )
    mock_print.assert_called_once_with(
        "1,2,3,4", file=mock_open.return_value, flush=True
    )


@mock.patch("builtins.open", new_callable=mock.mock_open)
@mock.patch("builtins.print")
def test_log_death(mock_print, mock_open):
    """Test the log_death function."""

    utils.log_death(1, 2, 3, 4, 5)

    mock_open.assert_called_once_with("./covid_out_deaths_5.csv", "a", encoding="utf-8")
    mock_print.assert_called_once_with(
        "1,2,3,4", file=mock_open.return_value, flush=True
    )


@mock.patch("builtins.open", new_callable=mock.mock_open)
@mock.patch("builtins.print")
def test_log_recovery(mock_print, mock_open):
    """Test the log_death function."""

    utils.log_recovery(1, 2, 3, 4, 5)

    mock_open.assert_called_once_with(
        "./covid_out_recoveries_5.csv", "a", encoding="utf-8"
    )
    mock_print.assert_called_once_with(
        "1,2,3,4", file=mock_open.return_value, flush=True
    )
