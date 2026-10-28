# SHLS Utilities: Encoder and Decoder

This repository contains Python implementations of the **SHLS (Sebis Hierarchical List Structure)** Encoder and Decoder. These tools are designed to encode Python data structures into SHLS format and decode SHLS-formatted strings back into structured data.

---

## Table of Contents

- [Introduction](#introduction)
- [File Descriptions](#file-descriptions)
- [Usage Instructions](#usage-instructions)
- [Reading and Writing in Detail](#reading-and-writing-in-detail)
- [Tests](#tests)

---

## Introduction

SHLS is a hierarchical data format designed for compact and token-efficient data representation. These utilities provide easy-to-use methods for handling SHLS data in Python. The encoder converts Python dictionaries and lists into SHLS format, while the decoder parses SHLS strings into Python structures.

---

## File Descriptions

- **`SHLSEncoder.py`**: Contains the `SHLSEncoder` class for encoding Python data structures into SHLS format.
- **`SHLSDecoder.py`**: Contains the `SHLSDecoder` class for decoding SHLS-formatted strings into Python dictionaries or lists.

---

## Usage Instructions

### SHLS Encoding

1. Import the `SHLSEncoder` or `SHLSDecoder` class from `SHLSEncoder.py` or `SHLSDecoder.py`.
2. Initialize an object and pass your data structure to the `encode` or the SHLS-string into the `decode` method.
3. The `encode` method returns an SHLS-formatted string while the `decode`-method returns a list.

---

## Reading and Writing in Detail

`SHLSDecoder`:

- Blank lines, also lines with only spaces, separate the key block from the records; everywhere else they are skipped.
- Records are counted by the number of keys. A last record with fewer values keeps the values it has.
- A nested key without deeper lines below it holds an empty list, also at the end of the text.
- Every data block of a section is kept: records under a repeated section line are added to the ones before.
- A section with a key block and no records is an empty list.
- Keys may have any name, numbers such as `0` or `1` included.
- Lines indented deeper than the record they stand in are ignored.

`SHLSEncoder`:

- The data passed in stays unchanged; the encoder works on a copy.
- A value of the top-level dictionary that is not a list becomes a list with this value.
- A dictionary inside a record becomes a list with this one record, so the decoder can read it back.
- A plain value in a list (not a dictionary) becomes a record with the one key `Value`.
- The keys of a nested list come from its records in all records; a list that is empty everywhere gets the key `Value`.

Read back with `SHLSDecoder`, the text gives this shape with every value as a string.

---

## Tests

```
python3 -m unittest discover tests
```
