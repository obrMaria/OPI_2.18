#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import json
import os.path
import sys


def show_add(students, name, groop, marks):
    """
    Добавить данные о студенте
    """
    # Добавить данные о студенте
    students.append(
        {"name": name, "groop": groop, "marks": [int(i) for i in marks.split()]}
    )
    return students


def show_display(students):
    """
    Вывести данные о студентах.
    """
    # Заголовок таблицы.
    line = "+-{}-+-{}-+-{}-+".format("-" * 30, "-" * 20, "-" * 9)
    print(line)
    print("| {:^30} | {:^20} | {:^9} |".format("Ф.И.О.", "Группа", "Оценки"))
    print(line)

    for student in students:
        print(
            "| {:<30} | {:<20} | {:>7} |".format(
                student.get("name", ""),
                student.get("groop", ""),
                ",".join(map(str, student["marks"])),
            )
        )
    print(line)


def show_select(students):
    """
    Выбрать студентов со средним баллом не ниже 4.
    """
    result = []
    for student in students:
        res = all(int(x) > 3 for x in student["marks"])
        if res:
            result.append(student)
    return result


def help():
    """
    Вывести список комманд
    """
    print("Список команд:\n")
    print("add - добавить студента;")
    print("display - вывести список студентов;")
    print("select - запросить студентов с баллом выше 4.0;")
    print("save - сохранить список студентов;")
    print("load - загрузить список студентов;")
    print("exit - завершить работу с программой.")


def save_students(file_name, students):
    """
    Сохранить всех студентов в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    """
    Загрузить всех студентов из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    """
    Главная функция программы.
    """
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument("-d", "--data", action="store", help="The data file name")

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version", action="version", help="The main parser", version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления студента.
    add = subparsers.add_parser("add", parents=[file_parser], help="Add a new student")
    add.add_argument(
        "-n", "--name", action="store", required=True, help="The student's name"
    )
    add.add_argument("-g", "--groop", action="store", help="The student's group")
    add.add_argument(
        "-m", "--marks", action="store", required=True, help="The student's marks"
    )

    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all students"
    )

    # Создать субпарсер для выбора студентов.
    _ = subparsers.add_parser(
        "select", parents=[file_parser], help="Select the students"
    )
    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    data_file = args.data
    if not data_file:
        data_file = os.environ.get("STUDENTS_DATA")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    # Загрузить всех студентов из файла, если файл существует.
    is_dirty = False
    if os.path.exists(data_file):
        students = load_students(data_file)
    else:
        students = []

    # Добавить студента.

    if args.command == "add":
        students = show_add(students, args.name, args.groop, args.marks)
        if len(students) > 1:
            students.sort(key=lambda item: sum(item["marks"]) / len(item["marks"]))

        is_dirty = True
    # Отобразить всех студентов.
    elif args.command == "display":
        show_display(students)
    # Выбрать требуемых студентов.
    elif args.command == "select":

        selected = show_select(students)
        show_display(selected)
    # Сохранить данные в файл, если список студентов был изменен.
    if is_dirty:
        save_students(data_file, students)


if __name__ == "__main__":
    main()