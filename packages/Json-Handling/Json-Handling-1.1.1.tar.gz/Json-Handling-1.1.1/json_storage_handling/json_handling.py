import json
from pathlib import Path


class JsonStorage:
    """
    This class handles Json Data.

    Arguments:
        project_root: the project root; this to make the class as generic as possible.
        json_directory_under_root: the location of the Json folder the file is in under the project root.
    """
    def __init__(self, project_root, json_directory_under_root):
        self.project_root = str(project_root)
        self.folder_location_specified = str(json_directory_under_root)
        self.json_directory = (self.project_root + self.folder_location_specified)

    def read_json_file(self, file_name):
        """
        This function returns the data from a json file.

        Arguments:
            file_name: the name of the file to read.
        """
        file_path = Path(self.json_directory, file_name)

        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            print("File was not found!")
            print(f"File name: {file_name}")
            print(f"File file_path: {file_path}")
        except TypeError as _error:
            print(f"Type Error: {_error}")
            print(f"File name: {file_name}")

    def write_json_file(self, data, file_name):
        """
        This function writes to a json file.

        Arguments:
            file_name: the name of the file to write to.
            data: the data to write.
        """
        file_path = Path(self.json_directory, file_name)

        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            print("File was not found!")
            print(f"File name: {file_name}")
            print(f"File file_path: {file_path}")
        except TypeError as _error:
            print(f"Type Error: {_error}")
            print(f"File name: {file_name}")

    def read_json_file_table(self, file_name, table: str):
        """
        This function returns the table data from a json file.

        Arguments:
            file_name: the name of the file to read.
            table: the name of the table to read.
        """
        try:
            return self.read_json_file(file_name)[table]
        except KeyError:
            print("Table wasn't found!")
        except TypeError as _error:
            print(f"Type Error: {_error}")
            print(f"File name: {file_name}, Table name: {table}")

    def write_json_file_table(self, file_name, table: str, input_data):
        """
        This function writes to table data from a json file.

        Arguments:
            file_name: the name of the file to write to.
            table: the name of the table to write to.
            input_data: the data to insert into the table.
        """
        data = {table: input_data}
        try:
            self.write_json_file(data, file_name)
        except KeyError:
            print("Table wasn't found!")
        except TypeError as _error:
            print(f"Type Error: {_error}")
            print(f"File name: {file_name}, Table name: {table}")
