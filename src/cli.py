from src.lib import read_data, get_descriptive_statistics, get_industry_avg_net_worth


def main():
    dataset_path = "Top_1000_wealthiest_people.csv"

    try:
        data = read_data(dataset_path)
    except FileNotFoundError:
        print(f"Error: File not found - {dataset_path}")
        return

    # Display a sample of the data
    print("Sample Data:\n", data.head())

    # Descriptive statistics
    print("\nDescriptive statistics:")
    print(get_descriptive_statistics(data))

    # Group data by industry and show average net worth
    industry_stats = get_industry_avg_net_worth(data)
    print("\nAverage Net Worth by Industry:")
    print(industry_stats)


# if __name__ == "__main__":
#     main()
