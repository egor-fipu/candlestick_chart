from typing import List, Union

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc


class CandlestickChart:
    """
    Класс для создания графика свечей
    с экспоненциальной скользящей средней (EMA).

    Args:
        data_file_path (str): Имя файла с данными.
        interval_input (str): Интервал свечей
            (например, '5T' для 5 минут, '1H' для 1 часа, '1D' для 1 дня).
        ema_period (int): Период для расчета EMA (от 7 до 200).

    Attributes:
        df (pd.DataFrame): DataFrame для хранения данных из файла.
        candlestick_df (pd.DataFrame): DataFrame для хранения свечей.
        interval_input (str): Интервал свечей.
        time_interval (pd.Timedelta): Временной интервал для свечей.
        ema_period (int): Период для расчета EMA.

    Methods:
        prepare_df(data_file: str) -> pd.DataFrame: Загружает данные из файла
            и подготавливает DataFrame.
        calculate_candlestick_data_ema(): Рассчитывает данные для свечей
            на основе временного интервала и EMA.
        save_result_csv(): Сохраняет результат в CSV файл.
        plot_candlestick_chart(): Строит график свечей с EMA.
    """

    def __init__(
        self, data_file_path: str, interval_input: str, ema_period: int
    ) -> None:
        self.df = self.prepare_df(data_file_path)
        self.candlestick_df: pd.DataFrame = pd.DataFrame(
            columns=["Open", "High", "Low", "Close"]
        )
        self.interval_input: str = interval_input
        self.time_interval: pd.Timedelta = pd.Timedelta(interval_input)
        self.ema_period: int = ema_period

    def prepare_df(self, data_file: str) -> pd.DataFrame:
        """
        Загружает данные из файла и подготавливает DataFrame.
        """
        df: pd.DataFrame = pd.read_csv(data_file, parse_dates=["TS"])
        df.set_index("TS", inplace=True)
        df.sort_index(inplace=True)
        return df

    def calculate_candlestick_data_and_ema(self) -> None:
        """
        Рассчитывает данные для свечей на основе временного интервала.
        Рассчитывает экспоненциальную скользящую среднюю (EMA).
        """
        start_time = self.df.index[0]
        close_price = 0
        while start_time <= self.df.index[-1]:
            end_time = start_time + self.time_interval
            data_in_interval = self.df[start_time:end_time]
            if not data_in_interval.empty:
                open_price = data_in_interval["PRICE"].iloc[0]
                high_price = data_in_interval["PRICE"].max()
                low_price = data_in_interval["PRICE"].min()
                close_price = data_in_interval["PRICE"].iloc[-1]
            else:
                open_price = close_price
                high_price = close_price
                low_price = close_price
                close_price = close_price
            self.candlestick_df.loc[start_time] = [
                open_price,
                high_price,
                low_price,
                close_price,
            ]
            start_time = end_time

        self.candlestick_df["EMA"] = (
            self.candlestick_df["Close"].ewm(span=self.ema_period).mean()
        )

    def save_result_csv(self) -> None:
        self.candlestick_df.to_csv("result.csv", index_label="Timestamp")

    def plot_candlestick_chart(self) -> None:
        """
        Строит график свечей с экспоненциальной скользящей средней (EMA).
        """
        candlestick_data: List[
            List[Union[float, float, float, float, float]]
        ] = [
            [
                mdates.date2num(timestamp),
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
            ]
            for timestamp, row in self.candlestick_df.iterrows()
        ]

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=10))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        candlestick_ohlc(
            ax, candlestick_data, width=0.0005, colorup="g", colordown="r"
        )
        plt.plot(
            self.candlestick_df.index,
            self.candlestick_df["EMA"],
            label=f"EMA-{self.ema_period}",
        )
        plt.title(
            f"Candlestick Chart with EMA ({self.interval_input} interval)"
        )
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.xticks(rotation=45)
        fig.subplots_adjust(bottom=0.2)
        plt.legend()
        plt.show()
