"""
SAJALNI – IMEI Registration System (PyQt5)

PROGRAM CONCEPT
- The user enters: IMEI, Passport, Year, Brand, Category (4G/5G) in a GUI.
- If the device data is valid, it is SAVED in: IMEI_V.dat  (binary file using pickle).
- If the device data is invalid, it is SAVED in: blocage.txt (text file).

GUI BUTTONS
- Add: validate then save (authorized or blocked)
- Show: display authorized devices in a table (optionally sorted)
- Blocked: display blocked devices from blocage.txt
"""

from pickle import dump, load
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
file = open("IMEI_V.dat", "ab")


# ------------------------------------------------------------
# Function: Check if a string contains only letters (A-Z) or digits (0-9)
# Why? Passport must not contain spaces/symbols like @, -, etc.
# ------------------------------------------------------------
def is_alphanumeric(text):
    index = 0
    valid = True
    while valid and index < len(text):
        # HARD LINE: accept ONLY letters or digits, reject everything else
        if not ('A' <= text[index].upper() <= 'Z' or '0' <= text[index] <= '9'):
            valid = False
        else:
            index += 1
    return valid


# ------------------------------------------------------------
# Function: Validate an IMEI using LUHN algorithm 
# HARD CONCEPT (LUHN):
# - Some digits are doubled 
# - If doubling makes number >= 10 => subtract 9
# - Sum all digits, valid if sum % 10 == 0
# ------------------------------------------------------------
def check_luhn(imei):
    total = 0
    for i in range(len(imei)):
        if i % 2 == 0:
            doubled = int(imei[i]) * 2
            if doubled >= 10:
                total += doubled - 9
            else:
                total += doubled
        else:
            total += int(imei[i])
    return total % 10 == 0


# ------------------------------------------------------------
# Function: Bubble sort 
# HARD CONCEPT:
# - Compare adjacent items and swap if order is wrong
# - Repeat until no swaps occur
# - If key2 != "" then key2 is used when key1 values are equal
# ------------------------------------------------------------
def bubble_sort(records, size, key1, key2):
    swapped = True
    while swapped:
        swapped = False
        for i in range(size - 1):
            condition = records[i][key1] > records[i + 1][key1]

            # HARD LINE: secondary sort key when primary fields are equal
            if key2 != "":
                condition = condition or (
                    records[i][key1] == records[i + 1][key1]
                    and records[i][key2] > records[i + 1][key2]
                )

            if condition:
                swapped = True
                temp = records[i]
                records[i] = records[i + 1]
                records[i + 1] = temp


# ------------------------------------------------------------
# Function: Check if IMEI already exists in IMEI_V.dat
# HARD CONCEPT:
# IMEI_V.dat stores many pickle records. We keep loading until EOF happens.
# The "try/except" is used to stop when the file ends.
# ------------------------------------------------------------
def imei_exists(imei):
    file = open("IMEI_V.dat", "rb")
    end_of_file = False
    found = False

    while not end_of_file and not found:
        try:
            record = load(file)
            if record["imei"] == imei:
                found = True
        except:
            # HARD LINE: when pickle reaches end of file (EOF), it throws an error
            end_of_file = True

    file.close()
    return found


# ------------------------------------------------------------
# Function: Count how many records exist in IMEI_V.dat
# ------------------------------------------------------------
def count_devices():
    file = open("IMEI_V.dat", "rb")
    end_of_file = False
    count = 0

    while not end_of_file:
        try:
            _ = load(file)
            count += 1
        except:
            end_of_file = True

    file.close()
    return count


# ------------------------------------------------------------
# Function: Display authorized devices in the table
# - Reads all records from IMEI_V.dat
# - Optional sort by brand/year using bubble_sort
# - Fills the QTableWidget
# ------------------------------------------------------------
def display_devices():
    sort_brand = w.sort_brand.isChecked()
    sort_year = w.sort_year.isChecked()

    total = count_devices()
    devices = [dict()] * total

    file = open("IMEI_V.dat", "rb")
    for i in range(total):
        devices[i] = dict()
        devices[i] = load(file)
    file.close()

    # Same decision logic as your code (no changes)
    if sort_brand and sort_year:
        key1 = "brand"
        key2 = "year"
    elif sort_brand and not sort_year:
        key1 = "brand"
        key2 = ""
    elif sort_year and not sort_brand:
        key1 = "year"
        key2 = ""
    else:
        key1 = ""
        key2 = ""

    if key1 != "":
        bubble_sort(devices, total, key1, key2)

    # Fill the GUI table
    w.table.setRowCount(0)
    for i in range(total):
        w.table.insertRow(i)
        w.table.setItem(i, 0, QTableWidgetItem(devices[i]["imei"]))
        w.table.setItem(i, 1, QTableWidgetItem(devices[i]["passport"]))
        w.table.setItem(i, 2, QTableWidgetItem(devices[i]["year"]))
        w.table.setItem(i, 3, QTableWidgetItem(devices[i]["brand"]))
        w.table.setItem(i, 4, QTableWidgetItem(devices[i]["category"]))


# ------------------------------------------------------------
# Function: Display blocked devices from blocage.txt
# ------------------------------------------------------------
def display_blocked():
    file = open("blocage.txt", "r")
    content = file.read()
    w.blocked.setText(content[:-1])
    file.close()


# ------------------------------------------------------------
# Function: Add a device
# - Reads user input from GUI
# - Validates IMEI (digits + length + LUHN)
# - Validates passport (length + alphanumeric)
# - Checks IMEI uniqueness
# - Saves to IMEI_V.dat if valid, else blocage.txt
# ------------------------------------------------------------
def add_device():
    imei = w.imei.text()
    passport = w.passport.text()
    year = w.year.text()
    brand = w.brand.currentText()

    # Category selection (same logic: if not 4G => 5G)
    if w.cat_4g.isChecked():
        category = "4G"
    else:
        category = "5G"

    device = {
        "imei": imei,
        "passport": passport,
        "year": year,
        "brand": brand,
        "category": category
    }

    # IMEI must be 15 digits + LUHN valid
    if len(imei) != 15 or not imei.isdigit() :
        QMessageBox.critical(w,"error","IMEI code should be composed of 15 digits")
    # Passport must be 8 characters and only letters/digits
    elif len(passport) != 8 or not is_alphanumeric(passport):
        QMessageBox.critical(w,"error","Passport number is invalid")
    
    elif (len(year)==0):
         QMessageBox.critical(w,"error","Add the year")
    elif brand=="Choose a brand":
        QMessageBox.critical(w,"error","Choose a brand")
    # IMEI must be unique in authorized file
    elif imei_exists(imei):
        QMessageBox.critical(w,"error","The device is already registered")

    elif not check_luhn(imei):
        file = open("blocage.txt", "a")
        file.write(f"{passport} {imei} {year} {brand} {category}\n")
        file.close()
        QMessageBox.critical(w,"error","IMEI code is invalid, device unauthorised")
    else:
        file = open("IMEI_V.dat", "ab")
        dump(device, file)
        file.close()
        QMessageBox.information(w,"done","the device was added successfully")


# ============================================================
# MAIN PROGRAM (GUI START)
# ============================================================
app = QApplication([])
w = loadUi("imei.ui")
w.show()

# Connect GUI buttons to functions
w.add_btn.clicked.connect(add_device)
w.show_btn.clicked.connect(display_devices)
w.blocked_btn.clicked.connect(display_blocked)

app.exec_()
