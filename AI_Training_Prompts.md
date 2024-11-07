
# Prompt for Training AI on SHLS (Sebis Hierarchical List Structure) Rules

**SHLS (Sebis Hierarchical List Structure)** is a highly efficient data format developed for representing hierarchical data in a compact, readable, and token-efficient way. It’s particularly useful in bandwidth- or storage-constrained environments due to its minimalistic syntax. This prompt will guide the AI to understand the core rules, syntax, and structure of SHLS and apply it to interpret or generate data accurately.

### Objective

The goal is to enable the AI to:
1. **Parse SHLS data accurately** by following specific formatting rules.
2. **Generate SHLS-compliant data structures** that follow the exact formatting conventions.
3. **Identify and correct formatting errors** based on SHLS rules to ensure data structure integrity.

### Key Rules of SHLS Formatting

1. **Indexing at the Beginning**:
   - Each SHLS file must start with a complete **index of keys** that will be used in the document. This index defines the structure by listing each key and its hierarchical order, setting up the template for the data that follows.
   - The index separates data fields, subarrays, and nested structures to ensure consistent formatting.
   - This index is required and is crucial for interpreting the data accurately.

2. **Hierarchy Through Indentation**:
   - SHLS relies solely on **indentation** (spaces) to establish hierarchy.
   - Each indentation level represents a new depth in the data hierarchy, replacing symbols like brackets or colons in other formats.

3. **Naming Subarrays Explicitly**:
   - Subarrays must be labeled with a key, as listed in the initial index.
   - When two arrays appear consecutively, this key avoids ambiguity by clearly defining the start of each array.
   - For example, if an employee list is nested within each department in a company structure, each employee array should be labeled with a consistent key like `Employees`.

4. **Values Treated as Strings**:
   - All values in SHLS are initially treated as strings.
   - **Data type interpretation** (e.g., converting `"true"` to a boolean or `"2023-05-15"` to a date) should be handled by an interpreter after parsing. 
   - This helps maintain simplicity within SHLS while allowing for flexible data usage.

5. **Single Space After the Key List**:
   - After the initial key list (index), a single blank line separates the index from the actual data entries.
   - Additional blank spaces within the structure are not allowed as they add no functional value—indentation alone defines structure.

---

### Example Data Structure in SHLS

The following example highlights a three-level hierarchical structure with multiple data types, which the AI should recognize and interpret as strings by default:

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

### Expected Behavior

1. **Parsing**:
   - The AI should recognize and separate the index from data entries.
   - It should interpret hierarchy based on indentation alone, without relying on additional symbols.
   - It should ensure each subarray has a defining key, following the initial index.

2. **Generation**:
   - The AI should create SHLS structures that adhere to these rules, accurately representing hierarchical data in a minimalistic, readable format.
   - Generated data should follow the index-key structure, apply single spacing after the index, and avoid unnecessary blank lines.

3. **Error Handling**:
   - The AI should detect and correct formatting errors, such as missing subarray keys, inconsistent indentation, or missing initial index.
   - It should flag incorrect data types within values if a reinterpretation function is requested.

---

### Summary

By following this prompt, the AI will gain a robust understanding of SHLS formatting, allowing it to parse, generate, and validate SHLS-compliant data structures effectively.
