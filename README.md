# SHLS (Sebis Hierarchical List Structure)

**Sebis Hierarchical List Structure (SHLS)**, developed by *Sebastian Grünwald*, is a format optimized for token-efficient, structured data representation. All values in SHLS are interpreted exclusively as strings. Reinterpretation of these values to other data types must be handled by an interpreter.

### Table of Contents

- [Introduction](#introduction)
- [Rules for Formatting SHLS](#rules-for-formatting-shls)
  - [1. Indexing at the Beginning](#1-indexing-at-the-beginning)
  - [2. Key Requirement for Subarrays](#2-key-requirement-for-subarrays)
  - [3. Single Space after the Key List](#3-single-space-after-the-key-list)
- [Example](#example)
- [Benefits](#benefits)
- [License](#license)

---

## Introduction

SHLS is designed for efficient, compact data representation by using indentation for hierarchy without redundant symbols like quotation marks, brackets, or colons. It’s particularly effective in constrained environments where minimizing data size and network load is important. All values in SHLS are treated as strings by default. If values need to be converted to other types (e.g., integers, booleans), this should be done by an interpreter.

## Rules for Formatting SHLS

### 1. Indexing at the Beginning
   - Each SHLS file must start with an **index**. This index lists all the keys used within the file and outlines the document structure.
   - The index defines the hierarchy and serves as a blueprint for the data structure that follows, making it easier for readers and parsers to understand the format.

### 2. Key Requirement for Subarrays
   - Every subarray in SHLS must have a **named key**, as listed in the initial index. This is particularly crucial when multiple arrays appear consecutively.
   - The key for each subarray ensures clarity, helping to distinguish between different levels and groups of data, and prevents misinterpretation of relationships among elements. Note the PH (placeholder) in the example. Its only use is for a clear structure.

### 3. Single new line after the Key List
   - After the initial key list (index), a single blank line is required to separate the index from the actual data entries.
   - Additional blank spaces after the key list are unnecessary, as SHLS hierarchy is controlled solely by indentation (spaces) and counting of values. Extra lines do not impact the structure and are not required.

---

## Example

Below is an example of a SHLS data structure with values interpreted as strings. Converting values to other data types (e.g., integers or booleans) requires an interpreter:

```plaintext
Product
 Name
 Category
 Price
 InStock
 Released

 Smartphone A1
 Electronics
 599.99
 true
 2023-09-01

 Laptop B2
 Electronics
 1299.99
 false
 2022-05-15

 Table X5
 Furniture
 349.99
 true
 2021-11-12

Company
 Name
 Location
  Country
  City
 Founded
 Employees

 TechCorp
 PH
  USA
  San Francisco
  USA
  New York
 2010
 500

 FurniCo
 PH
  Germany
  Berlin
  Switzerland
  Zürich
 2015
 150
```

In this example, each value is stored as a string by default. An interpreter is required to convert data types as needed for processing (e.g., "true" to boolean, "2023-09-01" to a date, and "599.99" to a float).

## Benefits

- **Token-efficient and compact**: Saves space by eliminating redundant characters and reducing data volume.
- **Clarity through hierarchy**: Defined structure makes it readable and easy to parse, with clear separation between data elements.
- **Ideal for constrained environments**: SHLS is especially useful in settings with limited storage or bandwidth or high traffic expenses.

## License

SHLS is a project by Sebastian Grünwald. For questions, please contact me: sebiscodes@gmail.com
