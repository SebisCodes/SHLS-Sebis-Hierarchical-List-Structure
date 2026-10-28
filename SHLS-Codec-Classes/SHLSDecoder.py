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

class SHLSDecoder:
    """
    SHLSDecoder is a utility class for decoding SHLS-formatted strings into structured data.

    A section starts with its name (no indentation) and a key block: one key per line,
    indented; the keys of a nested list one level deeper, below the key that holds the list.
    The records follow the key block after a blank line, or later under the section name
    repeated. A record has one line per key, in the order of the keys; a nested key's line
    is followed by the records of its list, one level deeper.

    How the decoder reads:
      - Blank lines (also lines with only spaces) separate the key block from the records;
        everywhere else they are skipped.
      - Records are counted by the number of keys. A last record with fewer values keeps
        the values it has.
      - A nested key without deeper lines below it holds an empty list.
      - Every data block of a section is kept, in the order of the text.
      - A section with a key block and no records is an empty list.
      - Lines indented deeper than the record they stand in are ignored.
    """

    def __init__(self):
        """
        Initializes the SHLSDecoder with default indentation settings.
        """
        self.__indentation = ' '  # One space is one step of indentation

    def decode(self, shls_string):
        """
        Decodes an SHLS-formatted string into a structured dictionary.

        Args:
            shls_string (str): The SHLS-formatted string to decode.

        Returns:
            dict: Each section name with the list of its records (dictionaries of strings,
            nested lists as lists of dictionaries).
        """
        self.__lines = shls_string.strip().splitlines()
        self.__pos = 0  # The next line to read
        data = {}
        templates = {}  # The key block of each section
        top_level_key = ""

        while self.__pos < len(self.__lines):
            line = self.__lines[self.__pos]
            self.__pos += 1
            value = line.strip()
            if value == "":
                continue
            if self.__get_level(line) == 0:
                top_level_key = value
            if top_level_key == "":
                continue  # Indented lines before the first section

            next_level, _ = self.__peek()
            if not next_level:
                continue  # The end of the text or the next section
            if top_level_key not in templates:
                templates[top_level_key] = self.__get_template(next_level, block=True)
                data.setdefault(top_level_key, [])
                next_level, _ = self.__peek()
                if not next_level:
                    continue  # Only the key block: its records come later
            data.setdefault(top_level_key, []).extend(self.__get_data(templates[top_level_key], next_level))
        return data

    def __get_level(self, line):
        """
        Returns the indentation of a line: the number of spaces before its content.
        """
        return len(line) - len(line.lstrip(self.__indentation))

    def __peek(self):
        """
        Looks at the next line with content without reading it; blank lines are passed over.

        Returns:
            tuple: (its indentation level, its index), or (None, None) at the end of the text.
        """
        i = self.__pos
        while i < len(self.__lines) and self.__lines[i].strip() == "":
            i += 1
        if i == len(self.__lines):
            return None, None
        return self.__get_level(self.__lines[i]), i

    def __get_template(self, base_level, block=False):
        """
        Reads a key block at base_level; deeper lines are the keys of a nested list and
        belong to the key above them.

        Args:
            base_level (int): The indentation of the keys.
            block (bool): True for the key block of a section, which ends at a blank line
                followed by a line at its own level (the records follow).

        Returns:
            list: [key, nested keys or None] for each key, in their order.
        """
        keys = []
        while True:
            level, i = self.__peek()
            if level is None or level < base_level:
                break  # The end of the text or a line further out
            if block and level == base_level and i > self.__pos and keys:
                break  # The blank line between the key block and the records
            if level > base_level:
                sub = self.__get_template(level)
                if keys:
                    keys[-1][1] = sub
                else:
                    keys.append(["", sub])
                continue
            self.__pos = i + 1
            keys.append([self.__lines[i].strip(), None])
        return keys

    def __get_data(self, template, base_level):
        """
        Reads records at base_level: one line per key in the order of the template;
        a nested key's line is followed by the records of its list, one level deeper.

        Args:
            template (list): The keys, as returned by __get_template.
            base_level (int): The indentation of the values.

        Returns:
            list: A list of dictionaries containing the extracted data.
        """
        data = []
        record = {}
        counter = 0
        while template:
            level, i = self.__peek()
            if level is None or level < base_level:
                break  # The end of the text or a line further out
            self.__pos = i + 1
            if level > base_level:
                continue  # A line deeper than the records, not below a nested key
            key, sub = template[counter]
            if sub is None:
                record[key] = self.__lines[i].strip()
            else:
                next_level, _ = self.__peek()
                record[key] = self.__get_data(sub, next_level) if next_level is not None and next_level > base_level else []
            counter += 1
            if counter == len(template):
                data.append(record)
                record = {}
                counter = 0
        if record:
            data.append(record)  # A last record with fewer values than keys
        return data
