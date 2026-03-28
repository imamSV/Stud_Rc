import pytest
import csv
from src.reports import get_report, MedianCoffeeReport
from src.main import load_data


@pytest.fixture
def sample_csv(tmp_path):
    file_path = tmp_path / "test_data.csv"
    data = [
        {"student": "Иван Кузнецов", "coffee_spent": "600", "exam": "Математика"},
        {"student": "Иван Кузнецов", "coffee_spent": "700", "exam": "Математика"},
        {"student": "Иван Кузнецов", "coffee_spent": "800", "exam": "Математика"},
        {"student": "Мария Соколова", "coffee_spent": "150", "exam": "Математика"}
    ]
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return str(file_path)


def test_load_data_success(sample_csv):
    data = load_data([sample_csv])
    assert len(data) == 4
    assert data[0]["student"] == "Иван Кузнецов"


def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data(["non_existent_file.csv"])


def test_median_coffee_report_logic():
    data = [
        {"student": "Алексей", "coffee_spent": "100"},
        {"student": "Алексей", "coffee_spent": "200"},
        {"student": "Алексей", "coffee_spent": "300"},  # медиана: 200
        {"student": "Дарья", "coffee_spent": "500"},
        {"student": "Дарья", "coffee_spent": "600"}  # медиана: 550
    ]
    report = MedianCoffeeReport()
    result = report.generate(data)

    assert result[0] == ["Дарья", 550]
    assert result[1] == ["Алексей", 200]


def test_get_report_valid():
    report = get_report("median-coffee")
    assert isinstance(report, MedianCoffeeReport)


def test_get_report_invalid():
    with pytest.raises(ValueError):
        get_report("unknown-report")