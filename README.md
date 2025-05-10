# Invoice Generator

This is a simple desktop application built with Python and Tkinter to help you generate printable invoices in PDF format. It supports Arabic language and calculates totals, discounts, and final amounts.

## Features

* Add products with quantity and price.
* Automatically calculate total for each product.
* Apply a discount percentage.
* Generate an invoice in Arabic as a PDF file.
* Clean and user-friendly interface.
* Supports right-to-left text rendering.

## Requirements

* Python 3.7+
* All required libraries are listed in `requirements.txt`

## Setup Instructions

Follow these steps to run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/nmys9/Invoice-Generator.git
cd Invoice-Generator
```

### 2. Create a Virtual Environment (Recommended)

It's best to work in a virtual environment to avoid conflicts:

```bash
# For Windows
python -m venv env
env\Scripts\activate

# For macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

Install all required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Once everything is installed, run the main Python file:

```bash
python app.py
```

Make sure you have the Arabic font file `Amiri-Regular.ttf` in the project directory, as it is required to render Arabic text correctly in the PDF.

## Output

The generated invoice will be saved as `فاتورة.pdf` in the same directory.

## License

This project is open-source and available for educational and personal use.
