import argparse
import csv
import sys
import os
from typing import List, Dict
from tabulate import tabulate
from src.reports import get_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Генератор отчетов по студентам")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к CSV файлам с данными"
    )
    parser.add_argument(
        "--report",
        type=str,
        required=True,
        help="Название отчета (например, median-coffee)"
    )
    return parser.parse_args()


def load_data(file_paths: List[str]) -> List[Dict[str, str]]:
    combined_data = []
    for path in file_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл не найден: {path}")

        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                combined_data.append(row)
    return combined_data


def main():
    args = parse_args()
    try:
        report_strategy = get_report(args.report)

        data = load_data(args.files)
        if not data:
            print("Переданные файлы пусты.")
            return
        report_data = report_strategy.generate(data)
        print(tabulate(report_data, headers=report_strategy.columns, tablefmt="rst"))

    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()