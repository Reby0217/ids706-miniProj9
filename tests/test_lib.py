import pytest
import pandas as pd
from unittest.mock import patch
from src.lib import (
    read_data,
    get_descriptive_statistics,
    get_industry_avg_net_worth,
    calculate_skewness_kurtosis,
    plot_industry_avg_net_worth,
    plot_net_worth_distribution_by_industry,
    validate_dataframe,
)

# Sample test data
@pytest.fixture
def sample_data():
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Country": ["USA", "UK", "Canada"],
        "Industry": ["Tech", "Finance", "Tech"],
        "Net Worth (in billions)": [100, 200, 150],
        "Company": ["CompanyA", "CompanyB", "CompanyC"],
    }
    return pd.DataFrame(data)


# Test validate_dataframe for empty DataFrame
def test_validate_dataframe_empty():
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="The DataFrame is empty."):
        validate_dataframe(empty_df, ["Net Worth (in billions)"])


# Test validate_dataframe for missing columns
def test_validate_dataframe_missing_columns(sample_data):
    # We expect 'MissingColumn' to be the missing one, as 'Country' and 'Net Worth (in billions)' exist
    with pytest.raises(KeyError, match="Missing columns: MissingColumn"):
        validate_dataframe(
            sample_data, ["Net Worth (in billions)", "Country", "MissingColumn"]
        )


def test_get_descriptive_statistics(sample_data):
    # Test the descriptive statistics function
    stats = get_descriptive_statistics(sample_data)

    # Ensure that the columns and values are correct
    assert "Net Worth (in billions)" in stats.columns
    assert stats["Net Worth (in billions)"]["mean"] == 150
    assert stats["Net Worth (in billions)"]["std"] > 0  # Check for standard deviation
    assert stats.shape == (8, 1)


# Additional test to handle missing columns in get_descriptive_statistics
def test_get_descriptive_statistics_missing_column():
    data = pd.DataFrame(
        {"Name": ["Alice", "Bob", "Charlie"], "Country": ["USA", "UK", "Canada"]}
    )
    with pytest.raises(KeyError):
        get_descriptive_statistics(data)


def test_get_industry_avg_net_worth(sample_data):
    # Test the average net worth by industry function
    industry_avg = get_industry_avg_net_worth(sample_data)

    # Check the output for both Tech and Finance industries
    assert industry_avg["Tech"] == 125
    assert industry_avg["Finance"] == 200
    assert len(industry_avg) == 2  # Ensure only two industries are present


# Test for missing 'Industry' column in get_industry_avg_net_worth
def test_get_industry_avg_net_worth_missing_column():
    data = pd.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Net Worth (in billions)": [100, 200, 150],
        }
    )
    with pytest.raises(KeyError):
        get_industry_avg_net_worth(data)


def test_calculate_skewness_kurtosis(sample_data):
    # Test the skewness and kurtosis calculation function
    skewness, kurtosis = calculate_skewness_kurtosis(sample_data)

    # Ensure that skewness and kurtosis are both floats
    assert isinstance(skewness, float)
    assert isinstance(kurtosis, float)


# Test for missing 'Net Worth (in billions)' column in calculate_skewness_kurtosis
def test_calculate_skewness_kurtosis_missing_column():
    data = pd.DataFrame(
        {"Name": ["Alice", "Bob", "Charlie"], "Industry": ["Tech", "Finance", "Tech"]}
    )
    with pytest.raises(KeyError):
        calculate_skewness_kurtosis(data)


def test_read_data(tmp_path):
    # Test the read_data function by creating a temporary CSV file
    csv_file = tmp_path / "test_data.csv"
    sample_data = {
        "Name": ["Alice", "Bob"],
        "Country": ["USA", "UK"],
        "Industry": ["Tech", "Finance"],
        "Net Worth (in billions)": [100, 200],
        "Company": ["CompanyA", "CompanyB"],
    }
    df = pd.DataFrame(sample_data)
    df.to_csv(csv_file, index=False)

    # Read the data using the function
    read_df = read_data(csv_file)

    # Check that the data was read correctly
    assert not read_df.empty
    assert read_df.shape == (2, 5)
    assert "Name" in read_df.columns
    assert read_df["Net Worth (in billions)"].sum() == 300


def test_read_data_invalid_path():
    # Test that an invalid file path raises the proper error
    with pytest.raises(FileNotFoundError):
        read_data("invalid_path.csv")


# Test empty dataframe behavior
def test_get_descriptive_statistics_empty():
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError):
        get_descriptive_statistics(empty_df)


# Test plot_industry_avg_net_worth with empty data
def test_plot_industry_avg_net_worth_empty():
    industry_avg = pd.Series(dtype=float)
    with pytest.raises(ValueError, match="No data to plot for average net worth."):
        plot_industry_avg_net_worth(industry_avg)


# Test plot_industry_avg_net_worth by mocking plt.show
@patch("src.lib.plt.show")
def test_plot_industry_avg_net_worth(mock_show, sample_data):
    # Get industry average
    industry_avg = get_industry_avg_net_worth(sample_data)

    # Call the plot function
    plot_industry_avg_net_worth(industry_avg)

    # Assert plt.show() was called
    mock_show.assert_called_once()


# Test plot_net_worth_distribution_by_industry with empty DataFrame
def test_plot_net_worth_distribution_by_industry_empty():
    empty_df = pd.DataFrame(columns=["Industry", "Net Worth (in billions)"])
    with pytest.raises(ValueError):
        plot_net_worth_distribution_by_industry(empty_df)


# Test plot_net_worth_distribution_by_industry by mocking plt.show
@patch("src.lib.plt.show")
def test_plot_net_worth_distribution_by_industry(mock_show, sample_data):
    # Call the plot function
    plot_net_worth_distribution_by_industry(sample_data)

    # Assert plt.show() was called
    mock_show.assert_called_once()
