import datetime
import math
import os
import unittest

import pandas as pd

from services import CandlestickChart
from tests.recipes import test_data


class TestCandlestickChart(unittest.TestCase):
    """
    Testing CandlestickChart.
    """
    @classmethod
    def setUp(cls) -> None:
        cls.test_data_file = "test_prices.csv"
        test_df = pd.DataFrame(test_data)
        test_df.to_csv(cls.test_data_file, index=False)

    @classmethod
    def tearDown(cls) -> None:
        os.remove(cls.test_data_file)

    def test_calculate_candlestick_data(self) -> None:
        """
        Tests the candles calculation.
        """
        chart = CandlestickChart(self.test_data_file, "1H", 14)
        chart.calculate_candlestick_data_and_ema()
        self.assertFalse(
            chart.candlestick_df.empty, "There are no candles values."
        )

    def test_calculate_ema(self) -> None:
        """
        Tests the EMA calculation.
        """
        chart = CandlestickChart(self.test_data_file, "1H", 14)
        chart.calculate_candlestick_data_and_ema()
        self.assertTrue(
            "EMA" in chart.candlestick_df.columns, "The EMA column is missing."
        )
        self.assertFalse(
            chart.candlestick_df["EMA"].empty, "There are no EMA values."
        )

    def test_candles_count(self) -> None:
        """
        Tests the correctness of the number of received candles.
        """
        test_tuple = (("minutes", "T", 5), ("hours", "H", 1), ("days", "D", 1))
        for period, abbreviation, value in test_tuple:
            with self.subTest(
                period=period, abbreviation=abbreviation, value=value
            ):
                chart = CandlestickChart(
                    self.test_data_file, f"{value}{abbreviation}", 14
                )
                chart.calculate_candlestick_data_and_ema()
                expected_count = math.ceil(
                    (chart.df.index[-1] - chart.df.index[0])
                    / datetime.timedelta(**{period: value})
                )
                self.assertEqual(
                    expected_count,
                    len(chart.candlestick_df),
                    "The resulting number of candles "
                    "does not match the expected.",
                )
