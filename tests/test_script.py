import pytest
from src.cli import main
import pandas as pd
from unittest.mock import patch


@pytest.fixture
def mock_data():
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Country": ["USA", "UK", "Canada"],
        "Industry": ["Tech", "Finance", "Tech"],
        "Net Worth (in billions)": [100, 200, 150],
        "Company": ["CompanyA", "CompanyB", "CompanyC"],
    }
    return pd.DataFrame(data)


# Notice the updated patch path to correctly patch `read_data` where it's used in `cli.py`
@patch("src.cli.read_data")
@patch("src.cli.get_descriptive_statistics")
@patch("src.cli.get_industry_avg_net_worth")
def test_main(mock_get_industry_avg, mock_get_stats, mock_read_data, mock_data, capsys):
    # Mock the read_data function to return the sample dataframe
    mock_read_data.return_value = mock_data

    # Mock the get_descriptive_statistics function
    mock_get_stats.return_value = mock_data.describe()

    # Mock the get_industry_avg_net_worth function
    mock_get_industry_avg.return_value = mock_data.groupby("Industry")[
        "Net Worth (in billions)"
    ].mean()

    # Run the main function
    main()

    # Capture the output
    captured = capsys.readouterr()

    # Check that the output contains the expected data
    assert "Sample Data" in captured.out
    assert "Descriptive statistics" in captured.out
    assert "Average Net Worth by Industry" in captured.out

    # Ensure specific values from the mock data are printed
    assert "Alice" in captured.out
    assert "Tech" in captured.out
    assert "Finance" in captured.out
    assert "150.0" in captured.out  # Verify specific value

    # Ensure functions were called the correct number of times
    mock_read_data.assert_called_once()
    mock_get_stats.assert_called_once()
    mock_get_industry_avg.assert_called_once()


# Test when the dataset file is missing
@patch("src.cli.read_data", side_effect=FileNotFoundError)
def test_main_file_not_found(mock_read_data, capsys):
    # Run the main function and capture the return value
    result = main()

    # Capture the output
    captured = capsys.readouterr()

    # Check that the error message is printed
    assert "Error: File not found" in captured.out

    # Ensure that read_data was called once and raised the FileNotFoundError
    mock_read_data.assert_called_once()

    # Check that the function returns None (implicit return on early exit)
    assert result is None  # This checks if the return statement is hit
