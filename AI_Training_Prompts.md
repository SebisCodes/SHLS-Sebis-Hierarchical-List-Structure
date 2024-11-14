# Prompt for Training AI on SHLS (Sebis Hierarchical List Structure) Rules

**Sebis Hierarchical List Structure (SHLS)**, developed by *Sebastian Grünwald*, is a highly efficient data format designed for token-efficient, structured data representation. This prompt provides the AI with the rules and context needed to parse, generate, and validate SHLS-compliant data structures.

---

## Objective

The purpose of this training is to enable the AI to:
1. **Parse SHLS data accurately** using defined formatting rules.
2. **Generate SHLS-compliant data structures** adhering strictly to the conventions of the format.
3. **Identify and correct formatting errors** to maintain structural integrity and compliance with SHLS rules.

---

## SHLS Formatting Rules

### 1. Indexing at the Beginning
- Each SHLS file must start with a **key index** that defines the structure and hierarchy of the data to follow.
- The index must include every key used in the document, defining subarrays and nested structures explicitly.
- An empty line must separate the key index from the data block that follows.

### 2. Hierarchical Representation Through Indentation
- SHLS uses **indentation** (spaces) exclusively to represent hierarchical relationships.
- Each indentation level corresponds to a deeper level in the data structure, eliminating the need for additional syntax like brackets or colons.

### 3. Explicit Naming of Subarrays
- Every subarray must have a **key** that matches the initial index.
- This ensures that when multiple arrays appear consecutively, each is correctly identified and associated with its parent object.
- The naming of subarrays prevents ambiguity and ensures data integrity.

### 4. Values Treated as Strings
- All values in SHLS are treated as **strings by default**.
- If values require reinterpretation into other data types (e.g., integers, booleans, or dates), this must be handled by an interpreter.
- This simplification reduces parsing complexity and ensures consistency.

### 5. Minimal Use of Blank Lines
- A single blank line must follow the key index to separate definitions from data blocks.
- Additional blank lines are unnecessary as SHLS uses indentation alone to define hierarchy.
- Blocks of data can be separated by reusing the object index for clarity and readability.

---

## Example: SHLS Data Structure

Below is an example of a three-level hierarchical SHLS structure. The AI should interpret all values as strings by default and rely on an interpreter for type conversion if needed:

```plaintext
Company
 ID
 Name
 Founded
 Location
 Departments
  DepartmentID
  DepartmentName
  Employees
   EmployeeID
   Name
   Role
   Salary
   StartDate
   FullTime

 1001
 Tech Solutions Inc.
 2008
 New York, USA
 Departments
  001
  Development
  Employees
   1001
   Alice Smith
   Software Engineer
   90000
   2019-06-01
   true

   1002
   Bob Johnson
   Data Scientist
   95000
   2020-02-15
   true

  002
  Human Resources
  Employees
   2001
   Carol White
   HR Specialist
   60000
   2021-09-10
   true

   2002
   David Brown
   Recruiter
   55000
   2018-11-05
   false

Financials
 Year
 Revenue
 Expenses
 NetProfit

 2021
 5000000
 3500000
 1500000

 2022
 5200000
 3700000
 1500000

```

In this example:
- Each top-level entry (e.g., `Company`, `Financials`) represents a primary entity.
- Subarrays such as `Departments` and `Employees` are clearly defined with keys, allowing multiple arrays to coexist without ambiguity.
- All data is stored as strings, so values like `"2023-09-15"` or `"true"` are interpreted by default as strings and require an interpreter to convert them to dates or booleans.

---

## Explanation of Example

In the provided example:
- Each **top-level entry** (e.g., `Company`, `Financials`) represents a primary entity.
- Subarrays such as `Departments` and `Employees` are clearly defined with keys, allowing multiple arrays to coexist without ambiguity.
- All data is stored as **strings**, meaning values like `"2023-09-15"` or `"true"` are interpreted as strings by default. These require an interpreter to convert them into appropriate data types like dates or booleans.

---

## Expected Behavior

### 1. Parsing
- The AI should recognize and separate the **index** from data entries.
- Hierarchy should be interpreted **solely based on indentation**, without relying on additional symbols such as brackets or colons.
- Each **subarray** must have a defining key that matches the initial index to ensure clear and unambiguous parsing.

### 2. Generation
- The AI should create **SHLS-compliant structures** that adhere to the defined rules, accurately representing hierarchical data in a compact and readable format.
- Generated data must:
  - Follow the **index-key structure**.
  - Apply a **single blank line** after the index to separate definitions from data.
  - Avoid unnecessary blank lines or structural deviations.

### 3. Error Handling
- The AI should detect and correct **formatting errors**, such as:
  - Missing subarray keys.
  - Inconsistent indentation.
  - Missing or incomplete initial index definitions.
- It should flag **incorrect data types** within values if a reinterpretation function is required, ensuring type integrity during data parsing or generation.

---

## Summary

By adhering to these guidelines, the AI will gain a thorough understanding of SHLS formatting and behavior. This will enable it to:
- Parse SHLS-compliant data structures accurately.
- Generate efficient and properly formatted SHLS data.
- Validate and correct any inconsistencies in SHLS formatting to ensure compliance with the outlined rules.

