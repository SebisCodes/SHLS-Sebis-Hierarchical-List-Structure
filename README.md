# SHLS (Sebis Hierarchical List Structure)

Sebis Hierarchical List Structure (SHLS), developed by Sebastian Grünwald, is a text-based format optimized for token-efficient, structured data representation. All values are strings by default. Any conversion to other data types must be performed by the interpreter or consumer.

---

## Table of Contents

- [Introduction](#introduction)
- [Rules for Formatting SHLS](#rules-for-formatting-shls)
  - [1. Indexing at the Beginning](#1-indexing-at-the-beginning)
  - [2. Named Keys for Nested Arrays](#2-named-keys-for-nested-arrays)
  - [3. Exactly One Blank Line after the Key List](#3-exactly-one-blank-line-after-the-key-list)
- [Examples](#examples)
- [Benefits](#benefits)
- [License](#license)

---

## Introduction

SHLS uses indentation to encode hierarchy and avoids redundant symbols such as quotes, brackets, or colons, which makes it token-efficient. Values are strings only; if other types are needed (for example, integers or booleans), conversion is the interpreter’s responsibility.

---

## Rules for Formatting SHLS

### 1. Indexing at the Beginning
- Each SHLS section starts with an index line that declares the structure.
-The index contains a key block listing all keys used in the section and serves as a blueprint for the data that follows.
-If data follows immediately, separate the key block from the data with exactly one blank line.
-You may also predefine multiple structures and provide their data later by reusing the same index line.

### 2. Named Keys for Nested Arrays
- Every nested array must have a named key, especially when multiple arrays appear consecutively.
-In the examples, PH denotes a placeholder to keep the hierarchy unambiguous. You may replace it with - or any other value.

### 3. Exactly One Blank Line after the Key List
- After the key block, insert exactly one blank line before the data if the data for the same section follows immediately.
-Additional blank lines are unnecessary. Indentation alone defines the hierarchy.
-You can separate definitions from data by repeating the section’s index line later.

---

## Examples

Below is an example of a SHLS data structure with values interpreted as strings. Converting values to other data types (e.g., integers or booleans) must be done by the user.

Example with data immediately following the definitions of **Product** and **Company**:

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

Example with predefined structures first and data below:

```plaintext
Product
 Name
 Category
 Price
 InStock
 Released

Company
 Name
 Location
  Country
  City
 Founded
 Employees

Product
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

In these examples, every value is stored as a string. Downstream consumers must perform any type conversions as needed (for example, true to a boolean, 2023-09-01 to a date, or 599.99 to a float). Multiline fields are not supported. Use workarounds if needed (for example, escape sequences or external references).

## Benefits

- Token-efficient and compact: no quotes, brackets, colons or redundant keys.
- Readable hierarchy: indentation clearly separates elements.
- Ideal for local AI models.


## License

SHLS was developed by Sebastian Grünwald at ZHAW. It is free for personal and commercial use. Please reference my GitHub repository when you use it.