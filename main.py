import os
import sys
import shutil
import pandas as pd
from typing import List

from src.main.data_analysis import DataAnalysis
from src.utils.city_mention import CityMentionAnalyzer


def validate_file(file_path: str, keywords: List[str]) -> bool:
    """
    Validate if file at given path contains the required keywords in its name.

    Args:
        file_path (str): The path to the file.
        keywords (List[str]): The list of keywords to be found in the file name.

    Returns:
        bool: True if all keywords are found in the file name, False otherwise.
    """
    file_name = os.path.basename(file_path)
    return all(keyword in file_name for keyword in keywords)


def get_year_uf_from_filename(file_path: str) -> (str, str):
    """
    Extract the year and federal unit from the file name.

    Args:
        file_path (str): The path to the file.

    Returns:
        tuple: The extracted year and federal unit.
    """
    file_name = os.path.basename(file_path)
    year, uf = file_name.split("_")[-2:]
    uf = uf.split(".")[0]  # remove file extension
    return year, uf


def move_file_to_new_directory(file_path: str, year: str, uf: str) -> str:
    """
    Move the file to the new directory structure (data/year/uf).

    Args:
        file_path (str): The path to the file.
        year (str): The year extracted from the file name.
        uf (str): The federal unit extracted from the file name.

    Returns:
        str: The new path to the moved file.
    """
    new_directory = f"./data/{year}/{uf}/"
    os.makedirs(new_directory, exist_ok=True)

    # Obtain the file name from the original path
    file_name = os.path.basename(file_path)

    # Create a new file path
    new_file_path = os.path.join(new_directory, file_name)

    # Move the file to the new path
    shutil.move(file_path, new_file_path)

    return new_file_path


def main():
    """
    The main function to handle the file operations.
    """
    try:
        file_path = sys.argv[1]
    except IndexError:
        print("Please provide a file path as a command-line argument.")
        sys.exit(1)

    if not os.path.isfile(file_path):
        print(f"No such file: '{file_path}'")
        sys.exit(1)

    if not validate_file(file_path, ["votacao", "municipio"]):
        print("The provided file does not meet the requirements.")
        sys.exit(1)

    year, uf = get_year_uf_from_filename(file_path)
    new_file_path = move_file_to_new_directory(file_path, year, uf)
    print(f"File has been successfully moved to ./data/{year}/{uf}/")

    tse = DataAnalysis(new_file_path)
    tse.run_analysis()

    city_names = tse.city_names

    city_mention_path = f"./data/{year}/{uf}/city_mentions_twitter_data.csv"
    while not os.path.isfile(city_mention_path):
        print(
            f"Please acquire the Twitter data for {year} {uf} and place it in {city_mention_path}."
        )
        input("Press ENTER once you've moved the file.")

    tweets_path = f"./data/{year}/{uf}/tweets.csv"
    if os.path.isfile(tweets_path):
        CityMentionAnalyzer(tweets_path, city_names).identify_city_mentions()

    twitter_data = DataAnalysis(city_mention_path, data_source="twitter").run_analysis()


if __name__ == "__main__":
    main()
