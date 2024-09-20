import csv
from typing import List, Dict, Any


class CSVMixin:
    def __init__(self, file_path: str) -> None:
        """
        Initializes the CSVMixin for working with the specified CSV file.

        :param file_path: Path to the CSV file
        """
        self.file_path = file_path

    def read_csv(self, delimiter: str = ',') -> List[str]:
        """
        Reads data from the CSV file and returns a list of dictionaries, where keys are column headers.

        :param delimiter: The character used as the column delimiter
        :return: A list of dictionaries containing the data from the CSV file
        """
        try:
            data = list()
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=delimiter)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            print(f"Failed to read CSV: {e}")
            raise e

    def write_csv(self, headers: List[str], rows: List[Dict[str, Any]], delimiter: str = ',') -> None:
        """
        Writes data to the CSV file, creating a new file or overwriting an existing one.

        :param headers: A list of column headers
        :param rows: A list of dictionaries, where keys are column headers
        :param delimiter: The character used as the column delimiter
        """
        try:
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(rows)
        except Exception as e:
            print(f"Failed to write CSV: {e}")
            raise e

    def append_to_csv(self, row: Dict[str, Any], delimiter: str = ',') -> None:
        """
        Appends a single row to the CSV file. The file must already contain headers.

        :param row: A dictionary with data to append
        :param delimiter: The character used as the column delimiter
        """
        try:
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=row.keys(), delimiter=delimiter)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(row)
        except Exception as e:
            print(f"Failed to append to CSV: {e}")
            raise e
