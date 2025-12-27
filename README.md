# IMEI Registration System (Python + Qt Designer / PyQt5)

This project is built with **Python** and **Qt Designer (PyQt5)** (learned during my secondary education).  
It’s a desktop GUI application used to register devices imported from abroad by saving the **IMEI** and its details, while blocking invalid IMEIs.

## How it works
1. The user enters the device information:
   - IMEI
   - Passport number
   - Year
   - Brand
   - Category (4G / 5G)

2. Validation rules (error messages appear in the GUI):
   - **IMEI must be exactly 15 digits** (numbers only)  
     📸 *Screenshot: IMEI 15 digits error*
   - **Passport must be exactly 8 characters** and **alphanumeric** (letters + digits only)  
     📸 *Screenshot: Passport invalid error*
   - **Year must not be empty**  
     📸 *Screenshot: Year missing error*
   - **Brand must be selected** (not “Choose a brand”)  
     📸 *Screenshot: Brand selection error*

3. After basic checks, the program verifies the IMEI using the **Luhn algorithm**:
   - If the IMEI **fails Luhn** → the device is **blocked** and appended to `blocage.txt`
   - If the IMEI **passes Luhn**:
     - If the IMEI already exists → an error message appears (“already registered”)
     - Otherwise → the device is **authorized** and saved to `IMEI_V.dat` (binary file using `pickle`)

## Features
- Add new devices with full validation
- Block invalid IMEIs and store them in a text file (`blocage.txt`)
- Save authorized devices in a binary database (`IMEI_V.dat`)
- Display authorized devices in a table
- Sort authorized devices by:
  - Brand
  - Year
  - Brand then Year
- Display blocked devices from `blocage.txt`

## Files
- `imei.ui` : GUI design (Qt Designer)
- `imei-project.py` : Python/PyQt5 application logic
- `IMEI_V.dat` : Authorized devices database (binary / pickle)
- `blocage.txt` : Blocked devices log (text)

## Tech Stack
- Python
- PyQt5
- Qt Designer
- pickle (for binary storage)
