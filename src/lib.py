import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def validate_dataframe(df: pd.DataFrame, required_columns: list):
    """
    Validates the given DataFrame for the following:
    - Checks if the DataFrame is empty.
    - Ensures required columns are present in the DataFrame.

    Args:
    - df (pd.DataFrame): The dataset as a DataFrame.
    - required_columns (list): List of required columns to check.

    Raises:
    - ValueError: If the DataFrame is empty.
    - KeyError: If any required column is missing.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing columns: {', '.join(missing_columns)}")


def read_data(filepath: str) -> pd.DataFrame:
    """
    Reads the dataset from the given file path and returns a pandas DataFrame.

    Args:
    - filepath (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: The dataset.
    """
    return pd.read_csv(filepath)


def get_descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the descriptive statistics of the given dataset.

    Args:
    - df (pd.DataFrame): The dataset as a DataFrame.

    Returns:
    - pd.DataFrame: Descriptive statistics of the dataset.

    Raises:
    - KeyError: If the 'Net Worth (in billions)' column is missing.
    - ValueError: If the DataFrame is empty.
    """
    validate_dataframe(df, ["Net Worth (in billions)"])
    return df.describe()


def get_industry_avg_net_worth(df: pd.DataFrame) -> pd.Series:
    """
    Groups the data by Industry and calculates the average net worth.

    Args:
    - df (pd.DataFrame): The dataset as a DataFrame.

    Returns:
    - pd.Series: A series with the average net worth for each industry.
    """
    validate_dataframe(df, ["Industry", "Net Worth (in billions)"])
    return df.groupby("Industry")["Net Worth (in billions)"].mean()


def calculate_skewness_kurtosis(df: pd.DataFrame) -> tuple:
    """
    Calculates the skewness and kurtosis of the net worth distribution.

    Args:
    - df (pd.DataFrame): The dataset as a DataFrame.

    Returns:
    - tuple: A tuple containing the skewness and kurtosis values.
    """
    validate_dataframe(df, ["Net Worth (in billions)"])
    skewness = df["Net Worth (in billions)"].skew()
    kurtosis = df["Net Worth (in billions)"].kurtosis()
    return skewness, kurtosis


def plot_industry_avg_net_worth(industry_avg: pd.Series):
    """
    Plots the average net worth by industry using a bar plot.

    Args:
    - industry_avg (pd.Series): A series with the average net worth for each industry.
    """
    if industry_avg.empty:
        raise ValueError("No data to plot for average net worth.")

    plt.figure(figsize=(10, 6))
    sns.barplot(x=industry_avg.index, y=industry_avg.values)
    plt.title("Average Net Worth by Industry")
    plt.xticks(rotation=90)
    plt.ylabel("Net Worth (in billions)")
    plt.show()


def plot_net_worth_distribution_by_industry(df: pd.DataFrame):
    """
    Plots a boxplot showing the distribution of net worth by industry.

    Args:
    - df (pd.DataFrame): The dataset as a DataFrame.
    """
    validate_dataframe(df, ["Industry", "Net Worth (in billions)"])

    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Industry", y="Net Worth (in billions)", data=df)
    plt.title("Net Worth Distribution by Industry")
    plt.xticks(rotation=90)
    plt.ylabel("Net Worth (in billions)")
    plt.show()
