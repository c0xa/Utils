import psutil
import sys
import json
import zipfile
import datetime
import os
from psutil._common import bytes2human
import xml.etree.ElementTree as ET


MAIN_MENU = ["Info about disk", "Working with a file", "Working with JSON",
                 "Working with XML", "Working with ZIP", "Exit"]

MENU_FILE = ["Create file", "Write string in file", "Read file", "Deleted file", "Main menu"]

MENU_JSON = ["Create JSON", "Write string in JSON", "Read JSON", "Deleted JSON", "Main menu"]

MENU_XML = ["Create XML", "Write string in XML", "Read XML", "Deleted XML", "Main menu"]

MENU_ZIP = ["Create ZIP", "Add file in ZIP", "Read ZIP", "Deleted ZIP", "Main menu"]

def disk_information():
    template = "%-17s %8s %8s %8s %5s%% %9s %s"
    print(template % ("Device", "Total", "Used", "Free", "Use ", "Type",
                   "Mount"))
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        usage = psutil.disk_usage(part.mountpoint)
        print(template % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))


def print_menu(argc):
    for i in range(len(argc)):
        print(i + 1, " " + argc[i])


def work(menu, switch):
    print_menu(menu)
    choose(len(menu), switch)

def work_with_file():
    work(MENU_FILE, switch_work_with_files)


def work_with_json():
    work(MENU_JSON, switch_work_with_json)


def work_with_xml():
    work(MENU_XML, switch_work_with_xml)


def work_with_zip():
    work(MENU_ZIP, switch_work_with_zip)


def create_file():
    print("File name = ", end="")
    file_name = input()
    open(file_name, "w")


def write_string_in_file():
    print("File name = ", end="")
    file_name = input()
    print("String = ", end="")
    string = input()

    try:
        fd = open(file_name, 'w')
        fd.write(string)
    except IOError:
        print("No file")


def read_file():
    print("File name = ", end="")
    file_name = input()

    try:
        fd = open(file_name, 'r')
        print(fd.read())
        fd.close()
    except IOError:
        print("No file")


def deleted_file():
    print("File name = ", end="")
    file_name = input()

    try:
        os.remove(file_name)
    except IOError:
        print("No file")


def switch_work_with_files(value):
    return {
        1: create_file,
        2: write_string_in_file,
        3: read_file,
        4: deleted_file,
        5: main_menu
    }.get(value)


def write_string_in_json():
    print("File name = ", end="")
    file_name = input()

    data = {'URL': 'datacamp.com', 'name': 'Datacamp'}

    try:
        with open(file_name, "w") as write_file:
            json.dump(data, write_file)
    except IOError:
        print("No file")


def read_json():
    print("File name = ", end="")
    file_name = input()

    try:
        with open(file_name, "r") as rf:
            decoded_data = json.load(rf)

        print(decoded_data)
    except IOError:
        print("No file")


def switch_work_with_json(value):
    return {
        1: create_file,
        2: write_string_in_json,
        3: read_json,
        4: deleted_file,
        5: main_menu
    }.get(value)


def write_string_in_xml():
    print("File name = ", end="")
    file_name = input()

    data = ET.Element('parent')
    ET.SubElement(data, 'child1')
    try:
        my_data = ET.tostring(data)
        with open(file_name, "wb") as binary_file:
            binary_file.write(my_data)
    except IOError:
        print("No file")


def read_xml():
    print("File name = ", end="")
    file_name = input()

    try:
        fd = open(file_name, 'r')
        print(fd.read())
        fd.close()
    except IOError:
        print("No file")


def switch_work_with_xml(value):
    return {
        1: create_file,
        2: write_string_in_xml,
        3: read_xml,
        4: deleted_file,
        5: main_menu
    }.get(value)


def create_zip():
    print("Zip name = ", end="")
    zip_name = input()
    try:
        zipfile.ZipFile(zip_name, mode='w', compression=zipfile.ZIP_DEFLATED)
    except Exception:
        print("No file")


def add_file_in_zip():
    print("File name = ", end="")
    file_name = input()

    print("Zip name = ", end="")
    zip_name = input()
    try:
        with zipfile.ZipFile(zip_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_name)
    except Exception:
        print("No file")


def read_zip():
    print("File name = ", end="")
    file_name = input()

    try:
        with zipfile.ZipFile(file_name, mode='a') as zf:
            for file in zf.infolist():
                date = datetime.datetime(*file.date_time)
                name = os.path.basename(file.filename)
                print(f"{name},\t{file.file_size},\t{file.compress_size},\t \
                                       {date.strftime('%H:%M %d.%m.%Y')}")
    except Exception:
        print("No file")


def switch_work_with_zip(value):
    return {
        1: create_zip,
        2: add_file_in_zip,
        3: read_zip,
        4: deleted_file,
        5: main_menu
    }.get(value)


def main_menu():
    print_menu(MAIN_MENU)
    choose(len(MAIN_MENU), switch_main_menu)


def choose(count_action, func):
    flag = True
    while flag:
        try:
            print("Action = ", end="")
            number_action = int(input())
            flag = False
        except Exception:
            print('Wrong number')
    if number_action <= count_action:
        try:
            print("_" * 100)
            func(number_action)()
            print("_" * 100)
            choose(count_action, func)
        except KeyError as e:
            raise ValueError('Undefined unit: {}'.format(e.args[0]))


def switch_main_menu(value):
    return {
        1: disk_information,
        2: work_with_file,
        3: work_with_json,
        4: work_with_xml,
        5: work_with_zip,
        6: sys.exit
    }.get(value)

if __name__ == '__main__':
    main_menu()
