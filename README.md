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
     (https://github.com/bouka06/imei-registration-project/blob/1cc7c79e561bb37a3d69990036b72949d7d741bd/Screenshot%202025-12-27%20171142.png)
   - **Passport must be exactly 8 characters** and **alphanumeric** (letters + digits only)  
     (https://github.com/bouka06/imei-registration-project/blob/11125e600f679cf83a33a70b36e167ab154a8f6a/Screenshot%202025-12-27%20171206.png)
   - **Year must not be empty**  
   - **Brand must be selected** (not “Choose a brand”)  
     

3. After basic checks, the program verifies the IMEI using the **Luhn algorithm**:
   - If the IMEI **fails Luhn** → the device is **blocked** and appended to `blocage.txt`
   - (https://github.com/bouka06/imei-registration-project/blob/2747f6ba92b299030787b56869ed869623db51b6/Screenshot%202025-12-27%20171224.png)
   - If the IMEI **passes Luhn**:
     - If the IMEI already exists → an error message appears (“already registered”)
     - (https://github.com/bouka06/imei-registration-project/blob/18387ce5ba634e4ee44242290969982828558a23/Screenshot%202025-12-27%20174359.png)
     - Otherwise → the device is **authorized** and saved to `IMEI_V.dat` (binary file using `pickle`)
     - (https://github.com/bouka06/imei-registration-project/blob/0df0280b9407e80bde043e139200c64815d3c82f/Screenshot%202025-12-27%20171247.png)
    
   - (https://github.com/bouka06/imei-registration-project/blob/deb3fd08808e7fdd0e02497518de4e5122920689/Screenshot%202025-12-27%20190502.png)

## Features
- Add new devices with full validation
- Block invalid IMEIs and store them in a text file (`blocage.txt`)
- Save authorized devices in a binary database (`IMEI_V.dat`)
- Display unauthorized devices in a list
  ()
- Display authorized devices in a table
(https://github.com/bouka06/imei-registration-project/blob/5f9b1b8ef951d392a5f4996daacd00c0deb62496/Screenshot%202025-12-27%20185012.png)
(https://github.com/bouka06/imei-registration-project/blob/5f9b1b8ef951d392a5f4996daacd00c0deb62496/Screenshot%202025-12-27%20185650.png)
- Sort authorized devices by:
  - Brand
  - Year
  - Brand then Year
- Display blocked devices from `blocage.txt`
- (https://github.com/bouka06/imei-registration-project/blob/e934a73f25cf9783ccb67b88d36489b8ed59e4d0/Screenshot%202025-12-27%20171304.png)

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



