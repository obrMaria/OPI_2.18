#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import argparse
import json
import sys
import os.path
from dotenv import load_dotenv


def get_student(students, name, group, marks):
    """
    Добавить данные о студенте.
    """
    # Создать словарь.
    students.append(
        {
            'name': name,
            'group': group,
            'marks': [int(i) for i in marks.split()]
        }
    )

    return students


def display_students(students):
    """
    Отобразить список студентов.
    """
    # Проверить, что список студентов не пуст.
    if students:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Оценки"
            )
        )
        print(line)
        # Вывести данные о всех студентах.
        for idx, student in enumerate(students, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    ','.join(map(str, student['marks']))
                )
            )
        print(line)
    else:
        print("список студентов пуст")


def find_students(students):
    """
    Выбрать студентов со ср ариф. успеваемости >4.
    """
    result = []
    count = 0
    for student in students:
        marks = student.get('marks', '')
        if sum(marks) / (len(marks)) >= 4.0:
            result.append(student)
            count += 1

    return result


def save_students(file_name, students):
    """
    Сохранить всех студентов в файл JSON.
    """

    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(students, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    """
    Загрузить всех студентов из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        loaded = json.load(fin)
    return loaded


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d", "--data", action="store", required=False, help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления студента.
    add = subparsers.add_parser("add", parents=[file_parser], help="Add a new student")
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The student's name"
    )

    add.add_argument(
        "-g",
        "--group",
        action="store",
        help="The student's group"
    )

    add.add_argument(
        "-m",
        "--marks",
        action="store",
        required=True,
        help="The student's marks"
    )

    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all students"
    )

    # Создать субпарсер для поиска студентов.
    _ = subparsers.add_parser(
        "find",
        parents=[file_parser],
        help="find the students"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Подключение к окружению
    data_file = args.data
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    if not data_file:
        data_file = os.getenv("STUDENTS")
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
        students = get_student(
            students,
            args.name,
            args.group,
            args.marks
        )
        if len(students) > 1:
            students.sort(key=lambda item: sum(item["marks"]) / len(item["marks"]))
        is_dirty = True

    # Отобразить всех студентов.
    elif args.command == "display":
        display_students(students)

    # Выбрать требуемых студентов.
    elif args.command == "find":
        found = find_students(students)
        display_students(found)

    # Сохранить данные в файл, если список студентов был изменен.
    if is_dirty:
        save_students(data_file, students)


if __name__ == '__main__':
    main()
