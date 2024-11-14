# SHLS Utilities: Encoder and Decoder

This repository contains Python implementations of the **SHLS (Sebis Hierarchical List Structure)** Encoder and Decoder. These tools are designed to encode Python data structures into SHLS format and decode SHLS-formatted strings back into structured data.

---

## Table of Contents

- [Introduction](#introduction)
- [File Descriptions](#file-descriptions)
- [Usage Instructions](#usage-instructions)


---

## Introduction

SHLS is a hierarchical data format designed for compact and token-efficient data representation. These utilities provide easy-to-use methods for handling SHLS data in Python. The encoder converts Python dictionaries and lists into SHLS format, while the decoder parses SHLS strings into Python structures.

---

## File Descriptions

- **`SHLSEncoder.py`**: Contains the `SHLSEncoder` class for encoding Python data structures into SHLS format.
- **`SHLSDecoder.py`**: Contains the `SHLSDecoder` class for decoding SHLS-formatted strings into Python dictionaries or lists.
- **`EncodeExample.py`**: Demonstrates the usage of `SHLSEncoder` to encode a Python data structure into SHLS format.
- **`DecodeExample.py`**: Demonstrates the usage of `SHLSDecoder` to decode an SHLS-formatted string into structured Python data.
- **`DecodeExample2.py`**: An additional example of decoding with a different SHLS input string.

---

## Usage Instructions

### SHLS Encoding

1. Import the `SHLSEncoder` or `SHLSDecoder` class from `SHLSEncoder.py` or `SHLSDecoder.py`.
2. Initialize an object and pass your data structure to the `encode` or the SHLS-string into the `decode` method.
3. The `encode` method returns an SHLS-formatted string while the `decode`-method returns a list.
