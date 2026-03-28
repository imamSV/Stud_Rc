import statistics
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from collections import defaultdict


class BaseReport(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def columns(self) -> List[str]:
        pass

    @abstractmethod
    def generate(self, data: List[Dict[str, str]]) -> List[List[Any]]:
        pass


class MedianCoffeeReport(BaseReport):
    @property
    def name(self) -> str:
        return "median-coffee"

    @property
    def columns(self) -> List[str]:
        return ["student", "median_coffee"]

    def generate(self, data: List[Dict[str, str]]) -> List[List[Any]]:
        student_coffee = defaultdict(list)

        for row in data:
            student = row["student"]
            coffee_spent = float(row["coffee_spent"])
            student_coffee[student].append(coffee_spent)

        result = []
        for student, expenses in student_coffee.items():
            med = statistics.median(expenses)
            if med.is_integer():
                med = int(med)
            result.append([student, med])

        result.sort(key=lambda x: x[1], reverse=True)
        return result


REPORT_REGISTRY: Dict[str, BaseReport] = {
    "median-coffee": MedianCoffeeReport()
}

def get_report(report_name: str) -> BaseReport:
    report = REPORT_REGISTRY.get(report_name)
    if not report:
        raise ValueError(
            f"Отчет '{report_name}' не найден. "
            f"Доступные отчеты: {', '.join(REPORT_REGISTRY.keys())}"
        )
    return report