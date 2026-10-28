"""
This file was created by Sebastian Gruenwald on 14.11.2024, Neuhausen am Rheinfall.

Contact:
  - Email: sebiscodes@gmail.com

Social Links:
  - GitHub: https://github.com/sebiscodes
  - Instagram: https://www.instagram.com/sebisprojects/
  - YouTube: https://www.youtube.com/@sebisprojects
  - Linktree: https://linktr.ee/sebisprojects
"""

class SHLSEncoder:
    """
    SHLSEncoder encodes Python dictionaries or lists into SHLS (Sebis Hierarchical List Structure) format.

    The SHLS format uses indentation to represent hierarchy, ensuring compact and token-efficient data serialization.
    The text holds lists of records, so the data is first brought into that shape (on a copy; the data
    passed in stays unchanged):
      - a value of the top-level dictionary that is not a list becomes a list with this value;
      - a dictionary inside a record becomes a list with this one record;
      - a plain value in a list (not a dictionary) becomes a record with the one key "Value".
    SHLSDecoder reads the text back as this shape, with every value as a string.

    Attributes:
        indentation (str): Defines the indentation for each hierarchical level (default is a single space).
    """
    def __init__(self):
        """
        Initializes the SHLSEncoder with default indentation settings.
        """
        self.indentation = " "  # Single space for indentation

    def encode(self, data):
        """
        Encodes a Python dictionary or list into SHLS format.

        - Creates a header section that defines the data structure (keys).
        - Serializes values into the SHLS format using indentation to represent hierarchy.

        Args:
            data (dict or list): The data to encode.

        Returns:
            str: The encoded SHLS string.
        """
        if isinstance(data, dict):
            data = {key: self.__records(value if isinstance(value, list) else [value]) for key, value in data.items()}
        elif isinstance(data, list):
            data = self.__records(data)

        # Generate the SHLS header and values sections
        header = self.__generate_header(data)
        values = self.__encode_values(data)

        # Combine the header and values with a blank line separator
        return f"{header}\n\n{values}"

    def __records(self, items):
        """
        A copy of a list as a list of records (see the class description).
        """
        return [self.__record(item if isinstance(item, dict) else {"Value": item}) for item in items]

    def __record(self, item):
        """
        A copy of a record: lists become lists of records, a dictionary a list with one record.
        """
        record = {}
        for key, value in item.items():
            if isinstance(value, list):
                record[key] = self.__records(value)
            elif isinstance(value, dict):
                record[key] = self.__records([value])
            else:
                record[key] = value
        return record

    def __generate_header(self, data, level=0):
        """
        Recursively generates the SHLS header section, defining the data structure.

        - For the top-level dictionary, lists its keys with the keys of their records below them.
        - For a list of records, uses the first record as the schema for keys; the keys of a nested
          list come from the records of that list in all records, and a list that is empty
          everywhere gets the key "Value".

        Args:
            data (dict or list): The data structure to analyze.
            level (int): The current indentation level.

        Returns:
            str: The header section of the SHLS string.
        """
        lines = []
        if isinstance(data, dict):
            for key, value in data.items():
                lines.append(f"{self.indentation * level}{key}")
                lines.append(self.__generate_header(value, level + 1))
        elif isinstance(data, list):
            schema = next((record for record in data if record), None)
            if schema is None:
                lines.append(f"{self.indentation * level}Value")
            else:
                for key, value in schema.items():
                    lines.append(f"{self.indentation * level}{key}")
                    if isinstance(value, list):
                        nested = [item for record in data if isinstance(record.get(key), list) for item in record[key]]
                        lines.append(self.__generate_header(nested, level + 1))
        return "\n".join(lines)

    def __encode_values(self, data, level=0):
        """
        Recursively encodes the data values into the SHLS format.

        - Processes the top-level dictionary by writing each key with its records below it.
        - Processes lists by writing each record's values; a nested list is its key followed by
          its records one level deeper (nothing for an empty list).

        Args:
            data (dict or list): The data structure to encode.
            level (int): The current indentation level.

        Returns:
            str: The values section of the SHLS string.
        """
        lines = []
        if isinstance(data, dict):
            for key, value in data.items():
                lines.append(f"{key}")
                if value:
                    lines.append(self.__encode_values(value, level + 1))
        elif isinstance(data, list):
            for record in data:
                for key, value in record.items():
                    if isinstance(value, list):
                        lines.append(f"{self.indentation * level}{key}")
                        if value:
                            lines.append(self.__encode_values(value, level + 1))
                    else:
                        lines.append(f"{self.indentation * level}{value}")
        return "\n".join(lines)
