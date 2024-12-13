# ZIP Checksum Comparator

## Overview

`ZIP Checksum Comparator` is a Python-based GUI tool for comparing the contents of two ZIP files. It computes and compares MD5 checksums for all files within the ZIP archives, helping you verify if their contents are identical or if there are discrepancies.

## Features

- Compare the contents of two ZIP files using MD5 checksums.
- Identify missing files, mismatched content, or identical contents between ZIP files.
- User-friendly GUI built with Tkinter.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sylar-my/zip-checksum-comparator.git
   cd zip-checksum-comparator
   ```

2. **Install the required dependencies**:
   This script uses Python's standard library and does not require additional dependencies.

3. **Run the application**:
   ```bash
   python zip-checksum-comparator.py
   ```

## Usage

1. Launch the application by running the script.
2. Use the "Browse" buttons to select the two ZIP files you want to compare.
3. Click on the "Compare ZIP Contents" button.
4. The results will be displayed in the results section, highlighting any differences or confirming identical contents.

## Screenshot

![Screenshot_20241213_234641](https://github.com/user-attachments/assets/8115c508-eed4-43b8-8234-61a5cead5042)


## How It Works

- **Checksum Calculation**:
  The tool computes MD5 checksums for all files inside each ZIP archive.

- **Comparison**:
  It compares filenames and checksums between the two ZIP files to detect discrepancies.

- **Output**:
  Displays a detailed report in the results section, listing missing files, content differences, or confirming identical contents.

## Requirements

- Python 3.6 or higher
- Tkinter (comes pre-installed with Python on most systems)

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

- **sylar-my** 

## Acknowledgments

- Inspired by the need for reliable file comparison tools.

---

*Feel free to reach out with any questions or feedback!*
