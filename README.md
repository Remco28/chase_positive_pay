# Chase Positive Pay CSV Validator

A simple utility to validate that a CSV file conforms to the Chase Bank Positive Pay standard. It checks for common errors such as incorrect field counts, invalid data formats, duplicate check numbers, and provides a summary report for valid files.

## How to Run

There are two ways to run the validator:

### 1. Using the Executable (Recommended)

The easiest method is to use the standalone executable:

1.  Navigate to the `dist` folder.
2.  Double-click `check_validator.exe`.

This requires no installation and can be run on any Windows machine.

### 2. Using the VBS Script

If you have Python installed, you can use the VBS script. This method may have slightly lower overhead.

1.  Double-click `run_validator.vbs` in the main project folder.

This will launch the validator GUI. This method requires a working Python installation.

## Features

*   **Simple GUI:** Easily select your CSV file.
*   **Detailed Validation:** Checks for a wide range of formatting and data errors.
*   **Clear Reports:** If errors are found, a detailed list is provided with line numbers.
*   **Success Summary:** For valid files, a summary report is displayed with totals and check counts.
*   **Save Errors:** Error reports can be saved to a text file for review.
