import os
import re

from services import CandlestickChart


def get_data_file_path() -> str:
    while True:
        file_path = input(
            "Введите имя .csv файла с данными (например, 'prices.csv'): "
        )
        if re.match(r"^.+\.csv$", file_path) and os.path.isfile(file_path):
            return file_path
        else:
            print(
                "Некорректное расширение файла либо файл не найден. "
                "Пожалуйста, укажите корректное имя файла."
            )


def get_interval() -> str:
    while True:
        interval_input: str = input(
            "Введите интервал свечей "
            "(например, '5T' для 5 минут, '1H' для 1 часа, '1D' для 1 дня): "
        )
        if re.match(r"^[1-9][THD]$", interval_input):
            return interval_input
        else:
            print(
                "Некорректный формат интервала. "
                "Пожалуйста, введите корректный интервал."
            )


def get_ema_period() -> int:
    while True:
        try:
            period: int = int(
                input("Введите количество периодов EMA (от 7 до 200): ")
            )
            if 7 <= period <= 200:
                return period
            raise ValueError
        except ValueError:
            print(
                "Некорректное значение. Пожалуйста, введите число от 7 до 200."
            )


if __name__ == "__main__":
    data_file_path = get_data_file_path()
    time_interval = get_interval()
    ema_period = get_ema_period()

    chart = CandlestickChart(data_file_path, time_interval, ema_period)
    chart.calculate_candlestick_data_and_ema()
    chart.save_result_csv()
    chart.plot_candlestick_chart()
